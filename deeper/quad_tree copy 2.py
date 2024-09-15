import glm  # Ensure PyGLM is installed: pip install PyGLM

from loguru import logger

from crunge.engine.math.rect import RectF
from crunge.engine.d2.vu_2d import Vu2D

'''
class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x  # Center x-coordinate
        self.y = y  # Center y-coordinate
        self.w = w  # Half of the rectangle's width
        self.h = h  # Half of the rectangle's height

    def contains(self, point):
        """Check if the rectangle contains a point."""
        return (self.x - self.w <= point.x <= self.x + self.w and
                self.y - self.h <= point.y <= self.y + self.h)

    def intersects(self, other):
        """Check if the rectangle intersects with another rectangle."""
        return not (other.x - other.w > self.x + self.w or
                    other.x + other.w < self.x - self.w or
                    other.y - other.h > self.y + self.h or
                    other.y + other.h < self.y - self.h)
'''

class QuadTree:
    def __init__(self, boundary: RectF, capacity=4):
        self.boundary = boundary  # The 2D space covered by this node
        self.capacity = capacity  # Max points before subdivision
        self.points = []          # Points within this node
        self.divided = False      # Has this node been subdivided?
        # Child nodes
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None

    def subdivide(self):
        """Subdivide the node into four child quadrants."""
        x, y = self.boundary.x, self.boundary.y
        w, h = self.boundary.width / 2, self.boundary.height / 2

        ne = RectF(x + w, y - h, w, h)
        nw = RectF(x - w, y - h, w, h)
        se = RectF(x + w, y + h, w, h)
        sw = RectF(x - w, y + h, w, h)

        self.northeast = QuadTree(ne, self.capacity)
        self.northwest = QuadTree(nw, self.capacity)
        self.southeast = QuadTree(se, self.capacity)
        self.southwest = QuadTree(sw, self.capacity)

        self.divided = True

    def insert(self, point):
        """Insert a point into the Quadtree."""
        #if not self.boundary.contains(point):
        if not self.boundary.intersects(point.aabb):
            return False  # Point is out of bounds

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()

            return (self.northeast.insert(point) or
                    self.northwest.insert(point) or
                    self.southeast.insert(point) or
                    self.southwest.insert(point))

    def query(self, range_rect, found):
        """Find all points within a given range."""
        if not self.boundary.intersects(range_rect):
            return  # Empty: no intersection
        else:
            for p in self.points:
                #if range_rect.contains(p):
                if range_rect.intersects(p.aabb):
                    found.append(p)
            if self.divided:
                self.northwest.query(range_rect, found)
                self.northeast.query(range_rect, found)
                self.southwest.query(range_rect, found)
                self.southeast.query(range_rect, found)

    def __str__(self, level=0):
        """String representation for debugging."""
        ret = "  " * level + f"Level {level}, Points: {len(self.points)}\n"
        if self.divided:
            ret += self.northwest.__str__(level + 1)
            ret += self.northeast.__str__(level + 1)
            ret += self.southwest.__str__(level + 1)
            ret += self.southeast.__str__(level + 1)
        return ret

'''
# Example usage
if __name__ == "__main__":
    # Define the boundary of the Quadtree (centered at (0, 0) with width and height of 400)
    boundary = Rectangle(0, 0, 200, 200)
    quadtree = Quadtree(boundary, capacity=4)

    # Insert random points into the Quadtree
    import random
    for _ in range(500):
        x = random.uniform(-200, 200)
        y = random.uniform(-200, 200)
        point = glm.vec2(x, y)
        quadtree.insert(point)

    # Define a range for querying (centered at (0, 0) with width and height of 100)
    query_range = Rectangle(0, 0, 50, 50)
    found_points = []
    quadtree.query(query_range, found_points)

    print(f"Total points found: {len(found_points)}")
    # Optionally print the Quadtree structure
    # print(quadtree)
'''