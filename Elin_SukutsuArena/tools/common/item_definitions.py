# -*- coding: utf-8 -*-
"""
item_definitions.py - カスタムアイテム定義

宣言的なアイテム定義を提供し、SourceThing.xlsx を自動生成する。
rewards.py の RewardItem パターンを参考に設計。
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum


class TraitType(Enum):
    """Trait種別"""
    VANILLA = "vanilla"       # バニラTrait使用
    CUSTOM = "custom"         # カスタムTrait（TraitSukutsuItem使用）


@dataclass
class ItemEffect:
    """アイテム効果定義"""
    # 一時バフ
    buff_element_id: Optional[int] = None  # 951=resCold など
    buff_value: int = 0
    buff_duration_power: int = 100  # 持続時間計算用

    # カルマ変動
    karma_change: int = 0

    # 永続効果（ModBase）
    permanent_stats: Dict[int, int] = field(default_factory=dict)


@dataclass
class ItemDefinition:
    """
    アイテム定義

    SourceThing の各カラムに対応するフィールドを持つ。
    """
    # 基本情報 (必須)
    id: str                    # id（ユニーク識別子）
    name_jp: str               # name_JP
    name_en: str               # name
    category: str              # category（drink, amulet, ring, armor など）

    # 表示
    detail_jp: str = ""        # detail_JP
    detail_en: str = ""        # detail

    # Trait設定
    trait_type: TraitType = TraitType.VANILLA
    trait_name: str = "Drink"  # trait - Trait名
    trait_params: List[str] = field(default_factory=list)  # trait パラメータ

    # 効果（カスタムTraitの場合に使用）
    effect: Optional[ItemEffect] = None

    # エレメント（装備エンチャント/フィート付与）
    # 形式: "alias/value,alias/value,..." (例: "featHeavyEater/1,r_life/10")
    elements: str = ""

    # ゲームデータ
    value: int = 100           # value（売却価格）
    lv: int = 1                # LV
    weight: int = 100          # weight (1/1000単位、100=0.1kg)

    # レンダリング
    tiles: int = 0             # tiles（スプライトID）
    render_data: str = "item"  # _idRenderData

    # タグ
    tags: List[str] = field(default_factory=list)  # tag

    # 販売情報
    sell_at: Optional[str] = None  # 販売NPCのID
    stock_rarity: str = "Normal"   # 在庫のレアリティ
    stock_num: int = 1             # 在庫数
    stock_restock: bool = True     # 補充するか


# ============================================================================
# アイテム定義
# ============================================================================

CUSTOM_ITEMS: Dict[str, ItemDefinition] = {
    # ========================================
    # 万難のエリクサー（Elixir of Trials）- 複合耐性
    # ========================================
    "sukutsu_kiss_of_inferno": ItemDefinition(
        id="sukutsu_kiss_of_inferno",
        name_jp="万難のエリクサー",
        name_en="Elixir of Trials",
        category="drink",
        detail_jp="あらゆる困難を退ける禁断の霊薬。複数の耐性を長時間得られるが、魂を代償に捧げる。",
        detail_en="A forbidden elixir that wards off all trials. Grants multiple resistances, but demands your soul.",

        trait_type=TraitType.CUSTOM,
        trait_name="SukutsuItem",
        trait_params=["kiss_of_inferno"],

        effect=ItemEffect(
            karma_change=-50,
        ),

        value=50000,
        lv=30,
        weight=50,
        tiles=176,

        tags=["neg"],

        sell_at="sukutsu_shady_merchant",
        stock_rarity="Artifact",
        stock_num=3,
        stock_restock=True,
    ),

    # ========================================
    # 個別耐性ポーション
    # ========================================

    # 冷気耐性
    "sukutsu_frost_ward": ItemDefinition(
        id="sukutsu_frost_ward",
        name_jp="凍牙の護り",
        name_en="Frostfang Ward",
        category="drink",
        detail_jp="氷のような冷たさを持つ青い薬。冷気への耐性を得る。",
        detail_en="A blue potion cold as ice. Grants resistance to cold.",

        trait_type=TraitType.CUSTOM,
        trait_name="SukutsuItem",
        trait_params=["frost_ward"],

        effect=ItemEffect(
            buff_element_id=951,  # resCold
            karma_change=-15,
        ),

        value=30000,
        lv=10,
        weight=50,
        tiles=176,

        tags=["neg"],

        sell_at="sukutsu_shady_merchant",
        stock_rarity="Artifact",
        stock_num=5,
        stock_restock=True,
    ),

    # 幻惑耐性
    "sukutsu_mind_ward": ItemDefinition(
        id="sukutsu_mind_ward",
        name_jp="明鏡の護り",
        name_en="Clarity Ward",
        category="drink",
        detail_jp="澄んだ銀色の薬。幻惑への耐性を得る。",
        detail_en="A clear silver potion. Grants resistance to darkness/blindness.",

        trait_type=TraitType.CUSTOM,
        trait_name="SukutsuItem",
        trait_params=["mind_ward"],

        effect=ItemEffect(
            buff_element_id=953,  # resDarkness
            karma_change=-15,
        ),

        value=30000,
        lv=10,
        weight=50,
        tiles=176,

        tags=["neg"],

        sell_at="sukutsu_shady_merchant",
        stock_rarity="Artifact",
        stock_num=5,
        stock_restock=True,
    ),

    # 混沌耐性
    "sukutsu_chaos_ward": ItemDefinition(
        id="sukutsu_chaos_ward",
        name_jp="秩序の護り",
        name_en="Order Ward",
        category="drink",
        detail_jp="虹色に揺らめく不思議な薬。混沌への耐性を得る。",
        detail_en="A potion shimmering with rainbow colors. Grants resistance to chaos.",

        trait_type=TraitType.CUSTOM,
        trait_name="SukutsuItem",
        trait_params=["chaos_ward"],

        effect=ItemEffect(
            buff_element_id=959,  # resChaos
            karma_change=-15,
        ),

        value=30000,
        lv=10,
        weight=50,
        tiles=176,

        tags=["neg"],

        sell_at="sukutsu_shady_merchant",
        stock_rarity="Artifact",
        stock_num=5,
        stock_restock=True,
    ),

    # 轟音耐性
    "sukutsu_sound_ward": ItemDefinition(
        id="sukutsu_sound_ward",
        name_jp="静寂の護り",
        name_en="Silence Ward",
        category="drink",
        detail_jp="飲むと耳鳴りがする黄色い薬。轟音への耐性を得る。",
        detail_en="A yellow potion that causes ringing in the ears. Grants resistance to sound.",

        trait_type=TraitType.CUSTOM,
        trait_name="SukutsuItem",
        trait_params=["sound_ward"],

        effect=ItemEffect(
            buff_element_id=957,  # resSound
            karma_change=-15,
        ),

        value=30000,
        lv=10,
        weight=50,
        tiles=176,

        tags=["neg"],

        sell_at="sukutsu_shady_merchant",
        stock_rarity="Artifact",
        stock_num=5,
        stock_restock=True,
    ),

    # 衝撃耐性
    "sukutsu_impact_ward": ItemDefinition(
        id="sukutsu_impact_ward",
        name_jp="鋼鉄の護り",
        name_en="Steel Ward",
        category="drink",
        detail_jp="鉄錆の味がする灰色の薬。衝撃への耐性を得る。",
        detail_en="A gray potion tasting of iron rust. Grants resistance to impact.",

        trait_type=TraitType.CUSTOM,
        trait_name="SukutsuItem",
        trait_params=["impact_ward"],

        effect=ItemEffect(
            buff_element_id=965,  # resImpact
            karma_change=-15,
        ),

        value=30000,
        lv=10,
        weight=50,
        tiles=176,

        tags=["neg"],

        sell_at="sukutsu_shady_merchant",
        stock_rarity="Artifact",
        stock_num=5,
        stock_restock=True,
    ),

    # 出血耐性
    "sukutsu_bleed_ward": ItemDefinition(
        id="sukutsu_bleed_ward",
        name_jp="凝血の護り",
        name_en="Clotting Ward",
        category="drink",
        detail_jp="血のように赤黒い薬。出血への耐性を得る。",
        detail_en="A dark red potion like blood. Grants resistance to bleeding.",

        trait_type=TraitType.CUSTOM,
        trait_name="SukutsuItem",
        trait_params=["bleed_ward"],

        effect=ItemEffect(
            buff_element_id=964,  # resCut
            karma_change=-15,
        ),

        value=30000,
        lv=10,
        weight=50,
        tiles=176,

        tags=["neg"],

        sell_at="sukutsu_shady_merchant",
        stock_rarity="Artifact",
        stock_num=5,
        stock_restock=True,
    ),

    # ========================================
    # 怪しい装備品 - elements 付与系
    # ========================================

    # 飢餓の首飾り - 大食いフィート付与
    "sukutsu_hunger_amulet": ItemDefinition(
        id="sukutsu_hunger_amulet",
        name_jp="飢餓の首飾り",
        name_en="Amulet of Hunger",
        category="amulet",
        detail_jp="装備者の食欲を異常なまでに刺激する呪われた首飾り。常に腹が減る。",
        detail_en="A cursed amulet that stimulates abnormal appetite. Always hungry.",

        trait_type=TraitType.VANILLA,
        trait_name="",  # 装備品は通常Traitなし

        elements="featHeavyEater/1",

        value=40000,
        lv=15,
        weight=50,
        tiles=1168,  # amulet sprite

        tags=["neg"],

        sell_at="sukutsu_shady_merchant",
        stock_rarity="Artifact",
        stock_num=1,
        stock_restock=True,
    ),

    # 儚き天禀 - マナ特化（生命力10%, マナ200%）
    "sukutsu_ephemeral_gift": ItemDefinition(
        id="sukutsu_ephemeral_gift",
        name_jp="儚き天禀",
        name_en="Ephemeral Gift",
        category="ring",
        detail_jp="魔力を増幅する代わりに生命力を奪う指輪。ガラス細工のように繊細。",
        detail_en="A ring that amplifies mana at the cost of vitality. Delicate as glass.",

        trait_type=TraitType.VANILLA,
        trait_name="",

        elements="r_life/10,r_mana/200",

        value=50000,
        lv=25,
        weight=10,
        tiles=1184,  # ring sprite

        tags=["neg"],

        sell_at="sukutsu_shady_merchant",
        stock_rarity="Artifact",
        stock_num=1,
        stock_restock=True,
    ),

    # 愚者の平穏 - 生命力特化（生命力200%, マナ10%）
    "sukutsu_fools_peace": ItemDefinition(
        id="sukutsu_fools_peace",
        name_jp="愚者の平穏",
        name_en="Fool's Peace",
        category="ring",
        detail_jp="頑強な肉体を与える代わりに魔力を封じる指輪。知らぬが仏。",
        detail_en="A ring that grants robust health but seals magical power. Ignorance is bliss.",

        trait_type=TraitType.VANILLA,
        trait_name="",

        elements="r_life/200,r_mana/10",

        value=50000,
        lv=25,
        weight=10,
        tiles=1184,  # ring sprite

        tags=["neg"],

        sell_at="sukutsu_shady_merchant",
        stock_rarity="Artifact",
        stock_num=1,
        stock_restock=True,
    ),

    # ========================================
    # カスタム効果が必要なアイテム（C#実装待ち）
    # ========================================

    # 痛覚遮断薬 - 物理ダメージ軽減40% + 強力な毒
    "sukutsu_painkiller": ItemDefinition(
        id="sukutsu_painkiller",
        name_jp="痛覚遮断薬",
        name_en="Painkiller",
        category="drink",
        detail_jp="痛みを感じなくなる危険な薬。物理ダメージを40%軽減するが、強烈な毒に侵される。",
        detail_en="A dangerous drug that numbs pain. Reduces physical damage by 40%, but causes severe poisoning.",

        trait_type=TraitType.CUSTOM,
        trait_name="SukutsuItem",
        trait_params=["painkiller"],

        effect=ItemEffect(karma_change=-10),

        value=30000,
        lv=20,
        weight=50,
        tiles=176,

        tags=["neg"],

        sell_at="sukutsu_shady_merchant",
        stock_rarity="Artifact",
        stock_num=3,
        stock_restock=True,
    ),

    # 禁断の覚醒剤 - ブースト状態 + 後遺症として強力な出血
    "sukutsu_stimulant": ItemDefinition(
        id="sukutsu_stimulant",
        name_jp="禁断の覚醒剤",
        name_en="Forbidden Stimulant",
        category="drink",
        detail_jp="極限まで神経を研ぎ澄ます禁断の薬。ブースト状態になるが、効果が切れると血管が破裂する。",
        detail_en="A forbidden drug that sharpens nerves to the limit. Grants Boost, but causes severe bleeding when it wears off.",

        trait_type=TraitType.CUSTOM,
        trait_name="SukutsuItem",
        trait_params=["stimulant"],

        effect=ItemEffect(karma_change=-15),

        value=40000,
        lv=30,
        weight=50,
        tiles=176,

        tags=["neg"],

        sell_at="sukutsu_shady_merchant",
        stock_rarity="Artifact",
        stock_num=2,
        stock_restock=True,
    ),

    # 虚飾の黄金鎧 - HPダメージの代わりに所持金喪失、速度-60
    "sukutsu_gilded_armor": ItemDefinition(
        id="sukutsu_gilded_armor",
        name_jp="虚飾の黄金鎧",
        name_en="Gilded Vanity Armor",
        category="armor",
        detail_jp="金箔で覆われた見た目だけの鎧。物理ダメージを受けると所持金が剥がれ落ちる。",
        detail_en="Armor covered in gold leaf. Physical damage costs gold instead of HP.",

        trait_type=TraitType.CUSTOM,
        trait_name="SukutsuGildedArmor",
        trait_params=[],

        effect=ItemEffect(),
        elements="SPD/-60",  # 速度-60

        value=80000,
        lv=30,
        weight=5000,  # 重い
        tiles=1056,

        tags=["neg"],

        sell_at="sukutsu_shady_merchant",
        stock_rarity="Artifact",
        stock_num=1,
        stock_restock=True,
    ),

    # 双子の鏡 - 装備時に影の自己を召喚
    "sukutsu_twin_mirror": ItemDefinition(
        id="sukutsu_twin_mirror",
        name_jp="双子の鏡",
        name_en="Twin Mirror",
        category="amulet",
        detail_jp="鏡に映る自分の影が実体化して付き従う。外すと消える。",
        detail_en="Your reflection in the mirror materializes as a minion. Vanishes when removed.",

        trait_type=TraitType.CUSTOM,
        trait_name="SukutsuTwinMirror",
        trait_params=[],

        effect=ItemEffect(),

        value=80000,
        lv=35,
        weight=100,
        tiles=1168,

        tags=["neg"],

        sell_at="sukutsu_shady_merchant",
        stock_rarity="Artifact",
        stock_num=1,
        stock_restock=True,
    ),
}


# ============================================================================
# 効果IDマッピング（C#側で参照用のドキュメント）
# ============================================================================

EFFECT_DEFINITIONS = {
    "kiss_of_inferno": {
        "description": "業火の接吻 - 冷気耐性バフ + カルマ減少",
        "buff_element": 951,  # resCold
        "buff_value": 20,
        "buff_power": 500,
        "karma": -30,
    },
}


# ============================================================================
# バリデーション
# ============================================================================

def validate_items() -> List[str]:
    """アイテム定義のバリデーション"""
    errors = []

    for item_id, item in CUSTOM_ITEMS.items():
        prefix = f"CUSTOM_ITEMS['{item_id}']"

        # ID一致チェック
        if item.id != item_id:
            errors.append(f"{prefix}: id が key と一致しません")

        # 必須フィールド
        if not item.name_jp:
            errors.append(f"{prefix}: name_jp が空です")
        if not item.name_en:
            errors.append(f"{prefix}: name_en が空です")

        # カスタムTraitの場合、effectが必要
        if item.trait_type == TraitType.CUSTOM and item.effect is None:
            errors.append(f"{prefix}: カスタムTraitですが effect が定義されていません")

        # 販売設定の整合性
        if item.sell_at and item.stock_rarity not in ["Normal", "Superior", "Legendary", "Mythical", "Artifact"]:
            errors.append(f"{prefix}: stock_rarity が不正です: {item.stock_rarity}")

    return errors


def get_items_by_seller(seller_id: str) -> List[ItemDefinition]:
    """特定のNPCが販売するアイテムを取得"""
    return [item for item in CUSTOM_ITEMS.values() if item.sell_at == seller_id]


if __name__ == "__main__":
    print("=== Item Definitions Validation ===\n")

    errors = validate_items()
    if errors:
        print("Errors found:")
        for error in errors:
            print(f"  - {error}")
        exit(1)
    else:
        print("All validations passed!")

    print(f"\nTotal items defined: {len(CUSTOM_ITEMS)}")
    for item_id, item in CUSTOM_ITEMS.items():
        print(f"  - {item_id}: {item.name_jp} ({item.name_en})")
        if item.effect:
            print(f"    Effect: element={item.effect.buff_element_id}, value={item.effect.buff_value}, karma={item.effect.karma_change}")
        if item.sell_at:
            print(f"    Sold by: {item.sell_at} ({item.stock_rarity}, x{item.stock_num})")
