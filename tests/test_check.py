"""Tests for scripts/check.py: the pkm version line, packs.txt and the word budget.

Each test runs check.py on a temporary copy of this repo, with a fake scripts-pkms checkout, so a test
changes only what it says. Run from the repo root: python3 -m unittest discover -s tests
"""

import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = pathlib.Path(__file__).resolve().parent.parent
COPY_IGNORE = shutil.ignore_patterns(".git", ".local_context", "__pycache__", ".agd.lock")
REQUIRE = "pkm version --require 0.1"
FAKE_PKM = "#!/bin/bash\nprintf 'version\\tSetup\\tthe release\\nevidence\\tCheck\\tlinks\\n'\n"


class CheckCase(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.repo = self.tmp / "repo"
        shutil.copytree(REPO, self.repo, ignore=COPY_IGNORE)
        self.checkout = self.tmp / "scripts-pkms"
        (self.checkout / "bin").mkdir(parents=True)
        (self.checkout / "VERSION").write_text("0.1.0\n")
        (self.checkout / "bin" / "pkm").write_text(FAKE_PKM)

    def edit(self, relative, old, new):
        path = self.repo / relative
        text = path.read_text()
        self.assertIn(old, text, f"{relative} doesn't contain the text to change")
        path.write_text(text.replace(old, new, 1))

    def run_check(self):
        env = dict(os.environ, SCRIPTS_PKMS=str(self.checkout))
        result = subprocess.run([sys.executable, str(self.repo / "scripts" / "check.py")], cwd=self.repo, env=env,
                                capture_output=True, text=True, stdin=subprocess.DEVNULL)
        return result.returncode, result.stdout


class VersionLine(CheckCase):
    def test_missing_line_is_reported(self):
        self.edit("kit/AGENTS.md", REQUIRE, "pkm version")
        _, out = self.run_check()
        self.assertIn("needs one 'pkm version --require <x.y>' line in 'Using pkm': found none", out)

    def test_two_lines_are_reported(self):
        self.edit("kit/AGENTS.md", "## Done means", f"Run `{REQUIRE}` again.\n\n## Done means")
        _, out = self.run_check()
        self.assertIn("appears 2 times in kit/", out)

    def test_line_outside_the_agreement_is_reported(self):
        self.edit("kit/AGENTS.md", REQUIRE, "pkm version")
        skill = self.repo / "kit/.claude/skills/tasks/SKILL.md"
        skill.write_text(skill.read_text() + f"\nRun `{REQUIRE}` first.\n")
        _, out = self.run_check()
        self.assertIn("the 'pkm version --require' line is in kit/.claude/skills/tasks/SKILL.md, not kit/AGENTS.md", out)

    def test_newer_than_the_checkout_is_reported(self):
        self.edit("kit/AGENTS.md", REQUIRE, "pkm version --require 0.2")
        _, out = self.run_check()
        self.assertIn("kit/AGENTS.md requires pkm 0.2, but the scripts-pkms checkout is 0.1.0", out)

    def test_same_version_as_the_checkout_passes(self):
        _, out = self.run_check()
        self.assertNotIn("requires pkm", out)
        self.assertNotIn("pkm version --require", out)


class Packs(CheckCase):
    def test_scripts_pkms_requirement_is_rejected(self):
        self.edit("packs.txt", "pack coaching requires core", "pack coaching requires core scripts-pkms:core")
        _, out = self.run_check()
        self.assertIn("pack 'coaching' requires 'scripts-pkms:core': the kit has no packs from other sources", out)

    def test_core_requiring_anything_is_rejected(self):
        self.edit("packs.txt", "pack core\n", "pack core requires coaching\n")
        _, out = self.run_check()
        self.assertIn("pack 'core' requires nothing", out)


class WordBudget(CheckCase):
    def test_over_the_budget_is_reported(self):
        self.edit("kit/AGENTS.md", "## Kit files", ("word " * 800) + "\n\n## Kit files")
        _, out = self.run_check()
        self.assertIn("over the 700-word budget", out)

    def test_the_real_agreement_is_within_the_budget(self):
        _, out = self.run_check()
        self.assertNotIn("words above 'This project'", out)


class PkmCommands(CheckCase):
    def test_unknown_command_in_a_code_span_is_reported(self):
        skill = self.repo / "kit/.claude/skills/tasks/SKILL.md"
        skill.write_text(skill.read_text() + "\nRun `pkm frobnicate` first.\n")
        _, out = self.run_check()
        self.assertIn("`pkm frobnicate` is not a command in `pkm help --all`", out)

    def test_missing_checkout_warns_and_skips(self):
        shutil.rmtree(self.checkout)
        code, out = self.run_checkout_env(remove=("SCRIPTS_PKMS", "CI"))
        self.assertEqual(code, 0, out)
        self.assertIn("Warnings:", out)
        self.assertIn("pkm commands and version not checked", out)

    def test_missing_checkout_fails_in_ci(self):
        shutil.rmtree(self.checkout)
        code, out = self.run_checkout_env(remove=("SCRIPTS_PKMS",), extra={"CI": "true"})
        self.assertEqual(code, 1)
        self.assertIn("CI must check out scripts-pkms", out)

    def run_checkout_env(self, remove=(), extra=None):
        env = {key: value for key, value in os.environ.items() if key not in remove}
        env.update(extra or {})
        result = subprocess.run([sys.executable, str(self.repo / "scripts" / "check.py")], cwd=self.repo, env=env,
                                capture_output=True, text=True, stdin=subprocess.DEVNULL)
        return result.returncode, result.stdout


class KitNames(CheckCase):
    def add_to_tasks_skill(self, text):
        skill = self.repo / "kit/.claude/skills/tasks/SKILL.md"
        skill.write_text(skill.read_text() + f"\n{text}\n")

    def test_tasks_md_is_reported(self):
        self.add_to_tasks_skill("Keep waiting tasks in tasks.md.")
        _, out = self.run_check()
        self.assertIn("names 'tasks.md', which vaults no longer have", out)

    def test_inbox_is_reported(self):
        self.add_to_tasks_skill("Capture it in inbox/ first.")
        _, out = self.run_check()
        self.assertIn("names 'inbox/', which vaults no longer have", out)

    def test_pkm_sh_is_reported(self):
        self.add_to_tasks_skill("Run pkm.sh check after.")
        _, out = self.run_check()
        self.assertIn("names 'pkm.sh', which vaults no longer have", out)

    def test_removed_skill_is_reported(self):
        self.add_to_tasks_skill("See the `catalog` skill for filing.")
        _, out = self.run_check()
        self.assertIn("names removed skill 'catalog'", out)


class CoreDescriptions(CheckCase):
    def test_over_the_budget_is_reported(self):
        self.edit("kit/.claude/skills/vault-search/SKILL.md", "description: Finds things",
                  "description: " + ("word " * 200) + "Finds things")
        _, out = self.run_check()
        self.assertRegex(out, r"core skills' descriptions total \d+ words, over the 250-word budget")

    def test_the_real_descriptions_are_within_the_budget(self):
        _, out = self.run_check()
        self.assertNotIn("over the 250-word budget", out)


class ReadmePacks(CheckCase):
    def test_pack_without_a_readme_row_is_reported(self):
        self.edit("README.md", "| `ledger` |", "| `money` |")
        _, out = self.run_check()
        self.assertIn("README.md has no row for pack 'ledger'", out)


if __name__ == "__main__":
    unittest.main()
