#!/usr/bin/env python3

import argparse
import json
from pathlib import Path

from teams_ccl_common import thread_csv_filename


def thread_csv_path(thread: dict) -> str:
    return f"teams_ccl_csv_v1/conversations/{thread_csv_filename(thread)}"


HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Michaelsoft Teams</title>
  <style>
    :root {
      --bg: #eef4ff;
      --bg-alt: #fff4e7;
      --panel: rgba(255,255,255,.82);
      --panel-strong: rgba(255,255,255,.96);
      --panel-soft: rgba(244,247,255,.88);
      --ink: #14233b;
      --muted: #5f6f86;
      --muted-strong: #415068;
      --line: rgba(123,145,179,.24);
      --line-strong: rgba(88,110,147,.34);
      --accent: #2563eb;
      --accent-strong: #1d4ed8;
      --accent-soft: rgba(37,99,235,.12);
      --accent-soft-strong: rgba(37,99,235,.18);
      --accent-alt: #f97316;
      --accent-alt-soft: rgba(249,115,22,.14);
      --success: #0f766e;
      --success-soft: rgba(15,118,110,.16);
      --warn: #c2410c;
      --warn-soft: rgba(194,65,12,.14);
      --shadow: 0 16px 34px rgba(15,23,42,.09);
      --shadow-soft: 0 10px 24px rgba(37,99,235,.10);
      --radius-xl: 24px;
      --radius-lg: 18px;
      --radius-md: 14px;
      --radius-sm: 10px;
      --ease: cubic-bezier(.2,.8,.2,1);
      --mono: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
      --sans: "Avenir Next", "Segoe UI Variable", "Segoe UI", "Helvetica Neue", Arial, sans-serif;
      --display: "Avenir Next", "Segoe UI Variable", "Segoe UI", "Helvetica Neue", Arial, sans-serif;
      --pcb-brand: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 220 180' fill='none'%3E%3Cg stroke='%23dbeafe' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round' stroke-opacity='.30'%3E%3Cpath d='M10 28h36c8 0 12 4 12 12v18c0 8 4 12 12 12h30'/%3E%3Cpath d='M140 18v22c0 8-4 12-12 12h-18c-8 0-12 4-12 12v24'/%3E%3Cpath d='M78 118h28c8 0 12-4 12-12V88c0-8 4-12 12-12h34'/%3E%3Cpath d='M188 56v20c0 8-4 12-12 12h-16c-8 0-12 4-12 12v28'/%3E%3Cpath d='M24 144h30c8 0 12-4 12-12v-10c0-8 4-12 12-12h28'/%3E%3Cpath d='M118 146h22c8 0 12-4 12-12v-8c0-8 4-12 12-12h24'/%3E%3Cpath d='M36 84h18c8 0 12-4 12-12V58c0-8 4-12 12-12h20'/%3E%3Cpath d='M174 130v-18c0-8 4-12 12-12h20'/%3E%3C/g%3E%3Cg fill='%23ffffff' fill-opacity='.38'%3E%3Ccircle cx='10' cy='28' r='3'/%3E%3Ccircle cx='100' cy='52' r='3'/%3E%3Ccircle cx='140' cy='18' r='3'/%3E%3Ccircle cx='164' cy='76' r='3'/%3E%3Ccircle cx='188' cy='130' r='3'/%3E%3Ccircle cx='24' cy='144' r='3'/%3E%3Ccircle cx='106' cy='110' r='3'/%3E%3Ccircle cx='186' cy='146' r='3'/%3E%3Ccircle cx='98' cy='46' r='3'/%3E%3C/g%3E%3C/svg%3E");
      --pcb-panel: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 96 96' fill='none'%3E%3Cg stroke='%231d4ed8' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round' stroke-opacity='.18'%3E%3Cpath d='M10 18h18c6 0 9 3 9 9v9c0 6 3 9 9 9h16'/%3E%3Cpath d='M70 12v18c0 6-3 9-9 9H49c-6 0-9 3-9 9v11'/%3E%3Cpath d='M18 72h19c6 0 9-3 9-9v-4c0-6 3-9 9-9h13'/%3E%3C/g%3E%3Cg fill='%231d4ed8' fill-opacity='.12'%3E%3Ccircle cx='10' cy='18' r='2.6'/%3E%3Ccircle cx='62' cy='45' r='2.6'/%3E%3Ccircle cx='70' cy='12' r='2.6'/%3E%3Ccircle cx='18' cy='72' r='2.6'/%3E%3C/g%3E%3C/svg%3E");
    }
    html {
      color-scheme: light;
    }
    *,
    *::before,
    *::after {
      box-sizing: border-box;
    }
    * {
      scrollbar-width: thin;
      scrollbar-color: rgba(77,102,140,.34) transparent;
    }
    *::-webkit-scrollbar {
      width: 11px;
      height: 11px;
    }
    *::-webkit-scrollbar-track {
      background: transparent;
    }
    *::-webkit-scrollbar-thumb {
      background: rgba(77,102,140,.28);
      border: 3px solid transparent;
      border-radius: 999px;
      background-clip: padding-box;
    }
    *::-webkit-scrollbar-thumb:hover {
      background: rgba(77,102,140,.44);
      background-clip: padding-box;
    }
    ::selection {
      background: rgba(37,99,235,.22);
    }
    body {
      margin: 0;
      min-height: 100vh;
      height: 100vh;
      overflow: hidden;
      font-family: var(--sans);
      color: var(--ink);
      background:
        radial-gradient(circle at 0% 0%, rgba(37,99,235,.16), transparent 28%),
        radial-gradient(circle at 100% 0%, rgba(14,165,233,.12), transparent 24%),
        radial-gradient(circle at 55% 100%, rgba(15,118,110,.10), transparent 24%),
        linear-gradient(180deg, #f8fbff 0%, #edf4ff 52%, #eef7fb 100%);
      padding: 8px;
      position: relative;
    }
    body::before,
    body::after {
      content: "";
      position: fixed;
      pointer-events: none;
      inset: auto;
      filter: blur(36px);
      opacity: .75;
      z-index: 0;
    }
    body::before {
      width: 280px;
      height: 280px;
      top: 5%;
      right: 10%;
      border-radius: 999px;
      background: rgba(37,99,235,.14);
    }
    body::after {
      width: 260px;
      height: 260px;
      left: 3%;
      bottom: 4%;
      border-radius: 999px;
      background: rgba(14,165,233,.12);
    }
    button,
    input,
    select {
      font: inherit;
    }
    button {
      appearance: none;
      border: 0;
      background: none;
      color: inherit;
    }
    a {
      color: inherit;
      text-decoration: none;
    }
    h1,
    h2,
    h3 {
      margin: 0;
      font-family: var(--display);
      font-weight: 700;
      letter-spacing: 0;
    }
    .app {
      position: relative;
      z-index: 1;
      display: grid;
      grid-template-columns: 380px minmax(0, 1fr);
      gap: 10px;
      width: 100%;
      height: calc(100vh - 16px);
      max-width: none;
      margin: 0;
    }
    .sidebar,
    .overview-panel,
    .content-panel {
      border: 1px solid var(--line);
      box-shadow: var(--shadow);
    }
    .sidebar {
      position: relative;
      display: flex;
      flex-direction: column;
      min-width: 0;
      min-height: 0;
      overflow: hidden;
      border-radius: var(--radius-xl);
      padding: 11px;
      background:
        linear-gradient(180deg, rgba(255,255,255,.84) 0%, rgba(246,249,255,.78) 100%);
    }
    .sidebar-top {
      display: grid;
      gap: 8px;
      min-width: 0;
      padding-bottom: 8px;
    }
    .brand-card {
      position: relative;
      isolation: isolate;
      display: grid;
      align-content: start;
      gap: 6px;
      padding: 18px;
      border-radius: 20px;
      overflow: hidden;
      background:
        linear-gradient(145deg, #102447 0%, #173874 34%, #1d4ed8 68%, #0f766e 100%);
      color: #fff;
      box-shadow: 0 16px 34px rgba(29,78,216,.20);
    }
    .brand-card::before {
      content: "";
      position: absolute;
      inset: 0;
      pointer-events: none;
      background:
        linear-gradient(135deg, rgba(255,255,255,.14) 0%, rgba(255,255,255,0) 42%);
      opacity: .9;
      z-index: 0;
    }
    .brand-card::after {
      content: "";
      position: absolute;
      top: 14px;
      right: 16px;
      bottom: 14px;
      width: 158px;
      pointer-events: none;
      border: 1px solid rgba(255,255,255,.16);
      border-radius: 18px;
      background:
        linear-gradient(180deg, rgba(255,255,255,.10), rgba(255,255,255,0) 74%),
        var(--pcb-brand) center / cover no-repeat;
      clip-path: polygon(24% 0, 100% 0, 100% 100%, 0 100%, 0 28%);
      opacity: .74;
      z-index: 0;
    }
    .brand-card > * {
      position: relative;
      z-index: 1;
    }
    .brand-kicker,
    .kicker {
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: .18em;
      font-weight: 700;
    }
    .brand-kicker {
      color: rgba(255,255,255,.82);
      order: 2;
    }
    .brand-title {
      font-family: var(--display);
      font-size: 28px;
      line-height: 1.05;
      letter-spacing: 0;
      font-weight: 700;
      order: 1;
    }
    .brand-profile {
      font-size: 13px;
      line-height: 1.45;
      color: rgba(255,255,255,.86);
      max-width: 100%;
    }
    .brand-profile {
      order: 3;
    }
    .view-tabs {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 6px;
      padding: 3px;
      border-radius: 16px;
      border: 1px solid var(--line);
      background: rgba(255,255,255,.72);
      box-shadow: inset 0 1px 0 rgba(255,255,255,.75);
    }
    .tab {
      border: 1px solid transparent;
      border-radius: 13px;
      min-height: 40px;
      padding: 6px 10px;
      color: var(--muted-strong);
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      transition:
        transform .18s var(--ease),
        border-color .18s var(--ease),
        color .18s var(--ease),
        background .18s var(--ease),
        box-shadow .18s var(--ease);
    }
    .tab:hover {
      transform: translateY(-1px);
      color: var(--ink);
    }
    .tab.active {
      color: var(--accent-strong);
      background: linear-gradient(180deg, rgba(255,255,255,.95), rgba(232,241,255,.98));
      border-color: rgba(37,99,235,.18);
      box-shadow: 0 8px 22px rgba(37,99,235,.14);
    }
    .toolbar {
      display: grid;
      gap: 7px;
      padding: 10px;
      border-radius: var(--radius-lg);
      border: 1px solid var(--line);
      background: linear-gradient(180deg, rgba(255,255,255,.84), rgba(245,248,255,.78));
      box-shadow: 0 10px 30px rgba(15,23,42,.07);
      align-items: stretch;
    }
    .hidden {
      display: none !important;
    }
    input,
    select {
      width: 100%;
      min-width: 0;
      max-width: 100%;
      min-height: 42px;
      padding: 8px 11px;
      border-radius: 12px;
      border: 1px solid rgba(88,110,147,.16);
      background: rgba(255,255,255,.96);
      color: var(--ink);
      box-shadow:
        inset 0 1px 0 rgba(255,255,255,.78),
        0 1px 2px rgba(15,23,42,.04);
      transition:
        border-color .18s var(--ease),
        box-shadow .18s var(--ease),
        transform .18s var(--ease);
    }
    input::placeholder {
      color: #8191a6;
    }
    input:focus,
    select:focus {
      outline: none;
      border-color: rgba(37,99,235,.46);
      box-shadow:
        0 0 0 4px rgba(37,99,235,.12),
        0 12px 24px rgba(37,99,235,.08);
      transform: translateY(-1px);
    }
    .tab:focus-visible,
    .seg-btn:focus-visible,
    .call-link:focus-visible,
    .filter-pill:focus-visible,
    .toggle-expandable-list:focus-visible {
      outline: none;
      box-shadow:
        0 0 0 4px rgba(37,99,235,.12),
        0 14px 24px rgba(37,99,235,.12);
    }
    .toolbar > * {
      min-width: 0;
    }
    .activity-month-nav {
      display: grid;
      grid-template-columns: 38px minmax(0, 1fr) 38px;
      gap: 6px;
      align-items: center;
    }
    .activity-month-nav .call-link {
      min-height: 38px;
      border-radius: 12px;
      padding: 0;
      font-size: 15px;
    }
    .activity-month-nav input[type="month"] {
      min-height: 38px;
    }
    .activity-work-hours {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 7px;
    }
    .activity-workdays {
      display: grid;
      grid-template-columns: repeat(7, minmax(0, 1fr));
      gap: 4px;
    }
    .workday-toggle {
      min-width: 0;
      cursor: pointer;
    }
    .workday-toggle input {
      position: absolute;
      opacity: 0;
      pointer-events: none;
    }
    .workday-toggle span {
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 30px;
      padding: 5px 2px;
      border-radius: 10px;
      border: 1px solid rgba(88,110,147,.14);
      background: rgba(226,232,240,.76);
      color: #64748b;
      font-size: 10px;
      line-height: 1;
      font-weight: 800;
      letter-spacing: .04em;
      transition:
        background .18s var(--ease),
        border-color .18s var(--ease),
        box-shadow .18s var(--ease),
        color .18s var(--ease);
    }
    .workday-toggle input:checked + span {
      color: var(--accent-strong);
      background: rgba(232,241,255,.96);
      border-color: rgba(37,99,235,.22);
      box-shadow: 0 6px 12px rgba(37,99,235,.08);
    }
    .workday-toggle input:focus-visible + span {
      outline: none;
      box-shadow:
        0 0 0 4px rgba(37,99,235,.12),
        0 6px 12px rgba(37,99,235,.08);
    }
    .activity-calendar {
      display: grid;
      gap: 8px;
      padding: 10px;
      border-radius: var(--radius-lg);
      border: 1px solid var(--line);
      background:
        linear-gradient(180deg, rgba(255,255,255,.90), rgba(245,248,255,.76));
      box-shadow:
        inset 0 1px 0 rgba(255,255,255,.78),
        0 8px 18px rgba(15,23,42,.05);
    }
    .calendar-heading {
      display: flex;
      justify-content: center;
      gap: 8px;
      align-items: center;
      text-align: center;
      color: var(--muted-strong);
      font-size: 12px;
      font-weight: 700;
    }
    .calendar-grid {
      display: grid;
      grid-template-columns: repeat(7, minmax(0, 1fr));
      gap: 4px;
    }
    .calendar-weekday {
      min-height: 20px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--muted);
      font-size: 10px;
      font-weight: 800;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    .calendar-day {
      position: relative;
      display: grid;
      place-items: center;
      gap: 1px;
      width: 100%;
      min-width: 0;
      aspect-ratio: 1;
      padding: 4px 2px;
      border-radius: 11px;
      border: 1px solid rgba(88,110,147,.13);
      background: rgba(255,255,255,.78);
      color: var(--muted-strong);
      cursor: pointer;
      transition:
        transform .18s var(--ease),
        border-color .18s var(--ease),
        background .18s var(--ease),
        box-shadow .18s var(--ease);
    }
    .calendar-day:hover {
      transform: translateY(-1px);
      border-color: rgba(37,99,235,.26);
      background: rgba(255,255,255,.98);
      box-shadow: 0 8px 14px rgba(37,99,235,.08);
    }
    .calendar-day:focus-visible {
      outline: none;
      box-shadow:
        0 0 0 4px rgba(37,99,235,.12),
        0 8px 14px rgba(37,99,235,.08);
    }
    .calendar-day.outside {
      opacity: .42;
    }
    .calendar-day.today {
      border-color: rgba(15,118,110,.28);
      color: var(--success);
    }
    .calendar-day.active {
      border-color: rgba(37,99,235,.30);
      background: linear-gradient(180deg, rgba(232,241,255,.98), rgba(255,255,255,.94));
      color: var(--accent-strong);
      box-shadow: 0 10px 18px rgba(37,99,235,.12);
    }
    .calendar-day.off-workday,
    .calendar-day.inactive-workday {
      background: rgba(226,232,240,.76);
      border-color: rgba(100,116,139,.18);
      color: #64748b;
    }
    .calendar-day.off-workday.active,
    .calendar-day.inactive-workday.active {
      border-color: rgba(37,99,235,.32);
      background:
        linear-gradient(180deg, rgba(232,241,255,.72), rgba(226,232,240,.84));
    }
    .calendar-date-num {
      font-size: 13px;
      line-height: 1;
      font-weight: 800;
    }
    .calendar-count {
      min-height: 11px;
      color: var(--muted);
      font-size: 9px;
      line-height: 1;
      font-weight: 700;
    }
    .calendar-activity-dot {
      width: 7px;
      height: 7px;
      border-radius: 999px;
      background: #111827;
      box-shadow: 0 0 0 2px rgba(17,24,39,.10);
    }
    .calendar-activity-dot.minimal {
      background: #DC2626;
      box-shadow: 0 0 0 2px rgba(220,38,38,.14);
    }
    .calendar-activity-dot.low {
      background: #EAB308;
      box-shadow: 0 0 0 2px rgba(234,179,8,.16);
    }
    .calendar-activity-dot.average {
      background: #16A34A;
      box-shadow: 0 0 0 2px rgba(22,163,74,.14);
    }
    .calendar-activity-dot.high {
      background: #2563EB;
      box-shadow: 0 0 0 2px rgba(37,99,235,.16);
    }
    .activity-sidebar-summary {
      display: grid;
      gap: 5px;
    }
    .activity-sidebar-stat {
      display: flex;
      justify-content: space-between;
      gap: 7px;
      align-items: center;
      padding: 6px 8px;
      border-radius: 12px;
      border: 1px solid rgba(88,110,147,.14);
      background: rgba(255,255,255,.78);
      color: var(--muted-strong);
      font-size: 11px;
      line-height: 1.18;
    }
    .activity-sidebar-stat strong {
      color: var(--ink);
      font-size: 12px;
    }
    .chip-row,
    .chips,
    .jump-list,
    .call-event-actions,
    .segmented {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }
    .active-filter-bar {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      min-height: 0;
    }
    .sidebar-divider {
      height: 1px;
      background: linear-gradient(90deg, transparent, rgba(88,110,147,.18), transparent);
      margin-right: 2px;
      flex: 0 0 auto;
    }
    .sidebar-list-wrap {
      flex: 1 1 auto;
      min-height: 0;
      overflow: auto;
      padding: 8px 1px 1px;
      scrollbar-gutter: stable;
    }
    .chip,
    .filter-pill,
    .list-pill,
    .msg-mini-chip {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 9px;
      border-radius: 999px;
      font-size: 11px;
      line-height: 1;
      border: 1px solid rgba(88,110,147,.18);
      background: rgba(255,255,255,.9);
      color: var(--muted-strong);
      white-space: nowrap;
    }
    .chip-strong {
      color: var(--accent-strong);
      background: rgba(232,241,255,.95);
      border-color: rgba(37,99,235,.20);
      box-shadow: 0 8px 20px rgba(37,99,235,.10);
    }
    .hotkey-chip {
      background: rgba(255,255,255,.72);
    }
    .filter-pill {
      cursor: pointer;
      transition:
        transform .18s var(--ease),
        background .18s var(--ease),
        border-color .18s var(--ease);
    }
    .filter-pill:hover {
      transform: translateY(-1px);
      background: rgba(255,255,255,.98);
      border-color: rgba(37,99,235,.24);
    }
    .filter-pill .dismiss {
      color: var(--accent-strong);
      font-weight: 700;
    }
    .list {
      display: grid;
      gap: 7px;
    }
    .list-row {
      position: relative;
      min-width: 0;
      overflow: hidden;
      padding: 10px 11px;
      border-radius: 16px;
      border: 1px solid transparent;
      background:
        linear-gradient(180deg, rgba(255,255,255,.86), rgba(245,248,255,.70));
      box-shadow:
        inset 0 1px 0 rgba(255,255,255,.78),
        0 6px 12px rgba(15,23,42,.04);
      cursor: pointer;
      transition:
        transform .18s var(--ease),
        box-shadow .18s var(--ease),
        border-color .18s var(--ease),
        background .18s var(--ease);
    }
    .list-row::before {
      content: "";
      position: absolute;
      inset: 0 auto 0 0;
      width: 4px;
      border-radius: 999px;
      background: var(--row-accent, var(--accent));
      opacity: .72;
    }
    .list-row:hover {
      transform: translateY(-2px);
      border-color: rgba(88,110,147,.20);
      box-shadow:
        0 12px 20px rgba(15,23,42,.06),
        0 0 0 1px rgba(255,255,255,.55) inset;
    }
    .list-row.active {
      border-color: rgba(37,99,235,.22);
      background:
        linear-gradient(180deg, rgba(236,243,255,.98), rgba(248,250,255,.92));
      box-shadow:
        0 14px 24px rgba(37,99,235,.10),
        0 0 0 1px rgba(255,255,255,.75) inset;
    }
    .list-row strong,
    .list-title {
      display: block;
      font-size: 14px;
      line-height: 1.28;
      overflow-wrap: anywhere;
      word-break: break-word;
    }
    .list-row-top,
    .list-stats,
    .list-row .meta {
      display: flex;
      justify-content: space-between;
      gap: 8px;
      align-items: center;
      min-width: 0;
    }
    .list-row-top {
      margin-bottom: 5px;
    }
    .list-row .meta,
    .list-time,
    .list-stats {
      color: var(--muted);
      font-size: 11px;
    }
    .list-stats {
      margin-top: 6px;
      color: var(--muted-strong);
    }
    .list-pill {
      color: var(--muted-strong);
      background: rgba(255,255,255,.76);
    }
    .preview {
      margin-top: 5px;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.4;
      display: -webkit-box;
      -webkit-line-clamp: 1;
      -webkit-box-orient: vertical;
      overflow: hidden;
      overflow-wrap: anywhere;
      word-break: break-word;
    }
    .main {
      position: relative;
      min-width: 0;
      min-height: 0;
      overflow: hidden;
      padding-right: 0;
    }
    .main-scroll {
      min-width: 0;
      min-height: 0;
      height: 100%;
      overflow: auto;
      scrollbar-gutter: stable;
    }
    .main-shell {
      display: grid;
      gap: 8px;
      min-height: 100%;
      align-content: start;
      padding-bottom: 6px;
    }
    .panel {
      min-width: 0;
      border-radius: var(--radius-xl);
      background:
        linear-gradient(180deg, rgba(255,255,255,.88), rgba(246,249,255,.78));
    }
    .overview-panel {
      position: sticky;
      top: 0;
      z-index: 6;
      padding: 14px 16px;
      background:
        linear-gradient(180deg, rgba(255,255,255,.94), rgba(244,248,255,.90));
      box-shadow:
        var(--shadow),
        0 0 0 1px rgba(255,255,255,.48) inset;
    }
    .overview-head {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: center;
      flex-wrap: wrap;
      margin-bottom: 10px;
    }
    .overview-quote {
      flex: 1 1 720px;
      max-width: min(980px, 100%);
      color: var(--muted-strong);
      font-size: 12px;
      line-height: 1.4;
      font-style: italic;
      font-weight: 500;
    }
    .overview-subtle {
      margin-top: 8px;
      color: var(--muted);
      font-size: 14px;
      line-height: 1.5;
    }
    .overview-side {
      display: grid;
      gap: 4px;
      justify-items: end;
      text-align: right;
    }
    .overview-mode {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 34px;
      padding: 5px 10px;
      border-radius: 999px;
      font-size: 10px;
      font-weight: 700;
      letter-spacing: .06em;
      text-transform: uppercase;
      color: var(--accent-strong);
      background: rgba(232,241,255,.92);
      border: 1px solid rgba(37,99,235,.18);
    }
    .summary {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 7px;
    }
    .card {
      position: relative;
      isolation: isolate;
      overflow: hidden;
      padding: 10px 10px 12px;
      border-radius: var(--radius-lg);
      border: 1px solid rgba(88,110,147,.16);
      box-shadow:
        0 12px 28px rgba(15,23,42,.06),
        0 0 0 1px rgba(255,255,255,.64) inset;
      background:
        linear-gradient(180deg, rgba(255,255,255,.96), rgba(245,248,255,.86));
    }
    .card::before {
      content: "";
      position: absolute;
      inset: 0 0 0 auto;
      width: 34%;
      pointer-events: none;
      background:
        linear-gradient(145deg, rgba(255,255,255,0) 0%, var(--card-geo, rgba(37,99,235,.14)) 24%, rgba(255,255,255,0) 100%);
      clip-path: polygon(30% 0, 100% 0, 100% 100%, 0 100%, 0 34%);
      opacity: .82;
      z-index: 0;
    }
    .card::after {
      content: "";
      position: absolute;
      top: 10px;
      right: 10px;
      bottom: 10px;
      width: 72px;
      pointer-events: none;
      border: 1px solid var(--card-outline, rgba(37,99,235,.10));
      border-radius: 14px;
      background:
        linear-gradient(180deg, rgba(255,255,255,.14), rgba(255,255,255,0) 76%),
        var(--pcb-panel) center / 92px 92px no-repeat;
      clip-path: polygon(24% 0, 100% 0, 100% 100%, 0 100%, 0 26%);
      opacity: .70;
      z-index: 0;
    }
    .threads-card {
      --card-geo: rgba(37,99,235,.16);
      --card-outline: rgba(37,99,235,.12);
    }
    .days-card {
      --card-geo: rgba(99,102,241,.15);
      --card-outline: rgba(99,102,241,.12);
    }
    .messages-card {
      --card-geo: rgba(14,165,233,.16);
      --card-outline: rgba(14,165,233,.12);
    }
    .calls-card {
      --card-geo: rgba(15,118,110,.16);
      --card-outline: rgba(15,118,110,.12);
    }
    .attachments-card {
      --card-geo: rgba(249,115,22,.16);
      --card-outline: rgba(249,115,22,.12);
    }
    .reactions-card {
      --card-geo: rgba(190,24,93,.13);
      --card-outline: rgba(190,24,93,.10);
    }
    .card .label {
      position: relative;
      z-index: 1;
      margin-bottom: 4px;
      color: var(--muted);
      font-size: 10px;
      font-weight: 700;
      letter-spacing: .12em;
      text-transform: uppercase;
    }
    .card .value {
      position: relative;
      z-index: 1;
      font-family: var(--display);
      font-size: 28px;
      line-height: .95;
      color: var(--ink);
      letter-spacing: -.03em;
    }
    .content-panel {
      padding: 15px;
      border-radius: var(--radius-xl);
      background:
        linear-gradient(180deg, rgba(255,255,255,.84), rgba(247,249,255,.78));
      box-shadow:
        var(--shadow),
        0 0 0 1px rgba(255,255,255,.46) inset;
    }
    .title {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      flex-wrap: wrap;
      gap: 7px;
      margin-bottom: 8px;
      min-width: 0;
    }
    .title > * {
      min-width: 0;
    }
    .title h1,
    .title h2,
    .title h3 {
      overflow-wrap: anywhere;
      word-break: break-word;
    }
    .detail-hero,
    .detail-toolbar,
    .search-group,
    .meta-block,
    .stat-card {
      border: 1px solid rgba(88,110,147,.16);
      border-radius: var(--radius-lg);
      background:
        linear-gradient(180deg, rgba(255,255,255,.92), rgba(245,248,255,.82));
      box-shadow:
        0 8px 18px rgba(15,23,42,.04),
        0 0 0 1px rgba(255,255,255,.56) inset;
    }
    .detail-hero {
      isolation: isolate;
      padding: 13px;
      margin-bottom: 10px;
      position: relative;
      overflow: hidden;
    }
    .detail-hero::before {
      content: "";
      position: absolute;
      inset: 0 0 0 auto;
      width: 28%;
      pointer-events: none;
      background:
        linear-gradient(145deg, rgba(255,255,255,0) 0%, rgba(37,99,235,.12) 22%, rgba(14,165,233,.05) 72%, rgba(255,255,255,0) 100%);
      clip-path: polygon(30% 0, 100% 0, 100% 100%, 0 100%, 0 34%);
      opacity: .84;
      z-index: 0;
    }
    .detail-hero::after {
      content: "";
      position: absolute;
      top: 12px;
      right: 14px;
      bottom: 12px;
      width: 92px;
      pointer-events: none;
      border: 1px solid rgba(37,99,235,.10);
      border-radius: 16px;
      background:
        linear-gradient(180deg, rgba(255,255,255,.14), rgba(255,255,255,0) 74%),
        var(--pcb-panel) center / 96px 96px no-repeat;
      clip-path: polygon(24% 0, 100% 0, 100% 100%, 0 100%, 0 28%);
      opacity: .68;
      z-index: 0;
    }
    .detail-hero > * {
      position: relative;
      z-index: 1;
    }
    .detail-hero .title {
      margin-bottom: 4px;
    }
    .detail-subtle,
    .subtle {
      color: var(--muted);
      font-size: 13px;
      line-height: 1.45;
    }
    .participant-cloud {
      margin-top: 10px;
    }
    .detail-toolbar {
      display: grid;
      gap: 7px;
      margin: 10px 0;
      padding: 10px;
    }
    .toolbar-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 7px;
      flex-wrap: wrap;
    }
    .range-controls,
    .sidebar-range-controls {
      display: flex;
      gap: 7px;
      flex-wrap: wrap;
      align-items: end;
      width: 100%;
    }
    .sidebar-range-controls {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }
    .sidebar-range-controls .range-field {
      min-width: 0;
    }
    .sidebar-range-controls .range-action {
      grid-column: 1 / -1;
      min-height: 36px;
      border-radius: 12px;
    }
    .toolbar-divider,
    .search-group-divider {
      height: 1px;
      width: 100%;
      background: linear-gradient(90deg, transparent, rgba(88,110,147,.18), transparent);
    }
    .range-field {
      display: grid;
      gap: 3px;
      min-width: 140px;
    }
    .range-field span {
      color: var(--muted);
      font-size: 11px;
      font-weight: 700;
      letter-spacing: .12em;
      text-transform: uppercase;
    }
    .seg-btn {
      padding: 6px 9px;
      border-radius: 999px;
      border: 1px solid rgba(88,110,147,.16);
      background: rgba(255,255,255,.86);
      color: var(--muted-strong);
      font-size: 12px;
      line-height: 1.2;
      font-weight: 600;
      cursor: pointer;
      transition:
        transform .18s var(--ease),
        border-color .18s var(--ease),
        background .18s var(--ease),
        color .18s var(--ease),
        box-shadow .18s var(--ease);
    }
    .seg-btn:hover,
    .call-link:hover,
    .toggle-expandable-list:hover {
      transform: translateY(-1px);
    }
    .seg-btn.active {
      color: var(--accent-strong);
      border-color: rgba(37,99,235,.22);
      background: rgba(232,241,255,.96);
      box-shadow: 0 6px 12px rgba(37,99,235,.08);
    }
    .call-link,
    .toggle-expandable-list {
      padding: 5px 8px;
      border-radius: 999px;
      border: 1px solid rgba(37,99,235,.18);
      background: linear-gradient(180deg, rgba(255,255,255,.96), rgba(232,241,255,.92));
      color: var(--accent-strong);
      font-size: 12px;
      line-height: 1.2;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      transition:
        transform .18s var(--ease),
        box-shadow .18s var(--ease),
        border-color .18s var(--ease),
        background .18s var(--ease);
      box-shadow: 0 4px 10px rgba(37,99,235,.06);
    }
    .call-link:hover,
    .toggle-expandable-list:hover {
      background: linear-gradient(180deg, rgba(255,255,255,.98), rgba(224,236,255,.96));
      border-color: rgba(37,99,235,.28);
      box-shadow: 0 8px 14px rgba(37,99,235,.08);
    }
    .call-link:disabled {
      cursor: not-allowed;
      opacity: .48;
      box-shadow: none;
    }
    .scroll-top-button {
      position: absolute;
      right: 12px;
      bottom: 12px;
      width: 32px;
      height: 32px;
      padding: 0;
      border-radius: 999px;
      border: 1px solid rgba(37,99,235,.22);
      background: linear-gradient(180deg, rgba(255,255,255,.98), rgba(232,241,255,.94));
      color: var(--accent-strong);
      font-size: 14px;
      line-height: 1;
      font-weight: 700;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 8px 18px rgba(15,23,42,.10);
      opacity: 0;
      pointer-events: none;
      transform: translateY(8px) scale(.96);
      transition:
        opacity .18s var(--ease),
        transform .18s var(--ease),
        background .18s var(--ease),
        border-color .18s var(--ease),
        box-shadow .18s var(--ease);
      z-index: 15;
    }
    .scroll-top-button.visible {
      opacity: 1;
      pointer-events: auto;
      transform: translateY(0) scale(1);
    }
    .scroll-top-button:hover {
      background: linear-gradient(180deg, rgba(255,255,255,.99), rgba(224,236,255,.96));
      border-color: rgba(37,99,235,.30);
      box-shadow: 0 10px 22px rgba(15,23,42,.12);
    }
    .scroll-top-button:focus-visible {
      outline: none;
      box-shadow:
        0 0 0 4px rgba(37,99,235,.12),
        0 10px 22px rgba(15,23,42,.14);
    }
    .stat-strip,
    .meta-grid {
      display: grid;
      gap: 8px;
      margin-top: 10px;
    }
    .stat-strip {
      grid-template-columns: repeat(4, minmax(0, 1fr));
    }
    .stat-card {
      padding: 10px 10px 11px;
      content-visibility: auto;
      contain: layout paint style;
      contain-intrinsic-size: 78px;
    }
    .stat-card .k,
    .meta-block .k,
    .call-event-block .k,
    .attachment-kind,
    .section-label {
      color: var(--muted);
      font-size: 10px;
      font-weight: 700;
      letter-spacing: .14em;
      text-transform: uppercase;
    }
    .stat-card .v {
      margin-top: 4px;
      color: var(--ink);
      font-size: 13px;
      line-height: 1.35;
      font-weight: 600;
    }
    .section-label {
      margin: 0;
    }
    .section-divider {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-top: 14px;
    }
    .section-divider::before,
    .section-divider::after {
      content: "";
      height: 1px;
      flex: 1;
      background: linear-gradient(90deg, transparent, rgba(88,110,147,.18), transparent);
    }
    .activity-report {
      display: grid;
      gap: 12px;
    }
    .activity-report-actions {
      display: flex;
      gap: 7px;
      flex-wrap: wrap;
      align-items: center;
      margin-top: 10px;
    }
    .activity-export-panel {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 160px)) auto;
      gap: 7px;
      align-items: end;
      width: 100%;
      margin-top: 8px;
      padding: 9px;
      border-radius: var(--radius-md);
      border: 1px solid rgba(88,110,147,.14);
      background: rgba(255,255,255,.72);
    }
    .activity-section {
      display: grid;
      gap: 9px;
      padding: 12px;
      border-radius: var(--radius-lg);
      border: 1px solid rgba(88,110,147,.16);
      background:
        linear-gradient(180deg, rgba(255,255,255,.90), rgba(245,248,255,.76));
      box-shadow:
        0 8px 18px rgba(15,23,42,.04),
        0 0 0 1px rgba(255,255,255,.56) inset;
    }
    .activity-section-head {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: baseline;
      flex-wrap: wrap;
    }
    .activity-section-title {
      font-size: 16px;
      line-height: 1.2;
      font-weight: 800;
      color: var(--ink);
    }
    .activity-section-subtitle {
      color: var(--muted);
      font-size: 12px;
      line-height: 1.35;
    }
    .activity-metric-grid,
    .activity-record-grid,
    .activity-target-grid {
      display: grid;
      gap: 8px;
    }
    .activity-metric-grid {
      grid-template-columns: repeat(4, minmax(0, 1fr));
    }
    .activity-record-grid {
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }
    .activity-target-grid {
      grid-template-columns: repeat(3, minmax(0, 1fr));
    }
    .activity-target-card {
      min-width: 0;
      display: grid;
      gap: 8px;
      padding: 10px;
      border-radius: var(--radius-md);
      border: 1px solid rgba(88,110,147,.15);
      background: rgba(255,255,255,.82);
      box-shadow:
        0 6px 12px rgba(15,23,42,.035),
        0 0 0 1px rgba(255,255,255,.50) inset;
    }
    .activity-target-link {
      cursor: pointer;
      transition:
        transform .18s var(--ease),
        border-color .18s var(--ease),
        box-shadow .18s var(--ease),
        background .18s var(--ease);
    }
    .activity-target-link:hover {
      transform: translateY(-1px);
      border-color: rgba(37,99,235,.28);
      background: rgba(255,255,255,.96);
      box-shadow:
        0 10px 18px rgba(37,99,235,.10),
        0 0 0 1px rgba(255,255,255,.56) inset;
    }
    .activity-target-link:focus-visible {
      outline: none;
      box-shadow:
        0 0 0 4px rgba(37,99,235,.13),
        0 10px 18px rgba(37,99,235,.10);
    }
    .activity-target-head {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 8px;
      min-width: 0;
    }
    .activity-target-title {
      color: var(--ink);
      font-size: 13px;
      line-height: 1.25;
      font-weight: 800;
      overflow-wrap: anywhere;
      word-break: break-word;
    }
    .activity-target-time {
      flex: 0 0 auto;
      max-width: 48%;
      color: var(--muted);
      font-size: 11px;
      line-height: 1.25;
      font-weight: 800;
      text-align: right;
      overflow-wrap: anywhere;
    }
    .activity-target-stats {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 6px;
    }
    .activity-target-stat {
      padding: 7px 8px;
      border-radius: 10px;
      border: 1px solid rgba(88,110,147,.12);
      background: rgba(245,248,255,.84);
      color: var(--muted-strong);
      font-size: 11px;
      line-height: 1.25;
    }
    .activity-target-stat strong {
      display: block;
      margin-top: 2px;
      color: var(--ink);
      font-size: 12px;
      line-height: 1.2;
    }
    .expandable-shell {
      display: grid;
      gap: 8px;
    }
    .expandable-list {
      position: relative;
      margin-top: 0;
      align-items: flex-start;
      min-width: 0;
    }
    .expandable-list.collapsed {
      max-height: 82px;
      overflow: hidden;
    }
    .expandable-list.expanded {
      max-height: none;
      overflow: visible;
    }
    .expandable-list.collapsed::after {
      content: "";
      position: absolute;
      left: 0;
      right: 0;
      bottom: 0;
      height: 22px;
      background: linear-gradient(180deg, rgba(255,255,255,0), rgba(246,249,255,.96));
      pointer-events: none;
    }
    .call-event-block .expandable-list.collapsed::after {
      background: linear-gradient(180deg, rgba(255,255,255,0), rgba(255,255,255,.98));
    }
    .participant-chip {
      font: inherit;
      line-height: 1.2;
    }
    .participant-chip-link {
      color: var(--accent-strong);
      background: rgba(232,241,255,.95);
      border-color: rgba(37,99,235,.18);
      cursor: pointer;
    }
    .participant-chip-link:hover {
      background: rgba(224,236,255,.98);
    }
    .participant-chip-static {
      color: var(--muted-strong);
      background: rgba(255,255,255,.86);
    }
    .messages,
    .search-results {
      display: grid;
      gap: 8px;
      margin-top: 10px;
    }
    .timeline-divider {
      display: flex;
      justify-content: center;
      margin: 6px 0 2px;
    }
    .timeline-divider span {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 24px;
      padding: 5px 9px;
      border-radius: 999px;
      border: 1px solid rgba(88,110,147,.16);
      background: rgba(255,255,255,.92);
      color: var(--muted-strong);
      font-size: 11px;
      font-weight: 700;
      letter-spacing: .06em;
      box-shadow: 0 8px 18px rgba(15,23,42,.05);
    }
    .search-group {
      padding: 11px;
      content-visibility: auto;
      contain: layout paint style;
      contain-intrinsic-size: 280px;
    }
    .search-group-header {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: center;
      flex-wrap: wrap;
    }
    .search-group-meta {
      margin-top: 4px;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.35;
    }
    .search-term {
      font-weight: 700;
      background: rgba(255,214,102,.76);
      border-radius: 5px;
      padding: 0 2px;
      box-decoration-break: clone;
      -webkit-box-decoration-break: clone;
    }
    .msg-row {
      display: grid;
      grid-template-columns: 40px minmax(0, 1fr);
      gap: 10px;
      align-items: end;
      min-width: 0;
    }
    .msg-row.self {
      grid-template-columns: minmax(0, 1fr) 40px;
    }
    .msg-row.self .msg-avatar {
      order: 2;
    }
    .msg-row.self .msg-stack {
      order: 1;
      align-items: end;
    }
    .msg-row.system {
      grid-template-columns: 1fr;
    }
    .msg-row.system .msg-avatar {
      display: none;
    }
    .msg-row.grouped-prev {
      margin-top: -4px;
    }
    .msg-row.grouped-prev .msg-avatar {
      opacity: 0;
      transform: scale(.86);
    }
    .msg-avatar {
      width: 36px;
      height: 36px;
      border-radius: 12px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-size: 12px;
      font-weight: 800;
      letter-spacing: .08em;
      color: #fff;
      background:
        linear-gradient(145deg, var(--msg-accent, var(--accent)), rgba(17,24,39,.82));
      box-shadow: 0 6px 12px rgba(15,23,42,.10);
      transition: opacity .18s var(--ease), transform .18s var(--ease);
    }
    .msg-stack {
      display: grid;
      gap: 5px;
      min-width: 0;
    }
    .msg {
      position: relative;
      min-width: 0;
      padding: 12px 13px;
      border-radius: 16px;
      border: 1px solid rgba(88,110,147,.14);
      background:
        linear-gradient(180deg, rgba(255,255,255,.96), rgba(245,248,255,.86));
      box-shadow:
        0 0 0 1px rgba(255,255,255,.48) inset;
      scroll-margin-top: 116px;
      transition:
        border-color .18s var(--ease),
        box-shadow .18s var(--ease),
        background .18s var(--ease);
    }
    .msg::before {
      content: "";
      position: absolute;
      inset: 0 auto 0 0;
      width: 4px;
      border-radius: 999px;
      background: var(--msg-accent, var(--accent));
      opacity: .8;
    }
    .msg-row.self .msg {
      background:
        linear-gradient(180deg, rgba(238,244,255,.98), rgba(228,238,255,.92));
      border-color: rgba(37,99,235,.18);
    }
    .msg-row.system .msg {
      background:
        linear-gradient(180deg, rgba(255,248,240,.94), rgba(255,255,255,.94));
      border-color: rgba(249,115,22,.20);
    }
    .msg.event {
      border-color: rgba(249,115,22,.18);
    }
    .msg.focused {
      border-color: rgba(37,99,235,.30);
      box-shadow:
        0 10px 18px rgba(37,99,235,.08),
        0 0 0 3px rgba(37,99,235,.10);
      background:
        linear-gradient(180deg, rgba(241,246,255,.98), rgba(255,255,255,.94));
    }
    .msg.search-match {
      border-color: rgba(37,99,235,.26);
      box-shadow:
        0 8px 14px rgba(37,99,235,.06),
        0 0 0 2px rgba(37,99,235,.09);
    }
    .msg .head {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
      min-width: 0;
      color: var(--muted);
      font-size: 11px;
      line-height: 1.35;
    }
    .msg .head.primary {
      margin-bottom: 6px;
    }
    .msg .head.secondary {
      margin-bottom: 10px;
      flex-wrap: wrap;
      justify-content: flex-start;
    }
    .msg .head.compact {
      margin-bottom: 8px;
      justify-content: space-between;
      flex-wrap: wrap;
    }
    .msg .sender {
      min-width: 0;
      color: var(--msg-accent, var(--accent));
      font-size: 13px;
      font-weight: 700;
      letter-spacing: -.01em;
      overflow-wrap: anywhere;
      word-break: break-word;
    }
    .msg-time {
      white-space: nowrap;
      color: var(--muted);
    }
    .msg-meta-pills {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      min-width: 0;
    }
    .msg-mini-chip {
      padding: 5px 8px;
      font-size: 10px;
      font-weight: 700;
      background: rgba(255,255,255,.92);
      color: var(--muted-strong);
    }
    .msg-mini-chip.muted {
      background: rgba(232,241,255,.90);
      color: var(--accent-strong);
    }
    .msg .body {
      white-space: pre-wrap;
      line-height: 1.5;
      word-break: break-word;
      font-size: 13px;
      color: var(--ink);
    }
    .msg .body.attachment-body {
      display: grid;
      gap: 8px;
      white-space: normal;
    }
    .msg .body-text {
      white-space: pre-wrap;
      line-height: 1.5;
      word-break: break-word;
      font-size: 13px;
    }
    .msg .body.reply-body {
      display: grid;
      gap: 10px;
      white-space: normal;
    }
    .reply-quote {
      display: grid;
      gap: 5px;
      padding: 10px 12px;
      border-left: 3px solid rgba(37,99,235,.34);
      border-radius: 10px;
      background:
        linear-gradient(180deg, rgba(236,243,255,.96), rgba(247,250,255,.92));
      color: var(--muted-strong);
    }
    .reply-quote-author {
      font-size: 11px;
      font-weight: 700;
      color: var(--accent-strong);
      overflow-wrap: anywhere;
      word-break: break-word;
    }
    .reply-quote-text {
      white-space: pre-wrap;
      line-height: 1.45;
      word-break: break-word;
      font-size: 12px;
    }
    .reply-response {
      white-space: pre-wrap;
      line-height: 1.5;
      word-break: break-word;
      font-size: 13px;
      color: var(--ink);
    }
    .reaction-bar {
      display: flex;
      justify-content: flex-end;
      margin-top: 10px;
    }
    .reaction-bubble {
      position: relative;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      min-height: 30px;
      padding: 6px 10px;
      border-radius: 999px;
      border: 1px solid rgba(88,110,147,.18);
      background:
        linear-gradient(180deg, rgba(255,255,255,.98), rgba(236,243,255,.92));
      box-shadow:
        0 6px 12px rgba(15,23,42,.08),
        0 0 0 1px rgba(255,255,255,.48) inset;
      color: var(--muted-strong);
      font-size: 12px;
      line-height: 1;
      cursor: default;
    }
    .reaction-count {
      font-weight: 800;
      color: var(--accent-strong);
    }
    .reaction-icons {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 15px;
    }
    .reaction-icon-more {
      font-size: 11px;
      font-weight: 700;
      color: var(--muted);
    }
    .reaction-tooltip {
      position: absolute;
      right: 0;
      bottom: calc(100% + 10px);
      min-width: 220px;
      max-width: min(320px, 72vw);
      display: grid;
      gap: 8px;
      padding: 10px;
      border-radius: 12px;
      border: 1px solid rgba(88,110,147,.20);
      background:
        linear-gradient(180deg, rgba(255,255,255,.99), rgba(241,246,255,.96));
      box-shadow:
        0 14px 26px rgba(15,23,42,.16),
        0 0 0 1px rgba(255,255,255,.58) inset;
      opacity: 0;
      pointer-events: none;
      transform: translateY(4px);
      transition:
        opacity .16s var(--ease),
        transform .16s var(--ease);
      z-index: 40;
    }
    .reaction-bubble:hover .reaction-tooltip,
    .reaction-bubble:focus-within .reaction-tooltip {
      opacity: 1;
      transform: translateY(0);
    }
    .reaction-tooltip-group {
      display: grid;
      gap: 5px;
    }
    .reaction-tooltip-heading {
      font-size: 11px;
      font-weight: 800;
      color: var(--accent-strong);
    }
    .reaction-tooltip-user {
      display: grid;
      grid-template-columns: auto 1fr;
      gap: 8px;
      align-items: start;
      font-size: 12px;
      color: var(--ink);
    }
    .reaction-tooltip-emoji {
      font-size: 14px;
      line-height: 1;
    }
    .reaction-tooltip-empty {
      font-size: 12px;
      color: var(--muted);
    }
    details.msg-collapsible {
      padding: 0;
      overflow: hidden;
    }
    details.msg-collapsible > summary {
      cursor: pointer;
      list-style-position: outside;
      padding: 12px 13px;
    }
    details.msg-collapsible > summary::-webkit-details-marker {
      margin-right: 8px;
    }
    details.msg-collapsible[open] > summary {
      padding-bottom: 10px;
    }
    details.msg-collapsible .msg-body-wrap {
      padding: 0 13px 13px;
      border-top: 1px solid rgba(88,110,147,.12);
    }
    .msg-summary-note {
      color: var(--muted);
      font-size: 12px;
      line-height: 1.35;
    }
    .attachment-stack {
      display: grid;
      gap: 8px;
    }
    .attachment-card {
      display: grid;
      gap: 7px;
      padding: 10px;
      border-radius: 12px;
      border: 1px solid rgba(88,110,147,.14);
      background:
        linear-gradient(180deg, rgba(255,255,255,.94), rgba(241,246,255,.84));
    }
    .attachment-meta {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 8px;
      flex-wrap: wrap;
    }
    .attachment-name {
      font-weight: 700;
      overflow-wrap: anywhere;
      word-break: break-word;
    }
    .attachment-actions {
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
    }
    .attachment-note {
      color: var(--muted);
      font-size: 12px;
      line-height: 1.35;
      margin-top: 2px;
    }
    .call-event {
      display: grid;
      gap: 10px;
      padding: 12px;
      border-radius: 14px;
      border: 1px solid var(--call-outline, rgba(88,110,147,.18));
      background: var(--call-bg, rgba(255,255,255,.94));
    }
    .call-event-header {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: center;
      flex-wrap: wrap;
    }
    .call-event-title {
      color: var(--call-title, var(--accent));
      font-weight: 700;
    }
    .call-event-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 7px;
    }
    .call-event-block {
      padding: 8px 10px;
      border-radius: 10px;
      border: 1px solid var(--call-outline, rgba(88,110,147,.14));
      background: var(--call-block-bg, rgba(255,255,255,.96));
    }
    .call-event-block.wide,
    .meta-block.wide {
      grid-column: 1 / -1;
    }
    .meta-grid {
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }
    .meta-block {
      padding: 10px;
      min-width: 0;
      font-size: 13px;
      line-height: 1.35;
      content-visibility: auto;
      contain: layout paint style;
      contain-intrinsic-size: 78px;
    }
    .meta-block .k {
      margin-bottom: 3px;
    }
    .mono {
      font-family: var(--mono);
      font-size: 11px;
      line-height: 1.45;
      word-break: break-word;
    }
    .toast {
      position: fixed;
      right: 24px;
      bottom: 24px;
      z-index: 20;
      display: inline-flex;
      align-items: center;
      gap: 10px;
      max-width: min(420px, calc(100vw - 48px));
      padding: 12px 14px;
      border-radius: 16px;
      border: 1px solid rgba(255,255,255,.12);
      background: rgba(15,23,42,.92);
      color: #fff;
      box-shadow: 0 18px 42px rgba(15,23,42,.28);
      opacity: 0;
      transform: translateY(10px);
      transition: opacity .18s var(--ease), transform .18s var(--ease);
      pointer-events: none;
    }
    .toast.show {
      opacity: 1;
      transform: translateY(0);
    }
    details.raw-event {
      border-top: 1px dashed rgba(88,110,147,.22);
      padding-top: 10px;
    }
    details.raw-event summary {
      cursor: pointer;
      color: var(--muted);
    }
    .empty {
      color: var(--muted);
      padding: 24px 8px;
      font-size: 14px;
      line-height: 1.6;
    }
    @keyframes shell-enter {
      from {
        opacity: 0;
        transform: translateY(6px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
    @media (max-width: 1320px) {
      .app {
        grid-template-columns: 340px minmax(0, 1fr);
      }
      .summary,
      .stat-strip {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
    }
    @media (max-width: 980px) {
      body {
        height: auto;
        overflow: auto;
      }
      .app {
        grid-template-columns: 1fr;
        height: auto;
      }
      .sidebar {
        min-height: auto;
      }
      .sidebar-list-wrap {
        overflow: visible;
      }
      .summary,
      .meta-grid,
      .call-event-grid,
      .stat-strip,
      .activity-metric-grid,
      .activity-record-grid,
      .activity-target-grid,
      .activity-export-panel {
        grid-template-columns: 1fr;
      }
      .main {
        overflow: visible;
      }
      .main-scroll {
        height: auto;
        overflow: visible;
      }
      .overview-panel {
        position: static;
      }
      .msg-row,
      .msg-row.self {
        grid-template-columns: 1fr;
      }
      .msg-avatar {
        display: none;
      }
    }
    @media (prefers-reduced-motion: reduce) {
      *,
      *::before,
      *::after {
        animation-duration: .01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: .01ms !important;
        scroll-behavior: auto !important;
      }
    }
  </style>
</head>
<body>
  <div class="app">
    <aside class="sidebar">
      <div class="sidebar-top">
        <section class="brand-card">
          <div class="brand-title">Michaelsoft Teams</div>
          <div class="brand-kicker">Offline Teams Archive</div>
          <div id="brandProfile" class="brand-profile">PROFILE: Recovered profile</div>
        </section>
        <div class="view-tabs">
          <button id="viewMessages" class="tab active" type="button">Messages</button>
          <button id="viewCalls" class="tab" type="button">Calls</button>
          <button id="viewActivity" class="tab" type="button">Activity</button>
        </div>
        <div id="messagesTools" class="toolbar">
          <input id="messageSearch" type="search" placeholder="Search Conversations and Messages...">
          <select id="categoryFilter">
            <option value="">All Message Types</option>
            <option value="chat_space">Chats</option>
            <option value="team_chat">Meetings</option>
            <option value="thread">Groups</option>
          </select>
          <div class="sidebar-range-controls">
            <label class="range-field">
              <span>From</span>
              <input id="messageDateFrom" type="date" value="">
            </label>
            <label class="range-field">
              <span>To</span>
              <input id="messageDateTo" type="date" value="">
            </label>
            <button id="clearMessageDateRange" type="button" class="call-link range-action">Clear Filters</button>
          </div>
        </div>
        <div id="callsTools" class="toolbar hidden">
          <input id="callSearch" type="search" placeholder="Search Calls and Details...">
          <select id="callGroupFilter">
            <option value="">All Call Types</option>
            <option value="call">Call</option>
            <option value="group">Group</option>
            <option value="meeting">Meeting</option>
            <option value="phone">Phone</option>
          </select>
          <select id="callDirectionFilter">
            <option value="">All Directions</option>
            <option value="inbound">Inbound</option>
            <option value="outbound">Outbound</option>
            <option value="missed">Missed</option>
            <option value="declined">Declined</option>
          </select>
          <div class="sidebar-range-controls">
            <label class="range-field">
              <span>From</span>
              <input id="callDateFrom" type="date" value="">
            </label>
            <label class="range-field">
              <span>To</span>
              <input id="callDateTo" type="date" value="">
            </label>
            <button id="clearCallDateRange" type="button" class="call-link range-action">Clear Filters</button>
          </div>
        </div>
        <div id="activityTools" class="toolbar hidden">
          <div class="activity-month-nav">
            <button id="activityPrevMonth" class="call-link" type="button" aria-label="Previous month">&#8249;</button>
            <input id="activityMonth" type="month" value="">
            <button id="activityNextMonth" class="call-link" type="button" aria-label="Next month">&#8250;</button>
          </div>
          <div class="activity-work-hours">
            <label class="range-field">
              <span>Work Start</span>
              <input id="activityWorkStart" type="time" value="08:00">
            </label>
            <label class="range-field">
              <span>Work End</span>
              <input id="activityWorkEnd" type="time" value="17:00">
            </label>
          </div>
          <div class="activity-workdays" aria-label="Work days">
            <label class="workday-toggle"><input class="activity-workday-input" type="checkbox" value="0"><span>Sun</span></label>
            <label class="workday-toggle"><input class="activity-workday-input" type="checkbox" value="1" checked><span>Mon</span></label>
            <label class="workday-toggle"><input class="activity-workday-input" type="checkbox" value="2" checked><span>Tue</span></label>
            <label class="workday-toggle"><input class="activity-workday-input" type="checkbox" value="3" checked><span>Wed</span></label>
            <label class="workday-toggle"><input class="activity-workday-input" type="checkbox" value="4" checked><span>Thu</span></label>
            <label class="workday-toggle"><input class="activity-workday-input" type="checkbox" value="5" checked><span>Fri</span></label>
            <label class="workday-toggle"><input class="activity-workday-input" type="checkbox" value="6"><span>Sat</span></label>
          </div>
          <button id="activityToday" type="button" class="call-link range-action">Today</button>
        </div>
        <div class="chip-row">
          <div id="sidebarCount" class="chip chip-strong"></div>
          <div class="chip hotkey-chip">/ Search</div>
          <div class="chip hotkey-chip">[ ] Navigate</div>
        </div>
        <div id="activeFilterBar" class="active-filter-bar"></div>
      </div>
      <div class="sidebar-divider"></div>
      <div class="sidebar-list-wrap">
        <div id="threadList" class="list"></div>
        <div id="callList" class="list hidden"></div>
        <div id="activityList" class="list hidden"></div>
      </div>
      <button id="sidebarScrollTop" class="scroll-top-button" type="button" aria-label="Scroll sidebar to top" aria-hidden="true">&#8593;</button>
    </aside>
    <main class="main">
      <div class="main-scroll">
        <div class="main-shell">
          <section class="overview-panel panel">
            <div class="overview-head">
              <div class="overview-quote">&ldquo;The Party told you to reject the evidence of your eyes and ears. It was their final, most essential command.&rdquo; - George Orwell</div>
              <div class="overview-side">
                <div id="overviewMode" class="overview-mode">Messages Workspace</div>
              </div>
            </div>
            <div class="summary">
              <div class="card days-card"><div class="label">Days</div><div class="value" id="sumDays"></div></div>
              <div class="card threads-card"><div class="label">Messages</div><div class="value" id="sumThreads"></div></div>
              <div class="card messages-card"><div class="label">Message Items</div><div class="value" id="sumMessages"></div></div>
              <div class="card calls-card"><div class="label">Calls</div><div class="value" id="sumCalls"></div></div>
              <div class="card attachments-card"><div class="label">Attachments</div><div class="value" id="sumAttachments"></div></div>
              <div class="card reactions-card"><div class="label">Reactions</div><div class="value" id="sumReactions"></div></div>
            </div>
          </section>
          <section id="contentPanel" class="panel content-panel"></section>
        </div>
      </div>
      <button id="mainScrollTop" class="scroll-top-button" type="button" aria-label="Scroll main content to top" aria-hidden="true">&#8593;</button>
    </main>
  </div>
  <div id="toast" class="toast"></div>
  <script>
    const DATA = __DATA__;

    const state = {
      view: "messages",
      messageSearch: "",
      messageDateFrom: "",
      messageDateTo: "",
      callSearch: "",
      category: "",
      callGroup: "",
      callDirection: "",
      callDateFrom: "",
      callDateTo: "",
      activityDate: "",
      activityMonth: "",
      activityWorkStart: "08:00",
      activityWorkEnd: "17:00",
      activityWorkDays: "1,2,3,4,5",
      activityExportFrom: "",
      activityExportTo: "",
      activityExportOpen: false,
      messageViewFilter: "all",
      threadDateFrom: "",
      threadDateTo: "",
      expandHiddenData: false,
      threadId: null,
      callKey: null,
      focusMessageId: null,
      focusCallKey: null,
      focusTimestamp: null,
      focusSearchQuery: "",
    };

    const appShell = document.querySelector(".app");
    const contentPanel = document.getElementById("contentPanel");
    const mainPanel = document.querySelector(".main");
    const mainScrollWrap = document.querySelector(".main-scroll");
    const sidebarListWrap = document.querySelector(".sidebar-list-wrap");
    const threadList = document.getElementById("threadList");
    const callList = document.getElementById("callList");
    const activityList = document.getElementById("activityList");
    const messagesTools = document.getElementById("messagesTools");
    const callsTools = document.getElementById("callsTools");
    const activityTools = document.getElementById("activityTools");
    const activeFilterBar = document.getElementById("activeFilterBar");
    const sidebarCount = document.getElementById("sidebarCount");
    const brandProfile = document.getElementById("brandProfile");
    const overviewMode = document.getElementById("overviewMode");
    const viewMessages = document.getElementById("viewMessages");
    const viewCalls = document.getElementById("viewCalls");
    const viewActivity = document.getElementById("viewActivity");
    const messageSearch = document.getElementById("messageSearch");
    const categoryFilter = document.getElementById("categoryFilter");
    const messageDateFrom = document.getElementById("messageDateFrom");
    const messageDateTo = document.getElementById("messageDateTo");
    const clearMessageDateRange = document.getElementById("clearMessageDateRange");
    const callSearch = document.getElementById("callSearch");
    const callGroupFilter = document.getElementById("callGroupFilter");
    const callDirectionFilter = document.getElementById("callDirectionFilter");
    const callDateFrom = document.getElementById("callDateFrom");
    const callDateTo = document.getElementById("callDateTo");
    const clearCallDateRange = document.getElementById("clearCallDateRange");
    const activityMonth = document.getElementById("activityMonth");
    const activityPrevMonth = document.getElementById("activityPrevMonth");
    const activityNextMonth = document.getElementById("activityNextMonth");
    const activityWorkStart = document.getElementById("activityWorkStart");
    const activityWorkEnd = document.getElementById("activityWorkEnd");
    const activityWorkdayInputs = [...document.querySelectorAll(".activity-workday-input")];
    const activityToday = document.getElementById("activityToday");
    const sidebarScrollTopButton = document.getElementById("sidebarScrollTop");
    const mainScrollTopButton = document.getElementById("mainScrollTop");
    const toast = document.getElementById("toast");
    const MESSAGE_ATTACHMENT_CACHE = new WeakMap();
    const MESSAGE_REPLY_QUOTE_CACHE = new WeakMap();
    const MESSAGE_REACTION_CACHE = new WeakMap();
    const NUMBER_FORMATTER = new Intl.NumberFormat();
    const UI_STATE_STORAGE_KEY = "michaelsoft_teams_ui_state_v2";

    const PERSON_NAME_BY_GUID = new Map(
      Object.entries(DATA.guid_directory || {})
        .map(([guid, name]) => [normalizeGuid(guid), normalizeTextValue(name)])
        .filter(([guid, name]) => guid && name)
    );
    const PERSON_GUID_BY_NAME = new Map(
      [...PERSON_NAME_BY_GUID.entries()]
        .map(([guid, name]) => [normalizeName(name), guid])
        .filter(([name, guid]) => name && guid)
    );
    const DIRECT_CHAT_BY_GUID = new Map();
    const DIRECT_CHAT_BY_NAME = new Map();
    const CALLS_BY_ID = new Map();
    const CALLS_BY_SHARED = new Map();
    const CALLS_BY_KEY = new Map();
    const THREAD_BY_ID = new Map();
    const PREFERRED_THREADS_BY_CALL_KEY = new Map();
    const CALL_JUMP_TARGETS_BY_CALL_KEY = new Map();
    const PHONE_CALL_BY_KEY = new Map();
    const CALL_EXTERNAL_PARTICIPANT_COUNT_BY_KEY = new Map();
    const CALL_GROUP_KEY_BY_KEY = new Map();
    const CALLS_BY_THREAD_ID = new Map();
    const CALLS_BY_GUID_PAIR = new Map();
    const CALLS_BY_NAME_PAIR = new Map();
    const SYNTHETIC_CALLS_CACHE = new Map();
    const THREAD_TIMELINE_CACHE = new Map();
    const SORTED_THREAD_TIMELINE_CACHE = new Map();
    const LINKED_CALLS_BY_THREAD_CACHE = new Map();
    const THREAD_SEARCH_TEXT_CACHE = new Map();
    const THREAD_SIDEBAR_SUMMARY_CACHE = new Map();
    const CALL_LABEL_CACHE = new Map();
    const CALL_SEARCH_TEXT_CACHE = new Map();
    const CALL_PRIMARY_TIME_VALUE_CACHE = new Map();
    const CALL_KEY_CACHE = new WeakMap();
    const LINKED_CALL_BY_MESSAGE_CACHE = new WeakMap();
    const MESSAGE_HIDDEN_META_CACHE = new WeakMap();
    const MESSAGE_SEARCH_TEXT_CACHE = new WeakMap();
    const SEARCH_GROUPS_CACHE = new Map();
    const ACTIVITY_COUNTS_BY_DAY_CACHE = { signature: "", value: null };
    const ACTIVITY_DAY_METRICS_CACHE = new Map();
    for (const call of DATA.calls || []) {
      rememberPerson(call.originator_id, call.originator_display_name);
      rememberPerson(call.target_id, call.target_display_name);
      for (const session of call.participant_sessions || []) {
        rememberPerson(session.id, session.display_name);
      }
      const participantIds = (call.participant_ids || []).map(normalizeGuid).filter(Boolean);
      const participantNames = (call.participant_display_names || []).map(value => normalizeTextValue(value)).filter(Boolean);
      if (participantIds.length === participantNames.length) {
        for (let index = 0; index < participantIds.length; index += 1) {
          rememberPerson(participantIds[index], participantNames[index]);
        }
      }
      if (call.call_id) CALLS_BY_ID.set(String(call.call_id).toLowerCase(), call);
      if (call.shared_correlation_id) CALLS_BY_SHARED.set(String(call.shared_correlation_id).toLowerCase(), call);
      CALLS_BY_KEY.set(callKey(call), call);
      if (call.conversation_id && call.conversation_id !== "48:calllogs") {
        addToMapList(CALLS_BY_THREAD_ID, String(call.conversation_id), call);
      }
      const guidPair = participantGuidPairKey(callParticipantIds(call));
      if (guidPair) addToMapList(CALLS_BY_GUID_PAIR, guidPair, call);
      const namePair = participantNamePairKey(callParticipantNames(call));
      if (namePair) addToMapList(CALLS_BY_NAME_PAIR, namePair, call);
    }

    document.getElementById("sumDays").textContent = NUMBER_FORMATTER.format(datasetDayCount());
    document.getElementById("sumThreads").textContent = NUMBER_FORMATTER.format(DATA.summary.threads_total || 0);
    document.getElementById("sumMessages").textContent = NUMBER_FORMATTER.format(DATA.summary.messages_total || 0);
    document.getElementById("sumCalls").textContent = NUMBER_FORMATTER.format(DATA.summary.calls_total || 0);
    document.getElementById("sumAttachments").textContent = NUMBER_FORMATTER.format(DATA.summary.attachments_total || 0);
    document.getElementById("sumReactions").textContent = NUMBER_FORMATTER.format(DATA.summary.reactions_total || 0);

    function fmt(value) {
      if (!value) return "[no_time]";
      const date = new Date(value);
      if (Number.isNaN(date.getTime())) return value;
      return date.toLocaleString();
    }

    function timeValue(value) {
      if (!value) return Number.NEGATIVE_INFINITY;
      const parsed = Date.parse(value);
      if (Number.isNaN(parsed)) return Number.NEGATIVE_INFINITY;
      return parsed;
    }

    function escapeHtml(value) {
      return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
    }

    function normalizeTextValue(value) {
      return String(value ?? "")
        .replace(/\\s{2,}/g, " ")
        .trim();
    }

    function cleanCallParticipantName(value) {
      let cleaned = normalizeTextValue(value || "").trim();
      if (!cleaned) return "";
      cleaned = cleaned.replace(/\\s+Conference Virtual Assistant$/i, "").trim();
      cleaned = cleaned.replace(
        /^(.*?)(?:\\s+\\d+\\s+(?:28:[0-9a-fA-F-]{36}|8:orgid:[0-9a-fA-F-]{36}|4:\\+?[0-9(). -]{7,})(?:\\s+\\+?1?[0-9(). -]{7,})?.*)$/i,
        "$1"
      ).trim();
      return normalizeTextValue(cleaned);
    }

    function normalizePhoneNumber(value) {
      let text = String(value || "").trim();
      if (!text) return "";
      text = text.replace(/^tel:/i, "");
      if (/^4:/i.test(text)) {
        text = text.replace(/^4:/i, "");
      }
      if (/[A-Za-z]/.test(text)) return "";
      if (!/^[+()0-9 .-]{7,}$/.test(text)) return "";
      text = text.replace(/[() .-]+/g, "");
      const hasPlus = text.startsWith("+");
      const digits = text.replace(/^\\+/, "");
      if (!digits || !/^\\d+$/.test(digits) || digits.length < 7) return "";
      return hasPlus ? `+${digits}` : digits;
    }

    function formatPhoneNumber(value) {
      const normalized = normalizePhoneNumber(value);
      if (!normalized) return "";
      const digits = normalized.replace(/^\\+/, "");
      if (digits.length === 10) {
        return `(${digits.slice(0, 3)}) ${digits.slice(3, 6)}-${digits.slice(6)}`;
      }
      if (digits.length === 11 && digits.startsWith("1")) {
        const local = digits.slice(1);
        return `(${local.slice(0, 3)}) ${local.slice(3, 6)}-${local.slice(6)}`;
      }
      return normalized.startsWith("+") ? normalized : digits;
    }

    function isGenericPhoneLabel(value) {
      return /^(wireless caller|state[_ ]of[_ ]alaska|unknown caller|anonymous|private caller|external caller)$/i.test(normalizeTextValue(value || ""));
    }

    function callPhoneNumber(call, side) {
      return formatPhoneNumber(call[`${side}_phone_number`] || call[`${side}_endpoint`]);
    }

    function callSideLabel(call, side) {
      const rawName = cleanCallParticipantName(call[`${side}_display_name`] || "");
      const phone = callPhoneNumber(call, side);
      if (phone) {
        if (!rawName || isGenericPhoneLabel(rawName)) return phone;
        if (normalizePhoneNumber(rawName) === normalizePhoneNumber(phone)) return phone;
        return rawName;
      }
      if (normalizePhoneNumber(rawName)) return formatPhoneNumber(rawName);
      return rawName || phone || normalizeTextValue(call[`${side}_id`] || call[`${side}_endpoint`] || "");
    }

    function callPanelSideLabel(call, side) {
      const label = callSideLabel(call, side);
      return isGenericPhoneLabel(label) ? "" : label;
    }

    function addToMapList(map, key, value) {
      if (!key) return;
      if (!map.has(key)) map.set(key, []);
      map.get(key).push(value);
    }

    function dedupe(values) {
      return [...new Set((values || []).filter(Boolean))];
    }

    function normalizeGuid(value) {
      const text = String(value || "").trim();
      if (!text) return "";
      const match = text.match(/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/);
      return match ? match[0].toLowerCase() : text.toLowerCase();
    }

    function normalizeName(value) {
      return normalizeTextValue(value).toLowerCase();
    }

    function rememberPerson(guid, displayName) {
      const normalizedGuid = normalizeGuid(guid);
      const cleanedName = cleanCallParticipantName(displayName);
      if (normalizedGuid && cleanedName && !PERSON_NAME_BY_GUID.has(normalizedGuid)) {
        PERSON_NAME_BY_GUID.set(normalizedGuid, cleanedName);
      }
      if (normalizedGuid && cleanedName && !PERSON_GUID_BY_NAME.has(normalizeName(cleanedName))) {
        PERSON_GUID_BY_NAME.set(normalizeName(cleanedName), normalizedGuid);
      }
    }

    function personNameForGuid(guid) {
      return normalizeTextValue(PERSON_NAME_BY_GUID.get(normalizeGuid(guid)) || "");
    }

    function participantBaseName(value) {
      const cleaned = cleanCallParticipantName(value || "").trim();
      if (!cleaned) return "";
      const bracketMatch = cleaned.match(/^(.*?)\\s*\\[([^\\]]+)\\]\\s*$/);
      if (bracketMatch && normalizePhoneNumber(bracketMatch[2])) {
        return cleanCallParticipantName(bracketMatch[1] || "");
      }
      return cleaned;
    }

    function personGuidForName(name) {
      return PERSON_GUID_BY_NAME.get(normalizeName(participantBaseName(name))) || "";
    }

    function looksLikeGuid(value) {
      return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(normalizeTextValue(value || ""));
    }

    const CURRENT_USER_ID = normalizeGuid(DATA.profile && DATA.profile.oid);
    const CURRENT_USER_NAME = normalizeName(DATA.profile && DATA.profile.display_name);
    const PROFILE_DISPLAY_NAME = normalizeTextValue((DATA.profile && DATA.profile.display_name) || "") || "Recovered profile";
    const MESSAGE_COLOR_SELF = "#355CDE";
    const MESSAGE_COLOR_PALETTE = [
      "#0F766E",
      "#C05621",
      "#B7791F",
      "#B83280",
      "#2F855A",
      "#9C4221",
      "#BE123C",
      "#4D7C0F",
    ];
    const CALL_VISUALS = {
      "#355CDE": { bg: "#88B5FF", outline: "#18357A", block: "#EAF3FF", title: "#16306F" },
      "#0F766E": { bg: "#72F2E7", outline: "#104641", block: "#EDFFFD", title: "#0E4C46" },
      "#C05621": { bg: "#FFB887", outline: "#6F2C08", block: "#FFF1E8", title: "#6F2C08" },
      "#B7791F": { bg: "#FFE27B", outline: "#6C4608", block: "#FFF9DE", title: "#654107" },
      "#B83280": { bg: "#FF9DDB", outline: "#6F1A4A", block: "#FFF2FA", title: "#6C1948" },
      "#2F855A": { bg: "#96F5C1", outline: "#18482F", block: "#EEFFF5", title: "#18482F" },
      "#9C4221": { bg: "#FFAA84", outline: "#5A1F0B", block: "#FFF0E9", title: "#5A1F0B" },
      "#BE123C": { bg: "#FF96AE", outline: "#6C1026", block: "#FFF1F5", title: "#6C1026" },
      "#4D7C0F": { bg: "#C6FA72", outline: "#2E4A09", block: "#F7FFE9", title: "#2E4A09" },
      "#8A6F5A": { bg: "#E9D7C6", outline: "#4D3B2C", block: "#FBF5F0", title: "#4D3B2C" },
    };

    function threadAllParticipantNames(thread) {
      const names = dedupe([
        ...(thread.participants || []).map(value => cleanCallParticipantName(value)),
        ...(thread.participant_ids || []).map(guid => personNameForGuid(guid)),
      ].filter(Boolean));
      return names;
    }

    function threadExternalParticipantNames(thread) {
      return threadAllParticipantNames(thread)
        .filter(name => normalizeName(name) !== CURRENT_USER_NAME);
    }

    function isPlaceholderThreadLabel(label) {
      const normalized = normalizeName(label || "");
      return !normalized || normalized === "just me" || normalized === CURRENT_USER_NAME;
    }

    function threadDisplayLabel(thread) {
      const fallback = normalizeTextValue(thread.label || thread.id || "Conversation");
      if (thread.category === "chat_space" && isPlaceholderThreadLabel(fallback)) {
        const others = threadExternalParticipantNames(thread);
        if (others.length === 1) return others[0];
        if (others.length > 1) return summarizeNames(others, 2);
      }
      return fallback;
    }

    function rememberDirectChatThread(thread) {
      if (!thread || thread.category !== "chat_space") return;
      if (!Array.isArray(thread.messages) || thread.messages.length === 0) return;
      const ids = dedupe((thread.participant_ids || []).map(normalizeGuid).filter(Boolean));
      const names = dedupe((thread.participants || []).map(value => normalizeTextValue(value)).filter(Boolean));
      const hasCurrentId = Boolean(CURRENT_USER_ID && ids.includes(CURRENT_USER_ID));
      const hasCurrentName = Boolean(CURRENT_USER_NAME && names.some(name => normalizeName(name) === CURRENT_USER_NAME));
      if (!hasCurrentId && !hasCurrentName) return;

      if (ids.length === 2 && names.length === 2) {
        const otherId = ids.find(guid => guid !== CURRENT_USER_ID) || "";
        const otherName = names.find(name => normalizeName(name) !== CURRENT_USER_NAME) || "";
        rememberPerson(otherId, otherName);
      }

      for (const guid of ids) {
        if (guid && guid !== CURRENT_USER_ID && !DIRECT_CHAT_BY_GUID.has(guid)) {
          DIRECT_CHAT_BY_GUID.set(guid, thread);
        }
      }
      for (const name of names) {
        const normalizedName = normalizeName(name);
        if (normalizedName && normalizedName !== CURRENT_USER_NAME && !DIRECT_CHAT_BY_NAME.has(normalizedName)) {
          DIRECT_CHAT_BY_NAME.set(normalizedName, thread);
        }
      }
    }

    for (const thread of DATA.threads || []) {
      if (thread && thread.id) {
        THREAD_BY_ID.set(thread.id, thread);
      }
      for (const message of thread.messages || []) {
        message.__thread_id = thread && thread.id ? thread.id : "";
        rememberPerson(message.sender_id, message.sender_display_name);
      }
      rememberDirectChatThread(thread);
    }

    function participantGuidPairKey(values) {
      const items = dedupe((values || []).map(normalizeGuid).filter(Boolean)).sort();
      return items.length === 2 ? items.join("|") : "";
    }

    function participantNamePairKey(values) {
      const items = dedupe((values || []).map(normalizeName).filter(Boolean)).sort();
      return items.length === 2 ? items.join("|") : "";
    }

    function summarizeNames(values, maxVisible = 3) {
      const items = dedupe((values || []).map(value => cleanCallParticipantName(value)).filter(Boolean));
      if (!items.length) return "";
      if (items.length <= maxVisible) return items.join(" / ");
      return `${items.slice(0, maxVisible).join(" / ")} + ${items.length - maxVisible} more`;
    }

    function actualGuid(value) {
      const match = String(value || "").match(/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/);
      return match ? match[0].toLowerCase() : "";
    }

    function participantNameIdentity(name) {
      const cleaned = participantBaseName(name);
      if (!cleaned) return "";
      const phone = normalizePhoneNumber(cleaned);
      if (phone) return `phone:${phone}`;
      const normalized = normalizeName(cleaned);
      return normalized ? `name:${normalized}` : "";
    }

    function isPhoneEnrichedLabel(name) {
      const cleaned = normalizeTextValue(name || "").trim();
      const bracketMatch = cleaned.match(/^(.*?)\\s*\\[([^\\]]+)\\]\\s*$/);
      return Boolean(bracketMatch && normalizePhoneNumber(bracketMatch[2]));
    }

    function chooseParticipantLabel(existingName, candidateName) {
      const existing = cleanCallParticipantName(existingName || "");
      const candidate = cleanCallParticipantName(candidateName || "");
      if (!existing) return candidate;
      if (!candidate) return existing;
      const existingEnriched = isPhoneEnrichedLabel(existing) || Boolean(normalizePhoneNumber(existing));
      const candidateEnriched = isPhoneEnrichedLabel(candidate) || Boolean(normalizePhoneNumber(candidate));
      if (candidateEnriched && !existingEnriched) return candidate;
      if (candidate.length > existing.length) return candidate;
      return existing;
    }

    function callParticipantDisplayNames(call) {
      return normalizeParticipantList(callParticipantEntries(call))
        .filter(entry => !entry.hidden)
        .map(entry => cleanCallParticipantName(entry.label || entry.name || ""))
        .filter(Boolean);
    }

    function callParticipantIds(call) {
      return dedupe([
        ...(call.participant_ids || []),
        call.originator_id,
        call.target_id,
      ].map(normalizeGuid).filter(Boolean));
    }

    function callParticipantNames(call) {
      return callParticipantDisplayNames(call).map(normalizeName).filter(Boolean);
    }

    function callParticipantEntries(call) {
      const combined = [];
      const mergedByIdentity = new Map();

      function mergeEntry(entry) {
        const name = normalizeTextValue(entry && entry.name || "");
        const cleanName = cleanCallParticipantName(name);
        if (!cleanName || isGenericPhoneLabel(cleanName)) return;
        const guid = actualGuid(entry && entry.id) || personGuidForName(cleanName);
        const identityKey = guid || participantNameIdentity(cleanName);
        if (!identityKey) return;
        const existing = mergedByIdentity.get(identityKey);
        mergedByIdentity.set(identityKey, {
          id: guid || (existing && existing.id) || "",
          name: chooseParticipantLabel(existing && existing.name, cleanName),
        });
      }

      const originatorLabel = callPanelSideLabel(call, "originator");
      if (originatorLabel) {
        mergeEntry({
          id: call.originator_id || call.originator_endpoint || "",
          name: originatorLabel,
        });
      }
      const targetLabel = callPanelSideLabel(call, "target");
      if (targetLabel) {
        mergeEntry({
          id: call.target_id || call.target_endpoint || "",
          name: targetLabel,
        });
      }

      for (const session of call.participant_sessions || []) {
        mergeEntry({
          id: session.id || "",
          name: session.display_name || "",
        });
      }

      const baseEntries = buildParticipantEntries(
        call.participant_ids || [],
        call.participant_display_names || []
      );
      for (const entry of baseEntries) {
        mergeEntry(entry);
      }
      for (const entry of mergedByIdentity.values()) {
        combined.push(entry);
      }
      return combined;
    }

    function threadCurrentMemberIds(thread) {
      return dedupe(((thread && thread.current_member_ids) || []).map(normalizeGuid).filter(Boolean));
    }

    function threadCurrentMemberSet(thread) {
      return new Set(threadCurrentMemberIds(thread));
    }

    function threadParticipantCount(thread) {
      const currentIds = threadCurrentMemberIds(thread);
      if (currentIds.length) return currentIds.length;
      return normalizeParticipantList(threadParticipantEntries(thread)).filter(entry => !entry.hidden).length;
    }

    function buildThreadScopedParticipantEntries(thread, ids = [], names = [], options = {}) {
      const entries = [];
      const currentIds = threadCurrentMemberSet(thread);
      const hasCurrentRoster = currentIds.size > 0;
      const normalizedIds = (ids || []).map(normalizeGuid);
      const cleanedNames = (names || []).map(value => cleanCallParticipantName(value));
      const maxLength = Math.max(normalizedIds.length, cleanedNames.length);

      for (let index = 0; index < maxLength; index += 1) {
        const guid = normalizedIds[index] || "";
        const explicitName = cleanedNames[index] || "";
        const resolvedName = explicitName || (guid ? personNameForGuid(guid) : "");
        const hiddenBecauseRemoved = Boolean(options.forceHidden) || (hasCurrentRoster && guid ? !currentIds.has(guid) : false);
        const hiddenBecauseUnresolved = !resolvedName;
        entries.push({
          id: guid,
          name: resolvedName,
          label: resolvedName || normalizeTextValue(guid || explicitName || ""),
          hidden: hiddenBecauseRemoved || hiddenBecauseUnresolved,
        });
      }

      return entries.filter(entry => entry.id || entry.name || entry.label);
    }

    function threadParticipantEntries(thread) {
      const entries = [];
      const currentIds = threadCurrentMemberSet(thread);
      const hasCurrentRoster = currentIds.size > 0;
      const resolvedIds = dedupe((thread.participant_ids || []).map(normalizeGuid).filter(Boolean));
      for (const guid of resolvedIds) {
        entries.push({
          id: guid,
          name: personNameForGuid(guid),
          hidden: hasCurrentRoster ? !currentIds.has(guid) : false,
        });
      }
      for (const name of thread.participants || []) {
        const cleanedName = cleanCallParticipantName(name);
        if (!cleanedName) continue;
        const guid = personGuidForName(cleanedName);
        entries.push({
          id: guid,
          name: cleanedName,
          hidden: hasCurrentRoster && guid ? !currentIds.has(guid) : false,
        });
      }
      return entries;
    }

    function callTimelineTimestamp(call) {
      return call.end_time || call.start_time || call.connect_time || "";
    }

    function callDurationSeconds(call) {
      const start = Date.parse(call.start_time || "");
      const end = Date.parse(call.end_time || "");
      if (Number.isNaN(start) || Number.isNaN(end) || end < start) return null;
      return Math.round((end - start) / 1000);
    }

    function isMeetingThreadId(value) {
      return /^e?19:meeting_/i.test(String(value || "").trim());
    }

    function hasRealMeetingWindow(call) {
      return [call.meeting_start_time, call.meeting_end_time]
        .some(value => value && !String(value).startsWith("0001-01-01"));
    }

    function isMeetingCall(call) {
      if (isMeetingThreadId(call.conversation_id) || isMeetingThreadId(call.group_chat_thread_id)) {
        return true;
      }
      if (hasRealMeetingWindow(call)) {
        return true;
      }
      return Boolean(String(call.meeting_series_kind || "").trim());
    }

    function normalizedCallType(call) {
      return String(call.call_type || "").trim().toLowerCase();
    }

    function normalizedCallQuality(call) {
      return String(call.quality || "").trim().toLowerCase();
    }

    function displayCallTypeLabel(call) {
      const value = normalizedCallType(call);
      const labels = {
        meeting: "Meeting",
        group: "Group",
        twoparty: "Two Party",
        multiparty: "Multi Party",
      };
      if (labels[value]) return labels[value];
      return value ? prettyCallEventName(value) : "";
    }

    function displayCallQualityLabel(call) {
      const value = normalizedCallQuality(call);
      const labels = {
        thread_event_inferred: "Inferred Call",
        calllog_enriched: "Call Log",
        structured: "Structured Call",
      };
      if (labels[value]) return labels[value];
      return value ? prettyCallEventName(value) : "";
    }

    function looksLikePhoneEndpoint(name) {
      const cleaned = normalizeTextValue(name || "").trim();
      if (!cleaned) return false;
      if (normalizePhoneNumber(cleaned)) return true;
      if (isGenericPhoneLabel(cleaned)) return true;
      if (cleaned.includes(",")) return false;
      return cleaned.length >= 5 && cleaned === cleaned.toUpperCase();
    }

    function isPhoneCall(call) {
      const key = callKey(call);
      if (PHONE_CALL_BY_KEY.has(key)) return PHONE_CALL_BY_KEY.get(key);
      let value = false;
      if (!isMeetingCall(call)) {
        const explicitPhoneEndpoint = Boolean(callPhoneNumber(call, "originator") || callPhoneNumber(call, "target"));
        const participants = dedupe([
          ...(call.participant_display_names || []),
          call.originator_display_name,
          call.target_display_name,
        ].map(value => normalizeTextValue(value)).filter(Boolean));
        const hasPhoneEndpoint = explicitPhoneEndpoint || participants.some(looksLikePhoneEndpoint);
        const inCallLogBucket = String(call.conversation_id || "").toLowerCase() === "48:calllogs";
        if (explicitPhoneEndpoint) {
          value = Boolean(inCallLogBucket);
        } else {
          const hasLinkedConversation = preferredThreadsForCall(call).length > 0;
          value = Boolean(hasPhoneEndpoint && inCallLogBucket && !hasLinkedConversation);
        }
      }
      PHONE_CALL_BY_KEY.set(key, value);
      return value;
    }

    function isCurrentUserParticipantEntry(entry) {
      const guid = normalizeGuid(entry && entry.id);
      const name = normalizeName(entry && (entry.name || entry.label || ""));
      return Boolean((guid && CURRENT_USER_ID && guid === CURRENT_USER_ID) || (name && CURRENT_USER_NAME && name === CURRENT_USER_NAME));
    }

    function callExternalParticipantCount(call) {
      const key = callKey(call);
      if (CALL_EXTERNAL_PARTICIPANT_COUNT_BY_KEY.has(key)) return CALL_EXTERNAL_PARTICIPANT_COUNT_BY_KEY.get(key);
      const entries = normalizeParticipantList(callParticipantEntries(call))
        .filter(entry => !entry.hidden)
        .filter(entry => !isCurrentUserParticipantEntry(entry));
      const count = entries.length;
      CALL_EXTERNAL_PARTICIPANT_COUNT_BY_KEY.set(key, count);
      return count;
    }

    function hasLinkedGroupThread(call) {
      return preferredThreadsForCall(call).some(thread => thread.category === "thread" && (thread.participants || []).length > 2);
    }

    function isGroupCall(call) {
      if (isMeetingCall(call) || isPhoneCall(call)) return false;
      if (call.group_chat_thread_id) return true;
      if (callExternalParticipantCount(call) > 1) return true;
      return hasLinkedGroupThread(call);
    }

    function callGroupKey(call) {
      const key = callKey(call);
      if (CALL_GROUP_KEY_BY_KEY.has(key)) return CALL_GROUP_KEY_BY_KEY.get(key);
      let value = "call";
      if (isPhoneCall(call)) value = "phone";
      else if (isMeetingCall(call)) value = "meeting";
      else if (isGroupCall(call)) value = "group";
      CALL_GROUP_KEY_BY_KEY.set(key, value);
      return value;
    }

    function displayCallGroupLabel(call) {
      const labels = {
        phone: "Phone",
        meeting: "Meeting",
        group: "Group",
        call: "Call",
      };
      return labels[callGroupKey(call)] || "Call";
    }

    function meetingParticipation(call) {
      const value = String(call.user_participation || "").toLowerCase();
      return value === "joined" || value === "missed" ? value : "";
    }

    function meetingCallTitle(call) {
      const subject = normalizeTextValue(call.meeting_subject || "").trim() || "Meeting";
      const when = fmt(call.start_time || call.meeting_start_time || call.connect_time);
      return when && when !== "[no_time]" ? `${subject} [${when}]` : subject;
    }

    function displayCallDirection(call) {
      if (isMeetingCall(call)) return "meeting";
      return String(call.direction || "").toLowerCase();
    }

    function displayCallDirectionLabel(call) {
      const direction = displayCallDirection(call);
      const labels = {
        incoming: "Inbound",
        outgoing: "Outbound",
        meeting: "Meeting",
      };
      return labels[direction] || (direction ? `${direction[0].toUpperCase()}${direction.slice(1)}` : "");
    }

    function shouldMarkMissed(call) {
      const seconds = callDurationSeconds(call);
      return (
        displayCallDirection(call) === "outgoing" &&
        seconds !== null &&
        seconds < 45
      );
    }

    function displayCallState(call) {
      if (isMeetingCall(call)) return meetingParticipation(call) || "meeting";
      if (shouldMarkMissed(call)) return "missed";
      const raw = String(call.call_state || "").toLowerCase();
      if (raw === "rejected" || raw === "declined" || raw === "cancelled") return "declined";
      return raw;
    }

    function displayCallStateLabel(call) {
      const state = displayCallState(call);
      const labels = {
        started: "Started",
        ended: "Ended",
        joined: "Joined",
        meeting: "Meeting",
        missed: "Missed",
        accepted: "Accepted",
        declined: "Declined",
        rejected: "Rejected",
        cancelled: "Cancelled",
      };
      if (labels[state]) return labels[state];
      return state ? prettyCallEventName(state) : "";
    }

    function displayCallStatus(call) {
      if (isMeetingCall(call)) {
        const participation = displayCallStateLabel(call);
        return participation && participation !== "Meeting" ? `Meeting | ${participation}` : "Meeting";
      }
      const direction = displayCallDirectionLabel(call);
      const state = displayCallStateLabel(call);
      if (direction && state) return `${direction} | ${state}`;
      return direction || state || "";
    }

    function includeRawCallTypeChip(call) {
      const rawType = normalizedCallType(call);
      const group = callGroupKey(call);
      if (!rawType) return false;
      if (group === "meeting" && rawType === "meeting") return false;
      if (group === "call" && (rawType === "twoparty" || rawType === "multiparty")) return false;
      if (group === "phone" && (rawType === "twoparty" || rawType === "multiparty")) return false;
      if (group === "group" && (rawType === "multiparty" || rawType === "group")) return false;
      return true;
    }

    function hashString(value) {
      let hash = 0;
      const text = String(value || "");
      for (let index = 0; index < text.length; index += 1) {
        hash = ((hash << 5) - hash) + text.charCodeAt(index);
        hash |= 0;
      }
      return Math.abs(hash);
    }

    function messageSenderKey(message) {
      return normalizeGuid(message.sender_id || "") || normalizeName(message.sender_display_name || "");
    }

    function isOwnMessage(message) {
      const senderId = normalizeGuid(message.sender_id || "");
      const senderName = normalizeName(message.sender_display_name || "");
      return Boolean(
        (CURRENT_USER_ID && senderId && senderId === CURRENT_USER_ID) ||
        (CURRENT_USER_NAME && senderName && senderName === CURRENT_USER_NAME)
      );
    }

    function messageAccent(message) {
      if (isOwnMessage(message)) return MESSAGE_COLOR_SELF;
      const key = messageSenderKey(message);
      if (!key) return "#8A6F5A";
      return MESSAGE_COLOR_PALETTE[hashString(key) % MESSAGE_COLOR_PALETTE.length];
    }

    function callVisualsForColor(color) {
      return CALL_VISUALS[color] || CALL_VISUALS["#8A6F5A"];
    }

    function inboundCallerAccent(linkedCall, message) {
      if (linkedCall && (linkedCall.originator_display_name || linkedCall.originator_id)) {
        return messageAccent({
          sender_display_name: linkedCall.originator_display_name || "",
          sender_id: linkedCall.originator_id || "",
        });
      }
      return messageAccent(message);
    }

    function callCardVisuals(message, linkedCall) {
      if (!linkedCall) {
        return callVisualsForColor(messageAccent(message));
      }
      if (displayCallDirection(linkedCall) === "outgoing") {
        return callVisualsForColor(MESSAGE_COLOR_SELF);
      }
      if (displayCallDirection(linkedCall) === "incoming") {
        return callVisualsForColor(inboundCallerAccent(linkedCall, message));
      }
      return callVisualsForColor(messageAccent(message));
    }

    function truncate(value, maxLength = 110) {
      const text = String(value ?? "").trim();
      if (text.length <= maxLength) return text;
      return `${text.slice(0, maxLength - 1)}…`;
    }

    function showToast(message) {
      toast.textContent = message;
      toast.classList.add("show");
      window.clearTimeout(showToast.timer);
      showToast.timer = window.setTimeout(() => toast.classList.remove("show"), 1600);
    }

    function scrollMainToTop() {
      window.requestAnimationFrame(() => {
        if (mainScrollWrap) {
          mainScrollWrap.scrollTop = 0;
          mainScrollWrap.scrollTo({ top: 0, behavior: "auto" });
        }
        if (contentPanel) {
          contentPanel.scrollTop = 0;
        }
        document.documentElement.scrollTop = 0;
        document.body.scrollTop = 0;
        window.scrollTo({ top: 0, left: 0, behavior: "auto" });
        scheduleSyncScrollTopButtons();
      });
    }

    function scrollSidebarToTop() {
      window.requestAnimationFrame(() => {
        if (sidebarListWrap) {
          sidebarListWrap.scrollTop = 0;
          sidebarListWrap.scrollTo({ top: 0, behavior: "auto" });
        }
        scheduleSyncScrollTopButtons();
      });
    }

    function scrollAllToTop() {
      scrollSidebarToTop();
      scrollMainToTop();
    }

    function centerElementInContainer(container, element, behavior = "smooth") {
      if (!element) return;
      if (!container || container === document.body || container === document.documentElement) {
        element.scrollIntoView({ block: "center", inline: "nearest", behavior });
        return;
      }
      const containerRect = container.getBoundingClientRect();
      const elementRect = element.getBoundingClientRect();
      const rawTop = container.scrollTop + (elementRect.top - containerRect.top) - ((container.clientHeight - elementRect.height) / 2);
      const maxTop = Math.max(0, container.scrollHeight - container.clientHeight);
      const nextTop = Math.max(0, Math.min(maxTop, rawTop));
      container.scrollTo({ top: nextTop, behavior });
    }

    function centerElementAfterLayout(container, element, behavior = "smooth") {
      if (!element) return;
      window.requestAnimationFrame(() => {
        window.requestAnimationFrame(() => {
          centerElementInContainer(container, element, behavior);
        });
      });
    }

    function offsetTopWithinContainer(container, element) {
      if (!container || !element) return 0;
      let top = 0;
      let current = element;
      while (current && current !== container) {
        top += current.offsetTop || 0;
        current = current.offsetParent;
      }
      if (current === container) {
        return top;
      }
      const containerRect = container.getBoundingClientRect();
      const elementRect = element.getBoundingClientRect();
      return container.scrollTop + (elementRect.top - containerRect.top);
    }

    function centerSidebarListRow(container, element, behavior = "smooth") {
      if (!container || !element) return;
      element.scrollIntoView({ block: "nearest", inline: "nearest", behavior: "auto" });
      window.requestAnimationFrame(() => {
        window.requestAnimationFrame(() => {
          const styles = window.getComputedStyle(container);
          const paddingTop = Number.parseFloat(styles.paddingTop || "0") || 0;
          const paddingBottom = Number.parseFloat(styles.paddingBottom || "0") || 0;
          const visibleHeight = Math.max(0, container.clientHeight - paddingTop - paddingBottom);
          const elementTop = offsetTopWithinContainer(container, element);
          const elementHeight = element.offsetHeight || element.getBoundingClientRect().height || 0;
          const rawTop = elementTop - paddingTop - ((visibleHeight - elementHeight) / 2);
          const maxTop = Math.max(0, container.scrollHeight - container.clientHeight);
          const nextTop = Math.max(0, Math.min(maxTop, rawTop));
          container.scrollTo({ top: nextTop, behavior });
        });
      });
    }

    function mainScrollTopInset(container) {
      if (!container) return 0;
      const stickyHeader = container.querySelector(".overview-panel");
      if (!stickyHeader) return 0;
      const containerRect = container.getBoundingClientRect();
      const headerRect = stickyHeader.getBoundingClientRect();
      const overlap = Math.min(containerRect.bottom, headerRect.bottom) - Math.max(containerRect.top, headerRect.top);
      return Math.max(0, overlap);
    }

    function centerMainTimelineRow(container, element, behavior = "smooth") {
      if (!container || !element) return;
      element.scrollIntoView({ block: "nearest", inline: "nearest", behavior: "auto" });
      window.requestAnimationFrame(() => {
        window.requestAnimationFrame(() => {
          const styles = window.getComputedStyle(container);
          const paddingTop = Number.parseFloat(styles.paddingTop || "0") || 0;
          const paddingBottom = Number.parseFloat(styles.paddingBottom || "0") || 0;
          const topInset = paddingTop + mainScrollTopInset(container);
          const visibleHeight = Math.max(0, container.clientHeight - topInset - paddingBottom);
          const elementTop = offsetTopWithinContainer(container, element);
          const elementHeight = element.offsetHeight || element.getBoundingClientRect().height || 0;
          const rawTop = elementTop - topInset - ((visibleHeight - elementHeight) / 2);
          const maxTop = Math.max(0, container.scrollHeight - container.clientHeight);
          const nextTop = Math.max(0, Math.min(maxTop, rawTop));
          container.scrollTo({ top: nextTop, behavior });
        });
      });
    }

    function updateScrollTopButton(button, container) {
      if (!button || !container) return;
      const canScroll = container.scrollHeight > container.clientHeight + 24;
      const shouldShow = canScroll && container.scrollTop > 120;
      button.classList.toggle("visible", shouldShow);
      button.setAttribute("aria-hidden", shouldShow ? "false" : "true");
    }

    function syncScrollTopButtons() {
      updateScrollTopButton(sidebarScrollTopButton, sidebarListWrap);
      updateScrollTopButton(mainScrollTopButton, mainScrollWrap);
    }

    function scheduleSyncScrollTopButtons() {
      window.cancelAnimationFrame(scheduleSyncScrollTopButtons.frame);
      scheduleSyncScrollTopButtons.frame = window.requestAnimationFrame(syncScrollTopButtons);
    }

    async function copyText(value, label) {
      const text = String(value ?? "");
      if (!text) return;
      try {
        await navigator.clipboard.writeText(text);
      } catch (error) {
        const area = document.createElement("textarea");
        area.value = text;
        area.setAttribute("readonly", "");
        area.style.position = "absolute";
        area.style.left = "-9999px";
        document.body.appendChild(area);
        area.select();
        document.execCommand("copy");
        document.body.removeChild(area);
      }
      showToast(label);
    }

    function formatDateOnly(value) {
      if (!value) return "";
      const date = new Date(String(value).length <= 10 ? `${value}T00:00:00` : value);
      if (Number.isNaN(date.getTime())) return String(value);
      return date.toLocaleDateString(undefined, {
        month: "short",
        day: "numeric",
        year: "numeric",
      });
    }

    function fmtTime(value) {
      if (!value) return "";
      const date = new Date(value);
      if (Number.isNaN(date.getTime())) return String(value);
      return date.toLocaleTimeString(undefined, {
        hour: "numeric",
        minute: "2-digit",
      });
    }

    function datasetDayCount() {
      const days = new Set();
      for (const thread of DATA.threads || []) {
        for (const message of thread.messages || []) {
          const key = localDateKey(message.timestamp);
          if (key) days.add(key);
          for (const reaction of message.reactions || []) {
            for (const user of reaction.users || []) {
              const reactionKey = localDateKey(user && user.reacted_at);
              if (reactionKey) days.add(reactionKey);
            }
          }
        }
      }
      for (const call of DATA.calls || []) {
        for (const value of [
          call.start_time,
          call.connect_time,
          call.end_time,
          call.meeting_start_time,
          call.meeting_end_time,
        ]) {
          const key = localDateKey(value);
          if (key) days.add(key);
        }
      }
      return days.size;
    }

    function pad2(value) {
      return String(value).padStart(2, "0");
    }

    function localDateKeyFromDate(date) {
      if (!(date instanceof Date) || Number.isNaN(date.getTime())) return "";
      return `${date.getFullYear()}-${pad2(date.getMonth() + 1)}-${pad2(date.getDate())}`;
    }

    function localDateKey(value) {
      if (!value) return "";
      const date = new Date(value);
      return localDateKeyFromDate(date);
    }

    function todayDateKey() {
      return localDateKeyFromDate(new Date());
    }

    function monthKeyFromDateKey(dateKey) {
      const match = String(dateKey || "").match(/^(\\d{4})-(\\d{2})/);
      return match ? `${match[1]}-${match[2]}` : "";
    }

    function parseMonthKey(monthKey) {
      const match = String(monthKey || "").match(/^(\\d{4})-(\\d{2})$/);
      if (!match) return null;
      const year = Number.parseInt(match[1], 10);
      const month = Number.parseInt(match[2], 10);
      if (!Number.isFinite(year) || !Number.isFinite(month) || month < 1 || month > 12) return null;
      return { year, month };
    }

    function shiftMonthKey(monthKey, offset) {
      const parsed = parseMonthKey(monthKey) || parseMonthKey(monthKeyFromDateKey(todayDateKey()));
      const date = new Date(parsed.year, parsed.month - 1 + offset, 1);
      return `${date.getFullYear()}-${pad2(date.getMonth() + 1)}`;
    }

    function dateKeyInMonth(monthKey, day) {
      const parsed = parseMonthKey(monthKey);
      if (!parsed) return "";
      return `${parsed.year}-${pad2(parsed.month)}-${pad2(day)}`;
    }

    function shiftDateKey(dateKey, offsetDays) {
      const parsed = String(dateKey || "").match(/^(\\d{4})-(\\d{2})-(\\d{2})$/);
      const base = parsed
        ? new Date(Number.parseInt(parsed[1], 10), Number.parseInt(parsed[2], 10) - 1, Number.parseInt(parsed[3], 10))
        : new Date();
      base.setDate(base.getDate() + offsetDays);
      return localDateKeyFromDate(base);
    }

    function selectedDayRange(dateKey = state.activityDate) {
      const start = dateBoundaryValue(dateKey, false);
      const end = dateBoundaryValue(dateKey, true);
      return { start, end };
    }

    function valueFallsOnDate(value, dateKey = state.activityDate) {
      const { start, end } = selectedDayRange(dateKey);
      if (start === null || end === null) return false;
      const current = timeValue(value);
      return Number.isFinite(current) && current >= start && current <= end;
    }

    function normalizeTimeInput(value, fallback) {
      const text = String(value || "").trim();
      return /^\\d{2}:\\d{2}$/.test(text) ? text : fallback;
    }

    function normalizedWorkStart() {
      return normalizeTimeInput(state.activityWorkStart, "08:00");
    }

    function normalizedWorkEnd() {
      return normalizeTimeInput(state.activityWorkEnd, "17:00");
    }

    function normalizedWorkDaysValue() {
      const seen = new Set();
      for (const value of String(state.activityWorkDays || "").split(",")) {
        const day = Number.parseInt(value, 10);
        if (Number.isInteger(day) && day >= 0 && day <= 6) seen.add(String(day));
      }
      return [...seen].sort((left, right) => Number(left) - Number(right)).join(",");
    }

    function configuredWorkdaySet() {
      return new Set(normalizedWorkDaysValue().split(",").filter(value => value !== ""));
    }

    function isConfiguredWorkday(dateKey) {
      const match = String(dateKey || "").match(/^(\\d{4})-(\\d{2})-(\\d{2})$/);
      if (!match) return false;
      const date = new Date(Number.parseInt(match[1], 10), Number.parseInt(match[2], 10) - 1, Number.parseInt(match[3], 10));
      return configuredWorkdaySet().has(String(date.getDay()));
    }

    function minutesFromTimeString(value) {
      const [hours, minutes] = normalizeTimeInput(value, "00:00").split(":").map(part => Number.parseInt(part, 10));
      return (hours * 60) + minutes;
    }

    function activityWorkWindow(dateKey) {
      const match = String(dateKey || "").match(/^(\\d{4})-(\\d{2})-(\\d{2})$/);
      if (!match) return { start: null, end: null };
      const year = Number.parseInt(match[1], 10);
      const month = Number.parseInt(match[2], 10) - 1;
      const day = Number.parseInt(match[3], 10);
      const startMinutes = minutesFromTimeString(normalizedWorkStart());
      const endMinutes = minutesFromTimeString(normalizedWorkEnd());
      const start = new Date(year, month, day, Math.floor(startMinutes / 60), startMinutes % 60, 0, 0).getTime();
      const endDate = new Date(year, month, day, Math.floor(endMinutes / 60), endMinutes % 60, 59, 999);
      if (endMinutes <= startMinutes) {
        endDate.setDate(endDate.getDate() + 1);
      }
      return { start, end: endDate.getTime() };
    }

    function activityResponseWindow(dateKey) {
      const { start, end } = activityWorkWindow(dateKey);
      if (start === null || end === null) return { start: null, end: null };
      const buffer = 2 * 60 * 60 * 1000;
      return { start: start - buffer, end: end + buffer };
    }

    function valueFallsInActivityWindow(value, dateKey = state.activityDate) {
      const { start, end } = activityResponseWindow(dateKey);
      if (start === null || end === null) return false;
      const current = timeValue(value);
      return Number.isFinite(current) && current >= start && current <= end;
    }

    function valueFallsInActivityResponseWindow(value, dateKey = state.activityDate) {
      const { start, end } = activityResponseWindow(dateKey);
      if (start === null || end === null) return false;
      const current = timeValue(value);
      return Number.isFinite(current) && current >= start && current <= end;
    }

    function callOverlapsActivityWindow(call, dateKey) {
      const { start, end } = activityResponseWindow(dateKey);
      if (start === null || end === null) return false;
      const callStart = timeValue(callActivityStartTimestamp(call));
      const callEnd = timeValue(callActivityEndTimestamp(call));
      if (!Number.isFinite(callStart) && !Number.isFinite(callEnd)) return false;
      const boundedStart = Number.isFinite(callStart) ? callStart : callEnd;
      const boundedEnd = Number.isFinite(callEnd) ? callEnd : callStart;
      return boundedStart <= end && boundedEnd >= start;
    }

    function activitySettingsSignature() {
      return `${normalizedWorkStart()}|${normalizedWorkEnd()}|${normalizedWorkDaysValue()}`;
    }

    function resetActivityCaches() {
      ACTIVITY_COUNTS_BY_DAY_CACHE.signature = "";
      ACTIVITY_COUNTS_BY_DAY_CACHE.value = null;
      ACTIVITY_DAY_METRICS_CACHE.clear();
    }

    function formatActivityClockTime(value) {
      const minutes = minutesFromTimeString(value);
      const hours24 = Math.floor(minutes / 60) % 24;
      const displayHours = hours24 % 12 || 12;
      const displayMinutes = pad2(minutes % 60);
      const suffix = hours24 >= 12 ? "PM" : "AM";
      return `${displayHours}:${displayMinutes}${suffix}`;
    }

    function activityWorkWindowLabel() {
      return `${formatActivityClockTime(normalizedWorkStart())} to ${formatActivityClockTime(normalizedWorkEnd())}`;
    }

    function activityWindowSummary(metrics) {
      return `${formatDurationHoursMinutes(metrics.activityWindowSeconds, "0m")} (${metrics.workWindowLabel})`;
    }

    function formatDateRangeLabel(fromValue, toValue) {
      const fromLabel = formatDateOnly(fromValue);
      const toLabel = formatDateOnly(toValue);
      if (fromLabel && toLabel) return `${fromLabel} to ${toLabel}`;
      return fromLabel || toLabel || "Any time";
    }

    function senderInitials(value, limit = 2) {
      const parts = String(value || "")
        .replace(/[^A-Za-z0-9 ]+/g, " ")
        .split(/\\s+/)
        .filter(Boolean);
      if (!parts.length) return "?";
      return parts
        .slice(0, limit)
        .map(part => part[0].toUpperCase())
        .join("");
    }

    function threadListAccent(thread) {
      if (thread.category === "team_chat" || thread.category === "meeting") return "#F97316";
      if (thread.category === "thread") return "#0F766E";
      return "#2563EB";
    }

    function callListAccent(call) {
      if (displayCallState(call) === "missed" || displayCallState(call) === "declined") return "#C2410C";
      if (isMeetingCall(call)) return "#CA8A04";
      if (displayCallDirection(call) === "incoming") return "#0F766E";
      return "#2563EB";
    }

    function callPreviewSummary(call) {
      const parts = dedupe([
        displayCallStatus(call),
        callDuration(call),
        normalizeTextValue(call.meeting_subject || ""),
      ].filter(Boolean));
      return parts.join(" | ");
    }

    function messageIsCallEvent(message) {
      return Boolean(
        message &&
        (
          message.synthetic_call ||
          message.message_type === "Event/Call" ||
          message.message_type === "Call/History"
        )
      );
    }

    function messageIsSystemEventRecord(message) {
      return Boolean(message && message.quality === "event" && !messageIsCallEvent(message));
    }

    function isSystemMessage(message) {
      return Boolean(message && (messageIsSystemEventRecord(message) || messageIsCallEvent(message)));
    }

    function messageDayKey(message) {
      const value = timeValue(message && message.timestamp);
      if (!Number.isFinite(value)) return "";
      const date = new Date(value);
      return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
    }

    function timelineDayLabel(message) {
      if (!message || !message.timestamp) return "";
      const date = new Date(message.timestamp);
      if (Number.isNaN(date.getTime())) return String(message.timestamp || "");
      return date.toLocaleDateString(undefined, {
        weekday: "short",
        month: "short",
        day: "numeric",
        year: "numeric",
      });
    }

    function messagesShareVisualCluster(previousMessage, nextMessage) {
      if (!previousMessage || !nextMessage) return false;
      if (isSystemMessage(previousMessage) || isSystemMessage(nextMessage)) return false;
      if (messageSenderKey(previousMessage) !== messageSenderKey(nextMessage)) return false;
      if (messageDayKey(previousMessage) !== messageDayKey(nextMessage)) return false;
      const timeGap = Math.abs(timeValue(previousMessage.timestamp) - timeValue(nextMessage.timestamp));
      return timeGap <= 5 * 60 * 1000;
    }

    function renderTimeline(messages, thread, options = {}) {
      const messageOptions = typeof options.messageOptions === "function"
        ? options.messageOptions
        : (() => ({}));
      const includeDayDividers = options.includeDayDividers !== false;
      const fragments = [];

      for (let index = 0; index < messages.length; index += 1) {
        const message = messages[index];
        const previousMessage = index > 0 ? messages[index - 1] : null;
        const nextMessage = index < messages.length - 1 ? messages[index + 1] : null;

        if (includeDayDividers && messageDayKey(message) !== messageDayKey(previousMessage)) {
          fragments.push(`<div class="timeline-divider"><span>${escapeHtml(timelineDayLabel(message))}</span></div>`);
        }

        fragments.push(renderMessageRow(message, thread, {
          ...messageOptions(message, index, messages),
          groupedWithPrevious: messagesShareVisualCluster(previousMessage, message),
          groupedWithNext: messagesShareVisualCluster(message, nextMessage),
        }));
      }

      return fragments.join("");
    }

    function syncInputsFromState() {
      messageSearch.value = state.messageSearch || "";
      categoryFilter.value = state.category || "";
      messageDateFrom.value = state.messageDateFrom || "";
      messageDateTo.value = state.messageDateTo || "";
      callSearch.value = state.callSearch || "";
      callGroupFilter.value = state.callGroup || "";
      callDirectionFilter.value = state.callDirection || "";
      callDateFrom.value = state.callDateFrom || "";
      callDateTo.value = state.callDateTo || "";
      if (activityMonth) activityMonth.value = state.activityMonth || monthKeyFromDateKey(state.activityDate) || "";
      if (activityWorkStart) activityWorkStart.value = normalizedWorkStart();
      if (activityWorkEnd) activityWorkEnd.value = normalizedWorkEnd();
      const checkedDays = configuredWorkdaySet();
      for (const input of activityWorkdayInputs) {
        input.checked = checkedDays.has(String(input.value));
      }
    }

    function renderChrome() {
      const modeLabel = state.view === "activity"
        ? "Activity Diagnostics"
        : (state.view === "calls"
          ? "Calls Workspace"
          : (state.messageSearch ? "Search Workspace" : "Messages Workspace"));
      if (brandProfile) brandProfile.textContent = `PROFILE: ${PROFILE_DISPLAY_NAME}`;
      if (overviewMode) overviewMode.textContent = modeLabel;
      if (appShell) appShell.dataset.view = state.view;
      if (contentPanel) contentPanel.dataset.view = state.view;
    }

    function activeFilterEntries() {
      const entries = [];
      if (state.view === "messages") {
        if (state.messageSearch) {
          entries.push({ key: "message-search", label: `Search: ${truncate(state.messageSearch, 28)}` });
        }
        if (state.category) {
          entries.push({ key: "message-category", label: `Type: ${prettyCategory(state.category)}` });
        }
        if (state.messageDateFrom || state.messageDateTo) {
          entries.push({ key: "message-date", label: `Global: ${formatDateRangeLabel(state.messageDateFrom, state.messageDateTo)}` });
        }
        if (state.threadDateFrom || state.threadDateTo) {
          entries.push({ key: "thread-date", label: `Timeline: ${formatDateRangeLabel(state.threadDateFrom, state.threadDateTo)}` });
        }
        if (state.messageViewFilter && state.messageViewFilter !== "all") {
          const messageViewFilterLabels = {
            messages: "Messages only",
            calls: "Calls only",
            events: "System events only",
          };
          const label = messageViewFilterLabels[state.messageViewFilter] || state.messageViewFilter;
          entries.push({ key: "message-view-filter", label: `View: ${label}` });
        }
      } else if (state.view === "calls") {
        if (state.callSearch) {
          entries.push({ key: "call-search", label: `Search: ${truncate(state.callSearch, 28)}` });
        }
        if (state.callGroup) {
          const callGroupLabels = {
            phone: "Phone",
            meeting: "Meeting",
            group: "Group",
            call: "Call",
          };
          entries.push({ key: "call-group", label: `Type: ${callGroupLabels[state.callGroup] || state.callGroup}` });
        }
        if (state.callDirection) {
          const directionLabels = {
            inbound: "Inbound",
            outbound: "Outbound",
            declined: "Declined",
            missed: "Missed",
          };
          entries.push({ key: "call-direction", label: `Direction: ${directionLabels[state.callDirection] || state.callDirection}` });
        }
        if (state.callDateFrom || state.callDateTo) {
          entries.push({ key: "call-date", label: `Window: ${formatDateRangeLabel(state.callDateFrom, state.callDateTo)}` });
        }
      } else if (state.view === "activity") {
        if (state.activityDate) {
          entries.push({ key: "activity-date", label: `Day: ${formatDateOnly(state.activityDate)}` });
        }
        entries.push({ key: "activity-window", label: `Work: ${activityWorkWindowLabel()}` });
      }
      return entries;
    }

    function renderActiveFilters() {
      if (!activeFilterBar) return;
      const entries = activeFilterEntries();
      activeFilterBar.innerHTML = entries.map(entry => `
        <button type="button" class="filter-pill" data-clear-filter="${escapeHtml(entry.key)}">
          <span>${escapeHtml(entry.label)}</span>
          <span class="dismiss">x</span>
        </button>
      `).join("") || `<div class="subtle">${state.view === "activity" ? "Select a day on the calendar." : "No active filters. Press / to search."}</div>`;
    }

    function persistState() {
      try {
        window.localStorage.setItem(UI_STATE_STORAGE_KEY, JSON.stringify({
          view: state.view,
          messageSearch: state.messageSearch,
          messageDateFrom: state.messageDateFrom,
          messageDateTo: state.messageDateTo,
          callSearch: state.callSearch,
          category: state.category,
          callGroup: state.callGroup,
          callDirection: state.callDirection,
          callDateFrom: state.callDateFrom,
          callDateTo: state.callDateTo,
          activityDate: state.activityDate,
          activityMonth: state.activityMonth,
          activityWorkStart: normalizedWorkStart(),
          activityWorkEnd: normalizedWorkEnd(),
          activityWorkDays: normalizedWorkDaysValue(),
          messageViewFilter: state.messageViewFilter,
          threadDateFrom: state.threadDateFrom,
          threadDateTo: state.threadDateTo,
          expandHiddenData: state.expandHiddenData,
          threadId: state.threadId,
          callKey: state.callKey,
        }));
      } catch (error) {
        // Ignore storage failures in local-file contexts or locked-down browsers.
      }
    }

    function schedulePersistState() {
      window.clearTimeout(schedulePersistState.timer);
      schedulePersistState.timer = window.setTimeout(persistState, 60);
    }

    function restoreState() {
      try {
        const raw = window.localStorage.getItem(UI_STATE_STORAGE_KEY);
        if (!raw) return;
        const parsed = JSON.parse(raw);
        if (!parsed || typeof parsed !== "object") return;
        const stringKeys = [
          "view",
          "messageSearch",
          "messageDateFrom",
          "messageDateTo",
          "callSearch",
          "category",
          "callGroup",
          "callDirection",
          "callDateFrom",
          "callDateTo",
          "activityDate",
          "activityMonth",
          "activityWorkStart",
          "activityWorkEnd",
          "activityWorkDays",
          "messageViewFilter",
          "threadDateFrom",
          "threadDateTo",
          "threadId",
          "callKey",
        ];
        for (const key of stringKeys) {
          if (typeof parsed[key] === "string") state[key] = parsed[key];
        }
        if (typeof parsed.expandHiddenData === "boolean") {
          state.expandHiddenData = parsed.expandHiddenData;
        }
        if (!["messages", "calls", "activity"].includes(state.view)) state.view = "messages";
        if (!["all", "messages", "calls", "events"].includes(state.messageViewFilter)) {
          state.messageViewFilter = "all";
        }
      } catch (error) {
        // Ignore malformed or unavailable local storage.
      }
    }

    function focusActiveSearchField() {
      if (state.view === "activity") return;
      const element = state.view === "calls" ? callSearch : messageSearch;
      if (!element) return;
      element.focus();
      element.select();
    }

    function isTypingTarget(target) {
      return Boolean(
        target &&
        (
          target.closest("input, textarea, select") ||
          target.isContentEditable
        )
      );
    }

    function clearCurrentSearch() {
      if (state.view === "calls" && state.callSearch) {
        state.callSearch = "";
        renderView();
        return true;
      }
      if (state.view === "messages" && state.messageSearch) {
        clearMessageSearchState();
        renderView();
        return true;
      }
      return false;
    }

    function clearMessageSearchState() {
      state.messageSearch = "";
      if (messageSearch) messageSearch.value = "";
      state.focusMessageId = null;
      state.focusCallKey = null;
      state.focusTimestamp = null;
      state.focusSearchQuery = "";
      window.clearTimeout(scheduleSearchGroupsComputation.timer);
      scheduleSearchGroupsComputation.pendingSignature = "";
    }

    function openThreadView(options = {}) {
      const threadId = String(options.threadId || "");
      if (!threadId) return;
      state.view = "messages";
      state.threadId = threadId;
      if (options.clearSearch) {
        clearMessageSearchState();
      }
      if (options.clearCategory) {
        state.category = "";
      }
      state.messageViewFilter = options.viewFilter || "all";
      if (options.syncThreadDateToSidebar) {
        state.threadDateFrom = state.messageDateFrom || "";
        state.threadDateTo = state.messageDateTo || "";
      } else {
        state.threadDateFrom = "";
        state.threadDateTo = "";
      }
      state.focusMessageId = options.focusMessageId || null;
      state.focusTimestamp = options.focusTimestamp || null;
      state.focusCallKey = options.focusCallKey || null;
      state.focusSearchQuery = String(options.focusSearchQuery || "").trim();
      renderView();
      if (options.revealInSidebar) {
        revealActiveListRow(threadList, { behavior: options.scrollBehavior || "smooth" });
      }
      if (options.scrollTop) {
        scrollMainToTop();
      }
    }

    function openCallView(options = {}) {
      const nextCallKey = String(options.callKey || "");
      if (!nextCallKey) return;
      state.view = "calls";
      state.callKey = nextCallKey;
      state.focusMessageId = null;
      state.focusCallKey = null;
      state.focusTimestamp = null;
      state.focusSearchQuery = "";
      renderView();
      if (options.revealInSidebar) {
        revealActiveListRow(callList, { behavior: options.scrollBehavior || "smooth" });
      }
      if (options.scrollTop) {
        scrollMainToTop();
      }
    }

    function revealActiveListRow(scope, options = {}) {
      if (!scope) return;
      const activeRow = scope.querySelector(".list-row.active");
      if (!activeRow) return;
      const container = scope.closest(".sidebar-list-wrap") || sidebarListWrap;
      centerSidebarListRow(container, activeRow, options.behavior || "smooth");
    }

    function moveSidebarSelection(direction) {
      if (state.view === "messages") {
        if (state.messageSearch) return;
        const rows = filteredThreads();
        if (!rows.length) return;
        let index = rows.findIndex(thread => thread.id === state.threadId);
        if (index < 0) index = 0;
        index = Math.max(0, Math.min(rows.length - 1, index + direction));
        state.threadId = rows[index].id;
        state.focusMessageId = null;
        state.focusCallKey = null;
        state.focusTimestamp = null;
        state.focusSearchQuery = "";
        renderView();
        revealActiveListRow(threadList);
        scrollMainToTop();
        return;
      }

      if (state.view === "activity") {
        selectActivityDate(shiftDateKey(state.activityDate || todayDateKey(), direction));
        return;
      }

      const rows = filteredCalls();
      if (!rows.length) return;
      let index = rows.findIndex(call => callKey(call) === state.callKey);
      if (index < 0) index = 0;
      index = Math.max(0, Math.min(rows.length - 1, index + direction));
      state.callKey = callKey(rows[index]);
      renderView();
      revealActiveListRow(callList);
    }

    function scheduleMessageSearchRender() {
      window.clearTimeout(scheduleMessageSearchRender.timer);
      scheduleMessageSearchRender.timer = window.setTimeout(() => {
        renderView();
        scrollMainToTop();
      }, 90);
    }

    function scheduleCallSearchRender() {
      window.clearTimeout(scheduleCallSearchRender.timer);
      scheduleCallSearchRender.timer = window.setTimeout(() => {
        renderView();
      }, 90);
    }

    function prettyCategory(category) {
      if (category === "chat_space") return "Chat";
      if (category === "team_chat" || category === "meeting") return "Meeting Chat";
      if (category === "thread") return "Group Chat";
      return category || "";
    }

    function isChatBasedThread(thread) {
      return ["chat_space", "thread", "team_chat", "meeting"].includes(thread.category);
    }

    function matchesThreadCategory(thread, category) {
      if (!category) return true;
      if (category === "team_chat") {
        return ["team_chat", "meeting"].includes(thread.category);
      }
      return thread.category === category;
    }

    function threadSearchText(thread) {
      const cacheKey = String(thread && thread.id || "");
      if (cacheKey && THREAD_SEARCH_TEXT_CACHE.has(cacheKey)) {
        return THREAD_SEARCH_TEXT_CACHE.get(cacheKey);
      }
      const parts = [
        thread.label,
        threadDisplayLabel(thread),
        thread.id,
        thread.category,
        ...(thread.participants || []),
      ];
      const value = parts.filter(Boolean).join(" ").toLowerCase();
      if (cacheKey) {
        THREAD_SEARCH_TEXT_CACHE.set(cacheKey, value);
      }
      return value;
    }

    function searchTermsForQuery(queryText) {
      return [...new Set(String(queryText || "")
        .trim()
        .toLowerCase()
        .split(" ")
        .map(term => term.trim())
        .filter(Boolean))];
    }

    function searchTerms() {
      return searchTermsForQuery(state.messageSearch);
    }

    function textMatchesQuery(text, queryText) {
      const haystack = String(text || "").toLowerCase();
      const query = String(queryText || "").trim().toLowerCase();
      if (!query) return true;
      if (!haystack) return false;
      if (haystack.includes(query)) return true;
      const terms = searchTermsForQuery(queryText);
      return terms.length > 1 && terms.every(term => haystack.includes(term));
    }

    function textMatchesSearch(text) {
      return textMatchesQuery(text, state.messageSearch);
    }

    function latestMatchingSearchMessage(thread, queryText = state.messageSearch) {
      if (!String(queryText || "").trim()) return null;
      for (const message of sortedThreadTimelineItems(thread)) {
        if (!messagePassesSidebarDateRange(message)) continue;
        if (!includeMessageInSearchResults(message)) continue;
        if (textMatchesQuery(searchMessageText(thread, message), queryText)) {
          return message;
        }
      }
      return null;
    }

    function threadMatchesSearch(thread) {
      if (!state.messageSearch) return true;
      if (textMatchesSearch(threadSearchText(thread))) {
        return true;
      }
      return Boolean(latestMatchingSearchMessage(thread));
    }

    function threadNameSearchPriority(thread) {
      const query = String(state.messageSearch || "").trim().toLowerCase();
      const terms = searchTerms();
      if (!query) return 2;
      const candidates = dedupe([
        threadDisplayLabel(thread),
        ...(thread.participants || []).map(value => normalizeTextValue(value)),
      ].filter(Boolean));
      let best = 2;
      for (const candidate of candidates) {
        const lowered = candidate.toLowerCase();
        const words = lowered.split(/[^a-z0-9]+/).filter(Boolean);
        if (!lowered) continue;
        if (lowered === query) return 0;
        if (words.some(word => word.startsWith(query))) {
          best = Math.min(best, 0);
          continue;
        }
        if (terms.length > 1 && terms.every(term => words.some(word => word.startsWith(term)))) {
          best = Math.min(best, 0);
          continue;
        }
        if (lowered.includes(query)) {
          best = Math.min(best, 1);
          continue;
        }
        if (terms.length > 1 && terms.every(term => lowered.includes(term))) {
          best = Math.min(best, 1);
        }
      }
      return best;
    }

    function threadSearchCategoryPriority(thread) {
      if (thread.category === "chat_space") return 0;
      if (thread.category === "thread") return 1;
      if (thread.category === "team_chat" || thread.category === "meeting") return 2;
      return 3;
    }

    function hasSidebarMessageDateRange() {
      return Boolean(state.messageDateFrom || state.messageDateTo);
    }

    function normalizedSidebarMessageDateRange() {
      const start = dateBoundaryValue(state.messageDateFrom, false);
      const end = dateBoundaryValue(state.messageDateTo, true);
      if (start === null && end === null) return { start: null, end: null };
      if (start !== null && end !== null && start > end) {
        return { start: end, end: start };
      }
      return { start, end };
    }

    function messagePassesSidebarDateRange(message) {
      const { start, end } = normalizedSidebarMessageDateRange();
      if (start === null && end === null) return true;
      const current = timeValue(message.timestamp);
      if (!Number.isFinite(current)) return false;
      if (start !== null && current < start) return false;
      if (end !== null && current > end) return false;
      return true;
    }

    function visibleSidebarThreadMessages(thread) {
      if (!hasSidebarMessageDateRange()) return thread.messages || [];
      return (thread.messages || []).filter(messagePassesSidebarDateRange);
    }

    function highlightSearchHtml(value, queryText = state.messageSearch) {
      const text = String(value ?? "");
      const terms = searchTermsForQuery(queryText).sort((left, right) => right.length - left.length);
      if (!text || !terms.length) return escapeHtml(text);

      const lower = text.toLowerCase();
      let html = "";
      let index = 0;

      while (index < text.length) {
        let matchedTerm = "";
        for (const term of terms) {
          if (term && lower.startsWith(term, index)) {
            matchedTerm = text.slice(index, index + term.length);
            break;
          }
        }
        if (matchedTerm) {
          html += `<strong class="search-term">${escapeHtml(matchedTerm)}</strong>`;
          index += matchedTerm.length;
          continue;
        }
        html += escapeHtml(text[index]);
        index += 1;
      }

      return html;
    }

    function threadSidebarSummary(thread) {
      const key = String(thread && thread.id || "");
      if (!key || hasSidebarMessageDateRange()) return null;
      if (THREAD_SIDEBAR_SUMMARY_CACHE.has(key)) {
        return THREAD_SIDEBAR_SUMMARY_CACHE.get(key);
      }

      let latestMessage = null;
      let latestTime = Number.NEGATIVE_INFINITY;
      for (const message of thread.messages || []) {
        const current = timeValue(message.timestamp);
        if (current >= latestTime) {
          latestTime = current;
          latestMessage = message;
        }
      }

      const summary = {
        latestMessage,
        latestTimestamp: latestTime,
        latestTimestampRaw: latestMessage ? (latestMessage.timestamp || null) : null,
      };
      THREAD_SIDEBAR_SUMMARY_CACHE.set(key, summary);
      return summary;
    }

    function threadPreviewForMessage(message) {
      if (!message) return "No recoverable message preview";
      const attachmentPreview = messageAttachmentPreview(message);
      const replyQuote = messageReplyQuote(message);
      if (replyQuote) {
        const replyParts = [];
        if (replyQuote.author && replyQuote.preview) {
          replyParts.push(`${replyQuote.author}: ${replyQuote.preview}`);
        } else if (replyQuote.preview) {
          replyParts.push(replyQuote.preview);
        }
        if (replyQuote.reply_text) {
          replyParts.push(replyQuote.reply_text);
        }
        if (replyParts.length) {
          const previewText = truncate(replyParts.join(" | "));
          if (attachmentPreview) {
            return truncate(`${previewText} [${attachmentPreview}]`);
          }
          return previewText;
        }
      }
      if (attachmentPreview) {
        if (message.content_text) {
          return truncate(`${normalizeTextValue(message.content_text)} [${attachmentPreview}]`);
        }
        return truncate(attachmentPreview);
      }
      if (message.message_type === "Event/Call") {
        return truncate(`Call event: ${prettyCallEventName(callEventName(message.content_text || ""))}`);
      }
      if (message.message_type === "ThreadActivity/AddMember") {
        const meta = messageHiddenMeta(message);
        return truncate(meta && meta.previewLabel ? meta.previewLabel : "Member added");
      }
      if (message.message_type === "ThreadActivity/MemberJoined") {
        const meta = messageHiddenMeta(message);
        return truncate(meta && meta.previewLabel ? meta.previewLabel : "Member joined");
      }
      if (message.message_type === "ThreadActivity/DeleteMember") {
        const meta = messageHiddenMeta(message);
        return truncate(meta && meta.previewLabel ? meta.previewLabel : "Member removed");
      }
      if (message.message_type === "ThreadActivity/TopicUpdate") {
        const parsed = parseTopicUpdateEvent(message);
        return truncate(`Topic updated: ${parsed.topic || "Unknown topic"}`);
      }
      return truncate(normalizeTextValue(message.content_text || message.message_type || ""));
    }

    function latestThreadMessage(thread) {
      const summary = threadSidebarSummary(thread);
      if (summary) return summary.latestMessage;
      let bestMessage = null;
      let bestTime = Number.NEGATIVE_INFINITY;
      for (const message of visibleSidebarThreadMessages(thread)) {
        const current = timeValue(message.timestamp);
        if (current >= bestTime) {
          bestTime = current;
          bestMessage = message;
        }
      }
      return bestMessage;
    }

    function latestThreadPreview(thread) {
      const summary = threadSidebarSummary(thread);
      if (summary) return threadPreviewForMessage(summary.latestMessage);
      return threadPreviewForMessage(latestThreadMessage(thread));
    }

    function callPrimaryTimestamp(call) {
      return call.start_time || call.connect_time || call.end_time || "";
    }

    function threadLastTimestamp(thread) {
      const summary = threadSidebarSummary(thread);
      if (summary) return summary.latestTimestamp;
      let latest = Number.NEGATIVE_INFINITY;
      for (const message of visibleSidebarThreadMessages(thread)) {
        latest = Math.max(latest, timeValue(message.timestamp));
      }
      return latest;
    }

    function threadLastTimestampRaw(thread) {
      const summary = threadSidebarSummary(thread);
      if (summary) return summary.latestTimestampRaw;
      let best = null;
      let latest = Number.NEGATIVE_INFINITY;
      for (const message of visibleSidebarThreadMessages(thread)) {
        const current = timeValue(message.timestamp);
        if (current >= latest) {
          latest = current;
          best = message.timestamp || best;
        }
      }
      return best;
    }

    function filteredThreads() {
      return DATA.threads
        .filter(thread => {
          if (thread.message_count <= 0 && !["team_chat", "meeting"].includes(thread.category)) return false;
          if (!matchesThreadCategory(thread, state.category)) {
            return false;
          }
          if (visibleSidebarThreadMessages(thread).length === 0) return false;
          if (!threadMatchesSearch(thread)) return false;
          return true;
        })
        .sort((left, right) => {
          if (state.messageSearch) {
            const leftPriority = threadNameSearchPriority(left);
            const rightPriority = threadNameSearchPriority(right);
            const priorityDiff = leftPriority - rightPriority;
            if (priorityDiff !== 0) return priorityDiff;
            if (leftPriority < 2 && rightPriority < 2) {
              const categoryDiff = threadSearchCategoryPriority(left) - threadSearchCategoryPriority(right);
              if (categoryDiff !== 0) return categoryDiff;
            }
          }
          const timeDiff = threadLastTimestamp(right) - threadLastTimestamp(left);
          if (timeDiff !== 0) return timeDiff;
          return (left.label || left.id || "").localeCompare(right.label || right.id || "");
        });
    }

    function callKey(call) {
      if (!call || typeof call !== "object") return "||||";
      if (CALL_KEY_CACHE.has(call)) return CALL_KEY_CACHE.get(call);
      const value = [
        call.call_id || "",
        call.start_time || "",
        call.shared_correlation_id || "",
        call.originator_id || "",
        call.target_id || "",
      ].join("|");
      CALL_KEY_CACHE.set(call, value);
      return value;
    }

    function callLabel(call) {
      const key = callKey(call);
      if (CALL_LABEL_CACHE.has(key)) return CALL_LABEL_CACHE.get(key);
      let value = "[unknown call]";
      if (isMeetingCall(call)) {
        value = meetingCallTitle(call);
      } else {
        const participants = callParticipantDisplayNames(call);
        if (participants.length) {
          value = summarizeNames(participants);
        } else {
          const origin = callSideLabel(call, "originator");
          const target = callSideLabel(call, "target");
          value = origin && target ? `${origin} -> ${target}` : (origin || target || call.summary_text || call.call_id || "[unknown call]");
        }
      }
      CALL_LABEL_CACHE.set(key, value);
      return value;
    }

    function extractGuids(text) {
      return Array.from(String(text || "").matchAll(/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/g))
        .map(match => match[0].toLowerCase());
    }

    function eventCallGuid(text) {
      const match = String(text || "").match(/\\b([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})\\b(?:\\s+False)?\\s*$/i);
      return match ? match[1].toLowerCase() : "";
    }

    function findLinkedCall(message) {
      if (LINKED_CALL_BY_MESSAGE_CACHE.has(message)) {
        return LINKED_CALL_BY_MESSAGE_CACHE.get(message);
      }
      let linked = null;
      if (message.synthetic_call_key && CALLS_BY_KEY.has(message.synthetic_call_key)) {
        linked = CALLS_BY_KEY.get(message.synthetic_call_key);
      } else {
        const eventGuid = eventCallGuid(message.content_text || "");
        if (eventGuid && CALLS_BY_ID.has(eventGuid)) {
          linked = CALLS_BY_ID.get(eventGuid);
        } else if (eventGuid && CALLS_BY_SHARED.has(eventGuid)) {
          linked = CALLS_BY_SHARED.get(eventGuid);
        } else {
          const ids = extractGuids(message.content_text || "");
          for (const id of ids) {
            if (CALLS_BY_ID.has(id)) {
              linked = CALLS_BY_ID.get(id);
              break;
            }
          }
          if (!linked) {
            for (const id of ids) {
              if (CALLS_BY_SHARED.has(id)) {
                linked = CALLS_BY_SHARED.get(id);
                break;
              }
            }
          }
        }
      }
      LINKED_CALL_BY_MESSAGE_CACHE.set(message, linked);
      return linked;
    }

    function callEventName(text) {
      const match = String(text || "").match(/\\b(callStarted|callEnded|callMissed|callAccepted|callRejected|callCancelled)\\b/i);
      return match ? match[1] : "callEvent";
    }

    function prettyCallEventName(value) {
      return String(value || "")
        .replace(/[_-]+/g, " ")
        .replace(/^call/, "Call ")
        .replace(/([a-z])([A-Z])/g, "$1 $2")
        .trim();
    }

    function collectEventParticipants(message) {
      const seen = [];
      for (const guid of extractGuids(message.content_text || "")) {
        const name = personNameForGuid(guid);
        if (name && !seen.includes(name)) {
          seen.push(name);
        }
      }
      if (message.sender_display_name && !seen.includes(message.sender_display_name)) {
        seen.push(message.sender_display_name);
      }
      return seen;
    }

    function representedCallKeys(thread) {
      const keys = new Set();
      for (const message of thread.messages || []) {
        const linked = findLinkedCall(message);
        if (linked) keys.add(callKey(linked));
      }
      return keys;
    }

    function syntheticCallsForThread(thread) {
      if (!thread || !thread.id) return [];
      if (SYNTHETIC_CALLS_CACHE.has(thread.id)) return SYNTHETIC_CALLS_CACHE.get(thread.id);

      const represented = representedCallKeys(thread);
      const matches = [];
      const seen = new Set();

      for (const call of CALLS_BY_THREAD_ID.get(String(thread.id)) || []) {
        const key = callKey(call);
        if (!represented.has(key) && !seen.has(key)) {
          seen.add(key);
          matches.push(call);
        }
      }

      const isTwoPersonConversation = (thread.participants || []).length === 2;
      if (isTwoPersonConversation) {
        const guidPair = participantGuidPairKey(thread.participant_ids || []);
        const namePair = participantNamePairKey(thread.participants || []);
        const pairMatches = [
          ...(guidPair ? (CALLS_BY_GUID_PAIR.get(guidPair) || []) : []),
          ...(namePair ? (CALLS_BY_NAME_PAIR.get(namePair) || []) : []),
        ];
        for (const call of pairMatches) {
          const key = callKey(call);
          if (!represented.has(key) && !seen.has(key)) {
            seen.add(key);
            matches.push(call);
          }
        }
      }

      matches.sort((left, right) => timeValue(callTimelineTimestamp(right)) - timeValue(callTimelineTimestamp(left)));
      SYNTHETIC_CALLS_CACHE.set(thread.id, matches);
      return matches;
    }

    function linkedCallsForThread(thread) {
      const cacheKey = String(thread && thread.id || "");
      if (cacheKey && LINKED_CALLS_BY_THREAD_CACHE.has(cacheKey)) {
        return LINKED_CALLS_BY_THREAD_CACHE.get(cacheKey);
      }
      const linked = new Map();
      for (const message of thread.messages || []) {
        const call = findLinkedCall(message);
        if (call) linked.set(callKey(call), call);
      }
      for (const call of syntheticCallsForThread(thread)) {
        linked.set(callKey(call), call);
      }
      const value = [...linked.values()].sort((left, right) => timeValue(callTimelineTimestamp(right)) - timeValue(callTimelineTimestamp(left)));
      if (cacheKey) {
        LINKED_CALLS_BY_THREAD_CACHE.set(cacheKey, value);
      }
      return value;
    }

    function syntheticCallMessages(thread) {
      return syntheticCallsForThread(thread).map(call => ({
        id: `synthetic-call:${callKey(call)}`,
        timestamp: callTimelineTimestamp(call),
        sender_display_name: call.originator_display_name || call.target_display_name || "Call Record",
        sender_id: call.originator_id || call.target_id || "",
        message_type: "Call/History",
        quality: "event",
        content_text: call.summary_text || "",
        synthetic_call: true,
        synthetic_call_key: callKey(call),
      }));
    }

    function renderCallEventBody(message) {
      const raw = message.content_text || "";
      const linkedCall = findLinkedCall(message);
      const eventName = message.synthetic_call ? "Call Record" : prettyCallEventName(callEventName(raw));
      const linkedKey = linkedCall ? callKey(linkedCall) : "";
      const visuals = callCardVisuals(message, linkedCall);
      const participantEntries = callEventParticipantEntries(message, linkedCall);

      const cardHtml = `
        <div class="call-event" style="--call-bg:${escapeHtml(visuals.bg)};--call-outline:${escapeHtml(visuals.outline)};--call-block-bg:${escapeHtml(visuals.block)};--call-title:${escapeHtml(visuals.title)};">
          <div class="call-event-header">
            <div class="call-event-title">${highlightSearchHtml(eventName)}</div>
            <div class="call-event-actions">
              ${linkedCall ? `<button class="call-link open-call-record" type="button" data-call-key="${escapeHtml(linkedKey)}">Open In Calls</button>` : ``}
            </div>
          </div>
          <div class="call-event-grid">
            <div class="call-event-block wide"><div class="k">Participants</div>${renderExpandableChipGroup(participantEntries, { emptyLabel: normalizeTextValue(callLabel(linkedCall || {})) || "No participants were resolved." })}</div>
            <div class="call-event-block"><div class="k">Direction</div><div>${highlightSearchHtml(linkedCall ? displayCallDirectionLabel(linkedCall) : "")}</div></div>
            <div class="call-event-block"><div class="k">State</div><div>${highlightSearchHtml(linkedCall ? displayCallStateLabel(linkedCall) : eventName)}</div></div>
            <div class="call-event-block"><div class="k">Start Time</div><div>${escapeHtml(fmt(linkedCall ? linkedCall.start_time : message.timestamp))}</div></div>
            <div class="call-event-block"><div class="k">End Time</div><div>${escapeHtml(fmt(linkedCall ? linkedCall.end_time : null))}</div></div>
          </div>
          ${message.synthetic_call
            ? `<div class="subtle">Merged from the Calls dataset for this conversation.</div>`
            : ``}
        </div>
      `;
      return cardHtml;
    }

    function messageLinkedCallKey(message) {
      if (message.synthetic_call_key) return message.synthetic_call_key;
      const linked = findLinkedCall(message);
      return linked ? callKey(linked) : "";
    }

    function threadTimelineItems(thread) {
      const cacheKey = String(thread && thread.id || "");
      if (cacheKey && THREAD_TIMELINE_CACHE.has(cacheKey)) {
        return THREAD_TIMELINE_CACHE.get(cacheKey);
      }
      const value = [...(thread.messages || []), ...syntheticCallMessages(thread)];
      if (cacheKey) {
        THREAD_TIMELINE_CACHE.set(cacheKey, value);
      }
      return value;
    }

    function sortedThreadTimelineItems(thread) {
      const cacheKey = String(thread && thread.id || "");
      if (cacheKey && SORTED_THREAD_TIMELINE_CACHE.has(cacheKey)) {
        return SORTED_THREAD_TIMELINE_CACHE.get(cacheKey);
      }
      const value = threadTimelineItems(thread)
        .slice()
        .sort((left, right) => {
          const timeDiff = timeValue(right.timestamp) - timeValue(left.timestamp);
          if (timeDiff !== 0) return timeDiff;
          return (right.id || "").localeCompare(left.id || "");
        });
      if (cacheKey) {
        SORTED_THREAD_TIMELINE_CACHE.set(cacheKey, value);
      }
      return value;
    }

    function hasNearbyCuratedMessages(thread, call) {
      const start = timeValue(call.start_time || call.end_time || "");
      const end = timeValue(call.end_time || call.start_time || "");
      if (!Number.isFinite(start) && !Number.isFinite(end)) return false;
      const windowStart = (Number.isFinite(start) ? start : end) - (15 * 60 * 1000);
      const windowEnd = (Number.isFinite(end) ? end : start) + (15 * 60 * 1000);
      return (thread.messages || []).some(message => {
        if (message.quality === "event") return false;
        const current = timeValue(message.timestamp);
        return Number.isFinite(current) && current >= windowStart && current <= windowEnd;
      });
    }

    function resolveGuidLabel(guid) {
      const cleaned = personNameForGuid(guid);
      return cleaned || normalizeTextValue(guid || "Unknown");
    }

    function systemEventActorLabel() {
      return "System";
    }

    function parseJsonObject(text) {
      try {
        const parsed = JSON.parse(String(text || ""));
        return parsed && typeof parsed === "object" ? parsed : null;
      } catch {
        return null;
      }
    }

    function resolveMemberEntries(entries) {
      const memberIds = [];
      const memberNames = [];
      for (const entry of Array.isArray(entries) ? entries : []) {
        const memberId = normalizeGuid((entry && (entry.id || entry.mri || entry.userId)) || "");
        const friendlyName = normalizeTextValue((entry && (entry.friendlyname || entry.displayName || entry.name)) || "");
        const resolvedName = friendlyName || (memberId ? personNameForGuid(memberId) : "");
        if (memberId && !memberIds.includes(memberId)) memberIds.push(memberId);
        if (resolvedName && !memberNames.includes(resolvedName)) memberNames.push(resolvedName);
      }
      return { memberIds, memberNames };
    }

    function participantEntryKey(entry) {
      const guid = normalizeGuid(entry && entry.id);
      const name = normalizeName(entry && entry.name);
      return guid || name || "";
    }

    function buildParticipantEntries(ids = [], names = []) {
      const entries = [];
      if (ids.length && ids.length === names.length) {
        for (let index = 0; index < ids.length; index += 1) {
          const guid = normalizeGuid(ids[index]);
          const name = cleanCallParticipantName(names[index] || (guid ? resolveGuidLabel(guid) : ""));
          entries.push({ id: guid, name: name || (guid ? resolveGuidLabel(guid) : "") });
        }
      } else {
        for (const guid of ids || []) {
          const normalizedGuid = normalizeGuid(guid);
          if (normalizedGuid) {
            entries.push({ id: normalizedGuid, name: resolveGuidLabel(normalizedGuid) });
          }
        }
        for (const name of names || []) {
          const cleanedName = cleanCallParticipantName(name);
          if (cleanedName) entries.push({ id: "", name: cleanedName });
        }
      }

      const unique = [];
      const seen = new Set();
      for (const entry of entries) {
        const key = participantEntryKey(entry);
        if (!key || seen.has(key)) continue;
        seen.add(key);
        unique.push({
          id: normalizeGuid(entry.id || ""),
          name: cleanCallParticipantName(entry.name || (entry.id ? personNameForGuid(entry.id) : "")),
        });
      }
      return unique;
    }

    function hiddenEntryMeta(entries, noun = "members") {
      const normalized = normalizeParticipantList(entries);
      const visibleEntries = sortParticipantEntries(normalized.filter(entry => !entry.hidden));
      const hiddenEntries = sortParticipantEntries(normalized.filter(entry => entry.hidden));
      const count = hiddenEntries.length;
      const singular = noun.replace(/s$/, "");
      return {
        count,
        label: count ? `${count} hidden ${count === 1 ? singular : noun}` : "",
        visibleEntries,
        hiddenEntries,
      };
    }

    function previewLabelForEntries(prefix, entries, noun = "members") {
      const meta = hiddenEntryMeta(entries, noun);
      const visibleLabels = meta.visibleEntries.map(entry => normalizeTextValue(entry.label || entry.name || ""));
      if (visibleLabels.length === 1 && meta.count === 0) return `${prefix}: ${visibleLabels[0]}`;
      if (visibleLabels.length > 1 && meta.count === 0) return `${prefix}: ${visibleLabels.length} ${noun}`;
      if (!visibleLabels.length && meta.count === 1) return `${prefix}: Hidden`;
      if (!visibleLabels.length && meta.count > 1) return `${prefix}: ${meta.label}`;
      return `${prefix}: ${visibleLabels.length + meta.count} ${noun}`;
    }

    function callEventParticipantEntries(message, linkedCall = findLinkedCall(message)) {
      const raw = message.content_text || "";
      const participants = collectEventParticipants(message);
      return linkedCall
        ? callParticipantEntries(linkedCall)
        : buildParticipantEntries(extractGuids(raw), participants.map(name => normalizeTextValue(name)));
    }

    function messageHiddenMeta(message) {
      if (MESSAGE_HIDDEN_META_CACHE.has(message)) {
        return MESSAGE_HIDDEN_META_CACHE.get(message);
      }
      let value = null;
      const sourceThread = message && message.__thread_id ? THREAD_BY_ID.get(message.__thread_id) : null;
      if (message.synthetic_call || message.message_type === "Event/Call") {
        const entries = callEventParticipantEntries(message);
        const meta = hiddenEntryMeta(entries, "participants");
        value = meta.count ? {
          count: meta.count,
          label: meta.label,
          noun: "participants",
          previewLabel: previewLabelForEntries("Call event", entries, "participants"),
        } : null;
      } else if (message.message_type === "ThreadActivity/AddMember") {
        const parsed = parseAddMemberEvent(message);
        const entries = buildThreadScopedParticipantEntries(sourceThread, parsed.addedIds, parsed.addedNames);
        const meta = hiddenEntryMeta(entries, "members");
        value = {
          count: meta.count,
          label: meta.label,
          noun: "members",
          previewLabel: previewLabelForEntries("Member added", entries, "members"),
        };
      } else if (message.message_type === "ThreadActivity/MemberJoined") {
        const parsed = parseMemberJoinedEvent(message);
        const entries = buildThreadScopedParticipantEntries(sourceThread, parsed.joinedIds, parsed.joinedNames);
        const meta = hiddenEntryMeta(entries, "members");
        value = {
          count: meta.count,
          label: meta.label,
          noun: "members",
          previewLabel: previewLabelForEntries("Member joined", entries, "members"),
        };
      } else if (message.message_type === "ThreadActivity/DeleteMember") {
        const parsed = parseDeleteMemberEvent(message);
        const entries = buildThreadScopedParticipantEntries(sourceThread, parsed.removedIds, parsed.removedNames, { forceHidden: true });
        const meta = hiddenEntryMeta(entries, "members");
        value = {
          count: meta.count,
          label: meta.label,
          noun: "members",
          previewLabel: previewLabelForEntries("Member removed", entries, "members"),
        };
      }
      MESSAGE_HIDDEN_META_CACHE.set(message, value);
      return value;
    }

    function displayMessageType(message) {
      if (message.message_type === "ThreadActivity/AddMember") return "Member Added";
      if (message.message_type === "ThreadActivity/MemberJoined") return "Member Joined";
      if (message.message_type === "ThreadActivity/DeleteMember") return "Member Removed";
      if (message.message_type === "ThreadActivity/TopicUpdate") return "Topic Updated";
      if (messageHasAttachments(message)) {
        if (message.content_text) return "Message + Attachment";
        return messageAttachmentPreview(message) || "Attachment";
      }
      return message.message_type || "";
    }

    function directChatThreadForPerson(entry) {
      const guid = normalizeGuid(entry && entry.id);
      const name = normalizeName(entry && entry.name);
      if ((guid && guid === CURRENT_USER_ID) || (name && name === CURRENT_USER_NAME)) return null;
      if (guid && DIRECT_CHAT_BY_GUID.has(guid)) {
        const thread = DIRECT_CHAT_BY_GUID.get(guid);
        if (!state.threadId || thread.id !== state.threadId) return thread;
      }
      if (name && DIRECT_CHAT_BY_NAME.has(name)) {
        const thread = DIRECT_CHAT_BY_NAME.get(name);
        if (!state.threadId || thread.id !== state.threadId) return thread;
      }
      return null;
    }

    function sortParticipantEntries(entries) {
      return entries.slice().sort((left, right) => {
        const leftLabel = normalizeTextValue(left.label || left.name || left.id || "").toLowerCase();
        const rightLabel = normalizeTextValue(right.label || right.name || right.id || "").toLowerCase();
        return leftLabel.localeCompare(rightLabel);
      });
    }

    function normalizeParticipantList(values) {
      const items = [];
      const seenIds = new Set();
      const seenNames = new Set();
      for (const value of values || []) {
        const entry = value && typeof value === "object" && !Array.isArray(value)
          ? {
              id: normalizeGuid(value.id || value.guid || value.userId || ""),
              name: cleanCallParticipantName(value.name || value.display_name || value.displayName || ""),
              label: cleanCallParticipantName(value.label || value.friendlyname || ""),
              hidden: Boolean(value.hidden),
            }
          : {
              id: "",
              name: cleanCallParticipantName(value),
              label: "",
              hidden: false,
            };
        const guid = normalizeGuid(entry.id);
        const resolvedName = cleanCallParticipantName(entry.name || (guid ? personNameForGuid(guid) : ""));
        const explicitHidden = Boolean(entry.hidden);
        const visibleLabel = !explicitHidden && resolvedName && !looksLikeGuid(resolvedName) ? resolvedName : "";
        const hiddenLabel = normalizeTextValue(entry.label || resolvedName || guid || entry.name || "");
        const entryIdKey = guid || "";
        const visibleKey = normalizeName(visibleLabel);
        const hiddenKey = normalizeName(hiddenLabel);
        if (visibleLabel) {
          if (entryIdKey && seenIds.has(entryIdKey)) continue;
          if (visibleKey && seenNames.has(visibleKey)) continue;
          if (entryIdKey) seenIds.add(entryIdKey);
          if (visibleKey) seenNames.add(visibleKey);
          items.push({
            id: guid,
            name: visibleLabel,
            label: visibleLabel,
            hidden: false,
          });
          continue;
        }
        if (!hiddenLabel) continue;
        if (entryIdKey && seenIds.has(entryIdKey)) continue;
        if (!entryIdKey && hiddenKey && seenNames.has(hiddenKey)) continue;
        if (entryIdKey) seenIds.add(entryIdKey);
        if (hiddenKey) seenNames.add(hiddenKey);
        items.push({
          id: guid,
          name: "",
          label: hiddenLabel,
          hidden: true,
        });
      }
      return items;
    }

    function renderHiddenEntries(entries, summaryLabel = "Show Hidden Data") {
      const hiddenEntries = sortParticipantEntries(entries.filter(entry => entry.hidden));
      if (!hiddenEntries.length) return "";
      return `
        <details class="raw-event hidden-data" ${state.expandHiddenData ? "open" : ""}>
          <summary>${escapeHtml(`${summaryLabel} (${hiddenEntries.length})`)}</summary>
          <div class="chips">
            ${hiddenEntries.map(entry => `<span class="chip participant-chip participant-chip-static">${escapeHtml(entry.label)}</span>`).join("")}
          </div>
        </details>
      `;
    }

    function renderExpandableChipGroup(values, options = {}) {
      const entries = normalizeParticipantList(values);
      const visibleEntries = sortParticipantEntries(entries.filter(entry => !entry.hidden));
      const hiddenDetails = renderHiddenEntries(entries, options.hiddenSummaryLabel || "Show Hidden Data");
      if (!visibleEntries.length) {
        return `
          <div class="expandable-shell">
            <div class="subtle">${escapeHtml(options.emptyLabel || "No visible people listed.")}</div>
            ${hiddenDetails}
          </div>
        `;
      }
      return `
        <div class="expandable-shell">
          <div class="chips expandable-list collapsed" data-expandable-list>
            ${visibleEntries.map(entry => {
              const chatThread = options.enableChatLinks === false ? null : directChatThreadForPerson(entry);
              const label = normalizeTextValue(entry.label || entry.name || "");
              if (chatThread) {
                return `<button type="button" class="chip participant-chip participant-chip-link open-participant-chat" data-thread-id="${escapeHtml(chatThread.id)}" data-label="${escapeHtml(label)}">${escapeHtml(label)}</button>`;
              }
              return `<span class="chip participant-chip participant-chip-static">${escapeHtml(label)}</span>`;
            }).join("")}
          </div>
          <button
            type="button"
            class="call-link toggle-expandable-list hidden"
            data-expand-label="${escapeHtml(options.expandLabel || "Expand")}"
            data-collapse-label="${escapeHtml(options.collapseLabel || "Collapse")}"
          >${escapeHtml(options.expandLabel || "Expand")}</button>
          ${hiddenDetails}
        </div>
      `;
    }

    function initExpandableLists(scope) {
      for (const shell of scope.querySelectorAll(".expandable-shell")) {
        const list = shell.querySelector("[data-expandable-list]");
        const button = shell.querySelector(".toggle-expandable-list");
        if (!list || !button) continue;

        list.classList.remove("expanded");
        list.classList.add("collapsed");
        const needsToggle = list.scrollHeight > list.clientHeight + 4;
        button.classList.toggle("hidden", !needsToggle);
        if (!needsToggle) {
          list.classList.remove("collapsed");
          continue;
        }

        const updateButtonText = () => {
          button.textContent = list.classList.contains("expanded")
            ? (button.dataset.collapseLabel || "Collapse")
            : (button.dataset.expandLabel || "Expand");
        };
        updateButtonText();
        button.addEventListener("click", () => {
          const expanded = list.classList.toggle("expanded");
          list.classList.toggle("collapsed", !expanded);
          updateButtonText();
        });
      }
    }

    function initParticipantChatLinks(scope) {
      for (const element of scope.querySelectorAll(".open-participant-chat")) {
        element.addEventListener("click", () => {
          openThreadView({
            threadId: element.dataset.threadId,
            clearSearch: true,
            clearCategory: true,
            revealInSidebar: true,
            scrollTop: true,
          });
        });
      }
    }

    function initAttachmentActions(scope) {
      for (const element of scope.querySelectorAll(".copy-attachment-link")) {
        element.addEventListener("click", () => copyText(element.dataset.url || "", "Attachment link copied"));
      }
    }

    function parseAddMemberEvent(message) {
      const unique = [];
      for (const guid of extractGuids(message.content_text || "")) {
        if (!unique.includes(guid)) unique.push(guid);
      }

      const senderId = String(message.sender_id || "").toLowerCase();
      const actorId = senderId || unique[0] || "";
      const actorName = normalizeTextValue(message.sender_display_name || personNameForGuid(actorId) || "");
      const addedIds = unique.filter(guid => guid !== actorId);
      const addedNames = addedIds.map(personNameForGuid);

      return {
        actorId,
        actorName,
        addedIds,
        addedNames,
      };
    }

    function parseMemberJoinedEvent(message) {
      const payload = parseJsonObject(message.content_text || "");
      const actorId = normalizeGuid(payload && payload.initiator);
      const actorName = normalizeTextValue(
        message.sender_display_name ||
        personNameForGuid(actorId) ||
        ""
      );
      const members = resolveMemberEntries(payload && payload.members);
      return {
        actorId,
        actorName,
        joinedIds: members.memberIds,
        joinedNames: members.memberNames,
      };
    }

    function parseDeleteMemberEvent(message) {
      const actorId = normalizeGuid(message.sender_id || extractGuids(message.content_text || "")[0] || "");
      const actorName = normalizeTextValue(
        message.sender_display_name ||
        personNameForGuid(actorId) ||
        ""
      );
      let removedIds = dedupe(extractGuids(message.content_text || "").map(normalizeGuid).filter(Boolean));
      if (actorId) {
        const filtered = removedIds.filter(id => id !== actorId);
        if (filtered.length) removedIds = filtered;
      }
      const removedNames = dedupe(removedIds.map(personNameForGuid).filter(Boolean));
      return {
        actorId,
        actorName,
        removedIds,
        removedNames,
      };
    }

    function threadActivityXmlValue(message, tagName) {
      const pattern = new RegExp(`<${tagName}>([\\s\\S]*?)</${tagName}>`, "i");
      const match = String(message && message.content_html || "").match(pattern);
      return cleanCallParticipantName(match && match[1] ? match[1] : "");
    }

    function parseTopicUpdateEvent(message) {
      const actorId = normalizeGuid(
        threadActivityXmlValue(message, "initiator") ||
        extractGuids(message.content_text || "")[0] ||
        message.sender_id ||
        ""
      );
      const actorName = normalizeTextValue(
        message.sender_display_name ||
        personNameForGuid(actorId) ||
        ""
      );
      let topic = normalizeTextValue(threadActivityXmlValue(message, "value") || "");
      if (!topic) {
        const rawText = normalizeTextValue(message.content_text || "");
        const match = rawText.match(/^\\d+\\s+(?:8:orgid:)?[0-9a-f-]{36}\\s+(.+)$/i);
        topic = normalizeTextValue(match ? match[1] : rawText);
      }
      return {
        actorId,
        actorName,
        topic,
      };
    }

    function isMembershipEvent(message) {
      return [
        "ThreadActivity/AddMember",
        "ThreadActivity/MemberJoined",
        "ThreadActivity/DeleteMember",
      ].includes(message.message_type);
    }

    function isStructuredThreadActivityEvent(message) {
      return [
        "ThreadActivity/AddMember",
        "ThreadActivity/MemberJoined",
        "ThreadActivity/DeleteMember",
        "ThreadActivity/TopicUpdate",
      ].includes(message.message_type);
    }

    function renderMembershipNamesBlock(label, values, emptyLabel = "No people listed.") {
      return `
        <div class="call-event-block wide">
          <div class="k">${escapeHtml(label)}</div>
          ${renderExpandableChipGroup(values, { emptyLabel })}
        </div>
      `;
    }

    function renderThreadActorBlock(thread, ids = [], names = [], emptyLabel = "No actor was resolved.") {
      const actorEntries = buildThreadScopedParticipantEntries(thread, ids, names);
      const hasSource = (ids || []).some(Boolean) || (names || []).some(Boolean);
      if (!hasSource && !actorEntries.length) {
        return `<div class="call-event-block"><div class="k">Actor</div><div>${escapeHtml(emptyLabel)}</div></div>`;
      }
      return `
        <div class="call-event-block">
          <div class="k">Actor</div>
          ${renderExpandableChipGroup(actorEntries, {
            emptyLabel,
            enableChatLinks: ["team_chat", "thread"].includes(thread.category),
          })}
        </div>
      `;
    }

    function renderAddMemberEventBody(message, thread) {
      const parsed = parseAddMemberEvent(message);
      const addedEntries = buildThreadScopedParticipantEntries(thread, parsed.addedIds, parsed.addedNames);
      const addedCount = parsed.addedIds.length;
      const cardHtml = `
        <div class="call-event" style="--call-bg:#e4e8ed;--call-outline:#66727f;--call-block-bg:#f4f6f8;--call-title:#3e4852;">
          <div class="call-event-header">
            <div class="call-event-title">${escapeHtml(addedCount > 1 ? "Members Added" : "Member Added")}</div>
          </div>
          <div class="call-event-grid">
            ${renderThreadActorBlock(thread, parsed.actorId ? [parsed.actorId] : [], parsed.actorName ? [parsed.actorName] : [])}
            <div class="call-event-block"><div class="k">Added Count</div><div>${escapeHtml(String(addedCount || 0))}</div></div>
            <div class="call-event-block"><div class="k">Current Conversation</div><div>${escapeHtml(threadDisplayLabel(thread))}</div></div>
            ${renderMembershipNamesBlock("Added", addedEntries, "No added members were resolved.")}
          </div>
        </div>
      `;
      return cardHtml;
    }

    function renderMemberJoinedEventBody(message, thread) {
      const parsed = parseMemberJoinedEvent(message);
      const joinedEntries = buildThreadScopedParticipantEntries(thread, parsed.joinedIds, parsed.joinedNames);
      const joinedCount = parsed.joinedIds.length;
      const cardHtml = `
        <div class="call-event" style="--call-bg:#e4f0e9;--call-outline:#5b7f69;--call-block-bg:#f5faf7;--call-title:#2f5e40;">
          <div class="call-event-header">
            <div class="call-event-title">${escapeHtml(joinedCount > 1 ? "Members Joined" : "Member Joined")}</div>
          </div>
          <div class="call-event-grid">
            ${renderThreadActorBlock(thread, parsed.actorId ? [parsed.actorId] : [], parsed.actorName ? [parsed.actorName] : [])}
            <div class="call-event-block"><div class="k">Joined Count</div><div>${escapeHtml(String(joinedCount || 0))}</div></div>
            <div class="call-event-block"><div class="k">Current Conversation</div><div>${escapeHtml(threadDisplayLabel(thread))}</div></div>
            ${renderMembershipNamesBlock("Joined", joinedEntries, "No joined members were resolved.")}
          </div>
        </div>
      `;
      return cardHtml;
    }

    function renderDeleteMemberEventBody(message, thread) {
      const parsed = parseDeleteMemberEvent(message);
      const removedEntries = buildThreadScopedParticipantEntries(thread, parsed.removedIds, parsed.removedNames, { forceHidden: true });
      const removedCount = parsed.removedIds.length;
      const cardHtml = `
        <div class="call-event" style="--call-bg:#f6ece4;--call-outline:#9a6b52;--call-block-bg:#fff7f1;--call-title:#7c523b;">
          <div class="call-event-header">
            <div class="call-event-title">${escapeHtml(removedCount > 1 ? "Members Removed" : "Member Removed")}</div>
          </div>
          <div class="call-event-grid">
            ${renderThreadActorBlock(thread, parsed.actorId ? [parsed.actorId] : [], parsed.actorName ? [parsed.actorName] : [])}
            <div class="call-event-block"><div class="k">Removed Count</div><div>${escapeHtml(String(removedCount || 0))}</div></div>
            <div class="call-event-block"><div class="k">Current Conversation</div><div>${escapeHtml(threadDisplayLabel(thread))}</div></div>
            ${renderMembershipNamesBlock("Removed", removedEntries, "Removed members are hidden because they are no longer in the current roster.")}
          </div>
        </div>
      `;
      return cardHtml;
    }

    function renderTopicUpdateEventBody(message, thread) {
      const parsed = parseTopicUpdateEvent(message);
      const updatedTopic = normalizeTextValue(parsed.topic || threadDisplayLabel(thread) || thread.id || "");
      const cardHtml = `
        <div class="call-event" style="--call-bg:#e9edf9;--call-outline:#5a6d9d;--call-block-bg:#f6f8ff;--call-title:#334778;">
          <div class="call-event-header">
            <div class="call-event-title">Topic Updated</div>
          </div>
          <div class="call-event-grid">
            ${renderThreadActorBlock(thread, parsed.actorId ? [parsed.actorId] : [], parsed.actorName ? [parsed.actorName] : [])}
            <div class="call-event-block"><div class="k">Updated Topic</div><div>${escapeHtml(updatedTopic || "Unknown")}</div></div>
            <div class="call-event-block"><div class="k">Current Conversation</div><div>${escapeHtml(threadDisplayLabel(thread))}</div></div>
          </div>
        </div>
      `;
      return cardHtml;
    }

    function renderMembershipEventBody(message, thread) {
      if (message.message_type === "ThreadActivity/AddMember") return renderAddMemberEventBody(message, thread);
      if (message.message_type === "ThreadActivity/MemberJoined") return renderMemberJoinedEventBody(message, thread);
      if (message.message_type === "ThreadActivity/DeleteMember") return renderDeleteMemberEventBody(message, thread);
      if (message.message_type === "ThreadActivity/TopicUpdate") return renderTopicUpdateEventBody(message, thread);
      return `<div class="body">${escapeHtml(message.content_text || "")}</div>`;
    }

    function linkedThreadsForCall(call) {
      const ids = [call.call_id, call.shared_correlation_id]
        .filter(Boolean)
        .map(value => String(value).toLowerCase());
      const targetKey = callKey(call);
      const matches = [];
      for (const thread of DATA.threads || []) {
        if (!thread || thread.category === "call_logs" || String(thread.id || "").toLowerCase() === "48:calllogs") continue;
        const directConversationMatch =
          call.conversation_id &&
          call.conversation_id !== "48:calllogs" &&
          String(thread.id || "").toLowerCase() === String(call.conversation_id || "").toLowerCase();
        const messageMatch = (thread.messages || []).some(message => {
          const linkedKey = messageLinkedCallKey(message);
          if (linkedKey && linkedKey === targetKey) return true;
          const text = String(message.content_text || "").toLowerCase();
          return ids.some(id => id && text.includes(id));
        });
        const syntheticMatch = syntheticCallsForThread(thread).some(candidate => callKey(candidate) === targetKey);
        if ((directConversationMatch || messageMatch || syntheticMatch) && !matches.some(existing => existing.id === thread.id)) {
          matches.push(thread);
        }
      }
      return matches.sort((left, right) => {
        const leftDirect = String(left.id || "").toLowerCase() === String(call.conversation_id || "").toLowerCase() ? 1 : 0;
        const rightDirect = String(right.id || "").toLowerCase() === String(call.conversation_id || "").toLowerCase() ? 1 : 0;
        if (rightDirect !== leftDirect) return rightDirect - leftDirect;
        return threadLastTimestamp(right) - threadLastTimestamp(left);
      });
    }

    function preferredThreadsForCall(call) {
      const key = callKey(call);
      if (PREFERRED_THREADS_BY_CALL_KEY.has(key)) return PREFERRED_THREADS_BY_CALL_KEY.get(key);
      const matches = linkedThreadsForCall(call);
      const directPairKeys = new Set(
        matches
          .filter(thread => thread.category === "chat_space" && (thread.participants || []).length === 2)
          .map(thread => participantNamePairKey(thread.participants || []))
          .filter(Boolean)
      );
      const filtered = matches.filter(thread => {
        const pairKey = participantNamePairKey(thread.participants || []);
        if (!pairKey || !directPairKeys.has(pairKey)) return true;
        return thread.category === "chat_space";
      });
      PREFERRED_THREADS_BY_CALL_KEY.set(key, filtered);
      return filtered;
    }

    function callJumpTargets(call) {
      const key = callKey(call);
      if (CALL_JUMP_TARGETS_BY_CALL_KEY.has(key)) return CALL_JUMP_TARGETS_BY_CALL_KEY.get(key);
      const targets = [];
      const targetKey = callKey(call);
      for (const thread of preferredThreadsForCall(call)) {
        const hasEventTarget = threadTimelineItems(thread).some(message => messageLinkedCallKey(message) === targetKey);
        const hasMessageTarget = hasNearbyCuratedMessages(thread, call);
        const focusTimestamp = call.start_time || call.end_time || "";
        if (hasMessageTarget || hasEventTarget) {
          targets.push({
            thread,
            focusTimestamp,
            focusCallKey: hasEventTarget ? targetKey : "",
            viewFilter: "all",
          });
        }
      }
      const seen = new Set();
      const filtered = targets.filter(target => {
        const key = `${target.thread.id}|${target.viewFilter}`;
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
      });
      CALL_JUMP_TARGETS_BY_CALL_KEY.set(key, filtered);
      return filtered;
    }

    function callJumpLabel(target) {
      const name = threadDisplayLabel(target.thread);
      const when = fmt(target.focusTimestamp);
      return when && when !== "[no_time]" ? `${name} [${when}]` : name;
    }

    function attachmentNameFromUrl(value) {
      const text = String(value || "").trim();
      if (!text) return "";
      try {
        const parsed = new URL(text);
        const parts = parsed.pathname.split("/").filter(Boolean);
        return decodeURIComponent(parts[parts.length - 1] || "").trim();
      } catch {
        return "";
      }
    }

    function attachmentExtension(value) {
      const text = normalizeTextValue(value || "").trim().toLowerCase();
      if (!text) return "";
      const target = text.includes(".") ? text : attachmentNameFromUrl(text).toLowerCase();
      const match = target.match(/\\.([a-z0-9]{2,6})(?:$|[?#])/i);
      return match ? match[1].toLowerCase() : "";
    }

    function normalizeAttachmentKind(value, name = "", url = "") {
      const raw = String(value || "").trim().toLowerCase();
      const ext = attachmentExtension(name) || attachmentExtension(url);
      if (["image", "amsimage", "inlineimage", "jpg", "jpeg", "png", "gif", "bmp", "webp", "heic", "heif", "tif", "tiff"].includes(raw) || ["jpg", "jpeg", "png", "gif", "bmp", "webp", "heic", "heif", "tif", "tiff"].includes(ext)) {
        return "image";
      }
      if (["video", "amsvideo", "mp4", "mov", "avi", "wmv", "m4v", "webm"].includes(raw) || ["mp4", "mov", "avi", "wmv", "m4v", "webm"].includes(ext)) {
        return "video";
      }
      return "file";
    }

    function attachmentKindLabel(kind) {
      const normalized = normalizeAttachmentKind(kind);
      if (normalized === "image") return "Photo";
      if (normalized === "video") return "Video";
      return "File";
    }

    function attachmentHost(url) {
      const value = String(url || "").trim();
      if (!value) return "";
      try {
        return new URL(value).hostname.toLowerCase();
      } catch (error) {
        return "";
      }
    }

    function attachmentSourceLabel(attachment) {
      const host = attachmentHost(attachment.url || attachment.preview_url || "");
      if (!host) return "Remote attachment";
      if (host.includes("api.ams.") || host.includes(".teams.microsoft.com")) return "Teams media";
      if (host.includes("sharepoint.com")) return "SharePoint";
      if (host.includes("onedrive.live.com")) return "OneDrive";
      return "Remote attachment";
    }

    function attachmentActionLabel(attachment) {
      const kindLabel = attachmentKindLabel(attachment.kind);
      const sourceLabel = attachmentSourceLabel(attachment);
      if (sourceLabel === "Teams media") {
        if (kindLabel === "Photo") return "Open Secure Photo";
        if (kindLabel === "Video") return "Open Secure Video";
        return "Open Secure File";
      }
      if (sourceLabel === "SharePoint") return kindLabel === "File" ? "Open SharePoint File" : `Open SharePoint ${kindLabel}`;
      if (sourceLabel === "OneDrive") return kindLabel === "File" ? "Open OneDrive File" : `Open OneDrive ${kindLabel}`;
      if (kindLabel === "Photo") return "Open Remote Photo";
      if (kindLabel === "Video") return "Open Remote Video";
      return "Open Remote File";
    }

    function attachmentAccessNote(attachment) {
      const sourceLabel = attachmentSourceLabel(attachment);
      if (!String(attachment.url || attachment.preview_url || "").trim()) {
        return "No recoverable attachment link was found in the export.";
      }
      if (sourceLabel === "Teams media") {
        return "Teams media link. Microsoft sign-in may be required.";
      }
      if (sourceLabel === "SharePoint") {
        return "SharePoint link. Microsoft sign-in may be required.";
      }
      if (sourceLabel === "OneDrive") {
        return "OneDrive link. Microsoft sign-in may be required.";
      }
      return "Remote attachment link. Authentication may be required.";
    }

    function normalizeAttachmentRecord(value) {
      if (!value || typeof value !== "object") return null;
      const url = String(value.url || "").trim();
      const previewUrl = String(value.preview_url || value.previewUrl || "").trim();
      const name = normalizeTextValue(value.name || "") || attachmentNameFromUrl(url || previewUrl) || attachmentKindLabel(value.kind || "file");
      const kind = normalizeAttachmentKind(value.kind, name, url || previewUrl);
      if (!url && !previewUrl) return null;
      return {
        id: String(value.id || "").trim(),
        name,
        url,
        preview_url: previewUrl,
        kind,
      };
    }

    function extractAttachmentsFromHtml(contentHtml) {
      const html = String(contentHtml || "").trim();
      if (!html) return [];
      const doc = new DOMParser().parseFromString(html, "text/html");
      const attachments = [];
      const seen = new Set();

      function addAttachment(record) {
        const normalized = normalizeAttachmentRecord(record);
        if (!normalized) return;
        const key = [normalized.id, normalized.url, normalized.preview_url, normalized.name].join("|");
        if (seen.has(key)) return;
        seen.add(key);
        attachments.push(normalized);
      }

      for (const node of doc.querySelectorAll("img[src]")) {
        const itemtype = String(node.getAttribute("itemtype") || "").toLowerCase();
        if (itemtype.includes("emoji")) continue;
        if (!(itemtype.includes("amsimage") || itemtype.includes("inlineimage") || itemtype.includes("amsvideo"))) continue;
        const src = String(node.getAttribute("src") || "").trim();
        addAttachment({
          id: node.getAttribute("itemid") || node.getAttribute("id") || "",
          name: node.getAttribute("alt") || node.getAttribute("title") || "",
          url: src,
          preview_url: src,
          kind: itemtype,
        });
      }

      for (const node of doc.querySelectorAll("a[href]")) {
        const itemtype = String(node.getAttribute("itemtype") || "").toLowerCase();
        if (!(itemtype.includes("hyperlink/files") || itemtype.includes("fileshyperlink"))) continue;
        const href = String(node.getAttribute("href") || "").trim();
        addAttachment({
          name: normalizeTextValue(node.textContent || "") || node.getAttribute("title") || "",
          url: href,
          kind: itemtype,
        });
      }
      return attachments;
    }

    function messageAttachments(message) {
      if (!message || typeof message !== "object") return [];
      if (MESSAGE_ATTACHMENT_CACHE.has(message)) return MESSAGE_ATTACHMENT_CACHE.get(message);
      const base = (message.attachments || [])
        .map(normalizeAttachmentRecord)
        .filter(Boolean);
      const htmlFallback = [];
      if (!base.length) {
        const rawHtml = String(message.content_html || "");
        if (rawHtml && (rawHtml.includes("itemtype=") || rawHtml.includes("<img") || rawHtml.includes("<a"))) {
          htmlFallback.push(...extractAttachmentsFromHtml(rawHtml));
        }
      }
      const combined = [];
      const seen = new Set();
      for (const record of [...base, ...htmlFallback]) {
        const key = [record.id, record.url, record.preview_url, record.name].join("|");
        if (seen.has(key)) continue;
        seen.add(key);
        combined.push(record);
      }
      MESSAGE_ATTACHMENT_CACHE.set(message, combined);
      return combined;
    }

    function messageHasAttachments(message) {
      return messageAttachments(message).length > 0;
    }

    function messageAttachmentPreview(message) {
      const attachments = messageAttachments(message);
      if (!attachments.length) return "";
      if (attachments.length === 1) {
        const attachment = attachments[0];
        const kind = attachmentKindLabel(attachment.kind);
        if (attachment.name && attachment.name !== kind) {
          return `${kind}: ${attachment.name}`;
        }
        return `${kind} attachment`;
      }
      return `${attachments.length} attachments`;
    }

    function renderAttachmentCards(message) {
      const attachments = messageAttachments(message);
      if (!attachments.length) return "";
      return `
        <div class="attachment-stack">
          ${attachments.map(attachment => {
            const openUrl = attachment.url || attachment.preview_url || "";
            const kindLabel = attachmentKindLabel(attachment.kind);
            const actionLabel = attachmentActionLabel(attachment);
            const accessNote = attachmentAccessNote(attachment);
            return `
              <div class="attachment-card">
                <div class="attachment-meta">
                  <div>
                    <div class="attachment-kind">${escapeHtml(kindLabel)} Attachment</div>
                    <div class="attachment-name">${escapeHtml(attachment.name || `${kindLabel} attachment`)}</div>
                    ${accessNote ? `<div class="attachment-note">${escapeHtml(accessNote)}</div>` : ``}
                  </div>
                  ${openUrl ? `<div class="attachment-actions"><a class="call-link" href="${escapeHtml(openUrl)}" target="_blank" rel="noopener">${escapeHtml(actionLabel)}</a><button type="button" class="call-link copy-attachment-link" data-url="${escapeHtml(openUrl)}">Copy Link</button></div>` : ``}
                </div>
              </div>
            `;
          }).join("")}
        </div>
      `;
    }

    function extractHtmlText(node) {
      if (!node) return "";
      if (node.nodeType === Node.TEXT_NODE) {
        return node.textContent || "";
      }
      if (node.nodeType !== Node.ELEMENT_NODE) {
        return "";
      }

      const tagName = String(node.tagName || "").toLowerCase();
      if (tagName === "br") {
        return "\\n";
      }

      let text = "";
      for (const child of node.childNodes || []) {
        text += extractHtmlText(child);
      }

      if (["p", "div", "li", "blockquote"].includes(tagName)) {
        text += "\\n";
      }
      return text;
    }

    function normalizeStructuredText(value) {
      return String(value ?? "")
        .replace(/\\u00a0/g, " ")
        .replace(/[ \\t]+\\n/g, "\\n")
        .replace(/\\n[ \\t]+/g, "\\n")
        .replace(/\\n{3,}/g, "\\n\\n")
        .replace(/[ \\t]{2,}/g, " ")
        .trim();
    }

    function messageReplyQuote(message) {
      if (!message || typeof message !== "object") return null;
      if (MESSAGE_REPLY_QUOTE_CACHE.has(message)) return MESSAGE_REPLY_QUOTE_CACHE.get(message);

      const rawHtml = String(message.content_html || "").trim();
      if (!rawHtml || !rawHtml.toLowerCase().includes("schema.skype.com/reply")) {
        MESSAGE_REPLY_QUOTE_CACHE.set(message, null);
        return null;
      }

      let parsed = null;
      try {
        const doc = new DOMParser().parseFromString(rawHtml, "text/html");
        const blockquote = [...doc.querySelectorAll("blockquote[itemtype]")]
          .find(node => String(node.getAttribute("itemtype") || "").toLowerCase().includes("schema.skype.com/reply"));
        if (!blockquote) {
          MESSAGE_REPLY_QUOTE_CACHE.set(message, null);
          return null;
        }

        const author = normalizeTextValue(
          (blockquote.querySelector("[itemprop='mri']") || {}).textContent || ""
        );
        const preview = normalizeStructuredText(
          (blockquote.querySelector("[itemprop='preview']") || {}).textContent || ""
        );
        const quotedMessageId = normalizeTextValue(blockquote.getAttribute("itemid") || "");
        blockquote.remove();
        const replyText = normalizeStructuredText(extractHtmlText(doc.body));

        parsed = {
          author,
          preview,
          quoted_message_id: quotedMessageId,
          reply_text: replyText,
        };
        if (!parsed.author && !parsed.preview && !parsed.reply_text) {
          parsed = null;
        }
      } catch {
        parsed = null;
      }

      MESSAGE_REPLY_QUOTE_CACHE.set(message, parsed);
      return parsed;
    }

    const REACTION_EMOJI_MAP = Object.freeze({
      like: "👍",
      heart: "❤️",
      laugh: "😂",
      rofl: "🤣",
      surprised: "😮",
      cry: "😢",
      angry: "😡",
      fire: "🔥",
      hug: "🤗",
      think: "🤔",
      cool: "😎",
      worry: "😟",
      party: "🥳",
      muscle: "💪",
      upsidedownface: "🙃",
      smilerobot: "🤖",
      crossedfingers: "🤞",
      pointupindex: "☝️",
      pinchedfingers: "🤌",
      fistbump: "👊",
      unamused: "😒",
      likewithfacemser: "👍",
      handsinair: "🙌",
      giggle: "🤭",
      hearteyes: "😍",
      plunger: "🪠",
      no: "👎",
      manfacepalming: "🤦‍♂️",
      starmser: "⭐",
      blankface: "😑",
      fingerheart: "🫰",
      bunnyhug: "🤗",
      rock: "🤘",
      shivering: "🥶",
      "yes-tone1": "👍🏻",
      "yes-tone2": "👍🏼",
      yes: "👍",
      poke: "👉",
      snegovik: "⛄",
      emo: "🙂",
    });

    const REACTION_LABEL_MAP = Object.freeze({
      like: "Like",
      heart: "Heart",
      laugh: "Laugh",
      rofl: "ROFL",
      surprised: "Surprised",
      cry: "Cry",
      angry: "Angry",
      fire: "Fire",
      hug: "Hug",
      think: "Think",
      cool: "Cool",
      worry: "Worry",
      party: "Party",
      muscle: "Muscle",
      upsidedownface: "Upside Down Face",
      smilerobot: "Smile Robot",
      crossedfingers: "Crossed Fingers",
      pointupindex: "Point Up",
      pinchedfingers: "Pinched Fingers",
      fistbump: "Fist Bump",
      unamused: "Unamused",
      likewithfacemser: "Like",
      handsinair: "Hands In Air",
      giggle: "Giggle",
      hearteyes: "Heart Eyes",
      plunger: "Plunger",
      no: "No",
      manfacepalming: "Facepalm",
      starmser: "Star",
      blankface: "Blank Face",
      fingerheart: "Finger Heart",
      bunnyhug: "Bunny Hug",
      rock: "Rock",
      shivering: "Shivering",
      "yes-tone1": "Thumbs Up",
      "yes-tone2": "Thumbs Up",
      yes: "Thumbs Up",
      poke: "Poke",
      snegovik: "Snowman",
      emo: "Emoji",
    });

    function reactionEmoji(key) {
      const normalizedKey = normalizeTextValue(key || "").toLowerCase();
      if (!normalizedKey) return "❔";
      if (REACTION_EMOJI_MAP[normalizedKey]) return REACTION_EMOJI_MAP[normalizedKey];
      const match = normalizedKey.match(/^([0-9a-f]{4,6}(?:-[0-9a-f]{4,6})*)(?:_|$)/i);
      if (match) {
        try {
          return match[1]
            .split("-")
            .map(value => String.fromCodePoint(Number.parseInt(value, 16)))
            .join("");
        } catch {
          return "❔";
        }
      }
      return "❔";
    }

    function reactionLabel(key) {
      const normalizedKey = normalizeTextValue(key || "").toLowerCase();
      if (!normalizedKey) return "Reaction";
      if (REACTION_LABEL_MAP[normalizedKey]) return REACTION_LABEL_MAP[normalizedKey];
      const withoutCodepoint = normalizedKey.replace(/^[0-9a-f]{4,6}(?:-[0-9a-f]{4,6})*_/i, "");
      const normalizedLabel = (withoutCodepoint || normalizedKey)
        .replace(/-tone\\d+/g, "")
        .replace(/mser$/i, "")
        .replace(/_/g, " ")
        .replace(/([a-z])([A-Z])/g, "$1 $2")
        .trim();
      return normalizedLabel
        ? normalizedLabel.replace(/\\b\\w/g, letter => letter.toUpperCase())
        : "Reaction";
    }

    function messageReactions(message) {
      if (!message || typeof message !== "object") return [];
      if (MESSAGE_REACTION_CACHE.has(message)) return MESSAGE_REACTION_CACHE.get(message);

      const normalized = [];
      for (const reaction of message.reactions || []) {
        if (!reaction || typeof reaction !== "object") continue;
        const key = normalizeTextValue(reaction.key || "").toLowerCase();
        if (!key) continue;
        const users = [];
        const seenUsers = new Set();
        for (const user of reaction.users || []) {
          const id = normalizeGuid(user && user.id || "");
          const displayName = normalizeTextValue(user && (user.display_name || (id ? personNameForGuid(id) : "")) || "");
          const reactedAt = normalizeTextValue(user && user.reacted_at || "");
          const identity = id || normalizeName(displayName) || reactedAt || `${key}:${users.length}`;
          if (seenUsers.has(identity)) continue;
          seenUsers.add(identity);
          users.push({
            id,
            display_name: displayName || (id ? personNameForGuid(id) : ""),
            reacted_at: reactedAt,
          });
        }
        const parsedCount = Number.parseInt(reaction.count, 10);
        const count = Number.isFinite(parsedCount) ? parsedCount : 0;
        normalized.push({
          key,
          emoji: reactionEmoji(key),
          label: reactionLabel(key),
          count: Math.max(count, users.length),
          users,
        });
      }

      normalized.sort((left, right) => right.count - left.count || left.label.localeCompare(right.label));
      MESSAGE_REACTION_CACHE.set(message, normalized);
      return normalized;
    }

    function renderMessageReactions(message, highlightQuery = "") {
      const reactions = messageReactions(message);
      if (!reactions.length) return "";

      const totalCount = reactions.reduce((sum, reaction) => sum + Math.max(reaction.count || 0, reaction.users.length || 0), 0);
      const emojiHtml = reactions.slice(0, 5)
        .map(reaction => `<span>${escapeHtml(reaction.emoji)}</span>`)
        .join("");
      const moreCount = reactions.length > 5 ? reactions.length - 5 : 0;
      const tooltipHtml = reactions.map(reaction => {
        const heading = `${reaction.emoji} ${reaction.label} ${reaction.count > 1 ? `· ${reaction.count}` : ""}`.trim();
        const headingHtml = highlightQuery
          ? highlightSearchHtml(heading, highlightQuery)
          : escapeHtml(heading);
        let rows = reaction.users.map(user => {
          const name = user.display_name || user.id || "Unknown user";
          const nameHtml = highlightQuery ? highlightSearchHtml(name, highlightQuery) : escapeHtml(name);
          return `<div class="reaction-tooltip-user"><span class="reaction-tooltip-emoji">${escapeHtml(reaction.emoji)}</span><span>${nameHtml}</span></div>`;
        }).join("");
        if (!rows) {
          rows = `<div class="reaction-tooltip-empty">${escapeHtml(`${reaction.count} reaction${reaction.count == 1 ? "" : "s"}`)}</div>`;
        }
        return `<div class="reaction-tooltip-group"><div class="reaction-tooltip-heading">${headingHtml}</div>${rows}</div>`;
      }).join("");

      return `
        <div class="reaction-bar">
          <div class="reaction-bubble" tabindex="0" aria-label="${escapeHtml(`${totalCount} reactions`)}">
            <span class="reaction-count">${escapeHtml(String(totalCount))}</span>
            <span class="reaction-icons">${emojiHtml}${moreCount ? `<span class="reaction-icon-more">+${escapeHtml(String(moreCount))}</span>` : ``}</span>
            <div class="reaction-tooltip">${tooltipHtml}</div>
          </div>
        </div>
      `;
    }

    function displayMessageQuality(message) {
      if (messageHasAttachments(message) && message.quality !== "event") return "attachment";
      return message.quality || "";
    }

    function messageDisplaySender(message) {
      if (message.message_type === "ThreadActivity/AddMember") {
        return systemEventActorLabel();
      }
      if (message.message_type === "ThreadActivity/MemberJoined") {
        return systemEventActorLabel();
      }
      if (message.message_type === "ThreadActivity/DeleteMember") {
        return systemEventActorLabel();
      }
      if (message.message_type === "ThreadActivity/TopicUpdate") {
        return systemEventActorLabel();
      }
      return normalizeTextValue(message.sender_display_name || message.sender_id || "Unknown");
    }

    function messagePassesFilter(message) {
      if (state.messageViewFilter === "messages") return !messageIsCallEvent(message) && !messageIsSystemEventRecord(message);
      if (state.messageViewFilter === "calls") return messageIsCallEvent(message);
      if (state.messageViewFilter === "events") return messageIsSystemEventRecord(message);
      return true;
    }

    function hasThreadDateRange() {
      return Boolean(state.threadDateFrom || state.threadDateTo);
    }

    function hasCallDateRange() {
      return Boolean(state.callDateFrom || state.callDateTo);
    }

    function dateBoundaryValue(value, isEnd) {
      if (!value) return null;
      const parsed = new Date(`${value}T${isEnd ? "23:59:59.999" : "00:00:00.000"}`);
      const time = parsed.getTime();
      return Number.isNaN(time) ? null : time;
    }

    function normalizedThreadDateRange() {
      const start = dateBoundaryValue(state.threadDateFrom, false);
      const end = dateBoundaryValue(state.threadDateTo, true);
      if (start === null && end === null) return { start: null, end: null };
      if (start !== null && end !== null && start > end) {
        return { start: end, end: start };
      }
      return { start, end };
    }

    function messagePassesThreadDateRange(message) {
      const { start, end } = normalizedThreadDateRange();
      if (start === null && end === null) return true;
      const current = timeValue(message.timestamp);
      if (!Number.isFinite(current)) return false;
      if (start !== null && current < start) return false;
      if (end !== null && current > end) return false;
      return true;
    }

    function messagePassesCombinedDateRange(message) {
      return messagePassesSidebarDateRange(message) && messagePassesThreadDateRange(message);
    }

    function clearAllMessageDateRanges() {
      state.messageDateFrom = "";
      state.messageDateTo = "";
      state.threadDateFrom = "";
      state.threadDateTo = "";
      if (messageDateFrom) messageDateFrom.value = "";
      if (messageDateTo) messageDateTo.value = "";
    }

    function hasMessageFilters() {
      return Boolean(
        state.messageSearch ||
        state.category ||
        state.messageDateFrom ||
        state.messageDateTo ||
        state.threadDateFrom ||
        state.threadDateTo ||
        (state.messageViewFilter && state.messageViewFilter !== "all")
      );
    }

    function clearMessageFilters() {
      clearMessageSearchState();
      state.category = "";
      clearAllMessageDateRanges();
      state.messageViewFilter = "all";
      state.focusMessageId = null;
      state.focusCallKey = null;
      state.focusTimestamp = null;
      state.focusSearchQuery = "";
    }

    function normalizedCallDateRange() {
      const start = dateBoundaryValue(state.callDateFrom, false);
      const end = dateBoundaryValue(state.callDateTo, true);
      if (start === null && end === null) return { start: null, end: null };
      if (start !== null && end !== null && start > end) {
        return { start: end, end: start };
      }
      return { start, end };
    }

    function callPassesDateRange(call) {
      const { start, end } = normalizedCallDateRange();
      if (start === null && end === null) return true;
      const current = timeValue(callPrimaryTimestamp(call));
      if (!Number.isFinite(current)) return false;
      if (start !== null && current < start) return false;
      if (end !== null && current > end) return false;
      return true;
    }

    function hasCallFilters() {
      return Boolean(
        state.callSearch ||
        state.callGroup ||
        state.callDirection ||
        state.callDateFrom ||
        state.callDateTo
      );
    }

    function clearCallFilters() {
      state.callSearch = "";
      state.callGroup = "";
      state.callDirection = "";
      state.callDateFrom = "";
      state.callDateTo = "";
      if (callSearch) callSearch.value = "";
      if (callGroupFilter) callGroupFilter.value = "";
      if (callDirectionFilter) callDirectionFilter.value = "";
      if (callDateFrom) callDateFrom.value = "";
      if (callDateTo) callDateTo.value = "";
    }

    function callSearchText(call) {
      const key = callKey(call);
      if (CALL_SEARCH_TEXT_CACHE.has(key)) return CALL_SEARCH_TEXT_CACHE.get(key);
      const participantEntries = callParticipantEntries(call);
      const parts = [
        callLabel(call),
        call.call_id,
        call.shared_correlation_id,
        displayCallDirection(call),
        displayCallDirectionLabel(call),
        displayCallState(call),
        displayCallStatus(call),
        displayCallGroupLabel(call),
        call.call_type,
        displayCallTypeLabel(call),
        displayCallQualityLabel(call),
        call.conversation_id,
        call.group_chat_thread_id,
        call.summary_text,
        call.meeting_subject,
        call.meeting_start_time,
        call.meeting_end_time,
        call.user_participation,
        callSideLabel(call, "originator"),
        call.originator_id,
        call.originator_endpoint,
        call.originator_phone_number,
        callSideLabel(call, "target"),
        call.target_id,
        call.target_endpoint,
        call.target_phone_number,
        ...participantEntries.map(entry => entry.label || entry.name || ""),
        ...participantEntries.map(entry => entry.id || ""),
      ];
      const value = parts.filter(Boolean).join(" ").toLowerCase();
      CALL_SEARCH_TEXT_CACHE.set(key, value);
      return value;
    }

    function callDuration(call) {
      let seconds = callDurationSeconds(call);
      if (seconds === null) return "";
      const hours = Math.floor(seconds / 3600);
      seconds -= hours * 3600;
      const minutes = Math.floor(seconds / 60);
      seconds -= minutes * 60;
      const parts = [];
      if (hours) parts.push(`${hours}h`);
      if (minutes || hours) parts.push(`${minutes}m`);
      parts.push(`${seconds}s`);
      return parts.join(" ");
    }

    function filteredCalls() {
      return DATA.calls
        .filter(call => {
          const query = String(state.callSearch || "").trim().toLowerCase();
          if (state.callGroup && callGroupKey(call) !== state.callGroup) {
            return false;
          }
          if (state.callDirection === "inbound") {
            if (displayCallDirection(call) !== "incoming") return false;
          } else if (state.callDirection === "outbound") {
            if (displayCallDirection(call) !== "outgoing") return false;
          } else if (state.callDirection === "declined") {
            const stateValue = displayCallState(call);
            if (stateValue !== "declined" && stateValue !== "rejected") return false;
          } else if (state.callDirection === "missed") {
            if (displayCallState(call) !== "missed") return false;
          }
          if (query && !callSearchText(call).includes(query)) {
            return false;
          }
          if (!callPassesDateRange(call)) {
            return false;
          }
          return true;
        })
        .sort((left, right) => callPrimaryTimestampValue(right) - callPrimaryTimestampValue(left));
    }

    function isCurrentUserIdentity(id, name) {
      const guid = normalizeGuid(id || "");
      const normalizedName = normalizeName(name || "");
      return Boolean(
        (CURRENT_USER_ID && guid && guid === CURRENT_USER_ID) ||
        (CURRENT_USER_NAME && normalizedName && normalizedName === CURRENT_USER_NAME)
      );
    }

    function isDiagnosticChatMessage(message) {
      return Boolean(
        message &&
        !messageIsCallEvent(message) &&
        !messageIsSystemEventRecord(message) &&
        Number.isFinite(timeValue(message.timestamp))
      );
    }

    function sortedChatMessagesAsc(thread) {
      return (thread.messages || [])
        .filter(isDiagnosticChatMessage)
        .slice()
        .sort((left, right) => {
          const timeDiff = timeValue(left.timestamp) - timeValue(right.timestamp);
          if (timeDiff !== 0) return timeDiff;
          return (left.id || "").localeCompare(right.id || "");
        });
    }

    function threadCounterpartyLabel(thread, message = null) {
      if (message && !isOwnMessage(message)) {
        return cleanCallParticipantName(message.sender_display_name || "") || "Originator";
      }
      const names = threadExternalParticipantNames(thread);
      if (names.length) return summarizeNames(names, 2);
      const fallback = threadDisplayLabel(thread);
      return fallback && !isPlaceholderThreadLabel(fallback) ? fallback : "Target";
    }

    function durationBetweenValues(startValue, endValue) {
      const start = timeValue(startValue);
      const end = timeValue(endValue);
      if (!Number.isFinite(start) || !Number.isFinite(end) || end < start) return null;
      return Math.round((end - start) / 1000);
    }

    function communicationDurationSeconds(call) {
      return durationBetweenValues(call.connect_time || call.start_time, call.end_time)
        ?? durationBetweenValues(call.start_time, call.end_time);
    }

    function acceptedCallDurationSeconds(call) {
      return isAcceptedCommunication(call) ? communicationDurationSeconds(call) : null;
    }

    function meetingDurationSeconds(call) {
      return durationBetweenValues(call.connect_time || call.meeting_start_time || call.start_time, call.end_time || call.meeting_end_time)
        ?? durationBetweenValues(call.meeting_start_time || call.start_time, call.meeting_end_time || call.end_time)
        ?? communicationDurationSeconds(call);
    }

    function formatDurationPrecise(totalSeconds, emptyLabel = "Unavailable") {
      if (!Number.isFinite(totalSeconds)) return emptyLabel;
      let seconds = Math.max(0, Math.round(totalSeconds));
      const hours = Math.floor(seconds / 3600);
      seconds -= hours * 3600;
      const minutes = Math.floor(seconds / 60);
      seconds -= minutes * 60;
      const parts = [];
      if (hours) parts.push(`${hours}h`);
      if (minutes || hours) parts.push(`${minutes}m`);
      if (!hours) parts.push(`${seconds}s`);
      return parts.join(" ") || "0s";
    }

    function formatDurationHoursMinutes(totalSeconds, emptyLabel = "Unavailable") {
      if (!Number.isFinite(totalSeconds)) return emptyLabel;
      const seconds = Math.max(0, Math.round(totalSeconds));
      const hours = Math.floor(seconds / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      if (hours) return `${hours}h ${minutes}m`;
      return `${minutes}m`;
    }

    function secondsStats(values) {
      const sorted = (values || [])
        .filter(value => Number.isFinite(value) && value >= 0)
        .slice()
        .sort((left, right) => left - right);
      if (!sorted.length) {
        return { count: 0, total: 0, average: null, median: null, min: null, max: null };
      }
      const total = sorted.reduce((sum, value) => sum + value, 0);
      const middle = Math.floor(sorted.length / 2);
      const median = sorted.length % 2 === 1
        ? sorted[middle]
        : ((sorted[middle - 1] + sorted[middle]) / 2);
      return {
        count: sorted.length,
        total,
        average: total / sorted.length,
        median,
        min: sorted[0],
        max: sorted[sorted.length - 1],
      };
    }

    function callActivityStartTimestamp(call) {
      return call.meeting_start_time || call.start_time || call.connect_time || call.end_time || "";
    }

    function callActivityEndTimestamp(call) {
      return call.end_time || call.meeting_end_time || call.connect_time || call.start_time || "";
    }

    function callOverlapsDate(call, dateKey) {
      const { start, end } = selectedDayRange(dateKey);
      if (start === null || end === null) return false;
      const callStart = timeValue(callActivityStartTimestamp(call));
      const callEnd = timeValue(callActivityEndTimestamp(call));
      if (!Number.isFinite(callStart) && !Number.isFinite(callEnd)) return false;
      const boundedStart = Number.isFinite(callStart) ? callStart : callEnd;
      const boundedEnd = Number.isFinite(callEnd) ? callEnd : callStart;
      return boundedStart <= end && boundedEnd >= start;
    }

    function isDeclinedCommunication(call) {
      const value = displayCallState(call);
      return value === "declined" || value === "rejected" || value === "cancelled";
    }

    function isMissedCommunication(call) {
      return displayCallState(call) === "missed";
    }

    function isAcceptedCommunication(call) {
      return !isMissedCommunication(call) && !isDeclinedCommunication(call) && Number.isFinite(communicationDurationSeconds(call));
    }

    function communicationOutcomeLabel(call) {
      if (isMissedCommunication(call)) return "Missed";
      if (isDeclinedCommunication(call)) return "Declined";
      if (isAcceptedCommunication(call)) return "Accepted";
      return displayCallStateLabel(call) || "Unknown";
    }

    function meetingStatusLabel(call) {
      const participation = meetingParticipation(call);
      if (participation === "joined") return "Attended";
      if (participation === "missed") return "Missed";
      return displayCallStateLabel(call) || "Scheduled";
    }

    function isAttendedMeeting(call) {
      return meetingParticipation(call) === "joined";
    }

    function isMissedMeeting(call) {
      return meetingParticipation(call) === "missed";
    }

    function callCounterpartyLabel(call) {
      const entries = normalizeParticipantList(callParticipantEntries(call))
        .filter(entry => !entry.hidden)
        .filter(entry => !isCurrentUserParticipantEntry(entry))
        .map(entry => normalizeTextValue(entry.label || entry.name || ""))
        .filter(Boolean);
      if (entries.length) return summarizeNames(entries, 2);
      if (displayCallDirection(call) === "outgoing") return callSideLabel(call, "target") || "Target";
      if (displayCallDirection(call) === "incoming") return callSideLabel(call, "originator") || "Originator";
      return normalizeTextValue(callLabel(call)) || "Participant";
    }

    function activityGroupFirstTime(group) {
      return Number.isFinite(group && group.firstTime) ? group.firstTime : Number.POSITIVE_INFINITY;
    }

    function compareActivityGroupsByFirstTimestamp(left, right) {
      const timeDiff = activityGroupFirstTime(left) - activityGroupFirstTime(right);
      if (timeDiff !== 0) return timeDiff;
      return String(left && left.label || "").localeCompare(String(right && right.label || ""));
    }

    function callParticipantMetricGroups(calls) {
      const groups = new Map();
      const ensure = label => {
        const key = normalizeTextValue(label || "Participant");
        if (!groups.has(key)) {
          groups.set(key, {
            label: key,
            accepted: 0,
            missed: 0,
            totalDuration: 0,
            total: 0,
            firstTimestamp: "",
            firstTime: Number.POSITIVE_INFINITY,
            firstCallKey: "",
          });
        }
        return groups.get(key);
      };
      for (const call of calls || []) {
        const group = ensure(callCounterpartyLabel(call));
        group.total += 1;
        const firstTimestamp = callActivityStartTimestamp(call);
        const firstTime = timeValue(firstTimestamp);
        if (Number.isFinite(firstTime) && firstTime < group.firstTime) {
          group.firstTimestamp = firstTimestamp;
          group.firstTime = firstTime;
          group.firstCallKey = callKey(call);
        }
        if (isAcceptedCommunication(call)) {
          group.accepted += 1;
          const duration = acceptedCallDurationSeconds(call);
          if (Number.isFinite(duration)) group.totalDuration += duration;
        }
        if (isMissedCommunication(call)) group.missed += 1;
      }
      return [...groups.values()].sort(compareActivityGroupsByFirstTimestamp);
    }

    function addActivityCount(map, dateKey, key, amount = 1, selfAmount = 0) {
      if (!dateKey) return;
      if (!map.has(dateKey)) {
        map.set(dateKey, { messages: 0, calls: 0, meetings: 0, reactions: 0, total: 0, selfActivity: 0 });
      }
      const record = map.get(dateKey);
      record[key] = (record[key] || 0) + amount;
      record.total += amount;
      record.selfActivity += selfAmount;
    }

    function activityCountsByDay() {
      const signature = activitySettingsSignature();
      if (ACTIVITY_COUNTS_BY_DAY_CACHE.value && ACTIVITY_COUNTS_BY_DAY_CACHE.signature === signature) {
        return ACTIVITY_COUNTS_BY_DAY_CACHE.value;
      }
      const counts = new Map();
      for (const thread of DATA.threads || []) {
        for (const message of thread.messages || []) {
          const messageDateKey = localDateKey(message.timestamp);
          if (isDiagnosticChatMessage(message) && valueFallsInActivityWindow(message.timestamp, messageDateKey)) {
            addActivityCount(counts, messageDateKey, "messages", 1, isOwnMessage(message) ? 1 : 0);
          }
          for (const reaction of messageReactions(message)) {
            for (const user of reaction.users || []) {
              if (!isCurrentUserIdentity(user.id, user.display_name)) continue;
              const reactionDateKey = localDateKey(user.reacted_at);
              if (valueFallsInActivityWindow(user.reacted_at, reactionDateKey)) {
                addActivityCount(counts, reactionDateKey, "reactions", 1, 1);
              }
            }
          }
        }
      }
      for (const call of DATA.calls || []) {
        const key = localDateKey(callActivityStartTimestamp(call));
        if (!key || !callOverlapsActivityWindow(call, key)) continue;
        let selfAmount = 0;
        if (isMeetingCall(call)) {
          selfAmount = isAttendedMeeting(call) ? 1 : 0;
        } else if (displayCallDirection(call) === "outgoing" || isAcceptedCommunication(call)) {
          selfAmount = 1;
        }
        addActivityCount(counts, key, isMeetingCall(call) ? "meetings" : "calls", 1, selfAmount);
      }
      ACTIVITY_COUNTS_BY_DAY_CACHE.signature = signature;
      ACTIVITY_COUNTS_BY_DAY_CACHE.value = counts;
      return counts;
    }

    function latestActivityDate() {
      const keys = [...activityCountsByDay().keys()].sort();
      return keys[keys.length - 1] || "";
    }

    function ensureActivityDate() {
      if (!String(state.activityDate || "").match(/^\\d{4}-\\d{2}-\\d{2}$/)) {
        state.activityDate = latestActivityDate() || todayDateKey();
      }
      if (!parseMonthKey(state.activityMonth)) {
        state.activityMonth = monthKeyFromDateKey(state.activityDate) || monthKeyFromDateKey(todayDateKey());
      }
      if (!monthKeyFromDateKey(state.activityDate)) {
        state.activityDate = latestActivityDate() || todayDateKey();
      }
    }

    function selectActivityDate(dateKey) {
      const normalized = String(dateKey || "").match(/^\\d{4}-\\d{2}-\\d{2}$/) ? dateKey : todayDateKey();
      state.activityDate = normalized;
      state.activityMonth = monthKeyFromDateKey(normalized);
      state.focusMessageId = null;
      state.focusCallKey = null;
      state.focusTimestamp = null;
      state.focusSearchQuery = "";
      renderView();
    }

    function activityResponsePairs(dateKey) {
      const userResponses = [];
      const counterpartResponses = [];
      for (const thread of DATA.threads || []) {
        const messages = sortedChatMessagesAsc(thread)
          .filter(message => valueFallsInActivityResponseWindow(message.timestamp, dateKey));
        let pending = null;
        for (let index = 0; index < messages.length; index += 1) {
          const current = messages[index];
          const currentIsOwn = isOwnMessage(current);
          if (!valueFallsInActivityResponseWindow(current.timestamp, dateKey)) continue;
          if (!pending) {
            pending = current;
            continue;
          }
          if (isOwnMessage(pending) === currentIsOwn) {
            pending = current;
            continue;
          }
          const previous = pending;
          if (!valueFallsInActivityResponseWindow(previous.timestamp, dateKey)) {
            pending = current;
            continue;
          }
          const delta = (timeValue(current.timestamp) - timeValue(previous.timestamp)) / 1000;
          if (!Number.isFinite(delta) || delta < 0) continue;
          if (currentIsOwn) {
            userResponses.push({
              seconds: delta,
              thread,
              previous,
              current,
              counterparty: threadCounterpartyLabel(thread, previous),
            });
          } else {
            counterpartResponses.push({
              seconds: delta,
              thread,
              previous,
              current,
              counterparty: threadCounterpartyLabel(thread, current),
            });
          }
          pending = current;
        }
      }
      return { userResponses, counterpartResponses };
    }

    function longestRapidChat(dayThreadMessages) {
      let best = null;
      const maxGapMs = 10 * 60 * 1000;
      for (const entry of dayThreadMessages) {
        const messages = entry.messages;
        let current = [];
        const finalize = () => {
          if (current.length < 2) return;
          let hasBackAndForth = false;
          for (let index = 1; index < current.length; index += 1) {
            if (isOwnMessage(current[index]) !== isOwnMessage(current[index - 1])) {
              hasBackAndForth = true;
              break;
            }
          }
          if (!hasBackAndForth) return;
          const first = current[0];
          const last = current[current.length - 1];
          const duration = (timeValue(last.timestamp) - timeValue(first.timestamp)) / 1000;
          if (!best || duration > best.durationSeconds) {
            best = {
              thread: entry.thread,
              first,
              last,
              count: current.length,
              durationSeconds: duration,
            };
          }
        };
        for (const message of messages) {
          const previous = current[current.length - 1];
          if (!previous || timeValue(message.timestamp) - timeValue(previous.timestamp) <= maxGapMs) {
            current.push(message);
            continue;
          }
          finalize();
          current = [message];
        }
        finalize();
      }
      return best;
    }

    function groupedMessageCounterpartMetrics(dayMessages, responses) {
      const groups = new Map();
      const ensure = label => {
        const key = normalizeTextValue(label || "Unknown");
        if (!groups.has(key)) {
          groups.set(key, {
            label: key,
            sent: 0,
            received: 0,
            userResponseSeconds: [],
            counterpartResponseSeconds: [],
            firstTimestamp: "",
            firstTime: Number.POSITIVE_INFINITY,
            firstThread: null,
            firstMessageId: "",
            lastTimestamp: "",
          });
        }
        return groups.get(key);
      };
      for (const item of dayMessages) {
        const label = threadCounterpartyLabel(item.thread, item.message);
        const group = ensure(label);
        if (isOwnMessage(item.message)) group.sent += 1;
        else group.received += 1;
        const currentTime = timeValue(item.message.timestamp);
        if (Number.isFinite(currentTime) && currentTime < group.firstTime) {
          group.firstTimestamp = item.message.timestamp;
          group.firstTime = currentTime;
          group.firstThread = item.thread;
          group.firstMessageId = item.message.id || "";
        }
        if (!group.lastTimestamp || timeValue(item.message.timestamp) > timeValue(group.lastTimestamp)) {
          group.lastTimestamp = item.message.timestamp;
        }
      }
      for (const pair of responses.userResponses || []) {
        ensure(pair.counterparty).userResponseSeconds.push(pair.seconds);
      }
      for (const pair of responses.counterpartResponses || []) {
        ensure(pair.counterparty).counterpartResponseSeconds.push(pair.seconds);
      }
      return [...groups.values()].sort(compareActivityGroupsByFirstTimestamp);
    }

    function buildActivityDayMetrics(dateKey) {
      const cacheKey = `${dateKey}|${activitySettingsSignature()}`;
      if (ACTIVITY_DAY_METRICS_CACHE.has(cacheKey)) return ACTIVITY_DAY_METRICS_CACHE.get(cacheKey);
      const actions = [];
      const dayMessages = [];
      const dayThreadMessages = [];
      for (const thread of DATA.threads || []) {
        const threadMessages = sortedChatMessagesAsc(thread).filter(message => valueFallsInActivityWindow(message.timestamp, dateKey));
        if (!threadMessages.length) continue;
        dayThreadMessages.push({ thread, messages: threadMessages });
        for (const message of threadMessages) {
          dayMessages.push({ thread, message });
          actions.push({
            timestamp: message.timestamp,
            time: timeValue(message.timestamp),
            action: isOwnMessage(message) ? "Message sent" : "Message received",
            detail: threadCounterpartyLabel(thread, message),
          });
        }
      }

      let reactionCount = 0;
      for (const thread of DATA.threads || []) {
        for (const message of thread.messages || []) {
          for (const reaction of messageReactions(message)) {
            for (const user of reaction.users || []) {
              if (!isCurrentUserIdentity(user.id, user.display_name)) continue;
              if (!valueFallsInActivityWindow(user.reacted_at, dateKey)) continue;
              reactionCount += 1;
              actions.push({
                timestamp: user.reacted_at,
                time: timeValue(user.reacted_at),
                action: "Reaction added",
                detail: `${reaction.label} | ${threadDisplayLabel(thread)}`,
              });
            }
          }
        }
      }

      const allDayCalls = (DATA.calls || []).filter(call => callOverlapsActivityWindow(call, dateKey));
      const dayCalls = allDayCalls.filter(call => !isMeetingCall(call));
      const dayMeetings = allDayCalls.filter(isMeetingCall);
      for (const call of dayCalls) {
        const start = callActivityStartTimestamp(call);
        const end = callActivityEndTimestamp(call);
        if (valueFallsInActivityWindow(start, dateKey)) {
          actions.push({
            timestamp: start,
            time: timeValue(start),
            action: displayCallDirection(call) === "outgoing" ? "Outbound call started" : "Inbound call received",
            detail: callCounterpartyLabel(call),
          });
        }
        if (end && end !== start && valueFallsInActivityWindow(end, dateKey)) {
          actions.push({
            timestamp: end,
            time: timeValue(end),
            action: "Call ended",
            detail: callCounterpartyLabel(call),
          });
        }
      }
      for (const meeting of dayMeetings) {
        const start = callActivityStartTimestamp(meeting);
        const end = callActivityEndTimestamp(meeting);
        if (valueFallsInActivityWindow(start, dateKey)) {
          actions.push({
            timestamp: start,
            time: timeValue(start),
            action: "Meeting started",
            detail: normalizeTextValue(meeting.meeting_subject || callLabel(meeting)),
          });
        }
        if (end && end !== start && valueFallsInActivityWindow(end, dateKey)) {
          actions.push({
            timestamp: end,
            time: timeValue(end),
            action: "Meeting ended",
            detail: normalizeTextValue(meeting.meeting_subject || callLabel(meeting)),
          });
        }
      }
      actions.sort((left, right) => left.time - right.time);

      dayMessages.sort((left, right) => timeValue(left.message.timestamp) - timeValue(right.message.timestamp));
      const sentMessages = dayMessages.filter(item => isOwnMessage(item.message));
      const receivedMessages = dayMessages.filter(item => !isOwnMessage(item.message));
      const endedChats = dayThreadMessages.filter(entry => isOwnMessage(entry.messages[entry.messages.length - 1])).length;
      const ghostedChats = dayThreadMessages.filter(entry => !isOwnMessage(entry.messages[entry.messages.length - 1])).length;
      const responses = activityResponsePairs(dateKey);
      const userResponseStats = secondsStats(responses.userResponses.map(pair => pair.seconds));
      const counterpartResponseStats = secondsStats(responses.counterpartResponses.map(pair => pair.seconds));
      const longestChat = longestRapidChat(dayThreadMessages);
      const firstSent = sentMessages[0] || null;
      const firstReceived = receivedMessages[0] || null;
      const messageCounterpartGroups = groupedMessageCounterpartMetrics(dayMessages, responses);

      const acceptedCalls = dayCalls.filter(isAcceptedCommunication);
      const acceptedCallDurations = acceptedCalls.map(acceptedCallDurationSeconds).filter(Number.isFinite);
      const callDurationStats = secondsStats(acceptedCallDurations);
      const inboundCalls = dayCalls.filter(call => displayCallDirection(call) === "incoming");
      const outboundCalls = dayCalls.filter(call => displayCallDirection(call) === "outgoing");
      const firstOutboundCall = outboundCalls.slice().sort((left, right) => timeValue(callActivityStartTimestamp(left)) - timeValue(callActivityStartTimestamp(right)))[0] || null;
      const firstInboundCall = inboundCalls.slice().sort((left, right) => timeValue(callActivityStartTimestamp(left)) - timeValue(callActivityStartTimestamp(right)))[0] || null;
      const inboundCallGroups = callParticipantMetricGroups(inboundCalls);
      const outboundCallGroups = callParticipantMetricGroups(outboundCalls);

      const attendedMeetings = dayMeetings.filter(isAttendedMeeting);
      const missedMeetings = dayMeetings.filter(isMissedMeeting);
      const meetingDurations = attendedMeetings.map(meetingDurationSeconds).filter(Number.isFinite);
      const meetingDurationStats = secondsStats(meetingDurations);
      const meetingsByTime = dayMeetings.slice().sort((left, right) => timeValue(callActivityStartTimestamp(left)) - timeValue(callActivityStartTimestamp(right)));

      const metrics = {
        dateKey,
        workWindowLabel: activityWorkWindowLabel(),
        actions,
        firstAction: actions[0] || null,
        lastAction: actions[actions.length - 1] || null,
        activityWindowSeconds: actions.length > 1 ? ((actions[actions.length - 1].time - actions[0].time) / 1000) : (actions.length === 1 ? 0 : null),
        selfActivityScore: (activityCountsByDay().get(dateKey) || {}).selfActivity || 0,
        reactions: reactionCount,
        messages: {
          totalChats: dayThreadMessages.length,
          totalMessages: dayMessages.length,
          sent: sentMessages.length,
          received: receivedMessages.length,
          endedChats,
          ghostedChats,
          longestChat,
          userResponseStats,
          counterpartResponseStats,
          firstSent,
          firstReceived,
          counterpartGroups: messageCounterpartGroups,
        },
        calls: {
          total: dayCalls.length,
          received: inboundCalls.length,
          sent: outboundCalls.length,
          totalDurationSeconds: acceptedCallDurations.reduce((sum, value) => sum + value, 0),
          durationStats: callDurationStats,
          accepted: acceptedCalls.length,
          firstOutboundCall,
          firstInboundCall,
          inboundGroups: inboundCallGroups,
          outboundGroups: outboundCallGroups,
        },
        meetings: {
          total: dayMeetings.length,
          attended: attendedMeetings.length,
          missed: missedMeetings.length,
          totalDurationSeconds: meetingDurations.reduce((sum, value) => sum + value, 0),
          durationStats: meetingDurationStats,
          first: meetingsByTime[0] || null,
          last: meetingsByTime[meetingsByTime.length - 1] || null,
        },
      };
      ACTIVITY_DAY_METRICS_CACHE.set(cacheKey, metrics);
      return metrics;
    }

    function renderActivityMetric(label, value) {
      return `<div class="stat-card"><div class="k">${escapeHtml(label)}</div><div class="v">${escapeHtml(value)}</div></div>`;
    }

    function renderActivityMetricGrid(items) {
      return `<div class="activity-metric-grid">${items.map(item => renderActivityMetric(item.label, item.value)).join("")}</div>`;
    }

    function renderActivityRecord(title, fields) {
      return `
        <div class="activity-target-card">
          <div class="activity-target-title">${escapeHtml(title)}</div>
          <div class="activity-target-stats">
            ${fields.map(field => `
              <div class="activity-target-stat">
                ${escapeHtml(field.label)}
                <strong>${escapeHtml(field.value)}</strong>
              </div>
            `).join("")}
          </div>
        </div>
      `;
    }

    function renderActivitySection(title, subtitle, bodyHtml) {
      return `
        <section class="activity-section">
          <div class="activity-section-head">
            <div>
              <div class="activity-section-title">${escapeHtml(title)}</div>
              ${subtitle ? `<div class="activity-section-subtitle">${escapeHtml(subtitle)}</div>` : ``}
            </div>
          </div>
          ${bodyHtml}
        </section>
      `;
    }

    function activityActionDisplayName(action) {
      const labels = {
        "Message sent": "Message Sent",
        "Message received": "Message Received",
        "Reaction added": "Reaction Added",
        "Outbound call started": "Outbound Call Started",
        "Inbound call received": "Inbound Call Received",
        "Call ended": "Call Ended",
        "Meeting started": "Meeting Started",
        "Meeting ended": "Meeting Ended",
      };
      return labels[action] || action || "Action";
    }

    function renderActivityActionRecord(record, emptyLabel, prefix = "") {
      if (!record) {
        return renderActivityRecord(emptyLabel, [
          { label: "Action", value: "No activity" },
          { label: "Timestamp", value: "Unavailable" },
        ]);
      }
      const title = prefix
        ? `${prefix} ${activityActionDisplayName(record.action)}`
        : activityActionDisplayName(record.action);
      return renderActivityRecord(title, [
        { label: "Timestamp", value: fmt(record.timestamp) },
        { label: "Detail", value: record.detail || "Unavailable" },
      ]);
    }

    function threadResponseStatsFor(pairs, thread) {
      if (!thread) return secondsStats([]);
      return secondsStats((pairs || []).filter(pair => pair.thread === thread).map(pair => pair.seconds));
    }

    function renderFirstMessageRecord(title, item, responseStats, responseLabel) {
      if (!item) {
        return renderActivityRecord(title, [
          { label: "Timestamp", value: "No chat found" },
          { label: "Participant", value: "Unavailable" },
          { label: responseLabel, value: "Unavailable" },
          { label: "Median response", value: "Unavailable" },
        ]);
      }
      return renderActivityRecord(title, [
        { label: "Timestamp", value: fmt(item.message.timestamp) },
        { label: "Participant", value: threadCounterpartyLabel(item.thread, item.message) },
        { label: responseLabel, value: formatDurationPrecise(responseStats.average) },
        { label: "Median response", value: formatDurationPrecise(responseStats.median) },
      ]);
    }

    function renderCallRecord(title, call) {
      if (!call) {
        return renderActivityRecord(title, [
          { label: "Timestamp", value: "No call found" },
          { label: "Participant", value: "Unavailable" },
          { label: "Status", value: "Unavailable" },
          { label: "Duration", value: "Unavailable" },
        ]);
      }
      return renderActivityRecord(title, [
        { label: "Timestamp", value: fmt(callActivityStartTimestamp(call)) },
        { label: "Participant", value: callCounterpartyLabel(call) },
        { label: "Status", value: communicationOutcomeLabel(call) },
        { label: "Duration", value: formatDurationPrecise(acceptedCallDurationSeconds(call)) },
      ]);
    }

    function renderMeetingRecord(title, meeting) {
      if (!meeting) {
        return renderActivityRecord(title, [
          { label: "Meeting", value: "No meeting found" },
          { label: "Timestamp", value: "Unavailable" },
          { label: "Status", value: "Unavailable" },
          { label: "Duration", value: "Unavailable" },
        ]);
      }
      return renderActivityRecord(title, [
        { label: "Meeting", value: normalizeTextValue(meeting.meeting_subject || callLabel(meeting)) || "Meeting" },
        { label: "Timestamp", value: fmt(callActivityStartTimestamp(meeting)) },
        { label: "Status", value: meetingStatusLabel(meeting) },
        { label: "Duration", value: formatDurationPrecise(meetingDurationSeconds(meeting)) },
      ]);
    }

    function renderActivityTargetCards(groups, fieldsForGroup, emptyLabel, options = {}) {
      if (!groups.length) return `<div class="empty">${escapeHtml(emptyLabel)}</div>`;
      return `
        <div class="activity-target-grid">
          ${groups.map(group => {
            const target = options.targetForGroup ? options.targetForGroup(group) : null;
            const timestampLabel = options.timestampForGroup ? options.timestampForGroup(group) : "";
            const attrs = target
              ? [
                  `role="button"`,
                  `tabindex="0"`,
                  `data-activity-target-kind="${escapeHtml(target.kind || "")}"`,
                  target.threadId ? `data-activity-thread-id="${escapeHtml(target.threadId)}"` : "",
                  target.focusMessageId ? `data-activity-focus-message-id="${escapeHtml(target.focusMessageId)}"` : "",
                  target.callKey ? `data-activity-call-key="${escapeHtml(target.callKey)}"` : "",
                  target.focusTimestamp ? `data-activity-focus-timestamp="${escapeHtml(target.focusTimestamp)}"` : "",
                  target.dateKey ? `data-activity-date-key="${escapeHtml(target.dateKey)}"` : "",
                  target.callDirection ? `data-activity-call-direction="${escapeHtml(target.callDirection)}"` : "",
                ].filter(Boolean).join(" ")
              : "";
            return `
            <div class="activity-target-card ${target ? "activity-target-link" : ""}" ${attrs}>
              <div class="activity-target-head">
                <div class="activity-target-title">${escapeHtml(group.label)}</div>
                ${timestampLabel ? `<div class="activity-target-time">${escapeHtml(timestampLabel)}</div>` : ``}
              </div>
              <div class="activity-target-stats">
                ${fieldsForGroup(group).map(field => `
                  <div class="activity-target-stat">
                    ${escapeHtml(field.label)}
                    <strong>${escapeHtml(field.value)}</strong>
                  </div>
                `).join("")}
              </div>
            </div>
          `;
          }).join("")}
        </div>
      `;
    }

    function initActivityTargetLinks(scope) {
      const activate = element => {
        const kind = element.dataset.activityTargetKind || "";
        const focusTimestamp = element.dataset.activityFocusTimestamp || "";
        const dateKey = element.dataset.activityDateKey || localDateKey(focusTimestamp) || state.activityDate;
        if (kind === "message") {
          state.messageDateFrom = dateKey;
          state.messageDateTo = dateKey;
          openThreadView({
            threadId: element.dataset.activityThreadId,
            clearSearch: true,
            clearCategory: true,
            syncThreadDateToSidebar: true,
            viewFilter: "all",
            focusMessageId: element.dataset.activityFocusMessageId || null,
            focusTimestamp: focusTimestamp || null,
            revealInSidebar: true,
          });
          return;
        }
        if (kind === "call") {
          state.callSearch = "";
          state.callGroup = "";
          state.callDirection = element.dataset.activityCallDirection || "";
          state.callDateFrom = dateKey;
          state.callDateTo = dateKey;
          openCallView({
            callKey: element.dataset.activityCallKey,
            revealInSidebar: true,
            scrollTop: true,
          });
        }
      };
      for (const element of scope.querySelectorAll(".activity-target-link")) {
        element.addEventListener("click", () => activate(element));
        element.addEventListener("keydown", event => {
          if (event.key !== "Enter" && event.key !== " ") return;
          event.preventDefault();
          activate(element);
        });
      }
    }

    function normalizeDateKeyInput(value, fallback) {
      const text = String(value || "").trim();
      return /^\\d{4}-\\d{2}-\\d{2}$/.test(text) ? text : fallback;
    }

    function dateKeyToLocalDate(dateKey) {
      const match = String(dateKey || "").match(/^(\\d{4})-(\\d{2})-(\\d{2})$/);
      if (!match) return null;
      return new Date(Number.parseInt(match[1], 10), Number.parseInt(match[2], 10) - 1, Number.parseInt(match[3], 10));
    }

    function enumerateDateKeys(fromDateKey, toDateKey) {
      const fromDate = dateKeyToLocalDate(fromDateKey);
      const toDate = dateKeyToLocalDate(toDateKey);
      if (!fromDate || !toDate) return [];
      const start = fromDate <= toDate ? fromDate : toDate;
      const end = fromDate <= toDate ? toDate : fromDate;
      const keys = [];
      const current = new Date(start.getFullYear(), start.getMonth(), start.getDate());
      while (current <= end && keys.length < 3660) {
        keys.push(localDateKeyFromDate(current));
        current.setDate(current.getDate() + 1);
      }
      return keys;
    }

    function csvCell(value) {
      const text = String(value ?? "");
      return /[",\\n\\r]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
    }

    function activityCsvPush(rows, dateKey, section, subject, metric, value, detail = "") {
      rows.push([
        dateKey,
        section,
        subject,
        metric,
        value,
        detail,
      ]);
    }

    function activityCsvRowsForDate(dateKey) {
      const metrics = buildActivityDayMetrics(dateKey);
      const rows = [];
      const messageStats = metrics.messages;
      const callStats = metrics.calls.durationStats;
      const meetingStats = metrics.meetings.durationStats;

      activityCsvPush(rows, dateKey, "Summary", "Day", "Work window", metrics.workWindowLabel);
      activityCsvPush(rows, dateKey, "Summary", "Day", "Activity window", activityWindowSummary(metrics));
      activityCsvPush(rows, dateKey, "Summary", "Day", "Observed actions", metrics.actions.length);
      activityCsvPush(rows, dateKey, "Summary", "Day", "Self activity score", metrics.selfActivityScore);
      activityCsvPush(rows, dateKey, "Summary", "Day", "Messages", messageStats.totalMessages);
      activityCsvPush(rows, dateKey, "Summary", "Day", "Calls", metrics.calls.total);
      activityCsvPush(rows, dateKey, "Summary", "Day", "Meetings", metrics.meetings.total);
      if (metrics.firstAction) {
        activityCsvPush(rows, dateKey, "Activity Window", "First Action", activityActionDisplayName(metrics.firstAction.action), fmt(metrics.firstAction.timestamp), metrics.firstAction.detail || "");
      }
      if (metrics.lastAction) {
        activityCsvPush(rows, dateKey, "Activity Window", "Last Action", activityActionDisplayName(metrics.lastAction.action), fmt(metrics.lastAction.timestamp), metrics.lastAction.detail || "");
      }

      activityCsvPush(rows, dateKey, "Messages", "Overview", "Total chats", messageStats.totalChats);
      activityCsvPush(rows, dateKey, "Messages", "Overview", "Total messages", messageStats.totalMessages);
      activityCsvPush(rows, dateKey, "Messages", "Overview", "Messages received", messageStats.received);
      activityCsvPush(rows, dateKey, "Messages", "Overview", "Messages sent", messageStats.sent);
      activityCsvPush(rows, dateKey, "Messages", "Overview", "Chats ended by user", messageStats.endedChats);
      activityCsvPush(rows, dateKey, "Messages", "Overview", "Chats awaiting user", messageStats.ghostedChats);
      activityCsvPush(rows, dateKey, "Messages", "Overview", "User average response", formatDurationPrecise(messageStats.userResponseStats.average));
      activityCsvPush(rows, dateKey, "Messages", "Overview", "User median response", formatDurationPrecise(messageStats.userResponseStats.median));
      activityCsvPush(rows, dateKey, "Messages", "Overview", "Colleague average response", formatDurationPrecise(messageStats.counterpartResponseStats.average));
      activityCsvPush(rows, dateKey, "Messages", "Overview", "Colleague median response", formatDurationPrecise(messageStats.counterpartResponseStats.median));
      if (messageStats.longestChat) {
        activityCsvPush(
          rows,
          dateKey,
          "Messages",
          threadDisplayLabel(messageStats.longestChat.thread),
          "Longest rapid chat",
          formatDurationPrecise(messageStats.longestChat.durationSeconds),
          `${messageStats.longestChat.count} timeline items`
        );
      }
      for (const group of messageStats.counterpartGroups) {
        const userStats = secondsStats(group.userResponseSeconds);
        const counterpartStats = secondsStats(group.counterpartResponseSeconds);
        activityCsvPush(rows, dateKey, "Coworker Message Snapshot", group.label, "Sent", group.sent);
        activityCsvPush(rows, dateKey, "Coworker Message Snapshot", group.label, "Received", group.received);
        activityCsvPush(rows, dateKey, "Coworker Message Snapshot", group.label, "First timestamp", fmt(group.firstTimestamp));
        activityCsvPush(rows, dateKey, "Coworker Message Snapshot", group.label, "User average response", formatDurationPrecise(userStats.average));
        activityCsvPush(rows, dateKey, "Coworker Message Snapshot", group.label, "Their average response", formatDurationPrecise(counterpartStats.average));
      }

      activityCsvPush(rows, dateKey, "User Call Metrics", "Profile", "Calls total", metrics.calls.total);
      activityCsvPush(rows, dateKey, "User Call Metrics", "Profile", "Calls received", metrics.calls.received);
      activityCsvPush(rows, dateKey, "User Call Metrics", "Profile", "Calls sent", metrics.calls.sent);
      activityCsvPush(rows, dateKey, "User Call Metrics", "Profile", "Accepted calls", metrics.calls.accepted);
      activityCsvPush(rows, dateKey, "User Call Metrics", "Profile", "Total duration", formatDurationPrecise(metrics.calls.totalDurationSeconds, "0s"));
      activityCsvPush(rows, dateKey, "User Call Metrics", "Profile", "Shortest accepted call", formatDurationPrecise(callStats.min));
      activityCsvPush(rows, dateKey, "User Call Metrics", "Profile", "Average accepted call", formatDurationPrecise(callStats.average));
      activityCsvPush(rows, dateKey, "User Call Metrics", "Profile", "Longest accepted call", formatDurationPrecise(callStats.max));
      const pushCallGroupRows = (section, group) => {
        activityCsvPush(rows, dateKey, section, group.label, "First timestamp", fmt(group.firstTimestamp));
        activityCsvPush(rows, dateKey, section, group.label, "Accepted", group.accepted);
        activityCsvPush(rows, dateKey, section, group.label, "Missed", group.missed);
        activityCsvPush(rows, dateKey, section, group.label, "Total calls", group.total);
        activityCsvPush(rows, dateKey, section, group.label, "Total duration", formatDurationPrecise(group.totalDuration, "0s"));
      };
      for (const group of metrics.calls.inboundGroups) pushCallGroupRows("Inbound Call Metrics", group);
      for (const group of metrics.calls.outboundGroups) pushCallGroupRows("Outbound Call Metrics", group);

      activityCsvPush(rows, dateKey, "Meetings", "Overview", "Meetings scheduled", metrics.meetings.total);
      activityCsvPush(rows, dateKey, "Meetings", "Overview", "Meetings attended", metrics.meetings.attended);
      activityCsvPush(rows, dateKey, "Meetings", "Overview", "Meetings missed", metrics.meetings.missed);
      activityCsvPush(rows, dateKey, "Meetings", "Overview", "Total meeting time", formatDurationPrecise(metrics.meetings.totalDurationSeconds, "0s"));
      activityCsvPush(rows, dateKey, "Meetings", "Overview", "Average attended meeting", formatDurationPrecise(meetingStats.average));
      activityCsvPush(rows, dateKey, "Meetings", "Overview", "Median attended meeting", formatDurationPrecise(meetingStats.median));
      return rows;
    }

    function buildActivityCsv(fromDateKey, toDateKey) {
      const rows = [["date", "section", "subject", "metric", "value", "detail"]];
      for (const dateKey of enumerateDateKeys(fromDateKey, toDateKey)) {
        rows.push(...activityCsvRowsForDate(dateKey));
      }
      return rows.map(row => row.map(csvCell).join(",")).join("\\n");
    }

    function downloadActivityCsv(fromDateKey, toDateKey) {
      const csv = buildActivityCsv(fromDateKey, toDateKey);
      const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = `teams_activity_${fromDateKey}_to_${toDateKey}.csv`;
      document.body.appendChild(anchor);
      anchor.click();
      document.body.removeChild(anchor);
      window.setTimeout(() => URL.revokeObjectURL(url), 1000);
      showToast("Activity CSV exported");
    }

    function quantile(sortedValues, ratio) {
      const values = sortedValues || [];
      if (!values.length) return null;
      const index = Math.min(values.length - 1, Math.max(0, Math.floor((values.length - 1) * ratio)));
      return values[index];
    }

    function activityIntensityForScore(score) {
      if (!Number.isFinite(score) || score <= 0) return "none";
      const scores = [...activityCountsByDay().values()]
        .map(record => record.selfActivity || 0)
        .filter(value => value > 0)
        .sort((left, right) => left - right);
      if (!scores.length) return "none";
      if (scores[0] === scores[scores.length - 1]) return "average";
      if (score >= quantile(scores, .75)) return "high";
      if (score >= quantile(scores, .40)) return "average";
      if (score >= quantile(scores, .15)) return "low";
      return "minimal";
    }

    function activityIntensityLabel(intensity) {
      const labels = {
        none: "None",
        minimal: "Minimal",
        low: "Low",
        average: "Average",
        high: "Very active",
      };
      return labels[intensity] || "None";
    }

    function bestActivityDateForMonth(monthKey) {
      const keys = [...activityCountsByDay().keys()]
        .filter(key => monthKeyFromDateKey(key) === monthKey)
        .sort();
      return keys[0] || dateKeyInMonth(monthKey, 1) || todayDateKey();
    }

    function renderActivityCalendar() {
      ensureActivityDate();
      const parsed = parseMonthKey(state.activityMonth)
        || parseMonthKey(monthKeyFromDateKey(state.activityDate))
        || parseMonthKey(monthKeyFromDateKey(todayDateKey()));
      const counts = activityCountsByDay();
      const firstOfMonth = new Date(parsed.year, parsed.month - 1, 1);
      const todayKey = todayDateKey();
      const weekdayLabels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
      const cells = [];
      const firstWeekday = firstOfMonth.getDay();
      for (let index = 0; index < 42; index += 1) {
        const cellDate = new Date(parsed.year, parsed.month - 1, 1 - firstWeekday + index);
        const dateKey = localDateKeyFromDate(cellDate);
        const record = counts.get(dateKey) || {};
        const total = record.total || 0;
        const selfActivity = record.selfActivity || 0;
        const intensity = activityIntensityForScore(selfActivity);
        const workday = isConfiguredWorkday(dateKey);
        const classes = [
          "calendar-day",
          cellDate.getMonth() === parsed.month - 1 ? "" : "outside",
          workday ? "" : "off-workday",
          workday && selfActivity <= 0 ? "inactive-workday" : "",
          dateKey === state.activityDate ? "active" : "",
          dateKey === todayKey ? "today" : "",
        ].filter(Boolean).join(" ");
        cells.push(`
          <button type="button" class="${escapeHtml(classes)}" data-date="${escapeHtml(dateKey)}" aria-label="${escapeHtml(`${formatDateOnly(dateKey)} | ${activityIntensityLabel(intensity)} | ${selfActivity} self actions | ${total} observed items`)}">
            <span class="calendar-date-num">${escapeHtml(String(cellDate.getDate()))}</span>
            <span class="calendar-activity-dot ${escapeHtml(intensity)}"></span>
            <span class="calendar-count">${total ? escapeHtml(NUMBER_FORMATTER.format(total)) : ""}</span>
          </button>
        `);
      }
      return `
        <div class="activity-calendar">
          <div class="calendar-heading">
            <span>${escapeHtml(formatDateOnly(state.activityDate))}</span>
          </div>
          <div class="calendar-grid">
            ${weekdayLabels.map(label => `<div class="calendar-weekday">${escapeHtml(label)}</div>`).join("")}
            ${cells.join("")}
          </div>
        </div>
      `;
    }

    function renderActivityList() {
      ensureActivityDate();
      const metrics = buildActivityDayMetrics(state.activityDate);
      sidebarCount.textContent = formatDateOnly(state.activityDate) || "Activity day";
      activityList.innerHTML = `
        ${renderActivityCalendar()}
        <div class="activity-sidebar-summary">
          <div class="activity-sidebar-stat"><span>Window</span><strong>${escapeHtml(activityWindowSummary(metrics))}</strong></div>
          <div class="activity-sidebar-stat"><span>Messages</span><strong>${escapeHtml(NUMBER_FORMATTER.format(metrics.messages.totalMessages))}</strong></div>
          <div class="activity-sidebar-stat"><span>Calls</span><strong>${escapeHtml(NUMBER_FORMATTER.format(metrics.calls.total))}</strong></div>
          <div class="activity-sidebar-stat"><span>Meetings</span><strong>${escapeHtml(NUMBER_FORMATTER.format(metrics.meetings.total))}</strong></div>
        </div>
      `;
      for (const day of activityList.querySelectorAll(".calendar-day[data-date]")) {
        day.addEventListener("click", () => {
          selectActivityDate(day.dataset.date);
        });
      }
    }

    function renderActivityPanel() {
      ensureActivityDate();
      const metrics = buildActivityDayMetrics(state.activityDate);
      const responses = activityResponsePairs(state.activityDate);
      const firstSentStats = metrics.messages.firstSent
        ? threadResponseStatsFor(responses.counterpartResponses, metrics.messages.firstSent.thread)
        : secondsStats([]);
      const firstReceivedStats = metrics.messages.firstReceived
        ? threadResponseStatsFor(responses.userResponses, metrics.messages.firstReceived.thread)
        : secondsStats([]);
      const callStats = metrics.calls.durationStats;
      const meetingStats = metrics.meetings.durationStats;
      const longestChat = metrics.messages.longestChat;
      contentPanel.innerHTML = `
        <div class="activity-report">
          <section class="detail-hero">
            <div class="kicker">Day View Diagnostics</div>
            <div class="title">
              <h2>${escapeHtml(formatDateOnly(metrics.dateKey))}</h2>
              <div class="chip chip-strong">${escapeHtml(NUMBER_FORMATTER.format(metrics.actions.length))} observed actions</div>
            </div>
            <div class="detail-subtle">Profile activity and counterpart activity involving ${escapeHtml(PROFILE_DISPLAY_NAME)} inside the selected work window.</div>
            <div class="activity-report-actions">
              <button type="button" class="call-link open-activity-messages">Open Messages For Day</button>
              <button type="button" class="call-link open-activity-calls">Open Calls For Day</button>
              <button type="button" class="call-link toggle-activity-export">Export CSV</button>
              <div class="activity-export-panel ${state.activityExportOpen ? "" : "hidden"}">
                <label class="range-field">
                  <span>Export From</span>
                  <input type="date" class="activity-export-from" value="${escapeHtml(state.activityExportFrom || metrics.dateKey)}">
                </label>
                <label class="range-field">
                  <span>Export To</span>
                  <input type="date" class="activity-export-to" value="${escapeHtml(state.activityExportTo || metrics.dateKey)}">
                </label>
                <button type="button" class="call-link download-activity-export">Download CSV</button>
              </div>
            </div>
          </section>
          ${renderActivitySection(
            "Teams Activity Window",
            "First observed action through last observed action for the selected date.",
            `
              ${renderActivityMetricGrid([
                { label: "Messages", value: NUMBER_FORMATTER.format(metrics.messages.totalMessages) },
                { label: "Calls", value: NUMBER_FORMATTER.format(metrics.calls.total) },
                { label: "Meetings", value: NUMBER_FORMATTER.format(metrics.meetings.total) },
                { label: "Observed Actions", value: NUMBER_FORMATTER.format(metrics.actions.length) },
              ])}
              <div class="activity-record-grid">
                ${renderActivityActionRecord(metrics.firstAction, "First Action", "First")}
                ${renderActivityActionRecord(metrics.lastAction, "Last Action", "Last")}
              </div>
            `
          )}
          ${renderActivitySection(
            "Messages",
            "Chat volume, endings, ghosted conversations, and response-time behavior.",
            `
              ${renderActivityMetricGrid([
                { label: "Total Chats", value: NUMBER_FORMATTER.format(metrics.messages.totalChats) },
                { label: "Total Messages", value: NUMBER_FORMATTER.format(metrics.messages.totalMessages) },
                { label: "Messages Received", value: NUMBER_FORMATTER.format(metrics.messages.received) },
                { label: "Messages Sent", value: NUMBER_FORMATTER.format(metrics.messages.sent) },
                { label: "Chats Ended By User", value: NUMBER_FORMATTER.format(metrics.messages.endedChats) },
                { label: "Chats Awaiting User", value: NUMBER_FORMATTER.format(metrics.messages.ghostedChats) },
                { label: "Longest Rapid Chat", value: longestChat ? `${formatDurationPrecise(longestChat.durationSeconds)} | ${threadDisplayLabel(longestChat.thread)}` : "Unavailable" },
                { label: "Rapid Chat Items", value: longestChat ? NUMBER_FORMATTER.format(longestChat.count) : "0" },
                { label: "User Avg Response", value: formatDurationPrecise(metrics.messages.userResponseStats.average) },
                { label: "User Median Response", value: formatDurationPrecise(metrics.messages.userResponseStats.median) },
                { label: "Colleague Avg Response", value: formatDurationPrecise(metrics.messages.counterpartResponseStats.average) },
                { label: "Colleague Median Response", value: formatDurationPrecise(metrics.messages.counterpartResponseStats.median) },
              ])}
              <div class="activity-record-grid">
                ${renderFirstMessageRecord("First Chat Sent By User", metrics.messages.firstSent, firstSentStats, "Target avg response")}
                ${renderFirstMessageRecord("First Chat Received From Originator", metrics.messages.firstReceived, firstReceivedStats, "User avg response")}
              </div>
              <div class="section-divider">
                <div class="section-label">Coworker Message Snapshot</div>
              </div>
              ${renderActivityTargetCards(
                metrics.messages.counterpartGroups,
                group => {
                  const userStats = secondsStats(group.userResponseSeconds);
                  const counterpartStats = secondsStats(group.counterpartResponseSeconds);
                  return [
                    { label: "Sent", value: NUMBER_FORMATTER.format(group.sent) },
                    { label: "Received", value: NUMBER_FORMATTER.format(group.received) },
                    { label: "User avg response", value: formatDurationPrecise(userStats.average) },
                    { label: "Their avg response", value: formatDurationPrecise(counterpartStats.average) },
                  ];
                },
                "No chat counterpart activity was found for this day.",
                {
                  targetForGroup: group => group.firstThread ? ({
                    kind: "message",
                    threadId: group.firstThread.id,
                    focusMessageId: group.firstMessageId || "",
                    focusTimestamp: group.firstTimestamp || "",
                    dateKey: localDateKey(group.firstTimestamp) || metrics.dateKey,
                  }) : null,
                }
              )}
            `
          )}
          ${renderActivitySection(
            "Calls",
            "Inbound and outbound participant activity with connected duration excluding missed calls.",
            `
              <div class="section-divider">
                <div class="section-label">User Call Metrics</div>
              </div>
              ${renderActivityMetricGrid([
                { label: "Calls Total", value: NUMBER_FORMATTER.format(metrics.calls.total) },
                { label: "Calls Received", value: NUMBER_FORMATTER.format(metrics.calls.received) },
                { label: "Calls Sent", value: NUMBER_FORMATTER.format(metrics.calls.sent) },
                { label: "Accepted Calls", value: NUMBER_FORMATTER.format(metrics.calls.accepted) },
                { label: "Total Duration", value: formatDurationPrecise(metrics.calls.totalDurationSeconds, "0s") },
                { label: "Shortest Accepted Call", value: formatDurationPrecise(callStats.min) },
                { label: "Average Accepted Call", value: formatDurationPrecise(callStats.average) },
                { label: "Longest Accepted Call", value: formatDurationPrecise(callStats.max) },
              ])}
              <div class="activity-record-grid">
                ${renderCallRecord("First Outbound Call", metrics.calls.firstOutboundCall)}
                ${renderCallRecord("First Inbound Call", metrics.calls.firstInboundCall)}
              </div>
              <div class="section-divider">
                <div class="section-label">Inbound Call Metrics</div>
              </div>
              ${renderActivityTargetCards(
                metrics.calls.inboundGroups,
                group => [
                  { label: "Accepted", value: NUMBER_FORMATTER.format(group.accepted) },
                  { label: "Missed", value: NUMBER_FORMATTER.format(group.missed) },
                  { label: "Total calls", value: NUMBER_FORMATTER.format(group.total) },
                  { label: "Total duration", value: formatDurationPrecise(group.totalDuration, "0s") },
                ],
                "No inbound participant call activity was found for this day.",
                {
                  timestampForGroup: group => fmt(group.firstTimestamp),
                  targetForGroup: group => group.firstCallKey ? ({
                    kind: "call",
                    callKey: group.firstCallKey,
                    focusTimestamp: group.firstTimestamp || "",
                    dateKey: localDateKey(group.firstTimestamp) || metrics.dateKey,
                    callDirection: "inbound",
                  }) : null,
                }
              )}
              <div class="section-divider">
                <div class="section-label">Outbound Call Metrics</div>
              </div>
              ${renderActivityTargetCards(
                metrics.calls.outboundGroups,
                group => [
                  { label: "Accepted", value: NUMBER_FORMATTER.format(group.accepted) },
                  { label: "Missed", value: NUMBER_FORMATTER.format(group.missed) },
                  { label: "Total calls", value: NUMBER_FORMATTER.format(group.total) },
                  { label: "Total duration", value: formatDurationPrecise(group.totalDuration, "0s") },
                ],
                "No outbound participant call activity was found for this day.",
                {
                  timestampForGroup: group => fmt(group.firstTimestamp),
                  targetForGroup: group => group.firstCallKey ? ({
                    kind: "call",
                    callKey: group.firstCallKey,
                    focusTimestamp: group.firstTimestamp || "",
                    dateKey: localDateKey(group.firstTimestamp) || metrics.dateKey,
                    callDirection: "outbound",
                  }) : null,
                }
              )}
            `
          )}
          ${renderActivitySection(
            "Meetings",
            "Scheduled meetings and attendance metrics inferred from Teams meeting call records.",
            `
              ${renderActivityMetricGrid([
                { label: "Meetings Scheduled", value: NUMBER_FORMATTER.format(metrics.meetings.total) },
                { label: "Meetings Attended", value: NUMBER_FORMATTER.format(metrics.meetings.attended) },
                { label: "Meetings Missed", value: NUMBER_FORMATTER.format(metrics.meetings.missed) },
                { label: "Total Meeting Time", value: formatDurationPrecise(metrics.meetings.totalDurationSeconds, "0s") },
                { label: "Shortest Attended Meeting", value: formatDurationPrecise(meetingStats.min) },
                { label: "Average Attended Meeting", value: formatDurationPrecise(meetingStats.average) },
                { label: "Median Attended Meeting", value: formatDurationPrecise(meetingStats.median) },
                { label: "Longest Attended Meeting", value: formatDurationPrecise(meetingStats.max) },
              ])}
              <div class="activity-record-grid">
                ${renderMeetingRecord("First Meeting", metrics.meetings.first)}
                ${renderMeetingRecord("Last Meeting", metrics.meetings.last)}
              </div>
            `
          )}
        </div>
      `;
      initActivityTargetLinks(contentPanel);
      const openMessagesForDay = contentPanel.querySelector(".open-activity-messages");
      if (openMessagesForDay) {
        openMessagesForDay.addEventListener("click", () => {
          state.view = "messages";
          clearMessageSearchState();
          state.category = "";
          state.messageDateFrom = metrics.dateKey;
          state.messageDateTo = metrics.dateKey;
          state.threadDateFrom = metrics.dateKey;
          state.threadDateTo = metrics.dateKey;
          state.messageViewFilter = "all";
          renderView();
          scrollAllToTop();
        });
      }
      const openCallsForDay = contentPanel.querySelector(".open-activity-calls");
      if (openCallsForDay) {
        openCallsForDay.addEventListener("click", () => {
          state.view = "calls";
          state.callSearch = "";
          state.callGroup = "";
          state.callDirection = "";
          state.callDateFrom = metrics.dateKey;
          state.callDateTo = metrics.dateKey;
          renderView();
          scrollAllToTop();
        });
      }
      const toggleExport = contentPanel.querySelector(".toggle-activity-export");
      if (toggleExport) {
        toggleExport.addEventListener("click", () => {
          state.activityExportOpen = !state.activityExportOpen;
          if (!state.activityExportFrom) state.activityExportFrom = metrics.dateKey;
          if (!state.activityExportTo) state.activityExportTo = metrics.dateKey;
          renderView();
        });
      }
      const exportFrom = contentPanel.querySelector(".activity-export-from");
      if (exportFrom) {
        exportFrom.addEventListener("change", event => {
          state.activityExportFrom = normalizeDateKeyInput(event.target.value, metrics.dateKey);
        });
      }
      const exportTo = contentPanel.querySelector(".activity-export-to");
      if (exportTo) {
        exportTo.addEventListener("change", event => {
          state.activityExportTo = normalizeDateKeyInput(event.target.value, state.activityExportFrom || metrics.dateKey);
        });
      }
      const downloadExport = contentPanel.querySelector(".download-activity-export");
      if (downloadExport) {
        downloadExport.addEventListener("click", () => {
          const fromValue = normalizeDateKeyInput((contentPanel.querySelector(".activity-export-from") || {}).value, metrics.dateKey);
          const toValue = normalizeDateKeyInput((contentPanel.querySelector(".activity-export-to") || {}).value, fromValue);
          state.activityExportFrom = fromValue;
          state.activityExportTo = toValue;
          downloadActivityCsv(fromValue, toValue);
        });
      }
    }

    function searchMessageText(thread, message) {
      if (MESSAGE_SEARCH_TEXT_CACHE.has(message)) {
        return MESSAGE_SEARCH_TEXT_CACHE.get(message);
      }
      const attachments = messageAttachments(message);
      const reactions = messageReactions(message);
      const parts = [
        thread.label,
        threadDisplayLabel(thread),
        thread.id,
        ...(thread.participants || []),
        messageDisplaySender(message),
        message.message_type,
        message.content_text,
        message.content_html,
        displayMessageType(message),
        displayMessageQuality(message),
        ...attachments.map(attachment => attachment.name),
        ...attachments.map(attachment => attachment.url),
        ...reactions.map(reaction => reaction.label),
        ...reactions.map(reaction => reaction.key),
        ...reactions.flatMap(reaction => reaction.users.map(user => user.display_name || user.id || "")),
      ];
      if (message.message_type === "ThreadActivity/AddMember") {
        const parsed = parseAddMemberEvent(message);
        parts.push(parsed.actorName, ...(parsed.addedNames || []));
      }
      if (message.message_type === "ThreadActivity/MemberJoined") {
        const parsed = parseMemberJoinedEvent(message);
        parts.push(parsed.actorName, ...(parsed.joinedNames || []));
      }
      if (message.message_type === "ThreadActivity/DeleteMember") {
        const parsed = parseDeleteMemberEvent(message);
        parts.push(parsed.actorName, ...(parsed.removedNames || []));
      }
      if (message.message_type === "ThreadActivity/TopicUpdate") {
        const parsed = parseTopicUpdateEvent(message);
        parts.push(parsed.actorName, parsed.topic);
      }
      const value = parts.filter(Boolean).join(" ").toLowerCase();
      MESSAGE_SEARCH_TEXT_CACHE.set(message, value);
      return value;
    }

    function includeMessageInSearchResults(message) {
      return Boolean(message && !messageIsCallEvent(message) && !messageIsSystemEventRecord(message));
    }

    function renderMessageBody(message, thread, highlightQuery = "") {
      const useHighlight = Boolean(String(highlightQuery || "").trim());
      if (messageIsCallEvent(message)) {
        return renderCallEventBody(message);
      }
      if (isStructuredThreadActivityEvent(message)) {
        return renderMembershipEventBody(message, thread);
      }
      const replyQuote = messageReplyQuote(message);
      if (replyQuote) {
        const quoteAuthorHtml = replyQuote.author
          ? `<div class="reply-quote-author">${useHighlight ? highlightSearchHtml(replyQuote.author, highlightQuery) : escapeHtml(replyQuote.author)}</div>`
          : ``;
        const quotePreviewHtml = replyQuote.preview
          ? `<div class="reply-quote-text">${useHighlight ? highlightSearchHtml(replyQuote.preview, highlightQuery) : escapeHtml(replyQuote.preview)}</div>`
          : ``;
        const replyTextHtml = replyQuote.reply_text
          ? `<div class="reply-response">${useHighlight ? highlightSearchHtml(replyQuote.reply_text, highlightQuery) : escapeHtml(replyQuote.reply_text)}</div>`
          : ``;
        const attachmentsHtml = messageHasAttachments(message) ? renderAttachmentCards(message) : ``;
        const quoteHtml = (quoteAuthorHtml || quotePreviewHtml)
          ? `<div class="reply-quote">${quoteAuthorHtml}${quotePreviewHtml}</div>`
          : ``;
        return `<div class="body reply-body">${quoteHtml}${replyTextHtml}${attachmentsHtml}</div>`;
      }
      if (messageHasAttachments(message)) {
        const textHtml = message.content_text
          ? `<div class="body-text">${useHighlight ? highlightSearchHtml(message.content_text || "", highlightQuery) : escapeHtml(message.content_text || "")}</div>`
          : ``;
        return `<div class="body attachment-body">${textHtml}${renderAttachmentCards(message)}</div>`;
      }
      return `<div class="body">${useHighlight ? highlightSearchHtml(message.content_text || "", highlightQuery) : escapeHtml(message.content_text || "")}</div>`;
    }

    function renderMessageRow(message, thread, options = {}) {
      const highlightQuery = String(options.highlightQuery || (options.highlight ? state.messageSearch : "") || "").trim();
      const useHighlight = Boolean(highlightQuery);
      const isFocused = Boolean(options.focused);
      const isSearchMatch = Boolean(options.searchMatch);
      const groupedWithPrevious = Boolean(options.groupedWithPrevious);
      const groupedWithNext = Boolean(options.groupedWithNext);
      const systemMessage = isSystemMessage(message);
      const selfMessage = !systemMessage && isOwnMessage(message);
      const accent = messageAccent(message);
      const senderLabel = messageDisplaySender(message);
      const classes = [
        "msg",
        message.quality === "event" ? "event" : "",
        isFocused ? "focused" : "",
        isSearchMatch ? "search-match" : "",
      ].filter(Boolean).join(" ");
      const senderHtml = useHighlight
        ? highlightSearchHtml(senderLabel, highlightQuery)
        : escapeHtml(senderLabel);
      const typeHtml = useHighlight
        ? highlightSearchHtml(displayMessageType(message), highlightQuery)
        : escapeHtml(displayMessageType(message));
      const bodyHtml = renderMessageBody(message, thread, highlightQuery);
      const reactionsHtml = renderMessageReactions(message, highlightQuery);
      const hiddenMeta = messageHiddenMeta(message);
      const collapsibleSystemEvent = systemMessage && !messageIsCallEvent(message);
      const hasCollapsibleContent = Boolean((hiddenMeta && hiddenMeta.count > 0) || collapsibleSystemEvent);
      const openHidden = hasCollapsibleContent && (
        (hiddenMeta && hiddenMeta.count > 0 && state.expandHiddenData) ||
        isFocused ||
        (collapsibleSystemEvent && isSearchMatch)
      );
      const shellAttrs = `class="${escapeHtml(classes)}${hasCollapsibleContent ? " msg-collapsible" : ""}" data-message-id="${escapeHtml(message.id || "")}" data-call-key="${escapeHtml(messageLinkedCallKey(message))}" data-timestamp="${escapeHtml(String(timeValue(message.timestamp)))}"`;
      const rowClasses = [
        "msg-row",
        selfMessage ? "self" : "",
        systemMessage ? "system" : "",
        groupedWithPrevious ? "grouped-prev" : "",
        groupedWithNext ? "grouped-next" : "",
      ].filter(Boolean).join(" ");
      const badgeHtml = `
        <div class="msg-meta-pills">
          <span class="msg-mini-chip">${typeHtml}</span>
          <span class="msg-mini-chip muted">${escapeHtml(displayMessageQuality(message))}</span>
        </div>
      `;
      const headerHtml = groupedWithPrevious && !systemMessage
        ? `
          <div class="head compact">
            <span class="msg-time">${escapeHtml(fmtTime(message.timestamp) || fmt(message.timestamp))}</span>
            ${badgeHtml}
          </div>
        `
        : `
          <div class="head primary">
            <span class="sender">${senderHtml}</span>
            <span class="msg-time">${escapeHtml(fmt(message.timestamp))}</span>
          </div>
          <div class="head secondary">
            ${badgeHtml}
          </div>
        `;
      const avatarLabel = senderInitials(systemMessage ? displayMessageType(message) : senderLabel, systemMessage ? 1 : 2);

      if (hasCollapsibleContent) {
        return `
          <article class="${escapeHtml(rowClasses)}" style="--msg-accent:${escapeHtml(accent)}">
            <div class="msg-avatar" aria-hidden="true">${escapeHtml(avatarLabel)}</div>
            <div class="msg-stack">
              <details ${shellAttrs} ${openHidden ? "open" : ""}>
                <summary>
                  ${headerHtml}
                  ${hiddenMeta && hiddenMeta.count > 0 ? `<div class="msg-summary-note">${escapeHtml(hiddenMeta.label)}</div>` : ``}
                </summary>
                <div class="msg-body-wrap">
                  ${bodyHtml}
                  ${reactionsHtml}
                </div>
              </details>
            </div>
          </article>
        `;
      }

      return `
        <article class="${escapeHtml(rowClasses)}" style="--msg-accent:${escapeHtml(accent)}">
          <div class="msg-avatar" aria-hidden="true">${escapeHtml(avatarLabel)}</div>
          <div class="msg-stack">
            <div ${shellAttrs}>
              ${headerHtml}
              ${bodyHtml}
              ${reactionsHtml}
            </div>
          </div>
        </article>
      `;
    }

    function messageSearchSignature() {
      const query = String(state.messageSearch || "").trim().toLowerCase();
      if (!query) return "";
      return JSON.stringify([
        query,
        state.category || "",
        state.messageViewFilter || "all",
        state.messageDateFrom || "",
        state.messageDateTo || "",
      ]);
    }

    function cacheSearchGroups(signature, groups) {
      if (!signature) return;
      if (SEARCH_GROUPS_CACHE.has(signature)) {
        SEARCH_GROUPS_CACHE.delete(signature);
      }
      SEARCH_GROUPS_CACHE.set(signature, groups);
      while (SEARCH_GROUPS_CACHE.size > 12) {
        const oldest = SEARCH_GROUPS_CACHE.keys().next().value;
        SEARCH_GROUPS_CACHE.delete(oldest);
      }
    }

    function scheduleSearchGroupsComputation() {
      const signature = messageSearchSignature();
      if (!signature) {
        window.clearTimeout(scheduleSearchGroupsComputation.timer);
        scheduleSearchGroupsComputation.pendingSignature = "";
        return;
      }
      if (SEARCH_GROUPS_CACHE.has(signature) || scheduleSearchGroupsComputation.pendingSignature === signature) {
        return;
      }
      scheduleSearchGroupsComputation.pendingSignature = signature;
      window.clearTimeout(scheduleSearchGroupsComputation.timer);
      scheduleSearchGroupsComputation.timer = window.setTimeout(() => {
        if (messageSearchSignature() !== signature) {
          if (scheduleSearchGroupsComputation.pendingSignature === signature) {
            scheduleSearchGroupsComputation.pendingSignature = "";
          }
          return;
        }
        const groups = buildSearchResultGroups();
        cacheSearchGroups(signature, groups);
        if (scheduleSearchGroupsComputation.pendingSignature === signature) {
          scheduleSearchGroupsComputation.pendingSignature = "";
        }
        if (state.view === "messages" && messageSearchSignature() === signature) {
          renderContent();
          scheduleSyncScrollTopButtons();
        }
      }, 160);
    }

    function buildSearchResultGroups() {
      const groups = [];
      if (!state.messageSearch) return groups;

      for (const thread of filteredThreads()) {
        const timeline = sortedThreadTimelineItems(thread)
          .filter(messagePassesSidebarDateRange)
          .filter(includeMessageInSearchResults);

        const hits = [];
        for (let index = 0; index < timeline.length; index += 1) {
          if (textMatchesSearch(searchMessageText(thread, timeline[index]))) {
            hits.push(index);
          }
        }
        if (!hits.length) continue;

        const clusters = [];
        for (const hitIndex of hits) {
          const start = Math.max(0, hitIndex - 1);
          const end = Math.min(timeline.length - 1, hitIndex + 1);
          const previous = clusters[clusters.length - 1];
          if (previous && start <= previous.end + 1) {
            previous.end = Math.max(previous.end, end);
            previous.hitCount += 1;
          } else {
            clusters.push({ start, end, hitCount: 1, hitIndex });
          }
        }

        for (const cluster of clusters) {
          const focusMessage = timeline[cluster.hitIndex];
          groups.push({
            thread,
            hitCount: cluster.hitCount,
            focusMessageId: focusMessage.id || "",
            focusTimestamp: focusMessage.timestamp || "",
            focusCallKey: "",
            viewFilter: "all",
            messages: timeline.slice(cluster.start, cluster.end + 1),
          });
        }
      }

      return groups.sort((left, right) => {
        const timeDiff = timeValue(right.focusTimestamp) - timeValue(left.focusTimestamp);
        if (timeDiff !== 0) return timeDiff;
        return threadDisplayLabel(left.thread).localeCompare(threadDisplayLabel(right.thread));
      });
    }

    function renderMessageList() {
      const rows = filteredThreads();
      sidebarCount.textContent = `${rows.length} conversations`;
      if (!state.threadId || !rows.some(thread => thread.id === state.threadId)) {
        state.threadId = rows[0] ? rows[0].id : null;
      }
      threadList.innerHTML = rows.map(thread => `
        <div class="list-row ${thread.id === state.threadId ? "active" : ""}" data-id="${escapeHtml(thread.id)}" style="--row-accent:${escapeHtml(threadListAccent(thread))}">
          <div class="list-row-top">
            <span class="list-pill">${escapeHtml(prettyCategory(thread.category))}</span>
            <span class="list-time">${escapeHtml(fmt(threadLastTimestampRaw(thread)))}</span>
          </div>
          <strong class="list-title">${escapeHtml(threadDisplayLabel(thread))}</strong>
          <div class="preview">${escapeHtml(latestThreadPreview(thread) || "No preview available.")}</div>
          <div class="list-stats">
            <span>${escapeHtml(NUMBER_FORMATTER.format(thread.message_count || (thread.messages || []).length))} items</span>
            <span>${escapeHtml(NUMBER_FORMATTER.format(threadParticipantCount(thread)))} people</span>
          </div>
        </div>
      `).join("") || `<div class="empty">No conversations match the current filters.</div>`;
    }

    function renderCallList() {
      const rows = filteredCalls();
      sidebarCount.textContent = `${rows.length} calls`;
      if (!state.callKey || !rows.some(call => callKey(call) === state.callKey)) {
        state.callKey = rows[0] ? callKey(rows[0]) : null;
      }
      callList.innerHTML = rows.map(call => `
        <div class="list-row ${callKey(call) === state.callKey ? "active" : ""}" data-key="${escapeHtml(callKey(call))}" style="--row-accent:${escapeHtml(callListAccent(call))}">
          <div class="list-row-top">
            <span class="list-pill">${escapeHtml(displayCallGroupLabel(call))}</span>
            <span class="list-time">${escapeHtml(fmt(callPrimaryTimestamp(call)))}</span>
          </div>
          <strong class="list-title">${escapeHtml(normalizeTextValue(callLabel(call)))}</strong>
          <div class="list-stats">
            <span>${escapeHtml(displayCallStatus(call) || "Unclassified")}</span>
            <span>${escapeHtml(callDuration(call) || "Duration unavailable")}</span>
          </div>
        </div>
      `).join("") || `<div class="empty">No calls match the current filters.</div>`;
    }

    function renderSearchLoadingPanel() {
      contentPanel.innerHTML = `
        <section class="detail-hero">
          <div class="kicker">Grouped Search Results</div>
          <div class="title">
            <h2>Search Results</h2>
            <div class="chip chip-strong">Searching...</div>
          </div>
          <div class="detail-subtle">Building grouped timeline matches for <strong>${escapeHtml(String(state.messageSearch || "").trim())}</strong>. Sidebar conversation matches are ready; detailed results will appear momentarily.</div>
        </section>
      `;
    }

    function renderSearchResultsPanel(groups) {
      const totalMatches = groups.reduce((sum, group) => sum + group.hitCount, 0);
      contentPanel.innerHTML = `
        <section class="detail-hero">
          <div class="kicker">Grouped Search Results</div>
          <div class="title">
            <h2>Search Results</h2>
            <div class="chip chip-strong">${escapeHtml(NUMBER_FORMATTER.format(totalMatches))} matches</div>
          </div>
          <div class="detail-subtle">Showing grouped timeline matches for <strong>${escapeHtml(state.messageSearch)}</strong> with plus or minus one surrounding timeline item.</div>
        </section>
        <div class="search-results">
          ${groups.map((group, index) => `
            <div class="search-group">
              <div class="search-group-header">
                <div>
                  <div><strong>${escapeHtml(threadDisplayLabel(group.thread))}</strong></div>
                  <div class="search-group-meta">${escapeHtml(prettyCategory(group.thread.category))} | ${escapeHtml(fmt(group.focusTimestamp))} | ${escapeHtml(String(group.hitCount))} match${group.hitCount === 1 ? "" : "es"}</div>
                </div>
                <button type="button" class="call-link open-search-thread" data-thread-id="${escapeHtml(group.thread.id)}" data-focus-message-id="${escapeHtml(group.focusMessageId || "")}" data-focus-time="${escapeHtml(group.focusTimestamp || "")}" data-focus-call-key="${escapeHtml(group.focusCallKey || "")}" data-view-filter="${escapeHtml(group.viewFilter || "all")}">Open In Chats</button>
              </div>
              <div class="messages">
                ${renderTimeline(group.messages, group.thread, {
                  messageOptions: message => ({
                    highlightQuery: state.messageSearch,
                    focused: group.focusMessageId && message.id === group.focusMessageId,
                    searchMatch: textMatchesSearch(searchMessageText(group.thread, message)),
                  }),
                })}
              </div>
            </div>
            ${index < groups.length - 1 ? `<div class="search-group-divider"></div>` : ``}
          `).join("") || `<div class="empty">No timeline items match the current search.</div>`}
        </div>
      `;
      initExpandableLists(contentPanel);
      initParticipantChatLinks(contentPanel);
      initAttachmentActions(contentPanel);

      [...contentPanel.querySelectorAll(".open-search-thread")].forEach(element => {
        element.addEventListener("click", () => {
          openThreadView({
            threadId: element.dataset.threadId,
            clearSearch: true,
            focusMessageId: element.dataset.focusMessageId || null,
            focusTimestamp: element.dataset.focusTime || null,
            focusCallKey: element.dataset.focusCallKey || null,
            focusSearchQuery: state.messageSearch,
            revealInSidebar: true,
          });
        });
      });

      [...contentPanel.querySelectorAll(".open-call-record")].forEach(element => {
        element.addEventListener("click", () => {
          openCallView({
            callKey: element.dataset.callKey,
            revealInSidebar: true,
            scrollTop: true,
          });
        });
      });
    }

    function renderThreadPanel() {
      const thread = THREAD_BY_ID.get(state.threadId);
      if (!thread) {
        contentPanel.innerHTML = `<div class="empty">Select a conversation to view its data.</div>`;
        return;
      }
      const meta = thread.metadata || {};
      const allMessages = sortedThreadTimelineItems(thread);
      const rangeMessages = allMessages.filter(messagePassesCombinedDateRange);
      const linkedCalls = linkedCallsForThread(thread);
      const linkedCallCount = linkedCalls.length;
      const meetingCall = linkedCalls.find(call => call.meeting_subject || call.meeting_start_time || call.meeting_end_time) || {};
      const messages = rangeMessages.filter(messagePassesFilter);
      const firstMessage = messages.length ? messages[messages.length - 1] : null;
      const lastMessage = messages[0] || null;
      const eventCount = messages.filter(message => message.quality === "event").length;
      const curatedCount = messages.filter(message => message.quality !== "event").length;
      const meeting = thread.meeting || {};
      const meetingSubject = normalizeTextValue(meeting.subject || meetingCall.meeting_subject || meta.topic || threadDisplayLabel(thread) || "");
      const meetingStart = meeting.startTime || meetingCall.meeting_start_time || "";
      const meetingEnd = meeting.endTime || meetingCall.meeting_end_time || "";
      const meetingWindowLabel = meetingStart ? `${fmt(meetingStart)} to ${fmt(meetingEnd)}` : "";
      const showCompactChatMeta = ["chat_space", "thread"].includes(thread.category);
      contentPanel.innerHTML = `
        <section class="detail-hero">
          <div class="kicker">${escapeHtml(prettyCategory(thread.category))}</div>
          <div class="title">
            <h2>${escapeHtml(threadDisplayLabel(thread))}</h2>
            <div class="chip chip-strong">${escapeHtml(NUMBER_FORMATTER.format(allMessages.length))} timeline items</div>
          </div>
          <div class="detail-subtle">${escapeHtml(showCompactChatMeta
            ? `${NUMBER_FORMATTER.format(threadParticipantCount(thread))} participants | ${NUMBER_FORMATTER.format(linkedCallCount)} linked calls`
            : (meetingSubject || "Meeting metadata available below"))}</div>
          <div class="participant-cloud">
            ${renderExpandableChipGroup(threadParticipantEntries(thread), {
              emptyLabel: "No participants were resolved.",
              enableChatLinks: ["team_chat", "thread"].includes(thread.category),
            })}
          </div>
        </section>
        <div class="detail-toolbar">
          <div class="toolbar-row">
            <div class="segmented">
              <button type="button" class="seg-btn message-filter ${state.messageViewFilter === "all" ? "active" : ""}" data-filter="all">All</button>
              <button type="button" class="seg-btn message-filter ${state.messageViewFilter === "messages" ? "active" : ""}" data-filter="messages">Messages</button>
              <button type="button" class="seg-btn message-filter ${state.messageViewFilter === "calls" ? "active" : ""}" data-filter="calls">Calls</button>
              <button type="button" class="seg-btn message-filter ${state.messageViewFilter === "events" ? "active" : ""}" data-filter="events">Events</button>
            </div>
            <div class="call-event-actions">
              <button type="button" class="call-link jump-newest">Newest</button>
              <button type="button" class="call-link jump-oldest">Oldest</button>
              ${thread.csv_path ? `<a class="call-link" href="${escapeHtml(thread.csv_path)}" target="_blank" rel="noopener">Open CSV</a>` : ``}
              <button type="button" class="call-link copy-thread-id">Copy Thread Id</button>
              <button type="button" class="call-link toggle-raw-events">${state.expandHiddenData ? "Hide Hidden Data" : "Show Hidden Data"}</button>
            </div>
          </div>
          <div class="range-controls">
            <label class="range-field">
              <span>From</span>
              <input type="date" class="thread-date-from" value="${escapeHtml(state.threadDateFrom)}">
            </label>
            <label class="range-field">
              <span>To</span>
              <input type="date" class="thread-date-to" value="${escapeHtml(state.threadDateTo)}">
            </label>
            <button type="button" class="call-link clear-date-range"${hasMessageFilters() ? "" : " disabled"}>Clear Filters</button>
          </div>
          <div class="toolbar-divider"></div>
        </div>
        <div class="stat-strip">
          <div class="stat-card"><div class="k">Visible</div><div class="v">${escapeHtml(NUMBER_FORMATTER.format(messages.length))}</div></div>
          <div class="stat-card"><div class="k">Curated</div><div class="v">${escapeHtml(NUMBER_FORMATTER.format(curatedCount))}</div></div>
          <div class="stat-card"><div class="k">Events</div><div class="v">${escapeHtml(NUMBER_FORMATTER.format(eventCount))}</div></div>
          <div class="stat-card"><div class="k">Last Activity</div><div class="v">${escapeHtml(fmt(lastMessage ? lastMessage.timestamp : null))}</div></div>
        </div>
        <div class="meta-grid">
          <div class="meta-block"><div class="k">Thread Id</div><div class="mono">${escapeHtml(thread.id)}</div></div>
          <div class="meta-block"><div class="k">Participants</div><div>${escapeHtml(NUMBER_FORMATTER.format(threadParticipantCount(thread)))}</div></div>
          <div class="meta-block"><div class="k">Merged Calls</div><div>${escapeHtml(NUMBER_FORMATTER.format(linkedCallCount))}</div></div>
          ${showCompactChatMeta ? "" : `<div class="meta-block"><div class="k">Meeting Subject</div><div>${escapeHtml(meetingSubject)}</div></div>`}
          ${showCompactChatMeta ? "" : `<div class="meta-block"><div class="k">Meeting Window</div><div>${escapeHtml(meetingWindowLabel)}</div></div>`}
          <div class="meta-block"><div class="k">First Activity</div><div>${escapeHtml(fmt(firstMessage ? firstMessage.timestamp : null))}</div></div>
        </div>
        <div class="section-divider">
          <div class="section-label">Timeline</div>
        </div>
        <div class="messages">
          ${renderTimeline(messages, thread, {
            messageOptions: message => ({
              highlightQuery: state.focusSearchQuery,
              focused: Boolean(
                (state.focusMessageId && message.id === state.focusMessageId) ||
                (!state.focusMessageId && state.focusCallKey && messageLinkedCallKey(message) === state.focusCallKey)
              ),
              searchMatch: state.focusSearchQuery
                ? textMatchesQuery(searchMessageText(thread, message), state.focusSearchQuery)
                : false,
            }),
          }) || `<div class="empty">${(hasThreadDateRange() || hasSidebarMessageDateRange()) ? "No timeline items match the current date range and filters." : "No messages in this conversation."}</div>`}
        </div>
      `;
      initExpandableLists(contentPanel);
      initParticipantChatLinks(contentPanel);
      initAttachmentActions(contentPanel);
      [...contentPanel.querySelectorAll(".message-filter")].forEach(element => {
        element.addEventListener("click", () => {
          state.messageViewFilter = element.dataset.filter;
          renderView();
        });
      });
      const threadDateFrom = contentPanel.querySelector(".thread-date-from");
      if (threadDateFrom) {
        threadDateFrom.addEventListener("change", event => {
          state.threadDateFrom = event.target.value || "";
          renderView();
        });
      }
      const threadDateTo = contentPanel.querySelector(".thread-date-to");
      if (threadDateTo) {
        threadDateTo.addEventListener("change", event => {
          state.threadDateTo = event.target.value || "";
          renderView();
        });
      }
      const clearDateRange = contentPanel.querySelector(".clear-date-range");
      if (clearDateRange) {
        clearDateRange.addEventListener("click", () => {
          clearMessageFilters();
          renderView();
          scrollAllToTop();
        });
      }
      const copyThreadId = contentPanel.querySelector(".copy-thread-id");
      if (copyThreadId) {
        copyThreadId.addEventListener("click", () => copyText(thread.id, "Thread id copied"));
      }
      const toggleRaw = contentPanel.querySelector(".toggle-raw-events");
      if (toggleRaw) {
        toggleRaw.addEventListener("click", () => {
          state.expandHiddenData = !state.expandHiddenData;
          renderView();
        });
      }
      const jumpNewest = contentPanel.querySelector(".jump-newest");
      if (jumpNewest) {
        jumpNewest.addEventListener("click", () => {
          const firstMessageCard = contentPanel.querySelector(".messages .msg");
          if (firstMessageCard) {
            firstMessageCard.scrollIntoView({ block: "center", behavior: "smooth" });
          }
        });
      }
      const jumpOldest = contentPanel.querySelector(".jump-oldest");
      if (jumpOldest) {
        jumpOldest.addEventListener("click", () => {
          const cards = contentPanel.querySelectorAll(".messages .msg");
          const lastMessageCard = cards[cards.length - 1];
          if (lastMessageCard) {
            lastMessageCard.scrollIntoView({ block: "center", behavior: "smooth" });
          }
        });
      }
      [...contentPanel.querySelectorAll(".open-call-record")].forEach(element => {
        element.addEventListener("click", () => {
          openCallView({
            callKey: element.dataset.callKey,
            revealInSidebar: true,
            scrollTop: true,
          });
        });
      });
      focusThreadPosition();
    }

    function focusThreadPosition() {
      if (!state.focusMessageId && !state.focusCallKey && !state.focusTimestamp) return;
      let target = null;
      if (state.focusMessageId) {
        target = contentPanel.querySelector(`.msg[data-message-id="${CSS.escape(state.focusMessageId)}"]`);
      }
      if (!target && state.focusCallKey) {
        target = contentPanel.querySelector(`.msg[data-call-key="${CSS.escape(state.focusCallKey)}"]`);
      }
      if (!target && state.focusTimestamp) {
        const focusTime = timeValue(state.focusTimestamp);
        let bestDiff = Number.POSITIVE_INFINITY;
        for (const element of contentPanel.querySelectorAll(".msg[data-timestamp]")) {
          const current = Number(element.dataset.timestamp || Number.NEGATIVE_INFINITY);
          const diff = Math.abs(current - focusTime);
          if (diff < bestDiff) {
            bestDiff = diff;
            target = element;
          }
        }
      }
      if (target) {
        target.classList.add("focused");
        centerMainTimelineRow(mainScrollWrap, target.closest(".msg-row") || target, "smooth");
      }
    }

    function renderCallPanel() {
      const call = CALLS_BY_KEY.get(state.callKey);
        if (!call) {
          contentPanel.innerHTML = `<div class="empty">Select a call to view its data.</div>`;
          return;
        }
      const callParticipantEntriesList = callParticipantEntries(call);
      const callMeetingWindow = call.meeting_start_time ? `${fmt(call.meeting_start_time)} to ${fmt(call.meeting_end_time)}` : "";
      const relatedThreads = preferredThreadsForCall(call);
      const jumpTargets = callJumpTargets(call);
      const callGroupLabel = displayCallGroupLabel(call);
      const callTypeLabel = displayCallTypeLabel(call);
      const callQualityLabel = displayCallQualityLabel(call);
      const callDurationLabel = callDuration(call);
      const showRawType = includeRawCallTypeChip(call);
      const topDetailChips = dedupe([
        callGroupLabel,
        showRawType ? callTypeLabel : "",
        callQualityLabel,
      ].filter(Boolean));
      contentPanel.innerHTML = `
        <section class="detail-hero">
          <div class="kicker">${escapeHtml(callGroupLabel)}</div>
          <div class="title">
            <h2>${escapeHtml(normalizeTextValue(callLabel(call)))}</h2>
            <div class="chip chip-strong">${escapeHtml(displayCallStatus(call))}</div>
          </div>
          <div class="chips">
            ${callDurationLabel ? `<div class="chip">${escapeHtml(callDurationLabel)}</div>` : ``}
            ${topDetailChips.map(label => `<div class="chip">${escapeHtml(label)}</div>`).join("")}
          </div>
        </section>
        <div class="detail-toolbar">
          <div class="call-event-actions">
            <a class="call-link" href="teams_ccl_csv_v1/call_history.csv" target="_blank" rel="noopener">Open Call CSV</a>
            <button type="button" class="call-link copy-call-id">Copy Call Id</button>
          </div>
        </div>
        <div class="stat-strip">
          <div class="stat-card"><div class="k">Start</div><div class="v">${escapeHtml(fmt(call.start_time))}</div></div>
          <div class="stat-card"><div class="k">End</div><div class="v">${escapeHtml(fmt(call.end_time))}</div></div>
          <div class="stat-card"><div class="k">Duration</div><div class="v">${escapeHtml(callDuration(call) || "Unavailable")}</div></div>
          <div class="stat-card"><div class="k">Linked Conversations</div><div class="v">${escapeHtml(NUMBER_FORMATTER.format(relatedThreads.length))}</div></div>
        </div>
        <div class="meta-grid">
          <div class="meta-block"><div class="k">Start Time</div><div>${escapeHtml(fmt(call.start_time))}</div></div>
          <div class="meta-block"><div class="k">Connect Time</div><div>${escapeHtml(fmt(call.connect_time))}</div></div>
          <div class="meta-block"><div class="k">End Time</div><div>${escapeHtml(fmt(call.end_time))}</div></div>
          <div class="meta-block"><div class="k">Direction</div><div>${escapeHtml(displayCallDirectionLabel(call))}</div></div>
          <div class="meta-block"><div class="k">State</div><div>${escapeHtml(displayCallStateLabel(call))}</div></div>
          <div class="meta-block"><div class="k">Type</div><div>${escapeHtml(callGroupLabel)}</div></div>
          ${showRawType ? `<div class="meta-block"><div class="k">Raw Type</div><div>${escapeHtml(callTypeLabel)}</div></div>` : ``}
          <div class="meta-block"><div class="k">Originator</div><div>${escapeHtml(callSideLabel(call, "originator"))}</div></div>
          ${(callSideLabel(call, "target")) ? `<div class="meta-block"><div class="k">Target</div><div>${escapeHtml(callSideLabel(call, "target"))}</div></div>` : ``}
          <div class="meta-block"><div class="k">Call Id</div><div class="mono">${escapeHtml(call.call_id || "")}</div></div>
          ${call.shared_correlation_id ? `<div class="meta-block"><div class="k">Shared Correlation Id</div><div class="mono">${escapeHtml(call.shared_correlation_id || "")}</div></div>` : ``}
          <div class="meta-block wide"><div class="k">Participants</div>${renderExpandableChipGroup(callParticipantEntriesList, { emptyLabel: normalizeTextValue(callLabel(call)) || "No participants were resolved." })}</div>
          ${call.meeting_subject ? `<div class="meta-block"><div class="k">Meeting Subject</div><div>${escapeHtml(normalizeTextValue(call.meeting_subject || ""))}</div></div>` : ``}
          ${callMeetingWindow ? `<div class="meta-block"><div class="k">Meeting Window</div><div>${escapeHtml(callMeetingWindow)}</div></div>` : ``}
        </div>
        <div class="section-divider">
          <div class="section-label">Open Conversation At Call Time</div>
        </div>
        ${jumpTargets.length
          ? `<div class="jump-list">
              ${jumpTargets.map(target => `<button type="button" class="call-link open-thread-record" data-thread-id="${escapeHtml(target.thread.id)}" data-focus-time="${escapeHtml(target.focusTimestamp || "")}" data-focus-call-key="${escapeHtml(target.focusCallKey || "")}" data-view-filter="${escapeHtml(target.viewFilter || "all")}">${escapeHtml(callJumpLabel(target))}</button>`).join("")}
            </div>`
          : `<div class="subtle">No linked conversation messages were found for this call.</div>`}
      `;
      const copyCallId = contentPanel.querySelector(".copy-call-id");
      if (copyCallId) {
        copyCallId.addEventListener("click", () => copyText(call.call_id || "", "Call id copied"));
      }
      initExpandableLists(contentPanel);
      initParticipantChatLinks(contentPanel);
      [...contentPanel.querySelectorAll(".open-thread-record")].forEach(element => {
        element.addEventListener("click", () => {
          openThreadView({
            threadId: element.dataset.threadId,
            clearSearch: true,
            viewFilter: element.dataset.viewFilter || "all",
            focusTimestamp: element.dataset.focusTime || null,
            focusCallKey: element.dataset.focusCallKey || null,
            syncThreadDateToSidebar: true,
            revealInSidebar: true,
          });
        });
      });
    }

    function renderContent() {
      if (state.view === "activity") {
        renderActivityPanel();
        return;
      }
      if (state.view === "calls") {
        renderCallPanel();
        return;
      }
      if (state.messageSearch) {
        const signature = messageSearchSignature();
        if (signature && SEARCH_GROUPS_CACHE.has(signature)) {
          renderSearchResultsPanel(SEARCH_GROUPS_CACHE.get(signature) || []);
        } else {
          scheduleSearchGroupsComputation();
          renderSearchLoadingPanel();
        }
        return;
      }
      renderThreadPanel();
    }

    function renderView() {
      window.clearTimeout(scheduleMessageSearchRender.timer);
      window.clearTimeout(scheduleCallSearchRender.timer);
      const showingMessages = state.view === "messages";
      const showingCalls = state.view === "calls";
      const showingActivity = state.view === "activity";
      viewMessages.classList.toggle("active", showingMessages);
      viewCalls.classList.toggle("active", showingCalls);
      viewActivity.classList.toggle("active", showingActivity);
      messagesTools.classList.toggle("hidden", !showingMessages);
      callsTools.classList.toggle("hidden", !showingCalls);
      activityTools.classList.toggle("hidden", !showingActivity);
      threadList.classList.toggle("hidden", !showingMessages);
      callList.classList.toggle("hidden", !showingCalls);
      activityList.classList.toggle("hidden", !showingActivity);
      if (showingMessages) {
        renderMessageList();
      } else if (showingCalls) {
        renderCallList();
      } else {
        renderActivityList();
      }
      renderContent();
      syncInputsFromState();
      renderChrome();
      renderActiveFilters();
      schedulePersistState();
      scheduleSyncScrollTopButtons();
    }

    viewMessages.addEventListener("click", () => {
      state.view = "messages";
      state.focusMessageId = null;
      state.focusCallKey = null;
      state.focusTimestamp = null;
      state.focusSearchQuery = "";
      renderView();
    });

    viewCalls.addEventListener("click", () => {
      state.view = "calls";
      state.focusMessageId = null;
      state.focusCallKey = null;
      state.focusTimestamp = null;
      state.focusSearchQuery = "";
      renderView();
    });

    viewActivity.addEventListener("click", () => {
      state.view = "activity";
      ensureActivityDate();
      state.focusMessageId = null;
      state.focusCallKey = null;
      state.focusTimestamp = null;
      state.focusSearchQuery = "";
      renderView();
      scrollAllToTop();
    });

    threadList.addEventListener("click", event => {
      const row = event.target.closest(".list-row[data-id]");
      if (!row || !threadList.contains(row)) return;
      if (state.messageSearch) {
        const thread = THREAD_BY_ID.get(row.dataset.id);
        const latestMatch = thread ? latestMatchingSearchMessage(thread) : null;
        openThreadView({
          threadId: row.dataset.id,
          clearSearch: true,
          focusMessageId: latestMatch && latestMatch.id ? latestMatch.id : null,
          focusTimestamp: latestMatch ? (latestMatch.timestamp || null) : null,
          focusSearchQuery: state.messageSearch,
          revealInSidebar: true,
          scrollTop: !latestMatch,
        });
        return;
      }
      state.threadId = row.dataset.id;
      state.threadDateFrom = state.messageDateFrom || "";
      state.threadDateTo = state.messageDateTo || "";
      state.focusMessageId = null;
      state.focusCallKey = null;
      state.focusTimestamp = null;
      state.focusSearchQuery = "";
      renderView();
      scrollMainToTop();
    });

    callList.addEventListener("click", event => {
      const row = event.target.closest(".list-row[data-key]");
      if (!row || !callList.contains(row)) return;
      openCallView({
        callKey: row.dataset.key,
      });
    });

    messageSearch.addEventListener("input", event => {
      const nextValue = String(event.target.value || "");
      state.messageSearch = nextValue.trim() ? nextValue : "";
      state.focusMessageId = null;
      state.focusCallKey = null;
      state.focusTimestamp = null;
      state.focusSearchQuery = "";
      scheduleMessageSearchRender();
    });

    messageSearch.addEventListener("focus", () => {
      scheduleIdleWork(primeMessageSearchCaches);
    });

    categoryFilter.addEventListener("change", event => {
      state.category = event.target.value;
      renderView();
    });

    messageDateFrom.addEventListener("change", event => {
      state.messageDateFrom = event.target.value || "";
      state.threadDateFrom = state.messageDateFrom;
      state.threadDateTo = state.messageDateTo;
      renderView();
    });

    messageDateTo.addEventListener("change", event => {
      state.messageDateTo = event.target.value || "";
      state.threadDateFrom = state.messageDateFrom;
      state.threadDateTo = state.messageDateTo;
      renderView();
    });

    clearMessageDateRange.addEventListener("click", () => {
      clearMessageFilters();
      renderView();
      scrollAllToTop();
    });

    callSearch.addEventListener("input", event => {
      state.callSearch = event.target.value.trim();
      scheduleCallSearchRender();
    });

    callGroupFilter.addEventListener("change", event => {
      state.callGroup = event.target.value;
      renderView();
    });

    callDirectionFilter.addEventListener("change", event => {
      state.callDirection = event.target.value;
      renderView();
    });

    callDateFrom.addEventListener("change", event => {
      state.callDateFrom = event.target.value || "";
      renderView();
    });

    callDateTo.addEventListener("change", event => {
      state.callDateTo = event.target.value || "";
      renderView();
    });

    clearCallDateRange.addEventListener("click", () => {
      clearCallFilters();
      renderView();
      scrollAllToTop();
    });

    if (activityMonth) {
      activityMonth.addEventListener("change", event => {
        const monthKey = event.target.value || monthKeyFromDateKey(todayDateKey());
        state.activityMonth = monthKey;
        if (monthKeyFromDateKey(state.activityDate) !== monthKey) {
          state.activityDate = bestActivityDateForMonth(monthKey);
        }
        renderView();
        scrollAllToTop();
      });
    }

    if (activityPrevMonth) {
      activityPrevMonth.addEventListener("click", () => {
        state.activityMonth = shiftMonthKey(state.activityMonth || monthKeyFromDateKey(state.activityDate) || monthKeyFromDateKey(todayDateKey()), -1);
        if (monthKeyFromDateKey(state.activityDate) !== state.activityMonth) {
          state.activityDate = bestActivityDateForMonth(state.activityMonth);
        }
        renderView();
        scrollAllToTop();
      });
    }

    if (activityNextMonth) {
      activityNextMonth.addEventListener("click", () => {
        state.activityMonth = shiftMonthKey(state.activityMonth || monthKeyFromDateKey(state.activityDate) || monthKeyFromDateKey(todayDateKey()), 1);
        if (monthKeyFromDateKey(state.activityDate) !== state.activityMonth) {
          state.activityDate = bestActivityDateForMonth(state.activityMonth);
        }
        renderView();
        scrollAllToTop();
      });
    }

    if (activityWorkStart) {
      activityWorkStart.addEventListener("change", event => {
        state.activityWorkStart = normalizeTimeInput(event.target.value, "08:00");
        resetActivityCaches();
        renderView();
        scrollAllToTop();
      });
    }

    if (activityWorkEnd) {
      activityWorkEnd.addEventListener("change", event => {
        state.activityWorkEnd = normalizeTimeInput(event.target.value, "17:00");
        resetActivityCaches();
        renderView();
        scrollAllToTop();
      });
    }

    for (const input of activityWorkdayInputs) {
      input.addEventListener("change", () => {
        state.activityWorkDays = activityWorkdayInputs
          .filter(candidate => candidate.checked)
          .map(candidate => String(candidate.value))
          .join(",");
        resetActivityCaches();
        renderView();
      });
    }

    if (activityToday) {
      activityToday.addEventListener("click", () => {
        selectActivityDate(todayDateKey());
        scrollAllToTop();
      });
    }

    if (sidebarListWrap) {
      sidebarListWrap.addEventListener("scroll", scheduleSyncScrollTopButtons, { passive: true });
    }
    if (mainScrollWrap) {
      mainScrollWrap.addEventListener("scroll", scheduleSyncScrollTopButtons, { passive: true });
    }
    if (sidebarScrollTopButton) {
      sidebarScrollTopButton.addEventListener("click", () => {
        if (!sidebarListWrap) return;
        sidebarListWrap.scrollTo({ top: 0, behavior: "smooth" });
      });
    }
    if (mainScrollTopButton) {
      mainScrollTopButton.addEventListener("click", () => {
        if (!mainScrollWrap) return;
        mainScrollWrap.scrollTo({ top: 0, behavior: "smooth" });
      });
    }
    window.addEventListener("resize", scheduleSyncScrollTopButtons);

    activeFilterBar.addEventListener("click", event => {
      const button = event.target.closest("[data-clear-filter]");
      if (!button || !activeFilterBar.contains(button)) return;
      const filterKey = button.dataset.clearFilter;
      if (filterKey === "message-search") clearMessageSearchState();
      if (filterKey === "message-category") state.category = "";
      if (filterKey === "message-date") {
        state.messageDateFrom = "";
        state.messageDateTo = "";
      }
      if (filterKey === "thread-date") {
        state.threadDateFrom = "";
        state.threadDateTo = "";
      }
      if (filterKey === "message-view-filter") state.messageViewFilter = "all";
      if (filterKey === "call-search") state.callSearch = "";
      if (filterKey === "call-group") state.callGroup = "";
      if (filterKey === "call-direction") state.callDirection = "";
      if (filterKey === "call-date") {
        state.callDateFrom = "";
        state.callDateTo = "";
      }
      if (filterKey === "activity-date") {
        selectActivityDate(todayDateKey());
        return;
      }
      if (filterKey === "activity-window") {
        state.activityWorkStart = "08:00";
        state.activityWorkEnd = "17:00";
        state.activityWorkDays = "1,2,3,4,5";
        resetActivityCaches();
      }
      renderView();
    });

    window.addEventListener("keydown", event => {
      const activeTarget = document.activeElement;
      const key = String(event.key || "");

      if ((key === "/" && !event.metaKey && !event.ctrlKey && !event.altKey) || ((event.metaKey || event.ctrlKey) && key.toLowerCase() === "k")) {
        if (!isTypingTarget(activeTarget)) {
          event.preventDefault();
          focusActiveSearchField();
        }
        return;
      }

      if (isTypingTarget(activeTarget)) {
        if (key === "Escape") activeTarget.blur();
        return;
      }

      if (key === "[") {
        event.preventDefault();
        moveSidebarSelection(-1);
        return;
      }
      if (key === "]") {
        event.preventDefault();
        moveSidebarSelection(1);
        return;
      }
      if (key === "Escape") {
        if (clearCurrentSearch()) {
          event.preventDefault();
        }
      }
    });

    function callPrimaryTimestampValue(call) {
      const key = callKey(call);
      if (CALL_PRIMARY_TIME_VALUE_CACHE.has(key)) {
        return CALL_PRIMARY_TIME_VALUE_CACHE.get(key);
      }
      const value = timeValue(callPrimaryTimestamp(call));
      CALL_PRIMARY_TIME_VALUE_CACHE.set(key, value);
      return value;
    }

    function scheduleIdleWork(callback) {
      if (window.requestIdleCallback) {
        window.requestIdleCallback(callback, { timeout: 250 });
        return;
      }
      window.setTimeout(() => callback({ didTimeout: true, timeRemaining: () => 0 }), 48);
    }

    function primeMessageSearchCaches(deadline) {
      const threads = DATA.threads || [];
      let threadIndex = primeMessageSearchCaches.threadIndex || 0;
      let messageIndex = primeMessageSearchCaches.messageIndex || 0;

      while (threadIndex < threads.length && (deadline.didTimeout || deadline.timeRemaining() > 4)) {
        const thread = threads[threadIndex];
        if (messageIndex === 0) {
          threadSearchText(thread);
          sortedThreadTimelineItems(thread);
        }
        const messages = thread.messages || [];
        while (messageIndex < messages.length && (deadline.didTimeout || deadline.timeRemaining() > 4)) {
          searchMessageText(thread, messages[messageIndex]);
          messageIndex += 1;
        }
        if (messageIndex >= messages.length) {
          threadIndex += 1;
          messageIndex = 0;
          continue;
        }
        break;
      }

      primeMessageSearchCaches.threadIndex = threadIndex;
      primeMessageSearchCaches.messageIndex = messageIndex;
      if (threadIndex < threads.length) {
        scheduleIdleWork(primeMessageSearchCaches);
      }
    }

    function primeCallCaches(deadline) {
      const calls = DATA.calls || [];
      let index = primeCallCaches.index || 0;
      let processed = 0;
      const maxBatch = deadline.didTimeout ? 12 : Number.POSITIVE_INFINITY;
      while (index < calls.length && processed < maxBatch && (deadline.didTimeout || deadline.timeRemaining() > 4)) {
        isPhoneCall(calls[index]);
        index += 1;
        processed += 1;
      }
      primeCallCaches.index = index;
      if (index < calls.length) {
        scheduleIdleWork(primeCallCaches);
      }
    }

    function renderInitialView() {
      renderView();
      scheduleIdleWork(primeMessageSearchCaches);
      scheduleIdleWork(primeCallCaches);
    }

    restoreState();
    syncInputsFromState();
    renderChrome();
    scheduleSyncScrollTopButtons();
    if (window.requestAnimationFrame) {
      window.requestAnimationFrame(renderInitialView);
    } else {
      renderInitialView();
    }
  </script>
</body>
</html>
"""


def load_export(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


SUMMARY_FIELDS = (
    "threads_total",
    "messages_total",
    "calls_total",
    "attachments_total",
    "reactions_total",
)
PROFILE_FIELDS = (
    "oid",
    "display_name",
)
THREAD_FIELDS = (
    "id",
    "category",
    "label",
    "message_count",
    "messages",
    "metadata",
    "meeting",
    "participant_ids",
    "participants",
)
THREAD_METADATA_FIELDS = ("topic",)
THREAD_MEETING_FIELDS = ("subject", "startTime", "endTime")
MESSAGE_FIELDS = (
    "id",
    "timestamp",
    "sender_display_name",
    "sender_id",
    "message_type",
    "content_text",
    "reactions",
    "attachments",
    "quality",
)
MESSAGE_ATTACHMENT_FIELDS = ("id", "name", "url", "preview_url", "kind")
MESSAGE_REACTION_FIELDS = ("key", "count", "users")
MESSAGE_REACTION_USER_FIELDS = ("id", "display_name", "reacted_at")
MESSAGE_HTML_TYPES = frozenset({"ThreadActivity/TopicUpdate"})
REPLY_QUOTE_HTML_MARKER = "schema.skype.com/reply"
CALL_FIELDS = (
    "call_id",
    "call_state",
    "call_type",
    "connect_time",
    "conversation_id",
    "direction",
    "end_time",
    "group_chat_thread_id",
    "meeting_end_time",
    "meeting_series_kind",
    "meeting_start_time",
    "meeting_subject",
    "originator_display_name",
    "originator_endpoint",
    "originator_id",
    "originator_phone_number",
    "participant_display_names",
    "participant_ids",
    "participant_sessions",
    "quality",
    "shared_correlation_id",
    "start_time",
    "summary_text",
    "target_display_name",
    "target_endpoint",
    "target_id",
    "target_phone_number",
    "user_participation",
)
CALL_PARTICIPANT_SESSION_FIELDS = ("id", "display_name", "duration_seconds")


def pick_fields(payload: dict | None, allowed_fields: tuple[str, ...]) -> dict:
    source = payload or {}
    return {key: source[key] for key in allowed_fields if key in source}


def build_message_payload(message: dict) -> dict:
    row = pick_fields(message, MESSAGE_FIELDS)
    content_html = message.get("content_html")
    if content_html and (
        message.get("message_type") in MESSAGE_HTML_TYPES
        or REPLY_QUOTE_HTML_MARKER in str(content_html).lower()
    ):
        row["content_html"] = content_html
    row["attachments"] = [
        pick_fields(attachment, MESSAGE_ATTACHMENT_FIELDS)
        for attachment in (message.get("attachments") or [])
    ]
    row["reactions"] = [
        {
            **pick_fields(reaction, MESSAGE_REACTION_FIELDS),
            "users": [
                pick_fields(user, MESSAGE_REACTION_USER_FIELDS)
                for user in (reaction.get("users") or [])
            ],
        }
        for reaction in (message.get("reactions") or [])
    ]
    return row


def build_browser_payload(export_data: dict) -> dict:
    threads = []
    for thread in export_data.get("threads") or []:
        row = pick_fields(thread, THREAD_FIELDS)
        row["metadata"] = pick_fields(row.get("metadata"), THREAD_METADATA_FIELDS)
        row["meeting"] = pick_fields(row.get("meeting"), THREAD_MEETING_FIELDS)
        row["messages"] = [build_message_payload(message) for message in (thread.get("messages") or [])]
        row["csv_path"] = thread_csv_path(thread)
        threads.append(row)

    calls = []
    for call in export_data.get("calls") or []:
        row = pick_fields(call, CALL_FIELDS)
        row["participant_sessions"] = [
            pick_fields(session, CALL_PARTICIPANT_SESSION_FIELDS)
            for session in (call.get("participant_sessions") or [])
        ]
        calls.append(row)

    return {
        "summary": pick_fields(export_data.get("summary"), SUMMARY_FIELDS),
        "profile": pick_fields(export_data.get("profile"), PROFILE_FIELDS),
        "threads": threads,
        "calls": calls,
        "guid_directory": export_data.get("guid_directory") or {},
    }


def build_browser(export_data: dict, output_path: Path) -> None:
    payload = build_browser_payload(export_data)
    html = HTML_TEMPLATE.replace("__DATA__", json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    output_path.write_text(html, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a single-file browser viewer for the Teams CCL export.")
    parser.add_argument("--input", default="teams_ccl_canonical_v1.json", help="Path to the canonical CCL JSON.")
    parser.add_argument("--output", default="teams_ccl_browser_v1.html", help="Path to write the browser HTML.")
    args = parser.parse_args()

    export_data = load_export(Path(args.input).resolve())
    build_browser(export_data, Path(args.output).resolve())


if __name__ == "__main__":
    main()
