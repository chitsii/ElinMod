# -*- coding: utf-8 -*-
"""
rewards.py - 汎用報酬システム

ランク報酬、サブクエスト報酬、任意の報酬を宣言的に定義。
ArenaDramaBuilderから使用される。
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict

from flag_definitions import Keys, QuestIds


@dataclass
class RewardItem:
    """アイテム報酬"""
    item_id: str      # "medal", "1165", "lovepotion"
    count: int = 1


@dataclass
class Reward:
    """
    汎用報酬定義

    ランク報酬、サブクエスト報酬、任意の報酬に使用可能。
    """
    # アイテム報酬
    items: List[RewardItem] = field(default_factory=list)

    # バフ報酬（C#メソッド呼び出し）
    buff_method: Optional[str] = None  # "GrantRankFBonus"

    # フラグ設定
    flags: Dict[str, int] = field(default_factory=dict)
    # 例: {Keys.RANK: 2}

    # メッセージ（NPC発言）
    message_jp: str = ""
    message_en: str = ""

    # システムメッセージ（称号獲得など）
    system_message_jp: str = ""
    system_message_en: str = ""


@dataclass
class RankReward(Reward):
    """
    ランク報酬定義

    Rewardを継承し、ランク固有の情報を追加。
    """
    # ランク値（Keys.RANKに設定する値）
    rank_value: int = 0

    # 対応するクエストID
    quest_id: str = ""


# ============================================================================
# ランク報酬定義（G〜A）
# ============================================================================

RANK_REWARDS: Dict[str, RankReward] = {
    "G": RankReward(
        items=[
            RewardItem("medal", 10),
            RewardItem("1165", 3),
            RewardItem("lovepotion", 30),
        ],
        rank_value=1,
        quest_id=QuestIds.RANK_UP_G,
        message_jp="報酬として、小さなメダル10枚、エーテル抗体3本、媚薬30本をお渡しします。",
        message_en="As your reward, I present you with 10 small medals, 3 ether antibodies, and 30 love potions.",
    ),
    "F": RankReward(
        items=[
            RewardItem("medal", 20),
            RewardItem("1165", 6),
            RewardItem("lovepotion", 60),
        ],
        buff_method="GrantRankFBonus",
        rank_value=2,
        quest_id=QuestIds.RANK_UP_F,
        message_jp="報酬として、小さなメダル20枚、エーテル抗体6本、媚薬60本をお渡しします。",
        message_en="As your reward, I present you with 20 small medals, 6 ether antibodies, and 60 love potions.",
        system_message_jp="【システム】称号『泥犬（Mud Dog）』を獲得しました。耐久+3、冷気耐性+5 の加護を得た！",
        system_message_en="[System] Title 'Mud Dog' acquired. Endurance+3, Cold Resistance+5 blessing obtained!",
    ),
    "E": RankReward(
        items=[
            RewardItem("medal", 30),
            RewardItem("1165", 9),
            RewardItem("lovepotion", 90),
        ],
        buff_method="GrantRankEBonus",
        rank_value=3,
        quest_id=QuestIds.RANK_UP_E,
        message_jp="報酬として、小さなメダル30枚、エーテル抗体9本、媚薬90本をお渡しします。",
        message_en="As your reward, I present you with 30 small medals, 9 ether antibodies, and 90 love potions.",
        system_message_jp="【システム】称号『鉄屑（Iron Scrap）』を獲得しました。筋力+3、PV+5 の加護を得た！",
        system_message_en="[System] Title 'Iron Scrap' acquired. Strength+3, PV+5 blessing obtained!",
    ),
    "D": RankReward(
        items=[
            RewardItem("medal", 40),
            RewardItem("1165", 12),
            RewardItem("lovepotion", 120),
        ],
        buff_method="GrantRankDBonus",
        rank_value=4,
        quest_id=QuestIds.RANK_UP_D,
        message_jp="報酬として、小さなメダル40枚、エーテル抗体12本、媚薬120本をお渡しします。",
        message_en="As your reward, I present you with 40 small medals, 12 ether antibodies, and 120 love potions.",
        system_message_jp="【システム】称号『銅貨稼ぎ（Copper Earner）』を獲得しました。回避+5、運+3 の加護を得た！",
        system_message_en="[System] Title 'Copper Earner' acquired. Evasion+5, Luck+3 blessing obtained!",
    ),
    "C": RankReward(
        items=[
            RewardItem("medal", 50),
            RewardItem("1165", 15),
            RewardItem("lovepotion", 150),
        ],
        buff_method="GrantRankCBonus",
        rank_value=5,
        quest_id=QuestIds.RANK_UP_C,
        message_jp="報酬として、小さなメダル50枚、エーテル抗体15本、媚薬150本をお渡しします。",
        message_en="As your reward, I present you with 50 small medals, 15 ether antibodies, and 150 love potions.",
        system_message_jp="【システム】称号『闘技場の鴉（Arena Crow）』を獲得しました。器用+5、スタミナ+10 の加護を得た！",
        system_message_en="[System] Title 'Arena Crow' acquired. Dexterity+5, Stamina+10 blessing obtained!",
    ),
    "B": RankReward(
        items=[
            RewardItem("medal", 60),
            RewardItem("1165", 18),
            RewardItem("lovepotion", 180),
        ],
        buff_method="GrantRankBBonus",
        rank_value=6,
        quest_id=QuestIds.RANK_UP_B,
        message_jp="報酬として、小さなメダル60枚、エーテル抗体18本、媚薬180本をお渡しします。",
        message_en="As your reward, I present you with 60 small medals, 18 ether antibodies, and 180 love potions.",
        system_message_jp="【システム】称号『銀翼（Silver Wing）』を獲得しました。全ステータス+3、魔法耐性+10 の加護を得た！",
        system_message_en="[System] Title 'Silver Wing' acquired. All stats+3, Magic Resistance+10 blessing obtained!",
    ),
    "A": RankReward(
        items=[
            RewardItem("medal", 70),
            RewardItem("1165", 21),
            RewardItem("lovepotion", 210),
        ],
        buff_method="GrantRankABonus",
        rank_value=7,
        quest_id=QuestIds.RANK_UP_A,
        message_jp="報酬として、小さなメダル70枚、エーテル抗体21本、媚薬210本をお渡しします。",
        message_en="As your reward, I present you with 70 small medals, 21 ether antibodies, and 210 love potions.",
        system_message_jp="【システム】称号『黄金の戦鬼（Golden War Demon）』を獲得しました。筋力+5、魔力+5、回避+5、PV+5 の加護を得た！",
        system_message_en="[System] Title 'Golden War Demon' acquired. Strength+5, Magic+5, Evasion+5, PV+5 blessing obtained!",
    ),
}


# ============================================================================
# サブクエスト報酬定義（将来の拡張用）
# ============================================================================

QUEST_REWARDS: Dict[str, Reward] = {
    # 将来の拡張用
}


# ============================================================================
# バリデーション
# ============================================================================

def validate_rank_rewards() -> List[str]:
    """
    ランク報酬定義のバリデーション

    Returns:
        エラーメッセージのリスト（空なら問題なし）
    """
    errors = []

    expected_ranks = ["G", "F", "E", "D", "C", "B", "A"]

    # 全ランクが定義されているか
    for rank in expected_ranks:
        if rank not in RANK_REWARDS:
            errors.append(f"RANK_REWARDS: ランク '{rank}' が定義されていません")

    # 各ランク報酬の検証
    for rank, reward in RANK_REWARDS.items():
        prefix = f"RANK_REWARDS['{rank}']"

        # rank_value が設定されているか
        if reward.rank_value <= 0:
            errors.append(f"{prefix}: rank_value が設定されていません")

        # quest_id が設定されているか
        if not reward.quest_id:
            errors.append(f"{prefix}: quest_id が設定されていません")

        # message_jp が設定されているか
        if not reward.message_jp:
            errors.append(f"{prefix}: message_jp が設定されていません")

        # アイテムが空でないか
        if not reward.items:
            errors.append(f"{prefix}: items が空です")

        # buff_method が設定されている場合、system_message_jp も必要（G以外）
        if rank != "G" and reward.buff_method and not reward.system_message_jp:
            errors.append(f"{prefix}: buff_method が設定されていますが system_message_jp がありません")

    return errors


def validate_all() -> List[str]:
    """
    全ての報酬定義をバリデーション

    Returns:
        エラーメッセージのリスト（空なら問題なし）
    """
    errors = []
    errors.extend(validate_rank_rewards())
    return errors


# ============================================================================
# テスト
# ============================================================================

if __name__ == "__main__":
    print("=== Rewards Validation ===\n")

    errors = validate_all()
    if errors:
        print("Errors found:")
        for error in errors:
            print(f"  - {error}")
        exit(1)
    else:
        print("All validations passed!")

    print("\n=== Rank Rewards Summary ===\n")
    for rank, reward in RANK_REWARDS.items():
        items_str = ", ".join([f"{item.item_id}x{item.count}" for item in reward.items])
        buff_str = reward.buff_method or "none"
        print(f"Rank {rank}: rank_value={reward.rank_value}, items=[{items_str}], buff={buff_str}")
