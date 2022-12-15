import math
import glm

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

CELL_WIDTH = 222
CELL_HEIGHT = 16
CELL_DEPTH = 254

WORLD_TILT = math.radians(33)
WORLD_ROTATION = math.radians(-30)

WORLD_UP = glm.vec3(0.0, 1.0, 0.0)
WORLD_AXIS_X = glm.vec3(1.0, 0.0, 0.0)
WORLD_AXIS_Y = glm.vec3(0.0, 1.0, 0.0)
WORLD_AXIS_Z = glm.vec3(0.0, 0.0, 1.0)
