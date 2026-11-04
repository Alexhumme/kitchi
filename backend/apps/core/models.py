from django.db import models

STATUS_PENDING = "pending"
STATUS_RUNNING = "running"
STATUS_COMPLETED = "completed"
STATUS_FAILED = "failed"

STATUS_CHOICES = [
    (STATUS_PENDING, "Pendiente"),
    (STATUS_RUNNING, "En ejecución"),
    (STATUS_COMPLETED, "Completado"),
    (STATUS_FAILED, "Fallido"),
]

# Transiciones legales del ciclo de vida (04_DATA_MODEL.md · Estados).
# Un trabajo puede fallar antes de arrancar (validación o proveedor caído) y un
# trabajo fallido puede volver a ponerse en cola.
ALLOWED_TRANSITIONS = {
    STATUS_PENDING: {STATUS_RUNNING, STATUS_FAILED},
    STATUS_RUNNING: {STATUS_COMPLETED, STATUS_FAILED},
    STATUS_COMPLETED: set(),
    STATUS_FAILED: {STATUS_PENDING},
}


class StatusMixin(models.Model):
    """Estado con transiciones validadas; reutilizado por paquetes y trabajos."""

    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_PENDING, db_index=True)
    error_code = models.CharField(max_length=64, blank=True)

    class Meta:
        abstract = True

    def can_transition_to(self, new_status: str) -> bool:
        return new_status in ALLOWED_TRANSITIONS.get(self.status, set())

    def transition_to(self, new_status: str, error_code: str = ""):
        """Cambia el estado sin guardar; lanza ValueError si la transición no es legal."""
        if not self.can_transition_to(new_status):
            raise ValueError(f"Transición de estado inválida: {self.status} → {new_status}")
        self.status = new_status
        if new_status == STATUS_FAILED:
            self.error_code = error_code or "UNKNOWN"
        elif new_status == STATUS_PENDING:
            self.error_code = ""
