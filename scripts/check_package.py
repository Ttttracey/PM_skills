"""Dependency-free structural checks for this package, not a behavioral evaluation."""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.duplicates = []
        self.local_links = []
        self.remote = []
        self.lang = False
        self.viewport = False
        self.title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        element_id = attrs.get('id')
        if element_id:
            if element_id in self.ids:
                self.duplicates.append(element_id)
            self.ids.add(element_id)
        self.lang |= tag == 'html' and bool(attrs.get('lang'))
        self.viewport |= tag == 'meta' and attrs.get('name') == 'viewport'
        self.title |= tag == 'title'
        for key in ('href', 'src'):
            url = attrs.get(key, '')
            if url.startswith('#'):
                self.local_links.append(url[1:])
            elif tag in ('script', 'link', 'img', 'iframe') and url:
                if urlsplit(url).scheme or url.startswith('//'):
                    self.remote.append(url)


def main():
    failures = []
    skill = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
    match = re.match(r'^---\n(.*?)\n---\n', skill, re.S)
    if not match:
        failures.append('SKILL.md: missing frontmatter')
    else:
        # This package deliberately uses only a two-key, single-line YAML subset.
        entries = match.group(1).splitlines()
        if len(entries) != 2 or not entries[0].startswith('name: ') or not entries[1].startswith('description: '):
            failures.append('SKILL.md: expected name and description')
        else:
            name = entries[0].split(': ', 1)[1]
            description = entries[1].split(': ', 1)[1]
            if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name) > 64:
                failures.append('SKILL.md: invalid skill name')
            if not (description.startswith('"') and description.endswith('"')) or len(description) <= 2:
                failures.append('SKILL.md: empty or unquoted description')
    for path in sorted(ROOT.rglob('*.md')):
        if '.git' in path.parts:
            continue
        text = path.read_text(encoding='utf-8')
        # Ignore fenced code so example links are not mistaken for package links.
        text = re.sub(r'```.*?```', '', text, flags=re.S)
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', text):
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith(('#', '//')):
                continue
            resolved = (path.parent / unquote(parsed.path)).resolve()
            if not resolved.is_relative_to(ROOT):
                failures.append(f'{path.relative_to(ROOT)}: link escapes package: {target}')
            elif not resolved.exists():
                failures.append(f'{path.relative_to(ROOT)}: missing link: {target}')
    for path in sorted(ROOT.rglob('*.html')):
        page = Page()
        page.feed(path.read_text(encoding='utf-8'))
        prefix = str(path.relative_to(ROOT))
        if not (page.lang and page.viewport and page.title):
            failures.append(f'{prefix}: missing language, viewport or title')
        if page.duplicates:
            failures.append(f'{prefix}: duplicate IDs: {page.duplicates}')
        for anchor in page.local_links:
            if anchor and anchor not in page.ids:
                failures.append(f'{prefix}: unknown anchor #{anchor}')
        if page.remote:
            failures.append(f'{prefix}: external assets break offline default: {page.remote}')
    if failures:
        print('\n'.join(failures))
        return 1
    print('PASS: skill metadata, local Markdown links, HTML IDs/anchors and offline assets.')
    print('Behavior, generated content quality and browser interactions are not covered.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
