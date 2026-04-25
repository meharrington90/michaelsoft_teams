import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from build_teams_ccl_browser import build_browser, build_browser_payload


class BuildBrowserPayloadTests(unittest.TestCase):
    def build_export_data(self) -> dict:
        return {
            "summary": {"threads_total": 1, "messages_total": 4, "calls_total": 0, "attachments_total": 1, "reactions_total": 3},
            "profile": {"oid": "user-1", "display_name": "Example User"},
            "threads": [
                {
                    "id": "19:thread@thread.v2",
                    "category": "thread",
                    "label": "Example Thread",
                    "message_count": 4,
                    "messages": [
                        {
                            "id": "m1",
                            "timestamp": "2025-01-01T00:00:00+00:00",
                            "sender_display_name": "Alice",
                            "sender_id": "user-2",
                            "message_type": "RichText/Html",
                            "content_html": "<div><strong>Hello</strong></div>",
                            "content_text": "Hello",
                            "reactions": [
                                {
                                    "key": "like",
                                    "count": 2,
                                    "users": [
                                        {"id": "user-1", "display_name": "Example User", "reacted_at": "2025-01-01T00:05:00+00:00"},
                                        {"id": "user-3", "display_name": "Bob", "reacted_at": "2025-01-01T00:06:00+00:00"},
                                    ],
                                },
                                {
                                    "key": "heart",
                                    "count": 1,
                                    "users": [
                                        {"id": "user-4", "display_name": "Cara", "reacted_at": "2025-01-01T00:07:00+00:00"},
                                    ],
                                },
                            ],
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
                        {
                            "id": "m4",
                            "timestamp": "2025-01-01T00:03:00+00:00",
                            "sender_display_name": "Alice",
                            "sender_id": "user-2",
                            "message_type": "RichText/Html",
                            "content_html": (
                                '<blockquote itemscope itemtype="http://schema.skype.com/Reply" itemid="m1">'
                                '<strong itemprop="mri">Example User</strong>'
                                '<p itemprop="preview">Hello</p>'
                                "</blockquote>"
                                "<p>Follow up</p>"
                            ),
                            "content_text": "Example User Hello Follow up",
                            "quality": "curated",
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

    def test_payload_keeps_html_for_topic_updates_and_reply_quotes(self) -> None:
        export_data = self.build_export_data()

        payload = build_browser_payload(export_data)
        messages = payload["threads"][0]["messages"]

        self.assertNotIn("content_html", messages[0])
        self.assertEqual(messages[1]["content_html"], "<value>New Topic</value>")
        self.assertIn("content_html", messages[3])
        self.assertIn("schema.skype.com/Reply", messages[3]["content_html"])
        self.assertEqual(messages[0]["reactions"][0]["key"], "like")
        self.assertEqual(messages[0]["reactions"][0]["users"][0]["display_name"], "Example User")
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
        self.assertIn("function offsetTopWithinContainer", html)
        self.assertIn("function centerSidebarListRow", html)
        self.assertIn("function centerMainTimelineRow", html)
        self.assertIn("function openCallView", html)
        self.assertIn('revealActiveListRow(callList', html)
        self.assertIn("function messageReplyQuote", html)
        self.assertIn("reply-quote", html)
        self.assertIn("reaction-bubble", html)
        self.assertIn("function renderMessageReactions", html)
        self.assertIn("sumAttachments", html)
        self.assertIn("sumReactions", html)
        self.assertIn("Example User", html)
        self.assertIn("👍", html)
        self.assertNotIn("contain-intrinsic-size: 108px;", html)
        self.assertNotIn("contain-intrinsic-size: 144px;", html)

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
