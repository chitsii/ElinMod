"""
00_zek.py - ゼク（怪しい商人）のメインダイアログ
NPCクリック時の会話処理
"""

from arena_drama_builder import ArenaDramaBuilder
from drama_constants import DramaNames
from flag_definitions import Keys, Actors, QuestIds


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
    pre_greeting = builder.label("pre_greeting")
    quest_notice = builder.label("quest_notice")
    check_quests = builder.label("check_quests")
    quest_none = builder.label("quest_none")
    greeting = builder.label("greeting")
    end = builder.label("end")

    # クエスト開始ラベル
    start_zek_intro = builder.label("start_zek_intro")
    start_zek_steal_bottle = builder.label("start_zek_steal_bottle")
    start_zek_steal_soulgem = builder.label("start_zek_steal_soulgem")

    # ========================================
    # エントリーポイント
    # ========================================
    builder.step(main).jump(pre_greeting)

    # ========================================
    # クエストチェック
    # ========================================
    builder.step(pre_greeting) \
        .check_available_quests_for_npc("sukutsu_shady_merchant") \
        .branch_if("sukutsu_available_quest_count", ">", 0, quest_notice) \
        .jump(greeting)

    # ========================================
    # クエスト通知
    # ========================================
    builder.step(quest_notice) \
        .say("quest_notice", "おや、{pcname}殿……。ちょうど良いところにお越しになりました。", "", actor=zek) \
        .say("quest_notice2", "少々、お耳に入れたい話がございまして……。", "", actor=zek) \
        .choice(check_quests, "話を聞く", "", text_id="c_hear") \
        .choice(greeting, "後にする", "", text_id="c_later") \
        .on_cancel(greeting)

    # ========================================
    # クエスト一覧表示
    # ========================================
    # sukutsu_quest_target_name: 21=intro, 23=bottle, 24=soulgem
    zek_quest_cases = [quest_none] * 21  # 0-20: fallback
    zek_quest_cases.append(start_zek_intro)       # 21
    zek_quest_cases.append(quest_none)            # 22: 未使用
    zek_quest_cases.append(start_zek_steal_bottle)  # 23
    zek_quest_cases.append(start_zek_steal_soulgem) # 24
    zek_quest_cases.append(quest_none)            # 末尾fallback

    builder.step(check_quests) \
        .say("quest_intro", "では、耳をお貸しください……。", "", actor=zek) \
        .set_flag("sukutsu_quest_found", 0) \
        .set_flag("sukutsu_quest_target_name", 0) \
        .debug_log_quests() \
        .check_quests([
            (QuestIds.ZEK_INTRO, "start_zek_intro"),
            (QuestIds.ZEK_STEAL_BOTTLE, "start_zek_steal_bottle"),
            (QuestIds.ZEK_STEAL_SOULGEM, "start_zek_steal_soulgem"),
        ]) \
        .switch_flag("sukutsu_quest_target_name", zek_quest_cases)

    # クエストが見つからなかった場合
    builder.step(quest_none) \
        .say("quest_none", "……おや、勘違いだったようです。失礼いたしました。", "", actor=zek) \
        .jump(greeting)

    # ゼク初対面: クエスト開始 + ドラマ遷移（高レベルAPI使用）
    builder.step(start_zek_intro) \
        .start_quest_drama(QuestIds.ZEK_INTRO, DramaNames.ZEK_INTRO)

    # 器すり替え: クエスト開始 + ドラマ遷移
    builder.step(start_zek_steal_bottle) \
        .start_quest_drama(QuestIds.ZEK_STEAL_BOTTLE, DramaNames.ZEK_STEAL_BOTTLE)

    # カイン魂の選択: クエスト開始 + ドラマ遷移
    builder.step(start_zek_steal_soulgem) \
        .start_quest_drama(QuestIds.ZEK_STEAL_SOULGEM, DramaNames.ZEK_STEAL_SOULGEM)

    # ========================================
    # 通常挨拶
    # ========================================
    builder.step(greeting) \
        .say("greet", "ふふ……何か御用でしょうか？", "", actor=zek) \
        .choice(end, "また今度", "", text_id="c_bye") \
        .on_cancel(end)

    # ========================================
    # 終了
    # ========================================
    builder.step(end).finish()
