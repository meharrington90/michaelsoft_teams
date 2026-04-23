#!/usr/bin/env python3

import argparse
from pathlib import Path

from dump_teams_indexeddb_ccl import iter_wrapper_databases, load_ccl, resolve_teams_source
from teams_ccl_common import decode_output_context, write_json


def safe_get_store(db, store_name: str):
    try:
        return db[store_name]
    except Exception:
        return None


def build_sample(label: str, sample: dict | None) -> dict | None:
    if not sample:
        return None
    if label == "people":
        return {
            "DisplayName": sample.get("DisplayName"),
            "EmailAddresses": sample.get("EmailAddresses"),
            "ExternalDirectoryObjectId": sample.get("ExternalDirectoryObjectId"),
        }
    if label == "conversations":
        return {
            "id": sample.get("id"),
            "type": sample.get("type"),
            "title": sample.get("title"),
            "member_count": len(sample.get("members", [])),
        }
    if label == "replychains":
        message_map = sample.get("messageMap") or {}
        first_message = next(iter(message_map.values()), {})
        return {
            "conversationId": sample.get("conversationId"),
            "replyChainId": sample.get("replyChainId"),
            "messageMap_count": len(message_map),
            "first_message": {
                "id": first_message.get("id"),
                "imDisplayName": first_message.get("imDisplayName"),
                "messageType": first_message.get("messageType"),
                "content_preview": (first_message.get("content") or "")[:300],
            },
        }
    if label == "call_history":
        return {
            "id": sample.get("id"),
            "callDirection": sample.get("callDirection"),
            "callType": sample.get("callType"),
            "callState": sample.get("callState"),
            "originator": (sample.get("originatorParticipant") or {}).get("displayName"),
            "target": (sample.get("targetParticipant") or {}).get("displayName"),
        }
    return sample


def collect_store_stats(store, label: str, show_decode_errors: bool = True) -> tuple[dict, dict | None]:
    record_count = 0
    sample = None
    extra_counts: dict[str, int] = {}
    with decode_output_context(show_decode_errors):
        for record in store.iterate_records(errors_to_stdout=True):
            value = record.value or {}
            record_count += 1
            if sample is None:
                sample = value
            if label == "replychains":
                message_map = value.get("messageMap") or {}
                if message_map:
                    extra_counts["messages_total"] = extra_counts.get("messages_total", 0) + len(message_map)
                    extra_counts["threads_with_messages"] = extra_counts.get("threads_with_messages", 0) + 1

    summary = {"found": True, "record_count": record_count, **extra_counts}
    return summary, build_sample(label, sample)


def build_summary(root: Path | str | None = None, show_decode_errors: bool = True) -> dict:
    source = resolve_teams_source(root)
    leveldb_path = source.leveldb_path
    blob_path = source.blob_path
    ccl = load_ccl()
    wrapper = ccl.WrappedIndexDB(str(leveldb_path), str(blob_path) if blob_path.exists() else None)

    summary = {
        "backend": "ccl_chromium_reader.wrapper",
        "platform": source.platform_name,
        "search_root": str(source.search_root),
        "profile_root": str(source.profile_root),
        "leveldb_path": str(leveldb_path),
        "blob_path": str(blob_path) if blob_path.exists() else None,
        "local_storage_dir": str(source.local_storage_dir) if source.local_storage_dir else None,
        "discovery_method": source.discovery_method,
        "databases_total": 0,
        "key_stores": {},
        "samples": {},
    }

    targets = {
        "people": ("Teams:substrate-suggestions-manager", "people"),
        "conversations": ("Teams:conversation-manager", "conversations"),
        "replychains": ("Teams:replychain-manager", "replychains"),
        "call_history": ("Teams:call-history-manager", "call-history"),
        "threads_internal": ("Teams:messaging-slice-manager", "threads-internal-items"),
        "drafts_internal": ("Teams:messaging-slice-manager", "drafts-internal-items"),
        "system_messages": ("Teams:channel-info-pane-manager", "system-messages-store"),
    }

    dbs = iter_wrapper_databases(wrapper)
    summary["databases_total"] = len(dbs)
    available_stores = {}
    for _, db in dbs:
        db_name = getattr(db, "name", "") or ""
        for label, (db_prefix, store_name) in targets.items():
            if label in available_stores:
                continue
            if not db_name.startswith(db_prefix):
                continue
            store = safe_get_store(db, store_name)
            if store is not None:
                available_stores[label] = store

    for label, (db_prefix, store_name) in targets.items():
        matched = available_stores.get(label)
        if matched is None:
            summary["key_stores"][label] = {"found": False}
            continue

        store_summary, sample = collect_store_stats(matched, label, show_decode_errors=show_decode_errors)
        summary["key_stores"][label] = store_summary
        if sample is not None:
            summary["samples"][label] = sample

    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize key Teams IndexedDB stores using ccl_chromium_reader.")
    parser.add_argument("--root", help="Teams source root, profile directory, copied evidence root, or IndexedDB directory.")
    parser.add_argument("--output", default="teams_ccl_summary.json", help="Path to write JSON output.")
    args = parser.parse_args()

    payload = build_summary(Path(args.root).resolve() if args.root else None)
    write_json(Path(args.output).resolve(), payload)


if __name__ == "__main__":
    main()
