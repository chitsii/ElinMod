"""
デバッグバトルドラマ
====================
全バトルステージに直接アクセスできるデバッグ用NPC

観測者（Debug Master）に話しかけると、各種バトルやフラグ操作が可能
"""

from drama_builder import DramaBuilder
from drama_constants import DramaNames
from flag_definitions import Actors


def define_debug_battle_drama(builder: DramaBuilder):
    """
    デバッグバトルドラマを定義
    全バトルステージへの直接アクセスと、フラグ操作を提供
    """
    pc = builder.register_actor(Actors.PC, "あなた", "You")
    observer = builder.register_actor("sukutsu_debug_master", "観測者", "Observer")

    # === ラベル定義 ===
    main = builder.label("main")
    end = builder.label("end")

    # メインメニュー
    menu_battle = builder.label("menu_battle")
    menu_rank_trial = builder.label("menu_rank_trial")
    menu_story_battle = builder.label("menu_story_battle")
    menu_debug = builder.label("menu_debug")
    menu_flags = builder.label("menu_flags")

    # バトル選択
    battle_stage1 = builder.label("battle_stage1")
    battle_stage2 = builder.label("battle_stage2")
    battle_stage3 = builder.label("battle_stage3")
    battle_stage4 = builder.label("battle_stage4")
    battle_debug_weak = builder.label("battle_debug_weak")
    battle_debug_strong = builder.label("battle_debug_strong")
    battle_debug_horde = builder.label("battle_debug_horde")
    battle_debug_gimmick = builder.label("battle_debug_gimmick")

    # ランクアップ試練
    trial_g = builder.label("trial_g")
    trial_f = builder.label("trial_f")
    trial_e = builder.label("trial_e")
    trial_d = builder.label("trial_d")
    trial_c = builder.label("trial_c")
    trial_b = builder.label("trial_b")
    trial_a = builder.label("trial_a")
    trial_s = builder.label("trial_s")
    trial_final = builder.label("trial_final")

    # フラグ操作
    flag_set_rank = builder.label("flag_set_rank")
    flag_reset_all = builder.label("flag_reset_all")
    flag_complete_all = builder.label("flag_complete_all")

    # === メインエントリー ===
    builder.step(main) \
        .say("greet", "我は次元の記録者……全ての可能性を観測する者なり。", "", actor=observer) \
        .say("greet2", "汝、何を望む？", "", actor=observer) \
        .choice(menu_battle, "[通常バトル]", "", text_id="c_battle") \
        .choice(menu_rank_trial, "[ランクアップ試練]", "", text_id="c_trial") \
        .choice(menu_story_battle, "[ストーリーバトル]", "", text_id="c_story") \
        .choice(menu_debug, "[デバッグバトル]", "", text_id="c_debug") \
        .choice(menu_flags, "[フラグ操作]", "", text_id="c_flags") \
        .choice(end, "去る", "", text_id="c_leave") \
        .on_cancel(end)

    # === 通常バトルメニュー ===
    builder.step(menu_battle) \
        .say("battle_menu", "通常バトルを選択せよ。", "", actor=observer) \
        .choice(battle_stage1, "Stage 1: 森の狼", "", text_id="c_s1") \
        .choice(battle_stage2, "Stage 2: ケンタウロス", "", text_id="c_s2") \
        .choice(battle_stage3, "Stage 3: ミノタウロス", "", text_id="c_s3") \
        .choice(battle_stage4, "Stage 4: ドラゴン", "", text_id="c_s4") \
        .choice(main, "戻る", "", text_id="c_back") \
        .on_cancel(main)

    # 通常バトル開始
    builder.step(battle_stage1) \
        .say("go", "森の狼との戦いへ……", "", actor=observer) \
        .start_battle_by_stage("stage_1") \
        .finish()

    builder.step(battle_stage2) \
        .say("go", "ケンタウロスとの戦いへ……", "", actor=observer) \
        .start_battle_by_stage("stage_2") \
        .finish()

    builder.step(battle_stage3) \
        .say("go", "ミノタウロスとの戦いへ……", "", actor=observer) \
        .start_battle_by_stage("stage_3") \
        .finish()

    builder.step(battle_stage4) \
        .say("go", "ドラゴンとの戦いへ……", "", actor=observer) \
        .start_battle_by_stage("stage_4") \
        .finish()

    # === ランクアップ試練メニュー ===
    builder.step(menu_rank_trial) \
        .say("trial_menu", "ランクアップ試練を選択せよ。", "", actor=observer) \
        .choice(trial_g, "G: 屑肉の洗礼", "", text_id="c_tg") \
        .choice(trial_f, "F: 氷獄の猟犬", "", text_id="c_tf") \
        .choice(trial_e, "E: カインの亡霊", "", text_id="c_te") \
        .choice(trial_d, "D: 銅貨稼ぎの洗礼", "", text_id="c_td") \
        .choice(main, "戻る", "", text_id="c_back") \
        .on_cancel(main)

    # 追加メニュー（上位ランク）
    menu_rank_trial_2 = builder.label("menu_rank_trial_2")
    builder.step(menu_rank_trial) \
        .say("trial_menu", "ランクアップ試練を選択せよ。", "", actor=observer) \
        .choice(trial_g, "G: 屑肉の洗礼", "", text_id="c_tg") \
        .choice(trial_f, "F: 氷獄の猟犬", "", text_id="c_tf") \
        .choice(trial_e, "E: カインの亡霊", "", text_id="c_te") \
        .choice(trial_d, "D: 銅貨稼ぎの洗礼", "", text_id="c_td") \
        .choice(menu_rank_trial_2, "次へ", "", text_id="c_next") \
        .choice(main, "戻る", "", text_id="c_back") \
        .on_cancel(main)

    builder.step(menu_rank_trial_2) \
        .say("trial_menu2", "上位ランク試練を選択せよ。", "", actor=observer) \
        .choice(trial_c, "C: 闘技場の鴉", "", text_id="c_tc") \
        .choice(trial_b, "B: 虚無の処刑人", "", text_id="c_tb") \
        .choice(trial_a, "A: 影の自己", "", text_id="c_ta") \
        .choice(trial_s, "S: 全盛期バルガス", "", text_id="c_ts") \
        .choice(trial_final, "FINAL: アスタロス", "", text_id="c_tfinal") \
        .choice(menu_rank_trial, "戻る", "", text_id="c_back") \
        .on_cancel(menu_rank_trial)

    # ランクアップ試練開始
    builder.step(trial_g) \
        .say("go", "屑肉の洗礼へ……", "", actor=observer) \
        .set_flag("sukutsu_rank_up_trial", 1) \
        .start_battle_by_stage("rank_g_trial") \
        .finish()

    builder.step(trial_f) \
        .say("go", "氷獄の猟犬との戦いへ……", "", actor=observer) \
        .set_flag("sukutsu_rank_up_trial", 2) \
        .start_battle_by_stage("rank_f_trial") \
        .finish()

    builder.step(trial_e) \
        .say("go", "カインの亡霊との戦いへ……", "", actor=observer) \
        .set_flag("sukutsu_rank_up_trial", 3) \
        .start_battle_by_stage("rank_e_trial") \
        .finish()

    builder.step(trial_d) \
        .say("go", "銅貨稼ぎの洗礼へ……", "", actor=observer) \
        .set_flag("sukutsu_rank_up_trial", 4) \
        .start_battle_by_stage("rank_d_trial") \
        .finish()

    builder.step(trial_c) \
        .say("go", "闘技場の鴉との戦いへ……", "", actor=observer) \
        .set_flag("sukutsu_rank_up_trial", 5) \
        .start_battle_by_stage("rank_c_trial") \
        .finish()

    builder.step(trial_b) \
        .say("go", "虚無の処刑人との戦いへ……", "", actor=observer) \
        .set_flag("sukutsu_rank_up_trial", 6) \
        .start_battle_by_stage("rank_b_trial") \
        .finish()

    builder.step(trial_a) \
        .say("go", "影の自己との戦いへ……", "", actor=observer) \
        .set_flag("sukutsu_rank_up_trial", 7) \
        .start_battle_by_stage("rank_a_trial") \
        .finish()

    builder.step(trial_s) \
        .say("go", "全盛期バルガスとの戦いへ……", "", actor=observer) \
        .set_flag("sukutsu_rank_up_trial", 8) \
        .start_battle_by_stage("rank_s_trial") \
        .finish()

    builder.step(trial_final) \
        .say("go", "アスタロスとの最終決戦へ……", "", actor=observer) \
        .start_battle_by_stage("final_astaroth") \
        .finish()

    # === ストーリーバトルメニュー ===
    story_balgas = builder.label("story_balgas")
    story_astaroth = builder.label("story_astaroth")

    builder.step(menu_story_battle) \
        .say("story_menu", "ストーリーバトルを選択せよ。", "", actor=observer) \
        .choice(story_balgas, "VS バルガス（全盛期）", "", text_id="c_sb") \
        .choice(story_astaroth, "VS アスタロス", "", text_id="c_sa") \
        .choice(main, "戻る", "", text_id="c_back") \
        .on_cancel(main)

    builder.step(story_balgas) \
        .say("go", "バルガスとの決戦へ……", "", actor=observer) \
        .start_battle_by_stage("rank_s_trial") \
        .finish()

    builder.step(story_astaroth) \
        .say("go", "アスタロスとの最終決戦へ……", "", actor=observer) \
        .start_battle_by_stage("final_astaroth") \
        .finish()

    # === デバッグバトルメニュー ===
    builder.step(menu_debug) \
        .say("debug_menu", "デバッグ用バトルを選択せよ。", "", actor=observer) \
        .choice(battle_debug_weak, "[DEBUG] 弱い敵 (Lv1)", "", text_id="c_dw") \
        .choice(battle_debug_strong, "[DEBUG] 強い敵 (Lv100)", "", text_id="c_ds") \
        .choice(battle_debug_horde, "[DEBUG] 敵の群れ (10体)", "", text_id="c_dh") \
        .choice(battle_debug_gimmick, "[DEBUG] ギミックテスト", "", text_id="c_dg") \
        .choice(main, "戻る", "", text_id="c_back") \
        .on_cancel(main)

    builder.step(battle_debug_weak) \
        .say("go", "弱い敵との戦いへ……", "", actor=observer) \
        .start_battle_by_stage("debug_weak") \
        .finish()

    builder.step(battle_debug_strong) \
        .say("go", "強い敵との戦いへ……", "", actor=observer) \
        .start_battle_by_stage("debug_strong") \
        .finish()

    builder.step(battle_debug_horde) \
        .say("go", "敵の群れとの戦いへ……", "", actor=observer) \
        .start_battle_by_stage("debug_horde") \
        .finish()

    builder.step(battle_debug_gimmick) \
        .say("go", "ギミックテストへ……観客の妨害に注意せよ。", "", actor=observer) \
        .start_battle_by_stage("debug_gimmick") \
        .finish()

    # === フラグ操作メニュー ===
    set_rank_menu = builder.label("set_rank_menu")
    set_rank_0 = builder.label("set_rank_0")
    set_rank_1 = builder.label("set_rank_1")
    set_rank_2 = builder.label("set_rank_2")
    set_rank_3 = builder.label("set_rank_3")
    set_rank_4 = builder.label("set_rank_4")
    set_rank_5 = builder.label("set_rank_5")
    set_rank_6 = builder.label("set_rank_6")
    set_rank_7 = builder.label("set_rank_7")
    set_rank_8 = builder.label("set_rank_8")

    builder.step(menu_flags) \
        .say("flag_menu", "フラグ操作を選択せよ。", "", actor=observer) \
        .choice(set_rank_menu, "ランクを設定", "", text_id="c_rank") \
        .choice(flag_reset_all, "フラグをリセット", "", text_id="c_reset") \
        .choice(flag_complete_all, "全クエスト完了", "", text_id="c_complete") \
        .choice(main, "戻る", "", text_id="c_back") \
        .on_cancel(main)

    # ランク設定メニュー
    builder.step(set_rank_menu) \
        .say("rank_menu", "設定するランクを選択せよ。", "", actor=observer) \
        .choice(set_rank_0, "Unranked (0)", "", text_id="c_r0") \
        .choice(set_rank_1, "G (1)", "", text_id="c_r1") \
        .choice(set_rank_2, "F (2)", "", text_id="c_r2") \
        .choice(set_rank_3, "E (3)", "", text_id="c_r3") \
        .choice(set_rank_4, "D (4)", "", text_id="c_r4") \
        .choice(menu_flags, "戻る", "", text_id="c_back") \
        .on_cancel(menu_flags)

    set_rank_menu_2 = builder.label("set_rank_menu_2")
    builder.step(set_rank_menu) \
        .say("rank_menu", "設定するランクを選択せよ。", "", actor=observer) \
        .choice(set_rank_0, "Unranked (0)", "", text_id="c_r0") \
        .choice(set_rank_1, "G (1)", "", text_id="c_r1") \
        .choice(set_rank_2, "F (2)", "", text_id="c_r2") \
        .choice(set_rank_3, "E (3)", "", text_id="c_r3") \
        .choice(set_rank_menu_2, "次へ", "", text_id="c_next") \
        .choice(menu_flags, "戻る", "", text_id="c_back") \
        .on_cancel(menu_flags)

    builder.step(set_rank_menu_2) \
        .say("rank_menu2", "上位ランクを選択せよ。", "", actor=observer) \
        .choice(set_rank_4, "D (4)", "", text_id="c_r4") \
        .choice(set_rank_5, "C (5)", "", text_id="c_r5") \
        .choice(set_rank_6, "B (6)", "", text_id="c_r6") \
        .choice(set_rank_7, "A (7)", "", text_id="c_r7") \
        .choice(set_rank_8, "S (8)", "", text_id="c_r8") \
        .choice(set_rank_menu, "戻る", "", text_id="c_back") \
        .on_cancel(set_rank_menu)

    # ランク設定実行
    def make_set_rank_step(label, rank_value, rank_name):
        builder.step(label) \
            .set_flag("chitsii.arena.player.rank", rank_value) \
            .say("rank_set", f"ランクを {rank_name} に設定した。", "", actor=observer) \
            .jump(menu_flags)

    make_set_rank_step(set_rank_0, 0, "Unranked")
    make_set_rank_step(set_rank_1, 1, "G")
    make_set_rank_step(set_rank_2, 2, "F")
    make_set_rank_step(set_rank_3, 3, "E")
    make_set_rank_step(set_rank_4, 4, "D")
    make_set_rank_step(set_rank_5, 5, "C")
    make_set_rank_step(set_rank_6, 6, "B")
    make_set_rank_step(set_rank_7, 7, "A")
    make_set_rank_step(set_rank_8, 8, "S")

    # フラグリセット
    builder.step(flag_reset_all) \
        .set_flag("chitsii.arena.player.rank", 0) \
        .set_flag("chitsii.arena.player.current_phase", 0) \
        .set_flag("sukutsu_gladiator", 0) \
        .set_flag("sukutsu_arena_stage", 1) \
        .say("reset_done", "主要フラグをリセットした。", "", actor=observer) \
        .jump(menu_flags)

    # 全クエスト完了（開発用）
    builder.step(flag_complete_all) \
        .set_flag("chitsii.arena.player.rank", 8) \
        .set_flag("chitsii.arena.player.current_phase", 5) \
        .set_flag("sukutsu_gladiator", 1) \
        .set_flag("sukutsu_arena_stage", 4) \
        .say("complete_done", "主要フラグを完了状態に設定した。", "", actor=observer) \
        .jump(menu_flags)

    # === 終了 ===
    builder.step(end) \
        .say("farewell", "また会おう、観測対象よ……", "", actor=observer) \
        .finish()
