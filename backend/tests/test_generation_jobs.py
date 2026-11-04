import pytest
from django.utils import timezone

from apps.ai_jobs.models import GenerationJob
from apps.core.models import ALLOWED_TRANSITIONS


@pytest.fixture
def job(user):
    return GenerationJob.objects.create(user=user, job_type=GenerationJob.JobType.PHOTO_TO_CHIBI)


def test_ciclo_completo_de_un_trabajo(job):
    job.mark_started(timezone.now())
    assert job.status == "running"

    job.mark_completed(timezone.now(), result={"stickers": 6})
    assert job.status == "completed"
    assert job.result == {"stickers": 6}
    assert job.completed_at is not None


def test_fallo_registra_codigo(job):
    job.mark_started(timezone.now())
    job.mark_failed("AI_TIMEOUT")
    assert job.status == "failed"
    assert job.error_code == "AI_TIMEOUT"


def test_transiciones_ilegales_no_aplican(job):
    with pytest.raises(ValueError):
        job.transition_to("completed")
    assert job.status == "pending"

    job.mark_started(timezone.now())
    with pytest.raises(ValueError):
        job.transition_to("pending")


def test_fallido_puede_reintentarse(job):
    job.mark_failed("AI_TIMEOUT")
    job.transition_to("pending")
    assert job.status == "pending"
    assert job.error_code == ""


def test_tabla_de_transiciones_es_coherente():
    assert ALLOWED_TRANSITIONS["pending"] == {"running", "failed"}
    assert ALLOWED_TRANSITIONS["completed"] == set()
    assert ALLOWED_TRANSITIONS["failed"] == {"pending"}
