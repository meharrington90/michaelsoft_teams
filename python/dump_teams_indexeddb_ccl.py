#!/usr/bin/env python3

import argparse
import json
import os
import platform
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TARGET_LEVELDB_DIR = "https_teams.microsoft.com_0.indexeddb.leveldb"
TARGET_BLOB_DIR = "https_teams.microsoft.com_0.indexeddb.blob"
PROFILE_PRIORITY = {"WV2Profile_tfw": 0, "Default": 1}
REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ARCHIVE_ROOT = REPO_ROOT / "Library" / "TeamsSourceArchive"


@dataclass(frozen=True)
class TeamsSourcePaths:
    platform_name: str
    search_root: Path
    profile_root: Path
    leveldb_path: Path
    blob_path: Path
    local_storage_dir: Path | None
    discovery_method: str


@dataclass(frozen=True)
class PreparedTeamsSource:
    active_source: TeamsSourcePaths
    live_source: TeamsSourcePaths | None
    archive_root: Path | None
    archive_manifest_path: Path | None
    used_archive: bool
    refreshed_archive: bool


def detect_platform() -> str:
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    if system == "windows":
        return "windows"
    return system or "unknown"


def default_archive_root() -> Path:
    return SOURCE_ARCHIVE_ROOT


def archive_current_root(archive_root: Path | None = None) -> Path:
    base = Path(archive_root).expanduser().resolve() if archive_root else default_archive_root()
    return base / "current"


def archive_profile_root(archive_root: Path | None = None) -> Path:
    return archive_current_root(archive_root) / "profile"


def archive_manifest_path(archive_root: Path | None = None) -> Path:
    return archive_current_root(archive_root) / "archive_manifest.json"


def path_is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def is_archive_source(path: Path, archive_root: Path | None = None) -> bool:
    return path_is_within(path, archive_current_root(archive_root))


def default_search_roots() -> list[Path]:
    override = os.environ.get("TEAMS_CCL_ROOT")
    if override:
        return [Path(override).expanduser()]

    home = Path.home()
    platform_name = detect_platform()

    if platform_name == "macos":
        return [home / "Library/Containers/com.microsoft.teams2/Data/Library"]

    if platform_name == "windows":
        roots = []
        appdata = os.environ.get("APPDATA")
        localappdata = os.environ.get("LOCALAPPDATA")
        if appdata:
            roots.append(Path(appdata) / "Microsoft/Teams")
        if localappdata:
            roots.append(Path(localappdata) / "Microsoft/MSTeams")
            roots.append(Path(localappdata) / "Packages/MSTeams_8wekyb3d8bbwe/LocalCache")
        return roots

    return []


def source_candidates(root: Path | str | None = None) -> list[Path]:
    return [Path(root).expanduser()] if root is not None else default_search_roots()


def candidate_profile_dirs(search_root: Path) -> list[Path]:
    candidates = [
        search_root,
        search_root / "EBWebView/WV2Profile_tfw",
        search_root / "EBWebView/Default",
        search_root / "Application Support/Microsoft/MSTeams/EBWebView/WV2Profile_tfw",
        search_root / "Application Support/Microsoft/MSTeams/EBWebView/Default",
        search_root / "Library/Application Support/Microsoft/MSTeams/EBWebView/WV2Profile_tfw",
        search_root / "Library/Application Support/Microsoft/MSTeams/EBWebView/Default",
    ]
    ordered = []
    seen = set()
    for candidate in candidates:
        key = str(candidate)
        if key in seen:
            continue
        seen.add(key)
        ordered.append(candidate)
    return ordered


def build_source_paths(leveldb_path: Path, search_root: Path, discovery_method: str) -> TeamsSourcePaths:
    indexeddb_root = leveldb_path.parent
    profile_root = indexeddb_root.parent
    local_storage_dir = profile_root / "Local Storage/leveldb"
    return TeamsSourcePaths(
        platform_name=detect_platform(),
        search_root=search_root,
        profile_root=profile_root,
        leveldb_path=leveldb_path,
        blob_path=indexeddb_root / TARGET_BLOB_DIR,
        local_storage_dir=local_storage_dir if local_storage_dir.exists() else None,
        discovery_method=discovery_method,
    )


def score_leveldb_path(leveldb_path: Path) -> tuple[int, int, int, str]:
    profile_root = leveldb_path.parent.parent
    local_storage_dir = profile_root / "Local Storage/leveldb"
    return (
        PROFILE_PRIORITY.get(profile_root.name, 99),
        0 if local_storage_dir.exists() else 1,
        len(leveldb_path.parts),
        str(leveldb_path),
    )


def discover_from_root(search_root: Path) -> TeamsSourcePaths | None:
    root = search_root.expanduser().resolve()
    if not root.exists():
        return None

    if root.name == TARGET_LEVELDB_DIR and root.is_dir():
        return build_source_paths(root, root, "explicit-leveldb")

    if (root / TARGET_LEVELDB_DIR).is_dir():
        return build_source_paths(root / TARGET_LEVELDB_DIR, root, "indexeddb-root")

    if (root / "IndexedDB" / TARGET_LEVELDB_DIR).is_dir():
        return build_source_paths(root / "IndexedDB" / TARGET_LEVELDB_DIR, root, "profile-root")

    for candidate in candidate_profile_dirs(root):
        leveldb_path = candidate / "IndexedDB" / TARGET_LEVELDB_DIR
        if leveldb_path.is_dir():
            return build_source_paths(leveldb_path, root, "known-layout")

    matches = sorted(
        (path for path in root.rglob(TARGET_LEVELDB_DIR) if path.is_dir()),
        key=score_leveldb_path,
    )
    if matches:
        return build_source_paths(matches[0], root, "recursive-search")
    return None


def resolve_source_from_candidates(candidates: list[Path], missing_message: str) -> TeamsSourcePaths:
    if not candidates:
        raise SystemExit(missing_message)

    for candidate in candidates:
        result = discover_from_root(candidate)
        if result is not None:
            return result

    searched = "\n".join(f"- {candidate}" for candidate in candidates)
    raise SystemExit(
        "Teams IndexedDB LevelDB path not found.\n"
        "Searched these roots:\n"
        f"{searched}\n"
        f"Expected to find a `{TARGET_LEVELDB_DIR}` directory under one of them."
    )


def resolve_live_teams_source(root: Path | str | None = None) -> TeamsSourcePaths:
    return resolve_source_from_candidates(
        source_candidates(root),
        "Unable to determine a default Teams data location for this platform.\n"
        "Pass --root with a Teams profile root, copied evidence root, or IndexedDB path.",
    )


def discover_archive_source(archive_root: Path | None = None) -> TeamsSourcePaths | None:
    current_root = archive_current_root(archive_root)
    for candidate in [archive_profile_root(archive_root), current_root]:
        result = discover_from_root(candidate)
        if result is not None:
            return build_source_paths(result.leveldb_path, current_root, "repo-archive-fallback")
    return None


def load_archive_manifest(archive_root: Path | None = None) -> dict | None:
    path = archive_manifest_path(archive_root)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def refresh_source_archive(source: TeamsSourcePaths, archive_root: Path | None = None) -> TeamsSourcePaths:
    if is_archive_source(source.profile_root, archive_root):
        return source

    base = Path(archive_root).expanduser().resolve() if archive_root else default_archive_root()
    current_root = archive_current_root(base)
    staging_root = base / ".staging"
    previous_root = base / ".previous"
    base.mkdir(parents=True, exist_ok=True)
    if staging_root.exists():
        shutil.rmtree(staging_root)
    if previous_root.exists():
        shutil.rmtree(previous_root)

    staging_root.mkdir(parents=True, exist_ok=True)
    staging_profile = staging_root / "profile"
    shutil.copytree(source.profile_root, staging_profile, copy_function=shutil.copy2)

    metadata = {
        "created_at": datetime.now(tz=timezone.utc).isoformat(),
        "platform": source.platform_name,
        "search_root": str(source.search_root),
        "source_root": str(source.profile_root),
        "leveldb_path": str(source.leveldb_path),
        "blob_path": str(source.blob_path) if source.blob_path.exists() else None,
        "local_storage_dir": str(source.local_storage_dir) if source.local_storage_dir else None,
        "discovery_method": source.discovery_method,
        "archive_profile_root": str(archive_profile_root(base)),
    }
    (staging_root / "archive_manifest.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    try:
        if current_root.exists():
            current_root.rename(previous_root)
        staging_root.rename(current_root)
    except Exception:
        if current_root.exists():
            shutil.rmtree(current_root)
        if previous_root.exists():
            previous_root.rename(current_root)
        raise
    else:
        if previous_root.exists():
            shutil.rmtree(previous_root)
    finally:
        if staging_root.exists():
            shutil.rmtree(staging_root)

    archived_leveldb = archive_profile_root(base) / "IndexedDB" / TARGET_LEVELDB_DIR
    return build_source_paths(archived_leveldb, current_root, "repo-archive-refresh")


def prepare_pipeline_source(
    root: Path | str | None = None,
    *,
    refresh_archive: bool = True,
    archive_root: Path | None = None,
) -> PreparedTeamsSource:
    archive_base = Path(archive_root).expanduser().resolve() if archive_root else default_archive_root()

    if root is not None:
        resolved = resolve_live_teams_source(root)
        if refresh_archive and not is_archive_source(resolved.profile_root, archive_base):
            archived = refresh_source_archive(resolved, archive_base)
            return PreparedTeamsSource(
                active_source=archived,
                live_source=resolved,
                archive_root=archive_base,
                archive_manifest_path=archive_manifest_path(archive_base),
                used_archive=True,
                refreshed_archive=True,
            )
        used_archive = is_archive_source(resolved.profile_root, archive_base)
        return PreparedTeamsSource(
            active_source=resolved,
            live_source=None if used_archive else resolved,
            archive_root=archive_base if used_archive else None,
            archive_manifest_path=archive_manifest_path(archive_base) if used_archive else None,
            used_archive=used_archive,
            refreshed_archive=False,
        )

    try:
        live_source = resolve_live_teams_source()
    except SystemExit:
        live_source = None

    if live_source is not None:
        if refresh_archive:
            archived = refresh_source_archive(live_source, archive_base)
            return PreparedTeamsSource(
                active_source=archived,
                live_source=live_source,
                archive_root=archive_base,
                archive_manifest_path=archive_manifest_path(archive_base),
                used_archive=True,
                refreshed_archive=True,
            )
        return PreparedTeamsSource(
            active_source=live_source,
            live_source=live_source,
            archive_root=None,
            archive_manifest_path=None,
            used_archive=False,
            refreshed_archive=False,
        )

    archived_source = discover_archive_source(archive_base)
    if archived_source is None:
        raise SystemExit(
            "Teams IndexedDB LevelDB path not found in the live default roots, and no repo archive copy is available.\n"
            f"Expected an archive under: {archive_current_root(archive_base)}"
        )
    return PreparedTeamsSource(
        active_source=archived_source,
        live_source=None,
        archive_root=archive_base,
        archive_manifest_path=archive_manifest_path(archive_base),
        used_archive=True,
        refreshed_archive=False,
    )


def resolve_teams_source(root: Path | str | None = None) -> TeamsSourcePaths:
    if root is not None:
        return resolve_live_teams_source(root)

    try:
        return resolve_live_teams_source()
    except SystemExit as live_error:
        archived = discover_archive_source()
        if archived is not None:
            return archived
        archive_root = archive_current_root()
        raise SystemExit(f"{live_error}\nNo repo archive copy was found under:\n- {archive_root}") from None


def find_default_paths(root: Path | str | None = None) -> tuple[Path, Path]:
    source = resolve_teams_source(root)
    return source.leveldb_path, source.blob_path


def find_local_storage_dir(root: Path | str | None = None) -> Path | None:
    return resolve_teams_source(root).local_storage_dir


def load_ccl() -> Any:
    try:
        from ccl_chromium_reader import ccl_chromium_indexeddb
    except ImportError as exc:  # pragma: no cover - dependency is optional in this workspace
        repo_root = Path(__file__).resolve().parents[1]
        candidates = []
        for env_name in [".venv", ".venv-ccl"]:
            env_root = repo_root / env_name
            candidates.extend(sorted((env_root / "lib").glob("python*/site-packages")))
            windows_site_packages = env_root / "Lib" / "site-packages"
            if windows_site_packages.exists():
                candidates.append(windows_site_packages)
        for candidate in candidates:
            if str(candidate) not in sys.path:
                sys.path.insert(0, str(candidate))
        try:
            from ccl_chromium_reader import ccl_chromium_indexeddb
        except ImportError:
            raise SystemExit(
                "Optional dependency missing: ccl_chromium_reader.\n"
                "This backend is provided for structured IndexedDB decoding when the CCL Chromium reader stack is installed."
            ) from exc
    return ccl_chromium_indexeddb


def serialize_value(value: Any, depth: int = 0) -> Any:
    if depth > 6:
        return repr(value)
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (bytes, bytearray)):
        return {"type": "bytes", "length": len(value), "preview_hex": bytes(value[:32]).hex()}
    if isinstance(value, list | tuple):
        return [serialize_value(item, depth + 1) for item in value]
    if isinstance(value, dict):
        return {str(key): serialize_value(item, depth + 1) for key, item in value.items()}

    result: dict[str, Any] = {"__class__": value.__class__.__name__}
    for attr in ["blob_number", "mime_type", "size", "file_name", "last_modified", "db_id", "obj_store_id"]:
        if hasattr(value, attr):
            result[attr] = serialize_value(getattr(value, attr), depth + 1)

    public_attrs = {}
    for name in dir(value):
        if name.startswith("_"):
            continue
        if name in result:
            continue
        try:
            attr_value = getattr(value, name)
        except Exception:
            continue
        if callable(attr_value):
            continue
        if name in {"value", "record_location", "ldb_key"}:
            continue
        public_attrs[name] = serialize_value(attr_value, depth + 1)

    if public_attrs:
        result["attrs"] = public_attrs
        return result
    return repr(value)


def iter_wrapper_databases(wrapper: Any) -> list[tuple[Any, Any]]:
    databases = []
    database_ids = getattr(wrapper, "database_ids", [])
    for item in database_ids:
        db_id = getattr(item, "dbid_no", item)
        try:
            db = wrapper[db_id]
        except Exception:
            continue
        databases.append((item, db))
    return databases


def dump_with_wrapper(ccl: Any, leveldb_path: Path, blob_path: Path | None) -> dict:
    wrapper = ccl.WrappedIndexDB(str(leveldb_path), str(blob_path) if blob_path and blob_path.exists() else None)
    payload = {
        "backend": "ccl_chromium_reader.wrapper",
        "leveldb_path": str(leveldb_path),
        "blob_path": str(blob_path) if blob_path and blob_path.exists() else None,
        "databases": [],
    }

    for db_meta, db in iter_wrapper_databases(wrapper):
        db_entry = {
            "db_id": getattr(db_meta, "dbid_no", db_meta),
            "db_name": getattr(db, "name", None),
            "origin": getattr(db, "origin", None),
            "object_stores": [],
        }
        store_names = getattr(db, "object_store_names", [])
        for store_name in store_names:
            try:
                store = db[store_name]
            except Exception:
                continue
            records = []
            for record in store.iterate_records(errors_to_stdout=True):
                record_entry = {
                    "user_key": serialize_value(getattr(record, "user_key", None)),
                    "value": serialize_value(getattr(record, "value", None)),
                }
                external = getattr(record, "external_objects", None)
                if external:
                    record_entry["external_objects"] = serialize_value(external)
                records.append(record_entry)
            db_entry["object_stores"].append({"name": store_name, "records": records})
        payload["databases"].append(db_entry)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Optional CCL-backed Teams IndexedDB dumper.")
    parser.add_argument("--root", help="Teams source root, profile directory, copied evidence root, or IndexedDB directory.")
    parser.add_argument("--leveldb", help="Path to the Teams IndexedDB .leveldb folder.")
    parser.add_argument("--blob-dir", help="Path to the matching Teams IndexedDB .blob folder.")
    parser.add_argument("--output", default="teams_indexeddb_ccl_dump.json", help="Path to write JSON output.")
    args = parser.parse_args()

    default_leveldb, default_blob = find_default_paths(args.root)
    leveldb_path = Path(args.leveldb).resolve() if args.leveldb else default_leveldb
    blob_path = Path(args.blob_dir).resolve() if args.blob_dir else default_blob

    if not leveldb_path.exists():
        raise SystemExit(f"IndexedDB LevelDB path not found: {leveldb_path}")

    ccl = load_ccl()
    payload = dump_with_wrapper(ccl, leveldb_path, blob_path if blob_path.exists() else None)
    Path(args.output).resolve().write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
