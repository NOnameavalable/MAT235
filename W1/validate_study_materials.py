"""Validate the portable Markdown study artifacts and their local assets."""
from pathlib import Path
import re
from urllib.parse import unquote
from PIL import Image

ROOT = Path(__file__).resolve().parent
errors = []

def anchors(text):
    result = set()
    counts = {}
    for title in re.findall(r'^#{1,6} (.+)$', text, re.M):
        slug = re.sub(r'[^\w\- ]', '', title.lower()).replace(' ', '-')
        n = counts.get(slug, 0)
        counts[slug] = n + 1
        result.add(slug if n == 0 else f'{slug}-{n}')
    return result

linked_images = set()
link_count = 0
for path in ROOT.glob('*.md'):
    text = path.read_text()
    if re.search(r'<\/?(?:a|div|span)\b', text):
        errors.append(f'{path.name}: raw HTML')
    # Currency occurs inside code spans; outside code, no dollar delimiters.
    plain = re.sub(r'```.*?```', '', text, flags=re.S)
    plain = re.sub(r'`[^`]*`', '', plain)
    if '$' in plain or re.search(r'\\(?:frac|sqrt|begin|\(|\[)', plain):
        errors.append(f'{path.name}: unsupported mathematics markup')
    for image, label, target in re.findall(r'(!?)\[([^\]]*)\]\(([^)]+)\)', text):
        if target.startswith(('https://', 'http://')):
            continue
        file, _, anchor = unquote(target).partition('#')
        dest = (path.parent / file).resolve() if file else path
        link_count += 1
        if not dest.exists():
            errors.append(f'{path.name}: missing {target}')
            continue
        if anchor and dest.suffix == '.md' and anchor not in anchors(dest.read_text()):
            errors.append(f'{path.name}: missing anchor {target}')
        if image:
            if not label.strip():
                errors.append(f'{path.name}: image lacks alt text')
            linked_images.add(dest)
    previous = None
    for n, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith('|'):
            cols = len(line.strip().split('|')) - 2
            if previous is not None and cols != previous:
                errors.append(f'{path.name}:{n}: inconsistent table columns')
            previous = cols
        else:
            previous = None

notes = (ROOT / 'Study-Notes.md').read_text()
types = re.findall(r'^### Problem type: ([^\n]+)\n(.*?)(?=^#{1,3} |\Z)', notes, re.M | re.S)
for name, body in types:
    positions = [body.find(label) for label in ['**Question:**', '**Worked solution:**', '**Answer:**']]
    if -1 in positions or positions != sorted(positions):
        errors.append(f'Problem type {name}: question/work/answer missing or out of order')
    if '**Teaching example**' not in body and '**Actual ' not in body:
        errors.append(f'Problem type {name}: source label missing')
    if '**Common mistakes:**' not in body:
        errors.append(f'Problem type {name}: knowledge-level common mistakes missing')

assigned = notes.split('## 12. Complete Assigned Textbook Exercises', 1)[1].split('## 13.', 1)[0]
exercises = re.findall(r'^### Exercise (\d+)\n(.*?)(?=^### Exercise |\Z)', assigned, re.M | re.S)
expected = {1,3,5,9,11,13,15,17,19,23,25,29,31,37}
if {int(n) for n,b in exercises} != expected:
    errors.append('Assigned exercise set differs from request')
for n, body in exercises:
    for label in ['**Question:**', 'Necessary work', 'Answer:', '**Knowledge:**']:
        if label not in body:
            errors.append(f'Exercise {n}: missing {label}')
    if any(label in body for label in ['**Recognize it:**', '**Method:**', '**Common mistakes:**', '**Complete final answer:**']):
        errors.append(f'Exercise {n}: repeated detailed guide')

for path in linked_images:
    with Image.open(path) as image:
        image.verify()
top_level_graphs = {p.resolve() for p in (ROOT / 'graphs').glob('*.png')}
if top_level_graphs != linked_images:
    errors.append(f'Unlinked top-level graphs: {top_level_graphs - linked_images}')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(types)} problem types; {len(exercises)} assigned exercises; '
      f'{len(linked_images)} verified image files; {link_count} working local links.')
