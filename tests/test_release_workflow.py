"""Exercise the release guard and archive against real temporary Git history."""

import hashlib
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
import zipfile

import yaml


WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/release.yml"
STEPS = yaml.safe_load(WORKFLOW.read_text())["jobs"]["publish"]["steps"]
GUARD = next(step["run"] for step in STEPS if step["name"] == "Verify release tag and main history")
PACKAGE = next(step["run"] for step in STEPS if step["name"] == "Package skills and checksum")


class ReleaseWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="skills-release-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Release test")
        self.git("config", "user.email", "release-test@example.invalid")
        (self.root / "README.md").write_text("Collection\n")
        skill = self.root / "skills/example"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("An example skill\n")
        private = self.root / "scripts"
        private.mkdir()
        (private / "not-a-skill.py").write_text("# Not release content\n")
        self.git("add", ".")
        self.git("commit", "-qm", "Initial collection")
        self.git("update-ref", "refs/remotes/origin/main", "HEAD")

    def git(self, *arguments):
        return subprocess.run(
            ["git", *arguments], cwd=self.root, check=True,
            text=True, capture_output=True,
        )

    def run_step(self, script, tag):
        return subprocess.run(
            ["bash", "-euo", "pipefail", "-c", script], cwd=self.root,
            env={**os.environ, "GITHUB_REF_NAME": tag},
            text=True, capture_output=True,
        )

    def test_annotated_main_tag_packages_only_public_collection(self):
        self.git("tag", "-a", "v1.2.3", "-m", "Release")
        result = self.run_step(GUARD, "v1.2.3")
        self.assertEqual(result.returncode, 0, result.stderr)
        result = self.run_step(PACKAGE, "v1.2.3")
        self.assertEqual(result.returncode, 0, result.stderr)
        archive = self.root / "dist/skills-v1.2.3.zip"
        with zipfile.ZipFile(archive) as bundle:
            files = {name for name in bundle.namelist() if not name.endswith("/")}
            self.assertEqual(files, {"skills/README.md", "skills/skills/example/SKILL.md"})
            self.assertEqual(bundle.read("skills/README.md"), b"Collection\n")
        checksum = (self.root / "dist/SHA256SUMS").read_text().split()
        self.assertEqual(checksum, [hashlib.sha256(archive.read_bytes()).hexdigest(), archive.name])

    def test_rejects_non_semver_tag(self):
        self.git("tag", "v1.2.3-rc.1")
        result = self.run_step(GUARD, "v1.2.3-rc.1")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("vMAJOR.MINOR.PATCH", result.stderr)

    def test_rejects_tag_outside_main_history(self):
        self.git("checkout", "-qb", "unmerged")
        (self.root / "README.md").write_text("Unmerged collection\n")
        self.git("add", "README.md")
        self.git("commit", "-qm", "Unmerged change")
        self.git("tag", "v1.2.3")
        self.assertNotEqual(self.run_step(GUARD, "v1.2.3").returncode, 0)


if __name__ == "__main__":
    unittest.main()
