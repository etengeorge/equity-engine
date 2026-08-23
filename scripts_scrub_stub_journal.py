"""
scripts_scrub_stub_journal.py - ONE-TIME v2 cleanup of v1 journal pollution.

v1 wrote deterministic "[STUB]" placeholder theses into store/journal/verticals/<Sector>/<TICKER>.md,
where future synthesis prompts read them as if they were prior judgment. v2 stops new ones
(engine.run journals only synthesis_source == "llm"); this removes the old ones.

Removes only thesis entries ("\n---\n## <date> — <TICKER>\n" blocks) whose body contains "[STUB]".
News blocks ("### News & updates") and live entries are untouched. Files left with no entries keep
their header line so the company doc still exists. Prints what it did; idempotent.

    python scripts_scrub_stub_journal.py            # apply
    python scripts_scrub_stub_journal.py --dry-run  # report only
"""
import glob
import os
import re
import sys

import config

ROOT = os.path.join(config.STORE_DIR, "journal", "verticals")
ENTRY = re.compile(r"\n---\n## \d{4}-\d{2}-\d{2} — [A-Z0-9.\-]+\n")


def scrub_file(path, dry=False):
    txt = open(path, encoding="utf-8").read()
    if "[STUB]" not in txt:
        return 0, 0
    starts = [m.start() for m in ENTRY.finditer(txt)]
    if not starts:
        return 0, 0
    # split into header + entries; an entry runs to the next entry marker or a news block
    pieces, kept, removed = [txt[:starts[0]]], 0, 0
    bounds = starts + [len(txt)]
    for i in range(len(starts)):
        seg = txt[bounds[i]:bounds[i + 1]]
        news_at = seg.find("\n### News & updates")
        entry, news = (seg[:news_at], seg[news_at:]) if news_at != -1 else (seg, "")
        if "[STUB]" in entry:
            removed += 1
        else:
            pieces.append(entry)
            kept += 1
        pieces.append(news)
    if not dry:
        with open(path, "w", encoding="utf-8") as f:
            f.write("".join(pieces))
    return kept, removed


def main():
    dry = "--dry-run" in sys.argv
    total = 0
    for p in sorted(glob.glob(os.path.join(ROOT, "*", "*.md"))):
        if os.path.basename(p).startswith("_"):
            continue
        kept, removed = scrub_file(p, dry)
        if removed:
            total += removed
            print(f"{'would remove' if dry else 'removed'} {removed} stub entr{'y' if removed == 1 else 'ies'} "
                  f"(kept {kept} live) in {os.path.relpath(p)}")
    print(f"{'would remove' if dry else 'removed'} {total} stub entries total")


if __name__ == "__main__":
    main()
