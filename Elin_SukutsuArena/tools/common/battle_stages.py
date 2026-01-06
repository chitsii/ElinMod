"""
Battle Stage Definitions
========================
各バトルステージの設定を定義

シナリオのランクアップ試練とデバッグ用バトルを定義
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
import json
import os


class Rarity(Enum):
    NORMAL = "Normal"
    SUPERIOR = "Superior"
    LEGENDARY = "Legendary"
    MYTHICAL = "Mythical"


class SpawnPosition(Enum):
    CENTER = "center"
    RANDOM = "random"
    FIXED = "fixed"


@dataclass
class GimmickConfig:
    """ギミック設定"""
    gimmick_type: str           # "audience_interference", "area_effect", etc.
    interval: float = 5.0       # 発動間隔（秒）
    damage: int = 15            # ダメージ量
    radius: int = 3             # 効果範囲
    start_delay: float = 3.0    # 開始遅延（秒）
    effect_name: str = "explosion"   # エフェクト名
    sound_name: str = "explosion"    # サウンド名
    # エスカレーション設定
    enable_escalation: bool = True      # エスカレーション有効
    escalation_rate: float = 0.9        # 間隔減少率（毎回掛け算）
    min_interval: float = 0.5           # 最小間隔（秒）
    max_radius: int = 8                 # 最大範囲
    radius_growth_interval: float = 30.0  # 範囲拡大間隔（秒）
    # アイテムドロップ設定
    enable_item_drop: bool = True       # アイテムドロップ有効
    item_drop_chance: float = 0.15      # ドロップ確率（15%）
    # 命中率設定
    blast_radius: int = 2               # 爆発範囲（この範囲内にダメージ）
    direct_hit_chance: float = 0.4      # プレイヤー直撃確率（40%）
    explosion_count: int = 1            # 同時爆発数

    def to_dict(self) -> Dict[str, Any]:
        return {
            "gimmickType": self.gimmick_type,
            "interval": self.interval,
            "damage": self.damage,
            "radius": self.radius,
            "startDelay": self.start_delay,
            "effectName": self.effect_name,
            "soundName": self.sound_name,
            "enableEscalation": self.enable_escalation,
            "escalationRate": self.escalation_rate,
            "minInterval": self.min_interval,
            "maxRadius": self.max_radius,
            "radiusGrowthInterval": self.radius_growth_interval,
            "enableItemDrop": self.enable_item_drop,
            "itemDropChance": self.item_drop_chance,
            "blastRadius": self.blast_radius,
            "directHitChance": self.direct_hit_chance,
            "explosionCount": self.explosion_count,
        }


@dataclass
class EnemyConfig:
    """敵の設定"""
    chara_id: str               # SourceCharaのID
    level: int = 10             # レベル
    rarity: str = "Normal"      # Normal/Superior/Legendary/Mythical
    position: str = "random"    # center/random/fixed
    position_x: int = 0         # fixed時のX座標
    position_z: int = 0         # fixed時のZ座標
    is_boss: bool = False       # ボスフラグ（大きいHPバー表示）
    count: int = 1              # 同じ敵の数

    def to_dict(self) -> Dict[str, Any]:
        return {
            "charaId": self.chara_id,
            "level": self.level,
            "rarity": self.rarity,
            "position": self.position,
            "positionX": self.position_x,
            "positionZ": self.position_z,
            "isBoss": self.is_boss,
            "count": self.count,
        }


@dataclass
class BattleStage:
    """バトルステージの設定"""
    stage_id: str               # ユニークID
    display_name_jp: str        # 日本語表示名
    display_name_en: str        # 英語表示名
    zone_type: str = "field"    # マップタイプ
    bgm_battle: str = ""        # 戦闘BGM (空なら102)
    bgm_victory: str = ""       # 勝利BGM (空なら106)
    reward_plat: int = 10       # プラチナコイン報酬
    enemies: List[EnemyConfig] = field(default_factory=list)
    gimmicks: List[GimmickConfig] = field(default_factory=list)  # ギミック設定
    description_jp: str = ""    # 日本語説明
    description_en: str = ""    # 英語説明

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stageId": self.stage_id,
            "displayNameJp": self.display_name_jp,
            "displayNameEn": self.display_name_en,
            "zoneType": self.zone_type,
            "bgmBattle": self.bgm_battle,
            "bgmVictory": self.bgm_victory,
            "rewardPlat": self.reward_plat,
            "enemies": [e.to_dict() for e in self.enemies],
            "gimmicks": [g.to_dict() for g in self.gimmicks],
            "descriptionJp": self.description_jp,
            "descriptionEn": self.description_en,
        }


# ========================================
# ランクアップ試練の定義
# ========================================

RANK_UP_STAGES: Dict[str, BattleStage] = {
    # ========================================
    # 第1階層：【塵芥の徒】（レベル 1〜100）
    # 地上の冒険者としても駆け出し。バルガスからは「動く死体」扱いされる時期。
    # ========================================

    # ランクG昇格試験: 屑肉の洗礼
    "rank_g_trial": BattleStage(
        stage_id="rank_g_trial",
        display_name_jp="屑肉の洗礼",
        display_name_en="Baptism of Scrap Meat",
        zone_type="field",
        bgm_battle="",  # デフォルト戦闘BGM
        reward_plat=5,
        enemies=[
            # 最弱の試練：スライム系の群れ
            EnemyConfig("putty", level=15, count=3),
            EnemyConfig("putty", level=20, count=2),
        ],
        description_jp="「動く死体」から「屑肉」へ。これがお前の第一歩だ——バルガス",
        description_en="'From walking corpse to scrap meat. This is your first step.' —Balgas",
    ),

    # ランクF昇格試験: 泥犬の牙
    "rank_f_trial": BattleStage(
        stage_id="rank_f_trial",
        display_name_jp="泥犬の牙",
        display_name_en="Fangs of the Mud Dog",
        zone_type="field",
        bgm_battle="BGM/Battle_RankE_Ice",
        reward_plat=10,
        enemies=[
            # 次元の狭間に適応した獣：猟犬の群れ
            EnemyConfig("hound", level=40, rarity="Superior"),
            EnemyConfig("hound", level=45, rarity="Superior"),
            EnemyConfig("wolf", level=50, rarity="Superior", is_boss=True),
        ],
        description_jp="次元の狭間で変異した獣たち。群れで狩りをする本能は、異次元でも健在だ。",
        description_en="Beasts mutated in the dimensional void. Their pack hunting instincts remain intact even in other dimensions.",
    ),

    # ランクE昇格試験: 錆びついた英雄（カイン）
    # lore: カインは生前Lv.60、残留思念としてLv.40相当だが、ティア1最終関門として強化
    "rank_e_trial": BattleStage(
        stage_id="rank_e_trial",
        display_name_jp="錆びついた英雄",
        display_name_en="The Rusty Hero",
        zone_type="field",
        bgm_battle="BGM/Battle_Kain_Requiem",
        reward_plat=20,
        enemies=[
            # カイン：鉄血団の元副団長、バルガスが息子のように愛した存在
            # 今は記憶を失った残留思念として試練の番人を務める
            EnemyConfig("sukutsu_kain_ghost", level=90, rarity="Legendary", is_boss=True),
        ],
        description_jp="鉄血団の元副団長——バルガスが息子のように愛した男。今は記憶の大半を失い、戦闘本能だけが残った残留思念。",
        description_en="Former vice-captain of the Iron Blood Corps—the man Balgas loved like a son. Now a lingering soul with only combat instincts remaining.",
    ),

    # ========================================
    # 第2階層：【境界の戦士】（レベル 100〜1,000）
    # 異次元の環境に適応し始めた時期。ゼク（商人）が顔を出し始める。
    # ========================================

    # ランクD昇格試験: 銅貨稼ぎの洗礼（観客ギミック付き）
    "rank_d_trial": BattleStage(
        stage_id="rank_d_trial",
        display_name_jp="銅貨稼ぎの洗礼",
        display_name_en="Copper Earner's Baptism",
        zone_type="field",
        bgm_battle="BGM/Battle_RankD_Chaos",
        reward_plat=30,
        enemies=[
            # ミノタウロス：第2階層への入口として相応しい強敵
            EnemyConfig("minotaur", level=150, rarity="Superior", is_boss=True),
            # 取り巻きのオーク
            EnemyConfig("orc", level=120, rarity="Normal", count=2),
        ],
        gimmicks=[
            GimmickConfig(
                gimmick_type="audience_interference",
                interval=4.0,
                damage=25,              # ティア2相応のダメージ
                radius=3,
                start_delay=3.0,
                enable_escalation=True,
                escalation_rate=0.90,
                min_interval=0.8,
                max_radius=6,
                radius_growth_interval=30.0,
                enable_item_drop=True,
                item_drop_chance=0.12,
                blast_radius=2,
                direct_hit_chance=0.35,
                explosion_count=1,
            ),
        ],
        description_jp="観客の「注目」が初めて本格的に向けられる試練。その視線は時に物理的な力となって降り注ぐ。",
        description_en="The first trial where the audience's 'attention' truly focuses on you. Their gaze sometimes manifests as physical force.",
    ),

    # ランクC昇格試験: 闘技場の鴉
    "rank_c_trial": BattleStage(
        stage_id="rank_c_trial",
        display_name_jp="闘技場の鴉",
        display_name_en="Ravens of the Coliseum",
        zone_type="field",
        bgm_battle="BGM/Battle_RankC_Heroic_Lament",
        reward_plat=50,
        enemies=[
            # 「鴉」たち：かつての挑戦者だった者たちが番人として立ちはだかる
            # 多数の敵との乱戦
            EnemyConfig("orc_warrior", level=350, rarity="Superior", count=2),
            EnemyConfig("minotaur", level=400, rarity="Legendary"),
            EnemyConfig("centaur", level=450, rarity="Legendary", is_boss=True),
        ],
        description_jp="アリーナに巣食う「鴉」たち——かつての挑戦者だった者たちが、今は番人として立ちはだかる。",
        description_en="The 'Ravens' that nest in the arena—former challengers who now stand as guardians.",
    ),

    # ランクB昇格試験: 虚無の処刑人ヌル
    # lore: Nulは「神の孵化場」計画の失敗作、暗殺人形、アリーナの「清掃係」
    "rank_b_trial": BattleStage(
        stage_id="rank_b_trial",
        display_name_jp="虚無の処刑人",
        display_name_en="Void Executioner Null",
        zone_type="field",
        bgm_battle="BGM/Battle_Null_Assassin",
        reward_plat=80,
        enemies=[
            # ヌル：透明化する暗殺人形、「神の孵化場」計画の失敗作
            # 誰かの記憶の欠片が眠っている
            EnemyConfig("sukutsu_null", level=800, rarity="Mythical", is_boss=True),
        ],
        description_jp="「神の孵化場」計画の失敗作——暗殺人形ヌル。透明化し、一撃で仕留める。彼女の中には、素材となった誰かの記憶が眠っている。",
        description_en="A failure of the 'God Hatchery' project—the assassin doll Null. She turns invisible and kills in one strike. Memories of whoever became her material still slumber within.",
    ),

    # ========================================
    # 第3階層：【英雄の領域】（レベル 1,000〜10,000）
    # 地上では伝説級。リリィが事務的ではなく「一人の異性」として興味を持ち始める。
    # ========================================

    # ランクA昇格試験: 黄金の戦鬼（影の自己）
    "rank_a_trial": BattleStage(
        stage_id="rank_a_trial",
        display_name_jp="黄金の戦鬼",
        display_name_en="Golden War Demon",
        zone_type="field",
        bgm_battle="BGM/Battle_Shadow_Self",
        reward_plat=120,
        enemies=[
            # 影の自己：観客の「注目」がプレイヤーの影から生み出した存在
            # プレイヤーの全てを知り、全てを模倣する
            EnemyConfig("sukutsu_shadow_self", level=2500, rarity="Mythical", is_boss=True),
        ],
        description_jp="観客の「注目」が生み出した、お前自身の影。お前の全てを知り、お前の全てを模倣する——だが、お前には「成長」がある。",
        description_en="A shadow born from the audience's 'attention'—it knows everything about you. But unlike it, you can grow.",
    ),

    # ランクS昇格試験: 屠竜者への道（全盛期バルガス）
    # lore: バルガスは68歳、全盛期は30代前半でLv.120相当
    # 「若返りの薬」使用条件は「真に命を賭けた戦いの場」でのみ
    "rank_s_trial": BattleStage(
        stage_id="rank_s_trial",
        display_name_jp="屠竜者への道",
        display_name_en="Path to Dragon Slayer",
        zone_type="field",
        bgm_battle="BGM/Battle_Balgas_Prime",
        reward_plat=200,
        enemies=[
            # 全盛期バルガス：「若返りの薬」で30代の力を取り戻した鉄血団の団長
            # 200名を超える精鋭を率いた伝説の傭兵
            EnemyConfig("sukutsu_balgas_prime", level=8000, rarity="Mythical", is_boss=True),
        ],
        description_jp="「若返りの薬」を服用し、全盛期の力を取り戻したバルガス。かつて200名の精鋭を率い、竜すら屠った伝説の傭兵団長。",
        description_en="Balgas restored to his prime by the 'Rejuvenation Potion.' The legendary mercenary captain who once led 200 elites and slew dragons.",
    ),

    # ========================================
    # エンドコンテンツ：【次元深度（Void Depth）】
    # ========================================

    # 最終決戦: グランドマスター・アスタロト
    # lore: イルヴァの神々と同格の竜神、Lv.100,000,000（システム上限）
    # 滅びた次元「カラドリウス」の唯一の生存者、アリーナ創設者
    "final_astaroth": BattleStage(
        stage_id="final_astaroth",
        display_name_jp="竜神との対峙",
        display_name_en="Confrontation with the Dragon God",
        zone_type="field",
        bgm_battle="BGM/Battle_Astaroth_Phase1",
        bgm_victory="BGM/Final_Liberation",
        reward_plat=10000,
        enemies=[
            # アスタロト：イルヴァの神々と同格の竜神
            # 観客の「注目」を力に変換する術を会得
            # 真の目的は「神の孵化場」——神格に至る存在を生み出し、その力を吸収して新次元を創造する
            EnemyConfig("sukutsu_astaroth", level=50000, rarity="Mythical", is_boss=True),
        ],
        description_jp="イルヴァの神々と同格の竜神。滅びた次元「カラドリウス」の唯一の生存者。3,000年間、観客の「注目」を力に変え続けてきたアリーナの創造者にして支配者。",
        description_en="A dragon god on par with the gods of Ilva. The sole survivor of fallen 'Caladrius.' For 3,000 years, he has converted the audience's 'attention' into power—the creator and ruler of the arena.",
    ),
}


# ========================================
# 通常ステージの定義
# ========================================

NORMAL_STAGES: Dict[str, BattleStage] = {
    "stage_1": BattleStage(
        stage_id="stage_1",
        display_name_jp="森の狼",
        display_name_en="Forest Wolf",
        zone_type="field",
        reward_plat=10,
        enemies=[
            EnemyConfig("wolf", level=5),
        ],
    ),
    "stage_2": BattleStage(
        stage_id="stage_2",
        display_name_jp="ケンタウロス",
        display_name_en="Centaur",
        zone_type="field",
        reward_plat=20,
        enemies=[
            EnemyConfig("centaur", level=15, rarity="Superior"),
        ],
    ),
    "stage_3": BattleStage(
        stage_id="stage_3",
        display_name_jp="ミノタウロス",
        display_name_en="Minotaur",
        zone_type="field",
        reward_plat=30,
        enemies=[
            EnemyConfig("minotaur", level=25, rarity="Superior"),
        ],
    ),
    "stage_4": BattleStage(
        stage_id="stage_4",
        display_name_jp="竜との対峙",
        display_name_en="Dragon Confrontation",
        zone_type="field",
        reward_plat=50,
        enemies=[
            EnemyConfig("dragon", level=40, rarity="Legendary", is_boss=True),
        ],
    ),

    # 上位存在クエスト: 見えざる観客の供物
    "upper_existence_battle": BattleStage(
        stage_id="upper_existence_battle",
        display_name_jp="見えざる観客の供物",
        display_name_en="Offering to the Unseen Audience",
        zone_type="field",
        bgm_battle="BGM/Battle_Audience_Chaos",
        reward_plat=15,
        enemies=[
            # 異次元の剣闘士
            EnemyConfig("gladiator", level=100, rarity="Superior", is_boss=True),
            EnemyConfig("gladiator", level=80, count=2),
        ],
        gimmicks=[
            GimmickConfig(
                gimmick_type="audience_interference",
                interval=5.0,
                damage=20,
                radius=3,
                start_delay=3.0,
                enable_escalation=True,
                escalation_rate=0.92,
                min_interval=1.0,
                max_radius=5,
                radius_growth_interval=25.0,
                enable_item_drop=True,
                item_drop_chance=0.15,
                blast_radius=2,
                direct_hit_chance=0.35,
                explosion_count=1,
            ),
        ],
        description_jp="観客の「注目」が初めて向けられる戦い。彼らのヤジは物理的な力となって降り注ぐ。",
        description_en="The first battle where the audience's 'attention' focuses on you. Their jeers manifest as physical force.",
    ),
}


# ========================================
# デバッグ用ステージ（全ステージへのアクセス）
# ========================================

DEBUG_STAGES: Dict[str, BattleStage] = {
    **RANK_UP_STAGES,
    **NORMAL_STAGES,

    # デバッグ専用: 弱い敵
    "debug_weak": BattleStage(
        stage_id="debug_weak",
        display_name_jp="[DEBUG] 弱い敵",
        display_name_en="[DEBUG] Weak Enemy",
        zone_type="field",
        reward_plat=1,
        enemies=[
            EnemyConfig("putty", level=1),
        ],
        description_jp="デバッグ用：レベル1のパティ",
    ),

    # デバッグ専用: 強い敵
    "debug_strong": BattleStage(
        stage_id="debug_strong",
        display_name_jp="[DEBUG] 強い敵",
        display_name_en="[DEBUG] Strong Enemy",
        zone_type="field",
        reward_plat=100,
        enemies=[
            EnemyConfig("dragon", level=100, rarity="Mythical", is_boss=True),
        ],
        description_jp="デバッグ用：レベル100の神話級ドラゴン",
    ),

    # デバッグ専用: 複数敵
    "debug_horde": BattleStage(
        stage_id="debug_horde",
        display_name_jp="[DEBUG] 敵の群れ",
        display_name_en="[DEBUG] Enemy Horde",
        zone_type="field",
        reward_plat=50,
        enemies=[
            EnemyConfig("goblin", level=10, count=10),
        ],
        description_jp="デバッグ用：10体のゴブリン",
    ),

    # デバッグ専用: ギミックテスト
    "debug_gimmick": BattleStage(
        stage_id="debug_gimmick",
        display_name_jp="[DEBUG] ギミックテスト",
        display_name_en="[DEBUG] Gimmick Test",
        zone_type="field",
        reward_plat=10,
        enemies=[
            EnemyConfig("putty", level=5, count=3),
        ],
        gimmicks=[
            GimmickConfig(
                gimmick_type="audience_interference",
                interval=2.0,           # 初期間隔（秒）- 短め
                damage=10,              # 基本ダメージ
                radius=2,               # 初期範囲
                start_delay=1.0,        # 開始遅延
                # エスカレーション（激しめ設定）
                enable_escalation=True,
                escalation_rate=0.80,   # 20%ずつ間隔短縮
                min_interval=0.3,       # 最終的にほぼ毎ターン
                max_radius=10,          # 最大範囲
                radius_growth_interval=10.0,  # 10秒ごとに範囲拡大
                # アイテムドロップ
                enable_item_drop=True,
                item_drop_chance=0.20,  # 20%でアイテムドロップ
                # 命中率（高めに設定）
                blast_radius=3,         # 爆発範囲3マス
                direct_hit_chance=0.6,  # 60%で直撃
                explosion_count=2,      # 同時に2発
            ),
        ],
        description_jp="デバッグ用：高命中率ギミック確認",
        description_en="Debug: High hit rate gimmick test",
    ),
}


# ========================================
# JSON出力
# ========================================

def export_stages_to_json(output_path: str):
    """ステージ定義をJSONにエクスポート"""
    data = {
        "rankUpStages": {k: v.to_dict() for k, v in RANK_UP_STAGES.items()},
        "normalStages": {k: v.to_dict() for k, v in NORMAL_STAGES.items()},
        "debugStages": {k: v.to_dict() for k, v in DEBUG_STAGES.items()},
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Exported battle stages to: {output_path}")


def get_all_stage_ids() -> List[str]:
    """全ステージIDのリストを取得"""
    return list(DEBUG_STAGES.keys())


def get_stage(stage_id: str) -> Optional[BattleStage]:
    """ステージIDからステージ定義を取得"""
    return DEBUG_STAGES.get(stage_id)


if __name__ == "__main__":
    # テスト出力
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    output_path = os.path.join(project_root, 'Package', 'battle_stages.json')
    export_stages_to_json(output_path)

    print("\n=== Stage IDs ===")
    for stage_id in get_all_stage_ids():
        stage = get_stage(stage_id)
        print(f"  {stage_id}: {stage.display_name_jp}")
