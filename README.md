# Traffic System Using Turtle

A Python Turtle Graphics project that simulates a small city traffic intersection with animated cars, traffic lights, a pedestrian, and a manually controlled vehicle. The scene is fully drawn with the standard `turtle` library, so no third-party packages are required.

## Overview

The simulation renders a compact city block with:

- a horizontal and vertical road crossing
- traffic signals that cycle through green, yellow, and red states
- moving vehicles on both horizontal lanes
- a pedestrian that crosses only when the signal allows it
- a player-controlled car that moves vertically through the intersection area
- decorative city elements such as buildings, trees, sidewalks, and a helipad

The animation runs continuously and updates the traffic logic, vehicle positions, and pedestrian movement in real time.

## Features

- Animated road traffic with multiple vehicles on each side of the intersection
- Signal timing logic that changes the road priority over time
- Pedestrian movement tied to the horizontal road signal state
- Keyboard controls for the manual car
- Custom scene drawing using helper functions for shapes, polygons, dashed lines, and filled areas
- No external dependencies beyond Python's built-in Turtle Graphics module

## Controls

Use the arrow keys while the simulation window is active:

- Up Arrow: move the manual car upward
- Down Arrow: move the manual car downward
- Left Arrow: switch the manual car to the left lane
- Right Arrow: switch the manual car to the right lane

The manual car is constrained to the vertical road and will respect the traffic signal barrier.

## Requirements

- Python 3.x
- A desktop environment that supports Turtle Graphics windows

## How to Run

From the project folder, run:

```bash
python simulation.py
```

If your system uses `python3`, you can run:

```bash
python3 simulation.py
```

## How It Works

The program uses a timed update loop to control the simulation:

- traffic signals cycle through green, yellow, and red states
- horizontal vehicles move when allowed by the signal logic
- the pedestrian moves only during the correct signal phase
- the manual car is blocked from crossing the stop line when the vertical road is not green
- the entire scene is redrawn on each update

## Project Structure

- `simulation.py`: main simulation script containing the drawing, animation, and input logic

## Notes

- The project uses `screen.tracer(0)` and manual redraws for smooth animation.
- The scene is drawn entirely with helper functions, which makes it easy to extend with new objects or new road layouts.
- Some values such as signal timings, road boundaries, and vehicle speeds are defined near the top of the script and can be tuned if you want to adjust the simulation behavior.
