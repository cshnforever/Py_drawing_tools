import numpy as np

class Shape:
    def __init__(self):
        self.color='black'
        self.linestyle='-'
        self.x=[]
        self.y=[]
        return
    def setX(self,x):
        self.x=x
    def setY(self,y):
        self.y=y
    def setColor(self,color):
        self.color=color
    def setLineStyle(self,linestyle):
        self.linestyle=linestyle
    def draw(self,ax,text='',text_loc=-1,alpha=1):
        ax.plot(self.x,self.y,color=self.color,linestyle=self.linestyle,alpha=alpha)
        ax.text(self.x[text_loc],self.y[text_loc],text)
    
class Line(Shape):
    def __init__(self):
        super().__init__()
        self.p1=[0,0]
        self.p2=[0,0]
    def setPoints(self,p1,p2):
        self.p1=p1
        self.p2=p2
    def setX(self,d):
        self.x=np.linspace(self.p1[0],self.p2[0],d)
    def setY(self,d):
        self.y=np.linspace(self.p1[1],self.p2[1],d)
    def setXY(self,d):
        self.setX(d)
        self.setY(d)
    def draw(self,ax,text='',text_loc=-1,alpha=1,d=20):
        self.setXY(d)
        super().draw(ax,text,text_loc,alpha)

class Coordinate(Shape):
    def __init__(self):
        super().__init__()
        self.l1=Line()
        self.l2=Line()
        self.l1.setPoints([0,0],[1,0])
        self.l2.setPoints([0,0],[0,1])
    def setPoints(self,p1):
        np_p1=np.array(p1)
        self.l1.setPoints(np_p1,np_p1+[1,0])
        self.l2.setPoints(np_p1,np_p1+[0,1])
    def draw(self,ax,text='',text_loc=-1,alpha=0.6,d=20):
        self.l1.setColor(self.color)
        self.l2.setColor(self.color)
        self.l1.setLineStyle(self.linestyle)
        self.l2.setLineStyle(self.linestyle)
        self.l1.draw(ax,text,text_loc,alpha,d)
        self.l2.draw(ax,text,text_loc,alpha,d)

class Arc(Shape):
    def __init__(self):
        super().__init__()
        self.p=[0,0]
        self.r=1
        self.theta=[0,0]
    def setPoints(self,p):
        self.p=p
    def setRadius(self,r):
        self.r=r
    def setTheta(self,theta):
        self.theta=theta
    def setX(self,d):
        self.x=self.r*np.cos(np.linspace(self.theta[0],self.theta[1],d))
    def setY(self,d):
        self.y=self.r*np.sin(np.linspace(self.theta[0],self.theta[1],d))
    def setXY(self,d):
        self.setX(d)
        self.setY(d)
    def draw(self,ax,text='',text_loc=-1,alpha=1,d=20):
        self.setXY(d)
        super().draw(ax,text,text_loc,alpha)

class Circle(Arc):
    def __init__(self):
        super().__init__()
        self.setTheta([0,2*np.pi])