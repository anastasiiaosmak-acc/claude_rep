#!/usr/bin/env python3
"""Tiny notes CLI — the only moving part of this pet project.

Storage is notes.json next to this file: a JSON list of
{"id": int, "text": str, "done": bool}. Stdlib only, on purpose —
see .claude/skills/notes-cli for the conventions before extending this.
"""

import argparse
import json
import os
import sys

STORE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes.json")


def load(path=STORE):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def save(notes, path=STORE):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(notes, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def add(text, path=STORE):
    if not text.strip():
        raise ValueError("note text must not be empty")
    notes = load(path)
    note = {"id": max((n["id"] for n in notes), default=0) + 1,
            "text": text.strip(),
            "done": False}
    notes.append(note)
    save(notes, path)
    return note


def done(note_id, path=STORE):
    notes = load(path)
    for note in notes:
        if note["id"] == note_id:
            note["done"] = True
            save(notes, path)
            return note
    raise KeyError("no note with id %d" % note_id)


def render(notes, show_all=False):
    rows = notes if show_all else [n for n in notes if not n["done"]]
    if not rows:
        return "no notes"
    return "\n".join("%s #%d %s" % ("x" if n["done"] else " ", n["id"], n["text"])
                     for n in rows)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="notes", description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="add a note")
    p_add.add_argument("text", nargs="+")

    p_list = sub.add_parser("list", help="list open notes")
    p_list.add_argument("--all", action="store_true", help="include done notes")

    p_done = sub.add_parser("done", help="mark a note done")
    p_done.add_argument("id", type=int)

    args = parser.parse_args(argv)

    if args.cmd == "add":
        try:
            note = add(" ".join(args.text))
        except ValueError as exc:
            print("notes: %s" % exc, file=sys.stderr)
            return 1
        print("added #%d" % note["id"])
    elif args.cmd == "list":
        print(render(load(), show_all=args.all))
    elif args.cmd == "done":
        try:
            note = done(args.id)
        except KeyError as exc:
            print(exc, file=sys.stderr)
            return 1
        print("done #%d" % note["id"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
