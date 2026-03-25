from unittest.mock import patch

from ..app.routers.action_items import extract_llm
from ..app.schemas import ExtractActionItemsLLMRequest
from ..app.services.extract import extract_action_items, extract_action_items_llm_with_meta


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


@patch("week2.app.services.extract.chat")
def test_extract_action_items_llm_success(mock_chat):
    mock_chat.return_value = {
        "message": {
            "content": '{"action_items": ["- [ ] Set up database", "Write tests", "write tests"]}'
        }
    }

    result = extract_action_items_llm_with_meta("Meeting notes")

    assert result["extraction_method"] == "llm"
    assert result["fallback_reason"] is None
    assert result["items"] == ["Set up database", "Write tests"]


@patch("week2.app.services.extract.chat")
def test_extract_action_items_llm_fallback_to_rules_on_bad_json(mock_chat):
    mock_chat.return_value = {"message": {"content": "not json"}}

    text = "- [ ] Set up database\nSome narrative"
    result = extract_action_items_llm_with_meta(text)

    assert result["extraction_method"] == "rules"
    assert "llm extraction failed" in str(result["fallback_reason"])
    assert result["items"] == ["Set up database"]


@patch("week2.app.services.extract.chat")
def test_extract_action_items_llm_route_returns_metadata(mock_chat, monkeypatch):
    mock_chat.return_value = {
        "message": {
            "content": '{"action_items": ["Implement API endpoint", "Write tests"]}'
        }
    }

    def _fake_insert_action_items(items, note_id=None):
        return list(range(1, len(items) + 1))

    monkeypatch.setattr("week2.app.routers.action_items.db.insert_action_items", _fake_insert_action_items)

    payload = extract_llm(ExtractActionItemsLLMRequest(text="some meeting text"))
    assert payload.extraction_method == "llm"
    assert payload.fallback_reason is None
    assert [i.text for i in payload.items] == ["Implement API endpoint", "Write tests"]


@patch("week2.app.services.extract.chat")
def test_extract_action_items_llm_route_fallback_metadata(mock_chat, monkeypatch):
    mock_chat.side_effect = RuntimeError("ollama unavailable")

    def _fake_insert_action_items(items, note_id=None):
        return list(range(1, len(items) + 1))

    monkeypatch.setattr("week2.app.routers.action_items.db.insert_action_items", _fake_insert_action_items)

    payload = extract_llm(ExtractActionItemsLLMRequest(text="- [ ] Set up database"))
    assert payload.extraction_method == "rules"
    assert "ollama unavailable" in str(payload.fallback_reason)
    assert [i.text for i in payload.items] == ["Set up database"]
