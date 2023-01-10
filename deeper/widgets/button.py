import imgui

from deeper.dimgui import Widget

class Button(Widget):
    def __init__(self, text, callback, small=False):
        super().__init__()
        self.text = text
        self.callback = callback
        self.small = small

    def draw(self):
        clicked = imgui.small_button(self.text) if self.small else imgui.button(self.text)
        if clicked:
            self.callback()

class RadioButton(Widget):
    def __init__(self, text, callback, active=False):
        super().__init__()
        self.text = text
        self.callback = callback
        self.active = active

    def draw(self):
        changed = imgui.radio_button(self.text, self.active)
        if changed:
            self.active = not self.active
            self.callback()

class RadioButtonGroup(Widget):
    def __init__(self, children=...):
        super().__init__(children)
        #self.selected = children[0]

    def add_child(self, child):
        super().add_child(child)
        if child.active:
            self.selected = child
        child_callback = child.callback
        child.callback = lambda: self.on_child_select(child, child_callback)

    def on_child_select(self, child, child_callback):
        if self.selected:
            self.selected.active = False
        self.selected = child
        child_callback()