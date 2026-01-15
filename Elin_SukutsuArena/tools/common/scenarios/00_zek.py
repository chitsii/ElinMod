"""
00_zek.py - ゼク（怪しい商人）のメインダイアログ
NPCクリック時の会話処理
"""

from arena_drama_builder import ArenaDramaBuilder
from drama_constants import DramaNames
from flag_definitions import Keys, Actors, QuestIds
from arena_types import QuestEntry


# ゼクのクエストエントリ定義
ZEK_QUESTS = [
    QuestEntry(QuestIds.ZEK_INTRO, 21, "start_zek_intro"),
    QuestEntry(QuestIds.ZEK_STEAL_BOTTLE, 23, "start_zek_steal_bottle"),
    QuestEntry(QuestIds.ZEK_STEAL_SOULGEM, 24, "start_zek_steal_soulgem"),
    QuestEntry(QuestIds.LAST_BATTLE, 33, "start_last_battle"),
]


def define_zek_main_drama(builder: ArenaDramaBuilder):
    """
    ゼクのメインダイアログ
    NPCクリック時に表示される会話
    """
    # アクター登録
    pc = builder.register_actor(Actors.PC, "あなた", "You")
    zek = builder.register_actor(Actors.ZEK, "ゼク", "Zek")

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
        .say("greet", "おや……何か御用でしょうか？", "", actor=zek) \
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
    quest_labels = builder.build_quest_dispatcher(
        ZEK_QUESTS,
        entry_step=check_quests,
        fallback_step=quest_none,
        actor=zek,
    )

    # クエストが見つからなかった場合 → 選択肢に戻る
    builder.step(quest_none) \
        .say("quest_none", "……おや、今は特にお伝えすることがないようです。", "", actor=zek) \
        .jump(choices)

    # 各クエスト開始 → ドラマ遷移
    builder.step(quest_labels["start_zek_intro"]) \
        .start_quest_drama(QuestIds.ZEK_INTRO, DramaNames.ZEK_INTRO)

    builder.step(quest_labels["start_zek_steal_bottle"]) \
        .start_quest_drama(QuestIds.ZEK_STEAL_BOTTLE, DramaNames.ZEK_STEAL_BOTTLE)

    builder.step(quest_labels["start_zek_steal_soulgem"]) \
        .start_quest_drama(QuestIds.ZEK_STEAL_SOULGEM, DramaNames.ZEK_STEAL_SOULGEM)

    builder.step(quest_labels["start_last_battle"]) \
        .start_quest_drama(QuestIds.LAST_BATTLE, DramaNames.LAST_BATTLE)

    # ========================================
    # 終了
    # ========================================
    builder.step(end).finish()
