from enum import Enum

from loguru import logger
from crunge import imgui

from crunge.engine import Renderer
from crunge.engine.imgui.widget import Widget, WidgetGroup


class SelectableMode(Enum):
    SELECT = (0,)
    EDIT = 1


class SelectableBase(Widget):
    def __init__(self, label, callback, selected=False, children=[], width=0, height=0):
        super().__init__(children)
        self.label = label
        self.callback = callback
        self.selected = selected
        self.width = width
        self.height = height

    def select(self, selected=True):
        self.selected = selected
        self.callback(self)
        self.on_select(selected)

    def on_select(self, selected):
        pass


class Selectable(SelectableBase):
    def draw(self, renderer: Renderer):
        clicked, selected = imgui.selectable(
            self.label, self.selected, width=self.width, height=self.height
        )
        if clicked:
            self.select(selected)


class EditableSelectable(SelectableBase):
    def __init__(
        self,
        label,
        callback,
        selected=False,
        mode=SelectableMode.SELECT,
        width=0,
        height=0,
    ):
        super().__init__(label, callback, selected, width=width, height=height)
        self.mode = mode

    def on_select(self, selected):
        if not selected:
            self.mode = SelectableMode.SELECT

    def draw(self, renderer: Renderer):
        if self.mode == SelectableMode.SELECT:
            clicked, selected = imgui.selectable(
                self.label,
                self.selected,
                flags=imgui.SelectableFlags.ALLOW_DOUBLE_CLICK,
                size=(self.width, self.height),
            )
            #if imgui.is_item_hovered() and imgui.is_mouse_double_clicked():
            if imgui.is_item_hovered() and imgui.is_mouse_double_clicked(0):
                self.mode = SelectableMode.EDIT
            elif clicked:
                self.select(selected)
        else:
            changed, value = imgui.input_text(f'##{id(self)}', self.label, 32)
            if changed:
                #logger.debug(changed)
                #logger.debug(value)
                self.label = value

            # TODO: need to detect other loss of focus?
            if imgui.is_key_down(imgui.KEY_ESCAPE):
                self.mode = SelectableMode.SELECT


class SelectableGroup(WidgetGroup):
    def __init__(self, children, callback=lambda: None):
        super().__init__(children)
        self.callback = callback

    def attach(self, child):
        super().attach(child)
        child_callback = child.callback
        child.callback = lambda child: self.on_child_select(child, child_callback)

    def on_child_select(self, child, child_callback):
        #logger.debug(child)
        child_callback()
        self.callback()


class ExclusiveSelectableGroup(SelectableGroup):
    def __init__(self, children, callback=lambda: None):
        super().__init__(children, callback)
        self.selection = None

    def on_child_select(self, child, child_callback):
        logger.debug(child)
        if self.selection == child:
            return
        if self.selection:
            logger.debug(self.selection)
            # self.selection.selected = False
            self.selection.select(False)
        self.selection = child
        child.selected = True
        child_callback(child)
        self.callback(child)
