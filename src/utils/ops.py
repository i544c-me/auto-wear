from contextlib import contextmanager
import bpy

def parent_object(from_obj: bpy.types.Object, to_obj: bpy.types.Object):
    bpy.ops.object.select_all(action="DESELECT")

    for obj in from_obj.children:
        obj.select_set(True)

    bpy.context.view_layer.objects.active = to_obj

    bpy.ops.object.parent_set(keep_transform=True)


def change_armature(objs: tuple[bpy.types.Object], avatar_obj: tuple[bpy.types.Object]):
    for obj in objs:
        modifiers = [modifier for modifier in obj.modifiers if modifier.type == "ARMATURE"]
        if len(modifiers) > 0:
            modifiers[0].object = avatar_obj


@contextmanager
def use_edit_mode():
    bpy.ops.object.mode_set(mode="EDIT")
    yield
    bpy.ops.object.mode_set(mode="OBJECT")
