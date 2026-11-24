#!/usr/bin/env python3
"""
Generate schematic and reconstructed figures for MAT235 Week 4 Study Notes
(Sections 12.6, 13.1, 13.2: Limits and Continuity, Displacement Vectors, Vectors in General).
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, Rectangle
from mpl_toolkits.mplot3d import proj3d

plt.rcParams.update({
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "figure.dpi": 160,
})

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")
os.makedirs(OUT_DIR, exist_ok=True)


class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def do_3d_projection(self, renderer=None):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        return np.min(zs)


def make_fig01_limit_representations():
    """
    Fig 01: Continuous vs. Discontinuous limit behavior at (0,0) (Reconstructed / Schematic)
    Compares f(x,y) = x^2 y / (x^2 + y^2) (limit 0) and g(x,y) = x^2 / (x^2 + y^2) (DNE).
    """
    fig = plt.figure(figsize=(12, 9.2))
    gs = fig.add_gridspec(2, 2, hspace=0.34, wspace=0.28)

    # Grid avoiding exact (0,0)
    lin = np.linspace(-1.0, 1.0, 150)
    X, Y = np.meshgrid(lin, lin)
    R2 = X**2 + Y**2 + 1e-12
    F = (X**2 * Y) / R2
    G = (X**2) / R2

    # (a) 3D surface of f(x,y) = x^2 y / (x^2 + y^2)
    ax1 = fig.add_subplot(gs[0, 0], projection="3d")
    surf1 = ax1.plot_surface(X, Y, F, cmap="coolwarm", edgecolor="none", alpha=0.88)
    ax1.scatter([0], [0], [0], color="black", s=45, zorder=10, label="f(0,0) = 0 (continuous)")
    ax1.set_title(r"(a) Surface $z = \frac{x^2 y}{x^2+y^2}$ (Limit $= 0$ at $(0,0)$)")
    ax1.set_xlabel("$x$")
    ax1.set_ylabel("$y$")
    ax1.set_zlabel("$z$")
    ax1.set_zlim(-0.6, 0.6)
    ax1.view_init(elev=24, azim=-48)
    ax1.legend(loc="upper left", fontsize=8)

    # (b) Contour diagram of f(x,y) = x^2 y / (x^2 + y^2)
    ax2 = fig.add_subplot(gs[0, 1])
    levels_f = [-0.45, -0.35, -0.25, -0.15, -0.05, 0.05, 0.15, 0.25, 0.35, 0.45]
    cs2 = ax2.contour(X, Y, F, levels=levels_f, cmap="coolwarm", linewidths=1.4)
    ax2.clabel(cs2, inline=True, fontsize=8, fmt="%.2f")
    ax2.axhline(0, color="gray", lw=1.0, ls="--", label="$y = 0$ ($z = 0$)")
    ax2.axvline(0, color="gray", lw=1.0, ls=":")
    ax2.plot(0, 0, "ko", ms=6)
    ax2.annotate("Values near (0,0)\nall approach 0", xy=(0, 0), xytext=(0.22, -0.82),
                 arrowprops=dict(arrowstyle="->", lw=1.1, color="black"),
                 bbox=dict(boxstyle="round,pad=0.3", fc="#f8f9fa", ec="gray"))
    ax2.set_title(r"(b) Contours of $f(x,y) = \frac{x^2 y}{x^2+y^2}$ (Limit $0$; Continuous if $f(0,0)=0$)")
    ax2.set_xlabel("$x$")
    ax2.set_ylabel("$y$")
    ax2.set_aspect("equal")
    ax2.grid(True, alpha=0.25)

    # (c) 3D surface of g(x,y) = x^2 / (x^2 + y^2)
    ax3 = fig.add_subplot(gs[1, 0], projection="3d")
    # Polar grid for cleaner ridge rendering
    r_p = np.linspace(0.03, 1.0, 60)
    th_p = np.linspace(0, 2 * np.pi, 160)
    R_p, TH_p = np.meshgrid(r_p, th_p)
    Xp = R_p * np.cos(TH_p)
    Yp = R_p * np.sin(TH_p)
    Gp = np.cos(TH_p)**2
    ax3.plot_surface(Xp, Yp, Gp, cmap="viridis", edgecolor="none", alpha=0.88)
    ax3.plot([-1, 1], [0, 0], [1, 1], color="#d62728", lw=2.5, label="$x$-axis ($y=0, x\\neq 0$): $z=1$")
    ax3.plot([0, 0], [-1, 1], [0, 0], color="#1f77b4", lw=2.5, label="$y$-axis ($x=0, y\\neq 0$): $z=0$")
    ax3.set_title(r"(c) Surface $z = \frac{x^2}{x^2+y^2}$ (Pinched Ridge at $(0,0)$)")
    ax3.set_xlabel("$x$")
    ax3.set_ylabel("$y$")
    ax3.set_zlabel("$z$")
    ax3.set_zlim(0, 1.05)
    ax3.view_init(elev=26, azim=-52)
    ax3.legend(loc="upper left", fontsize=8)

    # (d) Radial contours of g(x,y) = x^2 / (x^2 + y^2) approaching punctured origin
    ax4 = fig.add_subplot(gs[1, 1])
    c_vals = [0.05, 0.25, 0.50, 0.75, 0.95]
    colors = plt.cm.viridis(np.linspace(0.1, 0.92, len(c_vals)))
    x_line = np.linspace(-1.0, 1.0, 200)
    for c, col in zip(c_vals, colors):
        # x^2 / (x^2 + y^2) = c => y = +/- sqrt((1-c)/c) x (for x != 0)
        m = np.sqrt((1.0 - c) / c)
        ax4.plot(x_line, m * x_line, color=col, lw=1.5, label=f"$g = {c:.2f}$")
        ax4.plot(x_line, -m * x_line, color=col, lw=1.5)
    ax4.axhline(0, color="#d62728", lw=2.2, label="$x$-axis ($g = 1, x\\neq 0$)")
    ax4.axvline(0, color="#1f77b4", lw=2.2, label="$y$-axis ($g = 0$)")
    ax4.plot(0, 0, "ko", ms=8, mfc="white", mew=2.2, zorder=10, label="Punctured limit point $(0,0)$")
    ax4.set_xlim(-1, 1)
    ax4.set_ylim(-1, 1)
    ax4.set_aspect("equal")
    ax4.set_title(r"(d) Contours of $g(x,y) = \frac{x^2}{x^2+y^2}$ (Distinct Levels Approach $(0,0) \Rightarrow$ DNE)")
    ax4.set_xlabel("$x$")
    ax4.set_ylabel("$y$")
    ax4.legend(loc="upper right", fontsize=7.2, framealpha=0.92)
    ax4.grid(True, alpha=0.25)

    fig.suptitle("Reconstructed / Schematic Comparison: Multivariable Limit Existence vs. Nonexistence at (0, 0)",
                 fontsize=12.5, fontweight="bold", y=0.98)
    fig.savefig(os.path.join(OUT_DIR, "fig01_limit_representations.png"), bbox_inches="tight")
    plt.close(fig)


def make_fig02_path_analysis_terrible_example():
    """
    Fig 02: Path Analysis and the 'Terrible Example' f(x,y) = x^2 y / (x^4 + y^2)
    Shows why all straight lines y = mx give limit 0, while parabola y = x^2 gives limit 1/2.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.2))
    fig.subplots_adjust(wspace=0.28)

    x = np.linspace(-1.0, 1.0, 400)
    # Left panel: Paths in the xy-plane
    for m, ls in [(-1.0, "--"), (-0.4, ":"), (0.0, "-"), (0.4, ":"), (1.0, "--")]:
        lbl = f"Line $y = {m:g}x$ ($\\lim = 0$)" if m in (-1.0, 0.0, 1.0) else None
        ax1.plot(x, m * x, color="#1f77b4", ls=ls, lw=1.4, alpha=0.85, label=lbl)
    ax1.axvline(0, color="#1f77b4", lw=1.4, alpha=0.85, label="$y$-axis $x = 0$ ($\\lim = 0$)")
    ax1.plot(x, x**2, color="#d62728", lw=2.6, label="Parabola $y = x^2$ ($f(x,x^2) = 1/2$)")
    ax1.plot(x, -x**2, color="#ff7f0e", lw=2.2, ls="-.", label="Parabola $y = -x^2$ ($f(x,-x^2) = -1/2$)")
    ax1.plot(0, 0, "ko", ms=7, mfc="white", mew=2, zorder=10)
    ax1.set_xlim(-1.0, 1.0)
    ax1.set_ylim(-1.0, 1.0)
    ax1.set_aspect("equal")
    ax1.set_title("(a) Approach Paths in the $xy$-Plane Near $(0,0)$")
    ax1.set_xlabel("$x$")
    ax1.set_ylabel("$y$")
    ax1.legend(loc="lower right", fontsize=8, framealpha=0.92)
    ax1.grid(True, alpha=0.3)

    # Right panel: Heatmap & contours of f(x,y) = x^2 y / (x^4 + y^2)
    xg = np.linspace(-0.8, 0.8, 300)
    yg = np.linspace(-0.6, 0.6, 300)
    X, Y = np.meshgrid(xg, yg)
    Z = (X**2 * Y) / (X**4 + Y**2 + 1e-12)

    im = ax2.pcolormesh(X, Y, Z, cmap="RdBu_r", vmin=-0.5, vmax=0.5, shading="auto")
    cbar = fig.colorbar(im, ax=ax2, fraction=0.046, pad=0.04)
    cbar.set_label(r"$f(x,y) = \frac{x^2 y}{x^4 + y^2}$")

    xp = np.linspace(-0.77, 0.77, 200)
    ax2.plot(xp, xp**2, color="black", lw=2.2, label="Ridge $y = x^2$ ($f = +1/2$)")
    ax2.plot(xp, -xp**2, color="black", lw=2.0, ls="--", label="Trough $y = -x^2$ ($f = -1/2$)")
    ax2.plot(xp, 0.5 * xp, color="#2ca02c", lw=1.8, label="Line $y = 0.5x$ (leaves ridge as $x\\to 0$)")
    ax2.plot(0, 0, "wo", ms=7, mec="black", mew=2, zorder=10)
    ax2.set_xlim(-0.8, 0.8)
    ax2.set_ylim(-0.6, 0.6)
    ax2.set_title(r"(b) Parabolic Ridge of $f(x,y) = \frac{x^2 y}{x^4 + y^2}$ Near $(0,0)$")
    ax2.set_xlabel("$x$")
    ax2.set_ylabel("$y$")
    ax2.legend(loc="lower right", fontsize=8, framealpha=0.92)

    fig.suptitle("Schematic Diagram: Why Equal Limits Along All Lines $y = mx$ Do Not Prove Limit Existence",
                 fontsize=12, fontweight="bold", y=1.01)
    fig.savefig(os.path.join(OUT_DIR, "fig02_path_analysis_terrible_example.png"), bbox_inches="tight")
    plt.close(fig)


def make_fig03_squeeze_and_continuity_domains():
    """
    Fig 03: Squeeze Theorem radial cross-section & Continuity Regions (Reconstructed / Schematic)
    Left: Squeeze Theorem bound |sin(x)(x^2+y^2)| <= x^2+y^2 (and x^4 sin(1/(x^2+|y|))).
    Right: Continuity vs. Discontinuity sets in R^2 (Textbook 12.6 #1, #5 and sep 28.pdf p. 4).
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.0))
    fig.subplots_adjust(wspace=0.28)

    # Left: Squeeze theorem slice along y = 0 for f(x,0) = x^2 sin(1/x) / sin(x)*x^2
    x = np.linspace(-0.8, 0.8, 1200)
    x_nz = np.where(np.abs(x) < 1e-4, 1e-4, x)
    upper = x**2
    lower = -x**2
    osc = (x**2) * np.sin(1.0 / x_nz)
    smooth_sq = np.sin(x) * (x**2)

    ax1.fill_between(x, lower, upper, color="#cce5ff", alpha=0.55, label=r"Envelope $-g(x,y) \leq f(x,y) \leq g(x,y)$")
    ax1.plot(x, upper, color="#004085", lw=2.0, ls="--", label="Upper bound $+g(x,0) = +x^2 \\to 0$")
    ax1.plot(x, lower, color="#004085", lw=2.0, ls=":", label="Lower bound $-g(x,0) = -x^2 \\to 0$")
    ax1.plot(x, osc, color="#d62728", lw=1.3, alpha=0.9, label=r"Oscillating slice $x^2 \sin(1/x)$")
    ax1.plot(x, smooth_sq, color="#2ca02c", lw=2.0, label=r"Lecture slice $\sin(x)\cdot x^2$ (sep 28 p. 4)")
    ax1.plot(0, 0, "ko", ms=6, zorder=10)
    ax1.set_xlim(-0.8, 0.8)
    ax1.set_ylim(-0.68, 0.68)
    ax1.set_title("(a) Squeeze Theorem Slice ($y = 0$): Trapping $f(x,y)$ at $(0,0)$")
    ax1.set_xlabel("$x$ (along $y = 0$)")
    ax1.set_ylabel("Function value")
    ax1.legend(loc="upper center", fontsize=8, framealpha=0.92)
    ax1.grid(True, alpha=0.3)

    # Right: Continuity regions & singular curves (Textbook 12.6 #5: tan(xy) on [-2,2]^2)
    rect = Rectangle((-2, -2), 4, 4, facecolor="#e8f5e9", edgecolor="#2e7d32", lw=2.0,
                     label="Square $R = [-2,2] \\times [-2,2]$ (Ex. 12.6 #5)")
    ax2.add_patch(rect)

    # Curves xy = +/- pi/2 and xy = +/- 3pi/2 inside [-2,2]^2
    xh1 = np.linspace(np.pi / 4, 2.0, 200)
    ax2.plot(xh1, (np.pi / 2) / xh1, color="#d62728", lw=2.2, label=r"Singular curves $xy = \pm \frac{\pi}{2} \approx \pm 1.57$")
    ax2.plot(-xh1, -(np.pi / 2) / xh1, color="#d62728", lw=2.2)
    ax2.plot(xh1, -(np.pi / 2) / xh1, color="#d62728", lw=2.2)
    ax2.plot(-xh1, (np.pi / 2) / xh1, color="#d62728", lw=2.2)

    # Curves xy = +/- 3pi/2 ( since 3pi/2 ~ 4.71 > 4, show just outside to illustrate why only k=0,-1 enter )
    xh2 = np.linspace(1.9, 2.5, 100)
    ax2.plot(xh2, (3 * np.pi / 2) / xh2, color="#ff7f0e", lw=1.6, ls="--",
             label=r"Next branch $xy = \pm \frac{3\pi}{2} \approx \pm 4.71$ (outside $R$)")
    ax2.plot(-xh2, -(3 * np.pi / 2) / xh2, color="#ff7f0e", lw=1.6, ls="--")

    ax2.plot(0, 0, "ko", ms=6, mfc="white", mew=2, label="Singular point $(0,0)$ for $1/(x^2+y^2)$ (Ex. 12.6 #1)")
    ax2.set_xlim(-2.6, 2.6)
    ax2.set_ylim(-2.6, 2.6)
    ax2.set_aspect("equal")
    ax2.set_title(r"(b) Discontinuity Curves of $\tan(xy)$ Inside $[-2,2]^2$ (Ex. 12.6 #5)")
    ax2.set_xlabel("$x$")
    ax2.set_ylabel("$y$")
    ax2.legend(loc="lower left", fontsize=7.5, framealpha=0.94)
    ax2.grid(True, alpha=0.3)

    fig.suptitle("Schematic Visual Guide: Squeeze Theorem Bounds and Region Continuity Checks",
                 fontsize=12, fontweight="bold", y=1.01)
    fig.savefig(os.path.join(OUT_DIR, "fig03_squeeze_and_continuity_domains.png"), bbox_inches="tight")
    plt.close(fig)


def make_fig04_textbook_12_6_contours():
    """
    Fig 04: Reconstructed Figure 12.101 from Textbook Section 12.6 (Exercises #12-15)
    In Figure 12.101, f(x,y) = 10 x^2 / (x^2 + y^2) has radial contours:
    - level 0 along y-axis (x = 0)
    - level 2 along y = +/- 2x (passes through (-1,2), (1,2), (-1,-2), (1,-2))
    - level 4 along y = +/- sqrt(1.5)x
    - level 6 along y = +/- sqrt(2/3)x
    - level 8 along y = +/- 0.5x (passes through (2,1), (-2,1), (2,-1), (-2,-1))
    - level 10 along x-axis (y = 0)
    """
    fig, ax = plt.subplots(figsize=(6.8, 6.4))

    ax.set_xlim(-3.2, 3.2)
    ax.set_ylim(-3.2, 3.2)
    ax.set_aspect("equal")

    # Outer box [-3, 3] x [-3, 3]
    box = Rectangle((-3, -3), 6, 6, fill=False, edgecolor="black", lw=1.4)
    ax.add_patch(box)

    # Coordinate axes
    ax.axhline(0, color="#1f77b4", lw=2.2)
    ax.axvline(0, color="#1f77b4", lw=2.2)

    # Radial contour lines: c in {2, 4, 6, 8}
    # Formula matching textbook Fig 12.101: f(x,y) = 10 x^2 / (x^2 + y^2)
    # Check: at (-1,2), 10(1)/(1+4) = 2; at (2,1), 10(4)/(4+1) = 8; at (-2,0), 10; at (0,y), 0!
    c_levels = [2, 4, 6, 8]
    for c in c_levels:
        m = np.sqrt((10.0 - c) / c)  # slope |y/x|
        # Intersect with box [-3, 3]^2
        if 3.0 * m <= 3.0:
            x_end = 3.0
            y_end = 3.0 * m
        else:
            y_end = 3.0
            x_end = 3.0 / m
        ax.plot([-x_end, x_end], [-y_end, y_end], color="#1f77b4", lw=1.5)
        ax.plot([-x_end, x_end], [y_end, -y_end], color="#1f77b4", lw=1.5)

        # Place contour labels near the border as in Figure 12.101
        r_lbl = 0.88
        for sx in (-1, 1):
            for sy in (-1, 1):
                ax.text(sx * x_end * r_lbl, sy * y_end * r_lbl, f"{c}",
                        fontsize=9, fontweight="bold", color="#0b3d91",
                        ha="center", va="center",
                        bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85))

    # Labels for 0 (on y-axis) and 10 (on x-axis)
    for sy in (-2.4, 2.4):
        ax.text(0.18, sy, "0", fontsize=9.5, fontweight="bold", color="#0b3d91",
                bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.85))
    for sx in (-2.4, 2.4):
        ax.text(sx, 0.18, "10", fontsize=9.5, fontweight="bold", color="#0b3d91",
                bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.85))

    # Highlight requested exercise points: #13 (-1, 2) and #15 (0, 0)
    ax.plot(-1, 2, "ro", ms=8, zorder=10, label="Ex. 12.6 #13: $(-1, 2)$ lies on contour $f = 2$")
    ax.annotate("$(-1, 2)$\n(Ex. #13: limit $\\approx 2$)", xy=(-1, 2), xytext=(-2.88, 1.05),
                arrowprops=dict(arrowstyle="->", color="#d62728", lw=1.4),
                fontsize=9, fontweight="bold", color="#b71c1c",
                bbox=dict(boxstyle="round,pad=0.25", fc="#ffebee", ec="#d62728"))

    ax.plot(0, 0, "ko", ms=8, mfc="white", mew=2.2, zorder=12,
            label="Ex. 12.6 #15: punctured origin $(0, 0)$ approached by levels $0,2,4,6,8,10$")
    ax.annotate("Punctured $(0, 0)$\n(Ex. #15: distinct levels\napproach $(0,0) \\Rightarrow$ DNE)",
                xy=(0, 0), xytext=(0.18, -1.85),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.4),
                fontsize=8.5, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.25", fc="#fff9c4", ec="black"))

    ax.set_xticks([-3, -2, -1, 0, 1, 2, 3])
    ax.set_yticks([-3, -2, -1, 0, 1, 2, 3])
    ax.grid(True, linestyle=":", alpha=0.45)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title("Reconstructed Figure 12.101 (Textbook Section 12.6, Exercises #12–15)\n"
                 r"Radial Contour Map of $f(x,y)$ on $[-3,3] \times [-3,3]$", fontweight="bold")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.11), fontsize=8.5, framealpha=0.95)

    fig.savefig(os.path.join(OUT_DIR, "fig04_textbook_12_6_contours.png"), bbox_inches="tight")
    plt.close(fig)


def make_fig05_vector_geometry_and_3d_box():
    """
    Fig 05: Vector Geometry, 3D Box Sums (Week4-sol.pdf p. 9 / SQ-12), and 2D Grid (Textbook 13.1 #1)
    """
    fig = plt.figure(figsize=(14.4, 4.9))
    gs = fig.add_gridspec(1, 3, wspace=0.28)

    # Panel A: Tip-to-tail sum v + w and difference w - v
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_xlim(-0.5, 5.2)
    ax1.set_ylim(-0.5, 4.2)
    ax1.set_aspect("equal")
    v = np.array([3.0, 1.0])
    w = np.array([1.2, 2.8])
    vw = v + w

    def draw_vec2d(ax, start, end, color, label, text_pos, lw=2.2, ls="-"):
        arr = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=15,
                              color=color, lw=lw, linestyle=ls)
        ax.add_patch(arr)
        ax.text(text_pos[0], text_pos[1], label, color=color, fontweight="bold", fontsize=9.2,
                bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.75))

    draw_vec2d(ax1, (0, 0), v, "#1f77b4", r"$\vec{v}$", (1.45, 0.15))
    draw_vec2d(ax1, (0, 0), w, "#2ca02c", r"$\vec{w}$", (0.12, 1.55))
    draw_vec2d(ax1, v, vw, "#2ca02c", r"$\vec{w}$ (shifted)", (3.55, 1.95), lw=1.6, ls="--")
    draw_vec2d(ax1, (0, 0), vw, "#9467bd", r"$\vec{v} + \vec{w}$", (1.75, 2.55), lw=2.4)
    draw_vec2d(ax1, v, w, "#d62728", r"$\vec{w} - \vec{v}$", (1.45, 1.55), lw=2.2)

    ax1.plot(0, 0, "ko", ms=5)
    ax1.text(-0.38, -0.32, "Start", fontsize=8.5)
    ax1.set_title(r"(a) Tip-to-Tail Sum $\vec{v}+\vec{w}$ & Difference $\vec{w}-\vec{v}$")
    ax1.set_xlabel("$x$")
    ax1.set_ylabel("$y$")
    ax1.grid(True, alpha=0.3)

    # Panel B: 3D Box vector sums (matching Week4-sol.pdf p. 9: u=+x, v=+y, w=+z)
    ax2 = fig.add_subplot(gs[0, 1], projection="3d")
    for x0 in [0, 1]:
        for y0 in [0, 1]:
            ax2.plot([x0, x0], [y0, y0], [0, 1], color="gray", lw=0.85, alpha=0.5)
    for x0 in [0, 1]:
        for z0 in [0, 1]:
            ax2.plot([x0, x0], [0, 1], [z0, z0], color="gray", lw=0.85, alpha=0.5)
    for y0 in [0, 1]:
        for z0 in [0, 1]:
            ax2.plot([0, 1], [y0, y0], [z0, z0], color="gray", lw=0.85, alpha=0.5)

    def add_arr3d(ax, p1, p2, col, lw=2.2, ls="-"):
        a = Arrow3D([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]],
                    mutation_scale=13, lw=lw, arrowstyle="-|>", color=col, linestyle=ls)
        ax.add_artist(a)

    # Origin O(0,0,0) at back-bottom corner
    ax2.plot([0], [0], [0], "ko", ms=4.5)
    ax2.text(-0.14, 0.04, 0.06, "$O$", fontsize=8.5, fontweight="bold")

    # Given box edge vectors from Week4-sol.pdf p. 9:
    # u along +x edge (0,0,0)->(1,0,0)
    add_arr3d(ax2, (0, 0, 0), (1, 0, 0), "black", lw=2.2)
    ax2.text(0.55, -0.18, -0.05, r"$\vec{u}$", color="black", fontweight="bold")

    # v printed on top-right +y edge (0,0,1)->(0,1,1) and shifted to bottom +y edge (1,0,0)->(1,1,0)
    add_arr3d(ax2, (0, 0, 1), (0, 1, 1), "black", lw=1.8)
    ax2.text(-0.08, 0.48, 1.06, r"$\vec{v}$", color="black", fontweight="bold")
    add_arr3d(ax2, (1, 0, 0), (1, 1, 0), "#1f77b4", lw=2.0, ls="--")
    ax2.text(1.08, 0.42, -0.10, r"$\vec{v}$ (shifted)", color="#1f77b4", fontsize=8.0, fontweight="bold")

    # w along front-most vertical +z edge (1,1,0)->(1,1,1)
    add_arr3d(ax2, (1, 1, 0), (1, 1, 1), "#ff7f0e", lw=2.2)
    ax2.text(1.05, 1.08, 0.48, r"$\vec{w}$", color="#ff7f0e", fontweight="bold")

    # Resulting sums from origin O(0,0,0):
    # u + v: bottom-face diagonal (0,0,0)->(1,1,0) in z=0 plane
    add_arr3d(ax2, (0, 0, 0), (1, 1, 0), "#9467bd", lw=2.4)
    ax2.text(0.35, 0.65, -0.08, r"$\vec{u}+\vec{v}$", color="#9467bd", fontweight="bold")

    # u + v + w: main space diagonal (0,0,0)->(1,1,1)
    add_arr3d(ax2, (0, 0, 0), (1, 1, 1), "#d62728", lw=2.5)
    ax2.text(0.28, 0.36, 0.64, r"$\vec{u}+\vec{v}+\vec{w}$", color="#d62728", fontweight="bold")

    # -v: exact length 1 along -y in z=0 plane from (1,0,0) to (1,-1,0)
    add_arr3d(ax2, (1, 0, 0), (1, -1, 0), "#1f77b4", lw=1.7, ls="--")
    ax2.text(1.08, -0.58, -0.06, r"$-\vec{v}$", color="#1f77b4", fontweight="bold")

    # u - v = u + (-v): in z=0 plane from (0,0,0) to (1,-1,0)
    add_arr3d(ax2, (0, 0, 0), (1, -1, 0), "#2ca02c", lw=2.3)
    ax2.text(0.35, -0.68, 0.05, r"$\vec{u}-\vec{v}$", color="#2ca02c", fontweight="bold")

    ax2.set_xlim(-0.15, 1.25)
    ax2.set_ylim(-1.15, 1.20)
    ax2.set_zlim(-0.15, 1.18)
    ax2.set_xlabel("$x$")
    ax2.set_ylabel("$y$")
    ax2.set_zlabel("$z$")
    ax2.view_init(elev=24, azim=20)
    ax2.set_title("(b) 3D Box Vector Sums (Week 4 Worksheet p. 9)")

    # Panel C: Reconstructed 2D grid for Textbook Section 13.1 Exercise #1
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.set_xlim(-2.6, 3.6)
    ax3.set_ylim(-2.6, 3.6)
    ax3.set_aspect("equal")
    ax3.axhline(0, color="black", lw=1.2)
    ax3.axvline(0, color="black", lw=1.2)
    ax3.set_xticks([-2, -1, 0, 1, 2, 3])
    ax3.set_yticks([-2, -1, 0, 1, 2, 3])
    ax3.grid(True, linestyle="--", alpha=0.5)

    draw_vec2d(ax3, (0, 0), (1, 3), "#1f77b4", r"$\vec{a} = \vec{i}+3\vec{j}$", (0.55, 3.12))
    draw_vec2d(ax3, (0, 0), (3, 2), "#2ca02c", r"$\vec{b} = 3\vec{i}+2\vec{j}$", (1.55, 0.78))
    draw_vec2d(ax3, (0, 0), (-2, -2), "#d62728", r"$\vec{v} = -2\vec{i}-2\vec{j}$", (-2.42, -2.42))
    draw_vec2d(ax3, (0, 0), (-1, 2), "#9467bd", r"$\vec{w} = -\vec{i}+2\vec{j}$", (-2.42, 2.15))

    ax3.set_title("(c) Reconstructed Grid: Textbook Ex. 13.1 #1")
    ax3.set_xlabel("$x$")
    ax3.set_ylabel("$y$")

    fig.suptitle("Reconstructed / Schematic Diagrams: Geometric Vector Operations and Component Resolution",
                 fontsize=12, fontweight="bold", y=1.02)
    fig.savefig(os.path.join(OUT_DIR, "fig05_vector_geometry_and_3d_box.png"), bbox_inches="tight")
    plt.close(fig)


def make_fig06_physics_vectors_force_velocity():
    """
    Fig 06: Physical Vector Applications (Section 13.2)
    (a) Static Force Equilibrium (Week4-sol.pdf p. 12: F1 = 300 east, F2 = 400 SE, F3 = -(F1+F2))
    (b) Relative Velocity Addition (Boat in river current / Plane in wind, oct 2.pdf & Ex. 13.2 #11)
    (c) Uniform Circular Motion (oct 2.pdf p. 4: tangent velocity v perpendicular to inward force F)
    """
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14.4, 4.6))
    fig.subplots_adjust(wspace=0.30)

    def draw_vec(ax, start, end, color, label, text_pos, lw=2.3, ls="-"):
        arr = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=15,
                              color=color, lw=lw, linestyle=ls)
        ax.add_patch(arr)
        if label:
            ax.text(text_pos[0], text_pos[1], label, color=color, fontweight="bold", fontsize=8.8,
                    bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.82))

    # Panel A: Force Equilibrium (Week4-sol.pdf p. 12)
    ax1.axhline(0, color="gray", lw=1.0)
    ax1.axvline(0, color="gray", lw=1.0)
    F1 = np.array([300.0, 0.0])
    F2 = np.array([400.0 / np.sqrt(2), -400.0 / np.sqrt(2)])  # (282.8, -282.8)
    F3 = -(F1 + F2)  # (-582.8, +282.8)
    draw_vec(ax1, (0, 0), F1, "#1f77b4", r"$\vec{F}_1 = 300\vec{i}$", (85, 45))
    draw_vec(ax1, (0, 0), F2, "#ff7f0e", r"$\vec{F}_2$ ($400$ lb SE, $-45^\circ$)", (-260, -335))
    draw_vec(ax1, (0, 0), F1 + F2, "gray", r"$\vec{F}_1+\vec{F}_2$", (330, -135), lw=1.5, ls="--")
    draw_vec(ax1, (0, 0), F3, "#d62728", r"$\vec{F}_3 = -(\vec{F}_1+\vec{F}_2)$", (-610, 315))
    ax1.plot(0, 0, "ko", ms=6)
    ax1.set_xlim(-660, 660)
    ax1.set_ylim(-410, 420)
    ax1.set_aspect("equal")
    ax1.set_title(r"(a) Force Equilibrium $\vec{F}_1+\vec{F}_2+\vec{F}_3=\vec{0}$" + "\n(Worksheet p. 12)")
    ax1.set_xlabel("East ($+x$, lb)")
    ax1.set_ylabel("North ($+y$, lb)")
    ax1.grid(True, alpha=0.3)

    # Panel B: Relative Velocity (Boat in River: oct 2.pdf p. 1, v_boat = 4j, v_curr = 3i, v_ground = 3i + 4j)
    ax2.axhline(0, color="gray", lw=1.0)
    ax2.axvline(0, color="gray", lw=1.0)
    draw_vec(ax2, (0, 0), (3, 0), "#1f77b4", r"$\vec{v}_{\mathrm{curr}} = (3,0)$ m/s", (0.55, -0.58))
    draw_vec(ax2, (0, 0), (0, 4), "#2ca02c", r"$\vec{v}_{\mathrm{boat/water}} = (0,4)$", (-2.05, 2.05))
    draw_vec(ax2, (3, 0), (3, 4), "#2ca02c", "", (3.1, 2.0), lw=1.5, ls="--")
    draw_vec(ax2, (0, 0), (3, 4), "#d62728", r"$\vec{v}_{\mathrm{ground}} = (3,4)$" + "\n(speed $= 5$ m/s)", (0.85, 1.35))
    ax2.set_xlim(-2.3, 4.5)
    ax2.set_ylim(-1.0, 4.7)
    ax2.set_aspect("equal")
    ax2.set_title("(b) Relative Velocity Addition\n(Oct 2 Lecture Notes p. 1)")
    ax2.set_xlabel("East ($+x$, m/s)")
    ax2.set_ylabel("North ($+y$, m/s)")
    ax2.grid(True, alpha=0.3)

    # Panel C: Uniform Circular Motion (oct 2.pdf p. 4 & Ex. 13.2 #27)
    circle = Circle((0, 0), 1.0, fill=False, edgecolor="black", lw=1.6, ls="--")
    ax3.add_patch(circle)
    ax3.plot(0, 0, "ko", ms=6)
    ax3.text(0.06, -0.16, "Center", fontsize=8.5)

    ax3.plot(0, 1, "bo", ms=7)
    draw_vec(ax3, (0, 1), (-0.85, 1.0), "#1f77b4", r"$\vec{v}(t_1)$ (tangent)", (-1.32, 1.15))
    draw_vec(ax3, (0, 1), (0.0, 0.25), "#d62728", r"$\vec{F} = m\vec{a}$ (inward)", (0.08, 0.55))

    ax3.plot(-1, 0, "bo", ms=7)
    draw_vec(ax3, (-1, 0), (-1.0, -0.85), "#1f77b4", r"$\vec{v}(t_2)$", (-1.45, -0.52))
    draw_vec(ax3, (-1, 0), (-0.25, 0.0), "#d62728", r"$\vec{F} = m\vec{a}$", (-0.82, 0.14))

    ax3.set_xlim(-1.6, 1.4)
    ax3.set_ylim(-1.4, 1.5)
    ax3.set_aspect("equal")
    ax3.set_title(r"(c) Uniform Circular Motion ($\vec{v} \perp \vec{a}$)" + "\nConstant Speed, Changing Velocity")
    ax3.set_xlabel("$x$")
    ax3.set_ylabel("$y$")
    ax3.grid(True, alpha=0.3)

    fig.suptitle("Schematic Diagrams: Physics Applications of Vectors (Force, Relative Velocity, Circular Motion)",
                 fontsize=12, fontweight="bold", y=1.02)
    fig.savefig(os.path.join(OUT_DIR, "fig06_physics_vectors_force_velocity.png"), bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    make_fig01_limit_representations()
    make_fig02_path_analysis_terrible_example()
    make_fig03_squeeze_and_continuity_domains()
    make_fig04_textbook_12_6_contours()
    make_fig05_vector_geometry_and_3d_box()
    make_fig06_physics_vectors_force_velocity()
    print("All 6 figures generated successfully in:", OUT_DIR)
