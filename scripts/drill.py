#!/usr/bin/env python3
"""Drills: the kit's skills tried by a real assistant on a made-up vault, and the result graded.

A drill is a folder in tests/drills/<name>/ with drill.json (the request in turns, the repositories a fake gh
serves, and what the vault must look like after) and vault/, files laid over the base vault. Drills cost model
calls, so neither check.py nor CI runs them.

  python3 scripts/drill.py list
  python3 scripts/drill.py run <name> [--model haiku] [--dir <folder>]    drives claude -p, turn by turn, then grades
  python3 scripts/drill.py setup <name> <folder>                          a vault to try by hand, as with Copilot
  python3 scripts/drill.py mark <folder>                                  after the first answer, in a run by hand
  python3 scripts/drill.py check <name> <folder>                          grades a vault

pkm comes from SCRIPTS_PKMS (or ../scripts-pkms), so the drill uses the version the kit requires.
"""

import argparse
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parent.parent
DRILLS = REPO / "tests/drills"
KIT = REPO / "kit"
SCRIPTS_PKMS = pathlib.Path(os.environ.get("SCRIPTS_PKMS") or REPO.parent / "scripts-pkms")
# What the assistant may run in a drill: pkm, the fake gh, jq, and file tools. acceptEdits also lets it edit files
# and run file commands such as mkdir and mv in the vault, as an assistant in a vault usually can; anything else is
# refused.
ALLOWED_TOOLS = ["Bash(pkm:*)", "Bash(gh:*)", "Bash(jq:*)", "Bash(ls:*)", "Read", "Edit", "Write", "Glob", "Grep",
                 "Skill"]

FAKE_GH = r'''#!/usr/bin/env python3
"""A fake gh for drills: serves the repositories of gh-data.json, and logs every call to gh.log."""
import json, pathlib, subprocess, sys
here = pathlib.Path(__file__).resolve().parent
args = sys.argv[1:]
with open(here.parent / "gh.log", "a") as log:
    log.write(json.dumps(args) + "\n")
data = json.loads((here / "gh-data.json").read_text())

def option(name, default=None):
    for i, a in enumerate(args):
        if a == name and i + 1 < len(args):
            return args[i + 1]
        if a.startswith(name + "="):
            return a.split("=", 1)[1]
    return default

def emit(rows):
    fields = option("--json")
    if fields:
        rows = [{k: r.get(k) for k in fields.split(",")} for r in rows]
        text = json.dumps(rows)
        jq = option("--jq") or option("-q")
        if jq:
            sys.exit(subprocess.run(["jq", "-r", jq], input=text, text=True).returncode)
        print(text)
    else:
        for r in rows:
            print(f"{r['url'].split('github.com/')[1]}\t{r.get('description', '')}\t{'archived' if r['isArchived'] else 'public'}")

if args[:2] == ["auth", "status"]:
    print("github.com: logged in as drill-user"); sys.exit(0)
if args[:2] == ["repo", "list"]:
    owner = next((a for a in args[2:] if not a.startswith("-") and a not in (option("--json"), option("--jq"), option("--limit"), option("-L"), option("-q"))), None)
    if owner not in data:
        print(f"no organization {owner}", file=sys.stderr); sys.exit(1)
    emit(data[owner])
    sys.exit(0)
if args[:2] == ["search", "repos"]:
    words = [a for a in args[2:] if not a.startswith("-") and a not in (option("--owner"), option("--json"), option("--jq"), option("--limit"), option("-L"))]
    owners = [option("--owner")] if option("--owner") else list(data)
    rows = [r for o in owners for r in data.get(o, []) if all(w.lower() in r["name"].lower() for w in words)]
    emit(rows)
    sys.exit(0)
print("drill: gh " + " ".join(args) + " is not available in this drill", file=sys.stderr)
sys.exit(1)
'''


def load(name):
    path = DRILLS / name / "drill.json"
    if not path.exists():
        sys.exit(f"No drill {name}: python3 scripts/drill.py list")
    return json.loads(path.read_text())


def pkm_bin():
    pkm = SCRIPTS_PKMS / "bin/pkm"
    if not pkm.exists():
        sys.exit(f"No pkm at {pkm}: clone scripts-pkms next to this repo, or set SCRIPTS_PKMS.")
    return pkm


def environment(run, drill):
    env = dict(os.environ)
    env["PATH"] = f"{run / 'bin'}{os.pathsep}{env.get('PATH', '')}"
    env["PKM_NOW"] = drill["now"]
    env.pop("PKM_VAULT", None)
    return env


def snapshot(vault):
    """sha256 of every file in the vault, except pkm's cache and state, by path."""
    result = {}
    for path in sorted(vault.rglob("*")):
        rel = path.relative_to(vault).as_posix()
        if path.is_file() and not rel.startswith((".pkm/cache", ".pkm/state")):
            result[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def setup(name, run):
    """Makes run/vault (the base vault, the drill's files and the kit) and run/bin (pkm and the fake gh)."""
    drill = load(name)
    if run.exists() and any(run.iterdir()):
        sys.exit(f"{run} is not empty.")
    vault, bin_dir = run / "vault", run / "bin"
    shutil.copytree(REPO / drill["base"], vault, ignore=shutil.ignore_patterns("cache", "state"))
    overlay = DRILLS / name / "vault"
    if overlay.exists():
        shutil.copytree(overlay, vault, dirs_exist_ok=True)
    for item in KIT.iterdir():
        target = vault / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)
    bin_dir.mkdir(parents=True)
    (bin_dir / "pkm").symlink_to(pkm_bin())
    (bin_dir / "gh").write_text(FAKE_GH)
    (bin_dir / "gh").chmod(0o755)
    (bin_dir / "gh-data.json").write_text(json.dumps(drill["gh_repos"], indent=2))
    (run / "start.json").write_text(json.dumps({"drill": name, "files": snapshot(vault)}, indent=2))
    return drill


def mark(run):
    """After the first answer: records which files it changed, for the proposal-first check."""
    start = json.loads((run / "start.json").read_text())
    now = snapshot(run / "vault")
    changed = sorted(p for p in set(start["files"]) | set(now) if start["files"].get(p) != now.get(p))
    (run / "turn1.json").write_text(json.dumps({"changed": changed}, indent=2))
    return changed


def frontmatter(text):
    match = re.match(r"^﻿?---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    fields = {}
    if match:
        for line in match.group(1).splitlines():
            key = re.match(r"^([A-Za-z0-9_-]+):(.*)$", line)
            if key:
                fields[key.group(1)] = key.group(2).strip()
    return fields, text[match.end():] if match else text


def bare(value):
    value = value.strip().strip("\"'")
    if value.startswith("[[") and value.endswith("]]"):
        value = value[2:-2].split("|")[0]
    return value


def note_paths(vault):
    """name -> path of each note (not a day or close page), by file name."""
    paths = {}
    for path in vault.rglob("*.md"):
        rel = path.relative_to(vault).as_posix()
        if rel.startswith(("daybook/", "closes/", ".claude/", "templates/")) or path.name in ("AGENTS.md", "CLAUDE.md", "README.md"):
            continue
        paths.setdefault(path.stem, []).append(rel)
    return paths


def check(name, run):
    """Grades run/vault against the drill. Prints one line per check and returns the number that failed."""
    drill, vault = load(name), run / "vault"
    start = json.loads((run / "start.json").read_text())["files"]
    expect = drill["expect"]
    results = []

    def record(ok, label, detail="", warn=False):
        results.append({"ok": bool(ok), "check": label, "detail": detail, "warn": warn})

    turn1 = run / "turn1.json"
    if turn1.exists():
        changed = [p for p in json.loads(turn1.read_text())["changed"] if not p.startswith(".pkm/moves")]
        record(not changed, "proposal first: nothing written before the owner's yes", ", ".join(changed))
    else:
        record(False, "proposal first: nothing written before the owner's yes", "no turn1.json: run mark after the first answer")

    paths = note_paths(vault)
    for note, want in expect["notes"].items():
        found = paths.get(note, [])
        if len(found) != 1:
            record(False, f"{note}: one note", f"found {found or 'none'}")
            continue
        places = want["path"] if isinstance(want["path"], list) else [want["path"]]
        record(found[0] in places, f"{note}: at {' or '.join(places)}", found[0])
        fields, _ = frontmatter((vault / found[0]).read_text())
        if "type" in want:
            record(fields.get("type") == want["type"], f"{note}: type {want['type']}", fields.get("type", "none"))
        for key, value in want.get("fields", {}).items():
            got = fields.get(key, "")
            same = bare(got) == value or (key == "url" and re.sub(r"(\.git)?/*$", "", bare(got)) == value)
            record(same, f"{note}: {key} {value}", got or "empty")

    for note in expect.get("absent", []):
        record(note not in paths, f"no note {note}", ", ".join(paths.get(note, [])))

    urls = {}
    for note, found in paths.items():
        for rel in found:
            if rel.startswith("archive/"):
                continue
            url = frontmatter((vault / rel).read_text())[0].get("url")
            if url:
                urls.setdefault(url.rstrip("/"), []).append(note)
    doubles = {u: n for u, n in urls.items() if len(n) > 1}
    record(not doubles, "one note per repository", "; ".join(f"{u}: {', '.join(n)}" for u, n in doubles.items()))

    for rel in expect.get("unchanged", []) + [p for p in start if p.startswith("daybook/")]:
        now = vault / rel
        same = now.exists() and hashlib.sha256(now.read_bytes()).hexdigest() == start.get(rel)
        record(same, f"{rel} unchanged")

    base_vault = REPO / drill["base"]
    overlay = DRILLS / name / "vault"
    for note in expect.get("body_unchanged", []):
        before = next((p for folder in (overlay, base_vault) if folder.exists() for p in sorted(folder.rglob(f"{note}.md"))), None)
        found = paths.get(note, [])
        if before is None or len(found) != 1:
            record(False, f"{note}: the owner's text unchanged", "note missing")
            continue
        record(frontmatter(before.read_text())[1] == frontmatter((vault / found[0]).read_text())[1],
               f"{note}: the owner's text unchanged")

    descriptions = [r["description"] for repos in drill["gh_repos"].values() for r in repos if r.get("description")]
    copied = [d for d in descriptions for path in vault.rglob("*.md")
              if not path.relative_to(vault).as_posix().startswith(".claude/") and d in path.read_text()]
    record(not copied, "nothing copied from the tool", "; ".join(sorted(set(copied))))

    moves = (vault / ".pkm/moves.tsv").read_text() if (vault / ".pkm/moves.tsv").exists() else ""
    start_paths = {pathlib.PurePosixPath(p).stem: p for p in start if p.endswith(".md")}
    for note, found in paths.items():
        if note in start_paths and found and found[0] != start_paths[note]:
            record(f"\t{found[0]}" in moves, f"{note}: moved with pkm", f"{start_paths[note]} -> {found[0]}")

    pkm_check = subprocess.run([str(pkm_bin()), "--vault", str(vault), "check"], capture_output=True, text=True,
                               env=environment(run, drill))
    problems = pkm_check.stdout.split("Problems:")[1].split("Notices:")[0].strip() if "Problems:" in pkm_check.stdout else ""
    record(pkm_check.returncode == 0, "pkm check finds no problems", problems.replace("\n", " "))
    notices = pkm_check.stdout.split("Notices:")[1] if "Notices:" in pkm_check.stdout else ""
    for words in expect.get("notices_absent", []):
        left = [line for line in notices.splitlines() if words in line]
        record(not left, f"pkm check has no notice with \"{words}\"", " ".join(left))

    transcript = run / "transcript.json"
    if transcript.exists():
        outside = looked_outside_pkm(json.loads(transcript.read_text()))
        record(not outside, "looked at the vault with pkm only", f"{len(outside)} times, such as: {outside[0][:120]}" if outside else "",
               warn=True)

    graded = [r for r in results if not r["warn"]]
    failed = [r for r in graded if not r["ok"]]
    for r in results:
        mark = "PASS" if r["ok"] else ("WARN" if r["warn"] else "FAIL")
        print(f"{mark}  {r['check']}" + (f"  ({r['detail']})" if r["detail"] and not r["ok"] else ""))
    warned = sum(1 for r in results if r["warn"] and not r["ok"])
    print(f"\n{name}: {len(graded) - len(failed)}/{len(graded)} checks passed" + (f", {warned} warning." if warned else "."))
    (run / "result.json").write_text(json.dumps(results, indent=2))
    return len(failed)


READERS = {"ls", "cat", "find", "grep", "rg", "head", "tail", "sed", "awk", "less", "tree"}
KIT_FILES = (".claude/", "AGENTS.md", "CLAUDE.md", ".pkm/", "gh-data.json")


def looked_outside_pkm(log):
    """The tool calls that read the vault without pkm: ls, cat, find and the like in Bash, and the Read, Grep and
    Glob tools, except on the kit's own files and pkm's settings."""
    found = []
    for turn in log:
        for tool in turn.get("tools", []):
            name, _, rest = tool.partition(": ")
            if name == "Bash":
                for part in re.split(r"&&|\|\||;", rest):
                    part = part.split("|")[0]  # what a pipe feeds into only filters
                    words = part.strip().lstrip("(").split()
                    if words and words[0] in READERS and not any(k in part for k in KIT_FILES):
                        found.append(part.strip())
            elif name in ("Read", "Grep", "Glob") and not any(k in rest for k in KIT_FILES):
                found.append(tool)
    return found


def claude_turn(text, run, drill, model, session):
    """One turn of claude -p. Returns its result event, with "tools": each tool call of the turn, in order."""
    command = ["claude", "-p", text, "--model", model, "--output-format", "stream-json", "--verbose",
               "--permission-mode", "acceptEdits", "--setting-sources", "project,local", "--strict-mcp-config",
               "--allowedTools", *ALLOWED_TOOLS]
    if session:
        command += ["--resume", session]
    done = subprocess.run(command, cwd=run / "vault", env=environment(run, drill), capture_output=True, text=True,
                          timeout=900)
    tools, answer = [], None
    for line in done.stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "assistant":
            for part in event.get("message", {}).get("content", []):
                if part.get("type") == "tool_use":
                    data = part.get("input", {})
                    tools.append(f"{part.get('name')}: {data.get('command') or data.get('skill') or data.get('file_path') or json.dumps(data)[:200]}")
        elif event.get("type") == "result":
            answer = event
    if answer is None:
        sys.exit(f"claude gave no result (exit {done.returncode}): {done.stderr[-2000:]}")
    answer["tools"] = tools
    return answer


def run_drill(name, model, folder):
    run = pathlib.Path(folder) if folder else pathlib.Path(tempfile.mkdtemp(prefix=f"drill-{name}-"))
    drill = setup(name, run)
    if not shutil.which("claude"):
        sys.exit("claude is not on PATH. Try the drill by hand: python3 scripts/drill.py setup " + name + " <folder>")
    print(f"Drill {name} with {model} in {run}")
    session, log = None, []
    for i, text in enumerate(drill["turns"], 1):
        answer = claude_turn(text, run, drill, model, session)
        session = answer.get("session_id", session)
        log.append({"turn": i, "owner": text, "assistant": answer.get("result", ""),
                    "cost_usd": answer.get("total_cost_usd"), "turns": answer.get("num_turns"),
                    "tools": answer["tools"]})
        print(f"\n--- turn {i}: {text}")
        for tool in answer["tools"]:
            print(f"  > {tool}")
        print(f"\n{answer.get('result', '').strip()}\n")
        if i == 1:
            mark(run)
        elif check_quietly(name, run) == 0:
            break
    (run / "transcript.json").write_text(json.dumps(log, indent=2))
    cost = sum(t["cost_usd"] or 0 for t in log)
    print(f"--- {len(log)} turns, ${cost:.3f}. Transcript: {run / 'transcript.json'}, gh calls: {run / 'gh.log'}\n")
    return check(name, run)


def check_quietly(name, run):
    stdout = sys.stdout
    try:
        sys.stdout = open(os.devnull, "w")
        return check(name, run)
    finally:
        sys.stdout.close()
        sys.stdout = stdout


def main():
    parser = argparse.ArgumentParser(description="Drills: the kit tried by an assistant on a made-up vault.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list")
    p = sub.add_parser("run"); p.add_argument("name"); p.add_argument("--model", default="haiku"); p.add_argument("--dir")
    p = sub.add_parser("setup"); p.add_argument("name"); p.add_argument("folder")
    p = sub.add_parser("mark"); p.add_argument("folder")
    p = sub.add_parser("check"); p.add_argument("name"); p.add_argument("folder")
    args = parser.parse_args()
    if args.command == "list":
        for path in sorted(DRILLS.glob("*/drill.json")):
            print(f"{path.parent.name}\t{json.loads(path.read_text())['title']}")
    elif args.command == "run":
        sys.exit(1 if run_drill(args.name, args.model, args.dir) else 0)
    elif args.command == "setup":
        run = pathlib.Path(args.folder).resolve()
        drill = setup(args.name, run)
        print(f"Vault: {run / 'vault'}\nIn a terminal there:\n  export PATH=\"{run / 'bin'}:$PATH\" PKM_NOW={drill['now']}\n"
              f"Then give your assistant these turns, one at a time:")
        for i, text in enumerate(drill["turns"], 1):
            print(f"  {i}. {text}")
        print(f"After its first answer: python3 scripts/drill.py mark {run}\n"
              f"At the end: python3 scripts/drill.py check {args.name} {run}")
    elif args.command == "mark":
        changed = mark(pathlib.Path(args.folder).resolve())
        print("Nothing written yet." if not changed else "Written before a yes: " + ", ".join(changed))
    elif args.command == "check":
        sys.exit(1 if check(args.name, pathlib.Path(args.folder).resolve()) else 0)


if __name__ == "__main__":
    main()
