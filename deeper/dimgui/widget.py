class Widget:
    _parent: None
    def __init__(self, children=[]):
        self.children = []
        self.add_children(children)
        self.gui = None

    def create(self, gui):
        self.gui = gui
        for child in self.children:
            child.create(gui)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent


    def add_children(self, children):
        for child in children:
            self.add_child(child)

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def draw(self):
        for child in self.children:
            child.draw()
        return True