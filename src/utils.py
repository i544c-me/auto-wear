import bpy

type NormalizedBones = dict[str, str]

def parent_object(from_obj: bpy.types.Object, to_obj: bpy.types.Object):
    bpy.ops.object.select_all(action="DESELECT")

    for obj in from_obj.children:
        obj.select = True

    bpy.context.view_layer.objects.active = to_obj

    bpy.ops.object.parent_set(keep_transform=True)


def normalize_bones(bones: list[bpy.types.Bone]) -> NormalizedBones:
    dic = {}

    for bone in bones:
        dic[normalize_bonename(bone.name)] = bone.name

    return dic


def normalize_bonename(bone_name: str) -> str:
    # TODO: cloth_bone を変形して、avatar_bone と同じ命名規則にする
    # ex: UpperLeg_L → Upper Leg.L
    # キャメルケースは空白で区切る
    # _ は . に置換する
    #
    # 例外
    # Toe は Toes に置換する

    return ""


class MoveBones:
    def __init__(self, avatar_object: bpy.types.Object, cloth_object: bpy.types.Object):
        self.avatar_bones = avatar_object.data.bones
        self.cloth_bones = cloth_object.data.bones
        self.avatar_normalized_bones = normalize_bones(self.avatar_bones)
        self.cloth_normalized_bones = normalize_bones(self.cloth_bones)

    def move_bones(self):
        root_bones = [bone for bone in self.cloth_bones if not bone.parent]

        for root_bone in root_bones:
            self.traverse_bone(root_bone)

    def traverse_bone(self, bone: bpy.types.Bone):
        if normalize_bonename(bone.name) not in self.avatar_normalized_bones:
            bone.parent = self.avatar_bones[self.avatar_normalized_bones[normalize_bonename(bone.parent.name)]]
            return

        for child in bone.children:
            self.traverse_bone(child)
