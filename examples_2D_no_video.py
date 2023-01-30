import numpy as np
import matplotlib.pyplot as plt
import shapes

fig,ax = plt.subplots(figsize=(5,5))

x_lim=[-2,2]
y_lim=[-2,2]

any_shape=shapes.Shape()
line=shapes.Line()
co_xy=shapes.Coordinate()
arc=shapes.Arc()
circle=shapes.Circle()

theta=np.linspace(0,2*np.pi,20)
r=1+np.sin(theta)

x=np.sqrt(r)*np.cos(theta)
y=np.sqrt(r)*np.sin(theta)
any_shape.setX(x)
any_shape.setY(y)
any_shape.setColor('blue')
any_shape.setLineStyle('-.')
any_shape.draw(ax,'Any Shape')

line.setPoints([0,0],[1,1])
line.setColor('red')
line.setLineStyle('--')
line.draw(ax,'line')

co_xy.setPoints([1,1])
co_xy.setColor('green')
co_xy.draw(ax)

d=10
arc.setPoints([0,0])
arc.setRadius(1)
arc.setTheta([np.pi/2,3*np.pi/2])
arc.setColor('black')
arc.draw(ax,'arc',d=d,text_loc=d//2)

circle.setPoints([0,-1])
circle.setRadius(0.5)
circle.setLineStyle(':')
circle.draw(ax,'circle',d=30,alpha=0.7)

plt.show()