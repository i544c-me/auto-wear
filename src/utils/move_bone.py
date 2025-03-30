import bpy

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
        self.normalized_name = self._normalize_name(self.name)
        self.children = []
        self.parent = None
        self.delete_flag = False
    
    def _normalize_name(self, name: str) -> str:
        return name.lower() \
            .replace(" ", "") \
            .replace("_", ".") \
            .replace("toes", "toe")

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

    def list(self):
        "root から順に返すイテレータ"
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
        return self.name.endswith(["_end"])

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


def main(avatar_obj: bpy.types.Object, cloth_obj: bpy.types.Object):
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
    bpy.ops.object.mode_set(mode="EDIT")

    for cloth_bone in cloth_tree.list():
        same_in_avatar = avatar_tree.find(cloth_bone.normalized_name)

        if not same_in_avatar and not cloth_bone.is_leaf_bone:
            avatar_parent_bone = avatar_obj.data.edit_bones.get(avatar_tree.find(cloth_bone.parent.normalized_name).name)
            cloth_target_bone = avatar_obj.data.edit_bones.get(cloth_bone.name)
            cloth_target_bone.parent = avatar_parent_bone
            print(f"元の名前は {cloth_bone.name}")
            print(f"{cloth_target_bone.name} の親を {avatar_parent_bone.name} に変更")
            BoneTree.set_delete(cloth_bone, True)
        else:
            print(f"{cloth_bone.name} はアバターにもあるボーンのため移動しない")

    bpy.ops.object.mode_set(mode="OBJECT")
