
from drama_builder import DramaBuilder
from drama_constants import DramaNames
from flag_definitions import (
    Keys, Actors, QuestIds,
    Motivation, Rank,
    PlayerFlags, RelFlags
)
from scenarios.rank_up.rank_g import add_rank_up_G_result_steps
from scenarios.rank_up.rank_f import add_rank_up_F_result_steps
from scenarios.rank_up.rank_e import add_rank_up_E_result_steps
from scenarios.rank_up.rank_d import add_rank_up_D_result_steps
from scenarios.rank_up.rank_c import add_rank_up_C_result_steps
from scenarios.rank_up.rank_b import add_rank_up_B_result_steps

def define_arena_master_drama(builder: DramaBuilder):
    """
    アリーナマスターのドラマを定義
    フラグ管理システムを使用（ランク/関係値チェック）
    """
    pc = builder.register_actor(Actors.PC, "あなた", "You")
    vargus = builder.register_actor(Actors.BALGAS, "バルガス", "Vargus")
    lily = builder.register_actor(Actors.LILY, "リリィ", "Lily")

    main = builder.label("main")
    victory_comment = builder.label("victory_comment")
    defeat_comment = builder.label("defeat_comment")
    defeat_stage2 = builder.label("defeat_stage2")
    defeat_stage3 = builder.label("defeat_stage3")
    defeat_champion = builder.label("defeat_champion")
    registered = builder.label("registered")
    registered_choices = builder.label("registered_choices")
    greet_unranked = builder.label("greet_unranked")
    greet_G = builder.label("greet_G")
    greet_F = builder.label("greet_F")
    greet_E = builder.label("greet_E")
    greet_D = builder.label("greet_D")
    greet_C = builder.label("greet_C")
    greet_B = builder.label("greet_B")
    greet_A = builder.label("greet_A")
    greet_S = builder.label("greet_S")
    greet_SS = builder.label("greet_SS")
    greet_SSS = builder.label("greet_SSS")
    greet_U = builder.label("greet_U")
    greet_Z = builder.label("greet_Z")
    greet_god_slayer = builder.label("greet_god_slayer")
    greet_singularity = builder.label("greet_singularity")
    greet_void_king = builder.label("greet_void_king")
    greet_default = builder.label("greet_default")
    join_yes = builder.label("join_yes")
    join_no = builder.label("join_no")
    battle_prep = builder.label("battle_prep")
    stage2_prep = builder.label("stage2_prep")
    stage3_prep = builder.label("stage3_prep")
    stage_champion = builder.label("stage_champion")
    battle_start_stage1 = builder.label("battle_start_stage1")
    battle_start_stage2 = builder.label("battle_start_stage2")
    battle_start_stage3 = builder.label("battle_start_stage3")
    battle_start_champion = builder.label("battle_start_champion")
    end = builder.label("end")

    rank_check = builder.label("rank_check")
    rank_up_check = builder.label("rank_up_check")
    to_rank_up = builder.label("to_rank_up")

    # --- Helper Function for Common Choices ---
    check_available_quests = builder.label("check_available_quests")
    quest_info = builder.label("quest_info")
    quest_none = builder.label("quest_none")

    def add_choices(b):
        """共通の選択肢を追加する"""
        b.choice(battle_prep, "戦いに挑む", "", text_id="c3") \
         .choice(rank_check, "ランクを確認したい", "", text_id="c_rank_check") \
         .choice(rank_up_check, "昇格試験を受けたい", "", text_id="c_rank_up") \
         .choice(check_available_quests, "利用可能なクエストを確認", "", text_id="c_check_quests") \
         .choice(end, "また今度", "", text_id="c4") \
         .on_cancel(end)

    # Rank Up Result Dispatch Logic
    rank_up_victory_g = builder.label("rank_up_victory_g")
    rank_up_defeat_g = builder.label("rank_up_defeat_g")
    rank_up_victory_f = builder.label("rank_up_victory_f")
    rank_up_defeat_f = builder.label("rank_up_defeat_f")
    rank_up_victory_e = builder.label("rank_up_victory_e")
    rank_up_defeat_e = builder.label("rank_up_defeat_e")
    rank_up_victory_d = builder.label("rank_up_victory_d")
    rank_up_defeat_d = builder.label("rank_up_defeat_d")
    rank_up_victory_c = builder.label("rank_up_victory_c")
    rank_up_defeat_c = builder.label("rank_up_defeat_c")
    rank_up_victory_b = builder.label("rank_up_victory_b")
    rank_up_defeat_b = builder.label("rank_up_defeat_b")

    # Main Step
    # ランクアップ結果の場合は勝敗フラグで分岐
    builder.step(main) \
        .branch_if("sukutsu_is_rank_up_result", "==", 1, "rank_up_result_check") \
        .branch_if("sukutsu_arena_result", "==", 1, victory_comment) \
        .branch_if("sukutsu_arena_result", "==", 2, defeat_comment) \
        .branch_if("sukutsu_gladiator", "==", 1, registered)

    # ランクアップ結果チェック（勝利/敗北を判定）
    # sukutsu_rank_up_trial フラグで試験種別を判定: 1=G, 2=F, 3=E, 4=D, 5=C, 6=B
    builder.label("rank_up_result_check")
    rank_up_result_g = builder.label("rank_up_result_g")
    rank_up_result_f = builder.label("rank_up_result_f")
    rank_up_result_e = builder.label("rank_up_result_e")
    rank_up_result_d = builder.label("rank_up_result_d")
    rank_up_result_c = builder.label("rank_up_result_c")
    rank_up_result_b = builder.label("rank_up_result_b")

    builder.step("rank_up_result_check") \
        .set_flag("sukutsu_is_rank_up_result", 0) \
        .switch_on_flag("sukutsu_rank_up_trial", {
            1: rank_up_result_g,
            2: rank_up_result_f,
            3: rank_up_result_e,
            4: rank_up_result_d,
            5: rank_up_result_c,
            6: rank_up_result_b,
        }, fallback=registered)

    # Rank G 結果分岐
    builder.step(rank_up_result_g) \
        .switch_on_flag("sukutsu_arena_result", {
            1: rank_up_victory_g,
            2: rank_up_defeat_g,
        }, fallback=registered)

    # Rank F 結果分岐
    builder.step(rank_up_result_f) \
        .switch_on_flag("sukutsu_arena_result", {
            1: rank_up_victory_f,
            2: rank_up_defeat_f,
        }, fallback=registered)

    # Rank E 結果分岐
    builder.step(rank_up_result_e) \
        .switch_on_flag("sukutsu_arena_result", {
            1: rank_up_victory_e,
            2: rank_up_defeat_e,
        }, fallback=registered)

    # Rank D 結果分岐
    builder.step(rank_up_result_d) \
        .switch_on_flag("sukutsu_arena_result", {
            1: rank_up_victory_d,
            2: rank_up_defeat_d,
        }, fallback=registered)

    # Rank C 結果分岐
    builder.step(rank_up_result_c) \
        .switch_on_flag("sukutsu_arena_result", {
            1: rank_up_victory_c,
            2: rank_up_defeat_c,
        }, fallback=registered)

    # Rank B 結果分岐
    builder.step(rank_up_result_b) \
        .switch_on_flag("sukutsu_arena_result", {
            1: rank_up_victory_b,
            2: rank_up_defeat_b,
        }, fallback=registered)

    # === Rank G 昇格試験 勝利/敗北 ===
    add_rank_up_G_result_steps(builder, rank_up_victory_g, rank_up_defeat_g, registered_choices)

    # === Rank F 昇格試験 勝利/敗北 ===
    add_rank_up_F_result_steps(builder, rank_up_victory_f, rank_up_defeat_f, registered_choices)

    # === Rank E 昇格試験 勝利/敗北 ===
    add_rank_up_E_result_steps(builder, rank_up_victory_e, rank_up_defeat_e, registered_choices)

    # === Rank D 昇格試験 勝利/敗北 ===
    add_rank_up_D_result_steps(builder, rank_up_victory_d, rank_up_defeat_d, registered_choices)

    # === Rank C 昇格試験 勝利/敗北 ===
    add_rank_up_C_result_steps(builder, rank_up_victory_c, rank_up_defeat_c, registered_choices)

    # === Rank B 昇格試験 勝利/敗北 ===
    add_rank_up_B_result_steps(builder, rank_up_victory_b, rank_up_defeat_b, registered_choices)

    # 未登録者挨拶
    builder.say("greet1", "何の用だ、ひよっこ。見たところ、戦いの「せ」の字も知らなそうだな。", "", actor=vargus) \
        .choice(join_yes, "闘士になりたい", "", text_id="c1") \
        .choice(join_no, "いや、やめておく", "", text_id="c2") \
        .on_cancel(end)

    # Victory/Defeat Comments (Directly add choices)
    b = builder.step(victory_comment) \
        .set_flag("sukutsu_arena_result", 0) \
        .say("vic_msg", "やるじゃねえか。だが調子に乗るなよ。", "", actor=vargus)
    add_choices(b)

    b = builder.step(defeat_comment) \
        .set_flag("sukutsu_arena_result", 0) \
        .say("def_msg", "無様だな。出直してこい。", "", actor=vargus)
    add_choices(b)

    # === Rank Check Logic ===
    # ランク確認表示 (ログに詳細を表示)
    b = builder.step(rank_check) \
        .show_rank_info_log() \
        .say("rank_info", "現在のステータスをログに表示したぜ。確認しな。", "", actor=vargus)
    add_choices(b) # Jumpではなく直接追加

    # 昇格試験への分岐（クエストシステムベース）
    rank_up_not_ready = builder.label("rank_up_not_ready")
    start_rank_g = builder.label("start_rank_g")
    start_rank_f = builder.label("start_rank_f")
    start_rank_e = builder.label("start_rank_e")
    start_rank_d = builder.label("start_rank_d")
    start_rank_c = builder.label("start_rank_c")
    start_rank_b = builder.label("start_rank_b")
    start_rank_g_confirmed = builder.label("start_rank_g_confirmed")
    start_rank_f_confirmed = builder.label("start_rank_f_confirmed")
    start_rank_e_confirmed = builder.label("start_rank_e_confirmed")
    start_rank_d_confirmed = builder.label("start_rank_d_confirmed")
    start_rank_c_confirmed = builder.label("start_rank_c_confirmed")
    start_rank_b_confirmed = builder.label("start_rank_b_confirmed")

    # 昇格試験チェックのエントリーポイント
    # sukutsu_quest_target_name: 11=G, 12=F, 13=E, 14=D, 15=C, 16=B
    builder.step(rank_up_check) \
        .set_flag("sukutsu_quest_found", 0) \
        .set_flag("sukutsu_quest_target_name", 0) \
        .check_quests([
            (QuestIds.RANK_UP_G, start_rank_g),
            (QuestIds.RANK_UP_F, start_rank_f),
            (QuestIds.RANK_UP_E, start_rank_e),
            (QuestIds.RANK_UP_D, start_rank_d),
            (QuestIds.RANK_UP_C, start_rank_c),
            (QuestIds.RANK_UP_B, start_rank_b),
        ]) \
        .switch_on_flag("sukutsu_quest_target_name", {
            11: start_rank_g,
            12: start_rank_f,
            13: start_rank_e,
            14: start_rank_d,
            15: start_rank_c,
            16: start_rank_b,
        }, fallback=rank_up_not_ready)

    # 利用可能な昇格試験がない場合
    b = builder.step(rank_up_not_ready) \
        .say("rank_up_error", "まだお前には早い。条件を満たしていないか、すでに昇格済みだ。", "", actor=vargus)
    add_choices(b)

    # ランクG試験開始確認
    builder.step(start_rank_g) \
        .say("rank_up_confirm_g", "ほう…『屑肉の洗礼』を受けるつもりか？死んでも文句は言えんぞ。", "", actor=vargus) \
        .choice(start_rank_g_confirmed, "問題ない", "", text_id="c_confirm_rup_g") \
        .choice(registered_choices, "やめておく", "", text_id="c_cancel_rup") \
        .on_cancel(registered_choices)

    # ランクG試験実行
    builder.step(start_rank_g_confirmed) \
        .set_flag("sukutsu_rank_up_trial", 1) \
        .say_and_start_drama("いい度胸だ！", DramaNames.RANK_UP_G, "sukutsu_arena_master") \
        .jump(end)

    # ランクF試験開始確認
    builder.step(start_rank_f) \
        .say("rank_up_confirm_f", "『凍土の魔犬』との戦いだな。覚悟はいいか？", "", actor=vargus) \
        .choice(start_rank_f_confirmed, "いくぞ", "", text_id="c_confirm_rup_f") \
        .choice(registered_choices, "やめておく", "", text_id="c_cancel_rup") \
        .on_cancel(registered_choices)

    # ランクF試験実行
    builder.step(start_rank_f_confirmed) \
        .set_flag("sukutsu_rank_up_trial", 2) \
        .say_and_start_drama("行ってこい！", DramaNames.RANK_UP_F, "sukutsu_arena_master") \
        .jump(end)

    # ランクE試験開始確認
    builder.step(start_rank_e) \
        .say("rank_up_confirm_e", "『カイン亡霊戦』だな。あいつは……俺が知る中でも最強の剣闘士だった。覚悟はいいか？", "", actor=vargus) \
        .choice(start_rank_e_confirmed, "挑む", "", text_id="c_confirm_rup_e") \
        .choice(registered_choices, "やめておく", "", text_id="c_cancel_rup") \
        .on_cancel(registered_choices)

    # ランクE試験実行
    builder.step(start_rank_e_confirmed) \
        .set_flag("sukutsu_rank_up_trial", 3) \
        .say_and_start_drama("……あいつの魂を、解放してやれ。", DramaNames.RANK_UP_E, "sukutsu_arena_master") \
        .jump(end)

    # ランクD試験開始確認
    builder.step(start_rank_d) \
        .say("rank_up_confirm_d", "『銅貨稼ぎの洗礼』だな。観客のヤジが降ってくる。避けながら戦えるか？", "", actor=vargus) \
        .choice(start_rank_d_confirmed, "やってみる", "", text_id="c_confirm_rup_d") \
        .choice(registered_choices, "やめておく", "", text_id="c_cancel_rup") \
        .on_cancel(registered_choices)

    # ランクD試験実行
    builder.step(start_rank_d_confirmed) \
        .set_flag("sukutsu_rank_up_trial", 4) \
        .say_and_start_drama("観客を楽しませてやれ！", DramaNames.RANK_UP_D, "sukutsu_arena_master") \
        .jump(end)

    # ランクC試験開始確認
    builder.step(start_rank_c) \
        .say("rank_up_confirm_c", "『闘技場の鴉』への試練だな……俺のかつての仲間たちと戦ってもらう。", "", actor=vargus) \
        .choice(start_rank_c_confirmed, "分かった", "", text_id="c_confirm_rup_c") \
        .choice(registered_choices, "やめておく", "", text_id="c_cancel_rup") \
        .on_cancel(registered_choices)

    # ランクC試験実行
    builder.step(start_rank_c_confirmed) \
        .set_flag("sukutsu_rank_up_trial", 5) \
        .say_and_start_drama("……頼んだぞ。あいつらを、この地獄から解放してやってくれ。", DramaNames.RANK_UP_C, "sukutsu_arena_master") \
        .jump(end)

    # ランクB試験開始確認
    builder.step(start_rank_b) \
        .say("rank_up_confirm_b", "『虚無の処刑人』……ヌルとの戦いだ。あいつは、虚空そのものだ。覚悟はいいか？", "", actor=vargus) \
        .choice(start_rank_b_confirmed, "挑む", "", text_id="c_confirm_rup_b") \
        .choice(registered_choices, "やめておく", "", text_id="c_cancel_rup") \
        .on_cancel(registered_choices)

    # ランクB試験実行
    builder.step(start_rank_b_confirmed) \
        .set_flag("sukutsu_rank_up_trial", 6) \
        .say_and_start_drama("……虚空を見つめるな。飲み込まれるぞ。", DramaNames.RANK_UP_B, "sukutsu_arena_master") \
        .jump(end)


    # === Registered Greeting ===

    builder.step(registered) \
        .switch_on_flag("player.rank", {
            0: greet_unranked,
            1: greet_G,
            2: greet_F,
            3: greet_E,
            4: greet_D,
            5: greet_C,
            6: greet_B,
            7: greet_A,
            8: greet_S,
            9: greet_SS,
            10: greet_SSS,
            11: greet_U,
            12: greet_Z,
            13: greet_god_slayer,
            14: greet_singularity,
            15: greet_void_king,
        }, fallback=greet_default)

    # 戻り先として確保(on_cancel等用)
    b = builder.step(registered_choices)
    add_choices(b)


    # 各ランク挨拶 + 選択肢インライン展開
    b = builder.step(greet_unranked).say("greet_u", "おう、ひよっこ。今日は何の用だ？", "", actor=vargus)
    add_choices(b)

    b = builder.step(greet_G).say("greet_G", "おう、『屑肉』よ。今日は何の用だ？", "", actor=vargus)
    add_choices(b)

    b = builder.step(greet_F).say("greet_F", "おう、『泥犬』よ。今日は何の用だ？", "", actor=vargus)
    add_choices(b)

    b = builder.step(greet_E).say("greet_E", "おう、『鉄屑』よ。今日は何の用だ？", "", actor=vargus)
    add_choices(b)

    b = builder.step(greet_D).say("greet_D", "おう、『銅貨稼ぎ』よ。今日は何の用だ？", "", actor=vargus)
    add_choices(b)

    b = builder.step(greet_C).say("greet_C", "おう、『鴉』よ。今日は何の用だ？", "", actor=vargus)
    add_choices(b)

    b = builder.step(greet_B).say("greet_B", "おう、『銀翼』よ。今日は何の用だ？", "", actor=vargus)
    add_choices(b)

    b = builder.step(greet_A).say("greet_A", "おう、『戦鬼』よ。今日は何の用だ？", "", actor=vargus)
    add_choices(b)

    b = builder.step(greet_S).say("greet_S", "……待っていたぞ、『屠竜者』！何の用だ？", "", actor=vargus)
    add_choices(b)

    b = builder.step(greet_SS).say("greet_SS", "……『覇者』か。相変わらず凄まじい覇気だ。今日は何用だ？", "", actor=vargus)
    add_choices(b)

    b = builder.step(greet_SSS).say("greet_SSS", "……よお、『因果を断つ者』よ。酒でも飲みに来たか？", "", actor=vargus)
    add_choices(b)

    b = builder.step(greet_U).say("greet_U", "……ははっ、『星砕き』よ。今日はどの星を落とすつもりだ？", "", actor=vargus)
    add_choices(b)

    b = builder.step(greet_Z).say("greet_Z", "……『終末の観測者』よ。お前の瞳には、この世界の最期が見えているのか？", "", actor=vargus)
    add_choices(b)

    b = builder.step(greet_god_slayer).say("greet_gs", "……『神殺し』よ。その翼、どこまで広げるつもりだ？", "", actor=vargus)
    add_choices(b)

    b = builder.step(greet_singularity).say("greet_sg", "……『特異点』よ。お前の存在だけで空間が歪む音がするぜ。用件を聞こうか。", "", actor=vargus)
    add_choices(b)

    b = builder.step(greet_void_king).say("greet_vk", "……『虚空の王』よ。この俺に命令があるのか？ それとも、ただの気まぐれか？", "", actor=vargus)
    add_choices(b)

    b = builder.step(greet_default).say("greet_def", "おう、闘士よ。今日は何の用だ？", "", actor=vargus)
    add_choices(b)


    # === Join Yes ===
    builder.step(join_yes) \
        .say("join1", "おまえが？ハーッハッハ...まあいい、死にたいなら止めはしない。これでお前も闘士だ。戦いの準備ができたら声をかけろ。", "", actor=vargus) \
        .set_flag("sukutsu_gladiator", 1) \
        .set_flag("sukutsu_arena_stage", 1) \
        .set_flag(Keys.RANK, 0) \
        .set_flag(Keys.REL_LILY, 30) \
        .set_flag(Keys.REL_BALGAS, 20) \
        .action("reload", jump=main)

    # === Join No ===
    builder.step(join_no) \
        .say("reject1", "話は終わりだ。ママのミルクでも飲んでな。", "", actor=vargus) \
        .jump(end)

    # === Battle Prep ===
    builder.step(battle_prep) \
        .branch_if("sukutsu_arena_stage", ">=", 2, stage2_prep) \
        .say("stage1_advice", "お前の最初の相手は「森の狼」だ。素早い攻撃には気をつけろ。武器と防具は整えたか？回復アイテムもあると安心だぞ。", "", actor=vargus) \
        .choice(battle_start_stage1, "準備できた、行く！", "", text_id="c_go1") \
        .choice(registered_choices, "もう少し準備してくる", "", text_id="c_cancel1") \
        .on_cancel(registered_choices)

    # Stage 2 Prep
    builder.step(stage2_prep) \
        .branch_if("sukutsu_arena_stage", ">=", 3, stage3_prep) \
        .say("stage2_advice", "次の相手は「ケンタウロス」だ。奴の突進は威力があるぞ。", "", actor=vargus) \
        .choice(battle_start_stage2, "準備できた！", "", text_id="c_go2") \
        .choice(registered_choices, "待ってくれ", "", text_id="c_cancel2") \
        .on_cancel(registered_choices)

    # Stage 3 Prep
    builder.step(stage3_prep) \
        .branch_if("sukutsu_arena_stage", ">=", 4, stage_champion) \
        .say("stage3_advice", "ここからが本番だ。「ミノタウロス」...奴は俺も手こずった相手だ。力任せに攻めるな。奴の隙を狙え。", "", actor=vargus) \
        .choice(battle_start_stage3, "挑む！", "", text_id="c_go3") \
        .choice(registered_choices, "...もう少し鍛えてくる", "", text_id="c_cancel3") \
        .on_cancel(registered_choices)

    # Champion Prep
    builder.step(stage_champion) \
        .say("champion_advice", "よくぞここまで来た。最後の相手は...グランドマスターだ。覚悟はいいか？あれは...俺でも勝てるかわからん相手だ。", "", actor=vargus) \
        .choice(battle_start_champion, "俺は負けない", "", text_id="c_go_champ") \
        .choice(registered_choices, "...考え直す", "", text_id="c_cancel_champ") \
        .on_cancel(registered_choices)

    # === Battle Starts ===
    builder.step(battle_start_stage1) \
        .say("sendoff1", "よし、行け！生きて戻ってこい...できればな。", "", actor=vargus) \
        .start_battle(1) \
        .finish()

    builder.step(battle_start_stage2) \
        .say("sendoff2", "いい度胸だ。お前ならやれる！", "", actor=vargus) \
        .start_battle(2) \
        .finish()

    builder.step(battle_start_stage3) \
        .say("sendoff3", "...無茶するなよ。お前はもうただの新人じゃない。", "", actor=vargus) \
        .start_battle(3) \
        .finish()

    builder.step(battle_start_champion) \
        .say("sendoff_champ", "...見届けてやる。行って来い、闘士よ。", "", actor=vargus) \
        .start_battle(4) \
        .finish()

    # === Quest System Integration ===

    # クエスト確認 - 利用可能なクエストをチェック
    # ラベル定義（使用前に定義が必要）
    # ランクアップ系
    quest_rank_up_g = builder.label("quest_rank_up_g")
    quest_rank_up_f = builder.label("quest_rank_up_f")
    quest_rank_up_e = builder.label("quest_rank_up_e")
    quest_rank_up_d = builder.label("quest_rank_up_d")
    quest_rank_up_c = builder.label("quest_rank_up_c")
    quest_rank_up_b = builder.label("quest_rank_up_b")
    # ストーリー系
    quest_zek_intro = builder.label("quest_zek_intro")
    quest_lily_exp = builder.label("quest_lily_exp")
    quest_zek_steal_bottle = builder.label("quest_zek_steal_bottle")
    quest_zek_steal_soulgem = builder.label("quest_zek_steal_soulgem")
    quest_upper_existence = builder.label("quest_upper_existence")
    quest_lily_private = builder.label("quest_lily_private")
    quest_balgas_training = builder.label("quest_balgas_training")
    quest_makuma = builder.label("quest_makuma")
    quest_makuma2 = builder.label("quest_makuma2")
    quest_vs_balgas = builder.label("quest_vs_balgas")
    quest_lily_real_name = builder.label("quest_lily_real_name")
    quest_vs_grandmaster_1 = builder.label("quest_vs_grandmaster_1")
    quest_last_battle = builder.label("quest_last_battle")

    # クエスト確認開始（フラグをクリアしてからチェック）
    # sukutsu_quest_target_name マッピング:
    # 11-16: ランクアップ (G, F, E, D, C, B)
    # 21-33: ストーリークエスト
    builder.step(check_available_quests) \
        .say("quest_check", "利用可能なクエストがあるか確認するぜ...", "", actor=vargus) \
        .set_flag("sukutsu_quest_found", 0) \
        .set_flag("sukutsu_quest_target_name", 0) \
        .debug_log_quests() \
        .check_quests([
            # ランクアップ系
            (QuestIds.RANK_UP_G, quest_rank_up_g),
            (QuestIds.RANK_UP_F, quest_rank_up_f),
            (QuestIds.RANK_UP_E, quest_rank_up_e),
            (QuestIds.RANK_UP_D, quest_rank_up_d),
            (QuestIds.RANK_UP_C, quest_rank_up_c),
            (QuestIds.RANK_UP_B, quest_rank_up_b),
            # ストーリー系
            (QuestIds.ZEK_INTRO, quest_zek_intro),
            (QuestIds.LILY_EXPERIMENT, quest_lily_exp),
            (QuestIds.ZEK_STEAL_BOTTLE, quest_zek_steal_bottle),
            (QuestIds.ZEK_STEAL_SOULGEM, quest_zek_steal_soulgem),
            (QuestIds.UPPER_EXISTENCE, quest_upper_existence),
            (QuestIds.LILY_PRIVATE, quest_lily_private),
            (QuestIds.BALGAS_TRAINING, quest_balgas_training),
            (QuestIds.MAKUMA, quest_makuma),
            (QuestIds.MAKUMA2, quest_makuma2),
            (QuestIds.RANK_UP_S, quest_vs_balgas),
            (QuestIds.LILY_REAL_NAME, quest_lily_real_name),
            (QuestIds.VS_GRANDMASTER_1, quest_vs_grandmaster_1),
            (QuestIds.LAST_BATTLE, quest_last_battle),
        ]) \
        .switch_on_flag("sukutsu_quest_target_name", {
            # ランクアップ系
            11: quest_rank_up_g,
            12: quest_rank_up_f,
            13: quest_rank_up_e,
            14: quest_rank_up_d,
            15: quest_rank_up_c,
            16: quest_rank_up_b,
            # ストーリー系
            21: quest_zek_intro,
            22: quest_lily_exp,
            23: quest_zek_steal_bottle,
            24: quest_zek_steal_soulgem,
            25: quest_upper_existence,
            26: quest_lily_private,
            27: quest_balgas_training,
            28: quest_makuma,
            29: quest_makuma2,
            30: quest_vs_balgas,
            31: quest_lily_real_name,
            32: quest_vs_grandmaster_1,
            33: quest_last_battle,
        }, fallback=quest_none)

    # === ランクアップ系クエスト情報 ===
    builder.step(quest_rank_up_g) \
        .say("quest_rank_g_info", "【昇格試験】ランクG『屑肉の洗礼』が受けられるぜ。「昇格試験を受けたい」を選んでくれ。", "", actor=vargus) \
        .jump(registered_choices)

    builder.step(quest_rank_up_f) \
        .say("quest_rank_f_info", "【昇格試験】ランクF『凍土の魔犬』が受けられるぜ。「昇格試験を受けたい」を選んでくれ。", "", actor=vargus) \
        .jump(registered_choices)

    builder.step(quest_rank_up_e) \
        .say("quest_rank_e_info", "【昇格試験】ランクE『カイン亡霊戦』が受けられるぜ。「昇格試験を受けたい」を選んでくれ。", "", actor=vargus) \
        .jump(registered_choices)

    builder.step(quest_rank_up_d) \
        .say("quest_rank_d_info", "【昇格試験】ランクD『銅貨稼ぎの洗礼』が受けられるぜ。「昇格試験を受けたい」を選んでくれ。", "", actor=vargus) \
        .jump(registered_choices)

    builder.step(quest_rank_up_c) \
        .say("quest_rank_c_info", "【昇格試験】ランクC『闘技場の鴉』が受けられるぜ。「昇格試験を受けたい」を選んでくれ。", "", actor=vargus) \
        .jump(registered_choices)

    builder.step(quest_rank_up_b) \
        .say("quest_rank_b_info", "【昇格試験】ランクB『虚無の処刑人』が受けられるぜ。「昇格試験を受けたい」を選んでくれ。", "", actor=vargus) \
        .jump(registered_choices)

    # === ストーリー系クエスト ===
    # バルガス（アリーナマスター）直接開始用ラベル
    start_upper_existence = builder.label("start_upper_existence")
    start_balgas_training = builder.label("start_balgas_training")
    start_vs_balgas = builder.label("start_vs_balgas")

    # -------------------------------------------
    # ゼクのクエスト（情報提供のみ、ゼクに話しかけて開始）
    # -------------------------------------------
    # クエスト: ゼクとの出会い
    builder.step(quest_zek_intro) \
        .say("quest_zek_info", "おい、見慣れねえ商人が来てるぞ。『ゼク』って名乗る怪しい野郎だ。", "", actor=vargus) \
        .say("quest_zek_info2", "ロビーの隅にいるはずだ。興味があるなら話しかけてみろ。", "", actor=vargus) \
        .jump(registered_choices)

    # クエスト: ゼクの瓶すり替え提案
    builder.step(quest_zek_steal_bottle) \
        .say("quest_zek_bottle_info", "ゼクの野郎が何やら企んでやがる。あいつに話しかけてみろ。", "", actor=vargus) \
        .say("quest_zek_bottle_info2", "……俺は関わらねえが、お前の判断だ。", "", actor=vargus) \
        .jump(registered_choices)

    # クエスト: カインの魂の選択
    builder.step(quest_zek_steal_soulgem) \
        .say("quest_zek_soulgem_info", "ゼクがカインの『魂宝石』について何か言いたいことがあるらしい。", "", actor=vargus) \
        .say("quest_zek_soulgem_info2", "あいつのところへ行け。……慎重に選べよ。", "", actor=vargus) \
        .jump(registered_choices)

    # -------------------------------------------
    # リリィのクエスト（情報提供のみ、リリィに話しかけて開始）
    # -------------------------------------------
    # クエスト: リリィの実験
    builder.step(quest_lily_exp) \
        .say("quest_lily_info", "リリィが何やら困ってるらしいぜ。『虚空の共鳴瓶』とかいう怪しげなアイテムを作りたいとか。", "", actor=vargus) \
        .say("quest_lily_info2", "あいつのところへ行って話を聞いてやれ。", "", actor=vargus) \
        .jump(registered_choices)

    # クエスト: リリィの私室
    builder.step(quest_lily_private) \
        .say("quest_lily_priv_info", "リリィが『自分の過去』について話したいらしい。……珍しいな。", "", actor=vargus) \
        .say("quest_lily_priv_info2", "興味があるならあいつに話しかけてやれ。", "", actor=vargus) \
        .jump(registered_choices)

    # クエスト: マクマ登場
    builder.step(quest_makuma) \
        .say("quest_makuma_info", "怪しい連中が闘技場をうろついてる。『マクマ』とかいう組織らしい。", "", actor=vargus) \
        .say("quest_makuma_info2", "リリィが詳しく知ってるかもしれねえ。あいつに聞いてみろ。", "", actor=vargus) \
        .jump(registered_choices)

    # クエスト: リリィの真名
    builder.step(quest_lily_real_name) \
        .say("quest_lily_name_info", "リリィが『真の名』を教えてくれるらしい。", "", actor=vargus) \
        .say("quest_lily_name_info2", "……あいつを本気で信用するのか？　あいつに話しかけろ。", "", actor=vargus) \
        .jump(registered_choices)

    # -------------------------------------------
    # バルガス（アリーナマスター）のクエスト（直接開始可能）
    # -------------------------------------------
    # クエスト: 高次元存在の真実
    builder.step(quest_upper_existence) \
        .say("quest_upper_info", "……お前には『観客』の正体を教えておく必要がある。", "", actor=vargus) \
        .say("quest_upper_info2", "聞く覚悟はあるか？　真実は重いぞ。", "", actor=vargus) \
        .choice(start_upper_existence, "聞く", "", text_id="c_accept_upper") \
        .choice(registered_choices, "今はいい", "", text_id="c_decline_upper") \
        .on_cancel(registered_choices)

    # 高次元存在ドラマ開始
    builder.step(start_upper_existence) \
        .say_and_start_drama("……いいだろう。座れ。", DramaNames.UPPER_EXISTENCE, "sukutsu_arena_master") \
        .jump(end)

    # クエスト: バルガスの訓練
    builder.step(quest_balgas_training) \
        .say("quest_balgas_info", "……おい。俺が直接、お前を鍛えてやろうと思ってる。", "", actor=vargus) \
        .say("quest_balgas_info2", "死にたくなければ付いてこい。どうだ？", "", actor=vargus) \
        .choice(start_balgas_training, "ついていく", "", text_id="c_accept_balgas") \
        .choice(registered_choices, "今はやめておく", "", text_id="c_decline_balgas") \
        .on_cancel(registered_choices)

    # バルガス訓練ドラマ開始
    builder.step(start_balgas_training) \
        .say_and_start_drama("よし、来い！", DramaNames.BALGAS_TRAINING, "sukutsu_arena_master") \
        .jump(end)

    # クエスト: バルガス戦（ランクS昇格）
    builder.step(quest_vs_balgas) \
        .say("quest_vs_balgas_info", "……おい。俺と本気で戦う気はあるか？", "", actor=vargus) \
        .say("quest_vs_balgas_info2", "これは試験じゃねえ。俺の『決着』だ。", "", actor=vargus) \
        .choice(start_vs_balgas, "受けて立つ", "", text_id="c_accept_vs_balgas") \
        .choice(registered_choices, "今は遠慮する", "", text_id="c_decline_vs_balgas") \
        .on_cancel(registered_choices)

    # バルガス戦ドラマ開始
    builder.step(start_vs_balgas) \
        .say_and_start_drama("……覚悟はいいな。", DramaNames.VS_BALGAS, "sukutsu_arena_master") \
        .jump(end)

    # -------------------------------------------
    # 自動発動クエスト（情報提供のみ）
    # -------------------------------------------
    # クエスト: マクマの陰謀（自動発動のため情報のみ）
    builder.step(quest_makuma2) \
        .say("quest_makuma2_info", "マクマの連中が何か企んでやがる。リリィも巻き込まれてるかもしれねえ。", "", actor=vargus) \
        .say("quest_makuma2_info2", "……気をつけろ。", "", actor=vargus) \
        .jump(registered_choices)

    # クエスト: グランドマスター戦（自動発動のため情報のみ）
    builder.step(quest_vs_grandmaster_1) \
        .say("quest_gm_info", "……いよいよだな。グランドマスターとの戦いが近い。", "", actor=vargus) \
        .say("quest_gm_info2", "覚悟しておけ。", "", actor=vargus) \
        .jump(registered_choices)

    # クエスト: 最終決戦（自動発動のため情報のみ）
    builder.step(quest_last_battle) \
        .say("quest_last_info", "……これが最後の戦いだ。", "", actor=vargus) \
        .say("quest_last_info2", "お前は何のために戦う？　答えを見つけておけ。", "", actor=vargus) \
        .jump(registered_choices)

    # 汎用クエスト受諾（現在は未使用、将来の拡張用）
    builder.step(quest_info) \
        .say("quest_accepted", "よし、頑張れよ。報酬は期待できるかもしれねえぞ。", "", actor=vargus) \
        .jump(registered_choices)

    # 利用可能なクエストがない場合
    builder.step(quest_none) \
        .say("no_quest", "今は特に依頼はねえな。まずは実力をつけることだ。", "", actor=vargus) \
        .jump(registered_choices)

    builder.step(end).finish()
