#!/usr/bin/env python3
"""
learnings.py — helper for the sharded Durable Learning store.

The store lives at:  memory/learnings/<namespace>/<date>-<key>.json
One learning per file. Namespaces:  global, fnx-pearl, sbdc, northfork, personal.
This replaces the single durable-learnings.jsonl so multiple AI instances can
write at once without ever touching the same file (no locks, no Drive conflicts).

Run it with `py learnings.py ...` on Windows or `python3 learnings.py ...`.

Commands
--------
  migrate <file.jsonl>   Split an old flat JSONL store into per-entry files.
  add                    Create one learning (flags below).
  list [--namespace N]   One-line index of active learnings (query with --grep TERM,
                         --skill NAME, --full KEY..., --all to include non-active).
  compile [--namespace N]  Rebuild read-only flat views under memory/learnings/_views/.
  prune                  List superseded / deprecated / expired entries to review (never deletes).

Add example
-----------
  py learnings.py add --namespace sbdc --key crm-bcc-postbox \
     --insight "{{CRM}} logs the session only if the follow-up email BCCs the postbox." \
     --type pitfall --confidence 9 --usefulness 9 --source user-stated \
     --evidence "{{USER}} confirmed 2026-08-15."
"""
import argparse, json, os, re, sys, datetime, subprocess

NAMESPACES = ["global", "fnx-pearl", "sbdc", "northfork", "personal"]


def _workspace_root():
    """LEARNINGS_ROOT env var, else the git top-level of the current directory, else the current directory."""
    env = os.environ.get("LEARNINGS_ROOT")
    if env:
        return os.path.abspath(env)
    try:
        r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, timeout=10)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except Exception:  # noqa: BLE001
        pass
    return os.getcwd()


ROOT = os.path.join(_workspace_root(), "memory", "learnings")


def slug(text, maxlen=60):
    s = re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")
    return (s[:maxlen].rstrip("-")) or "untitled"


def ns_dir(ns):
    if ns not in NAMESPACES:
        ns = "global"
    d = os.path.join(ROOT, ns)
    os.makedirs(d, exist_ok=True)
    return d


def entry_path(obj):
    ns = obj.get("namespace", "global")
    date = obj.get("saved") or obj.get("review_after") or datetime.date.today().isoformat()
    date = str(date)[:10]
    key = slug(obj.get("key") or obj.get("insight", "untitled"))
    return os.path.join(ns_dir(ns), f"{date}-{key}.json")


def write_entry(obj, force=False):
    path = entry_path(obj)
    if os.path.exists(path) and not force:
        return path, False
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return path, True


def iter_entries(namespace=None):
    targets = [namespace] if namespace else NAMESPACES
    for ns in targets:
        d = os.path.join(ROOT, ns)
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            if name.endswith(".json"):
                p = os.path.join(d, name)
                try:
                    with open(p, encoding="utf-8") as f:
                        yield ns, p, json.load(f)
                except Exception as e:
                    print(f"  ! unreadable {p}: {e}", file=sys.stderr)


def cmd_migrate(args):
    # Robust to lines that hold more than one JSON object concatenated
    # together (a concurrent-append collision) by decoding repeatedly.
    dec = json.JSONDecoder()
    written = skipped = bad = 0
    with open(args.file, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            s = line.strip()
            while s:
                try:
                    obj, end = dec.raw_decode(s)
                except json.JSONDecodeError as e:
                    bad += 1
                    print(f"  ! line {i} could not be parsed: {e}", file=sys.stderr)
                    break
                _, did = write_entry(obj, force=args.force)
                written += did
                skipped += (not did)
                s = s[end:].lstrip()
    print(f"migrated: {written} written, {skipped} already existed, {bad} unparseable")
    print(f"store: {ROOT}")


def cmd_add(args):
    obj = {
        "namespace": args.namespace,
        "memory_type": args.memory_type,
        "skill": args.skill,
        "type": args.type,
        "key": args.key,
        "insight": args.insight,
        "confidence": args.confidence,
        "usefulness": args.usefulness,
        "source": args.source,
        "evidence": args.evidence,
        "files": [],
        "status": "active",
        "lifecycle": args.lifecycle,
        "review_after": args.review_after,
        "saved": datetime.date.today().isoformat(),
    }
    path, did = write_entry(obj, force=args.force)
    print(("wrote " if did else "exists (use --force) ") + path)


def cmd_list(args):
    # Read-side query. Bare = one-line index; --grep/--skill/--full print whole rows.
    rows = [o for _ns, _p, o in iter_entries(args.namespace)
            if args.all or (o.get("status") or "active") == "active"]
    if args.full:
        rows = [o for o in rows if o.get("key") in set(args.full)]
    if args.skill:
        rows = [o for o in rows if o.get("skill") == args.skill]
    if args.grep:
        t = args.grep.lower()
        rows = [o for o in rows if t in json.dumps(o, ensure_ascii=False).lower()]
    if args.full or args.skill or args.grep:
        for o in rows:
            print(json.dumps(o, ensure_ascii=False))
        return
    for o in rows:
        ins = (o.get("insight") or "").replace("\n", " ")
        if len(ins) > 130:
            ins = ins[:130].rsplit(" ", 1)[0] + "..."
        print(f"{o.get('key','?')} [{o.get('namespace','?')}] {ins}")
    print(f"\n{len(rows)} learning(s).")


def cmd_compile(args):
    views = os.path.join(ROOT, "_views")
    os.makedirs(views, exist_ok=True)
    buckets = {}
    for ns, _p, o in iter_entries(args.namespace):
        buckets.setdefault(ns, []).append(o)
    for ns, objs in buckets.items():
        out = os.path.join(views, f"{ns}.jsonl")
        with open(out, "w", encoding="utf-8") as f:
            for o in objs:
                f.write(json.dumps(o, ensure_ascii=False) + "\n")
        print(f"compiled {len(objs):3} -> {out}")


def cmd_prune(args):
    today = datetime.date.today().isoformat()
    flagged = 0
    for ns, p, o in iter_entries(args.namespace):
        reasons = []
        if o.get("status") in ("superseded", "deprecated", "rejected"):
            reasons.append(o["status"])
        ra = o.get("review_after")
        if o.get("lifecycle") == "expires" and ra and str(ra) < today:
            reasons.append(f"expired {ra}")
        if reasons:
            flagged += 1
            print(f"[{ns}] {o.get('key','?')}  <- {', '.join(reasons)}\n      {p}")
    print(f"\n{flagged} entr(y/ies) to review. Nothing was deleted.")


def main():
    ap = argparse.ArgumentParser(description="Sharded durable-learning store helper.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("migrate"); m.add_argument("file"); m.add_argument("--force", action="store_true"); m.set_defaults(func=cmd_migrate)

    a = sub.add_parser("add")
    a.add_argument("--namespace", required=True, choices=NAMESPACES)
    a.add_argument("--key", required=True)
    a.add_argument("--insight", required=True)
    a.add_argument("--type", default="operational")
    a.add_argument("--memory-type", dest="memory_type", default="semantic")
    a.add_argument("--skill", default="manual")
    a.add_argument("--confidence", type=int, default=8)
    a.add_argument("--usefulness", type=int, default=8)
    a.add_argument("--source", default="user-stated")
    a.add_argument("--evidence", default="")
    a.add_argument("--lifecycle", default="stable")
    a.add_argument("--review-after", dest="review_after", default=None)
    a.add_argument("--force", action="store_true")
    a.set_defaults(func=cmd_add)

    l = sub.add_parser("list"); l.add_argument("--namespace", choices=NAMESPACES)
    l.add_argument("--grep", help="full rows whose JSON contains this term (case-insensitive)")
    l.add_argument("--skill", help="full rows for one task/skill name")
    l.add_argument("--full", nargs="+", metavar="KEY", help="full rows by key")
    l.add_argument("--all", action="store_true", help="include superseded/deprecated/rejected")
    l.set_defaults(func=cmd_list)
    c = sub.add_parser("compile"); c.add_argument("--namespace", choices=NAMESPACES); c.set_defaults(func=cmd_compile)
    p = sub.add_parser("prune"); p.add_argument("--namespace", choices=NAMESPACES); p.set_defaults(func=cmd_prune)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
