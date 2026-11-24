"""Tests for scripts/drill.py: each drill's own solution passes its grader, and the messes a weak assistant makes fail.

They run pkm from a scripts-pkms checkout (SCRIPTS_PKMS, or ../scripts-pkms) and skip without one, as check.py
warns. No model is called. Run from the repo root: python3 -m unittest discover -s tests
"""

import contextlib
import io
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
import drill  # noqa: E402

DRILL_NAMES = sorted(p.parent.name for p in (REPO / "tests/drills").glob("*/drill.json"))


@unittest.skipUnless((drill.SCRIPTS_PKMS / "bin/pkm").exists(), "needs a scripts-pkms checkout")
class DrillCase(unittest.TestCase):
    def start(self, name):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.run_dir = pathlib.Path(self.tmp.name) / "run"
        self.drill = drill.setup(name, self.run_dir)
        self.vault = self.run_dir / "vault"
        self.name = name

    def pkm(self, *args):
        env = drill.environment(self.run_dir, self.drill)
        done = subprocess.run(["pkm", "--vault", str(self.vault), *args], env=env, capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)

    def grade(self):
        """The checks that failed, by label."""
        with contextlib.redirect_stdout(io.StringIO()):
            drill.check(self.name, self.run_dir)
        results = json.loads((self.run_dir / "result.json").read_text())
        return [r["check"] for r in results if not r["ok"]]

    def solve(self):
        drill.mark(self.run_dir)
        for args in self.drill["solution"]:
            self.pkm(*args)


class Solutions(DrillCase):
    def test_each_solution_passes(self):
        for name in DRILL_NAMES:
            with self.subTest(name):
                self.start(name)
                self.solve()
                self.assertEqual(self.grade(), [])


class Messes(DrillCase):
    def test_writing_before_the_yes_fails(self):
        self.start("connect-repos")
        self.pkm(*self.drill["solution"][1])
        drill.mark(self.run_dir)
        self.assertIn("proposal first: nothing written before the owner's yes", self.grade())

    def test_a_hand_made_note_in_the_wrong_place_fails(self):
        self.start("project-folders")
        drill.mark(self.run_dir)
        self.pkm("new", "project", "hermes")
        (self.vault / "notes/hermes-api.md").write_text(
            "---\ntype: note\nrepo: https://github.com/acme-example/hermes-api\ndescription: Order export rewrite\n---\n\n# hermes-api\n")
        os.rename(self.vault / "notes/hermes-kickoff.md", self.vault / "notes/hermes-kick-off.md")
        failed = self.grade()
        for label in ("hermes-api: at notes/hermes/hermes-api.md", "hermes-api: type repo",
                      "hermes-api: part_of hermes", "hermes-ui: one note", "hermes-kickoff: one note",
                      "nothing copied from the tool"):
            self.assertIn(label, failed)

    def test_a_double_note_an_archived_repo_and_a_hand_move_fail(self):
        self.start("connect-repos")
        self.solve()
        self.pkm("new", "repo", "--url", "https://github.com/acme-example/apollo-legacy", "--set", "part_of=apollo")
        self.pkm("new", "repo", "--url", "https://github.com/acme-example/apollo-api", "--name", "apollo-api-2")
        (self.vault / "notes/sub").mkdir()
        os.rename(self.vault / "notes/apollo-docs.md", self.vault / "notes/sub/apollo-docs.md")
        failed = self.grade()
        for label in ("no note apollo-legacy", "one note per repository", "apollo-docs: moved with pkm",
                      "apollo-docs: at notes/apollo-docs.md"):
            self.assertIn(label, failed)

    def test_changed_owner_text_fails(self):
        self.start("connect-repos")
        self.solve()
        path = self.vault / "notes/apollo.md"
        path.write_text(path.read_text().replace("## Links\n", "## Links\n\n- Repo: [[apollo-api]]\n"))
        self.assertIn("apollo: the owner's text unchanged", self.grade())


if __name__ == "__main__":
    unittest.main()
