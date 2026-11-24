"""Generate reconstructed diagrams and extract original textbook exercise figures for MAT235 Week 9."""
import os
import subprocess
import tempfile
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR = os.path.join(BASE_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "mathtext.fontset": "cm",
})


def setup_plane(ax, lim=2.4):
    ax.axhline(0, color="#555555", lw=0.9, zorder=1)
    ax.axvline(0, color="#555555", lw=0.9, zorder=1)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(lim - 0.15, -0.25, r"$x$", fontsize=11, ha="right", color="#333333")
    ax.text(0.15, lim - 0.18, r"$y$", fontsize=11, va="top", color="#333333")
    for spine in ax.spines.values():
        spine.set_color("#cccccc")


def make_fig01_divergence():
    fig, axes = plt.subplots(1, 4, figsize=(14.5, 3.8), dpi=180)
    g = np.linspace(-2, 2, 9)
    X, Y = np.meshgrid(g, g)

    # (a) Source: F = xi + yj
    ax = axes[0]
    setup_plane(ax)
    ax.quiver(X, Y, X, Y, color="#1f6feb", scale=22, width=0.009, zorder=2)
    box = patches.Rectangle((-0.65, -0.65), 1.3, 1.3, lw=2.0, ec="#d97706", fc="#fef3c7", alpha=0.45, zorder=3)
    ax.add_patch(box)
    ax.plot(0, 0, "o", color="#b91c1c", ms=5, zorder=4)
    ax.set_title(r"(a) Source: $\vec{F}=x\vec{i}+y\vec{j}$" + "\n" + r"$\mathrm{div}\,\vec{F}=2>0$ (net outflow)", fontsize=9.8)

    # (b) Sink: F = -xi - yj
    ax = axes[1]
    setup_plane(ax)
    ax.quiver(X, Y, -X, -Y, color="#1f6feb", scale=22, width=0.009, zorder=2)
    box = patches.Rectangle((-0.65, -0.65), 1.3, 1.3, lw=2.0, ec="#d97706", fc="#fef3c7", alpha=0.45, zorder=3)
    ax.add_patch(box)
    ax.plot(0, 0, "o", color="#b91c1c", ms=5, zorder=4)
    ax.set_title(r"(b) Sink: $\vec{F}=-x\vec{i}-y\vec{j}$" + "\n" + r"$\mathrm{div}\,\vec{F}=-2<0$ (net inflow)", fontsize=9.8)

    # (c) Shear: F = y i
    ax = axes[2]
    setup_plane(ax)
    ax.quiver(X, Y, Y, np.zeros_like(Y), color="#1f6feb", scale=18, width=0.009, zorder=2)
    box = patches.Rectangle((-0.6, 0.4), 1.2, 1.2, lw=2.0, ec="#059669", fc="#d1fae5", alpha=0.45, zorder=3)
    ax.add_patch(box)
    ax.plot(0, 1.0, "o", color="#b91c1c", ms=5, zorder=4)
    ax.set_title(r"(c) Shear: $\vec{F}=y\vec{i}$" + "\n" + r"$\mathrm{div}\,\vec{F}=0$ (inflow = outflow)", fontsize=9.8)

    # (d) Outward-pointing yet negative div: F = r / ||r||^3
    ax = axes[3]
    setup_plane(ax, lim=2.6)
    g2 = np.linspace(-2.2, 2.2, 11)
    X2, Y2 = np.meshgrid(g2, g2)
    R2 = np.sqrt(X2**2 + Y2**2)
    mask = R2 >= 0.75
    U = np.where(mask, X2 / np.maximum(R2, 0.75)**3, np.nan)
    V = np.where(mask, Y2 / np.maximum(R2, 0.75)**3, np.nan)
    ax.quiver(X2, Y2, U, V, color="#1f6feb", scale=6.0, width=0.009, zorder=2)
    box = patches.Rectangle((0.85, 0.85), 1.1, 1.1, lw=2.0, ec="#d97706", fc="#fef3c7", alpha=0.45, zorder=3)
    ax.add_patch(box)
    ax.plot(0, 0, "o", color="#6b7280", mfc="white", ms=6, mew=1.5, zorder=4)
    ax.set_title(r"(d) $\vec{F}=\vec{r}/\|\vec{r}\|^3$ ($\vec{r}\neq\vec{0}$)" + "\n" + r"$\mathrm{div}\,\vec{F}=-1/\|\vec{r}\|^3<0$ (arrows shrink)", fontsize=9.5)

    fig.suptitle("Reconstructed Diagrams: Interpreting Local Divergence from Planar Vector Fields", fontsize=12, fontweight="bold", y=1.01)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "fig01_divergence_models.png"), bbox_inches="tight")
    plt.close(fig)


def make_fig02_curl():
    fig, axes = plt.subplots(1, 4, figsize=(14.5, 3.8), dpi=180)
    g = np.linspace(-2, 2, 9)
    X, Y = np.meshgrid(g, g)

    # (a) CCW: F = -y i + x j
    ax = axes[0]
    setup_plane(ax)
    ax.quiver(X, Y, -Y, X, color="#1f6feb", scale=22, width=0.009, zorder=2)
    circ = patches.Circle((0, 0), 0.55, lw=1.8, ec="#b91c1c", fc="#fee2e2", alpha=0.5, zorder=3)
    ax.add_patch(circ)
    ax.annotate("", xy=(-0.1, 0.55), xytext=(0.45, 0.32),
                arrowprops=dict(arrowstyle="->", color="#b91c1c", lw=2.0, connectionstyle="arc3,rad=0.35"), zorder=4)
    ax.plot(0, 0, "o", color="#b91c1c", ms=4, zorder=5)
    ax.set_title(r"(a) CCW: $\vec{F}=-y\vec{i}+x\vec{j}$" + "\n" + r"$\mathrm{curl}\,\vec{F}=2\vec{k}$ (out of page $\odot$)", fontsize=9.6)

    # (b) CW: F = y i - x j
    ax = axes[1]
    setup_plane(ax)
    ax.quiver(X, Y, Y, -X, color="#1f6feb", scale=22, width=0.009, zorder=2)
    circ = patches.Circle((0, 0), 0.55, lw=1.8, ec="#7c3aed", fc="#ede9fe", alpha=0.5, zorder=3)
    ax.add_patch(circ)
    ax.annotate("", xy=(0.45, 0.32), xytext=(-0.1, 0.55),
                arrowprops=dict(arrowstyle="->", color="#7c3aed", lw=2.0, connectionstyle="arc3,rad=-0.35"), zorder=4)
    ax.plot(0, 0, "x", color="#7c3aed", ms=6, mew=2, zorder=5)
    ax.set_title(r"(b) CW: $\vec{F}=y\vec{i}-x\vec{j}$" + "\n" + r"$\mathrm{curl}\,\vec{F}=-2\vec{k}$ (into page $\otimes$)", fontsize=9.6)

    # (c) Shear with curl: F = -(y+1) i
    ax = axes[2]
    setup_plane(ax)
    ax.quiver(X, Y, -(Y + 1.0), np.zeros_like(Y), color="#1f6feb", scale=24, width=0.009, zorder=2)
    circ = patches.Circle((0, 0), 0.55, lw=1.8, ec="#b91c1c", fc="#fee2e2", alpha=0.5, zorder=3)
    ax.add_patch(circ)
    ax.annotate("", xy=(-0.4, 0.38), xytext=(0.4, 0.38),
                arrowprops=dict(arrowstyle="->", color="#b91c1c", lw=2.0, connectionstyle="arc3,rad=0.3"), zorder=4)
    ax.set_title(r"(c) Shear: $\vec{F}=-(y+1)\vec{i}$" + "\n" + r"$\mathrm{curl}\,\vec{F}=+\vec{k}$ (faster top $\Rightarrow$ CCW)", fontsize=9.4)

    # (d) Two-twigs saddle: F = y i + x j
    ax = axes[3]
    setup_plane(ax)
    ax.quiver(X, Y, Y, X, color="#1f6feb", scale=22, width=0.009, zorder=2)
    ax.plot([-1.0, 1.0], [0, 0], color="#059669", lw=3.0, zorder=3, label="x-twig (CCW)")
    ax.plot([0, 0], [-1.0, 1.0], color="#d97706", lw=3.0, zorder=3, label="y-twig (CW)")
    ax.plot(0, 0, "o", color="#111827", ms=5, zorder=4)
    ax.set_title(r"(d) Saddle: $\vec{F}=y\vec{i}+x\vec{j}$" + "\n" + r"$\mathrm{curl}\,\vec{F}=\vec{0}$ (CCW & CW cancel)", fontsize=9.5)

    fig.suptitle("Reconstructed Diagrams: Paddle-Wheel Rotation and the Right-Hand Rule for Curl", fontsize=12, fontweight="bold", y=1.01)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "fig02_curl_right_hand_rule.png"), bbox_inches="tight")
    plt.close(fig)


def draw_node(ax, x, y, text, color="#dbeafe", ec="#1d4ed8"):
    ax.text(x, y, text, ha="center", va="center", fontsize=12, fontweight="bold",
            bbox=dict(boxstyle="circle,pad=0.32", fc=color, ec=ec, lw=1.6), zorder=4)


def draw_edge(ax, p1, p2, label, lx, ly, color="#374151", lw=1.6, lcolor="#111827"):
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, lw=lw, zorder=2)
    ax.text(lx, ly, label, ha="center", va="center", fontsize=10.5, color=lcolor,
            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85), zorder=5)


def make_fig03_dependency_trees():
    fig, axes = plt.subplots(1, 3, figsize=(14.5, 4.3), dpi=180)
    for ax in axes:
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis("off")

    # (a) 1 independent variable: z -> x, y -> t
    ax = axes[0]
    draw_node(ax, 5, 8.4, r"$z$")
    draw_node(ax, 2.5, 5.0, r"$x$", color="#fef3c7", ec="#d97706")
    draw_node(ax, 7.5, 5.0, r"$y$", color="#fef3c7", ec="#d97706")
    draw_node(ax, 5, 1.6, r"$t$", color="#dcfce7", ec="#15803d")
    draw_edge(ax, (5, 8.4), (2.5, 5.0), r"$\frac{\partial z}{\partial x}$", 3.1, 7.0)
    draw_edge(ax, (5, 8.4), (7.5, 5.0), r"$\frac{\partial z}{\partial y}$", 6.9, 7.0)
    draw_edge(ax, (2.5, 5.0), (5, 1.6), r"$\frac{dx}{dt}$", 3.1, 3.0)
    draw_edge(ax, (7.5, 5.0), (5, 1.6), r"$\frac{dy}{dt}$", 6.9, 3.0)
    ax.text(5, 0.2, r"$\frac{dz}{dt}=\frac{\partial z}{\partial x}\frac{dx}{dt}+\frac{\partial z}{\partial y}\frac{dy}{dt}$",
            ha="center", va="center", fontsize=11, color="#111827")
    ax.set_title("(a) One Independent Variable ($t$)", fontsize=10.5)

    # (b) 2 independent variables: z -> x, y -> u, v (highlight u-paths)
    ax = axes[1]
    draw_node(ax, 5, 8.4, r"$z$")
    draw_node(ax, 2.5, 5.0, r"$x$", color="#fef3c7", ec="#d97706")
    draw_node(ax, 7.5, 5.0, r"$y$", color="#fef3c7", ec="#d97706")
    draw_node(ax, 2.5, 1.6, r"$u$", color="#dcfce7", ec="#15803d")
    draw_node(ax, 7.5, 1.6, r"$v$", color="#dcfce7", ec="#15803d")
    draw_edge(ax, (5, 8.4), (2.5, 5.0), r"$\frac{\partial z}{\partial x}$", 3.1, 7.0, color="#dc2626", lw=2.3, lcolor="#b91c1c")
    draw_edge(ax, (5, 8.4), (7.5, 5.0), r"$\frac{\partial z}{\partial y}$", 6.9, 7.0, color="#dc2626", lw=2.3, lcolor="#b91c1c")
    draw_edge(ax, (2.5, 5.0), (2.5, 1.6), r"$\frac{\partial x}{\partial u}$", 1.5, 3.3, color="#dc2626", lw=2.3, lcolor="#b91c1c")
    draw_edge(ax, (7.5, 5.0), (2.5, 1.6), r"$\frac{\partial y}{\partial u}$", 5.8, 3.9, color="#dc2626", lw=2.3, lcolor="#b91c1c")
    draw_edge(ax, (2.5, 5.0), (7.5, 1.6), r"$\frac{\partial x}{\partial v}$", 4.2, 3.9, color="#9ca3af", lw=1.3, lcolor="#6b7280")
    draw_edge(ax, (7.5, 5.0), (7.5, 1.6), r"$\frac{\partial y}{\partial v}$", 8.5, 3.3, color="#9ca3af", lw=1.3, lcolor="#6b7280")
    ax.text(5, 0.2, r"Red paths: $\frac{\partial z}{\partial u}=\frac{\partial z}{\partial x}\frac{\partial x}{\partial u}+\frac{\partial z}{\partial y}\frac{\partial y}{\partial u}$",
            ha="center", va="center", fontsize=10.5, color="#b91c1c")
    ax.set_title("(b) Two Independent Variables ($u,v$)", fontsize=10.5)

    # (c) Multi-level tree: Ohm's law V(I, R), R(R1, R2), all -> t
    ax = axes[2]
    draw_node(ax, 5, 8.8, r"$V$")
    draw_node(ax, 2.2, 6.2, r"$I$", color="#fef3c7", ec="#d97706")
    draw_node(ax, 7.2, 6.2, r"$R$", color="#fef3c7", ec="#d97706")
    draw_node(ax, 5.2, 3.6, r"$R_1$", color="#fde68a", ec="#b45309")
    draw_node(ax, 8.6, 3.6, r"$R_2$", color="#fde68a", ec="#b45309")
    draw_node(ax, 5, 1.3, r"$t$", color="#dcfce7", ec="#15803d")
    draw_edge(ax, (5, 8.8), (2.2, 6.2), r"$\frac{\partial V}{\partial I}$", 3.0, 7.8)
    draw_edge(ax, (5, 8.8), (7.2, 6.2), r"$\frac{\partial V}{\partial R}$", 6.6, 7.8)
    draw_edge(ax, (2.2, 6.2), (5, 1.3), r"$\frac{dI}{dt}$", 2.8, 3.6)
    draw_edge(ax, (7.2, 6.2), (5.2, 3.6), r"$\frac{\partial R}{\partial R_1}$", 5.7, 5.1)
    draw_edge(ax, (7.2, 6.2), (8.6, 3.6), r"$\frac{\partial R}{\partial R_2}$", 8.5, 5.1)
    draw_edge(ax, (5.2, 3.6), (5, 1.3), r"$\frac{dR_1}{dt}$", 4.3, 2.3)
    draw_edge(ax, (8.6, 3.6), (5, 1.3), r"$\frac{dR_2}{dt}$", 7.4, 2.2)
    ax.text(5, 0.15, r"3 paths from $V$ to $t$ (Ohm's Law + parallel resistors)",
            ha="center", va="center", fontsize=9.8, color="#111827")
    ax.set_title("(c) Multi-Level Dependency Tree", fontsize=10.5)

    fig.suptitle("Reconstructed Diagrams: Multivariable Chain Rule Dependency Trees", fontsize=12, fontweight="bold", y=1.01)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "fig03_dependency_trees.png"), bbox_inches="tight")
    plt.close(fig)


def make_fig04_teaching_examples():
    """Original vector-field diagrams for PT-01 and PT-04 teaching examples."""
    fig, axes = plt.subplots(1, 4, figsize=(14.5, 3.7), dpi=180)
    g = np.linspace(-2, 2, 9)
    X, Y = np.meshgrid(g, g)

    # PT-01(i): F = 2y j at P(1, 1) -> div = 2 > 0
    ax = axes[0]
    setup_plane(ax)
    ax.quiver(X, Y, np.zeros_like(X), 1.4 * Y, color="#1f6feb", scale=22, width=0.009, zorder=2)
    ax.plot(1.0, 1.0, "o", color="#b91c1c", ms=7, zorder=4)
    ax.text(1.15, 1.12, r"$P$", fontsize=11, fontweight="bold", color="#b91c1c")
    ax.set_title("PT-01 Example (i)\nFind sign of div at $P$", fontsize=10)

    # PT-01(ii): F = -2x i at Q(-1, 1) -> div = -2 < 0
    ax = axes[1]
    setup_plane(ax)
    ax.quiver(X, Y, -1.4 * X, np.zeros_like(Y), color="#1f6feb", scale=22, width=0.009, zorder=2)
    ax.plot(-1.0, 1.0, "o", color="#b91c1c", ms=7, zorder=4)
    ax.text(-0.82, 1.12, r"$Q$", fontsize=11, fontweight="bold", color="#b91c1c")
    ax.set_title("PT-01 Example (ii)\nFind sign of div at $Q$", fontsize=10)

    # PT-04(i): Shear F = (y + 1.5) i at origin -> curl = -k (CW)
    ax = axes[2]
    setup_plane(ax)
    ax.quiver(X, Y, Y + 1.5, np.zeros_like(Y), color="#1f6feb", scale=26, width=0.009, zorder=2)
    ax.plot(0, 0, "o", color="#b91c1c", ms=7, zorder=4)
    ax.set_title("PT-04 Example (i)\nCurl direction at $(0,0)$?", fontsize=10)

    # PT-04(ii): Pure radial sink F = -x i - y j at origin -> curl = 0
    ax = axes[3]
    setup_plane(ax)
    ax.quiver(X, Y, -X, -Y, color="#1f6feb", scale=22, width=0.009, zorder=2)
    ax.plot(0, 0, "o", color="#b91c1c", ms=7, zorder=4)
    ax.set_title("PT-04 Example (ii)\nCurl direction at $(0,0)$?", fontsize=10)

    fig.suptitle("Reconstructed Diagrams: Original Teaching-Example Vector Fields (PT-01 and PT-04)", fontsize=11.5, fontweight="bold", y=1.01)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "fig04_teaching_examples.png"), bbox_inches="tight")
    plt.close(fig)


def make_fig05_selftest_fields():
    """Original vector-field diagrams for Self-Test Questions Q1 (div) and Q4 (curl)."""
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.7), dpi=180)
    g = np.linspace(-2, 2, 9)
    X, Y = np.meshgrid(g, g)

    # Self-Test Q1: Horizontal shear F = -y i at P(1, -1) -> div = 0
    ax = axes[0]
    setup_plane(ax)
    ax.quiver(X, Y, -Y, np.zeros_like(Y), color="#1f6feb", scale=18, width=0.009, zorder=2)
    ax.plot(1.0, -1.0, "o", color="#b91c1c", ms=7, zorder=4)
    ax.text(1.18, -0.88, r"$P$", fontsize=11, fontweight="bold", color="#b91c1c")
    ax.set_title("Self-Test Q1 (PT-01)\nSign of divergence at $P$?", fontsize=10)

    # Self-Test Q4: Vertical shear F = (x + 1.5) j at origin -> curl = +k (CCW)
    ax = axes[1]
    setup_plane(ax)
    ax.quiver(X, Y, np.zeros_like(X), X + 1.5, color="#1f6feb", scale=26, width=0.009, zorder=2)
    ax.plot(0, 0, "o", color="#b91c1c", ms=7, zorder=4)
    ax.set_title("Self-Test Q4 (PT-04)\nCurl direction at $(0,0)$?", fontsize=10)

    fig.suptitle("Reconstructed Diagrams: Self-Test Planar Vector Fields", fontsize=11.5, fontweight="bold", y=1.01)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "fig05_selftest_fields.png"), bbox_inches="tight")
    plt.close(fig)


def extract_textbook_figures():
    """Crop original diagrams for §19.3 Ex. 3, 13 (printed p. 1045) and §20.1 Ex. 15, 17 (printed p. 1062)."""
    textbook_pdf = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), "MAT235_textbook.pdf")
    if not os.path.exists(textbook_pdf):
        print("Skipping textbook crop: MAT235_textbook.pdf not found at", textbook_pdf)
        return
    with tempfile.TemporaryDirectory() as tmp:
        for pdf_page in (1065, 1082):
            subprocess.run([
                "gs", "-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=png16m", "-r240",
                f"-dFirstPage={pdf_page}", f"-dLastPage={pdf_page}",
                f"-sOutputFile={tmp}/p{pdf_page}.png", textbook_pdf
            ], check=True)
        im1 = Image.open(f"{tmp}/p1065.png")
        w, h = im1.size
        im1.crop((int(w * 0.155), int(h * 0.305), int(w * 0.485), int(h * 0.420))).save(
            os.path.join(FIG_DIR, "fig06_ex19_3_03.png")
        )
        im1.crop((int(w * 0.520), int(h * 0.325), int(w * 0.885), int(h * 0.562))).save(
            os.path.join(FIG_DIR, "fig07_ex19_3_13.png")
        )
        im2 = Image.open(f"{tmp}/p1082.png")
        w, h = im2.size
        im2.crop((int(w * 0.665), int(h * 0.203), int(w * 0.855), int(h * 0.328))).save(
            os.path.join(FIG_DIR, "fig08_ex20_1_15.png")
        )
        im2.crop((int(w * 0.665), int(h * 0.325), int(w * 0.855), int(h * 0.455))).save(
            os.path.join(FIG_DIR, "fig09_ex20_1_17.png")
        )


if __name__ == "__main__":
    make_fig01_divergence()
    make_fig02_curl()
    make_fig03_dependency_trees()
    make_fig04_teaching_examples()
    make_fig05_selftest_fields()
    extract_textbook_figures()
    print("Generated/extracted 9 figures in", FIG_DIR)
