"""Cliente de la API según docs/05_API_CONTRACTS.md.

Modos:
- local (por defecto): el frontend trabaja con almacenamiento de invitado;
  no hay backend todavía (P02/P03 pendientes).
- http: apunta a KITCHI_API_URL (Django real o scripts/mock_api.py simulado).

La autenticación está pendiente de decisión (P03, A+B): este cliente no
implementa login hasta que exista el ADR correspondiente.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

from . import catalog


class ApiError(Exception):
    def __init__(self, code: str, message: str, status: int | None = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status


class ApiClient:
    def __init__(self, base_url: str | None = None):
        self.base_url = (base_url or os.environ.get("KITCHI_API_URL") or "").rstrip("/")

    @property
    def mode(self) -> str:
        return "http" if self.base_url else "local"

    def _get(self, path: str) -> dict:
        url = f"{self.base_url}{path}"
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            try:
                payload = json.loads(exc.read().decode("utf-8"))
                error = payload.get("error", {})
                raise ApiError(
                    error.get("code", "HTTP_ERROR"),
                    error.get("message", f"Error HTTP {exc.code}"),
                    exc.code,
                ) from exc
            except (json.JSONDecodeError, UnicodeDecodeError):
                raise ApiError("HTTP_ERROR", f"Error HTTP {exc.code}", exc.code) from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise ApiError("API_UNREACHABLE", "No se pudo conectar con la API.") from exc

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

    def get_publications(self, page: int = 1, page_size: int = 12) -> dict:
        if self.mode == "local":
            return {"count": 0, "results": [], "pending_backend": True}
        return self._get(f"/api/publications/?page={page}&page_size={page_size}")