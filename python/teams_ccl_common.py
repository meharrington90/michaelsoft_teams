#!/usr/bin/env python3

import io
import json
import re
from contextlib import ExitStack, contextmanager, redirect_stderr, redirect_stdout
from html import unescape
from pathlib import Path
from typing import Any


THREAD_ID_PATTERN = (
    r"(?:E?19:meeting_[A-Za-z0-9_-]+@thread\.v2|(?:-19:|19:)[^\s\"\x00]+@(?:thread\.v2|unq\.gbl\.spaces)|48:calllogs)"
)
STRICT_THREAD_ID_RE = re.compile(
    r"^(?:48:calllogs|E?19:meeting_[A-Za-z0-9_-]+@thread\.v2|-19:[^\s\"\x00]+@thread\.v2|19:[^\s\"\x00]+@thread\.v2|19:[^\s\"\x00]+@unq\.gbl\.spaces)$",
    re.I,
)
GUID_RE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I)
CONTROL_RE = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]+")
MULTISPACE_RE = re.compile(r"\s+")
HTML_TAG_RE = re.compile(r"<[^>]+>")
HTML_ATTR_RE = re.compile(r"([A-Za-z_:][-A-Za-z0-9_:.]*)\s*=\s*(['\"])(.*?)\2", re.S)
HTML_EMOJI_IMG_RE = re.compile(r"<img\b(?=[^>]*\bitemtype=(['\"])http://schema\.skype\.com/Emoji\1)[^>]*>", re.I)
EMOJI_CODEPOINT_RE = re.compile(r"^[0-9a-f]{4,6}(?:-[0-9a-f]{4,6})*$", re.I)
PROFILE_RE = re.compile(
    r'"displayName":"([^"]+)".+?"email":"([^"]+)".+?"tenantId":"([^"]+)".+?"oid":"([^"]+)"',
    re.S,
)
SAFE_NAME_RE = re.compile(r"[^A-Za-z0-9._-]+")


def read_text(path: Path) -> str:
    return path.read_bytes().decode("utf-8", "ignore")


def is_undefined_value(value: Any) -> bool:
    if isinstance(value, str):
        return value == "<Undefined>"
    return value is not None and value.__class__.__name__ == "_Undefined"


def clean_value(value: Any) -> str | None:
    if value is None or is_undefined_value(value):
        return None
    if not isinstance(value, str):
        return None
    value = CONTROL_RE.sub("", value)
    value = value.replace("\x00", "")
    value = value.strip()
    return value or None


def clean_text(value: str | None) -> str | None:
    value = clean_value(value)
    if value is None:
        return None
    value = MULTISPACE_RE.sub(" ", value)
    return value.strip() or None


def emoji_from_identifier(value: str | None) -> str | None:
    cleaned = clean_text(value)
    if not cleaned:
        return None
    codepoints = cleaned.strip("()").split("_", 1)[0]
    if not EMOJI_CODEPOINT_RE.fullmatch(codepoints):
        return None
    try:
        return "".join(chr(int(codepoint, 16)) for codepoint in codepoints.split("-"))
    except ValueError:
        return None


def replace_emoji_img_with_text(match: re.Match[str]) -> str:
    tag = match.group(0)
    attrs = {
        name.lower(): unescape(value)
        for name, _, value in HTML_ATTR_RE.findall(tag)
    }
    return (
        clean_text(attrs.get("alt"))
        or emoji_from_identifier(attrs.get("itemid"))
        or emoji_from_identifier(attrs.get("type"))
        or " "
    )


def html_to_text(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
    value = HTML_EMOJI_IMG_RE.sub(replace_emoji_img_with_text, value)
    value = HTML_TAG_RE.sub(" ", value)
    value = unescape(value)
    return clean_text(value)


def safe_name(value: str | None, default: str = "untitled") -> str:
    cleaned = SAFE_NAME_RE.sub("_", value or "")
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return cleaned or default


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def normalize_json_value(value: Any) -> Any:
    if is_undefined_value(value):
        return None
    if isinstance(value, dict):
        return {str(key): normalize_json_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize_json_value(item) for item in value]
    if isinstance(value, tuple):
        return [normalize_json_value(item) for item in value]
    return value


def write_json(path: Path, payload: Any, *, pretty: bool = True) -> None:
    kwargs = {"ensure_ascii": False}
    if pretty:
        kwargs["indent"] = 2
    else:
        kwargs["separators"] = (",", ":")
    path.write_text(json.dumps(normalize_json_value(payload), **kwargs), encoding="utf-8")


@contextmanager
def decode_output_context(show_decode_errors: bool):
    if show_decode_errors:
        yield
        return

    sink = io.StringIO()
    with ExitStack() as stack:
        stack.enter_context(redirect_stdout(sink))
        stack.enter_context(redirect_stderr(sink))
        yield


def normalize_thread_id(value: str | None) -> str | None:
    value = clean_value(value)
    if value is None:
        return None
    value = value.lstrip("[")
    if STRICT_THREAD_ID_RE.match(value):
        return value
    return None


def classify_thread(thread_id: str, thread_type: str | None = None) -> str:
    if thread_id == "48:calllogs":
        return "call_logs"
    normalized_type = (clean_text(thread_type) or "").lower()
    if normalized_type == "meeting" or thread_id.startswith(("E19:meeting_", "19:meeting_")):
        return "team_chat"
    if thread_id.endswith("@unq.gbl.spaces"):
        return "chat_space"
    if thread_id.endswith("@thread.v2"):
        return "thread"
    return "unknown"


def init_thread_record(thread_id: str) -> dict:
    return {
        "id": thread_id,
        "category": classify_thread(thread_id),
        "label": None,
        "metadata_quality": "inventory_only",
        "inventory": {},
        "metadata": {},
        "meeting": None,
        "participants": [],
        "participant_ids": [],
        "current_member_ids": [],
        "last_message": None,
        "messages": [],
        "source_files": [],
    }


def parse_profile(local_storage_dir: Path) -> dict | None:
    for path in sorted(local_storage_dir.glob("*")):
        if path.suffix not in {".ldb", ".log"}:
            continue
        try:
            data = read_text(path)
        except Exception:
            continue
        match = PROFILE_RE.search(data)
        if not match:
            continue
        return {
            "display_name": clean_text(match.group(1)),
            "email": clean_text(match.group(2)),
            "tenant_id": clean_text(match.group(3)),
            "oid": clean_text(match.group(4)),
            "source": str(path),
        }
    return None
