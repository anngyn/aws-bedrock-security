"""Build an offline HTML archive from the public AWS workshop source."""
import base64
import concurrent.futures
import datetime
import hashlib
import html
import json
import mimetypes
import posixpath
import re
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import unquote, urljoin, urlsplit
from urllib.request import Request, urlopen

from markdown_it import MarkdownIt
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
BUILD = 'c4660d38-851e-45db-9894-729d4fa65763'
BASE = f'https://static.us-east-1.prod.workshops.aws/public/{BUILD}/'
PUBLIC = 'https://catalog.us-east-1.prod.workshops.aws/workshops/1ff65006-cc4a-48fd-99c9-3ef1e3d7a5ef/en-US'
PAGES = json.loads((ROOT / 'pages.json').read_text())
RECORDS = []
ASSETS = {}
ALIASES = {}

for index, page in enumerate(PAGES):
    page['section_id'] = f'chapter-{index:02}'
    for path in [page['path'], page['path'].replace('-', '.'), page['resource'].removesuffix('index.en.md').removesuffix('/').removeprefix('/content')]:
        ALIASES[path.rstrip('/') or '/'] = page['section_id']

def render(page):
    source = (ROOT / page['resource'].lstrip('/')).read_text()
    source = re.sub(r'^---\s*\n.*?\n---\s*\n', '', source, count=1, flags=re.S)
    source = re.sub(r':button\[([^\]]+)\]\{href="([^"]+)"[^}]*\}', r'<p><a class="download" href="\2" download>\1</a></p>', source)
    rendered = MarkdownIt('commonmark', {'html': True}).enable(['table', 'strikethrough']).render(source)
    soup = BeautifulSoup(rendered, 'html.parser')
    local_ids = {}
    heading_counts = {}
    for heading in soup.find_all(re.compile(r'^h[1-6]$')):
        title = heading.get_text(' ', strip=True).lower()
        slug = re.sub(r'[^\w\- ]', '', title).strip().replace(' ', '-')
        heading_counts[slug] = heading_counts.get(slug, 0) + 1
        if heading_counts[slug] > 1:
            slug += '-' + str(heading_counts[slug])
        heading['id'] = slug
    for node in soup.select('[id]'):
        old = node['id']
        node['id'] = page['section_id'] + '--' + old
        local_ids[old] = node['id']
    for node in soup.find_all(['img', 'a', 'video', 'source']):
        attr = 'href' if node.name == 'a' else 'src'
        if not node.get(attr):
            continue
        original = html.unescape(node[attr])
        parts = urlsplit(original)
        record = {'page': page['title'], 'page_path': page['path'], 'kind': node.name, 'label': node.get('alt') or node.get_text(' ', strip=True), 'original': original}
        if original.startswith('#'):
            node[attr] = '#' + local_ids.get(original[1:], page['section_id'])
            record['resolved'] = PUBLIC + page['path'] + original
        elif 'static/' in parts.path and (not parts.netloc or parts.netloc == 'static.us-east-1.prod.workshops.aws'):
            relative = 'static/' + unquote(parts.path.split('static/', 1)[1])
            canonical = BASE + relative
            original_url = original if parts.scheme else canonical
            ASSETS.setdefault(relative, {'relative': relative, 'url': original_url, 'fallback': canonical})
            node[attr] = relative
            node['data-original-url'] = original_url
            record.update(resolved=original_url, local=relative)
        elif parts.scheme in ['http', 'https', 'mailto'] or original.startswith('//'):
            record['resolved'] = original
            if node.name == 'a':
                node['rel'] = 'noopener noreferrer'
        elif not parts.scheme:
            normalized = posixpath.normpath(posixpath.join(page['path'].rstrip('/') + '/', parts.path)).rstrip('/') or '/'
            section = ALIASES.get(normalized)
            if section:
                node[attr] = '#' + section
                record['resolved'] = PUBLIC + normalized
                record['local'] = '#' + section
            else:
                node[attr] = urljoin(PUBLIC + page['path'].rstrip('/') + '/', original)
                record['resolved'] = node[attr]
                record['unmapped_internal'] = True
        else:
            record['resolved'] = original
        RECORDS.append(record)
    # Bare URLs remain in the source and are also included in the resource index.
    for match in re.finditer(r'https?://[^\s<>"`]+', source):
        url = match.group(0).rstrip('.,;)')
        if not any(x['page_path'] == page['path'] and x['original'] == url for x in RECORDS):
            RECORDS.append({'page': page['title'], 'page_path': page['path'], 'kind': 'text-url', 'label': url, 'original': url, 'resolved': url})
    return soup

def fetch_asset(asset):
    dest = ROOT / asset['relative']
    dest.parent.mkdir(parents=True, exist_ok=True)
    receipt = dict(asset)
    errors = []
    if dest.is_file():
        data = dest.read_bytes()
        receipt['downloaded_url'] = asset['fallback']
    else:
        for url in dict.fromkeys([asset['url'], asset['fallback']]):
            try:
                with urlopen(Request(url, headers={'User-Agent': 'Workshop offline archive'}), timeout=45) as response:
                    data = response.read()
                    receipt['content_type'] = response.headers.get('Content-Type', '')
                if data.lstrip().startswith((b'<Error>', b'<?xml')):
                    raise ValueError('XML error response')
                dest.write_bytes(data)
                receipt['downloaded_url'] = url
                break
            except Exception as error:
                errors.append(f'{url}: {error}')
        else:
            receipt.update(status='failed', errors=errors)
            return receipt
    receipt.update(status='ok', bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    if errors:
        receipt['prior_errors'] = errors
    return receipt

CSS = '''
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f4f6f8;color:#182330;font:16px/1.65 system-ui,-apple-system,sans-serif}a{color:#0066ad;overflow-wrap:anywhere}nav{position:fixed;inset:0 auto 0 0;width:300px;overflow:auto;background:#142334;color:#fff;padding:24px 20px}nav h2{font-size:19px;line-height:1.3}nav a{display:block;color:#dbe9f5;font-size:13px;text-decoration:none;padding:7px 0;border-bottom:1px solid #304052}nav a.sub{padding-left:14px}main{margin-left:300px;max-width:1300px;padding:32px 48px}header,article,.resource-index{background:#fff;border:1px solid #d8e0e7;border-radius:10px;padding:28px 34px;margin-bottom:24px}h1{font-size:30px;line-height:1.25}h2{font-size:25px;line-height:1.35;margin-top:36px}h3{line-height:1.4}article{scroll-margin-top:20px}article>h1{border-bottom:3px solid #e99b32;padding-bottom:16px}img{max-width:100%;height:auto;object-fit:contain}table{border-collapse:collapse;width:100%;display:block;overflow:auto;margin:22px 0}td,th{border:1px solid #d9e0e6;padding:10px 12px;text-align:left}th{background:#eaf0f5}pre{background:#142334;color:#edf5fc;padding:20px;overflow:auto;border-radius:7px;line-height:1.5;white-space:pre}code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.88em}p code,li code,td code{background:#e9eef3;padding:2px 4px;border-radius:3px}blockquote{margin:20px 0;padding:10px 20px;background:#edf5fc;border-left:4px solid #3685bb}details{margin:16px 0}.meta{font-size:13px;color:#596b7a}.resource-index td{font-size:13px}input{padding:10px;width:100%;border:1px solid #c4d0dc;border-radius:5px}.download{display:inline-block;padding:8px 14px;background:#e9f3fb;border:1px solid #3281b7;border-radius:6px}.failure{color:#a22}.back-top{font-size:13px}.source-raw{max-height:500px}.no-results{display:none}@media(max-width:1000px){nav{position:static;width:auto;max-height:300px}main{margin:0;padding:16px}header,article,.resource-index{padding:20px}}@media print{nav,.search-panel,.back-top{display:none}main{margin:0;max-width:none;padding:0}article,header,.resource-index{border:0;padding:0;break-before:page}pre{white-space:pre-wrap}a{color:inherit}}
'''

def main():
    soups = [render(page) for page in PAGES]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        receipts = list(pool.map(fetch_asset, ASSETS.values()))
    (ROOT / 'asset-downloads.json').write_text(json.dumps(receipts, indent=2))
    failed = [x for x in receipts if x['status'] != 'ok']
    success = {x['relative']: x for x in receipts if x['status'] == 'ok'}
    nav = ''.join(f'<a class="{"sub" if p["path"].count("/") > 1 else ""}" href="#{p["section_id"]}">{html.escape(p["title"])}</a>' for p in PAGES)
    sections = []
    asset_anchors = {}
    for page, soup in zip(PAGES, soups):
        for image in soup.find_all('img'):
            relative = image.get('src', '')
            if relative in success:
                if relative not in asset_anchors:
                    image['id'] = 'asset-' + hashlib.sha256(relative.encode()).hexdigest()[:16]
                    asset_anchors[relative] = image['id']
                data = (ROOT / relative).read_bytes()
                mime = mimetypes.guess_type(relative)[0] or 'application/octet-stream'
                image['src'] = 'data:' + mime + ';base64,' + base64.b64encode(data).decode()
                image['loading'] = 'lazy'
            elif relative in ASSETS:
                image['src'] = ASSETS[relative]['fallback']
        for link in soup.find_all('a'):
            relative = link.get('href', '')
            if relative in success:
                data = (ROOT / relative).read_bytes()
                link['href'] = 'data:application/octet-stream;base64,' + base64.b64encode(data).decode()
                link['download'] = Path(relative).name
        raw = (ROOT / page['resource'].lstrip('/')).read_text()
        sections.append(f'<article id="{page["section_id"]}"><p class="meta">{html.escape(page["path"])} · <a href="{html.escape(PUBLIC + (page["path"] if page["path"] != "/" else ""))}">Original workshop page</a></p><h1>{html.escape(page["title"])}</h1>{soup}<details><summary>Exact original Markdown source</summary><pre class="source-raw">{html.escape(raw)}</pre></details><a class="back-top" href="#top">Back to top</a></article>')
    rows = []
    unique = set()
    for record in RECORDS:
        key = (record['page_path'], record['original'])
        if key in unique:
            continue
        unique.add(key)
        url = record['resolved']
        local = record.get('local', '')
        local_target = '#' + asset_anchors[local] if local in asset_anchors else local
        download_attr = ''
        if local in success and local not in asset_anchors:
            local_target = 'data:application/octet-stream;base64,' + base64.b64encode((ROOT / local).read_bytes()).decode()
            download_attr = f' download="{html.escape(Path(local).name)}"'
        local_link = f'<a href="{html.escape(local_target)}"{download_attr}>Local copy</a>' if local else ''
        rows.append(f'<tr><td>{html.escape(record["page"])}</td><td>{html.escape(record["kind"])}</td><td><code>{html.escape(record["original"])}</code><br><a href="{html.escape(url)}">{html.escape(url)}</a> {local_link}</td></tr>')
    resources = '<section id="resources" class="resource-index"><h1>All resource links</h1><p>Original destinations are retained here. AWS-hosted images and workshop attachments are also saved locally. External sites remain online links.</p><input id="resource-search" type="search" placeholder="Filter resource links"><table><thead><tr><th>Source page</th><th>Type</th><th>Original and resolved destination</th></tr></thead><tbody id="resource-rows">' + ''.join(rows) + '</tbody></table></section>'
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    note = f'26 English pages · {len(success)} local assets · public build {BUILD} · retrieved {now}'
    warning = '<p class="failure">Some original AWS assets could not be downloaded; see verification.json.</p>' if failed else ''
    document = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Amazon Bedrock security — complete English workshop</title><style>{CSS}</style></head><body><nav><h2>Amazon Bedrock security</h2><a href="#top">Archive information</a>{nav}<a href="#resources">All resource links</a></nav><main><header id="top"><h1>Agentic SecOps with Cybersecurity Agent Factory and Amazon Bedrock</h1><p>Offline archive of the official public AWS workshop. Original English text, code, tables and resource destinations are preserved; presentation has been rebuilt for offline reading.</p><p class="meta">{note}</p><p><a href="{PUBLIC}">Official public workshop</a> · <a href="#resources">Resource index</a></p><p class="meta">The public workshop structure and overview match the joined event. Event-only account details and credentials are not included. The event build identifier was not exposed in the captured interface, so exact build equivalence cannot be independently confirmed.</p>{warning}<div class="search-panel"><label for="search">Find a chapter by text</label><input id="search" type="search" placeholder="Search the workshop"></div></header>{"".join(sections)}{resources}</main><script>document.getElementById("search").addEventListener("input",function(){{const q=this.value.toLowerCase();document.querySelectorAll("article").forEach(a=>a.hidden=!a.textContent.toLowerCase().includes(q))}});document.getElementById("resource-search").addEventListener("input",function(){{const q=this.value.toLowerCase();document.querySelectorAll("#resource-rows tr").forEach(r=>r.hidden=!r.textContent.toLowerCase().includes(q))}});</script></body></html>'
    (ROOT / 'workshop.html').write_text(document)
    (ROOT / 'resources.json').write_text(json.dumps(RECORDS, ensure_ascii=False, indent=2))
    verification = {'source': PUBLIC, 'build_id': BUILD, 'retrieved_at': now, 'pages_expected': len(PAGES), 'pages_downloaded': len(json.loads((ROOT / 'source-downloads.json').read_text())), 'images_and_attachments_expected': len(ASSETS), 'assets_downloaded': len(success), 'asset_failures': failed, 'unmapped_internal_links': [x for x in RECORDS if x.get('unmapped_internal')], 'resource_entries': len(rows), 'html_bytes': len(document.encode()), 'event_build_match': 'Public overview and module structure match observed event; event build ID unverified.'}
    (ROOT / 'verification.json').write_text(json.dumps(verification, ensure_ascii=False, indent=2))
    print(json.dumps(verification, indent=2))

if __name__ == '__main__':
    main()
