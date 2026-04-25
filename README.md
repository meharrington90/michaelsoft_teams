# Michaelsoft Teams

Microsoft Teams is (apparently) a collaborative business platform. In practice, it's more like a padded corporate messaging container made from old Skype, Electron, bad decisions, and just enough convenience for businesses to keep tolerating it.

MSTeams stores your messages, meetings, calls, and attachment metadata locally on your machine for caching purposes (unencrypted)... which is fascinating, cause it also pretends like you're unable to copy, export, archive, or review any chat data without requesting it from your local IT Professional.

So... me being an IT Professional... decided to make **Michaelsoft Teams**.


This project exists because I wanted ownership over my own communication data, but Microsoft is apparently uncomfortable with that concept. **Michaelsoft Teams** reads local MSTeams database artifacts directly from the newer Teams client, pulls all useful data into structured exports, and then generates a standalone browser app that is actually pleasant to use... which makes this far more emotionally supportive than MSTeams itself.

In plain English: this tool lets you save/view/archive your own data from the bloated Microsoft prison box that originally collected it.


## Why This Exists

Because "searching your own message history" should not feel like an act of archaeological recovery.

Because "exporting your own communication data" should not require prayer, packet captures, and emotional resilience.

Because if software stores my conversations on my computer, I reserve the right to inspect them with something better than the native UI equivalent of a mandatory team-building exercise.

Michaelsoft Teams is built for:

- forensic review
- local archiving
- offline browsing
- structured export
- proving that your data does, in fact, belong to you

## Current Scope

Michaelsoft Teams currently:

- automatically discovers the current Teams profile on macOS and Windows, or accepts an explicit `--root` pointing at a copied evidence root, profile root, IndexedDB root, or `.leveldb` directory
- refreshes a repo-local snapshot of the active Teams IndexedDB/blob data and Local Storage profile hints under `Library/TeamsSourceArchive/current/` on each normal run, then builds exports from that snapshot so the source data remains archived locally if the live files disappear later
- uses `ccl_chromium_reader` to decode structured IndexedDB stores from the Teams profile and matching blob directory
- builds a summary report, canonical JSON export, flat CSVs, per-conversation CSVs, a run manifest, and a standalone HTML viewer
- extracts message attachments currently recoverable from replychains, including inline images, inline videos, direct attachment records, and file/share links surfaced through message HTML or message properties
- merges structured call-history records with call events inferred from conversation messages so the browser can cross-link related calls and message timelines
- includes a browser UI with separate Messages and Calls views, search, filters, date ranges, linked navigation, and direct links to conversation CSVs

## What It Does

Michaelsoft Teams pulls useful artifacts out of the local Teams client and turns them into outputs a human can read without entering a dissociative state.

It reads the local IndexedDB profile, produces structured JSON and CSV exports, and builds a single-file HTML interface for reviewing:

- messages
- meetings
- calls
- attachment references
- conversation timelines

All offline. All locally. All without having to beg Teams to cooperate.

## How To Run

Use one of the launchers from the repo root:

- macOS: `MacOS Launcher.command`
- Windows: `Windows Launcher.bat`

Both launchers:

- create `.venv/` with local Python when available
- fall back to a bundled `uv` runtime when Python is not installed
- install dependencies on first run
- refresh the repo-local Teams artifact snapshot and run `python/run_teams_pipeline.py --open-browser`
- pause at the end so you can review any errors instead of watching a terminal window vanish like a witness in a conspiracy movie

After a successful run, the generated browser viewer opens automatically in your default browser.

If you want to run it manually:

```bash
python3 -m venv .venv
. .venv/bin/activate
python python/bootstrap_dependencies.py
python python/run_teams_pipeline.py --open-browser
```

If you need to bypass the snapshot refresh and read directly from the discovered source, use:

```bash
python python/run_teams_pipeline.py --skip-source-archive
```
