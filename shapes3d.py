import numpy as np

class Shape:
    def __init__(self):
        self.color='black'
        self.linestyle='-'
        self.x=[]
        self.y=[]
        self.z=[]
        return
    def setX(self,x):
        self.x=x
    def setY(self,y):
        self.y=y
    def setZ(self,z):
        self.z=z
    def setColor(self,color):
        self.color=color
    def setLineStyle(self,linestyle):
        self.linestyle=linestyle
    def draw(self,ax,text='',alpha=1):
        ax.plot(self.x,self.y,self.z,color=self.color,linestyle=self.linestyle,alpha=alpha)
        ax.text(self.x[-1],self.y[-1],self.z[-1],text)

class Line(Shape):
    def __init__(self):
        super().__init__()
        self.p1=np.array([0,0,0])
        self.p2=np.array([0,0,0])
    def setPoints(self,p1,p2):
        self.p1=np.array(p1)
        self.p2=np.array(p2)

    def getXYZ(self,d):
        self.x=np.linspace(self.p1[0],self.p2[0],d)
        self.y=np.linspace(self.p1[1],self.p2[1],d)
        self.z=np.linspace(self.p1[2],self.p2[2],d)
        return self.x,self.y,self.z

    def draw(self,ax,text='',alpha=1,d=10):
        self.x,self.y,self.z=self.getXYZ(d)
        ax.plot(self.x,self.y,self.z,color=self.color,linestyle=self.linestyle,alpha=alpha)
        ax.text(self.x[d//2],self.y[d//2],self.z[d//2],text)

class Coordinate(Shape):
    def __init__(self):
        super().__init__()
        self.p=np.array([0,0,0])
        self.dx=np.array([1,0,0])
        self.dy=np.array([0,1,0])
        self.dz=np.array([0,0,1])
    def setPoints(self,p):
        self.p=np.array(p)
    def setCoordinates(self,dx,dy,dz):
        self.dx=np.array(dx)
        self.dy=np.array(dy)
        self.dz=np.array(dz)
    def getCoordinates(self):
        return self.dx,self.dy,self.dz
    def is_orthogonal(self):
        if not (np.inner(self.dx,self.dy)==0 and np.inner(self.dx,self.dz)==0 and np.inner(self.dy,self.dz)==0):
            print("Not Normal...(setCoordinates)")
            return False
        else:
            return True
    def normalize(self):
        self.dx=self.dx/np.linalg.norm(self.dx)
        self.dy=self.dy/np.linalg.norm(self.dy)
        self.dz=self.dz/np.linalg.norm(self.dz)
    def rotationMatrix(self):
        A=np.concatenate((self.dx.reshape(-1,1),self.dy.reshape(-1,1),self.dz.reshape(-1,1)),axis=1)
        return A
    def move(self,xx,yy,zz):
        return xx+self.p[0], yy+self.p[1], zz+self.p[2]
    def rotate(self,xx,yy,zz):
        A=self.rotationMatrix()
        xyz=np.concatenate((xx.reshape(-1,1),yy.reshape(-1,1),zz.reshape(-1,1)),axis=1).T
        xyz1=np.matmul(A,xyz)
        return xyz1[0], xyz1[1], xyz1[2]
    def transform(self,xx,yy,zz):
        xx,yy,zz=self.rotate(xx,yy,zz)
        xxx,yyy,zzz=self.move(xx,yy,zz)
        return xxx,yyy,zzz
    def draw(self,ax,text='',alpha=0.6,d=10):
        x=Line()
        y=Line()
        z=Line()
        x.setPoints(self.p,self.p+self.dx)
        y.setPoints(self.p,self.p+self.dy)
        z.setPoints(self.p,self.p+self.dz)
        x.setColor(self.color)
        y.setColor(self.color)
        z.setColor(self.color)
        x.draw(ax,text,alpha,d)
        y.draw(ax,text,alpha,d)
        z.draw(ax,text,alpha,d)

class Shape2D(Shape):
    def __init__(self):
        super().__init__()
        self.coordinate=Coordinate()
    def setPoints(self,p):
        self.coordinate.setPoints(p)
    def setLines(self,l1,l2):
        l1=np.array(l1)
        l2=np.array(l2)
        l3=np.cross(l1,l2)
        self.coordinate.setCoordinates(l1,l2,l3)
    def setOtherPoints(self,p1,p2):
        self.setLines((np.array(p1)-self.coordinate.p),(np.array(p2)-self.coordinate.p))
    def setNLine(self,n,l1):
        n=np.array(n)
        l1=np.array(l1)
        if not np.inner(n,l1)==0:
            print("Not Normal... (setNLine)")
            return
        l2=np.cross(n,l1)
        self.coordinate.setCoordinates(l1,l2,n)
    def normalize(self):
        self.coordinate.normalize()
    def draw2D(self,ax,text='',alpha=0.3):
        ax.plot_wireframe(self.x,self.y,self.z,color=self.color,linestyle=self.linestyle,alpha=alpha)

class Plane(Shape2D):   # 2 Lines or 2 Points
    def __init__(self):
        super().__init__()
    def draw_base(self,d):
        xx=np.linspace(0,1,d)
        yy=np.linspace(0,1,d)
        xx,yy=np.meshgrid(xx,yy)
        xx=xx.reshape(-1,1)
        yy=yy.reshape(-1,1)
        zz=np.zeros((d*d,1))
        return xx,yy,zz
    def getXYZ(self,d):
        xx,yy,zz=self.draw_base(d)
        self.x,self.y,self.z=self.coordinate.transform(xx,yy,zz)
        self.x=self.x.reshape(-1,d)
        self.y=self.y.reshape(-1,d)
        self.z=self.z.reshape(-1,d)
        return self.x,self.y,self.z
    def draw2D(self,ax,text='',alpha=0.3,d=30):
        self.x,self.y,self.z=self.getXYZ(d)
        super().draw2D(ax,alpha)

class ArcPlane(Plane):  #(2 Lines -> to rotation matrix...)->setLines or (1 Line, 1 normal, theta -> to rotation matrix...) -> setNLine
    def __init__(self):
        super().__init__()
        self.r=[0,1]
        self.theta=[0,2*np.pi]
    def setRadius(self,r):
        self.r=r
    def setTheta(self,theta):
        self.theta=theta
    def draw_base(self,d):
        if self.coordinate.is_orthogonal()==False:
            rr=np.linspace(0,1,d)
            tt=np.linspace(0,np.pi/2,d)
        else:
            self.coordinate.normalize()
            rr=np.linspace(self.r[0],self.r[1],d)
            tt=np.linspace(self.theta[0],self.theta[1],d)
        rr,tt=np.meshgrid(rr,tt)
        xx=rr*np.cos(tt)
        yy=rr*np.sin(tt)
        xx=xx.reshape(-1,1)
        yy=yy.reshape(-1,1)
        zz=np.zeros((d*d,1))
        return xx,yy,zz

    def draw2D(self,ax,mode='in',text='',alpha=0.3,d=30):
        if self.coordinate.is_orthogonal()==False:
            if mode=='in':
                self.x,self.y,self.z=self.getXYZ(d)
                super().draw2D(ax,text,alpha,d)
            else:
                ap1=ArcPlane()
                ap1.setPoints(self.coordinate.p)
                ap1.setLines(self.coordinate.dy,-self.coordinate.dx)
                ap1.setColor(self.color)
                ap1.setLineStyle(self.linestyle)
                ap2=ArcPlane()
                ap2.setPoints(self.coordinate.p)
                ap2.setLines(-self.coordinate.dx,-self.coordinate.dy)
                ap2.setColor(self.color)
                ap2.setLineStyle(self.linestyle)
                ap3=ArcPlane()
                ap3.setPoints(self.coordinate.p)
                ap3.setLines(-self.coordinate.dy,self.coordinate.dx)
                ap3.setColor(self.color)
                ap3.setLineStyle(self.linestyle)
                ap1.draw2D(ax,mode='in',text=text,alpha=alpha,d=d//3)
                ap2.draw2D(ax,mode='in',text=text,alpha=alpha,d=d//3)
                ap3.draw2D(ax,mode='in',text=text,alpha=alpha,d=d//3)
        else:
            self.x,self.y,self.z=self.getXYZ(d)
            super().draw2D(ax,text,alpha,d)

class CirclePlane(ArcPlane):    #(1 normal, 1 line) -> setN
    def __init__(self):
        super().__init__()
        self.r=[0,1]
        self.theta=[0,2*np.pi]
    def setLines(self,l1,l2):
        print("No use setLines in circleplane! Please use setNLine")
        return
    def draw2D(self,ax,mode='in',text='',alpha=0.3,d=30):
        self.x,self.y,self.z=self.getXYZ(d)
        super().draw2D(ax,text,alpha,d)

class SphereArc(Shape2D):
    def __init__(self):
        super().__init__()
        self.r=1
        self.theta=[0,2*np.pi]
        self.phi=[0,np.pi]
    def setRadius(self,r):
        self.r=r
    def setTheta(self,theta):
        self.theta=theta
    def setPhi(self,phi):
        self.phi=phi
    def draw_base(self,d):
        theta_ls=np.linspace(self.theta[0],self.theta[1],d)
        phi_ls=np.linspace(self.phi[0],self.phi[1],d)
        ts,ps=np.meshgrid(theta_ls,phi_ls)
        xx=self.r*np.cos(ts)*np.sin(ps)
        yy=self.r*np.sin(ts)*np.sin(ps)
        zz=self.r*np.cos(ps)
        return xx,yy,zz
    def getXYZ(self,d):
        xx,yy,zz=self.draw_base(d)
        self.x,self.y,self.z=self.coordinate.transform(xx,yy,zz)
        self.x=self.x.reshape(-1,d)
        self.y=self.y.reshape(-1,d)
        self.z=self.z.reshape(-1,d)
        return self.x,self.y,self.z
    def draw2D(self,ax,text='',alpha=0.3,d=30):
        self.x,self.y,self.z=self.getXYZ(d)
        super().draw2D(ax,alpha)

class Sphere(SphereArc):
    def __init__(self):
        super().__init__()
        self.setTheta([0,2*np.pi])
        self.setPhi([0,np.pi])

class CylinderSurf(Shape2D):
    def __init__(self):
        super().__init__()
        self.r=1
        self.h=1
        self.theta=[0,2*np.pi]
    def setRadius(self,r):
        self.r=r
    def setHeight(self,h):
        self.h=h
    def setTheta(self,theta):
        self.theta=theta
    def setNLine(self,n,l1=[1,0,0]):
        n=np.array(n)
        l1=np.array(l1)
        if not np.inner(n,l1)==0:
            print("Not Normal... (setNLine), Use pre-assigned coordinates")
            l1=np.array([0,n[2],-n[1]])
        l2=np.cross(n,l1)
        self.coordinate.setCoordinates(l1,l2,n)
        self.coordinate.normalize()
    def draw_base(self,d):
        theta_ls=np.linspace(self.theta[0],self.theta[1],d)
        h_ls=np.linspace(0,self.h,d)
        ts,hs=np.meshgrid(theta_ls,h_ls)
        xx=self.r*np.cos(ts)
        yy=self.r*np.sin(ts)
        zz=hs
        xx=xx.reshape(-1,1)
        yy=yy.reshape(-1,1)
        zz=zz.reshape(-1,1)
        return xx,yy,zz
    def getXYZ(self,d):
        xx,yy,zz=self.draw_base(d)
        self.x,self.y,self.z=self.coordinate.transform(xx,yy,zz)
        self.x=self.x.reshape(-1,d)
        self.y=self.y.reshape(-1,d)
        self.z=self.z.reshape(-1,d)
        return self.x,self.y,self.z
    def draw2D(self,ax,text='',alpha=0.3,d=30):
        self.x,self.y,self.z=self.getXYZ(d)
        super().draw2D(ax,alpha)

class Cylinder(Shape2D):
    def __init__(self):
        super().__init__()
        self.r=[0,1]
        self.h=1
        self.theta=[0,2*np.pi]
        self.c1=ArcPlane()
        self.c2=ArcPlane()
        self.s_in=CylinderSurf()
        self.s_out=CylinderSurf()
    def setRadius(self,r):
        self.r=r
    def setHeight(self,h):
        self.h=h
    def setTheta(self,theta):
        self.theta=theta
    def getItems(self):
        self.coordinate.normalize()
        dx,dy,dz=self.coordinate.getCoordinates()

        self.c1.coordinate.setPoints(self.coordinate.p)
        self.c1.coordinate.setCoordinates(dx,dy,dz)
        self.c1.setRadius(self.r)
        self.c1.setTheta(self.theta)
        self.c1.setColor(self.color)

        self.c2.coordinate.setPoints(self.coordinate.p+self.h*(dz))
        self.c2.coordinate.setCoordinates(dx,dy,dz)
        self.c2.setRadius(self.r)
        self.c2.setTheta(self.theta)
        self.c2.setColor(self.color)

        self.s_in.coordinate.setPoints(self.coordinate.p)
        self.s_in.coordinate.setCoordinates(dx,dy,dz)
        self.s_in.setRadius(self.r[0])
        self.s_in.setTheta(self.theta)
        self.s_in.setHeight(self.h)
        self.s_in.setColor(self.color)

        self.s_out.coordinate.setPoints(self.coordinate.p)
        self.s_out.coordinate.setCoordinates(dx,dy,dz)
        self.s_out.setRadius(self.r[1])
        self.s_out.setTheta(self.theta)
        self.s_out.setHeight(self.h)
        self.s_out.setColor(self.color)

        return self.c1, self.c2, self.s_in, self.s_out

    def draw2D(self,ax,text='',alpha=0.3,d=30):
        self.c1, self.c2, self.s_in, self.s_out = self.getItems()
        self.c1.draw2D(ax,text,alpha,d)
        self.c2.draw2D(ax,text,alpha,d)
        self.s_in.draw2D(ax,text,alpha,d)
        self.s_out.draw2D(ax,text,alpha,d)