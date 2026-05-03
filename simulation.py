import turtle
import math

# -----------------------------
# Screen setup
# -----------------------------
screen = turtle.Screen()
screen.setup(1000, 700)
screen.bgcolor((0.70, 1.0, 0.70))
screen.title("City Traffic Simulation - Turtle")
screen.tracer(0)

screen.setworldcoordinates(-100, -100, 100, 70) #--- check

# -----------------------------
# Global state
# -----------------------------
signalState = 0
directionControl = 0

c1x, c1y = -120, -8
c1xx, c1yy = -140, -8
c1xxx, c1yyy = -160, -8
c1xxxx, c1yyyy = -180, -8
c1xxxxx, c1yyyyy = -200, -8

c2x, c2y = 120, -33
c2xx, c2yy = 160, -33

h1y = -48
hDirection = 0

timer_count = 0
LEFT_EXT = -106

# -----------------------------
# Speed controls
# -----------------------------
MANUAL_STEP = 8
TRAFFIC_STEP = 1
PEDESTRIAN_STEP = 1
TIMER_DELAY = 0

# -----------------------------
# Manual vertical car state
# -----------------------------
VERT_LEFT_X = -12
VERT_RIGHT_X = 12

manual_x = VERT_RIGHT_X
manual_y = 50
manual_lane = "right"
manual_route = "down"

CAR_HALF_W = 6
CAR_HALF_H = 6

SCREEN_MIN_X = -100
SCREEN_MAX_X = 100
SCREEN_MIN_Y = -100
SCREEN_MAX_Y = 70

VERT_ROAD_MIN_X = -20
VERT_ROAD_MAX_X = 20

TOP_STOP_Y = 16
BOTTOM_STOP_Y = -58
CENTER_Y = -20

# -----------------------------
# Drawing turtle
# -----------------------------
pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)
pen.penup()

# -----------------------------
# Helpers
# -----------------------------
def goto(x, y):
    pen.penup()
    pen.goto(x, y)

def setc(r, g, b):
    pen.pencolor(r, g, b)
    pen.fillcolor(r, g, b)

def filled_rect(x1, y1, x2, y2, color):
    setc(*color)
    pen.penup()
    pen.goto(x1, y1)
    pen.setheading(0)
    pen.begin_fill()
    pen.pendown()
    pen.goto(x2, y1)
    pen.goto(x2, y2)
    pen.goto(x1, y2)
    pen.goto(x1, y1)
    pen.end_fill()
    pen.penup()

def line(x1, y1, x2, y2, color=(0, 0, 0), width=1):
    pen.pensize(width)
    pen.pencolor(color)
    pen.penup()
    pen.goto(x1, y1)
    pen.pendown()
    pen.goto(x2, y2)
    pen.penup()
    pen.pensize(1)

def draw_circle(cx, cy, r, color, steps=40):
    setc(*color)
    pen.penup()
    pen.goto(cx, cy - r)
    pen.setheading(0)
    pen.begin_fill()
    pen.pendown()
    pen.circle(r, steps=steps)
    pen.end_fill()
    pen.penup()

def draw_ellipse(cx, cy, rx, ry, color, steps=60):
    setc(*color)
    pen.penup()
    pen.goto(cx + rx, cy)
    pen.begin_fill()
    first = True
    for i in range(steps + 1):
        ang = 2 * math.pi * i / steps
        x = cx + rx * math.cos(ang)
        y = cy + ry * math.sin(ang)
        if first:
            pen.goto(x, y)
            pen.pendown()
            first = False
        else:
            pen.goto(x, y)
    pen.end_fill()
    pen.penup()

def draw_polygon(points, color):
    setc(*color)
    pen.penup()
    pen.goto(points[0][0], points[0][1])
    pen.begin_fill()
    pen.pendown()
    for x, y in points[1:]:
        pen.goto(x, y)
    pen.goto(points[0][0], points[0][1])
    pen.end_fill()
    pen.penup()

def dda_dashed(x1, y1, x2, y2, dash=10, gap=10, color=(1, 1, 1), width=2):
    dx = x2 - x1
    dy = y2 - y1

    if dx != 0:
        m = dy / dx
    else:
        m = float('inf')

    x = x1
    y = y1
    cycle = dash + gap

    pen.pensize(width)
    pen.pencolor(color)
    pen.penup()

    if abs(m) < 1:
        steps = abs(dx)
        step_x = 1 if dx > 0 else -1

        for i in range(steps + 1):
            if (i % cycle) < dash:
                if not pen.isdown():
                    pen.goto(round(x), round(y))
                    pen.pendown()
                else:
                    pen.goto(round(x), round(y))
            else:
                if pen.isdown():
                    pen.penup()
                pen.goto(round(x), round(y))

            x = x + step_x
            y = y + m * step_x

    elif abs(m) == 1:
        steps = abs(dx)
        step_x = 1 if dx > 0 else -1
        step_y = 1 if dy > 0 else -1

        for i in range(steps + 1):
            if (i % cycle) < dash:
                if not pen.isdown():
                    pen.goto(round(x), round(y))
                    pen.pendown()
                else:
                    pen.goto(round(x), round(y))
            else:
                if pen.isdown():
                    pen.penup()
                pen.goto(round(x), round(y))

            x = x + step_x
            y = y + step_y

    else:
        steps = abs(dy)
        step_y = 1 if dy > 0 else -1

        for i in range(steps + 1):
            if (i % cycle) < dash:
                if not pen.isdown():
                    pen.goto(round(x), round(y))
                    pen.pendown()
                else:
                    pen.goto(round(x), round(y))
            else:
                if pen.isdown():
                    pen.penup()
                pen.goto(round(x), round(y))

            if dx == 0:
                y = y + step_y
            else:
                x = x + (step_y / m)
                y = y + step_y

    pen.penup()
    pen.pensize(1)

def draw_multi_line(x1, y1, x2, y2, n, gap, color=(0, 0, 0), width=1):
    for i in range(n):
        if y1 == y2:
            yy = y1 - i * gap
            line(x1, yy, x2, yy, color, width)
        elif x1 == x2:
            xx = x1 + i * (gap - 1)
            line(xx, y1, xx, y2, color, width)

def rotate_point(x, y, angle_deg):
    ang = math.radians(angle_deg)
    xr = x * math.cos(ang) - y * math.sin(ang)
    yr = x * math.sin(ang) + y * math.cos(ang)
    return xr, yr

def transform_points(points, tx=0, ty=0, angle=0):
    out = []
    for x, y in points:
        xr, yr = rotate_point(x, y, angle)
        out.append((xr + tx, yr + ty))
    return out

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def vertical_green():
    return directionControl == 1 and signalState == 0

def sync_route_with_lane():
    global manual_route
    manual_route = "up" if manual_lane == "left" else "down"

def manual_angle():
    sync_route_with_lane()
    return 90 if manual_route == "up" else -90

def approaching_from_top():
    return manual_y >= CENTER_Y

def enforce_manual_bounds():
    global manual_x, manual_y
    manual_x = clamp(manual_x, VERT_ROAD_MIN_X + CAR_HALF_W, VERT_ROAD_MAX_X - CAR_HALF_W)
    manual_y = clamp(manual_y, SCREEN_MIN_Y + CAR_HALF_H, SCREEN_MAX_Y - CAR_HALF_H)

def set_lane_left():
    global manual_x, manual_lane
    manual_lane = "left"
    manual_x = VERT_LEFT_X
    sync_route_with_lane()
    enforce_manual_bounds()

def set_lane_right():
    global manual_x, manual_lane
    manual_lane = "right"
    manual_x = VERT_RIGHT_X
    sync_route_with_lane()
    enforce_manual_bounds()

def enforce_signal_barrier():
    global manual_y

    if vertical_green():
        return

    if approaching_from_top():
        manual_y = max(manual_y, TOP_STOP_Y)
    else:
        manual_y = min(manual_y, BOTTOM_STOP_Y)

# -----------------------------
# Manual car controls
# -----------------------------
def move_up():
    global manual_y
    sync_route_with_lane()

    if manual_route != "up":
        return

    next_y = manual_y + MANUAL_STEP

    if not vertical_green():
        if approaching_from_top():
            next_y = max(next_y, TOP_STOP_Y)
        else:
            next_y = min(next_y, BOTTOM_STOP_Y)

    manual_y = next_y
    enforce_manual_bounds()
    enforce_signal_barrier()
    redraw()

def move_down():
    global manual_y
    sync_route_with_lane()

    if manual_route != "down":
        return

    next_y = manual_y - MANUAL_STEP

    if not vertical_green():
        if approaching_from_top():
            next_y = max(next_y, TOP_STOP_Y)
        else:
            next_y = min(next_y, BOTTOM_STOP_Y)

    manual_y = next_y
    enforce_manual_bounds()
    enforce_signal_barrier()
    redraw()

def move_left_lane():
    if manual_lane == "left":
        return
    set_lane_left()
    enforce_signal_barrier()
    redraw()

def move_right_lane():
    if manual_lane == "right":
        return
    set_lane_right()
    enforce_signal_barrier()
    redraw()

# -----------------------------
# Scene objects
# -----------------------------
def circle_shape(rx, ry, cx, cy, color):
    if abs(rx - ry) < 0.001:
        draw_circle(cx, cy, rx, color)
    else:
        draw_ellipse(cx, cy, rx, ry, color)

def car(tx, ty, angle, r, g, b):
    body = [(-6, -3), (6, -3), (6, 3), (-6, 3)]
    top = [(-3, 3), (3, 3), (2, 6), (-2, 6)]

    draw_polygon(transform_points(body, tx, ty, angle), (r, g, b))
    draw_polygon(transform_points(top, tx, ty, angle), (r, g, b))

    for wx, wy in [(-3, -3), (3, -3)]:
        xr, yr = rotate_point(wx, wy, angle)
        circle_shape(2, 2, tx + xr, ty + yr, (0, 0, 0))
        circle_shape(1, 1, tx + xr, ty + yr, (0.7, 0.7, 0.7))

def tree(x, y, r):
    filled_rect(x - 1, y - 5, x + 1, y + 5, (0.5, 0.3, 0.1))
    circle_shape(r, r - 0.5, x, y + 5, (0.0, 0.75, 0.0))

def human(tx, ty, r, g, b):
    circle_shape(1.2, 1.0, tx + 0, ty + 3, (1, 0.8, 0.6))
    filled_rect(tx - 2.2, ty + 0, tx - 1.5, ty + 2, (1, 0.8, 0.6))
    filled_rect(tx + 1.5, ty + 0, tx + 2.2, ty + 2, (1, 0.8, 0.6))
    filled_rect(tx - 1.5, ty - 1, tx + 1.5, ty + 2.5, (r, g, b))
    filled_rect(tx - 1.5, ty - 4, tx - 0.2, ty - 1, (0.1, 0.1, 0.1))
    filled_rect(tx + 0.2, ty - 4, tx + 1.5, ty - 1, (0.1, 0.1, 0.1))
    filled_rect(tx - 1.6, ty - 4.5, tx - 0.1, ty - 4, (1, 1, 1))
    filled_rect(tx + 0.1, ty - 4.5, tx + 1.6, ty - 4, (1, 1, 1))

def traffic_box(tx, ty, angle, active):
    pole = [(0, 0), (2, 0), (2, 12), (0, 12)]
    box = [(-3, 12), (5, 12), (5, 28), (-3, 28)]
    stand = [(-1, -2), (3, -2), (3, 1), (-1, 1)]

    draw_polygon(transform_points(pole, tx, ty, angle), (0.3, 0.3, 0.3))
    draw_polygon(transform_points(box, tx, ty, angle), (0.1, 0.1, 0.1))
    draw_polygon(transform_points(stand, tx, ty, angle), (0.3, 0.3, 0.3))

    if active:
        red = (1, 0, 0) if signalState == 2 else (0.3, 0, 0)
        yellow = (1, 1, 0.2) if signalState == 1 else (0.3, 0.3, 0)
        green = (0, 1, 0) if signalState == 0 else (0, 0.3, 0)
    else:
        red = (1, 0, 0)
        yellow = (0.3, 0.3, 0)
        green = (0, 0.3, 0)

    for cx, cy, col in [(1, 25, red), (1, 20, yellow), (1, 15, green)]:
        xr, yr = rotate_point(cx, cy, angle)
        circle_shape(2, 2, tx + xr, ty + yr, col)

def draw_park_area():
    filled_rect(-100, -100, -30, -50, (0.72, 0.96, 0.72))

    line(-99, -99, -31, -99, (0.35, 0.6, 0.35), 2)
    line(-99, -51, -31, -51, (0.35, 0.6, 0.35), 2)
    line(-99, -99, -99, -51, (0.35, 0.6, 0.35), 2)
    line(-31, -99, -31, -51, (0.35, 0.6, 0.35), 2)

    back_row = [
        (-84, -60, 4.2), (-72, -60, 4.0), (-48, -60, 4.1), (-36, -60, 4.0)
    ]
    for x, y, r in back_row:
        tree(x, y, r)

    filled_rect(-67, -96, -63, -54, (0.85, 0.82, 0.72))
    filled_rect(-95, -77, -35, -73, (0.85, 0.82, 0.72))

    draw_circle(-65, -75, 4, (0.80, 0.88, 0.80))
    draw_circle(-65, -75, 2.2, (0.3, 0.65, 0.3))

    front_row = [
        (-88, -88, 4.4), (-78, -88, 3.7), (-68, -88, 4.2), (-58, -88, 3.6), (-48, -88, 4.0), (-38, -88, 3.8),
        (-88, -68, 4.6), (-76, -66, 5.0), (-54, -66, 4.9), (-42, -67, 4.4)
    ]
    for x, y, r in front_row:
        tree(x, y, r)

# -----------------------------
# Static scene
# -----------------------------
def draw_static_scene():
    pen.clear()

    # -----------------------------
    # Roads
    # -----------------------------
    filled_rect(LEFT_EXT, -50, 100, 10, (0.15, 0.15, 0.15))   
    filled_rect(-20, -100, 20, 100, (0.15, 0.15, 0.15))       

    # -----------------------------
    # Road edge / lane border lines (white)
    # -----------------------------
    white = (1, 1, 1)
    filled_rect(LEFT_EXT, 0, -20, 1, white)       
    filled_rect(20, 0, 100, 1, white)            
    filled_rect(LEFT_EXT, -41, -20, -40, white)   
    filled_rect(20, -41, 100, -40, white)         

    filled_rect(-21, 1, -20, 100, white)          
    filled_rect(-21, -100, -20, -40, white)       
    filled_rect(20, 1, 21, 100, white)            
    filled_rect(20, -100, 21, -40, white)         

    # -----------------------------
    # Footpaths / sidewalks (gray)
    # -----------------------------
    gray = (0.7, 0.7, 0.7)
    filled_rect(LEFT_EXT, 1, -21, 10, gray)        
    filled_rect(21, 1, 100, 10, gray)
    
    filled_rect(LEFT_EXT, -50, -21, -41, gray) 
    filled_rect(21, -50, 100, -41, gray)          

    filled_rect(-30, 1, -21, 100, gray)
    filled_rect(-30, -100, -21, -41, gray) 
      
    filled_rect(21, 1, 30, 100, gray)
    filled_rect(21, -100, 30, -41, gray)
    
             

    # -----------------------------
    # Sidewalk boundary / tile lines (black outlines)
    # -----------------------------
    black = (0, 0, 0)
    line(LEFT_EXT, 1, -21, 1, black)          
    line(LEFT_EXT, 10, -21, 10, black)            
    line(-30, 100, -30, 1, black)                 

    line(-21, 100, -21, 1, black)                 
    line(LEFT_EXT, -50, -21, -50, black)          
    line(LEFT_EXT, -41, -21, -41, black)          
    line(-30, -100, -30, -41, black)              
    line(-21, -100, -21, -41, black)              

    line(21, 1, 100, 1, black)                    
    line(21, 10, 100, 10, black)                  
    line(30, 100, 30, 1, black)                  
    line(21, 100, 21, 1, black)                   

    line(21, -41, 21, -100, black)                
    line(30, -41, 30, -100, black)                
    line(21, -41, 100, -41, black)                
    line(30, -50, 100, -50, black)                

    # -----------------------------
    # Sidewalk tile divider lines
    # -----------------------------
    draw_multi_line(LEFT_EXT, 1, LEFT_EXT, 10, 8, 10, black)      
    draw_multi_line(LEFT_EXT, -50, LEFT_EXT, -41, 8, 10, black)   
    draw_multi_line(21, 1, 21, 10, 10, 10, black)                 
    draw_multi_line(21, -50, 21, -41, 10, 10, black)              

    draw_multi_line(-30, 100, -21, 100, 10, 10, black)            
    draw_multi_line(-30, -50, -21, -50, 8, 10, black)             
    draw_multi_line(21, 100, 30, 100, 10, 10, black)              
    draw_multi_line(21, -41, 30, -41, 10, 10, black)              

    # -----------------------------
    # Road center dashed lane markings
    # -----------------------------
    dda_dashed(LEFT_EXT, -20, 100, -20, 10, 10, white, 2)         
    dda_dashed(0, -100, 0, 70, 10, 10, white, 2)                  

    # -----------------------------
    # Zebra crossing - left side of intersection
    # -----------------------------
    line(-31, -2, -31, -38, white, 3)                             
    draw_multi_line(-28, -4, -22, -4, 12, 3, white, 3)           

    # -----------------------------
    # Zebra crossing - right side of intersection
    # -----------------------------
    line(31, -2, 31, -38, white, 3)                               
    draw_multi_line(28, -4, 22, -4, 12, 3, white, 3)             

    # -----------------------------
    # Zebra crossing - top side of intersection
    # -----------------------------
    line(-18, 12, 18, 12, white, 3)                               
    draw_multi_line(-17, 9, -17, 1, 18, 3, white, 3)             

    # -----------------------------
    # Zebra crossing - bottom side of intersection
    # -----------------------------
    line(-18, -52, 18, -52, white, 3)                             
    draw_multi_line(-17, -41, -17, -49, 18, 3, white, 3)         

    # -----------------------------
    # Center round marking of intersection
    # -----------------------------
    draw_circle(0, -20, 4, white)                                 

    # -----------------------------
    # Top-left trees
    # -----------------------------
    tree(-96, 27, 4)                                              
    tree(-94, 15, 6)                                              

    # -----------------------------
    # Top-left building (blue)
    # -----------------------------
    filled_rect(-90, 10, -60, 50, (0, 0.75, 1))                   
    for x1, y1, x2, y2 in [
        (-88, 48, -82, 40), (-78, 48, -72, 40), (-68, 48, -62, 40),
        (-88, 38, -82, 30), (-78, 38, -72, 30), (-68, 38, -62, 30),
        (-88, 28, -82, 20), (-68, 28, -62, 20), (-80, 28, -70, 10)
    ]:
        filled_rect(x1, y2, x2, y1, white)                      

    tree(-62, 15, 6)                                             
    draw_ellipse(-88, 13, 4, 3, (0.0, 0.7, 0.0))                  

    # -----------------------------
    # Top-right trees and bushes
    # -----------------------------
    tree(57, 24, 5)                                               
    draw_ellipse(59, 15, 6, 5, (0.0, 0.7, 0.0))                   
    tree(93, 24, 6)                                              
    draw_ellipse(98, 15, 4, 3, (0.0, 0.7, 0.0))                   

    # -----------------------------
    # Top-right building (orange)
    # -----------------------------
    filled_rect(60, 10, 90, 50, (1, 0.65, 0))                     
    for x1, y1, x2, y2 in [
        (62, 48, 68, 40), (72, 48, 78, 40), (82, 48, 88, 40),
        (62, 38, 68, 30), (72, 38, 78, 30), (82, 38, 88, 30),
        (62, 28, 68, 20), (82, 28, 88, 20), (70, 28, 80, 10)
    ]:
        filled_rect(x1, y2, x2, y1, white)                        

    draw_ellipse(59, 15, 6, 5, (0.0, 0.7, 0.0))                   
    draw_ellipse(90, 15, 6, 5, (0.0, 0.7, 0.0))                   

    # -----------------------------
    # Bottom-left park area
    # -----------------------------
    draw_park_area()                                              

    # -----------------------------
    # Bottom-right helipad / circular landing area
    # -----------------------------
    draw_circle(65, -75, 21, (0.5, 0.5, 0.5))                     

    pen.pensize(2)
    pen.pencolor(1, 1, 1)
    pen.penup()
    pen.goto(65, -95)
    pen.pendown()
    pen.circle(20)                                                 
    pen.penup()

    line(53, -80, 77, -80, (1, 1, 0), 4)                          
    line(53, -70, 77, -70, (1, 1, 0), 4)                          
    line(65, -70, 65, -80, (1, 1, 0), 4)                         

    # -----------------------------
    # Trees around helipad
    # -----------------------------
    tree(36, -92, 5)                                               
    tree(94, -92, 5)                                               
    tree(36, -62, 5)                                               
    tree(94, -62, 5)                                               

def draw_dynamic_scene():
    car(c1x, c1y, 0, 1, 0, 0)
    car(c1xx, c1yy, 0, 0, 0.5, 1)
    car(c1xxx, c1yyy, 0, 0, 0.6, 0.2)
    car(c1xxxx, c1yyyy, 0, 1, 0.8, 0)
    car(c1xxxxx, c1yyyyy, 0, 0.5, 0, 0.5)

    car(c2x, c2y, 0, 1, 0.4, 0)
    car(c2xx, c2yy, 0, 0, 1, 0)

    car(manual_x, manual_y, manual_angle(), 0.1, 0.2, 1.0)

    traffic_box(-58, 6, -90, directionControl == 0)
    traffic_box(58, -46, 90, directionControl == 0)
    traffic_box(-26, -78, 0, directionControl == 1)
    traffic_box(26, 38, 180, directionControl == 1)

    if h1y <= -44:
        human(-26, -45, 0.2, 0.5, 1)
    else:
        human(-26, h1y, 0.2, 0.5, 1)

def redraw():
    enforce_signal_barrier()
    draw_static_scene()
    draw_dynamic_scene()
    screen.update()

# -----------------------------
# Animation update
# -----------------------------
def update():
    global timer_count, signalState, directionControl
    global c1x, c1xx, c1xxx, c1xxxx, c1xxxxx
    global c2x, c2xx
    global h1y, hDirection

    # ---------------------------------
    # 1. Increase time for current signal
    # ---------------------------------
    timer_count += 1

    # ---------------------------------
    # 2. Change signal state when time ends
    # directionControl
    # ---------------------------------
    if signalState == 0:  
        if timer_count > 120:
            signalState = 1   # green -> yellow
            timer_count = 0

    elif signalState == 1:  
        if timer_count > 30:
            signalState = 2   # yellow -> red
            timer_count = 0

    elif signalState == 2:  
        if timer_count > 90:
            signalState = 0   # red -> green
            directionControl = 1 - directionControl   # switch road turn
            timer_count = 0

    # ---------------------------------
    # 3. Move left-to-right cars
    # Rule:
    # - move if horizontal road is green
    # - OR move if car already crossed stop line
    # ---------------------------------
    if (directionControl == 0 and signalState == 0) or (c1x > -38):
        c1x += TRAFFIC_STEP
    if c1x > 120:
        c1x = -120

    if (directionControl == 0 and signalState == 0) or (c1xx > -38):
        c1xx += TRAFFIC_STEP
    if c1xx > 120:
        c1xx = -140

    if (directionControl == 0 and signalState == 0) or (c1xxx > -38):
        c1xxx += TRAFFIC_STEP
    if c1xxx > 120:
        c1xxx = -160

    if (directionControl == 0 and signalState == 0) or (c1xxxx > -38):
        c1xxxx += TRAFFIC_STEP
    if c1xxxx > 120:
        c1xxxx = -180

    if (directionControl == 0 and signalState == 0) or (c1xxxxx > -38):
        c1xxxxx += TRAFFIC_STEP
    if c1xxxxx > 120:
        c1xxxxx = -200

    # ---------------------------------
    # 4. Move right-to-left cars
    # Rule:
    # - move if horizontal road is green
    # - OR move if car already crossed stop line
    # ---------------------------------
    if (directionControl == 0 and signalState == 0) or (c2x < 38):
        c2x -= TRAFFIC_STEP
    if c2x < -120:
        c2x = 120

    if (directionControl == 0 and signalState == 0) or (c2xx < 38):
        c2xx -= TRAFFIC_STEP
    if c2xx < -120:
        c2xx = 160

    # ---------------------------------
    # 5. Move pedestrian only when
    # horizontal road is red
    # ---------------------------------
    if signalState == 2 and directionControl == 0:
        if hDirection == 0:   # move upward
            if h1y < 6.0:
                h1y += PEDESTRIAN_STEP
            else:
                h1y = 6.0

        elif hDirection == 1:  # move downward
            if h1y > -48.0:
                h1y -= PEDESTRIAN_STEP
            else:
                h1y = -48.0

    # ---------------------------------
    # 6. Change pedestrian direction
    # when it reaches top or bottom
    # ---------------------------------
    if signalState == 0:
        if h1y >= 6.0:
            hDirection = 1   # next time go down
        if h1y <= -48.0:
            hDirection = 0   # next time go up

    # ---------------------------------
    # 7. Apply signal barrier to manual car,
    # redraw screen, and call update again
    # ---------------------------------
    enforce_signal_barrier() 
    redraw()
    screen.ontimer(update, TIMER_DELAY)

# -----------------------------
# Key bindings
# -----------------------------
screen.listen()
screen.onkeypress(move_up, "Up")
screen.onkeypress(move_down, "Down")
screen.onkeypress(move_left_lane, "Left")
screen.onkeypress(move_right_lane, "Right")

# -----------------------------
# Start
# -----------------------------
set_lane_right()
redraw()
update()
screen.mainloop()
