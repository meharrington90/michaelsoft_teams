#!/usr/bin/env python3

import argparse
import json
import re
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

from dump_teams_indexeddb_ccl import SUMMARY_TARGETS, get_target_stores, load_ccl, resolve_teams_source
from export_teams_ccl_summary import build_sample, collect_store_stats
from teams_ccl_common import (
    GUID_RE,
    classify_thread,
    clean_text,
    count_reactions,
    decode_output_context,
    html_to_text,
    init_thread_record,
    is_undefined_value,
    normalize_json_value,
    normalize_thread_id,
    parse_json_object,
    parse_profile,
    write_json,
)

EVENT_CALL_NAME_RE = re.compile(r"\b(callStarted|callEnded|callMissed|callAccepted|callRejected|callCancelled)\b", re.I)
EVENT_CALL_TRAILING_GUID_RE = re.compile(
    r"\b([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\b(?:\s+False)?\s*$",
    re.I,
)
EVENT_CALL_TIME_RE = re.compile(r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}(?: \+\d{2}:\d{2})?")
EVENT_CALL_URL_RE = re.compile(r"https://\S+")
EVENT_CALL_SERIES_KIND_RE = re.compile(r"(Occurrence|Exception|RecurringMaster|Recurring)\s*$", re.I)
GENERIC_PHONE_LABEL_RE = re.compile(
    r"^(?:WIRELESS CALLER|STATE[_ ]OF[_ ]ALASKA|UNKNOWN CALLER|ANONYMOUS|PRIVATE CALLER|EXTERNAL CALLER)$",
    re.I,
)
EVENT_CALL_PARTICIPANT_RE = re.compile(
    r"8:orgid:([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\s+(.+?)\s+(\d+)"
    r"(?=\s+8:orgid:|\s+[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|\s+\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2}|\s*$)",
    re.I,
)
EVENT_CALL_STATE_MAP = {
    "callstarted": "started",
    "callended": "ended",
    "callmissed": "missed",
    "callaccepted": "accepted",
    "callrejected": "rejected",
    "callcancelled": "cancelled",
}
EVENT_CALL_STATE_PRIORITY = {
    "started": 0,
    "accepted": 1,
    "ended": 2,
    "missed": 2,
    "rejected": 2,
    "cancelled": 2,
}
ATTACHMENT_IMAGE_TYPES = {"png", "jpg", "jpeg", "gif", "bmp", "webp", "heic", "heif", "tif", "tiff"}
ATTACHMENT_VIDEO_TYPES = {"mp4", "mov", "avi", "wmv", "m4v", "webm"}
ATTACHMENT_DOCUMENT_TYPES = {
    "csv",
    "doc",
    "docx",
    "key",
    "numbers",
    "pages",
    "pdf",
    "ppt",
    "pptx",
    "rtf",
    "txt",
    "xls",
    "xlsx",
    "zip",
}
ATTACHMENT_URL_HOST_HINTS = (
    "api.ams.",
    "api.asm.",
    "sharepoint.com",
    "onedrive.live.com",
    "1drv.ms",
)
MESSAGE_QUALITY_RANK = {
    "residual": 0,
    "event": 1,
    "attachment": 2,
    "curated": 3,
}


def safe_text(value) -> str | None:
    if isinstance(value, str):
        return clean_text(value)
    if isinstance(value, (bytes, bytearray)):
        return clean_text(bytes(value).decode("utf-8", "ignore"))
    return None


def first_text(*values) -> str | None:
    for value in values:
        cleaned = safe_text(value)
        if cleaned:
            return cleaned
    return None


def to_iso_from_millis(value) -> str | None:
    if value in {None, "", "<Undefined>"}:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    try:
        return datetime.fromtimestamp(number / 1000, tz=timezone.utc).isoformat()
    except (ValueError, OSError):
        return None


def extract_guid(value: str | None) -> str | None:
    if not value:
        return None
    match = GUID_RE.search(value)
    if not match:
        return None
    return match.group(0).lower()


def extract_guids(value: str | None) -> list[str]:
    if not value:
        return []
    seen = []
    for match in GUID_RE.finditer(value):
        guid = match.group(0).lower()
        if guid not in seen:
            seen.append(guid)
    return seen


def classify_quality(message_type: str | None, content_text: str | None) -> str:
    if message_type and message_type.startswith(("ThreadActivity/", "Event/")):
        return "event"
    if not content_text:
        return "residual"
    if len(content_text.strip()) <= 1:
        return "residual"
    return "curated"


def parse_json_list(value) -> list[dict]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        for nested_key in ("items", "files", "attachments", "value", "values"):
            nested = parse_json_list(value.get(nested_key))
            if nested:
                return nested
        attachment_like_keys = {
            "baseUrl",
            "contentUrl",
            "downloadUrl",
            "fileInfo",
            "filePreview",
            "fileUrl",
            "href",
            "objectUrl",
            "previewUrl",
            "shareUrl",
            "thumbnailUrl",
            "url",
        }
        if attachment_like_keys.intersection(value):
            return [value]
        return [item for item in value.values() if isinstance(item, dict)]
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return []
        if isinstance(parsed, (dict, list)):
            return parse_json_list(parsed)
    return []


def safe_dict(value) -> dict:
    if is_undefined_value(value):
        return {}
    return value if isinstance(value, dict) else {}


def file_name_from_url(value: str | None) -> str | None:
    cleaned = clean_text(value)
    if not cleaned:
        return None
    try:
        path = urlparse(cleaned).path or ""
    except ValueError:
        return None
    name = unquote(path.rsplit("/", 1)[-1]) if path else ""
    return clean_text(name) or None


def url_host(value: str | None) -> str:
    cleaned = clean_text(value)
    if not cleaned:
        return ""
    try:
        return (urlparse(cleaned).hostname or "").lower()
    except ValueError:
        return ""


def is_likely_attachment_url(value: str | None) -> bool:
    cleaned = clean_text(value)
    if not cleaned:
        return False
    host = url_host(cleaned)
    if any(hint in host for hint in ATTACHMENT_URL_HOST_HINTS):
        return True
    name = file_name_from_url(cleaned) or cleaned
    if "." not in name:
        return False
    extension = name.rsplit(".", 1)[-1].lower().split("?", 1)[0].split("#", 1)[0]
    return extension in ATTACHMENT_IMAGE_TYPES | ATTACHMENT_VIDEO_TYPES | ATTACHMENT_DOCUMENT_TYPES


def attachment_kind(name: str | None, url: str | None, file_type: str | None = None) -> str:
    raw_type = clean_text(file_type) or ""
    if raw_type.startswith("http://schema.skype.com/"):
        raw_type = raw_type.rsplit("/", 1)[-1]
    elif "/" in raw_type:
        raw_type = raw_type.rsplit("/", 1)[-1]
    raw_type = raw_type.lower()
    if not raw_type:
        source_name = clean_text(name) or file_name_from_url(url) or ""
        if "." in source_name:
            raw_type = source_name.rsplit(".", 1)[-1].lower()
    if raw_type in ATTACHMENT_IMAGE_TYPES or raw_type in {"amsimage", "inlineimage"}:
        return "image"
    if raw_type in ATTACHMENT_VIDEO_TYPES or raw_type == "amsvideo":
        return "video"
    return "file"


def attachment_identity_tokens(attachment: dict) -> set[str]:
    tokens = set()
    attachment_id = clean_text(attachment.get("id"))
    if attachment_id:
        tokens.add(f"id:{attachment_id.lower()}")
    for field in ("url", "preview_url"):
        link = clean_text(attachment.get(field))
        if link:
            tokens.add(f"url:{link}")
    return tokens


def append_attachment(attachments: list[dict], attachment: dict | None) -> None:
    if not isinstance(attachment, dict):
        return
    cleaned = {
        key: clean_text(value) if isinstance(value, str) else value
        for key, value in attachment.items()
        if value is not None and value != "" and value != []
    }
    if not cleaned.get("url") and not cleaned.get("preview_url"):
        return
    identity = attachment_identity_tokens(cleaned)
    if identity and any(identity & attachment_identity_tokens(existing) for existing in attachments):
        return
    attachments.append(cleaned)


def merge_attachment_lists(*attachment_lists: list[dict] | None) -> list[dict]:
    merged: list[dict] = []
    for attachments in attachment_lists:
        for attachment in attachments or []:
            append_attachment(merged, attachment)
    return merged


def attachment_from_object(item: dict) -> dict | None:
    if not isinstance(item, dict):
        return None

    file_info = item.get("fileInfo") or item.get("file_info") or {}
    preview = item.get("filePreview") or item.get("file_preview") or {}
    if not isinstance(file_info, dict):
        file_info = {}
    if not isinstance(preview, dict):
        preview = {}

    url = first_text(
        file_info.get("shareUrl"),
        file_info.get("fileUrl"),
        file_info.get("contentUrl"),
        item.get("shareUrl"),
        item.get("fileUrl"),
        item.get("contentUrl"),
        item.get("downloadUrl"),
        item.get("objectUrl"),
        item.get("baseUrl"),
        item.get("url"),
        item.get("href"),
    )
    preview_url = first_text(
        preview.get("previewUrl"),
        preview.get("thumbnailUrl"),
        item.get("previewUrl"),
        item.get("thumbnailUrl"),
        item.get("preview_url"),
    )
    if not url and not preview_url:
        return None

    name = (
        first_text(
            item.get("fileName"),
            item.get("name"),
            item.get("title"),
            item.get("displayName"),
            item.get("contentName"),
            file_info.get("fileName"),
            file_info.get("name"),
            file_info.get("title"),
        )
        or file_name_from_url(url or preview_url)
        or "File"
    )
    file_type = first_text(
        item.get("fileType"),
        item.get("contentType"),
        item.get("type"),
        item.get("itemType"),
        file_info.get("fileType"),
        file_info.get("contentType"),
        file_info.get("type"),
    )
    return {
        "id": first_text(item.get("itemid"), item.get("itemId"), item.get("id"), item.get("fileId"), item.get("objectId")),
        "name": name,
        "url": url,
        "preview_url": preview_url,
        "kind": attachment_kind(name, url or preview_url, file_type),
    }


class MessageAttachmentHtmlParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.attachments: list[dict] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        attrs_dict = {str(key).lower(): value for key, value in attrs}
        itemtype = clean_text(attrs_dict.get("itemtype")) or ""
        lowered_type = itemtype.lower()

        if tag.lower() == "img":
            if lowered_type.endswith("/emoji"):
                return
            src = clean_text(attrs_dict.get("src"))
            if (
                "amsimage" not in lowered_type
                and "inlineimage" not in lowered_type
                and "amsvideo" not in lowered_type
                and not is_likely_attachment_url(src)
            ):
                return
            name = clean_text(attrs_dict.get("alt")) or ("Video" if "amsvideo" in lowered_type else "Image")
            append_attachment(
                self.attachments,
                {
                    "id": clean_text(attrs_dict.get("itemid") or attrs_dict.get("id")),
                    "name": name,
                    "url": src,
                    "preview_url": src,
                    "kind": attachment_kind(name, src, itemtype),
                },
            )
            return

        if tag.lower() == "a":
            href = clean_text(attrs_dict.get("href"))
            if (
                "hyperlink/files" not in lowered_type
                and "fileshyperlink" not in lowered_type
                and not is_likely_attachment_url(href)
            ):
                return
            name = clean_text(attrs_dict.get("title")) or file_name_from_url(href) or "File"
            append_attachment(
                self.attachments,
                {
                    "name": name,
                    "url": href,
                    "kind": attachment_kind(name, href, itemtype),
                },
            )


def extract_html_attachments(content_html: str | None) -> list[dict]:
    html = clean_text(content_html)
    if not html:
        return []
    parser = MessageAttachmentHtmlParser()
    try:
        parser.feed(html)
    except Exception:
        return []
    return parser.attachments


def extract_message_attachments(raw: dict, content_html: str | None) -> list[dict]:
    attachments: list[dict] = []
    properties = raw.get("properties") or {}
    attachment_sources = [
        raw.get("attachments"),
        raw.get("files"),
        raw.get("amsReferences"),
        raw.get("amsreferences"),
    ]
    if isinstance(properties, dict):
        attachment_sources.extend(
            properties.get(key)
            for key in (
                "attachments",
                "files",
                "links",
                "amsReferences",
                "amsreferences",
            )
        )

    for source in attachment_sources:
        for item in parse_json_list(source):
            append_attachment(attachments, attachment_from_object(item))

    for attachment in extract_html_attachments(content_html):
        append_attachment(attachments, attachment)
    return attachments


def extract_message_reactions(raw: dict, guid_to_name: dict[str, str]) -> list[dict]:
    reaction_map: dict[str, dict] = {}
    properties = raw.get("properties") or {}
    emotion_items = parse_json_list(properties.get("emotions")) if isinstance(properties, dict) else []

    for item in emotion_items:
        key = (safe_text(item.get("key") or item.get("emotion") or item.get("name")) or "").lower()
        if not key:
            continue
        entry = reaction_map.setdefault(key, {"key": key, "count": 0, "users": []})
        seen_users = {
            (existing.get("id") or "", existing.get("display_name") or "", existing.get("reacted_at") or "")
            for existing in entry["users"]
            if isinstance(existing, dict)
        }
        for user in parse_json_list(item.get("users")):
            raw_id = safe_text(user.get("mri") or user.get("id") or user.get("userId"))
            user_id = extract_guid(raw_id)
            display_name = safe_text(user.get("displayName")) or (guid_to_name.get(user_id) if user_id else None)
            if user_id and display_name:
                guid_to_name.setdefault(user_id, display_name)
            reacted_at = to_iso_from_millis(user.get("time") or user.get("timestamp") or user.get("reactedAt"))
            identity = (user_id or "", display_name or "", reacted_at or "")
            if identity in seen_users:
                continue
            seen_users.add(identity)
            cleaned_user = {
                field: value
                for field, value in {
                    "id": user_id,
                    "display_name": display_name,
                    "reacted_at": reacted_at,
                }.items()
                if value is not None and value != ""
            }
            if cleaned_user:
                entry["users"].append(cleaned_user)
        entry["count"] = max(entry["count"], len(entry["users"]))

    annotations_summary = parse_json_object(raw.get("annotationsSummary")) or {}
    annotation_emotions = annotations_summary.get("emotions") or {}
    if isinstance(annotation_emotions, dict):
        for raw_key, raw_count in annotation_emotions.items():
            key = (safe_text(raw_key) or "").lower()
            if not key:
                continue
            entry = reaction_map.setdefault(key, {"key": key, "count": 0, "users": []})
            try:
                count = int(raw_count)
            except (TypeError, ValueError):
                count = 0
            entry["count"] = max(entry["count"], count, len(entry["users"]))

    normalized = []
    for reaction in reaction_map.values():
        count = max(reaction.get("count") or 0, len(reaction.get("users") or []))
        normalized.append(
            {
                "key": reaction["key"],
                "count": count,
                "users": reaction.get("users") or [],
            }
        )
    return sorted(normalized, key=lambda item: (-int(item.get("count") or 0), item.get("key") or ""))


def reaction_total(reactions: list[dict] | None) -> int:
    return count_reactions(reactions)


def merge_reaction_lists(*reaction_lists: list[dict] | None) -> list[dict]:
    merged: dict[str, dict] = {}
    for reactions in reaction_lists:
        for reaction in reactions or []:
            key = (safe_text(reaction.get("key")) or "").lower()
            if not key:
                continue
            entry = merged.setdefault(key, {"key": key, "count": 0, "users": []})
            try:
                count = int(reaction.get("count") or 0)
            except (TypeError, ValueError):
                count = 0
            entry["count"] = max(entry["count"], count)

            seen_users = {
                (existing.get("id") or "", existing.get("display_name") or "", existing.get("reacted_at") or "")
                for existing in entry["users"]
                if isinstance(existing, dict)
            }
            for user in reaction.get("users") or []:
                if not isinstance(user, dict):
                    continue
                cleaned_user = {
                    field: value
                    for field, value in {
                        "id": extract_guid(user.get("id")),
                        "display_name": safe_text(user.get("display_name")),
                        "reacted_at": safe_text(user.get("reacted_at")),
                    }.items()
                    if value is not None and value != ""
                }
                identity = (
                    cleaned_user.get("id") or "",
                    cleaned_user.get("display_name") or "",
                    cleaned_user.get("reacted_at") or "",
                )
                if identity in seen_users:
                    continue
                seen_users.add(identity)
                if cleaned_user:
                    entry["users"].append(cleaned_user)
            entry["count"] = max(entry["count"], len(entry["users"]))

    return sorted(
        merged.values(),
        key=lambda item: (-max(int(item.get("count") or 0), len(item.get("users") or [])), item.get("key") or ""),
    )


def message_richness_score(message: dict) -> tuple[int, int, int, int, int, int]:
    content_text = message.get("content_text") or ""
    attachments = message.get("attachments") or []
    reactions = message.get("reactions") or []
    return (
        MESSAGE_QUALITY_RANK.get(message.get("quality") or "", 0),
        1 if content_text else 0,
        len(content_text),
        len(attachments),
        reaction_total(reactions),
        1 if message.get("content_html") else 0,
    )


def merge_message_records(existing: dict, candidate: dict) -> dict:
    if message_richness_score(candidate) > message_richness_score(existing):
        primary = dict(candidate)
        secondary = existing
    else:
        primary = dict(existing)
        secondary = candidate

    for field in [
        "client_message_id",
        "timestamp",
        "sender_display_name",
        "sender_id",
        "message_type",
        "content_type",
        "content_html",
        "content_text",
        "source",
    ]:
        if not primary.get(field) and secondary.get(field):
            primary[field] = secondary[field]

    attachments = merge_attachment_lists(primary.get("attachments"), secondary.get("attachments"))
    if attachments:
        primary["attachments"] = attachments
    else:
        primary.pop("attachments", None)

    reactions = merge_reaction_lists(primary.get("reactions"), secondary.get("reactions"))
    if reactions:
        primary["reactions"] = reactions
    else:
        primary.pop("reactions", None)

    if primary.get("attachments") and primary.get("quality") == "residual":
        primary["quality"] = "attachment"
    return primary


def flatten_members(members: list[dict], guid_to_name: dict[str, str]) -> tuple[list[str], list[str]]:
    participant_ids = []
    participants = []
    for member in members or []:
        raw_id = member.get("id")
        guid = extract_guid(raw_id)
        if guid and guid not in participant_ids:
            participant_ids.append(guid)
        display_name = None
        name_hint = member.get("nameHint") or {}
        if isinstance(name_hint, dict):
            display_name = clean_text(name_hint.get("displayName"))
        if guid and display_name:
            guid_to_name.setdefault(guid, display_name)
        if not display_name and guid:
            display_name = guid_to_name.get(guid)
        if display_name and display_name not in participants:
            participants.append(display_name)
    return participant_ids, participants


def flatten_chat_title_users(chat_title: dict | None, guid_to_name: dict[str, str]) -> tuple[list[str], list[str]]:
    participant_ids = []
    participants = []
    if not isinstance(chat_title, dict):
        return participant_ids, participants

    for user in chat_title.get("avatarUsersInfo") or []:
        if not isinstance(user, dict):
            continue
        guid = extract_guid(
            safe_text(user.get("mri"))
            or safe_text(user.get("id"))
            or safe_text(user.get("userId"))
            or safe_text(user.get("homeMri"))
        )
        display_name = safe_text(user.get("displayName"))
        if guid and display_name:
            guid_to_name.setdefault(guid, display_name)
        if guid and guid not in participant_ids:
            participant_ids.append(guid)
        if display_name and display_name not in participants:
            participants.append(display_name)
    return participant_ids, participants


def merge_thread_participant(thread: dict, participant_id: str | None = None, participant_name: str | None = None) -> None:
    normalized_id = extract_guid(participant_id)
    cleaned_name = clean_text(participant_name)

    if normalized_id and normalized_id not in thread["participant_ids"]:
        thread["participant_ids"].append(normalized_id)
    if cleaned_name and cleaned_name not in thread["participants"]:
        thread["participants"].append(cleaned_name)


def to_iso_from_datetime_text(value: str | None) -> str | None:
    cleaned = clean_text(value)
    if not cleaned:
        return None
    for fmt in ("%m/%d/%Y %H:%M:%S %z", "%m/%d/%Y %H:%M:%S"):
        try:
            parsed = datetime.strptime(cleaned, fmt)
        except ValueError:
            continue
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc).isoformat()
    return None


def merge_unique_strings(existing: list[str] | None, values: list[str] | None) -> list[str]:
    merged = []
    for value in [*(existing or []), *(values or [])]:
        cleaned = clean_text(value)
        if cleaned and cleaned not in merged:
            merged.append(cleaned)
    return merged


def call_state_priority(value: str | None) -> int:
    return EVENT_CALL_STATE_PRIORITY.get((clean_text(value) or "").lower(), -1)


def parse_iso_datetime(value: str | None) -> datetime | None:
    cleaned = clean_text(value)
    if not cleaned:
        return None
    try:
        parsed = datetime.fromisoformat(cleaned.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def normalize_meeting_datetime_value(value: str | None) -> str | None:
    cleaned = safe_text(value)
    if not cleaned:
        return None
    if cleaned.startswith("0001-01-01"):
        return None
    parsed = parse_iso_datetime(cleaned)
    if parsed is not None and parsed.year <= 1:
        return None
    return cleaned


def iso_bounds(values: list[str | None]) -> tuple[str | None, str | None]:
    parsed_values = [parsed for parsed in (parse_iso_datetime(value) for value in values) if parsed is not None]
    if not parsed_values:
        return None, None
    return min(parsed_values).isoformat(), max(parsed_values).isoformat()


def normalize_phone_number(value: str | None) -> str | None:
    cleaned = safe_text(value)
    if not cleaned:
        return None
    cleaned = re.sub(r"^(?:4:|tel:)", "", cleaned, flags=re.I)
    if re.search(r"[A-Za-z]", cleaned):
        return None
    if not re.fullmatch(r"[+()0-9 .-]{7,}", cleaned):
        return None
    digits = re.sub(r"[(). -]+", "", cleaned)
    if not digits:
        return None
    if digits.startswith("+"):
        digits = f"+{re.sub(r'[^0-9]', '', digits)}"
    else:
        digits = re.sub(r"[^0-9]", "", digits)
    digits_only = digits.lstrip("+")
    if not digits_only.isdigit() or len(digits_only) < 7:
        return None
    return digits


def format_phone_number(value: str | None) -> str | None:
    normalized = normalize_phone_number(value)
    if not normalized:
        return None
    digits = normalized.lstrip("+")
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    if len(digits) == 11 and digits.startswith("1"):
        local = digits[1:]
        return f"+1 ({local[:3]}) {local[3:6]}-{local[6:]}"
    return normalized


def is_generic_phone_label(value: str | None) -> bool:
    cleaned = clean_text(value)
    if not cleaned:
        return False
    return bool(GENERIC_PHONE_LABEL_RE.match(cleaned))


def participant_phone_number(participant: dict | None, *fallback_values: str | None) -> str | None:
    values = []
    if isinstance(participant, dict):
        values.extend(
            [
                participant.get("phoneNumber"),
                participant.get("telephoneNumber"),
                participant.get("alternateId"),
                participant.get("id"),
            ]
        )
    values.extend(fallback_values)
    for value in values:
        formatted = format_phone_number(value)
        if formatted:
            return formatted
    return None


def participant_label(display_name: str | None, phone_number: str | None) -> str | None:
    cleaned_name = clean_text(display_name)
    if phone_number and (not cleaned_name or is_generic_phone_label(cleaned_name)):
        return phone_number
    return cleaned_name or phone_number


def collect_call_participants(participants: list[dict] | None, guid_to_name: dict[str, str]) -> tuple[list[str], list[str]]:
    participant_ids: list[str] = []
    participant_names: list[str] = []
    for participant in participants or []:
        if not isinstance(participant, dict):
            continue
        endpoint = safe_text(participant.get("id")) or safe_text(participant.get("alternateId"))
        guid = extract_guid(endpoint)
        phone_number = participant_phone_number(participant)
        display_name = participant_label(
            safe_text(participant.get("displayName")) or (guid_to_name.get(guid) if guid else None),
            phone_number,
        )
        if guid and display_name:
            guid_to_name.setdefault(guid, display_name)
        if guid and guid not in participant_ids:
            participant_ids.append(guid)
        if display_name and display_name not in participant_names:
            participant_names.append(display_name)
    return participant_ids, participant_names


def parse_event_call_message(message: dict, thread: dict, guid_to_name: dict[str, str]) -> dict | None:
    if message.get("message_type") != "Event/Call":
        return None

    content_text = message.get("content_text") or ""
    event_match = EVENT_CALL_NAME_RE.search(content_text)
    if not event_match:
        return None

    raw_event_name = event_match.group(1)
    call_state = EVENT_CALL_STATE_MAP.get(raw_event_name.lower(), clean_text(raw_event_name))

    call_guid_match = EVENT_CALL_TRAILING_GUID_RE.search(content_text)
    call_id = call_guid_match.group(1).lower() if call_guid_match else clean_text(message.get("id"))
    if not call_id:
        return None

    meeting = thread.get("meeting") or {}
    metadata = thread.get("metadata") or {}
    time_tokens = EVENT_CALL_TIME_RE.findall(content_text)
    occurrence_start = normalize_meeting_datetime_value(to_iso_from_datetime_text(time_tokens[-3])) if len(time_tokens) >= 3 else None
    occurrence_end = normalize_meeting_datetime_value(to_iso_from_datetime_text(time_tokens[-2])) if len(time_tokens) >= 2 else None
    event_start = to_iso_from_datetime_text(time_tokens[-1]) if time_tokens else None
    thread_meeting_start = normalize_meeting_datetime_value(clean_text(meeting.get("startTime")))
    thread_meeting_end = normalize_meeting_datetime_value(clean_text(meeting.get("endTime")))

    before_event = content_text[:event_match.start()].strip()
    series_kind_match = EVENT_CALL_SERIES_KIND_RE.search(before_event)
    series_kind = clean_text(series_kind_match.group(1)) if series_kind_match else None
    subject_source = before_event[:series_kind_match.start()].rstrip() if series_kind_match else before_event
    subject = None
    if len(time_tokens) >= 4:
        anchor = time_tokens[-2]
        index = subject_source.rfind(anchor)
        if index != -1:
            subject = clean_text(subject_source[index + len(anchor):])
    if not subject:
        subject = clean_text(meeting.get("subject")) or clean_text(metadata.get("topic")) or clean_text(thread.get("label"))

    conversation_type = (clean_text(metadata.get("conversation_type")) or "").lower()
    thread_type = (clean_text(metadata.get("thread_type")) or "").lower()
    is_meeting_thread = (
        thread.get("category") in {"team_chat", "meeting"}
        or conversation_type == "meeting"
        or thread_type == "meeting"
    )
    has_real_meeting_window = bool(occurrence_start or occurrence_end or thread_meeting_start or thread_meeting_end)
    is_meeting_call = is_meeting_thread or bool(series_kind) or has_real_meeting_window
    participant_ids = []
    participant_names = []
    participant_sessions = []
    for participant_id, participant_name, duration_text in EVENT_CALL_PARTICIPANT_RE.findall(content_text):
        guid = extract_guid(participant_id)
        name = clean_text(participant_name)
        if guid and guid not in participant_ids:
            participant_ids.append(guid)
        if name and name not in participant_names:
            participant_names.append(name)
        if guid and name:
            guid_to_name.setdefault(guid, name)
        try:
            duration_seconds = int(duration_text)
        except ValueError:
            duration_seconds = None
        participant_sessions.append(
            {
                key: value
                for key, value in {
                    "id": guid,
                    "display_name": name,
                    "duration_seconds": duration_seconds,
                }.items()
                if value not in {None, ""}
            }
        )
    for guid in extract_guids(content_text):
        if guid == call_id:
            continue
        name = guid_to_name.get(guid)
        if not name:
            continue
        if guid not in participant_ids:
            participant_ids.append(guid)
        if name not in participant_names:
            participant_names.append(name)

    originator_id = extract_guid(message.get("sender_id"))
    originator_name = clean_text(message.get("sender_display_name")) or (guid_to_name.get(originator_id) if originator_id else None)
    if originator_id and originator_name:
        if originator_id not in participant_ids:
            participant_ids.insert(0, originator_id)
        if originator_name not in participant_names:
            participant_names.insert(0, originator_name)

    other_participants = [
        (participant_ids[index], participant_names[index])
        for index in range(min(len(participant_ids), len(participant_names)))
        if participant_ids[index] != originator_id
    ]
    target_id = other_participants[0][0] if not is_meeting_call and len(participant_names) <= 2 and other_participants else None
    target_name = other_participants[0][1] if not is_meeting_call and len(participant_names) <= 2 and other_participants else None
    event_url_match = EVENT_CALL_URL_RE.search(content_text)
    summary_label = subject or clean_text(thread.get("label")) or "Call"

    call = {
        "call_id": call_id,
        "start_time": event_start or message.get("timestamp"),
        "connect_time": event_start if call_state == "accepted" else None,
        "end_time": message.get("timestamp") if call_state in {"ended", "missed", "rejected", "cancelled"} else None,
        "direction": "meeting" if is_meeting_call else None,
        "call_type": "Meeting" if is_meeting_call else ("Group" if len(participant_names) > 2 else "TwoParty"),
        "call_state": call_state,
        "originator_display_name": originator_name,
        "originator_id": originator_id,
        "target_display_name": target_name,
        "target_id": target_id,
        "conversation_id": thread.get("id"),
        "quality": "thread_event_inferred",
        "source": "ccl:replychains:event_call",
        "summary_text": clean_text(f"{summary_label} {'meeting ' if is_meeting_call else ''}call"),
        "participant_ids": participant_ids,
        "participant_display_names": participant_names,
        "participant_sessions": participant_sessions,
        "meeting_subject": subject if is_meeting_call else None,
        "meeting_start_time": (occurrence_start or thread_meeting_start) if is_meeting_call else None,
        "meeting_end_time": (occurrence_end or thread_meeting_end) if is_meeting_call else None,
        "meeting_series_kind": series_kind if is_meeting_call else None,
        "source_event_message_ids": [message.get("id")] if message.get("id") else [],
        "event_url": safe_text(event_url_match.group(0)) if event_url_match else None,
    }
    return {
        field: value
        for field, value in call.items()
        if value is not None and value != "" and value != []
    }


def merge_call_records(existing: dict, candidate: dict) -> None:
    for field in [
        "conversation_id",
        "direction",
        "call_type",
        "originator_display_name",
        "originator_id",
        "originator_endpoint",
        "originator_phone_number",
        "target_display_name",
        "target_id",
        "target_endpoint",
        "target_phone_number",
        "group_chat_thread_id",
        "meeting_subject",
        "meeting_start_time",
        "meeting_end_time",
        "meeting_series_kind",
        "event_url",
        "summary_text",
    ]:
        if candidate.get(field) and not existing.get(field):
            existing[field] = candidate[field]

    if candidate.get("start_time"):
        if not existing.get("start_time") or candidate["start_time"] < existing["start_time"]:
            existing["start_time"] = candidate["start_time"]
    if candidate.get("connect_time") and not existing.get("connect_time"):
        existing["connect_time"] = candidate["connect_time"]
    if candidate.get("end_time"):
        if not existing.get("end_time") or candidate["end_time"] > existing["end_time"]:
            existing["end_time"] = candidate["end_time"]

    candidate_state_priority = call_state_priority(candidate.get("call_state"))
    existing_state_priority = call_state_priority(existing.get("call_state"))
    if candidate.get("call_state") and (
        not existing.get("call_state")
        or candidate_state_priority > existing_state_priority
        or (candidate_state_priority == existing_state_priority and candidate_state_priority >= 0)
    ):
        existing["call_state"] = candidate.get("call_state")

    for list_field in ["participant_ids", "participant_display_names", "source_event_message_ids"]:
        merged = merge_unique_strings(existing.get(list_field), candidate.get(list_field))
        if merged:
            existing[list_field] = merged
    candidate_sessions = candidate.get("participant_sessions") or []
    existing_sessions = existing.get("participant_sessions") or []
    if candidate_sessions and len(candidate_sessions) >= len(existing_sessions):
        existing["participant_sessions"] = candidate_sessions

    if candidate.get("quality") and not existing.get("quality"):
        existing["quality"] = candidate["quality"]
    if candidate.get("source") and not existing.get("source"):
        existing["source"] = candidate["source"]


def merge_thread_event_calls(calls: list[dict], threads: dict[str, dict], guid_to_name: dict[str, str]) -> None:
    inferred_calls: dict[str, dict] = {}
    for thread in threads.values():
        for message in thread.get("messages", []):
            candidate = parse_event_call_message(message, thread, guid_to_name)
            if not candidate:
                continue
            key = candidate.get("call_id") or candidate.get("shared_correlation_id") or f"{thread.get('id')}|{message.get('id') or message.get('timestamp')}"
            existing = inferred_calls.get(key)
            if existing is None:
                inferred_calls[key] = candidate
                continue
            merge_call_records(existing, candidate)

    calls_by_call_id = {(call.get("call_id") or "").lower(): call for call in calls if call.get("call_id")}
    calls_by_shared = {
        (call.get("shared_correlation_id") or "").lower(): call
        for call in calls
        if call.get("shared_correlation_id")
    }
    for candidate in inferred_calls.values():
        existing = None
        call_id = (candidate.get("call_id") or "").lower()
        shared_correlation_id = (candidate.get("shared_correlation_id") or "").lower()
        if call_id:
            existing = calls_by_call_id.get(call_id)
        if existing is None and shared_correlation_id:
            existing = calls_by_shared.get(shared_correlation_id)
        if existing is not None:
            merge_call_records(existing, candidate)
            continue
        calls.append(candidate)


def normalize_name_key(value: str | None) -> str | None:
    cleaned = clean_text(value)
    return cleaned.lower() if cleaned else None


def call_has_meeting_context(call: dict) -> bool:
    for thread_id in [call.get("conversation_id"), call.get("group_chat_thread_id")]:
        normalized_thread_id = normalize_thread_id(thread_id)
        if normalized_thread_id and classify_thread(normalized_thread_id) == "team_chat":
            return True
    if clean_text(call.get("meeting_series_kind")):
        return True
    if normalize_meeting_datetime_value(call.get("meeting_start_time")) or normalize_meeting_datetime_value(call.get("meeting_end_time")):
        return True
    return False


def enrich_calls_for_current_user(calls: list[dict], current_user_oid: str | None, current_user_name: str | None) -> None:
    current_oid = extract_guid(current_user_oid)
    current_name = normalize_name_key(current_user_name)
    if not current_oid and not current_name:
        return

    for call in calls:
        is_meeting_call = call_has_meeting_context(call)
        if not is_meeting_call:
            continue

        call["call_type"] = "Meeting"
        call["direction"] = "meeting"

        participant_ids = set()
        for raw_guid in [*(call.get("participant_ids") or []), call.get("originator_id"), call.get("target_id")]:
            guid = extract_guid(raw_guid)
            if guid:
                participant_ids.add(guid)

        participant_names = set()
        for raw_name in [*(call.get("participant_display_names") or []), call.get("originator_display_name"), call.get("target_display_name")]:
            name = normalize_name_key(raw_name)
            if name:
                participant_names.add(name)

        matched_session = None
        for session in call.get("participant_sessions") or []:
            session_id = extract_guid(session.get("id"))
            session_name = normalize_name_key(session.get("display_name"))
            if (current_oid and session_id == current_oid) or (current_name and session_name == current_name):
                matched_session = session
                break

        joined = False
        if matched_session is not None:
            joined = True
        elif current_oid and current_oid in participant_ids:
            joined = True
        elif current_name and current_name in participant_names:
            joined = True

        has_attendance_roster = bool(call.get("participant_sessions"))
        if joined:
            call["user_participation"] = "joined"
        elif has_attendance_roster or (clean_text(call.get("call_state")) or "").lower() == "missed":
            call["user_participation"] = "missed"

        if call.get("connect_time"):
            continue

        duration_seconds = matched_session.get("duration_seconds") if isinstance(matched_session, dict) else None
        if isinstance(duration_seconds, int) and duration_seconds >= 0:
            end_time = parse_iso_datetime(call.get("end_time"))
            if end_time is None:
                continue
            connect_time = end_time - timedelta(seconds=duration_seconds)
            start_time = parse_iso_datetime(call.get("start_time"))
            if start_time and connect_time < start_time:
                connect_time = start_time
            call["connect_time"] = connect_time.isoformat()
            continue

        originator_id = extract_guid(call.get("originator_id"))
        originator_name = normalize_name_key(call.get("originator_display_name"))
        if ((current_oid and originator_id == current_oid) or (current_name and originator_name == current_name)) and call.get("start_time"):
            call["connect_time"] = call["start_time"]


def is_placeholder_label(label: str | None, thread_id: str) -> bool:
    cleaned = clean_text(label)
    if not cleaned:
        return True
    if cleaned == thread_id:
        return True
    return cleaned.startswith(("19:", "48:")) or cleaned.endswith(("@thread.v2", "@thread.skype", "@unq.gbl.spaces"))


def build_participant_label(participants: list[str], current_user_name: str | None) -> str | None:
    ordered = []
    for name in participants or []:
        cleaned = clean_text(name)
        if cleaned and cleaned not in ordered:
            ordered.append(cleaned)
    others = [name for name in ordered if name != current_user_name]
    display = others or ordered
    if not display:
        return None
    if len(display) <= 4:
        return " / ".join(display)
    return f'{" / ".join(display[:4])} + {len(display) - 4} more'


def build_export(root: Path | str | None = None, show_decode_errors: bool = True, collect_store_summary: bool = False) -> dict:
    source_info = resolve_teams_source(root)
    ccl = load_ccl()
    leveldb_path = source_info.leveldb_path
    blob_path = source_info.blob_path
    wrapper = ccl.WrappedIndexDB(str(leveldb_path), str(blob_path) if blob_path.exists() else None)
    dbs, available_stores = get_target_stores(wrapper, SUMMARY_TARGETS)

    profile = parse_profile(source_info.local_storage_dir) if source_info.local_storage_dir else None
    current_user_oid = (profile or {}).get("oid")
    current_user_name = (profile or {}).get("display_name")

    people_store = available_stores.get("people")
    conversations_store = available_stores.get("conversations")
    replychains_store = available_stores.get("replychains")
    call_history_store = available_stores.get("call_history")
    store_summary = (
        {
            "backend": "ccl_chromium_reader.wrapper",
            "platform": source_info.platform_name,
            "search_root": str(source_info.search_root),
            "profile_root": str(source_info.profile_root),
            "leveldb_path": str(leveldb_path),
            "blob_path": str(blob_path) if blob_path.exists() else None,
            "local_storage_dir": str(source_info.local_storage_dir) if source_info.local_storage_dir else None,
            "discovery_method": source_info.discovery_method,
            "databases_total": len(dbs),
            "key_stores": {},
            "samples": {},
        }
        if collect_store_summary
        else None
    )

    def update_store_summary(label: str, record_count: int, sample: dict | None = None, **extra_counts: int) -> None:
        if store_summary is None:
            return
        store_summary["key_stores"][label] = {
            "found": True,
            "record_count": record_count,
            **{key: value for key, value in extra_counts.items() if value},
        }
        sample_payload = build_sample(label, sample)
        if sample_payload is not None:
            store_summary["samples"][label] = sample_payload

    guid_to_name = {}
    if current_user_oid and current_user_name:
        guid_to_name[current_user_oid.lower()] = current_user_name

    if people_store is not None:
        people_count = 0
        people_sample = None
        with decode_output_context(show_decode_errors):
            for record in people_store.iterate_records(errors_to_stdout=True):
                value = record.value or {}
                people_count += 1
                if people_sample is None:
                    people_sample = value
                guid = clean_text(value.get("ExternalDirectoryObjectId")) or extract_guid(value.get("MRI")) or extract_guid(value.get("Id"))
                name = clean_text(value.get("DisplayName"))
                if guid and name:
                    guid_to_name[guid.lower()] = name
        update_store_summary("people", people_count, people_sample)

    threads: dict[str, dict] = {}
    thread_titles: dict[str, str] = {}
    thread_types: dict[str, str] = {}

    if conversations_store is not None:
        conversations_count = 0
        conversations_sample = None
        with decode_output_context(show_decode_errors):
            for record in conversations_store.iterate_records(errors_to_stdout=True):
                value = record.value or {}
                conversations_count += 1
                if conversations_sample is None:
                    conversations_sample = value
                thread_id = normalize_thread_id(value.get("id"))
                if not thread_id:
                    continue
                thread = threads.setdefault(thread_id, init_thread_record(thread_id))
                thread["metadata_quality"] = "detailed"
                thread_type = safe_text(value.get("type")) or ""
                thread_types[thread_id] = thread_type
                thread["category"] = classify_thread(thread_id, thread_type)

                title = safe_text(value.get("title"))
                if title:
                    thread_titles[thread_id] = title
                    thread["label"] = title

                metadata = thread["metadata"]
                if thread_type:
                    metadata["conversation_type"] = thread_type
                thread_properties = value.get("threadProperties") or {}
                if isinstance(thread_properties, dict):
                    mapping = {
                        "topic": "topic",
                        "topicThreadTopic": "topic_thread_topic",
                        "spaceThreadTopic": "space_thread_topic",
                        "threadType": "thread_type",
                        "creator": "creator",
                        "hasTranscript": "has_transcript",
                        "isLastMessageFromMe": "is_last_message_from_me",
                        "isLiveChatEnabled": "is_live_chat_enabled",
                    }
                    for source, dest in mapping.items():
                        if source in thread_properties:
                            metadata[dest] = thread_properties[source]
                    meeting = parse_json_object(thread_properties.get("meeting"))
                    if isinstance(meeting, dict):
                        thread["meeting"] = {
                            "subject": meeting.get("subject"),
                            "startTime": meeting.get("startTime"),
                            "endTime": meeting.get("endTime"),
                            "isCancelled": meeting.get("isCancelled"),
                        }

                participant_ids, participants = flatten_members(value.get("members") or [], guid_to_name)
                thread["participant_ids"] = sorted(set(thread["participant_ids"]) | set(participant_ids))
                thread["current_member_ids"] = sorted(set(thread.get("current_member_ids", [])) | set(participant_ids))
                thread["participants"] = sorted(set(thread["participants"]) | set(participants))

                chat_title = value.get("chatTitle") or {}
                if isinstance(chat_title, dict):
                    short_title = safe_text(chat_title.get("shortTitle"))
                    long_title = safe_text(chat_title.get("longTitle"))
                    if short_title:
                        metadata["chat_title_short"] = short_title
                    if long_title:
                        metadata["chat_title_long"] = long_title

                    participant_ids, participants = flatten_chat_title_users(chat_title, guid_to_name)
                    thread["participant_ids"] = sorted(set(thread["participant_ids"]) | set(participant_ids))
                    thread["participants"] = sorted(set(thread["participants"]) | set(participants))
        update_store_summary("conversations", conversations_count, conversations_sample)

    best_messages: dict[tuple[str, str], dict] = {}
    calllog_calls: dict[str, dict] = {}
    if replychains_store is not None:
        replychains_count = 0
        replychains_sample = None
        replychains_messages_total = 0
        replychains_threads_with_messages = 0
        with decode_output_context(show_decode_errors):
            for record in replychains_store.iterate_records(errors_to_stdout=True):
                value = record.value or {}
                replychains_count += 1
                if replychains_sample is None:
                    replychains_sample = value
                message_map = safe_dict(value.get("messageMap"))
                if message_map:
                    replychains_messages_total += len(message_map)
                    replychains_threads_with_messages += 1
                thread_id = normalize_thread_id(value.get("conversationId"))
                if not thread_id:
                    continue
                thread = threads.setdefault(thread_id, init_thread_record(thread_id))

                if thread_id == "48:calllogs":
                    for _, raw in message_map.items():
                        if not isinstance(raw, dict):
                            continue
                        content = raw.get("content")
                        content_string = None
                        if isinstance(content, str):
                            content_string = content
                        elif isinstance(content, (bytes, bytearray)):
                            content_string = bytes(content).decode("utf-8", "ignore")

                        content_text = safe_text(content_string if content_string is not None else content)
                        message_id = safe_text(raw.get("id") or raw.get("clientMessageId") or raw.get("searchKey"))
                        properties = raw.get("properties") or {}
                        call_log = parse_json_object(properties.get("call-log")) if isinstance(properties, dict) else None

                        originator = (call_log or {}).get("originatorParticipant") or {}
                        target = (call_log or {}).get("targetParticipant") or {}
                        originator_endpoint = safe_text(originator.get("id")) or safe_text((call_log or {}).get("originator"))
                        target_endpoint = safe_text(target.get("id")) or safe_text((call_log or {}).get("target"))
                        originator_id = extract_guid(originator_endpoint)
                        target_id = extract_guid(target_endpoint)
                        originator_phone_number = participant_phone_number(originator, (call_log or {}).get("originator"))
                        target_phone_number = participant_phone_number(target, (call_log or {}).get("target"))
                        originator_name = participant_label(
                            safe_text(originator.get("displayName")) or (guid_to_name.get(originator_id) if originator_id else None),
                            originator_phone_number,
                        )
                        target_name = participant_label(
                            safe_text(target.get("displayName")) or (guid_to_name.get(target_id) if target_id else None),
                            target_phone_number,
                        )
                        if originator_id and originator_name:
                            guid_to_name.setdefault(originator_id, originator_name)
                        if target_id and target_name:
                            guid_to_name.setdefault(target_id, target_name)
                        participant_ids, participant_names = collect_call_participants(
                            [originator, target, *((call_log or {}).get("participantList") or [])],
                            guid_to_name,
                        )

                        call_id = safe_text((call_log or {}).get("callId")) or extract_guid(content_text) or extract_guid(message_id)
                        timestamp = to_iso_from_millis(raw.get("originalArrivalTime") or raw.get("clientArrivalTime") or value.get("latestDeliveryTime"))
                        shared_correlation_id = safe_text((call_log or {}).get("sharedCorrelationId"))
                        key = call_id or shared_correlation_id or message_id
                        if not key:
                            continue

                        candidate = {
                            "call_id": call_id,
                            "shared_correlation_id": shared_correlation_id,
                            "start_time": safe_text((call_log or {}).get("startTime")) or timestamp,
                            "connect_time": safe_text((call_log or {}).get("connectTime")),
                            "end_time": safe_text((call_log or {}).get("endTime")),
                            "direction": safe_text((call_log or {}).get("callDirection")),
                            "call_type": safe_text((call_log or {}).get("callType")),
                            "call_state": safe_text((call_log or {}).get("callState")) or safe_text(raw.get("messageType")) or "calllog",
                            "originator_display_name": originator_name,
                            "originator_id": originator_id,
                            "originator_endpoint": originator_endpoint,
                            "originator_phone_number": originator_phone_number,
                            "target_display_name": target_name,
                            "target_id": target_id,
                            "target_endpoint": target_endpoint,
                            "target_phone_number": target_phone_number,
                            "participant_ids": participant_ids,
                            "participant_display_names": participant_names,
                            "conversation_id": safe_text((call_log or {}).get("threadId")) or thread_id,
                            "group_chat_thread_id": safe_text((call_log or {}).get("groupChatThreadId")),
                            "quality": "calllog_enriched" if call_log else "calllog",
                            "source": "ccl:replychains:48:calllogs",
                            "summary_text": content_text,
                        }
                        candidate = {
                            name: field
                            for name, field in candidate.items()
                            if field is not None and field != "" and field != []
                        }

                        existing = calllog_calls.get(key)
                        score = sum(
                            1
                            for field in [
                                "start_time",
                                "connect_time",
                                "end_time",
                                "direction",
                                "call_type",
                                "call_state",
                                "originator_display_name",
                                "target_display_name",
                                "shared_correlation_id",
                            ]
                            if candidate.get(field)
                        )
                        existing_score = sum(
                            1
                            for field in [
                                "start_time",
                                "connect_time",
                                "end_time",
                                "direction",
                                "call_type",
                                "call_state",
                                "originator_display_name",
                                "target_display_name",
                                "shared_correlation_id",
                            ]
                            if (existing or {}).get(field)
                        )
                        if existing is None or score > existing_score or len(candidate.get("summary_text", "")) > len(existing.get("summary_text", "")):
                            calllog_calls[key] = candidate
                    continue

                for _, raw in message_map.items():
                    if not isinstance(raw, dict):
                        continue
                    message_id = safe_text(raw.get("id") or raw.get("clientMessageId") or raw.get("searchKey"))
                    if not message_id:
                        continue

                    content = raw.get("content")
                    content_type = safe_text(raw.get("contentType"))
                    message_type = safe_text(raw.get("messageType"))
                    content_string = None
                    if isinstance(content, str):
                        content_string = content
                    elif isinstance(content, (bytes, bytearray)):
                        content_string = bytes(content).decode("utf-8", "ignore")

                    if message_type == "RichText/Html" or (isinstance(content_string, str) and content_string.startswith("<")):
                        content_html = content_string
                        content_text = html_to_text(content_string)
                    else:
                        content_html = None
                        content_text = safe_text(content_string if content_string is not None else content)
                    attachments = extract_message_attachments(raw, content_html)
                    reactions = extract_message_reactions(raw, guid_to_name)
                    quality = classify_quality(message_type, content_text)
                    if attachments and quality == "residual":
                        quality = "attachment"

                    sender_name = safe_text(raw.get("imDisplayName") or raw.get("fromDisplayNameInToken"))
                    sender_id = extract_guid(raw.get("creator")) or extract_guid(raw.get("fromUserId")) or extract_guid(raw.get("from"))
                    if sender_id and sender_name:
                        guid_to_name.setdefault(sender_id, sender_name)
                    if sender_id or sender_name:
                        merge_thread_participant(thread, sender_id, sender_name or (guid_to_name.get(sender_id) if sender_id else None))

                    timestamp = to_iso_from_millis(raw.get("originalArrivalTime") or raw.get("clientArrivalTime") or value.get("latestDeliveryTime"))
                    message = {
                        "id": message_id,
                        "client_message_id": safe_text(raw.get("clientMessageId")),
                        "timestamp": timestamp,
                        "sender_display_name": sender_name or (guid_to_name.get(sender_id) if sender_id else None),
                        "sender_id": sender_id,
                        "message_type": message_type,
                        "content_type": content_type,
                        "content_html": content_html,
                        "content_text": content_text,
                        "attachments": attachments,
                        "quality": quality,
                        "source": "ccl:replychains",
                    }
                    if reactions:
                        message["reactions"] = reactions
                    message = {key: value for key, value in message.items() if value is not None and value != "" and value != []}

                    key = (thread_id, message_id)
                    existing = best_messages.get(key)
                    if existing is None:
                        best_messages[key] = message
                    else:
                        best_messages[key] = merge_message_records(existing, message)
        update_store_summary(
            "replychains",
            replychains_count,
            replychains_sample,
            messages_total=replychains_messages_total,
            threads_with_messages=replychains_threads_with_messages,
        )

    for (thread_id, _), message in sorted(best_messages.items(), key=lambda item: (item[0][0], item[1].get("timestamp") or "", item[0][1])):
        thread = threads.setdefault(thread_id, init_thread_record(thread_id))
        thread["messages"].append(message)

    calls = []
    if call_history_store is not None:
        call_history_count = 0
        call_history_sample = None
        with decode_output_context(show_decode_errors):
            for record in call_history_store.iterate_records(errors_to_stdout=True):
                value = record.value or {}
                call_history_count += 1
                if call_history_sample is None:
                    call_history_sample = value
                originator = value.get("originatorParticipant") or {}
                target = value.get("targetParticipant") or {}
                originator_endpoint = safe_text(originator.get("id"))
                target_endpoint = safe_text(target.get("id"))
                originator_id = extract_guid(originator_endpoint)
                target_id = extract_guid(target_endpoint)
                originator_phone_number = participant_phone_number(originator)
                target_phone_number = participant_phone_number(target)
                originator_name = participant_label(
                    safe_text(originator.get("displayName")) or (guid_to_name.get(originator_id) if originator_id else None),
                    originator_phone_number,
                )
                target_name = participant_label(
                    safe_text(target.get("displayName")) or (guid_to_name.get(target_id) if target_id else None),
                    target_phone_number,
                )
                if originator_id and originator_name:
                    guid_to_name.setdefault(originator_id, originator_name)
                if target_id and target_name:
                    guid_to_name.setdefault(target_id, target_name)
                participant_ids, participant_names = collect_call_participants(
                    [originator, target, *(value.get("participantList") or [])],
                    guid_to_name,
                )

                calls.append(
                    {
                        "call_id": safe_text(value.get("callId")),
                        "shared_correlation_id": safe_text(value.get("sharedCorrelationId")),
                        "start_time": safe_text(value.get("startTime")),
                        "connect_time": safe_text(value.get("connectTime")),
                        "end_time": safe_text(value.get("endTime")),
                        "direction": safe_text(value.get("callDirection")),
                        "call_type": safe_text(value.get("callType")),
                        "call_state": safe_text(value.get("callState")),
                        "originator_display_name": originator_name,
                        "originator_id": originator_id,
                        "originator_endpoint": originator_endpoint,
                        "originator_phone_number": originator_phone_number,
                        "target_display_name": target_name,
                        "target_id": target_id,
                        "target_endpoint": target_endpoint,
                        "target_phone_number": target_phone_number,
                        "participant_ids": participant_ids,
                        "participant_display_names": participant_names,
                        "conversation_id": safe_text(value.get("conversationId")),
                        "group_chat_thread_id": safe_text(value.get("groupChatThreadId")),
                        "quality": "structured",
                        "source": "ccl:call-history",
                    }
                )
        update_store_summary("call_history", call_history_count, call_history_sample)

    if store_summary is not None:
        for label in SUMMARY_TARGETS:
            if label in store_summary["key_stores"]:
                continue
            matched = available_stores.get(label)
            if matched is None:
                store_summary["key_stores"][label] = {"found": False}
                continue
            store_entry, sample = collect_store_stats(matched, label, show_decode_errors=show_decode_errors)
            store_summary["key_stores"][label] = store_entry
            if sample is not None:
                store_summary["samples"][label] = sample

    structured_by_call_id = {(call["call_id"] or "").lower(): call for call in calls if call.get("call_id")}
    structured_by_shared_correlation_id = {
        (call["shared_correlation_id"] or "").lower(): call
        for call in calls
        if call.get("shared_correlation_id")
    }
    for call in sorted(calllog_calls.values(), key=lambda item: (item.get("start_time") or "", item.get("call_id") or "")):
        call_id = (call.get("call_id") or "").lower()
        shared_correlation_id = (call.get("shared_correlation_id") or "").lower()
        existing = None
        if call_id:
            existing = structured_by_call_id.get(call_id)
        if existing is None and shared_correlation_id:
            existing = structured_by_shared_correlation_id.get(shared_correlation_id)
        if existing is not None:
            merge_call_records(existing, call)
            continue
        calls.append(call)

    for call in calls:
        originator_id = (call.get("originator_id") or "").lower()
        target_id = (call.get("target_id") or "").lower()
        if originator_id and not call.get("originator_display_name") and guid_to_name.get(originator_id):
            call["originator_display_name"] = guid_to_name[originator_id]
        if target_id and not call.get("target_display_name") and guid_to_name.get(target_id):
            call["target_display_name"] = guid_to_name[target_id]

        conversation_id = normalize_thread_id(call.get("conversation_id"))
        if conversation_id and conversation_id in threads:
            thread = threads[conversation_id]
            merge_thread_participant(thread, originator_id, call.get("originator_display_name"))
            merge_thread_participant(thread, target_id, call.get("target_display_name"))

    for thread_id, thread in threads.items():
        for participant_id in list(thread.get("participant_ids", [])):
            if participant_id and guid_to_name.get(participant_id):
                merge_thread_participant(thread, participant_id, guid_to_name[participant_id])

        for message in thread.get("messages", []):
            merge_thread_participant(
                thread,
                message.get("sender_id"),
                message.get("sender_display_name") or (guid_to_name.get(message.get("sender_id")) if message.get("sender_id") else None),
            )

        if is_placeholder_label(thread.get("label"), thread_id):
            metadata = thread.get("metadata") or {}
            chat_title_short = clean_text(metadata.get("chat_title_short"))
            if chat_title_short and chat_title_short != current_user_name:
                thread["label"] = chat_title_short

        if is_placeholder_label(thread.get("label"), thread_id):
            explicit_title = thread_titles.get(thread_id)
            if explicit_title:
                thread["label"] = explicit_title

        if is_placeholder_label(thread.get("label"), thread_id) and thread["category"] == "chat_space":
            others = [name for name in thread.get("participants", []) if name != current_user_name]
            if len(others) == 1:
                thread["label"] = others[0]

        if is_placeholder_label(thread.get("label"), thread_id):
            metadata = thread.get("metadata") or {}
            for field in ["space_thread_topic", "topic_thread_topic", "topic"]:
                if clean_text(metadata.get(field)):
                    thread["label"] = clean_text(metadata[field])
                    break

        if is_placeholder_label(thread.get("label"), thread_id):
            participant_list_label = build_participant_label(thread.get("participants", []), current_user_name)
            if participant_list_label:
                thread["label"] = participant_list_label

        if is_placeholder_label(thread.get("label"), thread_id):
            thread["label"] = thread_id

        thread["message_count"] = len(thread["messages"])
        thread["participants"] = sorted(set(thread.get("participants", [])))
        thread["participant_ids"] = sorted(set(thread.get("participant_ids", [])))
        thread["current_member_ids"] = sorted(set(thread.get("current_member_ids", [])))

    merge_thread_event_calls(calls, threads, guid_to_name)
    enrich_calls_for_current_user(calls, current_user_oid, current_user_name)

    ordered_threads = sorted(
        threads.values(),
        key=lambda item: (
            item["category"] not in {"team_chat", "meeting"},
            item["metadata_quality"] != "detailed",
            -item.get("message_count", 0),
            item["label"],
        ),
    )
    ordered_messages = [message for thread in ordered_threads for message in thread.get("messages", [])]
    first_message_at, last_message_at = iso_bounds([message.get("timestamp") for message in ordered_messages])
    first_call_at, last_call_at = iso_bounds(
        [
            value
            for call in calls
            for value in (call.get("start_time"), call.get("connect_time"), call.get("end_time"))
        ]
    )

    summary = {
        "threads_total": len(ordered_threads),
        "threads_with_detail": sum(thread["metadata_quality"] == "detailed" for thread in ordered_threads),
        "threads_with_messages": sum(bool(thread["messages"]) for thread in ordered_threads),
        "messages_total": sum(thread["message_count"] for thread in ordered_threads),
        "messages_with_attachments": sum(bool(message.get("attachments")) for message in ordered_messages),
        "messages_with_reactions": sum(bool(message.get("reactions")) for message in ordered_messages),
        "attachments_total": sum(len(message.get("attachments") or []) for message in ordered_messages),
        "reactions_total": sum(reaction_total(message.get("reactions")) for message in ordered_messages),
        "calls_total": len(calls),
        "people_total": len(guid_to_name),
        "first_message_at": first_message_at,
        "last_message_at": last_message_at,
        "first_call_at": first_call_at,
        "last_call_at": last_call_at,
    }

    payload = {
        "export_format": "teams-ccl-canonical-v1",
        "generated_at": datetime.now(tz=timezone.utc).isoformat(),
        "source_root": str(source_info.profile_root),
        "search_root": str(source_info.search_root),
        "platform": source_info.platform_name,
        "leveldb_path": str(leveldb_path),
        "blob_path": str(blob_path) if blob_path.exists() else None,
        "local_storage_dir": str(source_info.local_storage_dir) if source_info.local_storage_dir else None,
        "discovery_method": source_info.discovery_method,
        "backend": "ccl_chromium_reader",
        "profile": profile,
        "summary": summary,
        "threads": ordered_threads,
        "calls": sorted(calls, key=lambda item: item.get("start_time") or "", reverse=True),
        "guid_directory": dict(sorted(guid_to_name.items())),
        "limitations": [
            "Built from structured IndexedDB object stores using ccl_chromium_reader and the matching blob directory.",
            "A small number of keys reported decode errors during CCL iteration and may be missing from this export.",
            "This canonical export surfaces replychain attachments and reaction summaries, but it still does not merge every auxiliary store such as notification surfaces.",
        ],
    }
    if store_summary is not None:
        payload["_store_summary"] = store_summary
    return normalize_json_value(payload)


def main() -> None:
    parser = argparse.ArgumentParser(description="Export Teams data from structured IndexedDB stores via ccl_chromium_reader.")
    parser.add_argument("--root", help="Teams source root, profile directory, copied evidence root, or IndexedDB directory.")
    parser.add_argument("--output", default="teams_ccl_canonical_v1.json", help="Path to write JSON output.")
    args = parser.parse_args()

    payload = build_export(Path(args.root).resolve() if args.root else None)
    write_json(Path(args.output).resolve(), payload)


if __name__ == "__main__":
    main()
