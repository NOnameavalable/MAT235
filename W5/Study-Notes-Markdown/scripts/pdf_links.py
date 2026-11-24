"""Convert cross-document links to native PDF GoToR named-destination links."""
from pathlib import Path
import sys
from urllib.parse import unquote
import pymupdf

for argument in sys.argv[1:]:
    file = Path(argument)
    doc = pymupdf.open(file)
    changes = 0
    for page in doc:
        for link in page.get_links():
            target = link.get('file', link.get('uri', ''))
            if '.pdf#nameddest=' not in target:
                continue
            other, name = target.split('#nameddest=', 1)
            page.update_link({'kind': pymupdf.LINK_GOTOR, 'xref': link['xref'],
                              'from': link['from'], 'file': other, 'page': -1,
                              'to': unquote(name)})
            changes += 1
    if changes:
        doc.saveIncr()
    doc.close()
    print(f'{file.name}: updated {changes} cross-PDF destinations')
