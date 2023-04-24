# Py_drawing_tools
Basic Drawing Tools for matplotlib in python

## Shapes.py
2차원 직선과 호, 원을 그려주는 Tool입니다.

### Class Shape()
기본적인 X,Y에 대한 정보와 linestyle, color를 가지고 있습니다.
    
pyplot을 이용할 때처럼, setLineStyle이나 setColor의 변수에 plt.plot(...,color='color',linestyle='linestyle')에 들어가는 Color, Linestyle을 써주면 됩니다.

주어진 x,y를 그릴 때에는 draw()를 이용하여 그리면 됩니다.

-아래의 모든 Class는 Shape를 상속받으므로, 
Line, Arc, Circle 모두 draw를 이용해서 그리면 되고, Color와 Linestyle도 동일하게 설정합니다.
(text -> text 넣고 싶을 때, text_loc -> text 위치 , alpha -> 투명도(0-1))


#### Class Line()
2차원 직선의 정보를 가지고 있습니다.

1. setPoints()를 이용해서, 두 점의 정보를 넣어주면 됩니다.

#### Class Coordinate()
직교 좌표계의 정보(x축, y축)의 정보를 가지고 있습니다.

두 개의 직선(x축, y축)으로 이루어져 있습니다.

1. x축: [0,0],[1,0]
2. y축: [0,0],[0,1]

setPoints()로 평행이동을 할 수 있습니다.

#### Class Arc()
호의 정보를 가지고 있습니다.

1. setPoints()로 중심이 되는 점을 설정하고
2. setRadius()로 반지름 설정,
3. setThetas()로 원하는 각도를 설정하면 됩니다.

그 외의 것들은 위의 Shape, Line과 동일합니다.

#### Class Circle()
원의 정보를 가지고 있습니다.

이 클래스는 Arc에 Theta가 [0,2pi]로 기본 설정이 되어있습니다.

========================================================================================

## Shapes3d.py
3차원에서의 직선, 평면, 구 등을 그려줍니다.

### Class Shape()
3차원 공간에 그려지는 1차원 도형입니다.
2차원과 동일하지만 z가 추가됩니다.

#### Class Line()
2차원과 동일합니다.

#### Class Coordinate()
2차원과 동일합니다. 그러나, 여기에선 회전변환의 기능도 가지고 있습니다.

setCoordinates(dx,dy,dz)로 원하는 좌표계를 넣어줄 수 있습니다.

다만, 직교좌표계가 아닌 경우, 뒤에 3차원 도형들이 이 Coordinate를 이용해서 회전하기 때문에 강제로 직교좌표계로 변환이 될 수 있습니다.

### Class Shape2D()
3차원 공간에 그려지는 2차원 도형입니다.
2차원 도형이므로, 그려지는 평면을 Coordinate를 이용해서 넣을 수 있습니다. 또한, 회전변환도 가능합니다.


1. setLines(l1,l2)
    2개의 직선을 받고, 하나의 직선은 외적을 이용해(l1 x l2) 좌표계를 만듭니다.
    이 때, l1,l2는 직교일 필요는 없습니다.
2. setPoints(p0),setOtherPoints(p1,p2)
    p0를 고정한 후, p0에서 p1, p0에서 p2로 이어지는 각 직선을 setLines()를 통해서 좌표계를 만듭니다.
3. setNLine(n,l1)
    하나의 직선방향(l1)과 법선벡터(n)을 이용해서 좌표계를 만듭니다.
    이 때, l1과 n이 직교가 아니면 에러가 발생합니다.
    
그리고, 아래에 나오는 Class들은 모두 Shape2D()를 상속받는데, 그릴 때에는 draw()가 아니라 draw2D()를 이용합니다.

draw2D에서는 plt.plot_wireframe을 이용합니다.

#### Class Plane()
3차원 공간에 그려지는 2차원 평면입니다.

Shape2D를 이용해서 그려질 평면을 정하면 됩니다.

#### Class ArcPlane()
3차원 공간에 그려지는 2차원 부채꼴입니다.

Shape2D를 이용해서 그려질 평면을 정하면 됩니다.

이 때 setRadius는 [a,b]를 받는데, 반지름이 a부터 b까지 부채꼴로 그려집니다.

#### Class CirclePlane()
3차원 공간에 그려지는 2차원 원입니다. ArcPlane()을 상속받습니다.

Shape2D를 이용해서 그려질 평면을 정하면 됩니다.

#### Class SphereArc()
3차원 공간에 그려지는 2차원 구면조각입니다.

구면좌표계를 이용해서 반지름, Theta, Phi를 생각하면 되고, 각각 setRadius(), setTheta(), setPhi()를 통해 설정할 수 있습니다. 이 때, setRadius는 그냥 반지름 r만 받습니다.

#### Class Sphere()
3차원 공간에 그려지는 2차원 구면입니다.

SphereArc()를 상속받고, Theta=[0,2pi], Phi=[0,pi]로 기본 설정되어있습니다.

#### Class CylinderSurf()
3차원 공간에 그려지는 2차원 실린더 **옆면**입니다.

Coordinate로 좌표계를 설정하고, setHeight로 높이를 설정할 수 있습니다. 기준점은 밑면(원) 중심입니다. 이 때, setRadius는 그냥 반지름 r만 받습니다.

#### Class Cylinder()
3차원 공간에 그려지는 2차원 실린더 입니다.

CirclePlane() 두개와 CylinderSurf() 두개로 이루어져 있습니다.

CirclePlane()은 각각 윗면과 아랫면, CylinderSurf()는 실린더 옆면의 바깥쪽과 안쪽입니다.

(이 때 setRadius는 [a,b]를 받는데, 반지름이 0~a인 부분이 뚫리게 됩니다.)
