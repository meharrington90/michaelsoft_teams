import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from export_teams_ccl_canonical import extract_message_reactions


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


if __name__ == "__main__":
    unittest.main()
