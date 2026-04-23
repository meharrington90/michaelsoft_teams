import csv
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from export_teams_ccl_csv import export_calls, export_conversations


class ExportCsvTests(unittest.TestCase):
    def test_conversation_and_call_exports_stream_expected_rows(self) -> None:
        export_data = {
            "threads": [
                {
                    "id": "thread-b",
                    "label": "Zulu",
                    "category": "thread",
                    "metadata_quality": "detailed",
                    "message_count": 1,
                    "participants": ["Bob"],
                    "messages": [
                        {
                            "id": "m2",
                            "timestamp": "2025-01-02T00:00:00+00:00",
                            "sender_display_name": "Bob",
                            "message_type": "RichText/Html",
                            "quality": "curated",
                            "content_text": "Second",
                            "source": "ccl:replychains",
                        }
                    ],
                },
                {
                    "id": "thread-a",
                    "label": "Alpha",
                    "category": "chat_space",
                    "metadata_quality": "detailed",
                    "message_count": 1,
                    "participants": ["Alice"],
                    "messages": [
                        {
                            "id": "m1",
                            "timestamp": "2025-01-01T00:00:00+00:00",
                            "sender_display_name": "Alice",
                            "message_type": "RichText/Html",
                            "quality": "curated",
                            "content_text": "First",
                            "source": "ccl:replychains",
                        }
                    ],
                },
            ],
            "calls": [
                {
                    "call_id": "call-1",
                    "participant_display_names": ["Alice", "Bob"],
                    "participant_ids": ["user-1", "user-2"],
                }
            ],
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            manifest = export_conversations(export_data, output_dir)
            export_calls(export_data, output_dir)

            with (output_dir / "conversations_all_flat.csv").open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            with (output_dir / "call_history.csv").open(newline="", encoding="utf-8") as handle:
                call_rows = list(csv.DictReader(handle))

            self.assertEqual([row["thread_label"] for row in rows], ["Alpha", "Zulu"])
            self.assertEqual(rows[0]["content_text"], "First")
            self.assertEqual(len(manifest), 2)
            self.assertTrue(manifest[0]["csv"].endswith(".csv"))
            self.assertEqual(call_rows[0]["participant_display_names"], "Alice; Bob")
            self.assertEqual(call_rows[0]["participant_ids"], "user-1; user-2")


if __name__ == "__main__":
    unittest.main()
