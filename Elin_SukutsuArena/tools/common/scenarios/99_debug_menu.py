"""
99_debug_menu.py - 自動生成デバッグメニュー

全てのドラマとバトルステージへのアクセスを提供。
新しいドラマ/バトルを追加すると自動的にメニューに反映される。

自動化の仕組み:
- ドラマ: ALL_DRAMA_IDS + get_drama_category() で動的カテゴリ分け
- バトル: battle_stages.py の辞書から自動取得
"""

from drama_builder import DramaBuilder
from drama_constants import (
    DramaIds,
    ALL_DRAMA_IDS,
    get_drama_category,
    DRAMA_DISPLAY_NAMES,
)
from battle_stages import DEBUG_STAGES, RANK_UP_STAGES, NORMAL_STAGES
from flag_definitions import Actors, Keys, FlagValues


def _get_dramas_by_category():
    """
    ALL_DRAMA_IDSをカテゴリ別に分類して返す

    Returns:
        dict: {'story': [...], 'rank': [...], 'character': [...]}
    """
    categorized = {'story': [], 'rank': [], 'character': []}

    for drama_id in ALL_DRAMA_IDS:
        # デバッグメニュー自体とメインドラマは除外
        if drama_id in (DramaIds.DEBUG_MENU, DramaIds.SUKUTSU_ARENA_MASTER):
            continue
        category = get_drama_category(drama_id)
        categorized[category].append(drama_id)

    return categorized


def define_debug_menu(builder: DramaBuilder):
    """
    デバッグメニュー定義

    全ドラマ/バトルへのアクセスを自動生成
    """
    # アクター
    pc = builder.register_actor(Actors.PC, "あなた", "You")
    debug_master = builder.register_actor("sukutsu_debug_master", "観測者", "Observer")

    # メインラベル
    main = builder.label("main")
    main_menu = builder.label("main_menu")
    drama_menu = builder.label("drama_menu")
    battle_menu = builder.label("battle_menu")
    quest_menu = builder.label("quest_menu")
    items_menu = builder.label("items_menu")
    npc_menu = builder.label("npc_menu")
    flags_menu = builder.label("flags_menu")
    end = builder.label("end")

    # ドラマサブメニュー
    drama_story = builder.label("drama_story")
    drama_rank = builder.label("drama_rank")
    drama_char = builder.label("drama_char")

    # バトルサブメニュー
    battle_rank = builder.label("battle_rank")
    battle_normal = builder.label("battle_normal")
    battle_debug = builder.label("battle_debug")

    # ========================================
    # メイン
    # ========================================
    builder.step(main) \
        .say("debug_welcome", "デバッグメニューへようこそ。何をテストしますか？", "", actor=debug_master)

    builder.choice(drama_menu, "ドラマを再生", "", text_id="c_drama") \
           .choice(battle_menu, "バトルを開始", "", text_id="c_battle") \
           .choice(quest_menu, "クエスト操作", "", text_id="c_quest") \
           .choice(items_menu, "アイテム取得", "", text_id="c_items") \
           .choice(npc_menu, "NPC操作", "", text_id="c_npc") \
           .choice(flags_menu, "フラグ操作", "", text_id="c_flags") \
           .choice(end, "終了", "", text_id="c_end")

    # main_menu ステップ（戻る先）
    builder.step(main_menu) \
        .say("debug_main", "何をテストしますか？", "", actor=debug_master)

    builder.choice(drama_menu, "ドラマを再生", "", text_id="c_drama_2") \
           .choice(battle_menu, "バトルを開始", "", text_id="c_battle_2") \
           .choice(quest_menu, "クエスト操作", "", text_id="c_quest_2") \
           .choice(items_menu, "アイテム取得", "", text_id="c_items_2") \
           .choice(npc_menu, "NPC操作", "", text_id="c_npc_2") \
           .choice(flags_menu, "フラグ操作", "", text_id="c_flags_2") \
           .choice(end, "終了", "", text_id="c_end_2")

    # ========================================
    # ドラマメニュー（動的カテゴリ分け）
    # ========================================
    categorized_dramas = _get_dramas_by_category()

    builder.step(drama_menu) \
        .say("drama_cat", "ドラマカテゴリを選択してください。", "", actor=debug_master)

    builder.choice(drama_story, "ストーリー", "", text_id="c_drama_story") \
           .choice(drama_rank, "ランクアップ", "", text_id="c_drama_rank") \
           .choice(drama_char, "キャラクター", "", text_id="c_drama_char") \
           .choice(main_menu, "戻る", "", text_id="c_drama_back")

    # ストーリードラマ（自動取得）
    _build_drama_submenu(builder, drama_story, categorized_dramas['story'], drama_menu, debug_master)

    # ランクアップドラマ（自動取得）
    _build_drama_submenu(builder, drama_rank, categorized_dramas['rank'], drama_menu, debug_master)

    # キャラクタードラマ（自動取得）
    _build_drama_submenu(builder, drama_char, categorized_dramas['character'], drama_menu, debug_master)

    # ========================================
    # バトルメニュー（自動取得）
    # ========================================
    builder.step(battle_menu) \
        .say("battle_cat", "バトルカテゴリを選択してください。", "", actor=debug_master)

    builder.choice(battle_rank, "ランクアップ試練", "", text_id="c_battle_rank") \
           .choice(battle_normal, "通常バトル", "", text_id="c_battle_normal") \
           .choice(battle_debug, "デバッグバトル", "", text_id="c_battle_debug") \
           .choice(main_menu, "戻る", "", text_id="c_battle_back")

    # ランクアップバトル
    _build_battle_submenu(builder, battle_rank, RANK_UP_STAGES, battle_menu, debug_master)

    # 通常バトル
    _build_battle_submenu(builder, battle_normal, NORMAL_STAGES, battle_menu, debug_master)

    # デバッグバトル
    debug_only = {k: v for k, v in DEBUG_STAGES.items() if k.startswith("debug_")}
    _build_battle_submenu(builder, battle_debug, debug_only, battle_menu, debug_master)

    # ========================================
    # クエスト操作メニュー（新規）
    # ========================================
    quest_pet_unlock = builder.label("quest_pet_unlock")
    quest_rank_b = builder.label("quest_rank_b")
    quest_rank_a = builder.label("quest_rank_a")
    quest_all = builder.label("quest_all")
    quest_reset = builder.label("quest_reset")

    builder.step(quest_menu) \
        .say("quest_info", "クエスト進行を操作します。", "", actor=debug_master)

    builder.choice(quest_pet_unlock, "ペット解禁のみ", "", text_id="c_quest_pet") \
           .choice(quest_rank_b, "Bランク到達", "", text_id="c_quest_b") \
           .choice(quest_rank_a, "Aランク到達", "", text_id="c_quest_a") \
           .choice(quest_all, "全クエスト完了", "", text_id="c_quest_all") \
           .choice(quest_reset, "クエストリセット", "", text_id="c_quest_reset") \
           .choice(main_menu, "戻る", "", text_id="c_quest_back")

    builder.step(quest_pet_unlock) \
        .action("eval", param="Elin_SukutsuArena.DebugHelper.CompleteQuestsUpTo(\"18_last_battle\");") \
        .say("quest_pet_done", "18_last_battleまで完了しました。ペット化が解禁されました。", "", actor=debug_master) \
        .jump(quest_menu)

    builder.step(quest_rank_b) \
        .action("eval", param="Elin_SukutsuArena.DebugHelper.CompleteQuestsUpTo(\"12_rank_b_trial\");") \
        .say("quest_b_done", "Bランク到達まで完了しました。Nulが非表示になります。", "", actor=debug_master) \
        .jump(quest_menu)

    builder.step(quest_rank_a) \
        .action("eval", param="Elin_SukutsuArena.DebugHelper.CompleteQuestsUpTo(\"14_rank_a_trial\");") \
        .say("quest_a_done", "Aランク到達まで完了しました。", "", actor=debug_master) \
        .jump(quest_menu)

    builder.step(quest_all) \
        .action("eval", param="Elin_SukutsuArena.ArenaQuestManager.Instance.DebugCompleteAllQuests();") \
        .say("quest_all_done", "全クエストを完了しました。", "", actor=debug_master) \
        .jump(quest_menu)

    builder.step(quest_reset) \
        .action("eval", param="Elin_SukutsuArena.DebugHelper.ResetAllQuests();") \
        .say("quest_reset_done", "全クエストをリセットしました。", "", actor=debug_master) \
        .jump(quest_menu)

    # ========================================
    # アイテム取得メニュー
    # ========================================
    item_makuma2 = builder.label("item_makuma2")
    item_lily_exp = builder.label("item_lily_exp")
    item_plat = builder.label("item_plat")

    builder.step(items_menu) \
        .say("items_info", "クエスト用素材を取得します。", "", actor=debug_master)

    builder.choice(item_makuma2, "虚空の心臓素材（心臓+ルーンモールド）", "", text_id="c_item_makuma2") \
           .choice(item_lily_exp, "残響の器素材（骨）", "", text_id="c_item_lily_exp") \
           .choice(item_plat, "プラチナコイン×10", "", text_id="c_item_plat") \
           .choice(main_menu, "戻る", "", text_id="c_items_back")

    # makuma2素材: 心臓×1 + ルーンモールド×1
    builder.step(item_makuma2) \
        .cs_eval("EClass.pc.Pick(ThingGen.Create(\"heart\"));") \
        .cs_eval("EClass.pc.Pick(ThingGen.Create(\"rune_mold_earth\"));") \
        .say("item_makuma2_got", "心臓×1とルーンモールド（大地）×1を取得しました。", "", actor=debug_master) \
        .jump(items_menu)

    # lily_experiment素材: 骨×1
    builder.step(item_lily_exp) \
        .cs_eval("EClass.pc.Pick(ThingGen.Create(\"bone\"));") \
        .say("item_lily_exp_got", "骨×1を取得しました。", "", actor=debug_master) \
        .jump(items_menu)

    # プラチナコイン×10
    builder.step(item_plat) \
        .cs_eval("for(int i=0; i<10; i++) { EClass.pc.Pick(ThingGen.Create(\"plat\")); }") \
        .say("item_plat_got", "プラチナコイン×10を取得しました。", "", actor=debug_master) \
        .jump(items_menu)

    # ========================================
    # NPC操作メニュー（新規）
    # ========================================
    npc_status = builder.label("npc_status")
    npc_hide_nul = builder.label("npc_hide_nul")
    npc_hide_astaroth = builder.label("npc_hide_astaroth")
    npc_restore_all = builder.label("npc_restore_all")
    npc_bad_end = builder.label("npc_bad_end")
    npc_flag_status = builder.label("npc_flag_status")

    builder.step(npc_menu) \
        .say("npc_info", "NPC状態を操作します。", "", actor=debug_master)

    builder.choice(npc_status, "NPC状態確認", "", text_id="c_npc_status") \
           .choice(npc_hide_nul, "Nul非表示", "", text_id="c_npc_hide_nul") \
           .choice(npc_hide_astaroth, "Astaroth非表示", "", text_id="c_npc_hide_ast") \
           .choice(npc_restore_all, "全NPC再表示", "", text_id="c_npc_restore") \
           .choice(npc_bad_end, "バッドエンドシミュ", "", text_id="c_npc_bad") \
           .choice(npc_flag_status, "フラグ状態確認", "", text_id="c_npc_flags") \
           .choice(main_menu, "戻る", "", text_id="c_npc_back")

    builder.step(npc_status) \
        .action("eval", param="Elin_SukutsuArena.DebugHelper.ShowNpcStatus();") \
        .say("npc_status_done", "NPC状態をログに出力しました。", "", actor=debug_master) \
        .jump(npc_menu)

    builder.step(npc_hide_nul) \
        .action("eval", param="Elin_SukutsuArena.DebugHelper.HideNpc(\"sukutsu_null\");") \
        .say("npc_hide_nul_done", "Nulを非表示にしました。", "", actor=debug_master) \
        .jump(npc_menu)

    builder.step(npc_hide_astaroth) \
        .action("eval", param="Elin_SukutsuArena.DebugHelper.HideNpc(\"sukutsu_astaroth\");") \
        .say("npc_hide_ast_done", "Astarothを非表示にしました。", "", actor=debug_master) \
        .jump(npc_menu)

    builder.step(npc_restore_all) \
        .action("eval", param="Elin_SukutsuArena.DebugHelper.RestoreAllNpcs();") \
        .say("npc_restore_done", "全NPCをアリーナに再表示しました。", "", actor=debug_master) \
        .jump(npc_menu)

    builder.step(npc_bad_end) \
        .set_flag(Keys.BALGAS_KILLED, FlagValues.BalgasChoice.KILLED) \
        .set_flag(Keys.LILY_HOSTILE, FlagValues.TRUE) \
        .say("npc_bad_done", "バッドエンドフラグを設定しました（バルガス死亡+リリィ離反）", "", actor=debug_master) \
        .jump(npc_menu)

    builder.step(npc_flag_status) \
        .action("eval", param="Elin_SukutsuArena.DebugHelper.ShowFlagStatus();") \
        .say("npc_flag_done", "フラグ状態をログに出力しました。", "", actor=debug_master) \
        .jump(npc_menu)

    # ========================================
    # フラグ操作メニュー
    # ========================================
    set_rank_s = builder.label("set_rank_s")
    set_all_quests = builder.label("set_all_quests")
    scenario_flags = builder.label("scenario_flags")

    builder.step(flags_menu) \
        .say("flags_info", "フラグ操作を選択してください。", "", actor=debug_master)

    builder.choice(set_rank_s, "ランクSに設定", "", text_id="c_set_rank_s") \
           .choice(scenario_flags, "シナリオ分岐フラグ", "", text_id="c_scenario_flags") \
           .choice(main_menu, "戻る", "", text_id="c_flags_back")

    # ランクSに設定するには、全ランクアップクエストを完了させる
    builder.step(set_rank_s) \
        .action("eval", param="Elin_SukutsuArena.DebugHelper.SetRankS();") \
        .say("rank_set", "ランクをSに設定しました（全ランクアップクエスト完了）", "", actor=debug_master) \
        .jump(flags_menu)

    # ========================================
    # シナリオ分岐フラグメニュー
    # ========================================
    set_balgas_killed = builder.label("set_balgas_killed")
    set_balgas_alive = builder.label("set_balgas_alive")
    set_lily_hostile = builder.label("set_lily_hostile")
    set_lily_friendly = builder.label("set_lily_friendly")
    set_worst_case = builder.label("set_worst_case")
    reset_all_flags = builder.label("reset_all_flags")

    builder.step(scenario_flags) \
        .say("scenario_info", "シナリオ分岐フラグを設定します。", "", actor=debug_master)

    builder.choice(set_balgas_killed, "バルガス殺害ON", "", text_id="c_balgas_killed") \
           .choice(set_balgas_alive, "バルガス殺害OFF", "", text_id="c_balgas_alive") \
           .choice(set_lily_hostile, "リリィ離反ON", "", text_id="c_lily_hostile") \
           .choice(set_lily_friendly, "リリィ離反OFF", "", text_id="c_lily_friendly") \
           .choice(set_worst_case, "最悪ルート（両方ON）", "", text_id="c_worst_case") \
           .choice(reset_all_flags, "全てリセット", "", text_id="c_reset_flags") \
           .choice(flags_menu, "戻る", "", text_id="c_scenario_back")

    builder.step(set_balgas_killed) \
        .set_flag(Keys.BALGAS_KILLED, FlagValues.BalgasChoice.KILLED) \
        .say("balgas_killed_set", "バルガス殺害フラグをONにしました。", "", actor=debug_master) \
        .jump(scenario_flags)

    builder.step(set_balgas_alive) \
        .set_flag(Keys.BALGAS_KILLED, FlagValues.BalgasChoice.SPARED) \
        .say("balgas_alive_set", "バルガス殺害フラグをOFFにしました。", "", actor=debug_master) \
        .jump(scenario_flags)

    builder.step(set_lily_hostile) \
        .set_flag(Keys.LILY_HOSTILE, FlagValues.TRUE) \
        .say("lily_hostile_set", "リリィ離反フラグをONにしました。", "", actor=debug_master) \
        .jump(scenario_flags)

    builder.step(set_lily_friendly) \
        .set_flag(Keys.LILY_HOSTILE, FlagValues.FALSE) \
        .say("lily_friendly_set", "リリィ離反フラグをOFFにしました。", "", actor=debug_master) \
        .jump(scenario_flags)

    builder.step(set_worst_case) \
        .set_flag(Keys.BALGAS_KILLED, FlagValues.BalgasChoice.KILLED) \
        .set_flag(Keys.LILY_HOSTILE, FlagValues.TRUE) \
        .say("worst_case_set", "最悪ルート設定完了（バルガス殺害+リリィ離反）", "", actor=debug_master) \
        .jump(scenario_flags)

    builder.step(reset_all_flags) \
        .set_flag(Keys.BALGAS_KILLED, FlagValues.BalgasChoice.SPARED) \
        .set_flag(Keys.LILY_HOSTILE, FlagValues.FALSE) \
        .say("flags_reset", "全フラグをリセットしました。", "", actor=debug_master) \
        .jump(scenario_flags)

    # ========================================
    # 終了
    # ========================================
    builder.step(end) \
        .say("debug_bye", "デバッグメニューを終了します。", "", actor=debug_master) \
        .finish()


def _build_drama_submenu(builder: DramaBuilder, entry_label: str, drama_ids: list, back_label: str, actor):
    """ドラマサブメニューを構築"""
    menu_label = f"{entry_label}_choice"

    builder.step(entry_label) \
        .say(f"{entry_label}_msg", "再生するドラマを選択してください。", "", actor=actor) \
        .jump(menu_label)

    # 選択肢を構築
    choice_labels = []
    for drama_id in drama_ids:
        label = f"play_{drama_id}"
        jp_name, en_name = DRAMA_DISPLAY_NAMES.get(drama_id, (drama_id, drama_id))
        choice_labels.append((label, jp_name, en_name))

    # 最初の選択肢
    if choice_labels:
        first = choice_labels[0]
        b = builder.choice(first[0], first[1], first[2], text_id=f"c_{first[0]}")

        # 残りの選択肢
        for label, jp, en in choice_labels[1:]:
            b.choice(label, jp, en, text_id=f"c_{label}")

        # 戻るボタン
        b.choice(back_label, "戻る", "Back", text_id=f"c_back_{entry_label}")

    # 各ドラマ再生ステップ
    for drama_id in drama_ids:
        label = f"play_{drama_id}"
        drama_name = f"drama_{drama_id}"
        builder.step(label) \
            ._start_drama(drama_name) \
            .finish()


def _build_battle_submenu(builder: DramaBuilder, entry_label: str, stages: dict, back_label: str, actor):
    """バトルサブメニューを構築"""
    menu_label = f"{entry_label}_choice"

    builder.step(entry_label) \
        .say(f"{entry_label}_msg", "バトルを選択してください。", "", actor=actor) \
        .jump(menu_label)

    # 選択肢を構築
    choice_labels = []
    for stage_id, stage in stages.items():
        label = f"fight_{stage_id}"
        choice_labels.append((label, stage.display_name_jp, stage.display_name_en, stage_id))

    # 最初の選択肢
    if choice_labels:
        first = choice_labels[0]
        b = builder.choice(first[0], first[1], first[2], text_id=f"c_{first[0]}")

        # 残りの選択肢
        for label, jp, en, _ in choice_labels[1:]:
            b.choice(label, jp, en, text_id=f"c_{label}")

        # 戻るボタン
        b.choice(back_label, "戻る", "Back", text_id=f"c_back_{entry_label}")

    # 各バトル開始ステップ
    for label, _, _, stage_id in choice_labels:
        builder.step(label) \
            .start_battle_by_stage(stage_id) \
            .finish()
