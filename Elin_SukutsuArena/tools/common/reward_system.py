"""
reward_system.py - 共通報酬選択システム

3択固定報酬:
- エーテル抗体のポーション (ID: 1165)
- 媚薬 (ID: lovepotion)
- 小さなコイン (ID: money)

数量はクエストの進行度に応じて増加
"""

from drama_builder import DramaBuilder, ChoiceReaction
from flag_definitions import Actors


# 報酬アイテムID
class RewardItems:
    ETHER_ANTIBODY = "1165"       # エーテル抗体のポーション
    LOVE_POTION = "lovepotion"    # 媚薬
    SMALL_COIN = "money"          # 小さなコイン（オレン）


# 報酬数量の定義（クエスト進行度別）
# tier: (ether_antibody, love_potion, small_coin)
REWARD_TIERS = {
    1: (1, 3, 20),      # 序盤クエスト
    2: (2, 6, 40),      # Rank G-F
    3: (3, 9, 60),      # Rank E-D
    4: (5, 15, 100),    # Rank C-B
    5: (8, 24, 160),    # Rank A
    6: (10, 30, 200),   # 最終クエスト・隠しクエスト
}


def _gen_reward_code(item_id: str, count: int) -> str:
    """報酬アイテム生成のC#コードを生成"""
    if count == 1:
        return f'EClass.pc.Pick(ThingGen.Create("{item_id}"));'
    else:
        return f'for(int i=0; i<{count}; i++) {{ EClass.pc.Pick(ThingGen.Create("{item_id}")); }}'


def add_reward_choice(
    builder: DramaBuilder,
    tier: int,
    choice_label_prefix: str,
    after_reward_label: str,
    lily_actor=Actors.LILY,
    pc_actor=Actors.PC
):
    """
    3択報酬選択を追加

    Args:
        builder: DramaBuilder インスタンス
        tier: 報酬ティア (1-6)
        choice_label_prefix: 選択肢ラベルのプレフィックス
        after_reward_label: 報酬受け取り後にジャンプするラベル
        lily_actor: リリィのアクターID
        pc_actor: PCのアクターID
    """
    tier = max(1, min(6, tier))  # 1-6に制限
    ether_count, love_count, coin_count = REWARD_TIERS[tier]

    # 選択肢テキスト
    ether_text = f"エーテル抗体のポーション×{ether_count}"
    love_text = f"媚薬×{love_count}"
    coin_text = f"小さなコイン×{coin_count}"

    # 報酬生成コード
    ether_code = _gen_reward_code(RewardItems.ETHER_ANTIBODY, ether_count)
    love_code = _gen_reward_code(RewardItems.LOVE_POTION, love_count)
    coin_code = _gen_reward_code(RewardItems.SMALL_COIN, coin_count)

    # 選択肢ブロック
    builder.choice_block([
        ChoiceReaction(ether_text, text_id=f"{choice_label_prefix}_ether")
            .say(f"{choice_label_prefix}_ether_r", "エーテル病の治療薬ですね。賢明な選択です。", "", actor=lily_actor)
            .action("eval", param=ether_code)
            .say(f"{choice_label_prefix}_ether_sys", f"『エーテル抗体のポーション』×{ether_count}を受け取った。", "", actor=pc_actor)
            .jump(after_reward_label),
        ChoiceReaction(love_text, text_id=f"{choice_label_prefix}_love")
            .say(f"{choice_label_prefix}_love_r", "ふふ、卵の孵化にお使いですか？", "", actor=lily_actor)
            .action("eval", param=love_code)
            .say(f"{choice_label_prefix}_love_sys", f"『媚薬』×{love_count}を受け取った。", "", actor=pc_actor)
            .jump(after_reward_label),
        ChoiceReaction(coin_text, text_id=f"{choice_label_prefix}_coin")
            .say(f"{choice_label_prefix}_coin_r", "現金主義ですか。まぁ、実用的ではありますね。", "", actor=lily_actor)
            .action("eval", param=coin_code)
            .say(f"{choice_label_prefix}_coin_sys", f"『小さなコイン』×{coin_count}を受け取った。", "", actor=pc_actor)
            .jump(after_reward_label),
    ], label_prefix=choice_label_prefix)


def get_reward_tier_for_rank(rank: str) -> int:
    """
    ランクに応じた報酬ティアを取得

    Args:
        rank: "G", "F", "E", "D", "C", "B", "A", "S"

    Returns:
        報酬ティア (1-6)
    """
    rank_tiers = {
        "G": 2,
        "F": 2,
        "E": 3,
        "D": 3,
        "C": 4,
        "B": 4,
        "A": 5,
        "S": 6,
    }
    return rank_tiers.get(rank.upper(), 1)
