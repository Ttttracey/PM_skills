"""Check packaged sources, installer mappings and public documentation links."""
from pathlib import Path
import ast
import importlib.util
import re
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent


def main():
    errors = []
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if not re.match(r'^---\nname: pm-workflow\ndescription: "[^\n]+"\n---', text):
        errors.append("Skill metadata is invalid")
    for path in ROOT.rglob("*.py"):
        if ".git" not in path.parts:
            try:
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            except SyntaxError as error:
                errors.append(str(error))
    spec = importlib.util.spec_from_file_location("pm_install_check", ROOT / "scripts/initialize.py")
    installer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(installer)
    for source, _, _ in installer.MAPPING:
        if not (ROOT / "assets" / source).is_file():
            errors.append("Missing installer source: " + source)
    for path in [ROOT / "README.md", *ROOT.glob("docs/*.md"), *ROOT.glob("evals/*.md")]:
        source = re.sub(r'```.*?```', '', path.read_text(encoding="utf-8"), flags=re.S)
        targets = re.findall(r'\[[^\]]*\]\(([^)]+)\)', source)
        targets += re.findall(r'(?:src|href)="([^"#][^"]*)"', source)
        for target in targets:
            url = urlsplit(target)
            if url.scheme or target.startswith(("#", "//")):
                continue
            resolved = (path.parent / unquote(url.path)).resolve()
            if not resolved.is_relative_to(ROOT) or not resolved.exists():
                errors.append(f"{path.name}: invalid local link {target}")
    for path in (ROOT / "assets/readme").glob("*.svg"):
        try:
            ET.parse(path)
        except ET.ParseError as error:
            errors.append(str(error))
    if errors:
        print("\n".join(errors))
        return 1
    print("PASS: Skill metadata, Python syntax, installer assets, documentation links and SVG.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
