from pathlib import Path
import importlib.util
import re
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


installer = load("pm_installer_tests", "scripts/initialize.py")
validator = load("pm_validator_tests", "assets/scripts/validate_prd.py")


class InstallationTests(unittest.TestCase):
    def test_complete_install_is_repeatable_and_repairs_missing_runtime(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            installer.install(project, quiet=True, with_launcher=False)
            for _, destination, _ in installer.MAPPING:
                self.assertTrue((project / destination).is_file(), destination)
            template = project / "scripts/prd-content.html"
            first = template.read_bytes()
            installer.install(project, quiet=True, with_launcher=False)
            self.assertEqual(first, template.read_bytes())
            helper = project / "scripts/validate_prd.py"
            helper.unlink()
            installer.install(project, quiet=True, with_launcher=False)
            self.assertEqual(helper.read_bytes(), (ROOT / "assets/scripts/validate_prd.py").read_bytes())

    def test_edited_workflow_and_template_are_preserved_with_update_proposals(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            installer.install(project, quiet=True, with_launcher=False)
            paths = [".agents/workflows/edu-pm-prd.md", "scripts/prd-content.html"]
            expected = {}
            for relative in paths:
                path = project / relative
                expected[relative] = path.read_bytes() + b"\n<!-- user customization -->\n"
                path.write_bytes(expected[relative])
            installer.install(project, quiet=True, with_launcher=False)
            for relative in paths:
                self.assertEqual((project / relative).read_bytes(), expected[relative])
                self.assertTrue((project / ".pm-workflow/updates" / relative).is_file())


class PrdValidationTests(unittest.TestCase):
    def setUp(self):
        body = (ROOT / "assets/templates/prd-content.html").read_text(encoding="utf-8")
        self.document = '<main id="prdContent"><style>body{color:#222}</style>' + body + '</main>'

    def rejects(self, document, message):
        with self.assertRaisesRegex(ValueError, message):
            validator.validate_prd(document)

    def test_full_skeleton_in_document_shell_passes(self):
        self.assertTrue(validator.validate_prd(self.document))

    def test_committed_example_passes(self):
        example = ROOT / "examples/favorites/收藏功能/需求文档/收藏功能-PRD.html"
        self.assertTrue(validator.validate_prd(example.read_text(encoding="utf-8")))

    def test_merged_module_rows_are_supported(self):
        match = re.search(r'<tr data-preview=.*?</tr>', self.document, re.S)
        row = match.group(0)
        first = row.replace('rowspan="1"', 'rowspan="2"', 1)
        second = re.sub(r'<td class="mod".*?</td>', '', row, count=1, flags=re.S)
        self.assertTrue(validator.validate_prd(self.document.replace(row, first + second, 1)))

    def test_missing_version_cell_is_rejected(self):
        self.rejects(self.document.replace('<td>[日期]</td>', '', 1), 'version-table 每行')

    def test_missing_goal_table_is_rejected(self):
        changed = re.sub(r'<table class="goal-table">.*?</table>', '', self.document, count=1, flags=re.S)
        self.rejects(changed, '缺少规范表格：goal-table')

    def test_empty_preview_id_is_rejected(self):
        self.rejects(self.document.replace('data-preview="[page-id]"', 'data-preview=""'), '非空 data-preview')

    def test_empty_tracking_cell_is_rejected(self):
        self.rejects(self.document.replace('<td>button_click</td>', '<td></td>'), '六列均不可为空')

    def test_missing_colgroup_is_rejected(self):
        self.rejects(re.sub(r'<colgroup>.*?</colgroup>', '', self.document, count=1, flags=re.S), '缺少 colgroup')

    def test_boundary_must_stay_with_owning_feature(self):
        self.rejects(self.document + '<h2>异常与边界</h2>', '不设独立的异常/边界章节')


if __name__ == "__main__":
    unittest.main()
