"""Extract textbook Figure 12.2 from Section 12.1; no other section is read."""
from pathlib import Path
import subprocess
import tempfile
from PIL import Image
from PIL import ImageDraw

folder = Path(__file__).resolve().parent
textbook = folder.parents[1] / 'MAT235_textbook.pdf'
with tempfile.TemporaryDirectory(prefix='w1-coordinate-') as scratch:
    prefix = Path(scratch) / 'page'
    subprocess.run(['pdftoppm', '-f', '716', '-l', '716', '-scale-to', '2400',
                    '-png', str(textbook), str(prefix)], check=True)
    im = Image.open(next(Path(scratch).glob('page-*.png')))
    # Relative bounds verified against printed page 696 (Figure and caption).
    w,h = im.size
    im.crop((int(.19*w), int(.556*h), int(.37*w), int(.70*h))).save(
        folder / '17-textbook-coordinate-axes.png')

with tempfile.TemporaryDirectory(prefix='w1-handwritten-') as scratch:
    prefix = Path(scratch) / 'page'
    subprocess.run(['pdftoppm', '-f', '2', '-l', '2', '-scale-to', '1800',
                    '-png', str(folder.parent / 'MAT235H-5201_Sept 10.pdf'), str(prefix)], check=True)
    im = Image.open(next(Path(scratch).glob('page-*.png')))
    w,h=im.size
    im=im.crop((int(.02*w),int(.43*h),int(.73*w),int(.74*h)))
    # Preserve the uncalibrated source sketch; do not invent a formula or ticks.
    ImageDraw.Draw(im).text((15,12),'Original qualitative sketch; no scale or formula supplied',fill='black')
    im.save(folder / '24-handwritten-qualitative-graph.png')
