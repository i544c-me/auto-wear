import bpy

class BoneTree:
    bone_obj: bpy.types.Bone
    name: str
    normalized_name: str
    children: list["BoneTree"]
    parent: "BoneTree"

    def __init__(self, bone_obj: bpy.types.Bone):
        self.bone_obj = bone_obj
        self.name = bone_obj.name
        self.normalized_name = self._normalize_name(self.name)
        self.children = []
        self.parent = None
    
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


    @staticmethod
    def create(root_bone: bpy.types.Bone) -> "BoneTree":
        root = BoneTree(root_bone)

        for child in root.bone_obj.children:
            root.add_child(BoneTree.create(child))

        return root


def main(avatar_obj: bpy.types.Object, cloth_obj: bpy.types.Object):
    avatar_root_bone: bpy.types.Bone = [bone for bone in avatar_obj.data.bones if bone.parent is None][0]
    cloth_root_bone: bpy.types.Bone = [bone for bone in cloth_obj.data.bones if bone.parent is None][0]

    avatar_tree = BoneTree.create(avatar_root_bone)
    cloth_tree = BoneTree.create(cloth_root_bone)

    avatar_tree.display()
    cloth_tree.display()
