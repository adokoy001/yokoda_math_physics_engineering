"""Verify archived bytes and the new Markdown navigation; no research code runs."""
from pathlib import Path
import hashlib
import json
import re
import sys
from urllib.parse import unquote, urlsplit

root = Path(__file__).resolve().parents[1]
errors = []
manifest = json.loads((root / 'provenance/files.json').read_text())
expected = {item['path'] for item in manifest['files']}
for item in manifest['files']:
    path = root / item['path']
    if not path.is_file():
        errors.append('missing: ' + item['path'])
        continue
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != item['sha256']:
        errors.append('hash mismatch: ' + item['path'])

navigation = [root / 'README.md', root / 'CATALOG.md', root / 'ARCHIVE_NOTES.md']
navigation.extend(sorted((root / 'research').glob('*/README.md')))
checked_links = 0
for doc in navigation:
    for target in re.findall(r'\]\(([^)]+)\)', doc.read_text()):
        target = target.split(' "', 1)[0]
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        checked_links += 1
        path = (doc.parent / unquote(parsed.path)).resolve()
        if not path.is_relative_to(root) or not path.exists():
            errors.append(f'broken navigation: {doc.relative_to(root)} -> {target}')

for name in ['source-manifest.json', 'extraction-manifest.json']:
    data = json.loads((root / 'provenance' / name).read_text())
    for item in data['files']:
        path = root / item['path']
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
            errors.append(f'provenance mismatch: {item["path"]}')
        if 'source_path' in item:
            source = root / item['source_path']
            if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest() != item['source_sha256']:
                errors.append(f'source mismatch: {item["source_path"]}')

print(json.dumps({'files_checked': len(expected), 'navigation_links_checked': checked_links,
                  'errors': errors, 'status': 'FAIL' if errors else 'PASS'}, ensure_ascii=False, indent=2))
sys.exit(bool(errors))
