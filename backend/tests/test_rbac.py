from apps.accounts.permissions import ROLE_MATRIX, owner_of, resolve_resource
from apps.ai_jobs.models import GenerationJob
from apps.catalog.models import CatalogOption
from apps.cats.models import Cat
from apps.community.models import Publication
from apps.stickers.models import StickerPack

from .conftest import FULL_CONFIGURATION


def test_el_rol_admin_ve_los_gatos_de_todos(member_client, admin_client, catalog, db):
    member_client.post("/api/cats/", {"name": "Michi", "configuration": FULL_CONFIGURATION}, format="json")
    listed = admin_client.get("/api/cats/").json()["results"]
    assert [cat["name"] for cat in listed] == ["Michi"]


def test_el_rol_admin_puede_editar_gato_ajeno(member_client, admin_client, catalog, db):
    cat_id = member_client.post(
        "/api/cats/", {"name": "Michi", "configuration": FULL_CONFIGURATION}, format="json"
    ).json()["id"]
    renamed = admin_client.patch(f"/api/cats/{cat_id}/", {"name": "Otro nombre"}, format="json")
    assert renamed.status_code == 200
    assert Cat.objects.get(pk=cat_id).name == "Otro nombre"


def test_matriz_rbac_restringe_escribir_recursos_compartidos():
    """El catálogo solo lo escribe el rol admin; los miembros leen (ADR-005)."""
    assert "POST" not in ROLE_MATRIX["member"]["shared"]
    assert "GET" in ROLE_MATRIX["member"]["shared"]
    assert {"GET", "POST", "PATCH", "DELETE"} <= ROLE_MATRIX["admin"]["shared"]
    assert "POST" in ROLE_MATRIX["member"]["owned"]


def test_lectura_del_catalogo_autenticada_por_token(anon_client, member_client, catalog, db):
    assert anon_client.get("/api/poses/").status_code == 200
    assert member_client.get("/api/poses/").status_code == 200


def test_resolucion_de_recursos_por_modelo(user, catalog, db):
    cat = Cat.objects.create(user=user, name="X", configuration={})
    pack = StickerPack.objects.create(cat=cat)
    publication = Publication.objects.create(cat=cat, user=user, title="T")
    job = GenerationJob.objects.create(user=user, job_type=GenerationJob.JobType.STICKER_PACK)

    assert resolve_resource(obj=cat) == "owned"
    assert resolve_resource(obj=pack) == "owned"
    assert resolve_resource(obj=publication) == "owned"
    assert resolve_resource(obj=job) == "owned"
    assert resolve_resource(obj=CatalogOption.objects.first()) == "shared"
    assert owner_of(pack).username == user.username
