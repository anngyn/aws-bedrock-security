import concurrent.futures
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
BASE = 'https://static.us-east-1.prod.workshops.aws/public/c4660d38-851e-45db-9894-729d4fa65763/'

def download(path):
    target = ROOT / path.lstrip('/')
    target.parent.mkdir(parents=True, exist_ok=True)
    url = BASE + path.lstrip('/')
    with urlopen(Request(url, headers={'User-Agent': 'Workshop offline archive'}), timeout=45) as response:
        data = response.read()
    if data.lstrip().startswith(b'<Error>'):
        raise RuntimeError(f'AWS error response: {path}')
    target.write_bytes(data)
    return {'path': path, 'url': url, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

if __name__ == '__main__':
    pages = json.loads((ROOT / 'pages.json').read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(download, [page['resource'] for page in pages]))
    (ROOT / 'source-downloads.json').write_text(json.dumps(results, indent=2))
    print(f'Downloaded {len(results)} English pages, {sum(x["bytes"] for x in results)} bytes')
