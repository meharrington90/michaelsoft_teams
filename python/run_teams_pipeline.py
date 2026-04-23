#!/usr/bin/env python3

import argparse
import webbrowser
from pathlib import Path

from build_teams_ccl_browser import build_browser
from dump_teams_indexeddb_ccl import load_archive_manifest, prepare_pipeline_source
from export_teams_ccl_canonical import build_export
from export_teams_ccl_csv import export_calls, export_conversations
from teams_ccl_common import ensure_dir, write_json


def print_stage(number: int, total: int, message: str) -> None:
    print()
    print(f"[{number}/{total}] {message}")


def run_pipeline(root: Path | str | None, output_root: Path, *, refresh_source_archive: bool = True) -> dict:
    prepared = prepare_pipeline_source(root, refresh_archive=refresh_source_archive)
    source = prepared.active_source
    source_root = source.profile_root
    discovery_root = source_root

    ensure_dir(output_root)
    csv_dir = output_root / "teams_ccl_csv_v1"
    ensure_dir(csv_dir)

    print("Starting Teams export pipeline")
    if prepared.live_source is not None:
        print(f"Live source profile: {prepared.live_source.profile_root}")
    if prepared.refreshed_archive:
        print(f"Local archive snapshot refreshed: {source_root}")
    elif prepared.used_archive:
        print(f"Using local archive snapshot: {source_root}")
    else:
        print(f"Source profile: {source_root}")

    print_stage(1, 3, "Scanning IndexedDB stores and assembling export data...")
    export_data = build_export(discovery_root, show_decode_errors=False, collect_store_summary=True)
    summary = export_data.pop("_store_summary")
    summary_path = output_root / "teams_ccl_summary.json"
    write_json(summary_path, summary)

    print_stage(2, 3, "Writing the canonical JSON dataset and CSV files...")
    canonical_path = output_root / "teams_ccl_canonical_v1.json"
    write_json(canonical_path, export_data, pretty=False)
    export_conversations(export_data, csv_dir)
    export_calls(export_data, csv_dir)
    write_json(csv_dir / "export_summary.json", export_data.get("summary") or {})

    print_stage(3, 3, "Building the standalone browser viewer...")
    browser_path = output_root / "teams_ccl_browser_v1.html"
    build_browser(export_data, browser_path)

    archive_manifest = load_archive_manifest(prepared.archive_root) if prepared.archive_root else None
    manifest = {
        "platform": source.platform_name,
        "search_root": str(source.search_root),
        "source_root": str(source_root),
        "leveldb_path": str(source.leveldb_path),
        "blob_path": str(source.blob_path) if source.blob_path.exists() else None,
        "local_storage_dir": str(source.local_storage_dir) if source.local_storage_dir else None,
        "discovery_method": source.discovery_method,
        "live_source_root": str(prepared.live_source.profile_root) if prepared.live_source else None,
        "live_leveldb_path": str(prepared.live_source.leveldb_path) if prepared.live_source else None,
        "source_archive": {
            "used_archive": prepared.used_archive,
            "refreshed_archive": prepared.refreshed_archive,
            "archive_root": str(prepared.archive_root) if prepared.archive_root else None,
            "archive_manifest_path": str(prepared.archive_manifest_path) if prepared.archive_manifest_path and prepared.archive_manifest_path.exists() else None,
            "source_root": archive_manifest.get("source_root") if archive_manifest else None,
            "created_at": archive_manifest.get("created_at") if archive_manifest else None,
        },
        "artifacts": {
            "summary_json": str(summary_path),
            "canonical_json": str(canonical_path),
            "csv_dir": str(csv_dir),
            "browser_html": str(browser_path),
        },
    }
    write_json(output_root / "run_manifest.json", manifest)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the full Teams CCL pipeline with automatic local-source discovery.")
    parser.add_argument("--root", help="Optional Teams source root, profile directory, copied evidence root, or IndexedDB directory.")
    parser.add_argument("--output-root", default="teams_pipeline_output", help="Directory for all generated artifacts.")
    parser.add_argument("--open-browser", action="store_true", help="Open the generated HTML viewer after a successful run.")
    parser.add_argument("--skip-source-archive", action="store_true", help="Run directly from the discovered source instead of refreshing the repo-local archive copy.")
    args = parser.parse_args()

    output_root = Path(args.output_root).expanduser().resolve()
    manifest = run_pipeline(
        Path(args.root).expanduser().resolve() if args.root else None,
        output_root,
        refresh_source_archive=not args.skip_source_archive,
    )
    browser_path = Path(manifest["artifacts"]["browser_html"])

    if args.open_browser:
        print()
        print("Opening the browser viewer...")
        webbrowser.open(browser_path.resolve().as_uri())

    print()
    print("Completed.")
    print(f"Output folder: {output_root}")
    print(f"Browser viewer: {browser_path}")


if __name__ == "__main__":
    main()
