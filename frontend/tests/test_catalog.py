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