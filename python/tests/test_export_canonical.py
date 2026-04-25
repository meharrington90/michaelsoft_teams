import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from export_teams_ccl_canonical import extract_message_attachments, extract_message_reactions, merge_message_records


class ExportCanonicalReactionTests(unittest.TestCase):
    def test_extract_message_reactions_prefers_emotion_users_and_annotation_counts(self) -> None:
        raw = {
            "annotationsSummary": {"emotions": {"like": 2, "heart": 1}},
            "properties": {
                "emotions": [
                    {
                        "key": "like",
                        "users": [
                            {
                                "mri": "8:orgid:user-1f8e7c2a-0000-4000-8000-000000000001",
                                "time": 1735689900000,
                            }
                        ],
                    }
                ]
            },
        }
        guid_to_name = {"1f8e7c2a-0000-4000-8000-000000000001": "Example User"}

        reactions = extract_message_reactions(raw, guid_to_name)

        self.assertEqual(
            reactions,
            [
                {
                    "key": "like",
                    "count": 2,
                    "users": [
                        {
                            "id": "1f8e7c2a-0000-4000-8000-000000000001",
                            "display_name": "Example User",
                            "reacted_at": "2025-01-01T00:05:00+00:00",
                        }
                    ],
                },
                {
                    "key": "heart",
                    "count": 1,
                    "users": [],
                },
            ],
        )

    def test_extract_message_attachments_reads_multiple_teams_shapes(self) -> None:
        raw = {
            "attachments": [
                {
                    "id": "direct-1",
                    "name": "direct.pdf",
                    "contentUrl": "https://contoso.sharepoint.com/sites/example/direct.pdf",
                    "contentType": "application/pdf",
                }
            ],
            "properties": {
                "files": [
                    {
                        "itemid": "file-1",
                        "fileName": "photo.png",
                        "fileInfo": {"shareUrl": "https://contoso.sharepoint.com/sites/example/photo.png"},
                        "filePreview": {"previewUrl": "https://contoso.sharepoint.com/sites/example/photo-preview.png"},
                        "fileType": "png",
                    }
                ],
                "links": '{"items":[{"title":"deck.pptx","url":"https://contoso.sharepoint.com/sites/example/deck.pptx"}]}',
            },
        }
        html = '<a href="https://contoso.sharepoint.com/sites/example/report.xlsx">Report</a>'

        attachments = extract_message_attachments(raw, html)

        self.assertEqual([attachment["name"] for attachment in attachments], ["direct.pdf", "photo.png", "deck.pptx", "report.xlsx"])
        self.assertEqual(attachments[1]["kind"], "image")
        self.assertEqual(attachments[2]["kind"], "file")

    def test_merge_message_records_preserves_curated_text_and_lower_score_artifacts(self) -> None:
        curated = {
            "id": "m1",
            "quality": "curated",
            "content_text": "Short",
            "attachments": [{"name": "one.pdf", "url": "https://contoso.sharepoint.com/one.pdf", "kind": "file"}],
        }
        residual = {
            "id": "m1",
            "quality": "residual",
            "content_text": "Longer but lower quality residual content",
            "attachments": [{"name": "two.pdf", "url": "https://contoso.sharepoint.com/two.pdf", "kind": "file"}],
            "reactions": [{"key": "like", "count": 2, "users": []}],
        }

        merged = merge_message_records(curated, residual)

        self.assertEqual(merged["quality"], "curated")
        self.assertEqual(merged["content_text"], "Short")
        self.assertEqual([attachment["name"] for attachment in merged["attachments"]], ["one.pdf", "two.pdf"])
        self.assertEqual(merged["reactions"][0]["count"], 2)


if __name__ == "__main__":
    unittest.main()
