from loguru import logger

from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.d2.sprite.dynamic import DynamicSpriteGroup
from crunge.engine.d2.sprite.sprite_vu_group import SpriteVuGroup
from crunge.engine.d2.sprite.instanced.instanced_sprite_program import InstancedSpriteProgram
from crunge.engine.render_group import RenderGroup
from crunge.engine.math import Rect2

from deeper.event import EventSource, LayerDirtyEvent

from .ecs.entity_group import EntityGroup
from .quad_tree import Quadtree

CAPACITY = 1024


class SequencedSpriteVuGroup(SpriteVuGroup):
    """Sprite group that orders by append sequence rather than by depth.

    deeper establishes draw order by the order it calls add_sprite_vu, so the
    group must not second-guess it. This reproduces the old
    InstancedSpriteVuGroup's stream exactly: stable sort on the sequence
    keeps insertion order, and extends() merges adjacent equal-texture runs,
    which is what batch() did.

    Delete this class once SpriteVu.sort_key returns something real for
    deeper; SpriteVuGroup's own (depth, material) key takes over and the
    material tie-break starts earning draw calls back.
    """

    def sort_key(self, vu: SpriteVu):
        return vu.group_sequence


class SceneLayer(EntityGroup):
    def __init__(self, scene, name):
        super().__init__(name)
        self.scene = scene
        self.name = name
        self.sprite_group = DynamicSpriteGroup(CAPACITY).enable()

        # is_managed: add_sprite_vu is the only way in. Nothing here is in a
        # node tree, so a vu's find_render_group would come back None
        # regardless, but saying so explicitly means wiring one up later
        # won't produce double appends.
        self.render_group = RenderGroup(is_managed=True)

        # Bound to locals rather than reached through self: a lambda closing
        # over self would make layer -> render_group -> factories -> closure
        # -> layer, which survives gen-0-only collection under gc.disable().
        sprite_group = self.sprite_group
        self.render_group.register(
            SpriteVu,
            lambda: SequencedSpriteVuGroup(CAPACITY, sprite_group, InstancedSpriteProgram()),
        )

        # ASSUMPTION: Chip.enable() works unseated, as it did for the old
        # InstancedSpriteVuGroup(...).enable() here.
        self.render_group.enable()

        self.visible = True
        self.locked = False
        self.dirty = True
        self.events = EventSource()

    def __str__(self) -> str:
        return f"Layer({self.name})"

    def __repr__(self) -> str:
        return self.__str__()

    def enable(self):
        pass

    def disable(self):
        pass

    def mark(self):
        self.dirty = True
        self.events.publish(LayerDirtyEvent())

    def unmark(self):
        self.dirty = False

    def clear(self):
        self.render_group.clear()

    def add_sprite_vu(self, vu: SpriteVu):
        # Tells the vu it is grouped, so it skips allocating a program,
        # buffers and bind groups it will never draw through. See the note
        # about enable ordering below.
        vu.render_group = self.render_group
        self.render_group.append(vu)
        return vu

    def update(self, delta_time: float):
        # Where the replan happens, so the clear -> add -> update ordering
        # the scene already uses is load-bearing. Anything appended after
        # update lands in no run and does not draw until the next frame.
        self.render_group.update(delta_time)

    def draw(self):
        if not self.visible:
            return
        self.render_group.draw()