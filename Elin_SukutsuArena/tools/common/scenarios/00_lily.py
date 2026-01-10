"""
00_lily.py - リリィ（受付嬢）のメインダイアログ
NPCクリック時の会話処理
"""

from arena_drama_builder import ArenaDramaBuilder
from drama_constants import DramaNames
from flag_definitions import Keys, Actors, QuestIds
from arena_high_level_api import QuestEntry, build_quest_dispatcher


# リリィのクエストエントリ定義
LILY_QUESTS = [
    QuestEntry(QuestIds.LILY_EXPERIMENT, 22, "start_lily_experiment"),
    QuestEntry(QuestIds.LILY_PRIVATE, 26, "start_lily_private"),
    QuestEntry(QuestIds.LILY_REAL_NAME, 31, "start_lily_real_name"),
]


def define_lily_main_drama(builder: ArenaDramaBuilder):
    """
    リリィのメインダイアログ
    NPCクリック時に表示される会話
    """
    # アクター登録
    pc = builder.register_actor(Actors.PC, "あなた", "You")
    lily = builder.register_actor(Actors.LILY, "リリィ", "Lily")

    # ラベル定義
    main = builder.label("main")
    greeting = builder.label("greeting")
    choices = builder.label("choices")
    check_quests = builder.label("check_quests")
    quest_none = builder.label("quest_none")
    end = builder.label("end")

    # ========================================
    # エントリーポイント → 挨拶
    # ========================================
    builder.step(main).jump(greeting)

    # ========================================
    # 挨拶
    # ========================================
    builder.step(greeting) \
        .say("greet", "いらっしゃいませ。何かお手伝いできることはありますか？", "", actor=lily) \
        .jump(choices)

    # ========================================
    # 選択肢
    # ========================================
    builder.step(choices) \
        .choice(builder.label("_buy"), "商品を見る", "", text_id="c_buy") \
        .choice(check_quests, "（イベントを開始）", "", text_id="c_event") \
        .choice(end, "また今度", "", text_id="c_bye") \
        .on_cancel(end)

    # ========================================
    # クエストディスパッチ（高レベルAPI使用）
    # ========================================
    quest_labels = build_quest_dispatcher(
        builder,
        LILY_QUESTS,
        entry_step=check_quests,
        fallback_step=quest_none,
        actor=lily,
    )

    # クエストが見つからなかった場合 → 選択肢に戻る
    builder.step(quest_none) \
        .say("quest_none", "……あら、今は特にお伝えすることがないみたいです。", "", actor=lily) \
        .jump(choices)

    # 各クエスト開始 → ドラマ遷移
    builder.step(quest_labels["start_lily_experiment"]) \
        .start_quest_drama(QuestIds.LILY_EXPERIMENT, DramaNames.LILY_EXPERIMENT)

    builder.step(quest_labels["start_lily_private"]) \
        .start_quest_drama(QuestIds.LILY_PRIVATE, DramaNames.LILY_PRIVATE)

    builder.step(quest_labels["start_lily_real_name"]) \
        .start_quest_drama(QuestIds.LILY_REAL_NAME, DramaNames.LILY_REAL_NAME)

    # ========================================
    # 終了
    # ========================================
    builder.step(end).finish()
