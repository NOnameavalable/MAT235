"""Rebuild original Week 3 diagrams and crop required source figures.

Run from any directory with Python, NumPy, Matplotlib, and PyMuPDF installed.
Source excerpts are direct crops of the local lecture and textbook PDFs;
the three other diagrams are original illustrations from formulas below.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pymupdf
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "graphs"
SLIDES = HERE.parents[1] / "Lec Note" / "Week3.pdf"
OUT.mkdir(exist_ok=True)


def linear_contours():
    x = np.linspace(-2.5, 2.5, 500)
    y = np.linspace(-5.0, 5.0, 500)
    xx, yy = np.meshgrid(x, y)
    zz = 2 + 2 * xx - yy
    fig, ax = plt.subplots(figsize=(6.0, 6.0), layout="constrained")
    levels = [0, 2, 4, 6]
    cs = ax.contour(xx, yy, zz, levels=levels, colors="#155a8a", linewidths=2)
    ax.clabel(cs, inline=True, fmt=lambda v: f"level {int(v)}", fontsize=10,
              manual=[(0.5, 3), (0.5, 1), (0.5, -1), (0.5, -3)])
    ax.axhline(0, color="#333333", linewidth=1)
    ax.axvline(0, color="#333333", linewidth=1)
    ax.set(xlim=(-2.5, 2.5), ylim=(-5, 5), xlabel="$x$", ylabel="$y$")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(alpha=0.23)
    ax.set_title("Contours of a linear function")
    fig.savefig(OUT / "pt04-linear-contours.png", dpi=190)
    plt.close(fig)


def plane_intercepts():
    fig = plt.figure(figsize=(6.8, 5.4), layout="constrained")
    ax = fig.add_subplot(111, projection="3d")
    pts = np.array([[4, 0, 0], [0, 5, 0], [0, 0, 6]])
    tri = Poly3DCollection([pts], facecolors="#77b5d8", edgecolors="#185777", alpha=0.62)
    ax.add_collection3d(tri)
    for point, label, shift in [
        (pts[0], "$x$-intercept", (0.1, 0, 0)),
        (pts[1], "$y$-intercept", (0, 0.1, 0)),
        (pts[2], "$z$-intercept", (0, 0, 0.15)),
    ]:
        ax.scatter(*point, color="#0f3954", s=25)
        ax.text(*(point + shift), label, fontsize=9)
    ax.set(xlim=(0, 5), ylim=(0, 6), zlim=(0, 7), xlabel="$x$", ylabel="$y$", zlabel="$z$")
    ax.view_init(elev=23, azim=-125)
    ax.set_box_aspect((1, 1, 1))
    ax.set_title("Plane patch in the first octant")
    fig.savefig(OUT / "pt05-plane-intercepts.png", dpi=190)
    plt.close(fig)


def level_surfaces():
    u = np.linspace(0, 2 * np.pi, 24)
    v = np.linspace(0, np.pi, 13)
    uu, vv = np.meshgrid(u, v)
    fig = plt.figure(figsize=(6.2, 5.5), layout="constrained")
    ax = fig.add_subplot(111, projection="3d")
    for radius, color, alpha in [(1.0, "#b65927", 0.85), (2.0, "#246b99", 0.5)]:
        x = radius * np.cos(uu) * np.sin(vv)
        y = radius * np.sin(uu) * np.sin(vv)
        z = radius * np.cos(vv)
        ax.plot_wireframe(x, y, z, rstride=2, cstride=2, color=color, linewidth=0.8, alpha=alpha)
    ax.set(xlim=(-2.2, 2.2), ylim=(-2.2, 2.2), zlim=(-2.2, 2.2), xlabel="$x$", ylabel="$y$", zlabel="$z$")
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=19, azim=-55)
    ax.legend(handles=[Line2D([0], [0], color="#b65927", label="inner level"),
                       Line2D([0], [0], color="#246b99", label="outer level")], loc="upper right")
    ax.set_title("Nested spherical level surfaces")
    fig.savefig(OUT / "pt06-level-surfaces.png", dpi=190)
    plt.close(fig)


def answer_plane_figures():
    cases = [
        ("week3-slide-05-plane.png", "Week 3 slide: intercept plane", [(3, 0, 0), (0, 2, 0), (0, 0, 6)],
         (0, 3.8), (0, 2.7), (0, 6.8), -125),
        ("tb-12-4-ex39-plane.png", "Textbook 12.4 #39: negative $y$ intercept",
         [(1, 0, 0), (0, -2, 0), (0, 0, 2)],
         (0, 1.4), (-2.5, 0.5), (0, 2.5), -62),
    ]
    for name, title, coords, xlim, ylim, zlim, azim in cases:
        pts = np.array(coords, dtype=float)
        fig = plt.figure(figsize=(7, 5.7), layout="constrained")
        ax = fig.add_subplot(111, projection="3d")
        ax.add_collection3d(Poly3DCollection([pts], facecolors="#83b7d7",
                                             edgecolors="#184a6b", alpha=0.67))
        for point, axis_name in zip(pts, ["x", "y", "z"]):
            ax.scatter(*point, color="#103d5a", s=28)
            ax.text(*point, f"  {axis_name}: ({point[0]:g}, {point[1]:g}, {point[2]:g})", fontsize=8)
        ax.set(xlim=xlim, ylim=ylim, zlim=zlim, xlabel="$x$", ylabel="$y$", zlabel="$z$")
        ax.view_init(elev=23, azim=azim)
        ax.set_box_aspect((1, 1, 1))
        ax.set_title(title)
        fig.savefig(OUT / name, dpi=190)
        plt.close(fig)


def source_contour_crops():
    doc = pymupdf.open(SLIDES)
    crops = [
        (3, "source-slide-04-contours.png", (0.09, 0.145, 0.39, 0.91)),
        (4, "source-slide-05-contours.png", (0.16, 0.27, 0.47, 0.53)),
    ]
    for page_index, name, (left, top, right, bottom) in crops:
        page = doc[page_index]
        r = page.rect
        clip = pymupdf.Rect(r.x0 + left * r.width, r.y0 + top * r.height,
                            r.x0 + right * r.width, r.y0 + bottom * r.height)
        page.get_pixmap(matrix=pymupdf.Matrix(3, 3), clip=clip, alpha=False).save(OUT / name)
    doc.close()


def textbook_figure_crops():
    book = HERE.parents[2] / "MAT235_textbook.pdf"
    doc = pymupdf.open(book)
    # (zero-based PDF page, output name, normalized page rectangle)
    crops = [
        (748, "source-textbook-12-4-ex13.png", (0.57, 0.17, 0.92, 0.37)),
        (748, "source-textbook-12-4-ex15.png", (0.22, 0.71, 0.48, 0.89)),
        (749, "source-textbook-12-4-ex21.png", (0.17, 0.54, 0.45, 0.725)),
        (749, "source-textbook-12-4-ex23.png", (0.50, 0.14, 0.71, 0.34)),
        (754, "source-textbook-surface-catalog.png", (0.16, 0.15, 0.85, 0.76)),
        (755, "source-textbook-12-5-ex01.png", (0.10, 0.75, 0.48, 0.92)),
    ]
    for page_index, name, (left, top, right, bottom) in crops:
        page = doc[page_index]
        r = page.rect
        clip = pymupdf.Rect(r.x0 + left * r.width, r.y0 + top * r.height,
                            r.x0 + right * r.width, r.y0 + bottom * r.height)
        page.get_pixmap(matrix=pymupdf.Matrix(3, 3), clip=clip, alpha=False).save(OUT / name)
    doc.close()


if __name__ == "__main__":
    linear_contours()
    plane_intercepts()
    level_surfaces()
    answer_plane_figures()
    source_contour_crops()
    textbook_figure_crops()
