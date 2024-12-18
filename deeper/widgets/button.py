from crunge import imgui

from crunge.engine import Renderer

from crunge.engine.imgui.widget import Widget

class Button(Widget):
    def __init__(self, label, callback, small=False):
        super().__init__()
        self.label = label
        self.callback = callback
        self.small = small

    def draw(self, renderer: Renderer):
        clicked = imgui.small_button(self.label) if self.small else imgui.button(self.label)
        if clicked:
            self.callback()

class RadioButton(Widget):
    def __init__(self, label, callback, active=False):
        super().__init__()
        self.label = label
        self.callback = callback
        self.active = active

    def draw(self, renderer: Renderer):
        changed = imgui.radio_button(self.label, self.active)
        if changed:
            self.active = not self.active
            self.callback()

class RadioButtonGroup(Widget):
    def __init__(self, children=...):
        super().__init__(children)
        #self.selected = children[0]

    def attach(self, child):
        super().attach(child)
        if child.active:
            self.selected = child
        child_callback = child.callback
        child.callback = lambda: self.on_child_select(child, child_callback)

    def on_child_select(self, child, child_callback):
        if self.selected:
            self.selected.active = False
        self.selected = child
        child_callback()