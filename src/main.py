import bpy
from bpy.types import AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty

bl_info = {
    "name": "graft bones",
    "author": "i544c",
    "version": (0, 1),
    "blender": (4, 0, 0),
    "description": "服からアバターへ骨を移植するツールです",
    "category": "Object",
}


class GraftBones(AddonPreferences):
    bl_idname = __name__

    filepath = StringProperty(
        name="Example File Path",
        subtype="FILE_PATH",
    )
    number = IntProperty(
        name="Example Number",
        default=4
    )
    boolean = BoolProperty(
        name="Example Boolean",
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="This is a preference example")
        row = layout.row()
        row.prop(self, "filepath")
        row.prop(self, "number")
        row.prop(self, "boolean")


def register():
    bpy.utils.register_class(GraftBones)


def unregister():
    bpy.utils.unregister_class(GraftBones)


if __name__ == "__main__":
    register()
