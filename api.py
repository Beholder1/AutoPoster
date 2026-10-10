import base64
import json
import os
import sys
import tempfile
from contextlib import contextmanager

import requests


def _app_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def _resolve_base_url():
    env = os.environ.get("AUTOPOSTER_API_URL")
    if env:
        return env.rstrip("/")
    path = os.path.join(_app_dir(), "api_url.txt")
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            content = f.read().strip()
        if content:
            return content.rstrip("/")
    raise RuntimeError(
        "Brak adresu backendu: ustaw zmienną AUTOPOSTER_API_URL "
        "albo wpisz go do pliku api_url.txt obok aplikacji."
    )


def _session_path():
    return os.path.join(_app_dir(), "session.txt")


def _settings_path():
    return os.path.join(_app_dir(), "settings.json")


class AuthError(Exception):
    """Brak/wygasla sesja — trzeba pokazac okno logowania."""


class Api:
    """Klient backendu auto-poster. Utrzymuje powierzchnie metod starej klasy
    Database (fetch/getA/update/...), zeby strony UI i skrypty dzialaly bez zmian."""

    def __init__(self, base_url=None):
        self.base_url = base_url or _resolve_base_url()
        self.http = requests.Session()
        self.user_email = None
        self._script_accounts = None  # cache: konta z odszyfrowanymi haslami
        self._script_products = None  # cache: produkty z categoryIds/imageIds
        self._categories = None       # cache: wspolny slownik (id, name)
        self._tmp_dir = None

    # --- HTTP ---

    def _request(self, method, path, **kwargs):
        try:
            response = self.http.request(method, self.base_url + path, timeout=60, **kwargs)
        except requests.ConnectionError as e:
            raise RuntimeError(f"Brak połączenia z backendem ({self.base_url}): {e}") from e
        if response.status_code == 401:
            raise AuthError("Sesja wygasła albo brak zalogowania")
        if not response.ok:
            if response.status_code == 413:
                raise RuntimeError(f"Błąd API 413: {method} {path} — za duży upload "
                                   f"(limit serwera na zdjęcia/żądanie)")
            detail = " ".join(response.text[:200].split())
            raise RuntimeError(f"Błąd API {response.status_code}: {method} {path}"
                               + (f" — {detail}" if detail else ""))
        return response

    def _get(self, path, **kwargs):
        return self._request("GET", path, **kwargs)

    def _invalidate(self):
        self._script_accounts = None
        self._script_products = None

    # --- logowanie / sesja ---

    def login(self, email, password):
        """Zwraca True przy poprawnych danych; zapisuje token do session.txt."""
        response = self.http.post(self.base_url + "/api/auth/login",
                                  json={"email": email, "password": password, "rememberMe": True},
                                  timeout=60)
        if response.status_code == 401:
            return False
        if not response.ok:
            raise RuntimeError(f"Błąd logowania: HTTP {response.status_code}")
        token = response.headers.get("Authorization")
        if not token:
            raise RuntimeError("Backend nie zwrócił tokenu")
        self.http.headers["Authorization"] = "Bearer " + token
        self.user_email = response.json().get("email", email)
        with open(_session_path(), "w", encoding="utf-8") as f:
            f.write(token + "\n" + self.user_email)
        return True

    def register(self, email, password):
        response = self.http.post(self.base_url + "/api/auth/register",
                                  json={"email": email, "password": password}, timeout=60)
        if not response.ok:
            raise ValueError("Rejestracja nieudana (email zajęty albo błąd serwera)")

    def resume_session(self):
        """Wznawia sesje z session.txt; zwraca True gdy token nadal dziala."""
        path = _session_path()
        if not os.path.isfile(path):
            return False
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
        if not lines or not lines[0].strip():
            return False
        self.http.headers["Authorization"] = "Bearer " + lines[0].strip()
        self.user_email = lines[1].strip() if len(lines) > 1 else None
        try:
            self._get("/api/accounts")  # tania weryfikacja tokenu
            return True
        except AuthError:
            self.http.headers.pop("Authorization", None)
            os.remove(path)
            return False

    def logout(self):
        # JWT jest bezstanowy — wylogowanie to usuniecie tokenu lokalnie
        self.http.headers.pop("Authorization", None)
        self.user_email = None
        path = _session_path()
        if os.path.isfile(path):
            os.remove(path)

    # --- ustawienia i profile Chrome (lokalne, per maszyna) ---

    def _read_settings(self):
        try:
            with open(_settings_path(), encoding="utf-8") as f:
                return json.load(f)
        except (OSError, ValueError):
            return {}

    def get_setting(self, key, default=None):
        return self._read_settings().get(key, default)

    def set_setting(self, key, value):
        settings = self._read_settings()
        settings[key] = str(value)
        with open(_settings_path(), "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)

    def get_or_create_profile(self, account, profiles_dir):
        profile = self.get_setting("profile." + account)
        if profile and os.path.isdir(os.path.join(profiles_dir, profile)):
            return profile
        return account

    # --- konta ---

    def _accounts(self):
        if self._script_accounts is None:
            self._script_accounts = self._get("/api/script/accounts").json()["accounts"]
        return self._script_accounts

    def _account_by_name(self, name):
        for account in self._accounts():
            if account["name"] == name:
                return account
        raise RuntimeError(f"Nie ma konta o nazwie: {name}")

    def getA(self, column, name):
        if column == "profile":
            return self.get_or_create_profile(name, "")
        return self._account_by_name(name)[column]

    def insert(self, email, password, name, profile):
        self._request("POST", "/api/accounts", json={"name": name, "email": email, "password": password})
        if profile:
            self.set_setting("profile." + name, profile)
        self._invalidate()

    def _edit_account(self, account, password=None):
        self._request("PUT", "/api/accounts", json={
            "id": account["id"], "name": account["name"], "email": account["email"],
            "password": password,
        })
        self._invalidate()

    # --- lokalizacje ---

    def _locations(self):
        return self._get("/api/script/locations").json()["locations"]

    def _location_by_name(self, name):
        for location in self._locations():
            if location["name"] == name:
                return location
        raise RuntimeError(f"Nie ma lokalizacji: {name}")

    def save_location(self, location):
        self._request("POST", "/api/locations", json={"name": location})

    # --- kategorie ---

    def _all_categories(self):
        if self._categories is None:
            self._categories = self._get("/api/categories").json()["categories"]
        return self._categories

    def find_category(self, category):
        for c in self._all_categories():
            if c["name"] == category:
                return c["id"]
        raise RuntimeError(f"Nie ma kategorii: {category}")

    # --- produkty ---

    def _products(self):
        if self._script_products is None:
            self._script_products = self._get("/api/script/products").json()["products"]
        return self._script_products

    def _product_by_name(self, name):
        for product in self._products():
            if product["name"] == name:
                return product
        raise RuntimeError(f"Nie ma produktu o nazwie: {name}")

    def find_product_by_name(self, product_name):
        p = self._product_by_name(product_name)
        return (p["id"], p["name"], p["title"], p["price"], p["description"])

    def find_all_product_categories_by_product_id(self, product_id):
        for product in self._products():
            if product["id"] == int(product_id):
                return [(category_id,) for category_id in product["categoryIds"]]
        return []

    def _edit_product(self, product):
        self._request("PUT", "/api/products", json={
            "id": product["id"], "name": product["name"], "title": product["title"],
            "description": product["description"], "price": product["price"],
            "categoryIds": product["categoryIds"],
        })
        self._invalidate()

    # Cloudflare Tunnel ucina requesty >100MB, wiec zdjecia wgrywamy partiami.
    _UPLOAD_BATCH_BYTES = 85 * 1024 * 1024

    def _image_batches(self, image_paths):
        batches, batch, size = [], [], 0
        for path in image_paths:
            file_size = os.path.getsize(path)
            if batch and size + file_size > self._UPLOAD_BATCH_BYTES:
                batches.append(batch)
                batch, size = [], 0
            batch.append(path)
            size += file_size
        if batch:
            batches.append(batch)
        return batches

    def _post_multipart(self, path, paths, data=None):
        files = [("images", (os.path.basename(p), open(p, "rb"))) for p in paths]
        try:
            self._request("POST", path, data=data or {}, files=files)
        finally:
            for _, (_, handle) in files:
                handle.close()

    def create_product(self, name, title, price, description, category_ids, image_paths):
        batches = self._image_batches(image_paths)
        data = {"name": name, "title": title, "price": str(price), "description": description,
                "categoryIds": [str(c) for c in category_ids]}
        self._post_multipart("/api/products", batches[0], data)
        self._invalidate()
        if len(batches) > 1:
            product_id = self._product_by_name(name)["id"]
            try:
                for batch in batches[1:]:
                    self._post_multipart(f"/api/products/{product_id}/images", batch)
            except Exception:
                # nie zostawiaj produktu z czescia zdjec — ponowna proba wgra go w calosci
                try:
                    self._request("DELETE", f"/api/products/{product_id}")
                except Exception:
                    pass
                self._invalidate()
                raise
            self._invalidate()

    def save_categories_for_products(self, product_id, category_id):
        product = self._product_by_id(product_id)
        if int(category_id) not in product["categoryIds"]:
            product["categoryIds"].append(int(category_id))
            self._edit_product(product)

    def update_category(self, new_category, product_id, category_id):
        product = self._product_by_id(product_id)
        ids = [int(new_category) if c == int(category_id) else c for c in product["categoryIds"]]
        product["categoryIds"] = ids
        self._edit_product(product)

    def delete_categories_for_products_by_id(self, product_id, category_id):
        product = self._product_by_id(product_id)
        product["categoryIds"] = [c for c in product["categoryIds"] if c != int(category_id)]
        self._edit_product(product)

    def _product_by_id(self, product_id):
        for product in self._products():
            if product["id"] == int(product_id):
                return product
        raise RuntimeError(f"Nie ma produktu o id: {product_id}")

    # --- zdjecia (bajty z backendu -> pliki tymczasowe dla Selenium) ---

    def find_all_images_by_product(self, product):
        product_id = self._product_by_name(product)["id"]
        images = self._get(f"/api/products/{product_id}/images").json()["images"]
        if self._tmp_dir is None:
            self._tmp_dir = tempfile.mkdtemp(prefix="autoposter_img_")
        paths = []
        for image in images:
            path = os.path.join(self._tmp_dir, f"img_{image['id']}.jpg")
            if not os.path.isfile(path):
                with open(path, "wb") as f:
                    f.write(base64.b64decode(image["url"]))
            paths.append((path,))
        return paths

    def count_all_images_by_product(self, product_name):
        return len(self._product_by_name(product_name)["imageIds"])

    def delete_all_images_by_product(self, product):
        pass  # DELETE /api/products usuwa zdjecia po stronie backendu

    def delete_all_categories_for_products_by_product(self, product):
        pass  # jw. — obsluguje to backend przy usuwaniu produktu

    # --- generyczne metody uzywane przez strony UI ---

    def fetch(self, table, column):
        if table == "parts":
            return [(a["name"],) for a in self._accounts()]
        if table == "product":
            return [(p["name"],) for p in self._products()]
        if table == "categories":
            return [(c["name"],) for c in self._all_categories()]
        if table == "localizations":
            return [(l["name"],) for l in self._locations()]
        raise RuntimeError(f"Nieznana tabela: {table}")

    def update(self, table, column, new, criterion_column, old):
        if table == "parts":
            if column == "profile":
                self.set_setting("profile." + old, new)
                return
            account = dict(self._account_by_name(old))
            if column == "password":
                self._edit_account(account, password=new)
            else:
                account[column] = new
                self._edit_account(account)
        elif table == "product":
            product = dict(self._product_by_name(old))
            field = "name" if column == "productName" else column
            product[field] = int(new) if field == "price" else new
            self._edit_product(product)
        elif table == "localizations":
            location = self._location_by_name(old)
            self._request("PUT", "/api/locations", json={"id": location["id"], "name": new})
        else:
            raise RuntimeError(f"Nieznana tabela: {table}")

    def remove(self, table, column, criterion):
        if table == "parts":
            self._request("DELETE", f"/api/accounts/{self._account_by_name(criterion)['id']}")
        elif table in ("product", "products"):
            self._request("DELETE", f"/api/products/{self._product_by_name(criterion)['id']}")
        elif table == "localizations":
            self._request("DELETE", f"/api/locations/{self._location_by_name(criterion)['id']}")
        else:
            raise RuntimeError(f"Nieznana tabela: {table}")
        self._invalidate()

    @contextmanager
    def transaction(self):
        yield  # operacje ida pojedynczymi wywolaniami API

    def close(self):
        self.http.close()
