import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from build_teams_ccl_browser import build_browser, build_browser_payload


class BuildBrowserPayloadTests(unittest.TestCase):
    def build_export_data(self) -> dict:
        return {
            "summary": {"threads_total": 1, "messages_total": 3, "calls_total": 0},
            "profile": {"oid": "user-1", "display_name": "Example User"},
            "threads": [
                {
                    "id": "19:thread@thread.v2",
                    "category": "thread",
                    "label": "Example Thread",
                    "message_count": 3,
                    "messages": [
                        {
                            "id": "m1",
                            "timestamp": "2025-01-01T00:00:00+00:00",
                            "sender_display_name": "Alice",
                            "sender_id": "user-2",
                            "message_type": "RichText/Html",
                            "content_html": "<div><strong>Hello</strong></div>",
                            "content_text": "Hello",
                            "quality": "curated",
                        },
                        {
                            "id": "m2",
                            "timestamp": "2025-01-01T00:01:00+00:00",
                            "sender_display_name": "Alice",
                            "sender_id": "user-2",
                            "message_type": "ThreadActivity/TopicUpdate",
                            "content_html": "<value>New Topic</value>",
                            "content_text": "Topic updated",
                            "quality": "event",
                        },
                        {
                            "id": "m3",
                            "timestamp": "2025-01-01T00:02:00+00:00",
                            "sender_display_name": "Alice",
                            "sender_id": "user-2",
                            "message_type": "RichText/Html",
                            "content_text": "Attachment message",
                            "quality": "attachment",
                            "attachments": [
                                {
                                    "id": "a1",
                                    "name": "report.pdf",
                                    "url": "https://example.test/report.pdf",
                                    "kind": "file",
                                }
                            ],
                        },
                    ],
                    "metadata": {"topic": "Topic"},
                    "meeting": {"subject": "Subject"},
                    "participant_ids": ["user-1", "user-2"],
                    "participants": ["Example User", "Alice"],
                }
            ],
            "calls": [],
            "guid_directory": {"user-2": "Alice"},
        }

    def test_payload_keeps_html_only_for_topic_updates(self) -> None:
        export_data = self.build_export_data()

        payload = build_browser_payload(export_data)
        messages = payload["threads"][0]["messages"]

        self.assertNotIn("content_html", messages[0])
        self.assertEqual(messages[1]["content_html"], "<value>New Topic</value>")
        self.assertEqual(messages[2]["attachments"][0]["name"], "report.pdf")
        self.assertTrue(payload["threads"][0]["csv_path"].endswith(".csv"))

    def test_generated_html_uses_clear_filters_and_message_targets(self) -> None:
        export_data = self.build_export_data()

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "browser.html"
            build_browser(export_data, output_path)
            html = output_path.read_text(encoding="utf-8")

        self.assertIn("Clear Filters", html)
        self.assertNotIn("Clear Range", html)
        self.assertIn("data-message-id", html)
        self.assertIn("focusMessageId", html)
        self.assertIn("centerElementInContainer", html)

    def test_generated_html_preserves_display_name_suffixes(self) -> None:
        export_data = self.build_export_data()
        export_data["profile"]["display_name"] = "Example User (FCS)"
        export_data["threads"][0]["messages"][0]["sender_display_name"] = "Alice (FCS)"

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "browser.html"
            build_browser(export_data, output_path)
            html = output_path.read_text(encoding="utf-8")

        self.assertIn("Alice (FCS)", html)
        self.assertIn("Example User (FCS)", html)
        self.assertIn("function normalizeTextValue", html)
        self.assertNotIn('.replace(/\\\\s*\\\\(FCS\\\\)/g, "")', html)


if __name__ == "__main__":
    unittest.main()
