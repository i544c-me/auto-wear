import bpy

def parent_object(from_obj: bpy.types.Object, to_obj: bpy.types.Object):
    bpy.ops.object.select_all(action="DESELECT")

    for obj in from_obj.children:
        obj.select_set(True)

    bpy.context.view_layer.objects.active = to_obj

    bpy.ops.object.parent_set(keep_transform=True)
