#!/usr/bin/env python3

import argparse
import csv
import json
from pathlib import Path

from teams_ccl_common import count_reactions, ensure_dir, read_json, thread_csv_filename


def load_export(path: Path) -> dict:
    return read_json(path)


def sort_key(message: dict) -> tuple[bool, str, str]:
    return (message.get("timestamp") is None, message.get("timestamp") or "", message.get("id") or "")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def reaction_count(reactions: list[dict] | None) -> int:
    return count_reactions(reactions)


def reaction_summary(reactions: list[dict] | None) -> str:
    parts = []
    for reaction in reactions or []:
        key = reaction.get("key")
        if not key:
            continue
        try:
            raw_count = int(reaction.get("count") or 0)
        except (TypeError, ValueError):
            raw_count = 0
        count = max(raw_count, len(reaction.get("users") or []))
        parts.append(f"{key}:{count}")
    return "; ".join(parts)


def export_conversations(export_data: dict, output_dir: Path) -> list[dict]:
    messages_dir = output_dir / "conversations"
    ensure_dir(messages_dir)

    manifest = []
    fields = [
        "thread_id",
        "thread_label",
        "thread_category",
        "metadata_quality",
        "message_id",
        "client_message_id",
        "timestamp",
        "sender_display_name",
        "sender_id",
        "message_type",
        "content_type",
        "quality",
        "content_text",
        "attachment_count",
        "attachment_names",
        "attachment_urls",
        "reaction_count",
        "reactions",
        "source",
    ]
    ordered_threads = sorted(export_data.get("threads", []), key=lambda thread: ((thread.get("label") or ""), thread.get("id") or ""))

    with (output_dir / "conversations_all_flat.csv").open("w", newline="", encoding="utf-8") as all_handle:
        all_writer = csv.DictWriter(all_handle, fieldnames=fields)
        all_writer.writeheader()

        for thread in ordered_threads:
            filename = thread_csv_filename(thread)
            thread_rows_written = 0
            thread_messages = sorted(thread.get("messages", []), key=sort_key)
            if thread_messages:
                with (messages_dir / filename).open("w", newline="", encoding="utf-8") as thread_handle:
                    thread_writer = csv.DictWriter(thread_handle, fieldnames=fields)
                    thread_writer.writeheader()

                    for message in thread_messages:
                        attachments = message.get("attachments") or []
                        reactions = message.get("reactions") or []
                        row = {
                            "thread_id": thread["id"],
                            "thread_label": thread.get("label"),
                            "thread_category": thread.get("category"),
                            "metadata_quality": thread.get("metadata_quality"),
                            "message_id": message.get("id"),
                            "client_message_id": message.get("client_message_id"),
                            "timestamp": message.get("timestamp"),
                            "sender_display_name": message.get("sender_display_name"),
                            "sender_id": message.get("sender_id"),
                            "message_type": message.get("message_type"),
                            "content_type": message.get("content_type"),
                            "quality": message.get("quality"),
                            "content_text": message.get("content_text"),
                            "attachment_count": len(attachments),
                            "attachment_names": "; ".join(
                                filter(None, (attachment.get("name") for attachment in attachments))
                            ),
                            "attachment_urls": "; ".join(
                                filter(
                                    None,
                                    (attachment.get("url") or attachment.get("preview_url") for attachment in attachments),
                                )
                            ),
                            "reaction_count": reaction_count(reactions),
                            "reactions": reaction_summary(reactions),
                            "source": message.get("source"),
                        }
                        thread_writer.writerow(row)
                        all_writer.writerow(row)
                        thread_rows_written += 1

            manifest.append(
                {
                    "thread_id": thread["id"],
                    "thread_label": thread.get("label"),
                    "thread_category": thread.get("category"),
                    "metadata_quality": thread.get("metadata_quality"),
                    "message_count": thread.get("message_count"),
                    "participant_count": len(thread.get("participants", [])),
                    "participants": "; ".join(thread.get("participants", [])),
                    "csv": str((messages_dir / filename).relative_to(output_dir)) if thread_rows_written else "",
                }
            )

    write_csv(
        output_dir / "conversation_manifest.csv",
        ["thread_id", "thread_label", "thread_category", "metadata_quality", "message_count", "participant_count", "participants", "csv"],
        manifest,
    )
    return manifest


def export_calls(export_data: dict, output_dir: Path) -> None:
    fields = [
        "call_id",
        "shared_correlation_id",
        "start_time",
        "connect_time",
        "end_time",
        "direction",
        "call_type",
        "call_state",
        "originator_display_name",
        "originator_id",
        "originator_endpoint",
        "originator_phone_number",
        "target_display_name",
        "target_id",
        "target_endpoint",
        "target_phone_number",
        "participant_display_names",
        "participant_ids",
        "conversation_id",
        "group_chat_thread_id",
        "meeting_subject",
        "meeting_start_time",
        "meeting_end_time",
        "meeting_series_kind",
        "quality",
        "summary_text",
        "source",
    ]
    with (output_dir / "call_history.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for call in export_data.get("calls", []):
            row = {field: call.get(field) for field in fields}
            row["participant_display_names"] = "; ".join(call.get("participant_display_names", []))
            row["participant_ids"] = "; ".join(call.get("participant_ids", []))
            writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser(description="Export the CCL canonical Teams JSON to per-conversation CSVs.")
    parser.add_argument("--input", default="teams_ccl_canonical_v1.json", help="Path to the canonical CCL JSON.")
    parser.add_argument("--output-dir", default="teams_ccl_csv_v1", help="Directory for CSV exports.")
    args = parser.parse_args()

    export_data = load_export(Path(args.input).resolve())
    output_dir = Path(args.output_dir).resolve()
    ensure_dir(output_dir)

    export_conversations(export_data, output_dir)
    export_calls(export_data, output_dir)
    (output_dir / "export_summary.json").write_text(json.dumps(export_data.get("summary") or {}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
