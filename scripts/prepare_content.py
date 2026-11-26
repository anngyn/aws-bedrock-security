"""Adapt the saved AWS Markdown for Hugo without changing the original files."""
import hashlib
import json
import posixpath
import re
import shutil
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / '.hugo-content'
ORIGINAL = 'https://catalog.us-east-1.prod.workshops.aws/workshops/1ff65006-cc4a-48fd-99c9-3ef1e3d7a5ef/en-US'
SHORT_TITLES = {
    '/': 'Workshop overview',
    '/module0': '0. Environment & services',
    '/module0-5-preparation': 'Preparation & console access',
    '/module1': '1. Platform & integrations',
    '/module2': '2. WAF threat analysis',
    '/module3': '3. Just-in-time database access',
    '/module4': '4. GuardDuty response',
    '/module5': '5. Security Hub remediation',
    '/module6': '6. AppSec & Inspector',
    '/summary': 'Summary & cleanup',
}


def verify_sources():
    for filename, key in [('source-downloads.json', 'path'), ('asset-downloads.json', 'relative')]:
        for item in json.loads((ROOT / filename).read_text()):
            path = ROOT / item[key].lstrip('/')
            if hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
                raise ValueError(f'Saved source integrity mismatch: {path}')


def write_evidence():
    catalog = json.loads((ROOT / 'evidence-catalog.json').read_text())
    base = OUTPUT / 'evidence'
    base.mkdir()
    index = ('---\ntitle: "Workshop evidence gallery"\nlinkTitle: "Evidence gallery"\nweight: 30\n---\n\n'
             'Visual checkpoints for the workshop: integrations, analysis, approvals, '
             'remediation, and code findings. These reference screens show example '
             'results to compare with your own lab.\n\n')
    for group in catalog['groups']:
        route = '/evidence/' + group['id']
        index += '- [' + group['title'] + ']({{% relref "' + route + '" %}}) — ' + str(len(group['images'])) + ' images\n'
        content = ('---\ntitle: ' + json.dumps(group['title']) + '\nweight: ' + str(group['weight'])
                   + '\n---\n\nReference screenshots of example configurations and results.\n\n'
                   + group['intro'] + '\n\n')
        content += '[Open the related workshop module]({{% relref "' + group['module'] + '" %}})\n\n'
        for number, item in enumerate(group['images'], 1):
            path = ROOT / 'static' / item['asset']
            if hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
                raise ValueError(f'Evidence integrity mismatch: {path}')
            content += '## ' + str(number) + '. ' + item['title'] + '\n\n'
            content += item['caption'] + '\n\n'
            content += '![' + item['title'] + ']({{% asset ' + json.dumps('static/' + item['asset']) + ' %}})\n\n'
        folder = base / group['id']
        folder.mkdir()
        (folder / '_index.md').write_text(content)
        module = OUTPUT / group['module'].lstrip('/') / '_index.md'
        with module.open('a') as file:
            file.write('\n\n## Visual checkpoints\n\n[View example screens for this module]({{% relref "' + route + '" %}}).\n')
    (base / '_index.md').write_text(index)
    print(f'Added {sum(len(group["images"]) for group in catalog["groups"])} reference images across {len(catalog["groups"])} evidence galleries.')


def main():
    verify_sources()
    pages = json.loads((ROOT / 'pages.json').read_text())
    aliases = {}
    for page in pages:
        source_path = posixpath.dirname(page['resource']).removeprefix('/content') or '/'
        for alias in (page['path'], source_path):
            aliases[alias.rstrip('/') or '/'] = page['path']

    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir()

    for order, page in enumerate(pages):
        raw = (ROOT / page['resource'].lstrip('/')).read_text()
        match = re.fullmatch(r'---\s*\n(.*?)\n---\s*\n(.*)', raw, re.S)
        if not match:
            raise ValueError(f'Missing front matter: {page["resource"]}')
        front, body = match.groups()
        front = re.sub(r'^weight:.*$', f'weight: {order}', front, flags=re.M)
        front += '\nlinkTitle: ' + json.dumps(SHORT_TITLES.get(page['path'], page['title']))
        if page['path'] == '/':
            front += '\ndescription: "Hands-on AWS security automation with Amazon Bedrock, GuardDuty, Security Hub, Inspector, and autobotAI."'

        def target(original):
            parts = urlsplit(original)
            if 'static/' in parts.path and (not parts.netloc or parts.netloc == 'static.us-east-1.prod.workshops.aws'):
                asset = 'static/' + unquote(parts.path.split('static/', 1)[1])
                if not (ROOT / asset).is_file():
                    raise ValueError(f'Missing asset: {asset}')
                return '{{< asset ' + json.dumps(asset) + ' >}}'
            if parts.scheme or parts.netloc or original.startswith('#'):
                return original
            path = posixpath.normpath(posixpath.join(page['path'].rstrip('/') + '/', parts.path))
            dest = aliases.get(path.rstrip('/') or '/')
            if dest is None:
                raise ValueError(f'Unmapped local link in {page["path"]}: {original}')
            suffix = ('#' + parts.fragment) if parts.fragment else ''
            return '{{% relref ' + json.dumps(dest + suffix) + ' %}}'

        # Only transform prose. Preserve every fenced command, JSON and diagram.
        result = []
        fence = None
        for line in body.splitlines(keepends=True):
            marker = re.match(r'^\s*(`{3,}|~{3,})', line)
            if marker:
                token = marker.group(1)
                if fence is None:
                    fence = token
                elif token[0] == fence[0] and len(token) >= len(fence):
                    fence = None
                result.append(line)
                continue
            if fence is None:
                line = re.sub(r':button\[([^\]]+)\]\{href="([^"]+)"[^}]*\}',
                              lambda m: '[' + m[1] + '](' + m[2] + ')', line)
                line = re.sub(r'\]\(([^\s)]+)',
                              lambda m: '](' + target(m[1]).replace('{{< asset ', '{{% asset ').replace(' >}}', ' %}}'), line)
                line = re.sub(r'\b(src|href)="([^"]+)"',
                              lambda m: m[1] + "='" + target(m[2]) + "'", line)
            result.append(line)

        body = ''.join(result)
        if page['path'] == '/':
            body = ('> **Community mirror of the AWS workshop.** Original English content, '
                    'screenshots, and lab resources are preserved from public build '
                    '`c4660d38-851e-45db-9894-729d4fa65763`.\n\n' + body)
        body += f'\n\n---\n\n[View this page in the original AWS workshop]({ORIGINAL}{page["path"] if page["path"] != "/" else ""})\n'
        # Branch bundles keep all nested lessons visible in Hugo's menu.
        path = OUTPUT / page['path'].lstrip('/') / '_index.md'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('---\n' + front + '\n---\n\n' + body)
    write_evidence()
    print(f'Prepared {len(pages)} Hugo pages; original Markdown and asset hashes verified.')


if __name__ == '__main__':
    main()
