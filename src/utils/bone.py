from collections.abc import Iterator
import bpy

from . import ops

class BoneTree:
    "ボーンを正規化して木構造として表現する"
    bone_obj: bpy.types.Bone
    name: str
    normalized_name: str
    children: list["BoneTree"]
    parent: "BoneTree"
    delete_flag: bool

    def __init__(self, bone_obj: bpy.types.Bone):
        self.bone_obj = bone_obj
        self.name = bone_obj.name
        self.normalized_name = normalize_name(self.name)
        self.children = []
        self.parent = None
        self.delete_flag = False

    def add_child(self, child_node: "BoneTree"):
        child_node.parent = self
        self.children.append(child_node)

    def remove_subtree(self):
        self.children.clear()
        if self.parent:
            self.parent.children.remove(self)
            self.parent = None

    def display(self, level=0):
        print(" " * level * 2 + self.normalized_name)
        for child in self.children:
            child.display(level + 1)

    def list(self) -> Iterator["BoneTree"]:
        "root から順に返すイテレータを返す"
        if self.delete_flag:
            return

        yield self
        for child in self.children:
            yield from child.list()

    def find(self, name: str) -> "BoneTree":
        for child in self.list():
            if name == child.normalized_name \
                or name + ".001" == child.normalized_name \
                or name == child.normalized_name + ".001":
                return child

    def is_leaf_bone(self) -> bool:
        return self.name.endswith("_end")

    @staticmethod
    def create(root_bone: bpy.types.Bone) -> "BoneTree":
        root = BoneTree(root_bone)

        for child in root.bone_obj.children:
            root.add_child(BoneTree.create(child))

        return root

    @staticmethod
    def set_delete(node: "BoneTree", flag=True):
        node.delete_flag = flag
        for child in node.children:
            BoneTree.set_delete(child, flag)


def normalize_name(name: str) -> str:
    return name.lower() \
        .replace(" ", "") \
        .replace("_", ".") \
        .replace("toes", "toe")


def main(avatar_obj: bpy.types.Object, cloth_child_objs: tuple[bpy.types.Object], cloth_obj: bpy.types.Object):
    avatar_root_bone: bpy.types.Bone = [bone for bone in avatar_obj.data.bones if bone.parent is None][0]
    cloth_root_bone: bpy.types.Bone = [bone for bone in cloth_obj.data.bones if bone.parent is None][0]

    avatar_tree = BoneTree.create(avatar_root_bone)
    cloth_tree = BoneTree.create(cloth_root_bone)

    avatar_tree.display()
    cloth_tree.display()

    # ボーンを結合する
    bpy.ops.object.select_all(action="DESELECT")
    cloth_obj.select_set(True)
    avatar_obj.select_set(True)
    bpy.context.view_layer.objects.active = avatar_obj
    bpy.ops.object.join()

    # ボーンを移植する
    with ops.use_edit_mode():
        for cloth_bone in cloth_tree.list():
            same_in_avatar = avatar_tree.find(cloth_bone.normalized_name)

            if same_in_avatar or cloth_bone.is_leaf_bone():
                print(f"{cloth_bone.name} はアバターにもあるボーンのため移動しない")
                continue

            avatar_parent_bone = avatar_obj.data.edit_bones.get(avatar_tree.find(cloth_bone.parent.normalized_name).name)
            cloth_target_bone = avatar_obj.data.edit_bones.get(cloth_bone.name)
            cloth_target_bone.parent = avatar_parent_bone
            print(f"元の名前は {cloth_bone.name}")
            print(f"{cloth_target_bone.name} の親を {avatar_parent_bone.name} に変更")
            BoneTree.set_delete(cloth_bone, True)

    # 頂点グループを修正する
    for obj in cloth_child_objs:
        print(f"オブジェクト: {obj.name}")
        for group in obj.vertex_groups:
            normalized_name = normalize_name(group.name)
            print(f"  頂点グループ: {group.name}")
            if avatar_bone := avatar_tree.find(normalized_name):
                print(f"  頂点グループ名を {avatar_bone.name} に変更")
                group.name = avatar_bone.name
