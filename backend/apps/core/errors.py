from rest_framework import status
from rest_framework.response import Response

DEFAULT_MESSAGES = {
    status.HTTP_400_BAD_REQUEST: "La petición no es válida.",
    status.HTTP_401_UNAUTHORIZED: "Debes iniciar sesión para continuar.",
    status.HTTP_403_FORBIDDEN: "No tienes permisos para esta operación.",
    status.HTTP_404_NOT_FOUND: "El recurso no existe.",
    status.HTTP_409_CONFLICT: "Conflicto con el estado actual del recurso.",
    status.HTTP_413_REQUEST_ENTITY_TOO_LARGE: "El archivo supera el tamaño permitido.",
    status.HTTP_429_TOO_MANY_REQUESTS: "Has alcanzado el límite de solicitudes del plan.",
    status.HTTP_503_SERVICE_UNAVAILABLE: "El servicio no está disponible en este momento.",
}


class APIError(Exception):
    """Error de negocio con código estable para la interfaz (05_API_CONTRACTS.md)."""

    def __init__(self, code, message=None, http_status=status.HTTP_400_BAD_REQUEST, details=None):
        self.code = code
        self.http_status = http_status
        self.message = message or DEFAULT_MESSAGES.get(http_status, "Error no clasificado.")
        self.details = details or {}
        super().__init__(self.message)

    def response(self):
        return Response(
            {"error": {"code": self.code, "message": self.message, "details": self.details}},
            status=self.http_status,
        )
