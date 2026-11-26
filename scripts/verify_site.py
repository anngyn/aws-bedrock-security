"""Check the built project-site URLs, images, downloads and lesson coverage."""
import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = set()
        self.links = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        for key in ('src', 'href', 'poster'):
            if attrs.get(key):
                self.links.append(attrs[key])


def fences(text):
    return re.findall(r'^\s*```[^\n]*\n(.*?)^\s*```', text, re.M | re.S)


def main():
    public = ROOT / 'public'
    default_base = re.search(r"^baseURL\s*=\s*['\"]([^'\"]+)", (ROOT / 'hugo.toml').read_text(), re.M)[1]
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-url', default=default_base)
    base = parser.parse_args().base_url
    prefix = urlsplit(base).path
    pages = json.loads((ROOT / 'pages.json').read_text())
    documents = {p: Page(p.read_text()) for p in public.rglob('*.html')}
    errors = []
    for page in pages:
        route = page['path'].lstrip('/')
        built = public / route / 'index.html'
        if built not in documents:
            errors.append(f'Missing lesson: {route}')
        original = (ROOT / page['resource'].lstrip('/')).read_text()
        generated = (ROOT / '.hugo-content' / route / '_index.md').read_text()
        if fences(original) != fences(generated):
            errors.append(f'Changed fenced code: {route}')

    catalog = json.loads((ROOT / 'evidence-catalog.json').read_text())
    evidence_images = 0
    for group in catalog['groups']:
        output = public / 'evidence' / group['id'] / 'index.html'
        if output not in documents:
            errors.append(f'Missing evidence gallery: {group["id"]}')
            continue
        for item in group['images']:
            expected = prefix + 'static/' + item['asset']
            if expected not in documents[output].links:
                errors.append(f'Missing gallery image: {expected}')
            evidence_images += 1

    references = 0
    for path, doc in documents.items():
        relative = str(path.relative_to(public))
        page_url = urljoin(base, relative.removesuffix('index.html'))
        for link in doc.links:
            if link.startswith(('data:', 'mailto:', 'javascript:', 'tel:')):
                continue
            url = urlsplit(urljoin(page_url, link))
            if url.netloc != urlsplit(base).netloc:
                continue
            if not unquote(url.path).startswith(prefix):
                errors.append(f'{relative}: URL escapes project base path: {link}')
                continue
            target = public / unquote(url.path).removeprefix(prefix)
            if target.is_dir():
                target /= 'index.html'
            if not target.is_file():
                errors.append(f'{relative}: missing local resource: {link}')
            elif url.fragment and target in documents and unquote(url.fragment) not in documents[target].ids:
                errors.append(f'{relative}: missing anchor: {link}')
            references += 1
    if errors:
        raise SystemExit('\n'.join(sorted(set(errors))))
    print(f'PASS: {len(pages)} lessons, {evidence_images} evidence images, {len(documents)} HTML pages, {references} local references; fenced code unchanged.')


if __name__ == '__main__':
    main()
