# Week 1 - Functions of Two Variables

Study materials for MAT235, based on the W1 lecture materials and textbook Section 12.1 (8th edition, printed pages 694-701).

1. Read [Study Notes](./Study-Notes.md) for complete concepts, explicit teaching questions, worked examples, common mistakes, and actual tables and graphs.
2. Complete [Practice and Self-Test](./Practice-and-Self-Test.md), then check the explained answers at the end.
3. Use the [Coverage Audit](./Coverage-Audit.md) to trace every source page and assigned exercise to the notes.
4. Use Section 12 of the notes for the complete assigned textbook questions, necessary work, and concise answers. Each exercise links to its detailed knowledge explanation.

The graph folder contains 22 generated mathematical illustrations and three source excerpts: the textbook weather map, textbook coordinate axes, and an uncalibrated handwritten sketch. To rebuild the generated figures with Python, NumPy, and Matplotlib, run `python3 W1/graphs/generate_graphs.py` from the MAT235 folder. To rebuild the coordinate and handwritten excerpts using Poppler and Pillow, run `python3 W1/graphs/extract_coordinate_figure.py`.

The notes use portable Markdown with code-formatted and Unicode mathematics, so formulas do not require a LaTeX renderer. Original instructional questions are labelled **Teaching example**; textbook, lecture, and worksheet questions carry source labels.

Run `python3 W1/validate_study_materials.py` to check links, images, table structure, and required question/work/answer sections. The [Coverage Audit](./Coverage-Audit.md) records the separate visual and source-content checks.

## Sources and scope

- [W1 lecture slides](./Lec%20Notes/Week1-with-answers.pdf)
- [September 10 notes](./Lec%20Notes/MAT235H-5201_Sept%2010.pdf)
- [Textbook](../MAT235_textbook.pdf): Section 12.1 only; printed pages 694-701 correspond to PDF pages 714-721.

The core is function notation and representations, reading tables, fixing one input, three-dimensional coordinates, planes, distance, and spheres. Every supplementary or preview item that appears in the Week 1 files is also included: contour-map estimation, qualitative temperature sections, the plane `z=1+x-y`, the cylinder `x²+y²=1`, and all six requested sections of `z=y³+xy`.
