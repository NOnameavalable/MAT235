"""Generate supporting figures for MAT235 Week 10 Study Notes and Answers."""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "figures")
os.makedirs(OUT_DIR, exist_ok=True)

plt.rcParams.update({
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.labelsize": 10,
    "figure.dpi": 180,
})


def make_fig1_taylor():
    fig = plt.figure(figsize=(11.5, 4.6))

    # Left: 3D comparison of f(x,y)=x^2 y, L(x,y)=y, Q(x,y)=y+2(x-1)y near (1,0)
    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    x = np.linspace(0.4, 1.6, 40)
    y = np.linspace(-0.5, 0.5, 40)
    X, Y = np.meshgrid(x, y)
    F = X**2 * Y
    L = Y
    Q = Y + 2 * (X - 1) * Y

    ax1.plot_surface(X, Y, F, color="#1f77b4", alpha=0.65, linewidth=0, antialiased=True)
    ax1.plot_wireframe(X, Y, Q, color="#d62728", rstride=5, cstride=5, linewidth=1.0, alpha=0.85)
    ax1.plot_surface(X, Y, L, color="#2ca02c", alpha=0.25, linewidth=0)
    ax1.scatter([1.0], [0.0], [0.0], color="black", s=45, zorder=10)
    ax1.set_title(r"$f(x,y)=x^2 y$ vs. $L(x,y)$ and $Q(x,y)$ near $(1,0)$")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.set_zlabel("z")
    ax1.view_init(elev=22, azim=-55)

    # Custom legend proxies
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    proxies = [
        Patch(facecolor="#1f77b4", alpha=0.65, label=r"Exact $f(x,y)=x^2 y$"),
        Line2D([0], [0], color="#d62728", lw=1.6, label=r"Quadratic $Q(x,y)=y+2(x-1)y$"),
        Patch(facecolor="#2ca02c", alpha=0.35, label=r"Linear $L(x,y)=y$"),
    ]
    ax1.legend(handles=proxies, loc="upper left", fontsize=8.5, frameon=True)

    # Right: Slice along y = 0.2 showing accuracy near x = 1 (and at x = 0.9)
    ax2 = fig.add_subplot(1, 2, 2)
    xs = np.linspace(0.4, 1.6, 200)
    y0 = 0.2
    fs = xs**2 * y0
    ls = np.full_like(xs, y0)
    qs = y0 + 2 * (xs - 1.0) * y0

    ax2.plot(xs, fs, color="#1f77b4", lw=2.3, label=r"Exact $f(x,0.2)=0.2x^2$")
    ax2.plot(xs, qs, color="#d62728", lw=2.0, ls="--", label=r"Quadratic $Q(x,0.2)=0.4x-0.2$")
    ax2.plot(xs, ls, color="#2ca02c", lw=2.0, ls=":", label=r"Linear $L(x,0.2)=0.2$")

    # Highlight x = 0.9
    x_eval = 0.9
    f_eval, l_eval, q_eval = 0.162, 0.200, 0.160
    ax2.axvline(1.0, color="gray", lw=0.9, ls="-.", alpha=0.6)
    ax2.axvline(x_eval, color="#555555", lw=0.9, ls="--", alpha=0.5)
    ax2.scatter([x_eval, x_eval, x_eval], [f_eval, q_eval, l_eval],
                color=["#1f77b4", "#d62728", "#2ca02c"], s=36, zorder=5)
    ax2.annotate(
        r"At $(0.9, 0.2)$:" + "\n"
        + r"$|f-L|=0.038$" + "\n"
        + r"$|f-Q|=0.002$",
        xy=(x_eval, f_eval),
        xytext=(0.45, 0.34),
        arrowprops=dict(arrowstyle="->", color="#333333", lw=1.0),
        bbox=dict(boxstyle="round,pad=0.35", facecolor="#fff8e7", edgecolor="#cc9900"),
        fontsize=8.8,
    )
    ax2.text(1.02, 0.49, r"$x=1$ (expansion)", fontsize=8.5, color="#444444")
    ax2.set_title(r"Cross-section at $y = 0.2$ (Error Comparison)")
    ax2.set_xlabel("x")
    ax2.set_ylabel("z")
    ax2.set_ylim(0.0, 0.55)
    ax2.grid(True, alpha=0.25)
    ax2.legend(loc="lower right", fontsize=8.5, frameon=True)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig1_taylor_linear_vs_quadratic.png"), bbox_inches="tight")
    plt.close(fig)


def make_fig2_diff_surfaces():
    fig = plt.figure(figsize=(12.2, 4.0))
    u = np.linspace(-1.0, 1.0, 65)
    X, Y = np.meshgrid(u, u)

    # (a) Differentiable: e^{-(x^2+y^2)}
    ax1 = fig.add_subplot(1, 3, 1, projection="3d")
    Z1 = np.exp(-(X**2 + Y**2))
    ax1.plot_surface(X, Y, Z1, cmap="viridis", alpha=0.85, linewidth=0)
    # Tangent plane at (0,0): z = 1
    tp = np.linspace(-0.6, 0.6, 10)
    TX, TY = np.meshgrid(tp, tp)
    ax1.plot_surface(TX, TY, np.ones_like(TX), color="#ff7f0e", alpha=0.35, linewidth=0)
    ax1.set_title("(a) Differentiable at (0,0)\n" + r"$f(x,y)=e^{-x^2-y^2}$ (smooth)")
    ax1.set_xlabel("x"); ax1.set_ylabel("y"); ax1.set_zlabel("z")
    ax1.view_init(elev=25, azim=-45)

    # (b) Cone: sqrt(x^2+y^2)
    ax2 = fig.add_subplot(1, 3, 2, projection="3d")
    Z2 = np.sqrt(X**2 + Y**2)
    ax2.plot_surface(X, Y, Z2, cmap="plasma", alpha=0.88, linewidth=0)
    ax2.scatter([0], [0], [0], color="black", s=35)
    ax2.set_title("(b) Continuous, NOT Differentiable\n" + r"$f(x,y)=\sqrt{x^2+y^2}$ (sharp vertex)")
    ax2.set_xlabel("x"); ax2.set_ylabel("y"); ax2.set_zlabel("z")
    ax2.view_init(elev=22, azim=-45)

    # (c) x^{1/3} y^{1/3}
    ax3 = fig.add_subplot(1, 3, 3, projection="3d")
    Z3 = np.cbrt(X) * np.cbrt(Y)
    ax3.plot_surface(X, Y, Z3, cmap="coolwarm", alpha=0.88, linewidth=0)
    ax3.plot_surface(TX, TY, np.zeros_like(TX), color="#888888", alpha=0.25, linewidth=0)
    ax3.set_title("(c) Partials Exist, NOT Differentiable\n" + r"$f(x,y)=x^{1/3}y^{1/3}$ ($f_x=f_y=0$)")
    ax3.set_xlabel("x"); ax3.set_ylabel("y"); ax3.set_zlabel("z")
    ax3.view_init(elev=25, azim=-45)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig2_differentiability_comparison.png"), bbox_inches="tight")
    plt.close(fig)


def make_fig3_logic_map():
    fig, ax = plt.subplots(figsize=(11.4, 4.9))
    ax.set_xlim(0, 11.4)
    ax.set_ylim(0, 4.9)
    ax.axis("off")

    def box(x, y, w, h, title, body, fc, ec):
        p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.12,rounding_size=0.18",
                           facecolor=fc, edgecolor=ec, linewidth=1.8)
        ax.add_patch(p)
        ax.text(x + w / 2, y + h * 0.68, title, ha="center", va="center",
                fontsize=10, fontweight="bold", color="#111111")
        ax.text(x + w / 2, y + h * 0.28, body, ha="center", va="center",
                fontsize=8.6, color="#222222")

    # Left: Sufficient condition
    box(0.25, 2.05, 2.85, 1.45,
        "Sufficient Condition\n(Continuously Diff.)",
        r"$f_x, f_y$ exist & are continuous" + "\non a disk around $(a,b)$",
        "#e6f4ea", "#1e8e3e")

    # Middle: Differentiable
    box(4.15, 2.05, 2.75, 1.45,
        "Differentiable\nat $(a,b)$",
        "Locally linear (graph looks\nlike a plane on zoom-in)",
        "#e8f0fe", "#1a73e8")

    # Right top: Continuous
    box(8.0, 3.15, 3.1, 1.25,
        "Continuous at $(a,b)$",
        r"$\lim_{(x,y)\to(a,b)} f(x,y)=f(a,b)$",
        "#fef7e0", "#f9ab00")

    # Right bottom: Partials exist + Chain Rule
    box(8.0, 1.15, 3.1, 1.45,
        "Partials Exist & Chain Rule",
        r"$f_x(a,b), f_y(a,b)$ exist;" + "\n" + r"$f_{\vec{u}}(a,b)=\nabla f(a,b)\cdot\vec{u}$",
        "#fef7e0", "#f9ab00")

    # Valid implication arrows (blue)
    arrow_kw = dict(arrowstyle="-|>,head_width=0.3,head_length=0.45", lw=2.2, color="#1a73e8")
    ax.annotate("", xy=(4.10, 2.78), xytext=(3.15, 2.78), arrowprops=arrow_kw)
    ax.text(3.62, 3.02, "IMPLIES", ha="center", fontsize=8.3, fontweight="bold", color="#1a73e8")

    ax.annotate("", xy=(7.95, 3.75), xytext=(6.95, 3.05), arrowprops=arrow_kw)
    ax.annotate("", xy=(7.95, 1.90), xytext=(6.95, 2.50), arrowprops=arrow_kw)
    ax.text(7.42, 2.78, "IMPLIES", ha="center", fontsize=8.3, fontweight="bold", color="#1a73e8")

    # Converse FAILS annotations (red)
    ax.text(3.62, 1.25,
            "Converse FALSE!\n" + r"e.g. $(x^2+y^2)\sin\!\left(1/\sqrt{x^2+y^2}\right)$",
            ha="center", va="center", fontsize=8.2, color="#c5221f",
            bbox=dict(boxstyle="round,pad=0.35", facecolor="#fce8e6", edgecolor="#c5221f", lw=1.0))

    ax.text(5.7, 0.38,
            "Converses FALSE!   "
            + r"Continuous $\nRightarrow$ Diff.: $\sqrt{x^2+y^2}$" + "   |   "
            + r"Partials exist $\nRightarrow$ Diff.: $x^{1/3}y^{1/3}$" + "   |   "
            + r"Partials exist $\nRightarrow$ Cont.: $xy/(x^2+y^2)$",
            ha="center", va="center", fontsize=8.3, color="#c5221f",
            bbox=dict(boxstyle="round,pad=0.35", facecolor="#fce8e6", edgecolor="#c5221f", lw=1.0))

    ax.set_title("Week 10 Differentiability Implications & Counterexamples (TT2 Scope)",
                 fontsize=11.5, fontweight="bold", pad=6)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig3_differentiability_logic_map.png"), bbox_inches="tight")
    plt.close(fig)


def make_fig4_contours():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 4.0))

    # Exercise 25: vertical lines 1,2,3,4,5 getting closer as x increases; P ON contour 3
    xs = [0.0, 1.2, 2.15, 2.85, 3.35]
    for val, xv in zip([1, 2, 3, 4, 5], xs):
        ax1.plot([xv, xv], [0, 4], color="#2a6fdb", lw=1.8)
        ax1.text(xv, 3.15, str(val), ha="center", va="center",
                 bbox=dict(facecolor="white", edgecolor="none", pad=1.2), fontsize=9.5)
    ax1.scatter([xs[2]], [1.9], color="black", s=45, zorder=5)
    ax1.text(xs[2] + 0.14, 2.08, "P", fontsize=10.5, fontweight="bold")
    ax1.set_xlim(-0.5, 4.0)
    ax1.set_ylim(-0.2, 4.2)
    ax1.set_title("§14.7 Exercise 25 (Reconstructed)\nVertical contours, spacing decreases rightward")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.set_xticks([]); ax1.set_yticks([])

    # Exercise 29: EQUALLY SPACED diagonal lines x + y = c (slope -1), values 1..5; P ON contour 3
    cs = [0.8, 1.6, 2.4, 3.2, 4.0]
    for val, c in zip([1, 2, 3, 4, 5], cs):
        # segment in first quadrant x >= 0, y >= 0 (matching textbook triangular clip)
        xl = np.linspace(0.0, c, 50)
        yl = c - xl
        ax2.plot(xl, yl, color="#2a6fdb", lw=1.8)
        # label along x = y diagonal (shifted slightly upper-left)
        lx = c / 2.0 - 0.18
        ly = c / 2.0 + 0.18
        ax2.text(lx, ly, str(val), ha="center", va="center",
                 bbox=dict(facecolor="white", edgecolor="none", pad=1.0), fontsize=9.5)
    # P ON contour 3 (c = 2.4)
    px, py = 1.35, 2.4 - 1.35
    ax2.scatter([px], [py], color="black", s=45, zorder=5)
    ax2.text(px + 0.18, py + 0.22, "P", fontsize=10.5, fontweight="bold")
    ax2.set_xlim(-0.2, 4.3)
    ax2.set_ylim(-0.2, 4.3)
    ax2.set_aspect("equal")
    ax2.set_title("§14.7 Exercise 29 (Reconstructed)\nEqually spaced diagonal contours (slope -1)")
    ax2.set_xlabel("x")
    ax2.set_ylabel("y")
    ax2.set_xticks([]); ax2.set_yticks([])

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig4_ex14_7_25_29_contours.png"), bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    make_fig1_taylor()
    make_fig2_diff_surfaces()
    make_fig3_logic_map()
    make_fig4_contours()
    print("Generated all 4 figures in", OUT_DIR)
