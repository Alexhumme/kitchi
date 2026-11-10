"""Cliente HTTP de la API de Kitchi Studio (Django REST Framework).

La URL se resuelve en este orden: `KITCHI_API_URL`, luego `API_BASE_URL`
(entorno o `.env` de la raíz) y, si no hay ninguna, el cliente queda en modo
local para que la interfaz de invitado siga funcionando sin backend.

La autenticación usa token de Django con el encabezado
`Authorization: Token <clave>`, según ADR-005 y docs/05_API_CONTRACTS.md.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path

from . import catalog

DEFAULT_TIMEOUT = 8
_UNSET = object()


def _read_dotenv() -> dict[str, str]:
    env_path = Path(__file__).resolve().parents[3] / ".env"
    values: dict[str, str] = {}
    if not env_path.exists():
        return values
    try:
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
    except OSError:
        return {}
    return values


def resolve_base_url() -> str:
    for name in ("KITCHI_API_URL", "API_BASE_URL"):
        value = os.environ.get(name)
        if value:
            return value.strip().rstrip("/")
    return _read_dotenv().get("API_BASE_URL", "").strip().rstrip("/")


class ApiError(Exception):
    """Error normalizado de la API: código de negocio, mensaje y estado HTTP."""

    def __init__(self, code: str, message: str, status: int | None = None, details: dict | None = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status
        self.details = details or {}

    def user_message(self) -> str:
        """Extrae el primer error de campo que devuelve DRF, si existe.

        Los errores de serializer llegan en `details.campo` (dict por campo) y los
        de validación de catálogo en `details.campos` (lista de problemas).
        """
        if not isinstance(self.details, dict):
            return self.message
        for key in ("campo", "campos"):
            value = self.details.get(key)
            parts: list[str] = []
            if isinstance(value, dict):
                for item in value.values():
                    if isinstance(item, (list, tuple)):
                        parts.extend(str(entry) for entry in item)
                    else:
                        parts.append(str(item))
            elif isinstance(value, (list, tuple)):
                parts.extend(str(item) for item in value)
            if parts:
                return " ".join(parts)
        return self.message


def _decode(raw: bytes) -> dict | list:
    if not raw:
        return {}
    try:
        return json.loads(raw.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {}


class ApiClient:
    def __init__(self, base_url=_UNSET, timeout: int = DEFAULT_TIMEOUT):
        if base_url is _UNSET:
            base_url = resolve_base_url()
        self.base_url = (base_url or "").rstrip("/")
        self.timeout = timeout
        self.token: str | None = None

    @property
    def mode(self) -> str:
        return "http" if self.base_url else "local"

    def set_token(self, token: str | None) -> None:
        self.token = token or None

    # --- transporte -----------------------------------------------------
    def _request(self, method: str, path: str, data: dict | None = None, token: str | None = None):
        url = f"{self.base_url}{path}"
        body = None
        headers = {"Accept": "application/json"}
        if data is not None:
            body = json.dumps(data, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json; charset=utf-8"
        auth_token = token if token is not None else self.token
        if auth_token:
            headers["Authorization"] = f"Token {auth_token}"

        request = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return _decode(response.read())
        except urllib.error.HTTPError as exc:
            payload = _decode(exc.read())
            error = payload.get("error", {}) if isinstance(payload, dict) else {}
            raise ApiError(
                error.get("code", f"HTTP_{exc.code}"),
                error.get("message", f"Error HTTP {exc.code}"),
                exc.code,
                error.get("details", {}),
            ) from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise ApiError("API_UNREACHABLE", "No se pudo conectar con la API.") from exc

    def _get(self, path: str):
        return self._request("GET", path)

    # --- disponibilidad y catálogo ---------------------------------------
    def health(self) -> dict:
        if self.mode == "local":
            return {"status": "local-mode", "simulated": False}
        return self._get("/api/health/")

    def get_catalog(self) -> dict:
        if self.mode == "local":
            return catalog.as_api_payload()
        return self._get("/api/catalog/")

    def get_poses(self) -> list[dict]:
        if self.mode == "local":
            return [
                {"code": code, "name": name}
                for code, name in (
                    ("greeting", "Saludo"),
                    ("happy", "Alegría"),
                    ("angry", "Enfado"),
                    ("sad", "Tristeza"),
                    ("surprised", "Sorpresa"),
                    ("sleepy", "Sueño"),
                )
            ]
        data = self._get("/api/poses/")
        return data.get("results", data) if isinstance(data, dict) else data

    # --- cuentas ---------------------------------------------------------
    def register(self, username: str, email: str, password: str) -> dict:
        return self._request(
            "POST",
            "/api/auth/register/",
            {"username": username, "email": email, "password": password},
        )

    def login(self, username: str, password: str) -> dict:
        return self._request("POST", "/api/auth/login/", {"username": username, "password": password})

    def logout(self) -> None:
        if self.mode == "http" and self.token:
            self._request("POST", "/api/auth/logout/")
        self.set_token(None)

    def me(self) -> dict:
        return self._request("GET", "/api/auth/me/")

    # --- gatos -----------------------------------------------------------
    def list_cats(self) -> list[dict]:
        data = self._get("/api/cats/")
        if isinstance(data, dict):
            return data.get("results", [])
        return data

    def create_cat(self, name: str, configuration: dict) -> dict:
        return self._request("POST", "/api/cats/", {"name": name, "configuration": configuration})

    def update_cat(self, cat_id, name: str | None = None, configuration: dict | None = None) -> dict:
        payload: dict = {}
        if name is not None:
            payload["name"] = name
        if configuration is not None:
            payload["configuration"] = configuration
        return self._request("PATCH", f"/api/cats/{cat_id}/", payload)

    def delete_cat(self, cat_id) -> None:
        self._request("DELETE", f"/api/cats/{cat_id}/")

    # --- comunidad -------------------------------------------------------
    def get_publications(self, page: int = 1, page_size: int = 12) -> dict:
        if self.mode == "local":
            return {"count": 0, "results": [], "pending_backend": True}
        return self._get(f"/api/publications/?page={page}&page_size={page_size}")
