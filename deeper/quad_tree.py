from crunge.engine.math.rect import RectF


class Quadtree:
    def __init__(self, boundary: RectF, capacity: int = 4):
        self.boundary = boundary  # The boundary of this node
        self.capacity = capacity  # Maximum objects before subdivision
        self.objects = []         # Objects stored in this node
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

        ne = RectF(x + w, y, w, h)
        nw = RectF(x, y, w, h)
        se = RectF(x + w, y + h, w, h)
        sw = RectF(x, y + h, w, h)

        self.northeast = Quadtree(ne, self.capacity)
        self.northwest = Quadtree(nw, self.capacity)
        self.southeast = Quadtree(se, self.capacity)
        self.southwest = Quadtree(sw, self.capacity)

        self.divided = True

    def insert(self, obj):
        """Insert an object with an AABB into the Quadtree."""
        if not self.boundary.intersects(obj.aabb):
            return False  # Object is out of bounds

        if self.divided:
            # Try to insert into a child that completely contains the object's AABB
            if self.northeast.boundary.contains_rect(obj.aabb):
                return self.northeast.insert(obj)
            elif self.northwest.boundary.contains_rect(obj.aabb):
                return self.northwest.insert(obj)
            elif self.southeast.boundary.contains_rect(obj.aabb):
                return self.southeast.insert(obj)
            elif self.southwest.boundary.contains_rect(obj.aabb):
                return self.southwest.insert(obj)
            else:
                # If it doesn't fit completely into any child, keep it here
                self.objects.append(obj)
                return True
        else:
            self.objects.append(obj)
            if len(self.objects) > self.capacity:
                self.subdivide()
                # Re-insert objects into appropriate child nodes
                i = 0
                while i < len(self.objects):
                    o = self.objects[i]
                    inserted = False
                    if self.northeast.boundary.contains_rect(o.aabb):
                        inserted = self.northeast.insert(o)
                    elif self.northwest.boundary.contains_rect(o.aabb):
                        inserted = self.northwest.insert(o)
                    elif self.southeast.boundary.contains_rect(o.aabb):
                        inserted = self.southeast.insert(o)
                    elif self.southwest.boundary.contains_rect(o.aabb):
                        inserted = self.southwest.insert(o)
                    if inserted:
                        self.objects.pop(i)
                    else:
                        # Object remains in parent node
                        i += 1
            return True

    def query(self, range_rect: RectF, found):
        """Find all objects that intersect with a given range."""
        if not self.boundary.intersects(range_rect):
            return  # Empty: no intersection
        else:
            for obj in self.objects:
                if obj.aabb.intersects(range_rect):
                    found.append(obj)
            if self.divided:
                self.northwest.query(range_rect, found)
                self.northeast.query(range_rect, found)
                self.southwest.query(range_rect, found)
                self.southeast.query(range_rect, found)

    def __str__(self, level=0):
        """String representation for debugging."""
        ret = "  " * level + f"Level {level}, Objects: {len(self.objects)}\n"
        if self.divided:
            ret += self.northwest.__str__(level + 1)
            ret += self.northeast.__str__(level + 1)
            ret += self.southwest.__str__(level + 1)
            ret += self.southeast.__str__(level + 1)
        return ret
