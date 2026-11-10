from kitchi import catalog
from kitchi.editor_state import EditorState


def test_select_updates_config_and_dirty():
    state = EditorState()
    assert state.select_option("fur", "bicolor")
    assert state.configuration["fur"] == "bicolor"
    assert state.dirty


def test_select_same_option_is_noop():
    state = EditorState()
    assert not state.select_option("fur", "tabby")
    assert not state.dirty
    assert state.history == []


def test_select_invalid_option_rejected():
    state = EditorState()
    assert not state.select_option("fur", "nope")
    assert not state.select_option("no_category", "tabby")
    assert not state.dirty


def test_undo_restores_previous_config():
    state = EditorState()
    state.select_option("fur", "bicolor")
    state.select_option("eyes", "big_blue")
    assert state.undo()
    assert state.configuration["eyes"] == "round_green"
    assert state.configuration["fur"] == "bicolor"
    assert state.undo()
    assert state.configuration["fur"] == "tabby"
    assert not state.undo()


def test_reset_is_undoable():
    state = EditorState()
    state.select_option("accessory", "bow")
    assert state.reset()
    assert state.configuration == catalog.default_config()
    assert state.undo()
    assert state.configuration["accessory"] == "bow"


def test_randomize_produces_valid_config():
    state = EditorState()
    state.randomize()
    assert catalog.validate_config(state.configuration) == []
    assert state.dirty


def test_mark_saved_clears_dirty():
    state = EditorState()
    state.select_option("top", "hoodie")
    state.mark_saved("abc123", "Michi")
    assert not state.dirty
    assert state.cat_id == "abc123"
    assert state.cat_name == "Michi"


def test_load_existing_cat():
    cat = {"id": "x1", "name": "Bigotes", "configuration": catalog.default_config()}
    state = EditorState(cat=cat)
    assert state.cat_id == "x1"
    assert state.cat_name == "Bigotes"
    assert not state.dirty


def test_history_is_bounded():
    state = EditorState()
    codes = ["tabby", "bicolor", "dark_spots"]
    for i in range(200):
        state.select_option("fur", codes[i % 3])
    from kitchi.editor_state import MAX_HISTORY
    assert len(state.history) <= MAX_HISTORY