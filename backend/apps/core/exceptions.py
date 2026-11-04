from rest_framework.views import exception_handler

from .errors import APIError


def kitchi_exception_handler(exc, context):
    """Devuelve todos los fallos de la API con el formato {error: {code, message, details}}.

    Contrato definido en docs/05_API_CONTRACTS.md (gestión de errores).
    """
    if isinstance(exc, APIError):
        return exc.response()

    response = exception_handler(exc, context)
    if response is None:
        return None

    detail = response.data
    if isinstance(detail, dict) and set(detail) == {"detail"}:
        message = str(detail["detail"])
        details = {}
    else:
        message = "Los datos enviados no son válidos."
        details = {"campo": detail if isinstance(detail, dict) else str(detail)}

    code = f"HTTP_{response.status_code}"
    response.data = {"error": {"code": code, "message": message, "details": details}}
    return response
