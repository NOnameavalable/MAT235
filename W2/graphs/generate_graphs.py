"""Reproducible original W2 figures. Run from any directory with NumPy/Matplotlib."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent
plt.rcParams.update({'font.size':10,'axes.titlesize':11,'figure.dpi':130})
x=np.linspace(-2,2,65); X,Y=np.meshgrid(x,x)
def save(fig,name):
 fig.tight_layout();fig.savefig(P/(name+'.png'),dpi=190,bbox_inches='tight');plt.close(fig)
def ax3(fig,n,title):
 a=fig.add_subplot(*n,projection='3d');a.set(xlabel='x',ylabel='y',zlabel='z',title=title);a.view_init(24,-58);return a
def surf(a,Z):a.plot_surface(X,Y,Z,cmap='viridis',alpha=.85,linewidth=0,rstride=2,cstride=2)
def flat(a,title,xl='x',yl='y'):
 a.set(title=title,xlabel=xl,ylabel=yl);a.axhline(0,color='gray',lw=.6);a.axvline(0,color='gray',lw=.6);a.grid(alpha=.25)
f=plt.figure(figsize=(11,7))
for k,(z,t) in enumerate([(1+X-Y,'Plane: z = 1+x-y'),(X*X+Y*Y,'Paraboloid: z = x²+y²'),(X*X-Y*Y,'Saddle: z = x²-y²'),(X*X,'Parabolic cylinder: z = x²')]):surf(ax3(f,(2,2,k+1),t),z)
save(f,'01-surfaces')
f=plt.figure(figsize=(11,3.8));t=np.linspace(0,2*np.pi,65);u=np.linspace(0,np.pi,45);T,U=np.meshgrid(t,u)
a=ax3(f,(1,3,1),'Sphere: x²+y²+z² = 1');a.plot_surface(np.sin(U)*np.cos(T),np.sin(U)*np.sin(T),np.cos(U),alpha=.6,color='teal');a.plot([0,0],[0,0],[-1.6,1.6],c='crimson');a.scatter([0,0],[0,0],[-1,1],c='crimson');a.set_box_aspect((1,1,1))
a=ax3(f,(1,3,2),'Upper hemisphere');U=U/2;a.plot_surface(np.sin(U)*np.cos(T),np.sin(U)*np.sin(T),np.cos(U),color='teal');a.set_zlim(-1,1);a.set_box_aspect((1,1,1))
a=ax3(f,(1,3,3),'Cylinder: x²+y² = 1');T,Z=np.meshgrid(t,np.linspace(-2,2,25));a.plot_surface(np.cos(T),np.sin(T),Z,alpha=.6,color='teal');a.set_box_aspect((1,1,1.5));save(f,'02-sphere-cylinder')
f,a=plt.subplots(1,2,figsize=(10,3.5));v=np.linspace(-2.2,2.2,400)
for c in [-1,0,1]:a[0].plot(v,v**3+c*v,label=f'x = {c}');a[1].plot(v,c**3+v*c,label=f'y = {c}')
flat(a[0],'z = y³+xy: x fixed','y','z');flat(a[1],'z = y³+xy: y fixed','x','z')
for b in a:b.legend();b.set_ylim(-9,9)
save(f,'03-cross-sections')
f,a=plt.subplots(1,2,figsize=(10,4));v=np.linspace(-3.1,3.1,301);XX,YY=np.meshgrid(v,v)
for b,Z,lv,title in [(a[0],XX**2+YY**2,[2,4,6,8],'Paraboloid: levels 0,2,4,6,8'),(a[1],np.sqrt(XX**2+YY**2),[1,2,3],'Cone: levels 0,1,2,3')]:
 cs=b.contour(XX,YY,Z,levels=lv,cmap='viridis');b.clabel(cs,inline=True,fmt='%g');b.plot(0,0,'ko',ms=3);b.annotate('0',(0,0),xytext=(5,5),textcoords='offset points');flat(b,title);b.set_aspect('equal')
save(f,'04-radial-contours')
f,a=plt.subplots(1,2,figsize=(10,4))
for b,Z,lv,title in [(a[0],2*YY-XX,[0,2,4,6],'Plane: z = 2y-x'),(a[1],XX**2-YY**2,[-4,-2,0,2,4],'Saddle: z = x²-y²')]:
 cs=b.contour(XX,YY,Z,levels=lv,cmap='coolwarm');b.clabel(cs,fmt='%g');flat(b,title);b.set_aspect('equal')
a[0].annotate('increasing z',xy=(-1,2),xytext=(0,0),arrowprops={'arrowstyle':'->'});save(f,'05-plane-saddle-contours')
f=plt.figure(figsize=(10,4));a=ax3(f,(1,2,1),'Tent roof: finite domain');xx,yy=np.meshgrid(np.linspace(0,2,41),np.linspace(0,3,31));a.plot_surface(xx,yy,4*np.minimum(xx,2-xx),color='teal',alpha=.7);a.set(xlabel='x (m)',ylabel='y (m)',zlabel='h (m)');
for name,p in {'A':(0,0,0),'B':(2,0,0),'C':(2,3,0),'D':(0,3,0),'P':(1,0,4),'Q':(1,3,4)}.items():a.text(*p,name)
b=f.add_subplot(1,2,2)
for c in [0,1,2,3,4]:
 for xx in sorted(set([c/4,2-c/4])):b.plot([xx,xx],[0,3],label=None,color=plt.cm.viridis(c/5));b.text(xx,3.06,str(c),ha='center',fontsize=9)
b.set(xlim=(-.15,2.15),ylim=(-.1,3.35),xlabel='x (m)',ylabel='y (m)',title='Tent contours (labels: height in m)');b.grid(alpha=.25);save(f,'06-tent')
f=plt.figure(figsize=(11,3.7))
for k,(Z,title) in enumerate([((X-1)**2+(Y-2)**2,'Shift: z=(x-1)²+(y-2)²'),(np.exp(-(X*X+Y*Y)),'Gaussian: z=exp(-x²-y²)'),(9-X*X-Y*Y,'Downward bowl: z=9-x²-y²')]):surf(ax3(f,(1,3,k+1),title),Z)
save(f,'07-transformations')
f,a=plt.subplots(1,2,figsize=(10,3.7));xx,yy=np.meshgrid(np.linspace(0,4,101),np.linspace(0,4,101));cs=a[0].contour(xx,yy,12-2*xx-yy,levels=[2,4,6,8,10],cmap='viridis');a[0].clabel(cs,fmt='%g');a[0].scatter([1,2,3],[4,2,0],color='crimson');flat(a[0],'Linear interpolation: f=12-2x-y');a[0].set_aspect('equal')
xx,yy=np.meshgrid(np.linspace(.1,6,100),np.linspace(.1,6,100));cs=a[1].contour(xx,yy,xx**.5*yy**.5,levels=[1,2,3,4,5],cmap='viridis');a[1].clabel(cs,fmt='%g');flat(a[1],'Production: P=√(KN)','K (capital units)','N (labor units)');save(f,'08-table-production')
f=plt.figure(figsize=(11,3.7));a=ax3(f,(1,3,1),'Preview: level surfaces x²+y²+z²=c');T,U=np.meshgrid(t,np.linspace(0,np.pi,40))
for r in [1,2]:a.plot_wireframe(r*np.sin(U)*np.cos(T),r*np.sin(U)*np.sin(T),r*np.cos(U),rstride=6,cstride=7,alpha=.6,label=f'c={r*r}')
a.legend(fontsize=8);a.set_box_aspect((1,1,1));a=ax3(f,(1,3,2),'Preview: y²+z²=1');T,V=np.meshgrid(t,np.linspace(-2,2,20));a.plot_surface(V,np.cos(T),np.sin(T),color='teal',alpha=.6);a=ax3(f,(1,3,3),'Preview: z=1');surf(a,np.ones_like(X));save(f,'09-level-surfaces')
f,a=plt.subplots(1,2,figsize=(10,3.8));xx,yy=np.meshgrid(np.linspace(-3,3,201),np.linspace(-3,3,201));cs=a[0].contour(xx,yy,12-xx**2-yy**2,levels=[4,8,10],cmap='viridis');a[0].clabel(cs,fmt='%g');a[0].plot([1.5],[0],'ro');a[0].annotate('A',(1.5,0),xytext=(3,7),textcoords='offset points');flat(a[0],'Self-test contour map');a[0].set_aspect('equal');v=np.linspace(-2,2,200)
for b in [-1,0,1]:a[1].plot(v,v*v-b*b,label=f'y={b}')
flat(a[1],'Self-test slices','x','z');a[1].legend();save(f,'10-self-test')
# Additional labelled lecture representations.
f=plt.figure(figsize=(9,4));a=ax3(f,(1,2,1),'Upper hemisphere and x = 1/2 slice');T,U=np.meshgrid(np.linspace(0,2*np.pi,60),np.linspace(0,np.pi/2,30));a.plot_surface(np.sin(U)*np.cos(T),np.sin(U)*np.sin(T),np.cos(U),color='lightsteelblue',alpha=.38);v=np.linspace(-np.sqrt(3)/2,np.sqrt(3)/2,150);a.plot(np.full_like(v,.5),v,np.sqrt(.75-v*v),color='crimson',lw=3,label='x=1/2');a.legend();a.set_box_aspect((1,1,1))
b=f.add_subplot(1,2,2);b.plot(v,np.sqrt(.75-v*v),color='crimson',lw=2);flat(b,'Trace in x=1/2 plane','y','z');b.set_aspect('equal');b.set_ylim(0,1);save(f,'11-hemisphere-slice')
f,a=plt.subplots(1,2,figsize=(10,4));t=np.linspace(0,12,120);d=np.linspace(0,5,120)
def heat(d,t):return 20+10*(1-np.exp(-t/4))*np.exp(-d/2)
for v in [1,2,3]:a[0].plot(t,heat(v,t),label=f'd={v} m')
for v in [0,5,10]:a[1].plot(d,heat(d,v),label=f't={v} min')
flat(a[0],'Illustrative heater model: fix d','t (min)','T (°C)');flat(a[1],'Illustrative heater model: fix t','d (m)','T (°C)')
for b in a:b.legend()
save(f,'12-heater-cross-sections')
f=plt.figure(figsize=(9,4));a=ax3(f,(1,2,1),'Coordinate points');points={'P':(0,0,2),'Q':(3,4,0),'R':(0,4,5),'S':(3,4,5)}
for label,pt in points.items():a.scatter(*pt,s=55);a.text(*pt,label)
a.set(xlim=(0,4),ylim=(0,5),zlim=(0,6));b=ax3(f,(1,2,2),'Plane: x/4+y/3+z/2=1');xx,yy=np.meshgrid(np.linspace(0,4,60),np.linspace(0,3,60));zz=2-xx/2-2*yy/3;zz=np.where(zz>=0,zz,np.nan);b.plot_surface(xx,yy,zz,alpha=.5,color='teal');
for label,pt in {'X':(4,0,0),'Y':(0,3,0),'Z':(0,0,2)}.items():b.scatter(*pt,color='crimson');b.text(*pt,label)
save(f,'13-coordinates-plane')
f=plt.figure(figsize=(6,4));a=ax3(f,(1,1,1),'Tent distance: shoes to bug');P0=(0,1,0);Q0=(.5,1,2);a.scatter(*P0,color='blue',s=80);a.scatter(*Q0,color='crimson',s=80);a.text(*P0,' shoes (0,1,0)');a.text(*Q0,' bug (1/2,1,2)');a.plot([0,.5],[1,1],[0,2],color='black',lw=2,label='d=√17/2 m');a.plot([0,.5],[1,1],[0,0],color='teal',ls='--',label='Δx=1/2 m');a.plot([.5,.5],[1,1],[0,2],color='orange',ls='--',label='Δz=2 m');a.set(xlim=(-.2,.9),ylim=(.6,1.4),zlim=(-.1,2.5));a.legend(loc='upper left',fontsize=8);save(f,'14-distance')
