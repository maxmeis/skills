import tempfile
import unittest
from pathlib import Path

from scripts.validate_skills import validate


class ValidateSkillsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skill = self.root / "skills" / "example-skill"
        self.skill.mkdir(parents=True)
        (self.skill / "SKILL.md").write_text(
            "---\nname: example-skill\ndescription: A useful example.\n---\n\n"
            "Read [details](references/details.md).\n",
            encoding="utf-8",
        )
        (self.skill / "references").mkdir()
        (self.skill / "references" / "details.md").write_text("Details.\n", encoding="utf-8")
        (self.root / "README.md").write_text(
            "See [the skill](skills/example-skill/SKILL.md).\n", encoding="utf-8"
        )

    def test_valid_repository(self):
        self.assertEqual(validate(self.root), [])

    def test_missing_required_metadata(self):
        (self.skill / "SKILL.md").write_text("---\nname: example-skill\n---\nBody.\n", encoding="utf-8")
        self.assertTrue(any("description must be" in error for error in validate(self.root)))

    def test_bad_yaml(self):
        (self.skill / "SKILL.md").write_text("---\nname: [oops\n---\nBody.\n", encoding="utf-8")
        self.assertTrue(any("invalid frontmatter YAML" in error for error in validate(self.root)))

    def test_missing_local_reference(self):
        (self.skill / "references" / "details.md").unlink()
        self.assertTrue(any("missing local link target" in error for error in validate(self.root)))

    def test_skill_reference_cannot_depend_on_repo_readme(self):
        (self.skill / "references" / "details.md").write_text(
            "Read [the repository README](../../../README.md).\n", encoding="utf-8"
        )
        self.assertTrue(any("local link escapes" in error for error in validate(self.root)))

    def test_empty_optional_openai_yaml(self):
        agents = self.skill / "agents"
        agents.mkdir()
        (agents / "openai.yaml").write_text("", encoding="utf-8")
        self.assertTrue(any("agents/openai.yaml must be a YAML mapping" in error for error in validate(self.root)))

    def test_absent_skill(self):
        (self.skill / "SKILL.md").unlink()
        self.assertTrue(any("missing SKILL.md" in error for error in validate(self.root)))

    def test_unsafe_symlink(self):
        outside = self.root.parent / f"{self.root.name}-outside.md"
        outside.write_text("Outside.\n", encoding="utf-8")
        self.addCleanup(outside.unlink)
        (self.skill / "references" / "outside.md").symlink_to(outside)
        self.assertTrue(any("symlink escapes repository" in error for error in validate(self.root)))


if __name__ == "__main__":
    unittest.main()
