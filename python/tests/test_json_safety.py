import json
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from teams_ccl_common import clean_text, html_to_text, normalize_json_value, normalize_thread_id, write_json


class _Undefined:
    def __repr__(self) -> str:
        return "<Undefined>"


class JsonSafetyTests(unittest.TestCase):
    def test_html_to_text_preserves_inline_emoji_images(self) -> None:
        html = (
            '<p><span title="Party popper" type="(1f389_partypopper)" class="animated-emoticon-20-1f389_partypopper" itemscope>'
            '<img itemscope itemtype="http://schema.skype.com/Emoji" itemid="1f389_partypopper" '
            'src="https://example.test/party.png" title="Party popper" alt="🎉" style="width:20px;height:20px" />'
            "</span></p>"
        )

        self.assertEqual(html_to_text(html), "🎉")

    def test_normalize_json_value_converts_ccl_undefined_sentinel(self) -> None:
        payload = {"metadata": {"topic": _Undefined()}, "values": ["<Undefined>", ("ok", _Undefined())]}

        normalized = normalize_json_value(payload)

        self.assertEqual(normalized, {"metadata": {"topic": None}, "values": [None, ["ok", None]]})
        json.dumps(normalized)

    def test_normalize_json_value_converts_bytes_to_preview_object(self) -> None:
        payload = {"blob": b"\x00\x01hello", "nested": [bytearray(b"\xff\x10")]}

        normalized = normalize_json_value(payload)

        self.assertEqual(
            normalized,
            {
                "blob": {"type": "bytes", "length": 7, "preview_hex": "000168656c6c6f"},
                "nested": [{"type": "bytes", "length": 2, "preview_hex": "ff10"}],
            },
        )
        json.dumps(normalized)

    def test_clean_text_treats_ccl_undefined_as_empty(self) -> None:
        self.assertIsNone(clean_text(_Undefined()))

    def test_normalize_thread_id_strips_wrapping_brackets(self) -> None:
        self.assertEqual(normalize_thread_id("[19:abc@thread.v2]"), "19:abc@thread.v2")

    def test_write_json_normalizes_before_serializing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "payload.json"

            write_json(output_path, {"topic": _Undefined()})

            self.assertEqual(json.loads(output_path.read_text(encoding="utf-8")), {"topic": None})


if __name__ == "__main__":
    unittest.main()
