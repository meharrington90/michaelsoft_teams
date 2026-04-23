import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dump_teams_indexeddb_ccl import (
    TARGET_BLOB_DIR,
    TARGET_LEVELDB_DIR,
    archive_manifest_path,
    build_source_paths,
    prepare_pipeline_source,
    refresh_source_archive,
)


def create_fake_profile(root: Path) -> Path:
    profile_root = root / "WV2Profile_tfw"
    leveldb_dir = profile_root / "IndexedDB" / TARGET_LEVELDB_DIR
    blob_dir = profile_root / "IndexedDB" / TARGET_BLOB_DIR
    local_storage_dir = profile_root / "Local Storage" / "leveldb"
    leveldb_dir.mkdir(parents=True, exist_ok=True)
    blob_dir.mkdir(parents=True, exist_ok=True)
    local_storage_dir.mkdir(parents=True, exist_ok=True)
    (leveldb_dir / "000003.log").write_text("leveldb", encoding="utf-8")
    (blob_dir / "1").write_text("blob", encoding="utf-8")
    (local_storage_dir / "000004.log").write_text("profile", encoding="utf-8")
    return profile_root


class SourceArchiveTests(unittest.TestCase):
    def test_refresh_source_archive_copies_profile_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            profile_root = create_fake_profile(temp_root / "live")
            archive_root = temp_root / "archive"
            source = build_source_paths(profile_root / "IndexedDB" / TARGET_LEVELDB_DIR, temp_root / "live", "test-live")

            archived = refresh_source_archive(source, archive_root=archive_root)

            self.assertTrue((archived.profile_root / "IndexedDB" / TARGET_LEVELDB_DIR / "000003.log").exists())
            self.assertTrue((archived.profile_root / "Local Storage" / "leveldb" / "000004.log").exists())
            self.assertEqual(archived.discovery_method, "repo-archive-refresh")

            metadata = json.loads(archive_manifest_path(archive_root).read_text(encoding="utf-8"))
            self.assertEqual(metadata["source_root"], str(source.profile_root))

    def test_prepare_pipeline_source_falls_back_to_existing_archive(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            profile_root = create_fake_profile(temp_root / "live")
            archive_root = temp_root / "archive"
            source = build_source_paths(profile_root / "IndexedDB" / TARGET_LEVELDB_DIR, temp_root / "live", "test-live")
            refresh_source_archive(source, archive_root=archive_root)

            with patch.dict(os.environ, {"TEAMS_CCL_ROOT": str(temp_root / "missing-live-root")}, clear=False):
                prepared = prepare_pipeline_source(archive_root=archive_root)

            self.assertTrue(prepared.used_archive)
            self.assertFalse(prepared.refreshed_archive)
            self.assertIsNone(prepared.live_source)
            self.assertEqual(prepared.active_source.profile_root.resolve(), (archive_root / "current" / "profile").resolve())


if __name__ == "__main__":
    unittest.main()
