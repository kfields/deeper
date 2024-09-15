from loguru import logger

from crunge.engine.math.rect import RectF
from crunge.engine.d2.vu_2d import Vu2D

class BoundingBox(Vu2D):
    def __init__(self, aabb: RectF) -> None:
        self.aabb = aabb

class QuadTree:
    def __init__(self, bounds: RectF, max_objects=4, max_levels=5, level=0):
        self.bounds = bounds  # A RectF or RectI representing the quad bounds
        self.max_objects = max_objects  # Max objects before subdivision
        self.max_levels = max_levels  # Max levels for recursion
        self.level = level  # Current level of this node
        self.objects: list[Vu2D] = []  # Objects within this node
        self.nodes: list["QuadTree"] = []  # Subnodes (if subdivided)

    def clear(self):
        """Clears the quadtree recursively"""
        self.objects.clear()
        self.nodes.clear()

    def subdivide(self):
        """Subdivides the current node into four subnodes"""
        x, y, width, height = self.bounds.x, self.bounds.y, self.bounds.width, self.bounds.height
        half_width = width / 2
        half_height = height / 2

        self.nodes = [
            QuadTree(RectF(x, y, half_width, half_height), self.max_objects, self.max_levels, self.level + 1),  # Top left
            QuadTree(RectF(x + half_width, y, half_width, half_height), self.max_objects, self.max_levels, self.level + 1),  # Top right
            QuadTree(RectF(x, y + half_height, half_width, half_height), self.max_objects, self.max_levels, self.level + 1),  # Bottom left
            QuadTree(RectF(x + half_width, y + half_height, half_width, half_height), self.max_objects, self.max_levels, self.level + 1)  # Bottom right
        ]

    def get_index(self, obj: Vu2D) -> int:
        """Determines which node the object belongs to.
        Returns -1 if the object doesn't fit completely in any subnode.
        """
        obj_bounds = obj.aabb

        # Find the midpoint
        vertical_midpoint = self.bounds.x + self.bounds.width / 2
        horizontal_midpoint = self.bounds.y + self.bounds.height / 2

        top_quadrant = obj_bounds.y + obj_bounds.height < horizontal_midpoint
        bottom_quadrant = obj_bounds.y > horizontal_midpoint
        left_quadrant = obj_bounds.x + obj_bounds.width < vertical_midpoint
        right_quadrant = obj_bounds.x > vertical_midpoint

        # Determine which quadrant the object fits into
        if left_quadrant:
            if top_quadrant:
                return 0  # Top left
            elif bottom_quadrant:
                return 2  # Bottom left
        elif right_quadrant:
            if top_quadrant:
                return 1  # Top right
            elif bottom_quadrant:
                return 3  # Bottom right

        return -1  # Object can't fit completely in any quadrant

    def insert(self, obj):
        """Inserts an object into the quad-tree. If the node exceeds capacity, it subdivides and reassigns objects."""
        if self.nodes:
            index = self.get_index(obj)
            if index != -1:
                self.nodes[index].insert(obj)
                return

        self.objects.append(obj)

        # If node exceeds max_objects, subdivide and reassign objects
        if len(self.objects) > self.max_objects and self.level < self.max_levels:
            if not self.nodes:
                self.subdivide()

            i = 0
            while i < len(self.objects):
                index = self.get_index(self.objects[i])
                if index != -1:
                    self.nodes[index].insert(self.objects.pop(i))
                else:
                    i += 1

    def retrieve(self, bounds: RectF) -> list[Vu2D]:
        """Returns all objects that could collide with the given bounds"""
        results = []
        index = self.get_index(BoundingBox(bounds))

        # If object fits in a subnode, retrieve from that node
        if index != -1 and self.nodes:
            results.extend(self.nodes[index].retrieve(bounds))

        # Always add objects in the current node
        results.extend(self.objects)
        return results
