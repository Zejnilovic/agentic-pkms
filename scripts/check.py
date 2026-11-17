#!/usr/bin/env python3
"""Consistency checks for the kit. Run before committing: python3 scripts/check.py

Checks frontmatter, skill and agent references, links, README coverage, templates, version markers, packs,
the always-on word budget, the core skill description budget, names the kit must not use (tasks.md, inbox/,
pkm.sh, removed skills), shell script syntax, and (when mmdc is installed) Mermaid rendering. The working
agreement names the pkm version the kit needs, once, in a "pkm version --require <x.y>" line. With a checkout
of scripts-pkms (SCRIPTS_PKMS, or ../scripts-pkms), also that its VERSION is at least that, and that every
`pkm <command>` in a code span of kit/ or docs/ is in the output of `pkm help --all`. Without a checkout this
warns and skips; with CI set (GitHub sets it) it fails. Exits 1 if any problem is found.
"""

import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parent.parent
KIT = REPO / "kit"
AGENTS_DIR = KIT / ".claude/agents"
SKILLS_DIR = KIT / ".claude/skills"
TEMPLATES_DIR = KIT / "templates"
# The pkm command comes from a scripts-pkms checkout, installed once per machine; no pack depends on it.
SCRIPTS_PKMS = pathlib.Path(os.environ.get("SCRIPTS_PKMS") or REPO.parent / "scripts-pkms")
AGREEMENT_WORD_BUDGET = 700  # kit/AGENTS.md is loaded into every conversation
CORE_DESCRIPTION_BUDGET = 250  # words in the descriptions of the core pack's skills, loaded in every vault
AGENT_FIELDS = {"name", "description", "model", "skills"}
MODELS = {"haiku", "sonnet", "opus", "inherit"}
MARKER = "From agentic-pkms"
# Names the kit must not use: vaults no longer have these files or commands, so an agent would look for them.
FORBIDDEN_NAMES = {r"tasks\.md": "tasks.md", r"\binbox/": "inbox/", r"\bpkm\.sh\b": "pkm.sh"}
REMOVED_SKILLS = {"catalog", "daily-notes", "entities", "zettelkasten", "people", "vault-conventions", "reviews"}

problems = []
warnings = []


def rel(path):
    return path.relative_to(REPO).as_posix()


def frontmatter(path):
    text = path.read_text()
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        problems.append(f"{rel(path)}: no frontmatter")
        return {}, text
    fields, key = {}, None
    for line in match.group(1).splitlines():
        item = re.match(r"^\s+- (.+)$", line)
        if item:
            fields.setdefault(key, [])
            if isinstance(fields[key], list):
                fields[key].append(item.group(1).strip())
        else:
            key, _, value = line.partition(":")
            key = key.strip()
            fields[key] = value.strip() or []
    return fields, text


def mentions(text, kind):
    return set(re.findall(rf"`([a-z0-9-]+)` {kind}", text))


def without_code(text):
    return re.sub(r"```.*?```", "", text, flags=re.S)


skills, descriptions = {}, {}
for path in sorted(SKILLS_DIR.glob("*/SKILL.md")):
    fields, text = frontmatter(path)
    name, description = fields.get("name"), fields.get("description")
    if name != path.parent.name:
        problems.append(f"{rel(path)}: name '{name}' doesn't match folder '{path.parent.name}'")
    if not name or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
        problems.append(f"{rel(path)}: name must be lowercase words joined by hyphens, at most 64 characters")
    if not description or len(description) > 1024:
        problems.append(f"{rel(path)}: description missing or longer than 1024 characters")
    skills[path.parent.name] = text
    descriptions[path.parent.name] = description or ""

agents ={path.stem for path in AGENTS_DIR.glob("*.md")}
preloads = {}
for path in sorted(AGENTS_DIR.glob("*.md")):
    fields, text = frontmatter(path)
    if fields.get("name") != path.stem:
        problems.append(f"{rel(path)}: name '{fields.get('name')}' doesn't match file name")
    if not fields.get("description"):
        problems.append(f"{rel(path)}: no description")
    extra = set(fields) - AGENT_FIELDS
    if extra:
        problems.append(f"{rel(path)}: unsupported fields {sorted(extra)} (allowed: {sorted(AGENT_FIELDS)})")
    if "model" in fields and fields["model"] not in MODELS:
        problems.append(f"{rel(path)}: model '{fields['model']}' is not one of {sorted(MODELS)}")
    preload = fields.get("skills") if isinstance(fields.get("skills"), list) else []
    preloads[path.stem] = preload
    for skill in set(preload) - set(skills):
        problems.append(f"{rel(path)}: preloads missing skill '{skill}'")

for path in [KIT / "AGENTS.md", *SKILLS_DIR.glob("*/SKILL.md"), *AGENTS_DIR.glob("*.md")]:
    text = path.read_text()
    for skill in mentions(text, "skill") - set(skills):
        problems.append(f"{rel(path)}: refers to missing skill '{skill}'")
    for agent in mentions(text, "agent") - agents:
        problems.append(f"{rel(path)}: refers to missing agent '{agent}'")

# Names the vault no longer has: files, the old script name, and skills that were removed.
for path in KIT.rglob("*.md"):
    text = path.read_text()
    for pattern, name in FORBIDDEN_NAMES.items():
        if re.search(pattern, text):
            problems.append(f"{rel(path)}: names '{name}', which vaults no longer have")
    for skill in sorted(REMOVED_SKILLS):
        if re.search(rf"\.claude/skills/{skill}/|`{skill}` skill", text):
            problems.append(f"{rel(path)}: names removed skill '{skill}'")

for path in [REPO / "README.md", REPO / "CHANGELOG.md", REPO / "AGENTS.md", *REPO.glob("docs/*.md"), *KIT.rglob("*.md")]:
    for link in re.findall(r"\]\(([^)#\s]+)", without_code(path.read_text())):
        if not re.match(r"[a-z]+:", link) and not (path.parent / link).exists():
            problems.append(f"{rel(path)}: broken link '{link}'")

readme = (REPO / "README.md").read_text()
for path in [*AGENTS_DIR.glob("*.md"), *SKILLS_DIR.glob("*/SKILL.md"), *TEMPLATES_DIR.glob("*.md")]:
    if rel(path) not in readme:
        problems.append(f"README.md doesn't list {rel(path)}")

# Templates: notes copy them, so they carry no kit marker. Each typed template names its type.
for path in sorted(TEMPLATES_DIR.glob("*.md")):
    text = path.read_text()
    if MARKER in text:
        problems.append(f"{rel(path)}: templates must not carry the '{MARKER}' marker: every new note would copy it")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if match:
        found = re.search(r"^type: *(\S+)$", match.group(1), re.M)
        expected = "review" if path.stem.startswith("review-") else path.stem
        if not found or found.group(1) != expected:
            problems.append(f"{rel(path)}: frontmatter needs 'type: {expected}'")
    else:
        problems.append(f"{rel(path)}: no frontmatter")

if (KIT / "CLAUDE.md").read_text() != "@AGENTS.md\n":
    problems.append("kit/CLAUDE.md must contain only '@AGENTS.md'")

version = (REPO / "VERSION").read_text().strip()
agreement = (KIT / "AGENTS.md").read_text()
if "\n## This project" not in agreement:
    problems.append("kit/AGENTS.md has no '## This project' section (agd keeps everything from it down as the vault's)")
marker = re.search(r"agentic-pkms (\d+\.\d+\.\d+)", agreement)
if not marker or marker.group(1) != version:
    problems.append(f"kit/AGENTS.md version marker doesn't match VERSION {version}")


def as_tuple(number):
    return tuple(int(part) for part in number.split("."))


# The pkm version the kit needs is written once: a "pkm version --require <x.y>" line, in kit/AGENTS.md.
require_lines = [(rel(path), match.group(1)) for path in sorted(KIT.rglob("*.md"))
                 for match in re.finditer(r"pkm version --require (\d+\.\d+)(?![\d.])", path.read_text())]
required_version = None
if len(require_lines) == 0:
    problems.append("kit/AGENTS.md needs one 'pkm version --require <x.y>' line in 'Using pkm': found none")
elif len(require_lines) > 1:
    problems.append(f"the 'pkm version --require' line appears {len(require_lines)} times in kit/: keep exactly one, "
                    f"in kit/AGENTS.md")
elif require_lines[0][0] != "kit/AGENTS.md":
    problems.append(f"the 'pkm version --require' line is in {require_lines[0][0]}, not kit/AGENTS.md: "
                    f"the agreement is the only place that names the pkm version")
else:
    required_version = require_lines[0][1]
# CHANGELOG.md holds at most one entry, for the unreleased VERSION; released versions are links
# under "## Released" to their GitHub releases (scripts/release.py moves an entry there).
changelog = (REPO / "CHANGELOG.md").read_text()
entries = re.findall(r"^## (\d+\.\d+\.\d+)([^\n]*)\n(.*?)(?=^## |\Z)", changelog, re.M | re.S)
for entry_version, entry_heading, _ in entries:
    if entry_version != version or entry_heading != " (unreleased)":
        problems.append(f"CHANGELOG.md: '## {entry_version}{entry_heading}' isn't the unreleased VERSION {version}; "
                        f"released versions belong under '## Released' as links")
released_links = set(re.findall(r"^- \[(\d+\.\d+\.\d+)\]\(https://github\.com/[^)\s]+/releases/tag/v\1\) "
                                r"\(\d{4}-\d{2}-\d{2}\)$", changelog, re.M))


def git(*args):
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True)


def check_unreleased_entry():
    entry = next((body for v, heading, body in entries if v == version and heading == " (unreleased)"), None)
    if entry is None:
        problems.append(f"CHANGELOG.md has no '## {version} (unreleased)' entry for VERSION {version}")
    elif not re.search(r"^- \S", entry, re.M):
        problems.append(f"CHANGELOG.md's {version} entry has no bullet points describing the change")
    elif "TODO" in entry:
        problems.append(f"CHANGELOG.md's {version} entry still has a TODO: describe the change")


# Release rule: once VERSION is tagged as released, any change to kit/ or packs.txt needs a new version.
tag = f"v{version}"
if git("rev-parse", "--git-dir").returncode != 0:
    release_note = "release rule skipped (not a git repository)"
    if version not in released_links:
        check_unreleased_entry()
elif git("rev-parse", "-q", "--verify", f"refs/tags/{tag}").returncode == 0:
    release_note = f"released as {tag}"
    if any(v == version for v, _, _ in entries):
        problems.append(f"CHANGELOG.md: {version} is released as {tag}, so its entry belongs in the GitHub release, "
                        f"not under '## {version}'")
    released = ("kit", "packs.txt")
    changed = sorted(set(git("diff", "--name-only", tag, "--", *released).stdout.splitlines())
                     | set(git("ls-files", "--others", "--exclude-standard", "--", *released).stdout.splitlines()))
    if changed:
        listed = ", ".join(changed[:3]) + (f" and {len(changed) - 3} more" if len(changed) > 3 else "")
        problems.append(f"kit/ or packs.txt changed since {tag} was released ({listed}). Start a new version with "
                        f"'bash scripts/bump.sh <version>': patch for wording and fixes, minor for new agents, "
                        f"skills, templates or commands, major for renames or removals")
else:
    release_note = f"not released yet (no tag {tag})"
    check_unreleased_entry()

# Every released (tagged) version is linked under "## Released".
if git("rev-parse", "--git-dir").returncode == 0:
    for released in git("tag", "-l", "v*").stdout.split():
        if released[1:] not in released_links:
            problems.append(f"CHANGELOG.md: {released[1:]} is released as {released}, so '## Released' needs "
                            f"'- [{released[1:]}](https://github.com/<owner>/<repo>/releases/tag/{released}) (YYYY-MM-DD)'")

# packs.txt groups kit files into the packs agd installs. agd copies whole packs, keeps everything
# from "## This project" down as the vault's, and splits packs.txt and its lock file on spaces.
if git("rev-parse", "--git-dir").returncode == 0:
    listed = git("ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", "kit").stdout.split("\0")
    kit_files = sorted({p[len("kit/"):] for p in listed if p and (REPO / p).is_file()})
else:
    kit_files = sorted(p.relative_to(KIT).as_posix() for p in KIT.rglob("*") if p.is_file() and p.name != ".DS_Store")

packs_file = REPO / "packs.txt"
if not packs_file.exists():
    problems.append("packs.txt is missing: it lists the packs agd installs")
pack_paths, requires, min_agd, current = {}, {}, None, None
for number, line in enumerate(packs_file.read_text().splitlines() if packs_file.exists() else [], 1):
    words = line.split()
    if not words or words[0].startswith("#"):
        continue
    if line[0].isspace():
        if current and len(words) == 1:
            pack_paths[current].append(words[0])
            continue
    elif words[0] == "min-agd" and len(words) == 2 and re.fullmatch(r"\d+\.\d+\.\d+", words[1]):
        min_agd = words[1]
        continue
    elif (words[0] == "pack" and (len(words) == 2 or (len(words) > 3 and words[2] == "requires"))
          and re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", words[1]) and words[1] not in pack_paths):
        current = words[1]
        pack_paths[current], requires[current] = [], words[3:]
        continue
    problems.append(f"packs.txt:{number}: expected 'min-agd <version>', 'pack <new-name> [requires <pack> ...]' "
                    f"or an indented kit path without spaces")

if min_agd is None:
    problems.append("packs.txt needs a 'min-agd <version>' line: the oldest agd (github.com/Zejnilovic/agd) "
                    "that can install this kit")

owners = {path: [] for path in kit_files}
for pack, paths in pack_paths.items():
    for entry in paths:
        matched = [path for path in kit_files if path == entry or (entry.endswith("/") and path.startswith(entry))]
        if not matched:
            problems.append(f"packs.txt: '{entry}' in pack '{pack}' matches no file in kit/")
        for path in matched:
            owners[path].append(pack)
for path, packs in owners.items():
    if not packs:
        problems.append(f"kit/{path} isn't in any pack: add it to packs.txt")
    elif len(packs) > 1:
        problems.append(f"kit/{path} is listed more than once in packs.txt ({', '.join(packs)}): keep it in one pack")
    if re.search(r"\s", path):
        problems.append(f"kit/{path}: kit paths can't contain whitespace (agd splits packs.txt and its lock on spaces)")
    if path != "AGENTS.md" and re.search(r"^## This project[ \t]*$", (KIT / path).read_text(errors="replace"), re.M):
        problems.append(f"kit/{path} has a '## This project' heading. Only kit/AGENTS.md may: in vaults, "
                        f"agd keeps everything from that heading down as the vault's")


def packs_of(folder):
    return {pack for path in kit_files if path.startswith(folder) for pack in owners[path]}


def required(pack):
    """Every pack that pack needs, directly or through others."""
    found, todo = set(), list(requires.get(pack, []))
    while todo:
        other = todo.pop()
        if other not in found:
            found.add(other)
            todo.extend(requires.get(other, []))
    return found


for pack, needed in requires.items():
    for other in needed:
        if ":" in other:
            problems.append(f"packs.txt: pack '{pack}' requires '{other}': the kit has no packs from other sources; "
                            f"pkm is installed once per machine, not as a pack")
        elif other not in requires:
            problems.append(f"packs.txt: pack '{pack}' requires '{other}', which isn't a pack")
    if pack in required(pack):
        problems.append(f"packs.txt: pack '{pack}' requires itself through a cycle")
if requires.get("core"):
    problems.append("packs.txt: pack 'core' requires nothing: pkm is installed once per machine")

for skill in skills:
    split = sorted(packs_of(f".claude/skills/{skill}/"))
    if len(split) > 1:
        problems.append(f"kit/.claude/skills/{skill}/ is split across packs ({', '.join(split)}): "
                        f"a skill folder belongs to one pack")

for pack in pack_paths:
    if f"| `{pack}` |" not in readme:
        problems.append(f"README.md has no row for pack '{pack}' in its packs table")

core_skills = [skill for skill in skills if "core" in packs_of(f".claude/skills/{skill}/")]
core_words = sum(len(descriptions[skill].split()) for skill in core_skills)
if core_words > CORE_DESCRIPTION_BUDGET:
    problems.append(f"the core skills' descriptions total {core_words} words, over the "
                    f"{CORE_DESCRIPTION_BUDGET}-word budget: vaults load them in every conversation")

for agent, preload in preloads.items():
    path = f".claude/agents/{agent}.md"
    if len(owners.get(path, [])) != 1:
        continue
    pack = owners[path][0]
    for skill in preload:
        outside = sorted(packs_of(f".claude/skills/{skill}/") - {pack} - required(pack))
        if outside:
            problems.append(f"kit/{path} preloads the '{skill}' skill from pack '{outside[0]}', "
                            f"which pack '{pack}' doesn't require")

# The skills and agents call pkm. Each `pkm <command>` in a code span of kit/ or docs/ must be listed by the
# checkout's `bin/pkm help --all`, and the checkout's VERSION must be at least the version the agreement requires.
# Without a checkout this only warns; in CI (GitHub sets CI) it fails, because CI must check the commands.
checkout = SCRIPTS_PKMS / "bin/pkm"
if checkout.is_file():
    listing = subprocess.run(["bash", str(checkout), "help", "--all"], capture_output=True, text=True,
                             stdin=subprocess.DEVNULL)
    commands = {line.split("\t")[0] for line in listing.stdout.splitlines() if line.strip()}
    if listing.returncode != 0 or not commands:
        problems.append(f"'{checkout} help --all' printed no commands (exit {listing.returncode})")
    version_file = SCRIPTS_PKMS / "VERSION"
    checkout_version = version_file.read_text().strip() if version_file.is_file() else ""
    if not checkout_version:
        problems.append(f"{version_file} is missing: the checkout's pkm version is unknown")
    elif required_version and as_tuple(required_version) > as_tuple(checkout_version):
        problems.append(f"kit/AGENTS.md requires pkm {required_version}, but the scripts-pkms checkout is {checkout_version}")
    for path in [*KIT.rglob("*.md"), *(REPO / "docs").glob("*.md")]:
        for span in re.findall(r"`([^`\n]+)`", without_code(path.read_text())):
            for match in re.finditer(r"\bpkm\s+([a-z][a-z-]*)", span):
                if match.group(1) not in commands:
                    problems.append(f"{rel(path)}: `{match.group(0)}` is not a command in `pkm help --all` of {SCRIPTS_PKMS}")
    script_note = f"commands and version checked against scripts-pkms {checkout_version or '(no version)'}"
elif os.environ.get("CI"):
    problems.append(f"no scripts-pkms checkout at {SCRIPTS_PKMS}: CI must check out scripts-pkms, so the pkm "
                    f"commands and version can be checked")
    script_note = "commands and version not checked (no scripts-pkms checkout)"
else:
    warnings.append(f"no scripts-pkms checkout at {SCRIPTS_PKMS}: pkm commands and version not checked. Clone "
                    f"scripts-pkms next to this repo or set SCRIPTS_PKMS")
    script_note = "commands and version not checked (no scripts-pkms checkout)"

# Only the kit's part counts: vaults replace everything from "## This project" down with their own.
words = len(agreement.split("\n## This project", 1)[0].split())
if words > AGREEMENT_WORD_BUDGET:
    problems.append(f"kit/AGENTS.md has {words} words above 'This project', over the {AGREEMENT_WORD_BUDGET}-word budget")

# Kit-owned files say so, so agents in a vault know not to edit them. Templates are exempt (see above).
marked = [*AGENTS_DIR.glob("*.md"), *SKILLS_DIR.glob("*/SKILL.md"), *KIT.rglob("*.sh"), KIT / "AGENTS.md"]
for path in marked:
    if MARKER not in path.read_text()[:1500]:
        problems.append(f"{rel(path)}: missing the '{MARKER}' marker near the top")

for script_path in [*KIT.rglob("*.sh"), *(REPO / "scripts").glob("*.sh")]:
    result = subprocess.run(["bash", "-n", str(script_path)], capture_output=True, text=True)
    if result.returncode != 0:
        problems.append(f"{rel(script_path)}: syntax error: {result.stderr.strip()}")

mermaid_files = [p for p in [REPO / "README.md", *REPO.glob("docs/*.md"), *KIT.rglob("*.md")]
                 if "```mermaid" in p.read_text()]
if os.environ.get("AGENTIC_PKMS_SKIP_MERMAID"):
    mermaid_note = "Mermaid rendering skipped (AGENTIC_PKMS_SKIP_MERMAID is set)"
elif shutil.which("mmdc"):
    with tempfile.TemporaryDirectory() as out:
        for path in mermaid_files:
            result = subprocess.run(["mmdc", "-q", "-i", str(path), "-o", f"{out}/{path.name}"],
                                    capture_output=True, text=True)
            if result.returncode != 0:
                problems.append(f"{rel(path)}: Mermaid diagram doesn't render: {result.stderr.strip()[:200]}")
    mermaid_note = f"{len(mermaid_files)} files with diagrams rendered"
else:
    mermaid_note = "Mermaid rendering skipped (mmdc not installed)"

print(f"Checked {len(skills)} skills, {len(agents)} agents, {len(list(TEMPLATES_DIR.glob('*.md')))} templates, "
      f"kit/AGENTS.md at {words}/{AGREEMENT_WORD_BUDGET} words, core descriptions at {core_words}/"
      f"{CORE_DESCRIPTION_BUDGET} words, version {version} {release_note}, {script_note}. {mermaid_note}.")
if warnings:
    print("\nWarnings:")
    for warning in warnings:
        print(f"- {warning}")
if problems:
    print("\nProblems:")
    for problem in problems:
        print(f"- {problem}")
    sys.exit(1)
print("No problems found.")
