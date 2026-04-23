import json
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from teams_ccl_common import clean_text, normalize_json_value, write_json


class _Undefined:
    def __repr__(self) -> str:
        return "<Undefined>"


class JsonSafetyTests(unittest.TestCase):
    def test_normalize_json_value_converts_ccl_undefined_sentinel(self) -> None:
        payload = {"metadata": {"topic": _Undefined()}, "values": ["<Undefined>", ("ok", _Undefined())]}

        normalized = normalize_json_value(payload)

        self.assertEqual(normalized, {"metadata": {"topic": None}, "values": [None, ["ok", None]]})
        json.dumps(normalized)

    def test_clean_text_treats_ccl_undefined_as_empty(self) -> None:
        self.assertIsNone(clean_text(_Undefined()))

    def test_write_json_normalizes_before_serializing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "payload.json"

            write_json(output_path, {"topic": _Undefined()})

            self.assertEqual(json.loads(output_path.read_text(encoding="utf-8")), {"topic": None})


if __name__ == "__main__":
    unittest.main()
