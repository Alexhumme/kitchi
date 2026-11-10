"""Servidor de API SIMULADO para desarrollo del frontend.

NO es el backend del proyecto: el backend real será Django REST Framework
(tareas P02/P03/P11, responsable B). Este script solo expone datos de
desarrollo etiquetados como simulados para probar el cliente HTTP del
frontend contra los contratos de docs/05_API_CONTRACTS.md.

Uso: python scripts/mock_api.py  → http://localhost:8001
El frontend lo consume con: KITCHI_API_URL=http://localhost:8001

Regla del proyecto: lo simulado se etiqueta y nunca se presenta como real
en la demo ni en la documentación.
"""

from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "frontend" / "src"))

from kitchi import catalog  # noqa: E402

POSES = [
    {"code": "greeting", "name": "Saludo"},
    {"code": "happy", "name": "Alegría"},
    {"code": "angry", "name": "Enfado"},
    {"code": "sad", "name": "Tristeza"},
    {"code": "surprised", "name": "Sorpresa"},
    {"code": "sleepy", "name": "Sueño"},
]


class MockHandler(BaseHTTPRequestHandler):
    def _send(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("X-Kitchi-Simulated", "true")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/health/":
            self._send(200, {"status": "ok", "simulated": True})
        elif path == "/api/catalog/":
            payload = catalog.as_api_payload()
            payload["simulated"] = True
            self._send(200, payload)
        elif path == "/api/poses/":
            self._send(200, {"simulated": True, "results": POSES})
        elif path == "/api/publications/":
            self._send(200, {"simulated": True, "count": 0, "results": [],
                             "note": "Sin publicaciones simuladas: el hub real llega con P18."})
        else:
            self._send(404, {"simulated": True,
                             "error": {"code": "NOT_IMPLEMENTED_IN_MOCK",
                                      "message": "Endpoint no implementado en el mock de desarrollo.",
                                      "details": {}}})

    def log_message(self, fmt, *args) -> None:
        print(f"[mock-api] {args[0]}")


def main() -> None:
    port = 8001
    server = ThreadingHTTPServer(("127.0.0.1", port), MockHandler)
    print("=" * 60)
    print("KITCHI MOCK API — SIMULADO, SOLO DESARROLLO")
    print("No es el backend Django del proyecto (P02/P03 pendientes).")
    print(f"Escuchando en http://127.0.0.1:{port}")
    print("=" * 60)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


if __name__ == "__main__":
    main()