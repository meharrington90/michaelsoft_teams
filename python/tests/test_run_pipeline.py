import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from run_teams_pipeline import run_pipeline


class RunPipelineTests(unittest.TestCase):
    def test_run_pipeline_reuses_export_store_summary(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = Path(temp_dir)
            source_root = output_root / "source-profile"
            prepared = SimpleNamespace(
                active_source=SimpleNamespace(
                    platform_name="macos",
                    search_root=source_root,
                    profile_root=source_root,
                    leveldb_path=source_root / "IndexedDB" / "db.leveldb",
                    blob_path=source_root / "IndexedDB" / "db.blob",
                    local_storage_dir=None,
                    discovery_method="profile-root",
                ),
                live_source=None,
                archive_root=None,
                archive_manifest_path=None,
                used_archive=False,
                refreshed_archive=False,
            )
            export_data = {
                "_store_summary": {
                    "backend": "ccl_chromium_reader.wrapper",
                    "platform": "macos",
                    "search_root": str(source_root),
                    "profile_root": str(source_root),
                    "leveldb_path": str(source_root / "IndexedDB" / "db.leveldb"),
                    "blob_path": None,
                    "local_storage_dir": None,
                    "discovery_method": "profile-root",
                    "databases_total": 1,
                    "key_stores": {"people": {"found": True, "record_count": 1}},
                    "samples": {},
                },
                "summary": {"threads_total": 0, "messages_total": 0, "calls_total": 0, "people_total": 0},
                "threads": [],
                "calls": [],
                "guid_directory": {},
                "limitations": [],
            }

            with (
                patch("run_teams_pipeline.prepare_pipeline_source", return_value=prepared),
                patch("run_teams_pipeline.build_export", return_value=dict(export_data)) as build_export_mock,
                patch("run_teams_pipeline.export_conversations") as export_conversations_mock,
                patch("run_teams_pipeline.export_calls") as export_calls_mock,
                patch("run_teams_pipeline.build_browser") as build_browser_mock,
                patch("run_teams_pipeline.load_archive_manifest", return_value=None),
            ):
                manifest = run_pipeline(None, output_root)

            build_export_mock.assert_called_once_with(source_root, show_decode_errors=False, collect_store_summary=True)
            export_conversations_mock.assert_called_once()
            export_calls_mock.assert_called_once()
            build_browser_mock.assert_called_once()

            summary_payload = json.loads((output_root / "teams_ccl_summary.json").read_text(encoding="utf-8"))
            canonical_payload = json.loads((output_root / "teams_ccl_canonical_v1.json").read_text(encoding="utf-8"))

            self.assertEqual(summary_payload["databases_total"], 1)
            self.assertNotIn("_store_summary", canonical_payload)
            self.assertEqual(manifest["artifacts"]["summary_json"], str(output_root / "teams_ccl_summary.json"))


if __name__ == "__main__":
    unittest.main()
