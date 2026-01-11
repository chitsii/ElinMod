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
from flag_definitions import Actors


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
           .choice(flags_menu, "フラグ操作", "", text_id="c_flags") \
           .choice(end, "終了", "", text_id="c_end")

    # main_menu ステップ（戻る先）
    builder.step(main_menu) \
        .say("debug_main", "何をテストしますか？", "", actor=debug_master)

    builder.choice(drama_menu, "ドラマを再生", "", text_id="c_drama_2") \
           .choice(battle_menu, "バトルを開始", "", text_id="c_battle_2") \
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
    # フラグ操作メニュー
    # ========================================
    set_rank_s = builder.label("set_rank_s")
    set_all_quests = builder.label("set_all_quests")
    set_relations = builder.label("set_relations")

    builder.step(flags_menu) \
        .say("flags_info", "フラグ操作を選択してください。", "", actor=debug_master)

    builder.choice(set_rank_s, "ランクSに設定", "", text_id="c_set_rank_s") \
           .choice(set_all_quests, "全クエスト完了", "", text_id="c_set_quests") \
           .choice(set_relations, "関係値MAX", "", text_id="c_set_relations") \
           .choice(main_menu, "戻る", "", text_id="c_flags_back")

    builder.step(set_rank_s) \
        .set_flag("chitsii.arena.player.rank", 8) \
        .set_flag("sukutsu_gladiator", 1) \
        .say("rank_set", "ランクをSに設定しました。", "", actor=debug_master) \
        .jump(flags_menu)

    builder.step(set_all_quests) \
        .action("eval", param="Elin_SukutsuArena.ArenaQuestManager.Instance.DebugCompleteAllQuests();") \
        .say("quests_set", "全クエストを完了しました。", "", actor=debug_master) \
        .jump(flags_menu)

    builder.step(set_relations) \
        .say("rel_set", "（旧システム: 関係値は削除されました）", "", actor=debug_master) \
        .jump(flags_menu)

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
