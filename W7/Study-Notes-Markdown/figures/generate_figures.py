import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

OUT = os.path.dirname(os.path.abspath(__file__))
plt.rcParams.update({
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.labelsize": 10,
    "figure.dpi": 160,
})

# 1. Cross-section slopes (Concept C2)
def make_cross_section_slopes():
    fig = plt.figure(figsize=(10, 4.3))
    X, Y = np.meshgrid(np.linspace(-2, 2, 50), np.linspace(-2, 2, 50))
    Z = 4.5 - 0.5 * X**2 - 0.5 * Y**2
    a, b = 1.0, 0.5
    z0 = 4.5 - 0.5 * a**2 - 0.5 * b**2
    fx0, fy0 = -a, -b

    # Panel 1: y = b slice -> f_x(a,b)
    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    ax1.plot_surface(X, Y, Z, alpha=0.35, color='#4C8BF5', edgecolor='none')
    xs = np.linspace(-2, 2, 100)
    ax1.plot(xs, np.full_like(xs, b), 4.5 - 0.5*xs**2 - 0.5*b**2, color='#1A3A7A', lw=2.2, label='Slice $z=f(x,b)$')
    xt = np.linspace(a - 0.9, a + 0.9, 20)
    ax1.plot(xt, np.full_like(xt, b), z0 + fx0*(xt - a), color='#D93025', lw=2.4, label=f'Tangent (slope $f_x={fx0:.1f}$)')
    ax1.scatter([a], [b], [z0], color='black', s=35, zorder=5)
    ax1.set_xlabel('$x$'); ax1.set_ylabel('$y$'); ax1.set_zlabel('$z$')
    ax1.set_title('Fix $y = b$: slope along $x$ is $f_x(a,b)$')
    ax1.view_init(elev=24, azim=35)
    ax1.legend(loc='upper right', fontsize=8.5)

    # Panel 2: x = a slice -> f_y(a,b)
    ax2 = fig.add_subplot(1, 2, 2, projection='3d')
    ax2.plot_surface(X, Y, Z, alpha=0.35, color='#4C8BF5', edgecolor='none')
    ys = np.linspace(-2, 2, 100)
    ax2.plot(np.full_like(ys, a), ys, 4.5 - 0.5*a**2 - 0.5*ys**2, color='#0F7B6C', lw=2.2, label='Slice $z=f(a,y)$')
    yt = np.linspace(b - 0.9, b + 0.9, 20)
    ax2.plot(np.full_like(yt, a), yt, z0 + fy0*(yt - b), color='#D93025', lw=2.4, label=f'Tangent (slope $f_y={fy0:.1f}$)')
    ax2.scatter([a], [b], [z0], color='black', s=35, zorder=5)
    ax2.set_xlabel('$x$'); ax2.set_ylabel('$y$'); ax2.set_zlabel('$z$')
    ax2.set_title('Fix $x = a$: slope along $y$ is $f_y(a,b)$')
    ax2.view_init(elev=24, azim=35)
    ax2.legend(loc='upper right', fontsize=8.5)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, 'fig_cross_section_slopes.png'), bbox_inches='tight')
    plt.close(fig)

# 2. PT-03 Teaching Example contour diagram: f(x,y) = 20 - (x-1)^2 - (y+1)^2 (concentric around (1,-1))
def make_pt03_teaching():
    fig, ax = plt.subplots(figsize=(5.2, 4.6))
    x = np.linspace(-2, 4, 300)
    y = np.linspace(-4, 2, 300)
    X, Y = np.meshgrid(x, y)
    Z = 20 - ((X - 1)**2 + (Y + 1)**2)
    levels = [4, 8, 12, 16, 19]
    cs = ax.contour(X, Y, Z, levels=levels, colors='#1E5AA8', linewidths=1.8)
    ax.clabel(cs, inline=True, fmt='%d', fontsize=9)
    # Points P(3, -1) on z=16? Wait: (3-1)^2 + 0 = 4 -> z=16! Let's put P=(3,-1) and Q=(-1, 1) -> (4+4=8 -> z=12)
    ax.scatter([3, -1], [-1, 1], color='#D93025', s=50, zorder=5)
    ax.annotate('$P(3,-1)$', (3, -1), xytext=(3.15, -0.75), fontweight='bold', color='#B31412')
    ax.annotate('$Q(-1,1)$', (-1, 1), xytext=(-0.85, 1.25), fontweight='bold', color='#B31412')
    ax.axhline(0, color='gray', lw=0.8, alpha=0.6)
    ax.axvline(0, color='gray', lw=0.8, alpha=0.6)
    ax.grid(True, linestyle=':', alpha=0.5)
    ax.set_aspect('equal')
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_title('Contour Diagram of $z = f(x,y)$ (PT-03 Teaching Example)')
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, 'fig_pt03_teaching_contour.png'), bbox_inches='tight')
    plt.close(fig)

# 3. PT-06 Teaching Example contour diagram: linear/mildly curved temperature T(x,y) with clear grid
# T(x,y) = 30 - 3x + 2y on [0,6] x [0,6], contours 18, 21, 24, 27, 30, 33, 36
def make_pt06_teaching():
    fig, ax = plt.subplots(figsize=(5.6, 4.8))
    x = np.linspace(0, 6, 300)
    y = np.linspace(0, 6, 300)
    X, Y = np.meshgrid(x, y)
    T = 30 - 3*X + 2*Y
    levels = [12, 15, 18, 21, 24, 27, 30, 33, 36, 39]
    cs = ax.contour(X, Y, T, levels=levels, colors='#1E5AA8', linewidths=1.8)
    ax.clabel(cs, inline=True, fmt='%d', fontsize=9)
    # Mark point (2, 3) -> T = 30 - 6 + 6 = 30
    ax.scatter([2], [3], color='#D93025', s=55, zorder=5)
    ax.annotate('$(2, 3)$', (2, 3), xytext=(2.15, 3.2), fontweight='bold', color='#B31412')
    ax.set_xticks(range(0, 7))
    ax.set_yticks(range(0, 7))
    ax.grid(True, linestyle='-', color='#CCCCCC', lw=0.8)
    ax.set_aspect('equal')
    ax.set_xlabel('$x$ (meters)')
    ax.set_ylabel('$y$ (meters)')
    ax.set_title('Temperature $T(x,y)$ ($^\\circ$C) Contour Diagram (PT-06 Teaching Example)')
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, 'fig_pt06_teaching_contour.png'), bbox_inches='tight')
    plt.close(fig)

# 4. §14.1 #41 Four-panel contour diagrams
def make_14_1_41():
    fig, axes = plt.subplots(2, 2, figsize=(7.5, 6.8))
    x = np.linspace(-3, 3, 200)
    y = np.linspace(-3, 3, 200)
    X, Y = np.meshgrid(x, y)
    configs = [
        ('(a) $f_x > 0,\\; f_y > 0$ (e.g., $f=x+y$)', X + Y),
        ('(b) $f_x > 0,\\; f_y < 0$ (e.g., $f=x-y$)', X - Y),
        ('(c) $f_x < 0,\\; f_y > 0$ (e.g., $f=-x+y$)', -X + Y),
        ('(d) $f_x < 0,\\; f_y < 0$ (e.g., $f=-x-y$)', -X - Y),
    ]
    for ax, (title, Z) in zip(axes.flat, configs):
        cs = ax.contour(X, Y, Z, levels=[-4, -2, 0, 2, 4], colors='#1E5AA8', linewidths=1.6)
        ax.clabel(cs, inline=True, fmt='%d', fontsize=8.5)
        ax.axhline(0, color='gray', lw=0.7)
        ax.axvline(0, color='gray', lw=0.7)
        ax.set_aspect('equal')
        ax.set_xlabel('$x$')
        ax.set_ylabel('$y$')
        ax.set_title(title, fontsize=9.8)
        ax.grid(True, linestyle=':', alpha=0.45)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, 'fig_ex14_1_41_four_cases.png'), bbox_inches='tight')
    plt.close(fig)

# 5. §14.2 #41 and #43 contour comparison centered at (1,1) with equal scales
def make_14_2_41_43():
    fig, axes = plt.subplots(1, 3, figsize=(9.6, 3.2))
    x = np.linspace(0.2, 1.8, 250)
    y = np.linspace(0.2, 1.8, 250)
    X, Y = np.meshgrid(x, y)
    panels = [
        ('(I) Matches #43: $x^2 + e^{y^2}$\n$|f_y(1,1)| > |f_x(1,1)|$', X**2 + np.exp(Y**2), np.arange(1, 20, 1.5)),
        ('(II) Matches #41: $x^2 + y^2$\n$|f_x(1,1)| = |f_y(1,1)|$', X**2 + Y**2, np.arange(0.5, 8, 0.7)),
        ('(III) For ref (#42): $e^{x^2} + y^2$\n$|f_x(1,1)| > |f_y(1,1)|$', np.exp(X**2) + Y**2, np.arange(1, 20, 1.5)),
    ]
    for ax, (title, Z, lvls) in zip(axes, panels):
        ax.contour(X, Y, Z, levels=lvls, colors='#1E5AA8', linewidths=1.4)
        ax.scatter([1], [1], color='#D93025', s=35, zorder=5)
        ax.set_aspect('equal')
        ax.set_xlim(0.2, 1.8); ax.set_ylim(0.2, 1.8)
        ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
        ax.set_title(title, fontsize=9.2)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, 'fig_ex14_2_41_43_contours.png'), bbox_inches='tight')
    plt.close(fig)

# 6. Week7-sol.pdf PDF p. 4 concentric contour diagram (Instructor Q9)
def make_week7sol_p4():
    fig, ax = plt.subplots(figsize=(5.0, 4.4), dpi=180)
    theta = np.linspace(0, 2*np.pi, 300)
    for rad, lbl in zip([1.0, 2.0, 3.0], ['1', '2', '3']):
        ax.plot(rad*np.cos(theta), rad*np.sin(theta), color='#1E5AA8', lw=1.9)
        ang = np.deg2rad(68)
        ax.text(rad*np.cos(ang), rad*np.sin(ang)+0.12, lbl, color='#1E5AA8', fontsize=10.5, fontweight='bold', ha='center')
    ax.annotate('', xy=(3.7, 0), xytext=(-3.6, 0), arrowprops=dict(arrowstyle='->', color='#222222', lw=1.2))
    ax.annotate('', xy=(0, 3.7), xytext=(0, -3.6), arrowprops=dict(arrowstyle='->', color='#222222', lw=1.2))
    ax.text(3.75, -0.05, '$x$', fontsize=11, va='center')
    ax.text(0.12, 3.65, '$y$', fontsize=11, ha='left')
    ax.text(-0.25, -0.32, '$0$', fontsize=9.5, color='#444444')
    ax.scatter([1.0, 2.0], [0, 0], color='#1E5AA8', s=45, zorder=5)
    ax.scatter([1.45], [0], color='#D93025', marker='x', s=75, linewidths=2.2, zorder=6)
    ax.text(1.0, -0.38, '$a$', fontsize=11, ha='center', fontweight='bold')
    ax.text(1.45, 0.25, '$x_0$', fontsize=11, ha='center', color='#B31412', fontweight='bold')
    ax.text(2.0, -0.38, '$b$', fontsize=11, ha='center', fontweight='bold')
    ax.set_xlim(-3.8, 4.1); ax.set_ylim(-3.8, 4.0); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('Contour Diagram of $f(x,y)$ (Week7-sol.pdf, PDF p. 4)', fontsize=10.5)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, 'fig_week7sol_p4_concentric.png'), bbox_inches='tight', facecolor='white')
    plt.close(fig)

if __name__ == '__main__':
    make_cross_section_slopes()
    make_pt03_teaching()
    make_pt06_teaching()
    make_14_1_41()
    make_14_2_41_43()
    make_week7sol_p4()
    print("Generated all programmatic figures successfully.")
