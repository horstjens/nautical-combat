import turtle

def zweig(laenge = 10, winkel=30, divisor=2):
	if laenge < 2:
		return
	turtle.forward(laenge)
	turtle.left(winkel)
	zweig(laenge//divisor, winkel, divisor)
	turtle.right(winkel*2)
	zweig(laenge//divisor, winkel, divisor)
	turtle.left(winkel)
	turtle.penup()
	turtle.forward(-laenge)
	turtle.pendown()
	
turtle.goto(-400,0)
turtle.clear()
zweig(150, 90, 1.5)
turtle.exitonclick()
