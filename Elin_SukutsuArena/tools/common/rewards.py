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

    # フィート報酬（闘志フィートのレベル）
    feat_level: int = 0  # 1-7 (0=なし)

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
        feat_level=1,
        rank_value=1,
        quest_id=QuestIds.RANK_UP_G,
        message_jp="報酬として、小さなメダル10枚、エーテル抗体3本、媚薬30本をお渡しします。",
        message_en="As your reward, I present you with 10 small medals, 3 ether antibodies, and 30 love potions.",
        system_message_jp="【システム】称号『屑肉（Scrap）』を獲得しました。フィート【闘志】Lv1（活力+5）を習得！",
        system_message_en="[System] Title 'Scrap' acquired. Feat 'Arena Spirit' Lv1 (Vigor+5) obtained!",
    ),
    "F": RankReward(
        items=[
            RewardItem("medal", 20),
            RewardItem("1165", 6),
            RewardItem("lovepotion", 60),
        ],
        feat_level=2,
        rank_value=2,
        quest_id=QuestIds.RANK_UP_F,
        message_jp="報酬として、小さなメダル20枚、エーテル抗体6本、媚薬60本をお渡しします。",
        message_en="As your reward, I present you with 20 small medals, 6 ether antibodies, and 60 love potions.",
        system_message_jp="【システム】称号『泥犬（Mud Dog）』を獲得しました。フィート【闘志】Lv2（活力+10）に成長！",
        system_message_en="[System] Title 'Mud Dog' acquired. Feat 'Arena Spirit' Lv2 (Vigor+10) obtained!",
    ),
    "E": RankReward(
        items=[
            RewardItem("medal", 30),
            RewardItem("1165", 9),
            RewardItem("lovepotion", 90),
        ],
        feat_level=3,
        rank_value=3,
        quest_id=QuestIds.RANK_UP_E,
        message_jp="報酬として、小さなメダル30枚、エーテル抗体9本、媚薬90本をお渡しします。",
        message_en="As your reward, I present you with 30 small medals, 9 ether antibodies, and 90 love potions.",
        system_message_jp="【システム】称号『鉄屑（Iron Scrap）』を獲得しました。フィート【闘志】Lv3（活力+15）に成長！",
        system_message_en="[System] Title 'Iron Scrap' acquired. Feat 'Arena Spirit' Lv3 (Vigor+15) obtained!",
    ),
    "D": RankReward(
        items=[
            RewardItem("medal", 40),
            RewardItem("1165", 12),
            RewardItem("lovepotion", 120),
        ],
        feat_level=4,
        rank_value=4,
        quest_id=QuestIds.RANK_UP_D,
        message_jp="報酬として、小さなメダル40枚、エーテル抗体12本、媚薬120本をお渡しします。",
        message_en="As your reward, I present you with 40 small medals, 12 ether antibodies, and 120 love potions.",
        system_message_jp="【システム】称号『銅貨稼ぎ（Copper Earner）』を獲得しました。フィート【闘志】Lv4（活力+20）に成長！",
        system_message_en="[System] Title 'Copper Earner' acquired. Feat 'Arena Spirit' Lv4 (Vigor+20) obtained!",
    ),
    "C": RankReward(
        items=[
            RewardItem("medal", 50),
            RewardItem("1165", 15),
            RewardItem("lovepotion", 150),
        ],
        feat_level=5,
        rank_value=5,
        quest_id=QuestIds.RANK_UP_C,
        message_jp="報酬として、小さなメダル50枚、エーテル抗体15本、媚薬150本をお渡しします。",
        message_en="As your reward, I present you with 50 small medals, 15 ether antibodies, and 150 love potions.",
        system_message_jp="【システム】称号『闘技場の鴉（Arena Crow）』を獲得しました。フィート【闘志】Lv5（活力+25）に成長！",
        system_message_en="[System] Title 'Arena Crow' acquired. Feat 'Arena Spirit' Lv5 (Vigor+25) obtained!",
    ),
    "B": RankReward(
        items=[
            RewardItem("medal", 60),
            RewardItem("1165", 18),
            RewardItem("lovepotion", 180),
        ],
        feat_level=6,
        rank_value=6,
        quest_id=QuestIds.RANK_UP_B,
        message_jp="報酬として、小さなメダル60枚、エーテル抗体18本、媚薬180本をお渡しします。",
        message_en="As your reward, I present you with 60 small medals, 18 ether antibodies, and 180 love potions.",
        system_message_jp="【システム】称号『銀翼（Silver Wing）』を獲得しました。フィート【闘志】Lv6（活力+30）に成長！",
        system_message_en="[System] Title 'Silver Wing' acquired. Feat 'Arena Spirit' Lv6 (Vigor+30) obtained!",
    ),
    "A": RankReward(
        items=[
            RewardItem("medal", 70),
            RewardItem("1165", 21),
            RewardItem("lovepotion", 210),
        ],
        feat_level=7,
        rank_value=7,
        quest_id=QuestIds.RANK_UP_A,
        message_jp="報酬として、小さなメダル70枚、エーテル抗体21本、媚薬210本をお渡しします。",
        message_en="As your reward, I present you with 70 small medals, 21 ether antibodies, and 210 love potions.",
        system_message_jp="【システム】称号『戦鬼（War Demon）』を獲得しました。フィート【闘志】Lv7（活力+40）に成長！",
        system_message_en="[System] Title 'War Demon' acquired. Feat 'Arena Spirit' Lv7 (Vigor+40) obtained!",
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

        # feat_level が設定されている場合、system_message_jp も必要
        if reward.feat_level > 0 and not reward.system_message_jp:
            errors.append(f"{prefix}: feat_level が設定されていますが system_message_jp がありません")

        # feat_level が rank_value と一致しているか
        if reward.feat_level != reward.rank_value:
            errors.append(f"{prefix}: feat_level ({reward.feat_level}) と rank_value ({reward.rank_value}) が一致しません")

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
        feat_str = f"Lv{reward.feat_level}" if reward.feat_level > 0 else "none"
        print(f"Rank {rank}: rank_value={reward.rank_value}, items=[{items_str}], feat={feat_str}")
