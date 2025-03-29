import bpy

from .utils import parent, move_bone

class Sidebar(bpy.types.Panel):
    bl_label = "i544cAutoWear"
    bl_idname = "i544cAutoWear_PT_sidebar"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "i544cAutoWear"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.label(text="今のところは自動的にボーンを移植するツールです。")
        layout.prop_search(scene, "avatar_object", bpy.data, "objects", text="アバターのオブジェクト")
        layout.prop_search(scene, "cloth_object", bpy.data, "objects", text="服のオブジェクト")
        row = layout.row()
        row.enabled = context.mode == "OBJECT" # 編集モードなどではこの先の処理を実行できないため
        row.operator("object.i544c_autowear_operator")


class Operator(bpy.types.Operator):
    "ボーンを移植します（オブジェクトモードでのみ実行可能）"
    bl_idname = "object.i544c_autowear_operator"
    bl_label = "着せる！"

    def execute(self, context):
        avatar_object: bpy.types.Object = context.scene.avatar_object
        cloth_object: bpy.types.Object = context.scene.cloth_object

        # parent
        parent.parent_object(cloth_object, avatar_object)
 
        # move-bone
        move_bone.main(avatar_object, cloth_object)

        self.report({'INFO'}, "処理が完了しました！")
        return {'FINISHED'}


def is_parent(self, obj):
    return obj.type == "ARMATURE"


def register():
    bpy.utils.register_class(Sidebar)
    bpy.utils.register_class(Operator)
    bpy.types.Scene.avatar_object = bpy.props.PointerProperty(
        name="Avatar Object",
        description="アバターのオブジェクトの名前",
        type=bpy.types.Object,
        poll=is_parent,
    )
    bpy.types.Scene.cloth_object = bpy.props.PointerProperty(
        name="Cloth Object",
        description="服のオブジェクトの名前",
        type=bpy.types.Object,
        poll=is_parent,
    )

def unregister():
    bpy.utils.unregister_class(Sidebar)
    bpy.utils.unregister_class(Operator)
    del bpy.types.Scene.avatar_object
    del bpy.types.Scene.cloth_object
