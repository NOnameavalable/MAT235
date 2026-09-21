"""Rebuild the Week 1 study figures with Python, NumPy, and Matplotlib."""
from pathlib import Path
import os
os.environ.setdefault('MPLCONFIGDIR', '/tmp/mat235-matplotlib')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path(__file__).parent
plt.rcParams.update({'font.size': 11, 'axes.titlesize': 13, 'figure.facecolor': 'white'})

def space(ax, title, lim=(-3, 3)):
    ax.set(xlabel='x', ylabel='y', zlabel='z', title=title,
           xlim=lim, ylim=lim, zlim=lim)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=24, azim=-55)

def save(fig, name):
    # 3D axis labels can fall outside Matplotlib's tight bounding box.
    # Place the height-variable label in axes coordinates so it is retained.
    for ax in fig.axes:
        if hasattr(ax, 'zaxis'):
            ax.set_zlabel('')
            label_x = -.04 if ax.azim < -90 else 1.02
            ax.text2D(label_x, .60, 'z', transform=ax.transAxes)
    fig.savefig(OUT / name, dpi=180, bbox_inches='tight')
    plt.close(fig)

# Coordinate planes and a line defined by two simultaneous constraints.
fig = plt.figure(figsize=(12, 5))
u, v = np.meshgrid(np.linspace(-3, 3, 15), np.linspace(-3, 3, 15))
ax = fig.add_subplot(121, projection='3d')
space(ax, 'The three coordinate planes')
ax.plot_surface(u, v, 0*u, color='#3b82f6', alpha=.23)
ax.plot_surface(u, 0*u, v, color='#f59e0b', alpha=.23)
ax.plot_surface(0*u, u, v, color='#10b981', alpha=.23)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=c, alpha=.4, label=s) for c,s in
    [('#3b82f6','xy: z = 0'),('#f59e0b','xz: y = 0'),('#10b981','yz: x = 0')]],
    loc='upper left', fontsize=9)
ax = fig.add_subplot(122, projection='3d')
space(ax, 'Two planes intersect in a line', (-1, 5))
u, v = np.meshgrid(np.linspace(-1, 5, 15), np.linspace(-1, 5, 15))
ax.plot_surface(u, v, 0*u+2, color='#3b82f6', alpha=.18)
ax.plot_surface(u, 0*u+4, v, color='#f59e0b', alpha=.18)
x = np.linspace(-1, 5, 100)
ax.plot(x, 0*x+4, 0*x+2, color='#be123c', lw=3, label='(x, 4, 2): x is free')
ax.legend(loc='upper left', fontsize=9)
save(fig, '01-coordinate-planes.png')

# Distance decomposed into perpendicular coordinate steps.
fig = plt.figure(figsize=(7, 6))
ax = fig.add_subplot(111, projection='3d')
space(ax, 'Distance from P = (1, 2, 1) to Q = (-3, 1, 2)', (-3.5, 3.5))
P, A, B, Q = map(np.array, [(1,2,1), (-3,2,1), (-3,1,1), (-3,1,2)])
for a, b, label, color in [(P,A,'x change: -4 (length 4)','#2563eb'), (A,B,'y change: -1 (length 1)','#059669'), (B,Q,'z change: +1 (length 1)','#f59e0b')]:
    ax.plot(*np.stack([a,b]).T, '--', color=color, lw=2,label=label)
ax.plot(*np.stack([P,Q]).T, color='#be123c', lw=3, label='Direct distance = sqrt(18)')
for p, label in [(P,'P'), (Q,'Q')]:
    ax.scatter(*p, color='#be123c', s=35)
    ax.text(*(p + .15), label)
M=(P+Q)/2
ax.scatter(*M,color='#7c3aed',s=40)
ax.text(*(M+np.array([0,.3,-.25])),'M: midpoint',fontsize=9)
ax.legend(loc='upper left',fontsize=9)
save(fig, '02-distance.png')

# Sphere-plane intersection, plus an undistorted view within the plane.
fig = plt.figure(figsize=(12, 5))
ax = fig.add_subplot(121, projection='3d')
space(ax, 'Sphere x² + y² + z² = 5 cut by z = 2')
theta, phi = np.meshgrid(np.linspace(0, 2*np.pi, 60), np.linspace(0,np.pi,35))
r = np.sqrt(5)
ax.plot_surface(r*np.sin(phi)*np.cos(theta), r*np.sin(phi)*np.sin(theta), r*np.cos(phi), color='#3b82f6', alpha=.16, linewidth=0)
u,v = np.meshgrid(np.linspace(-2.5,2.5,12), np.linspace(-2.5,2.5,12))
ax.plot_surface(u,v,0*u+2, color='#f59e0b', alpha=.17)
t = np.linspace(0,2*np.pi,200)
ax.plot(np.cos(t),np.sin(t),0*t+2, color='#be123c', lw=3)
ax = fig.add_subplot(122)
ax.plot(np.cos(t),np.sin(t), color='#be123c', lw=3)
ax.plot([0,1],[0,0], color='#334155', lw=2)
ax.text(.3,.08,'radius = 1')
ax.scatter([0],[0],color='#334155')
ax.set(xlabel='x',ylabel='y',title='View within the plane z = 2: x² + y² = 1', xlim=(-1.5,1.5),ylim=(-1.5,1.5))
ax.set_aspect('equal'); ax.grid(alpha=.25)
save(fig, '03-sphere-section.png')

# Exact cylinder-volume slices; explicitly use a mathematical model.
fig, axes = plt.subplots(1,2,figsize=(11,4.5))
h = np.linspace(0,5,100)
for r in [1,2]:
    axes[0].plot(h,np.pi*r*r*h,lw=2,label=f'r = {r}')
axes[0].set(xlabel='Height h (cm)',ylabel='Volume V (cm³)',title='Fix radius: V = πr²h is linear in h')
r = np.linspace(0,3,100)
for h in [1,2]:
    axes[1].plot(r,np.pi*r*r*h,lw=2,label=f'h = {h}')
axes[1].set(xlabel='Radius r (cm)',ylabel='Volume V (cm³)',title='Fix height: V = πhr² is quadratic in r')
for ax in axes:
    ax.legend(); ax.grid(alpha=.25); ax.set_xlim(left=0); ax.set_ylim(bottom=0)
fig.tight_layout()
save(fig, '04-fixed-variable.png')

# A supplementary example from the W1 worksheet.
fig = plt.figure(figsize=(7,6))
ax = fig.add_subplot(111, projection='3d')
space(ax, 'Supplement: x² + y² = 1 leaves z free')
t,z = np.meshgrid(np.linspace(0,2*np.pi,60),np.linspace(-3,3,25))
ax.plot_surface(np.cos(t),np.sin(t),z,color='#3b82f6',alpha=.3)
t = np.linspace(0,2*np.pi,200)
for z in [-2,0,2]:
    ax.plot(np.cos(t),np.sin(t),0*t+z,lw=2,label=f'z = {z}')
ax.legend(loc='upper left')
save(fig, '05-cylinder.png')

# The unanswered worksheet plane z = 1 + x - y.
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(221, projection='3d')
space(ax, 'Plane z = 1 + x - y (finite window)', (-2, 2))
ax.set_zlim(-3,5)
ax.view_init(elev=25,azim=-120)
x, y = np.meshgrid(np.linspace(-2, 2, 25), np.linspace(-2, 2, 25))
z = 1 + x - y
ax.plot_surface(x, y, z, color='#60a5fa', alpha=.42, edgecolor='none')
pts = np.array([[-1,0,0],[0,1,0],[0,0,1]])
for p, label in zip(pts, ['x-intercept (-1,0,0)','y-intercept (0,1,0)','z-intercept (0,0,1)']):
    ax.scatter(*p, s=45, label=label)
ax.legend(loc='upper left', fontsize=8)
xx = np.linspace(-3,3,150)
for pos, xlabel, ylabel, title, values, color in [
    (222,'x','y','xy-plane: z = 0, y = 1 + x',1+xx,'#2563eb'),
    (223,'y','z','yz-plane: x = 0, z = 1 - y',1-xx,'#be123c'),
    (224,'x','z','xz-plane: y = 0, z = 1 + x',1+xx,'#059669')]:
    ax=fig.add_subplot(pos)
    ax.plot(xx,values,lw=2.5,color=color)
    ax.axhline(0,color='#334155',lw=.8); ax.axvline(0,color='#334155',lw=.8)
    ax.set(xlabel=xlabel,ylabel=ylabel,title=title,xlim=(-3,3),ylim=(-4,4))
    ax.grid(alpha=.25)
fig.tight_layout()
save(fig, '06-plane-z-1-plus-x-minus-y.png')

# All six worksheet cross-sections of z = y^3 + xy.
fig, axes = plt.subplots(1,2,figsize=(12,4.8))
y = np.linspace(-2,2,300)
labels_x={-1:'x = -1: z = y³ - y',0:'x = 0: z = y³',1:'x = 1: z = y³ + y'}
for c, color in zip([-1,0,1], ['#2563eb','#be123c','#059669']):
    axes[0].plot(y, y**3+c*y, lw=2.4, color=color, label=labels_x[c])
axes[0].set(xlabel='y',ylabel='z',title='Fix x: cubic cross-sections',xlim=(-2,2),ylim=(-9,9))
x = np.linspace(-3,3,200)
labels_y={-1:'y = -1: z = -1 - x',0:'y = 0: z = 0',1:'y = 1: z = 1 + x'}
for c, color in zip([-1,0,1], ['#2563eb','#be123c','#059669']):
    axes[1].plot(x, c**3+x*c, lw=2.4, color=color, label=labels_y[c])
axes[1].set(xlabel='x',ylabel='z',title='Fix y: linear cross-sections',xlim=(-3,3),ylim=(-5,5))
for ax in axes:
    ax.axhline(0,color='#334155',lw=.8); ax.axvline(0,color='#334155',lw=.8)
    ax.grid(alpha=.25); ax.legend(fontsize=9)
fig.tight_layout()
save(fig, '07-cross-sections-y3-plus-xy.png')

# A clearly labelled illustrative model for the room-temperature prompt.
def temp(d,t): return 68 + 18*np.exp(-.6*d)*(1-np.exp(-.35*t))
fig, axes = plt.subplots(1,2,figsize=(12,4.8))
t=np.linspace(0,15,250)
for d in [1,2,3]: axes[0].plot(t,temp(d,t),lw=2.4,label=f'd = {d} m')
axes[0].set(xlabel='Time t (min)',ylabel='Temperature T (°F)',title='Fixed distance: T increases with time')
d=np.linspace(0,5,250)
for t0 in [0,5,10]: axes[1].plot(d,temp(d,t0),lw=2.4,label=f't = {t0} min')
axes[1].set(xlabel='Distance d (m)',ylabel='Temperature T (°F)',title='Fixed time: T decreases with distance')
for ax in axes: ax.grid(alpha=.25); ax.legend()
fig.suptitle('One plausible model: T(d,t) = 68 + 18e⁻⁰·⁶ᵈ(1-e⁻⁰·³⁵ᵗ)')
fig.tight_layout()
save(fig, '08-room-temperature-sections.png')

# A generic contour-map reading diagram (not a reproduction of the textbook map).
fig, ax = plt.subplots(figsize=(7,5.5))
x,y=np.meshgrid(np.linspace(-3,3,300),np.linspace(-2.5,2.5,250))
T=75+5*x-2*y+3*np.sin(y)
levels=np.arange(60,96,5)
cs=ax.contour(x,y,T,levels=levels,colors='#2563eb')
ax.clabel(cs,inline=True,fmt='%d°F')
ax.scatter([-.6],[.35],color='#be123c',s=45,zorder=3)
ax.text(-.48,.47,'P (between 70°F and 75°F)',fontsize=10)
ax.set(xlabel='east-west position',ylabel='north-south position',title='How a contour map represents T = f(x,y)')
ax.grid(alpha=.15)
save(fig, '09-contour-map.png')

# Function test: a parabola passes and an ellipse fails the vertical-line test.
fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))
x = np.linspace(-2.2, 2.2, 400)
axes[0].plot(x, x**2 - 1, color='#2563eb', lw=2.7)
axes[0].axvline(.8, color='#be123c', ls='--', lw=2, label='x = 0.8: one intersection')
axes[0].scatter([.8], [.8**2-1], color='#be123c', zorder=3)
axes[0].set(title='Passes: y = x² - 1', xlabel='x', ylabel='y', xlim=(-2.2,2.2), ylim=(-2,4))
t = np.linspace(0, 2*np.pi, 500)
axes[1].plot(2*np.cos(t), np.sin(t), color='#2563eb', lw=2.7)
x0=1
y0=np.sqrt(1-x0**2/4)
axes[1].axvline(x0, color='#be123c', ls='--', lw=2, label='x = 1: two intersections')
axes[1].scatter([x0,x0],[y0,-y0],color='#be123c',zorder=3)
axes[1].set(title='Fails: x²/4 + y² = 1', xlabel='x', ylabel='y', xlim=(-2.2,2.2), ylim=(-2,2))
for ax in axes:
    ax.axhline(0,color='#334155',lw=.8); ax.grid(alpha=.22); ax.legend(); ax.set_aspect('equal', adjustable='box')
fig.suptitle('Vertical-line test: one output y for each input x')
fig.tight_layout()
save(fig, '10-function-test.png')

# The four plotted points from the handwritten worksheet.
fig = plt.figure(figsize=(8,6.5))
ax = fig.add_subplot(111, projection='3d')
space(ax, 'Plotting points in 3-space', (0,5.5))
points={'P (0,0,2)':(0,0,2),'Q (3,4,0)':(3,4,0),'R (0,4,5)':(0,4,5),'S (3,4,5)':(3,4,5)}
colors=['#be123c','#2563eb','#059669','#7c3aed']
for (label,p),color in zip(points.items(),colors):
    ax.scatter(*p,s=55,color=color,label=label)
    ax.plot([p[0],p[0]],[p[1],p[1]],[0,p[2]],ls=':',color=color,alpha=.75)
ax.legend(loc='upper left')
save(fig, '11-points-in-3space.png')

# Parallel horizontal planes z = -1, 0, 3.
fig = plt.figure(figsize=(8,6.5))
ax = fig.add_subplot(111, projection='3d')
space(ax, 'Constant-z equations are horizontal planes', (-3,3))
u,v=np.meshgrid(np.linspace(-3,3,14),np.linspace(-3,3,14))
for z0,color in [(-1,'#2563eb'),(0,'#f59e0b'),(3,'#059669')]:
    ax.plot_surface(u,v,0*u+z0,color=color,alpha=.25)
ax.set_zlim(-2,4)
ax.legend(handles=[Patch(color=c,alpha=.45,label=f'z = {z0}') for z0,c in [(-1,'#2563eb'),(0,'#f59e0b'),(3,'#059669')]],loc='upper left')
save(fig, '12-parallel-z-planes.png')

# Introductory cross-sections drawn in the handwritten notes.
fig, axes = plt.subplots(1,2,figsize=(11,4.6))
y=np.linspace(-3,3,300)
axes[0].plot(y,y,color='#2563eb',lw=2.7)
axes[0].set(title='z = x + y at x = 0',xlabel='y',ylabel='z',xlim=(-3,3),ylim=(-3,3))
axes[1].plot(y,y**2,color='#059669',lw=2.7)
axes[1].set(title='z = x² + y² at x = 0',xlabel='y',ylabel='z',xlim=(-3,3),ylim=(-1,9))
for ax in axes:
    ax.axhline(0,color='#334155',lw=.8); ax.axvline(0,color='#334155',lw=.8); ax.grid(alpha=.22)
fig.suptitle('Cross-sections in the vertical plane x = 0')
fig.tight_layout()
save(fig, '13-intro-cross-sections.png')

# Exercise 5: top-view movement while facing the yz-plane.
fig, ax = plt.subplots(figsize=(7.5,6))
ax.axvline(0,color='#059669',lw=4,alpha=.5,label='yz-plane: x = 0')
start=np.array([3,1]); turn=np.array([1,1]); end=np.array([1,-1])
ax.annotate('',xy=turn,xytext=start,arrowprops=dict(arrowstyle='->',lw=3,color='#2563eb'))
ax.annotate('',xy=end,xytext=turn,arrowprops=dict(arrowstyle='->',lw=3,color='#be123c'))
ax.scatter(*start,s=55,color='#2563eb'); ax.scatter(*turn,s=55,color='#7c3aed'); ax.scatter(*end,s=55,color='#be123c')
ax.text(*(start+[-.1,.15]),'Start (3,1,1)',ha='right'); ax.text(*(turn+[-.35,.35]),'Turn (1,1,1)'); ax.text(*(end+[.08,-.22]),'Finish (1,-1,1)')
ax.text(1.75,.78,'forward: -x',color='#2563eb'); ax.text(1.08,0,'left: -y',color='#be123c',rotation=90)
ax.set(xlabel='x',ylabel='y',title='Exercise 5 top view (z remains 1)',xlim=(-.5,3.8),ylim=(-1.7,1.8))
ax.axhline(0,color='#334155',lw=1,label='xz-plane in top view: y = 0')
ax.set_aspect('equal'); ax.grid(alpha=.2); ax.legend(loc='lower right')
save(fig, '14-exercise-5-movement.png')

# Assigned graphing exercises 13, 15, and 19.
fig = plt.figure(figsize=(16,5.2))
u,v=np.meshgrid(np.linspace(-5,5,18),np.linspace(-2,6,18))
ax=fig.add_subplot(131,projection='3d'); space(ax,'Exercise 13: x = -3',(-5,5))
ax.plot_surface(0*u-3,u,v,color='#2563eb',alpha=.35)
ax.scatter([-3],[0],[0],color='#be123c',s=45,label='x-intercept (-3,0,0)'); ax.legend(fontsize=8)
ax=fig.add_subplot(132,projection='3d'); space(ax,'Exercise 15: y = 4 and z = 2',(-2,6))
xx=np.linspace(-2,6,150); ax.plot(xx,0*xx+4,0*xx+2,color='#be123c',lw=4,label='(x,4,2), x is free'); ax.legend(fontsize=8)
ax=fig.add_subplot(133,projection='3d'); space(ax,'Exercise 19: y = 3',(-5,5))
ax.plot_surface(u,0*u+3,v,color='#059669',alpha=.35)
ax.scatter([0],[3],[0],color='#be123c',s=45,label='y-intercept (0,3,0)'); ax.legend(fontsize=8)
fig.tight_layout()
save(fig, '15-assigned-graphing-exercises.png')

# Closed-cylinder geometry used to derive volume and total area.
fig=plt.figure(figsize=(7,6))
ax=fig.add_subplot(111,projection='3d')
t,z=np.meshgrid(np.linspace(0,2*np.pi,70),np.linspace(0,3,25))
ax.plot_surface(2*np.cos(t),2*np.sin(t),z,color='#60a5fa',alpha=.35)
angle,rad=np.meshgrid(np.linspace(0,2*np.pi,70),np.linspace(0,2,25))
for zz in [0,3]:
    ax.plot_surface(rad*np.cos(angle),rad*np.sin(angle),0*rad+zz,color='#60a5fa',alpha=.3)
ax.plot([0,2],[0,0],[3,3],color='#be123c',lw=3,label='r: centre to rim')
ax.plot([2,2],[0,0],[0,3],color='#059669',lw=3,label='h: vertical height')
ax.set(xlabel='x',ylabel='y',zlabel='z',title='Closed cylinder: two circular ends + curved side',xlim=(-2.5,2.5),ylim=(-2.5,2.5),zlim=(0,3.5))
ax.set_box_aspect((1,1,1)); ax.legend(loc='upper left'); ax.view_init(elev=25,azim=-55)
save(fig,'18-closed-cylinder.png')

# Actual surfaces for the handwritten function rules.
fig=plt.figure(figsize=(16,5))
x,y=np.meshgrid(np.linspace(-2,2,45),np.linspace(-2,2,45))
for pos,title,z,zlim in [(131,'z = xy: a saddle',x*y,(-4,4)),(132,'z = x² + y²: upward paraboloid',x*x+y*y,(0,8)),(133,'z = 3: constant horizontal plane',0*x+3,(0,4))]:
    ax=fig.add_subplot(pos,projection='3d'); space(ax,title,(-2,2)); ax.set_zlim(*zlim)
    ax.plot_surface(x,y,z,cmap='viridis',alpha=.75)
fig.tight_layout(); save(fig,'19-basic-function-surfaces.png')

# Sphere boundary versus solid ball, including the original unit-sphere idea.
fig=plt.figure(figsize=(12,10))
theta,phi=np.meshgrid(np.linspace(0,2*np.pi,60),np.linspace(0,np.pi,40))
ax=fig.add_subplot(221,projection='3d')
ax.plot_surface(1+4*np.sin(phi)*np.cos(theta),-2+4*np.sin(phi)*np.sin(theta),3+4*np.cos(phi),color='#60a5fa',alpha=.28)
ax.scatter([1],[-2],[3],color='#be123c',s=40,label='Centre (1,-2,3)')
ax.plot([1,5],[-2,-2],[3,3],color='#be123c',lw=3,label='Radius = 4')
ax.set(xlabel='x',ylabel='y',zlabel='z',title='Translated sphere: distance = 4',xlim=(-3.5,5.5),ylim=(-6.5,2.5),zlim=(-1.5,7.5))
ax.set_box_aspect((1,1,1)); ax.legend(fontsize=9)
t=np.linspace(0,2*np.pi,300)
ax=fig.add_subplot(222)
ax.fill(1+4*np.cos(t),-2+4*np.sin(t),color='#60a5fa',alpha=.25,label='Ball section: filled disk')
ax.plot(1+4*np.cos(t),-2+4*np.sin(t),color='#be123c',lw=2.5,label='Sphere section: circle only')
ax.scatter([1],[-2],color='#be123c'); ax.set(xlabel='x',ylabel='y',title='Central section z = 3',xlim=(-4,6),ylim=(-7,3)); ax.set_aspect('equal'); ax.grid(alpha=.2); ax.legend(fontsize=9)
ax=fig.add_subplot(223,projection='3d'); space(ax,'Unit sphere: x² + y² + z² = 1',(-1.2,1.2))
ax.plot_surface(np.sin(phi)*np.cos(theta),np.sin(phi)*np.sin(theta),np.cos(phi),color='#60a5fa',alpha=.3)
ax.plot([0,1],[0,0],[0,0],color='#be123c',lw=3,label='Radius = 1'); ax.legend()
ax=fig.add_subplot(224)
ax.fill(np.cos(t),np.sin(t),color='#60a5fa',alpha=.3,label='Unit ball: central disk included')
ax.plot(np.cos(t),np.sin(t),color='#be123c',lw=2,label='Boundary included (≤)')
ax.set(xlabel='x',ylabel='y',title='Unit ball x² + y² + z² ≤ 1, slice z = 0',xlim=(-1.3,1.3),ylim=(-1.3,1.3)); ax.set_aspect('equal'); ax.grid(alpha=.2); ax.legend(fontsize=9)
fig.tight_layout(); save(fig,'20-sphere-and-ball.png')

# Verbal set descriptions: intersection line and an open half-space.
fig=plt.figure(figsize=(12,5.5))
ax=fig.add_subplot(121,projection='3d'); space(ax,'x = 0 and z = -2: infinite line')
u,v=np.meshgrid(np.linspace(-3,3,15),np.linspace(-3,3,15))
ax.plot_surface(0*u,u,v,color='#60a5fa',alpha=.17)
yy=np.linspace(-3,3,100); ax.plot(0*yy,yy,0*yy-2,color='#be123c',lw=3,label='(0,y,-2), y is free'); ax.legend(fontsize=9)
ax=fig.add_subplot(122,projection='3d'); space(ax,'Behind the board: x < 0 (finite window)')
ax.plot_surface(0*u,u,v,color='#059669',alpha=.2)
ax.text(0,2,2,'Boundary x = 0\nexcluded',fontsize=9)
for xx in [-2.5,-1.5,-.5]:
    ax.scatter(0*u.ravel()+xx,u.ravel(),v.ravel(),color='#60a5fa',alpha=.12,s=7)
ax.text(-2,0,0,'x < 0',color='#be123c',fontsize=13)
fig.tight_layout(); save(fig,'21-verbal-regions.png')

# Source points A-D with perpendicular distances to the xz-plane.
fig=plt.figure(figsize=(8,6.5)); ax=fig.add_subplot(111,projection='3d'); space(ax,'Distance to xz-plane = |y|',(-4.5,4.5))
u,v=np.meshgrid(np.linspace(-4,4,15),np.linspace(-1,5,15)); ax.plot_surface(u,0*u,v,color='#60a5fa',alpha=.14)
for name,p,color in [('A',(1,-1,0),'#be123c'),('B',(0,3,4),'#2563eb'),('C',(2,2,1),'#059669'),('D',(0,-4,0),'#7c3aed')]:
    ax.scatter(*p,color=color,s=45,label=f'{name} {p}, |y| = {abs(p[1])}')
    ax.plot([p[0],p[0]],[p[1],0],[p[2],p[2]],'--',color=color,lw=2)
ax.legend(fontsize=9,loc='upper left'); ax.set_zlim(-1,5); save(fig,'22-coordinate-plane-test.png')

# Extra self-test answer graphs (not source textbook diagrams).
fig=plt.figure(figsize=(12,10))
ax=fig.add_subplot(221); y=np.linspace(-2,2,200); ax.plot(y,y**3+2*y,lw=2.5); ax.set(xlabel='y',ylabel='z',title='Self-test 19: x = 2, z = y³ + 2y'); ax.grid(alpha=.2)
ax=fig.add_subplot(222); x=np.linspace(-3,3,200); ax.plot(x,-8-2*x,lw=2.5,color='#be123c'); ax.set(xlabel='x',ylabel='z',title='Self-test 19: y = -2, z = -8 - 2x'); ax.grid(alpha=.2)
ax=fig.add_subplot(223,projection='3d'); space(ax,'Self-test 20: x² + z² = 4, y free',(-3,3))
t,y=np.meshgrid(np.linspace(0,2*np.pi,60),np.linspace(-3,3,25)); ax.plot_surface(2*np.cos(t),y,2*np.sin(t),color='#60a5fa',alpha=.3)
ax=fig.add_subplot(224,projection='3d'); space(ax,'Self-test 13: x² + y² = 4, z free',(-3,3))
ax.plot_surface(2*np.cos(t),2*np.sin(t),y,color='#60a5fa',alpha=.3)
fig.tight_layout(); save(fig,'23-self-test-graphs.png')

# Question figures that do not reveal the function-test or contour answers.
fig,axes=plt.subplots(1,2,figsize=(12,5))
t=np.linspace(0,2*np.pi,300)
axes[0].plot(2*np.cos(t),np.sin(t),lw=2.5,color='#2563eb')
axes[0].set(xlabel='x',ylabel='y',title='Self-test 15: x²/4 + y² = 1',xlim=(-2.4,2.4),ylim=(-1.5,1.5)); axes[0].set_aspect('equal'); axes[0].grid(alpha=.2)
axes[1].axvline(0,color='#2563eb',lw=2,label='60°F contour'); axes[1].axvline(4,color='#059669',lw=2,label='68°F contour')
axes[1].scatter([1],[0],color='#be123c',s=50); axes[1].text(1.1,.05,'Q: one quarter across')
axes[1].set(xlabel='Position x (arbitrary distance units)',ylabel='Position y (arbitrary distance units)',title='Self-test 16: schematic contour map',xlim=(-.5,4.5),ylim=(-1,1)); axes[1].legend(loc='lower center'); axes[1].grid(alpha=.2)
fig.tight_layout(); save(fig,'25-self-test-question-figures.png')
