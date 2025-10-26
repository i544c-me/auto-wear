import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# bpy モジュールをモック化してインポートエラーを回避
sys.modules["bpy"] = MagicMock()
sys.modules["bpy.types"] = MagicMock()

# このタイミングでメインのコードから normalize_name 関数をインポート
# そうでなければエラーになる
from src.utils.bone import normalize_name  # noqa: E402


class TestNormalizeName(unittest.TestCase):
    def test_suffix_pattern_with_space(self):
        """ラシューシャのテスト"""
        self.assertEqual(normalize_name("Upper Leg.L"), "upperleg.l")
        self.assertEqual(normalize_name("Upper Leg.R"), "upperleg.r")
        self.assertEqual(normalize_name("Upper Arm.L"), "upperarm.l")
        self.assertEqual(normalize_name("Upper Arm.R"), "upperarm.r")
        self.assertEqual(normalize_name("Thumb Proximal.L"), "thumbproximal.l")
        self.assertEqual(normalize_name("Thumb Proximal.R"), "thumbproximal.r")
        self.assertEqual(normalize_name("Toes.L"), "toe.l")
        self.assertEqual(normalize_name("Toes.R"), "toe.r")

    def test_suffix_pattern_with_no_space(self):
        """森羅のテスト"""
        self.assertEqual(normalize_name("UpperLeg_L"), "upperleg.l")
        self.assertEqual(normalize_name("UpperLeg_R"), "upperleg.r")
        self.assertEqual(normalize_name("UpperArm_L"), "upperarm.l")
        self.assertEqual(normalize_name("UpperArm_R"), "upperarm.r")
        self.assertEqual(normalize_name("Toe_L"), "toe.l")
        self.assertEqual(normalize_name("Toe_R"), "toe.r")

    def test_prefix_pattern_with_underscore(self):
        """QuQu のテスト"""
        self.assertEqual(normalize_name("L_UpperLeg"), "upperleg.l")
        self.assertEqual(normalize_name("R_UpperLeg"), "upperleg.r")
        self.assertEqual(normalize_name("L_UpperArm"), "upperarm.l")
        self.assertEqual(normalize_name("R_UpperArm"), "upperarm.r")
        self.assertEqual(normalize_name("L_thumb_proximal"), "thumbproximal.l")
        self.assertEqual(normalize_name("L_Toe"), "toe.l")
        self.assertEqual(normalize_name("R_Toe"), "toe.r")

    def test_lowercase_prefix_pattern(self):
        """小文字のプレフィックスパターンのテスト"""
        self.assertEqual(normalize_name("l_upperleg"), "upperleg.l")
        self.assertEqual(normalize_name("r_upperleg"), "upperleg.r")

    def test_no_side_suffix(self):
        """左右の指定がない場合のテスト"""
        self.assertEqual(normalize_name("Spine"), "spine")
        self.assertEqual(normalize_name("Head"), "head")
        self.assertEqual(normalize_name("Upper Body"), "upperbody")

    def test_underscore_to_dot(self):
        """アンダースコアをドットに変換（L/Rプレフィックスでない場合）"""
        self.assertEqual(normalize_name("Foot_IK.L"), "foot.ik.l")
        self.assertEqual(normalize_name("Hand_IK.R"), "hand.ik.r")

    def test_complex_names(self):
        """複雑なボーン名のテスト"""
        # プレフィックス除去後、残りのアンダースコアはそのまま保持される
        self.assertEqual(normalize_name("L_Upper_Leg"), "upperleg.l")
        self.assertEqual(normalize_name("R_Upper_Arm"), "upperarm.r")


if __name__ == "__main__":
    unittest.main()
