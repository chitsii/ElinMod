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
    chance: int = 0            # chance（0=ランダム生成対象外）

    # レンダリング
    tiles: int = 0             # tiles（スプライトID）
    render_data: str = "item"  # _idRenderData

    # 装備品用（鎧、武器など）
    def_mat: str = ""          # defMat（デフォルト素材: iron, gold など）
    tier_group: str = ""       # tierGroup（metal, wood など）
    defense: str = ""          # defense（防御値: "6,21" など）

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
        detail_jp="異端の錬金術師が生涯をかけて完成させた禁忌の霊薬。あらゆる災厄を退けるが、その代償として魂の一部を蝕む。術師は完成の日、自ら服用し、そのまま灰となった。",
        detail_en="A forbidden elixir perfected by a heretic alchemist over a lifetime. It wards off all calamities, but corrodes a part of the soul. On the day of completion, the alchemist drank it himself and turned to ash.",

        trait_type=TraitType.CUSTOM,
        trait_name="SukutsuItem",
        trait_params=["kiss_of_inferno"],

        effect=ItemEffect(
            karma_change=-50,
        ),

        value=50000,
        lv=30,
        weight=50,
        tiles=1551, # potion_alchemy	ポーション
        render_data="obj_S",

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
        detail_jp="北の凍土で採れる霜竜の血から精製された青き秘薬。飲めば身体の芯まで凍えるが、いかなる冷気も肌を刺すことはない。",
        detail_en="A blue elixir distilled from the blood of frost dragons found in the northern tundra. It chills to the bone, yet no cold can pierce the skin thereafter.",

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
        tiles=1614, # ポーション
        render_data="obj_S",

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
        detail_jp="真実のみを映す鏡を砕いて作られた銀の薬。飲めば全ての幻が剥がれ落ちる。だが、真実を見続けた者は皆、やがて己の目を抉り取ったという。",
        detail_en="A silver elixir made from a shattered mirror that reflected only truth. All illusions fall away upon drinking. Yet all who gazed upon truth unending eventually gouged out their own eyes.",

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
        tiles=1614, # ポーション
        render_data="obj_S",

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
        detail_jp="混沌の深淵を覗き込み、正気を失った賢者が遺した虹色の薬。秩序なき力を退けるが、その製法は狂気の書物にのみ記されている。",
        detail_en="A rainbow elixir left by a sage who gazed into the abyss of chaos and lost his mind. It repels the forces of disorder, though its recipe exists only in tomes of madness.",

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
        tiles=1614, # ポーション
        render_data="obj_S",

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
        detail_jp="雷神の落とした耳栓を溶かして作られたという黄金色の薬。一時的に聴覚が鈍るが、いかなる轟音も鼓膜を破ることはない。",
        detail_en="A golden potion said to be made from melted earplugs dropped by the thunder god. Hearing dulls temporarily, but no roar can burst the eardrums.",

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
        tiles=1614, # ポーション
        render_data="obj_S",

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
        detail_jp="鋼鉄の巨人の心臓から抽出された灰色の液体。飲めば全身が鉄のように硬くなり、いかなる衝撃も骨を砕くことはできない。",
        detail_en="A gray liquid extracted from the heart of a steel colossus. The body hardens like iron upon consumption, and no impact can shatter bone.",

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
        tiles=1614, # ポーション
        render_data="obj_S",

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
        detail_jp="不死の吸血鬼から採取した血を凝固させた赤黒い秘薬。飲めば傷口が瞬時に塞がり、いかなる刃も血を流させることはできない。",
        detail_en="A dark red elixir made from coagulated blood of an immortal vampire. Wounds close instantly, and no blade can draw blood.",

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
        tiles=1614, # ポーション
        render_data="obj_S",

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
        detail_jp="餓鬼道に堕ちた僧侶が首に掛けていた呪物。装備すると底なしの飢えに苛まれ、いくら食べても満たされることはない。僧侶は最期、己の腕を喰らったという。",
        detail_en="A cursed relic worn by a monk who fell into the realm of hungry ghosts. The wearer suffers endless hunger that cannot be sated. The monk is said to have devoured his own arms in the end.",

        trait_type=TraitType.VANILLA,
        trait_name="",  # 装備品は通常Traitなし

        elements="featHeavyEater/1",

        value=40000,
        lv=15,
        weight=50,
        tiles=1221,  # amulet_necklace	ネックレス
        render_data="obj_S flat",

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
        detail_jp="夭折した天才魔術師の指に嵌められていた硝子の指輪。魔力を極限まで高めるが、生命の炎を急速に燃やし尽くす。彼女は二十歳を迎えることなく灰となった。",
        detail_en="A glass ring found on the finger of a prodigy sorceress who died young. It amplifies magic to its limits but rapidly burns away the flame of life. She turned to ash before her twentieth year.",

        trait_type=TraitType.VANILLA,
        trait_name="",

        elements="r_life/-90,r_mana/200",

        value=50000,
        lv=25,
        weight=10,
        tiles=1219,  # aurora ring
        render_data="obj_S flat",

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
        detail_jp="魔法を恐れた愚かな王が鍛冶師に作らせた鉛の指輪。肉体を頑強にするが、一切の魔力を封じてしまう。王は魔術師の呪いから逃れたが、知恵までも失うこととなった。",
        detail_en="A leaden ring forged by a smith for a foolish king who feared magic. It grants robust flesh but seals all magical power. The king escaped the sorcerer's curse but lost his wisdom as well.",

        trait_type=TraitType.VANILLA,
        trait_name="",

        elements="r_life/200,r_mana/-90",

        value=50000,
        lv=25,
        weight=10,
        tiles=1219,  # aurora ring
        render_data="obj_S flat",

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
        detail_jp="拷問官が囚人に与えていた黒い薬。苦痛を遮断し肉体を守るが、臓腑を蝕む猛毒を含む。囚人たちは痛みを忘れたまま、静かに腐っていったという。",
        detail_en="A black drug given to prisoners by torturers. It blocks pain and protects the flesh, but contains a deadly poison that rots the organs. The prisoners forgot their pain and quietly decayed.",

        trait_type=TraitType.CUSTOM,
        trait_name="SukutsuItem",
        trait_params=["painkiller"],

        effect=ItemEffect(karma_change=-10),

        value=30000,
        lv=20,
        weight=50,
        tiles=1614, # ポーション
        render_data="obj_S",

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
        detail_jp="狂戦士たちが決死の戦いの前に服用した禁断の薬。神経を極限まで研ぎ澄ませるが、同時に血管が内側から破裂する。",
        detail_en="A forbidden drug taken by berserkers before battles to the death. It sharpens the nerves to their limit, but blood vessels rupture from within.",

        trait_type=TraitType.CUSTOM,
        trait_name="SukutsuItem",
        trait_params=["stimulant"],

        effect=ItemEffect(karma_change=-15),

        value=40000,
        lv=30,
        weight=50,
        tiles=1311,
        render_data="obj_S flat",

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
        category="torso",  # 胴装備（armorは親カテゴリ）
        detail_jp="かつて強欲な王が纏った呪われし黄金の鎧。その輝きは持ち主の富を喰らい、傷の代わりに金貨を剥ぎ取る。王は最期、一枚の金貨も残さず骸と化したという。",
        detail_en="A cursed golden armor once worn by a greedy king. Its radiance devours the wearer's wealth, shedding gold coins instead of blood. The king met his end as a penniless corpse.",

        trait_type=TraitType.CUSTOM,
        trait_name="SukutsuGildedArmor",
        trait_params=[],

        effect=ItemEffect(),
        elements="SPD/-60",  # 速度-60

        value=80000,
        lv=48,
        weight=7500,  # 重い
        tiles=1255,  # 重装鎧
        render_data="obj_S flat",  # 重装鎧と同じ
        def_mat="gold",  # 金
        tier_group="metal",
        defense="6,21",

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
        detail_jp="双子の魔女が互いを封じ込めた呪われた鏡。装備すると鏡の中からもう一人の自分が這い出し、主に付き従う。外せば影は鏡の中へ還る。",
        detail_en="A cursed mirror in which twin witches sealed each other. When worn, another self crawls out from the mirror to serve its master. Remove it, and the shadow returns within.",

        trait_type=TraitType.CUSTOM,
        trait_name="SukutsuTwinMirror",
        trait_params=[],

        effect=ItemEffect(),

        value=80000,
        lv=35,
        weight=100,
        tiles=1318, # 細工首輪
        render_data="obj_S flat",  # 細工首輪と同じ

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

# EFFECT_DEFINITIONS = {
#     "kiss_of_inferno": {
#         "description": "万難のエリクサー - 冷気耐性バフ + カルマ減少",
#         "buff_element": 951,  # resCold
#         "buff_value": 20,
#         "buff_power": 500,
#         "karma": -30,
#     },
# }


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
