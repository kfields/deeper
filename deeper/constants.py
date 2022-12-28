import math
import glm

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
#SCREEN_WIDTH = 800
#SCREEN_HEIGHT = 600

CELL_WIDTH = 0.875
CELL_HEIGHT = 1
CELL_DEPTH = 1

WORLD_TILT = math.radians(33)
WORLD_ROTATION = math.radians(-30)
WORLD_SCALE = 256

WORLD_UP = glm.vec3(0.0, 1.0, 0.0)
WORLD_AXIS_X = glm.vec3(1.0, 0.0, 0.0)
WORLD_AXIS_Y = glm.vec3(0.0, 1.0, 0.0)
WORLD_AXIS_Z = glm.vec3(0.0, 0.0, 1.0)

DEFAULT_VEC2 = glm.vec2()
DEFAULT_VEC3 = glm.vec3()