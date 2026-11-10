"""La consola de administración gestiona las entidades del dominio con las reglas del backend."""

import json

import pytest
from django.urls import reverse

from apps.ai_jobs.models import GenerationJob
from apps.catalog.models import CatalogOption, Pose
from apps.cats.models import Cat
from apps.community.models import Publication
from apps.core.models import STATUS_COMPLETED, STATUS_FAILED, STATUS_PENDING, STATUS_RUNNING
from apps.stickers.models import Sticker, StickerPack

from .conftest import FULL_CONFIGURATION

ENTIDADES = [
    ("auth", "user"),
    ("accounts", "userprofile"),
    ("catalog", "catalogoption"),
    ("catalog", "pose"),
    ("cats", "cat"),
    ("stickers", "stickerpack"),
    ("stickers", "sticker"),
    ("community", "publication"),
    ("ai_jobs", "generationjob"),
]


@pytest.fixture
def cat(user, catalog):
    return Cat.objects.create(user=user, name="Michi", configuration=FULL_CONFIGURATION)


@pytest.fixture
def pack(cat):
    return StickerPack.objects.create(cat=cat)


def _run_action(console_client, url_name, action, ids):
    return console_client.post(reverse(url_name), {"action": action, "index": 0, "_selected_action": ids})


def _cat_form(user, configuration):
    return {"user": user.pk, "name": "Michi", "configuration": json.dumps(configuration)}


@pytest.mark.parametrize(("app_label", "model"), ENTIDADES)
def test_la_consola_abre_listado_y_formulario(console_client, catalog, app_label, model):
    assert console_client.get(reverse(f"admin:{app_label}_{model}_changelist")).status_code == 200
    assert console_client.get(reverse(f"admin:{app_label}_{model}_add")).status_code == 200


def test_la_consola_identifica_el_proyecto(console_client, db):
    assert "Administración de Kitchi Studio" in console_client.get(reverse("admin:index")).content.decode()


def test_el_admin_valida_el_catalogo_antes_de_guardar(console_client, catalog, user, db):
    bad = {**FULL_CONFIGURATION, "top": "armadura_inexistente"}
    response = console_client.post(reverse("admin:cats_cat_add"), _cat_form(user, bad))

    assert response.status_code == 200
    assert "fuera del catálogo" in response.content.decode()
    assert Cat.objects.count() == 0


def test_el_admin_bloquea_opciones_premium_sin_plan(console_client, catalog, user, db):
    CatalogOption.objects.create(category="top", code="corona", label="Corona", is_premium=True)
    response = console_client.post(reverse("admin:cats_cat_add"), _cat_form(user, {**FULL_CONFIGURATION, "top": "corona"}))

    assert response.status_code == 200
    assert "premium" in response.content.decode()
    assert Cat.objects.count() == 0


def test_el_admin_normaliza_la_configuracion_guardada(console_client, catalog, user, db):
    response = console_client.post(reverse("admin:cats_cat_add"), _cat_form(user, FULL_CONFIGURATION))

    assert response.status_code == 302
    saved = Cat.objects.get()
    assert saved.schema_version == 1
    assert saved.configuration["top"] == {"code": "hoodie"}


def test_las_acciones_de_paquete_respetan_la_maquina_de_estados(console_client, pack, db):
    changelist = "admin:stickers_stickerpack_changelist"

    _run_action(console_client, changelist, "poner_en_ejecucion", [pack.pk])
    pack.refresh_from_db()
    assert pack.status == STATUS_RUNNING

    _run_action(console_client, changelist, "marcar_completados", [pack.pk])
    pack.refresh_from_db()
    assert pack.status == STATUS_COMPLETED
    assert pack.completed_at is not None

    _run_action(console_client, changelist, "poner_en_ejecucion", [pack.pk])
    pack.refresh_from_db()
    assert pack.status == STATUS_COMPLETED


def test_las_acciones_de_trabajo_usan_los_metodos_del_modelo(console_client, cat, user, db):
    changelist = "admin:ai_jobs_generationjob_changelist"
    job = GenerationJob.objects.create(user=user, job_type=GenerationJob.JobType.STICKER_PACK)

    _run_action(console_client, changelist, "poner_en_ejecucion", [job.pk])
    job.refresh_from_db()
    assert (job.status, job.started_at is not None) == (STATUS_RUNNING, True)

    _run_action(console_client, changelist, "marcar_fallidos", [job.pk])
    job.refresh_from_db()
    assert (job.status, job.error_code) == (STATUS_FAILED, "ADMIN_MANUAL")

    _run_action(console_client, changelist, "reintentar", [job.pk])
    job.refresh_from_db()
    assert (job.status, job.error_code) == (STATUS_PENDING, "")

    _run_action(console_client, changelist, "poner_en_ejecucion", [job.pk])
    _run_action(console_client, changelist, "marcar_completados", [job.pk])
    job.refresh_from_db()
    assert job.status == STATUS_COMPLETED
    assert job.completed_at is not None


def test_la_accion_publicar_cambia_la_visibilidad(console_client, cat, user, db):
    publication = Publication.objects.create(
        cat=cat, user=user, title="Michi", visibility=Publication.Visibility.PRIVATE
    )

    _run_action(console_client, "admin:community_publication_changelist", "hacer_publicas", [publication.pk])
    publication.refresh_from_db()
    assert publication.visibility == Publication.Visibility.PUBLIC


def test_no_se_elimina_una_pose_con_stickers(console_client, pack, db):
    pose = Pose.objects.create(code="bailando", name="Bailando")
    Sticker.objects.create(pack=pack, pose=pose, status=Sticker.Status.COMPLETED)

    console_client.post(reverse("admin:catalog_pose_delete", args=[pose.pk]), {"post": "yes"})
    assert Pose.objects.filter(pk=pose.pk).exists()
