
from drama_builder import DramaBuilder
from flag_definitions import (
    Keys,
    Motivation, Rank,
    PlayerFlags, RelFlags
)
from scenarios.rank_up.rank_g import add_rank_up_G_result_steps

def define_arena_master_drama(builder: DramaBuilder):
    """
    アリーナマスターのドラマを定義
    フラグ管理システムを使用（ランク/関係値チェック）
    """
    pc = builder.register_actor("pc", "あなた", "You")
    vargus = builder.register_actor("sukutsu_arena_master", "バルガス", "Vargus")
    lily = builder.register_actor("sukutsu_receptionist", "リリィ", "Lily")

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
    debug_quest_accept = builder.label("debug_quest_accept")

    def add_choices(b):
        """共通の選択肢を追加する"""
        b.choice(battle_prep, "戦いに挑む", "", text_id="c3") \
         .choice(rank_check, "ランクを確認したい", "", text_id="c_rank_check") \
         .choice(rank_up_check, "昇格試験を受けたい", "", text_id="c_rank_up") \
         .choice(debug_quest_accept, "[DEBUG] リリィのクエストを受ける", "", text_id="c_debug_quest") \
         .choice(end, "また今度", "", text_id="c4") \
         .on_cancel(end)

    # Rank Up Result Dispatch Logic
    rank_up_victory_g = builder.label("rank_up_victory_g")
    rank_up_defeat_g = builder.label("rank_up_defeat_g")

    # Main Step
    # ランクアップ結果の場合は勝敗フラグで分岐
    builder.step(main) \
        .branch_if("sukutsu_is_rank_up_result", "==", 1, "rank_up_result_check") \
        .branch_if("sukutsu_arena_result", "==", 1, victory_comment) \
        .branch_if("sukutsu_arena_result", "==", 2, defeat_comment) \
        .branch_if("sukutsu_gladiator", "==", 1, registered)

    # ランクアップ結果チェック（勝利/敗北を判定）
    builder.label("rank_up_result_check")
    builder.step("rank_up_result_check") \
        .set_flag("sukutsu_is_rank_up_result", 0) \
        .branch_if("sukutsu_arena_result", "==", 1, rank_up_victory_g) \
        .branch_if("sukutsu_arena_result", "==", 2, rank_up_defeat_g) \
        .jump(registered)  # fallback

    # === Rank G 昇格試験 勝利/敗北 ===
    # rank_g.py で管理されるヘルパー関数を使用
    add_rank_up_G_result_steps(builder, rank_up_victory_g, rank_up_defeat_g, registered_choices)

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

    # 昇格試験への分岐
    # 貢献度チェック: Unranked(rank==0)なら10pt必要
    rank_up_not_ready = builder.label("rank_up_not_ready")

    builder.step(rank_up_check) \
        .branch_if("chitsii.arena.player.rank", "!=", 0, rank_up_not_ready) \
        .branch_if("chitsii.arena.player.contribution", ">=", 10, to_rank_up) \
        .jump(rank_up_not_ready)

    b = builder.step(rank_up_not_ready) \
        .say("rank_up_error", "まだお前には早い。貢献度が足りねえか、すでに昇格済みだ。", "", actor=vargus)
    add_choices(b)

    # 昇格試験本番へ
    rank_up_battle_start = builder.label("rank_up_battle_start")

    # 昇格試験開始
    start_rank_g = builder.label("start_rank_g")

    builder.step(to_rank_up) \
        .say("rank_up_confirm", "ほう…『屑肉の洗礼』を受けるつもりか？死んでも文句は言えんぞ。", "", actor=vargus) \
        .choice(start_rank_g, "問題ない", "", text_id="c_confirm_rup") \
        .choice(registered_choices, "やめておく", "", text_id="c_cancel_rup") \
        .on_cancel(registered_choices)

    # Rank G 試験開始
    # say アクション後に eval を直接実行すると失敗するため、
    # say_and_start_drama を使用してC#側で一括処理
    builder.step(start_rank_g) \
        .action("eval", param="UnityEngine.Debug.Log(\"[SukutsuArena] start_rank_g reached\");") \
        .say_and_start_drama("いい度胸だ！", "drama_rank_up_G", "sukutsu_arena_master") \
        .finish()


    # === Registered Greeting ===

    builder.step(registered) \
        .branch_if("player.rank", "==", 0, greet_unranked) \
        .branch_if("player.rank", "==", 1, greet_G) \
        .branch_if("player.rank", "==", 2, greet_F) \
        .branch_if("player.rank", "==", 3, greet_E) \
        .branch_if("player.rank", "==", 4, greet_D) \
        .branch_if("player.rank", "==", 5, greet_C) \
        .branch_if("player.rank", "==", 6, greet_B) \
        .branch_if("player.rank", "==", 7, greet_A) \
        .branch_if("player.rank", "==", 8, greet_S) \
        .branch_if("player.rank", "==", 9, greet_SS) \
        .branch_if("player.rank", "==", 10, greet_SSS) \
        .branch_if("player.rank", "==", 11, greet_U) \
        .branch_if("player.rank", "==", 12, greet_Z) \
        .branch_if("player.rank", "==", 13, greet_god_slayer) \
        .branch_if("player.rank", "==", 14, greet_singularity) \
        .branch_if("player.rank", "==", 15, greet_void_king) \
        .jump(greet_default)

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

    builder.step(end).finish()
