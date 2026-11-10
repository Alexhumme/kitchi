from kitchi import catalog


def test_catalog_has_six_categories_with_three_options():
    assert len(catalog.CATEGORIES) == 6
    for cat in catalog.CATEGORIES:
        assert len(cat.options) == 3
        codes = [o.code for o in cat.options]
        assert len(set(codes)) == 3


def test_default_config_is_valid():
    assert catalog.validate_config(catalog.default_config()) == []


def test_validate_rejects_unknown_option():
    config = catalog.default_config()
    config["fur"] = "dragon_scales"
    errors = catalog.validate_config(config)
    assert any("fuera del catálogo" in e for e in errors)


def test_validate_rejects_missing_category():
    config = catalog.default_config()
    del config["accessory"]
    errors = catalog.validate_config(config)
    assert any("accessory" in e for e in errors)


def test_validate_rejects_wrong_schema_version():
    config = catalog.default_config()
    config["schema_version"] = 99
    assert catalog.validate_config(config)


def test_summary_covers_all_categories():
    summary = catalog.config_summary(catalog.default_config())
    assert len(summary) == 6
    assert all(name != "—" for _, name in summary)


def test_api_payload_shape():
    payload = catalog.as_api_payload()
    assert payload["provisional"] is True
    assert set(payload["categories"]) == set(catalog.CATEGORY_KEYS)
    assert all(len(opts) == 3 for opts in payload["categories"].values())


def _backend_payload() -> dict:
    return {
        "schema_version": 1,
        "categories": {
            category.key: [
                {
                    "category": category.key,
                    "code": option.code,
                    "label": option.name,
                    "asset_path": f"assets/placeholders/{category.key}/{option.code}.png",
                    "is_premium": False,
                }
                for option in category.options
            ]
            for category in catalog.CATEGORIES
        },
    }


def test_apply_api_catalog_keeps_backend_codes():
    try:
        assert catalog.apply_api_catalog(_backend_payload()) is True
        assert catalog.CATALOG_SOURCE == "api"
        assert len(catalog.CATEGORIES) == 6
        assert [o.code for o in catalog.CATEGORIES[0].options] == ["tabby", "bicolor", "dark_spots"]
        assert catalog.CATEGORIES[0].options[0].asset_path.endswith("tabby.png")
    finally:
        catalog.reset_catalog()


def test_apply_api_catalog_rejects_empty_backend():
    try:
        assert catalog.apply_api_catalog({"schema_version": 1, "categories": {}}) is False
        assert catalog.CATALOG_SOURCE == "bundled"
    finally:
        catalog.reset_catalog()


def test_normalize_configuration_accepts_backend_blocks():
    config = {
        "schema_version": 1,
        "fur": {"code": "bicolor"},
        "eyes": {"style": "big_blue"},
        "hair": "wavy",
        "top": "hoodie",
        "bottom": "skirt",
        "accessory": "desconocido",
    }
    normalized = catalog.normalize_configuration(config)
    assert normalized["fur"] == "bicolor"
    assert normalized["eyes"] == "big_blue"
    assert normalized["hair"] == "wavy"
    assert normalized["accessory"] == "glasses"
    assert catalog.validate_config(normalized) == []