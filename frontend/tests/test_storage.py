import pytest

from kitchi import catalog, models, storage


@pytest.mark.asyncio
async def test_roundtrip_persistence():
    mem = storage.MemoryStorage()
    cat = models.new_cat("Michi", catalog.default_config())
    await storage.persist_cats(mem, [cat])
    loaded = await storage.load_cats(mem)
    assert loaded == [cat]


@pytest.mark.asyncio
async def test_corrupted_storage_recovers_empty():
    mem = storage.MemoryStorage()
    await mem.set(storage.STORAGE_KEY, "{not json")
    assert await storage.load_cats(mem) == []


@pytest.mark.asyncio
async def test_invalid_records_are_filtered():
    mem = storage.MemoryStorage()
    good = models.new_cat("Michi", catalog.default_config())
    bad = {"id": "bad", "name": "", "configuration": {"fur": "dragon"}}
    await mem.set(storage.STORAGE_KEY, __import__("json").dumps([good, bad]))
    loaded = await storage.load_cats(mem)
    assert loaded == [good]


@pytest.mark.asyncio
async def test_session_roundtrip_and_clear():
    mem = storage.MemoryStorage()
    token, user = await storage.load_session(mem)
    assert token is None and user is None
    await storage.persist_session(mem, "abc123", {"username": "michi"})
    token, user = await storage.load_session(mem)
    assert token == "abc123"
    assert user == {"username": "michi"}
    await storage.clear_session(mem)
    assert await storage.load_session(mem) == (None, None)


def test_cat_from_api_flattens_configuration():
    record = {
        "id": 7,
        "name": "Michi",
        "configuration": {
            "schema_version": 1,
            "fur": {"code": "bicolor"},
            "eyes": {"style": "big_blue"},
            "hair": "wavy",
            "top": "hoodie",
            "bottom": "skirt",
            "accessory": "bow",
        },
        "created_at": "2026-11-09T10:00:00Z",
        "updated_at": "2026-11-09T10:00:00Z",
    }
    cat = models.cat_from_api(record)
    assert cat["id"] == 7
    assert cat["configuration"]["fur"] == "bicolor"
    assert cat["configuration"]["eyes"] == "big_blue"
    assert cat["configuration"]["hair"] == "wavy"


def test_guest_limit_of_three():
    cats = [models.new_cat(f"Gato {i}", catalog.default_config()) for i in range(3)]
    assert not models.can_add_cat(cats)
    assert models.can_add_cat(cats, editing_id=cats[0]["id"])
    assert models.can_add_cat(cats[:2])


def test_name_validation():
    assert models.validate_name("") is not None
    assert models.validate_name("   ") is not None
    assert models.validate_name("x" * 41) is not None
    assert models.validate_name("  Michi  ") is None


def test_new_cat_shape():
    cat = models.new_cat("Michi", catalog.default_config())
    assert models.validate_cat_record(cat) == []
    assert cat["configuration"] is not catalog.default_config()