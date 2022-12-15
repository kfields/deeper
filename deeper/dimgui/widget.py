class Widget:
    def __init__(self, children=[]):
        self.children = children

    def add_child(self, child):
        self.children.append(child)

    def draw(self):
        for child in self.children:
            child.draw()
        return True