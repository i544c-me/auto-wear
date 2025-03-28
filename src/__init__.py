import bpy

class Sidebar(bpy.types.Panel):
    bl_label = "i544cAutoWear"
    bl_idname = "i544cAutoWear.sidebar"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "i544cAutoWear"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.label(text="今のところは自動的にボーンを移植するツールです。")
        layout.prop_search(scene, "avatar_object", bpy.data, "objects", text="アバターのオブジェクト")
        layout.prop_search(scene, "cloth_object", bpy.data, "objects", text="服のオブジェクト")
        layout.operator("object.i544c_autowear_operator")


class Operator(bpy.types.Operator):
    bl_idname = "object.i544c_autowear_operator"
    bl_label = "着せる！"

    def execute(self, context):
        self.report({'INFO'}, "ボタンがクリックされました！")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(Sidebar)
    bpy.utils.register_class(Operator)
    bpy.types.Scene.avatar_object = bpy.props.StringProperty(
        name="Avatar Object",
        description="アバターのオブジェクトの名前",
    )
    bpy.types.Scene.cloth_object = bpy.props.StringProperty(
        name="Cloth Object",
        description="服のオブジェクトの名前",
    )

def unregister():
    bpy.utils.unregister_class(Sidebar)
    bpy.utils.unregister_class(Operator)
    del bpy.types.Scene.avatar_object
    del bpy.types.Scene.cloth_object
