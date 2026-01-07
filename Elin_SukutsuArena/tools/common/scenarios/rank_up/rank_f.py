"""
04_rank_up_02.md - ランクF昇格試験『凍土の魔犬と凍てつく咆哮』
"""

from drama_builder import DramaBuilder
from flag_definitions import Keys, Rank, Actors, QuestIds
from reward_system import add_reward_choice, get_reward_tier_for_rank

def define_rank_up_F(builder: DramaBuilder):
    """
    Rank F 昇格試験「凍土の魔犬と凍てつく咆哮」
    シナリオ: 04_rank_up_02.md
    """
    # アクター登録
    pc = builder.register_actor(Actors.PC, "あなた", "You")
    lily = builder.register_actor(Actors.LILY, "リリィ", "Lily")
    balgas = builder.register_actor(Actors.BALGAS, "バルガス", "Balgas")

    # ラベル定義
    main = builder.label("main")
    scene1_reception = builder.label("scene1_reception")
    choice_lily = builder.label("choice_lily")
    lily_r1 = builder.label("lily_r1")
    lily_r2 = builder.label("lily_r2")
    lily_r3 = builder.label("lily_r3")
    scene2_balgas = builder.label("scene2_balgas")
    choice_balgas = builder.label("choice_balgas")
    balgas_r1 = builder.label("balgas_r1")
    balgas_r2 = builder.label("balgas_r2")
    balgas_r3 = builder.label("balgas_r3")
    battle_start = builder.label("battle_start")

    # ========================================
    # シーン1: 凍てつく境界線（受付）
    # ========================================
    builder.step(main) \
        .play_bgm("BGM/Lobby_Normal") \
        .say("narr_1", "（ロビーの空気が一変している。受付カウンターには薄く霜が降り、リリィの吐息すら白く濁っている。）", "", actor=pc) \
        .say("narr_2", "（彼女は冷たくなった指先を温めるように摩りながら、氷の結晶が浮き出た登録証を提示した。）", "", actor=pc) \
        .say("narr_3", "（松明の炎すら、凍気に押されて小さく震えている。床の石畳には薄い氷膜が張り、踏むたびにパリパリと音を立てる。）", "", actor=pc) \
        .jump(scene1_reception)

    builder.step(scene1_reception) \
        .say("lily_1", "……次は『冷気』の洗礼です。", "", actor=lily) \
        .say("narr_4", "（彼女は氷の結晶が浮き出た登録証を、あなたの前に滑らせる。）", "", actor=pc) \
        .say("lily_2", "お気の毒に。観客席の『あの方々』は、今夜は新鮮なフローズン・ミートを召し上がりたい気分だそうですよ。", "", actor=lily) \
        .say("lily_3", "対戦相手は『ヴォイド・アイスハウンド』の群れ。その咆哮は空気を凍らせ、その牙は魂の熱を奪い去る。", "", actor=lily) \
        .say("lily_4", "……もし、心臓の鼓動を止められたくないのであれば、あのおぞましい商人から何か『温かいもの』でも買い取っておくことでしたね。ま、今からでも遅くはありませんが。", "", actor=lily)

    # プレイヤーの選択肢（リリィ）
    builder.choice(lily_r1, "ゼクの薬は使わない。自分の力で勝つ", "", text_id="c_lily_1") \
           .choice(lily_r2, "準備は整っている。すぐに始めよう", "", text_id="c_lily_2") \
           .choice(lily_r3, "少し……待ってくれ", "", text_id="c_lily_3")

    # 選択肢反応: 自分の力で勝つ
    builder.step(lily_r1) \
        .say("lily_r1_1", "ふふ、自信はおありのようで。……では、凍り付いた死体にならないよう、お祈りしておりますね。", "", actor=lily) \
        .jump(scene2_balgas)

    # 選択肢反応: すぐに始めよう
    builder.step(lily_r2) \
        .say("lily_r2_1", "準備万端、と。頼もしいこと。……それでは、どうぞ。地獄の冷凍庫へ。", "", actor=lily) \
        .jump(scene2_balgas)

    # 選択肢反応: 待ってくれ
    builder.step(lily_r3) \
        .say("lily_r3_1", "おや、少し震えていますよ。……まあ、無理もありませんが。急ぎませんから、準備が整ったらお声掛けくださいませ。", "", actor=lily) \
        .jump(scene2_balgas)

    # ========================================
    # シーン2: バルガスの冷徹な眼差し
    # ========================================
    builder.step(scene2_balgas) \
        .say("narr_5", "（闘技場の門扉からは、身を切るような極寒の風が吹き荒れている。バルガスは分厚い外套に身を包み、凍りついた鉄格子を乱暴に叩いた。）", "", actor=pc) \
        .say("balgas_1", "おい、顔色が青白いぜ。戦う前から死体ごっこか？", "", actor=balgas) \
        .say("balgas_2", "いいか、寒さってのは『恐怖』と同じだ。一度足が止まれば、そこが終着駅だと思え。", "", actor=balgas) \
        .say("narr_6", "（彼は凍りついた門扉を蹴り、氷の破片を散らす。）", "", actor=pc) \
        .say("balgas_3", "奴らは群れで動く。一匹が吠えれば、次の一匹がお前の死角に回り込む。", "", actor=balgas) \
        .say("balgas_4", "常に動き続けろ。止まれば凍る、動けば血が巡る……単純な理屈だ。", "", actor=balgas) \
        .say("narr_7", "（彼は酒瓶を一口飲み、吐息を白く吐き出す。）", "", actor=pc) \
        .say("balgas_5", "……死にたくなければ、その体内の火種を絶やすんじゃねえぞ。生きる意志ってのは、案外そういうところから潰えていくもんだ。", "", actor=balgas)

    # プレイヤーの選択肢（バルガス）
    builder.choice(balgas_r1, "分かった。必ず生きて帰る", "", text_id="c_balgas_1") \
           .choice(balgas_r2, "動き続ける……覚えておく", "", text_id="c_balgas_2") \
           .choice(balgas_r3, "（無言で頷く）", "", text_id="c_balgas_3")

    # 選択肢反応: 必ず生きて帰る
    builder.step(balgas_r1) \
        .say("balgas_r1_1", "……ああ。その目だ。それを忘れるな。", "", actor=balgas) \
        .jump(battle_start)

    # 選択肢反応: 覚えておく
    builder.step(balgas_r2) \
        .say("balgas_r2_1", "覚えるんじゃねえ。体に刻み込め。", "", actor=balgas) \
        .jump(battle_start)

    # 選択肢反応: 無言で頷く
    builder.step(balgas_r3) \
        .say("balgas_r3_1", "……フン。行ってこい。", "", actor=balgas) \
        .jump(battle_start)

    # ========================================
    # シーン3: 戦闘開始
    # ========================================
    builder.step(battle_start) \
        .play_bgm("BGM/Battle_RankE_Ice") \
        .say("narr_8", "（ゲートが開いた瞬間、視界を覆うのは吹き荒れる銀世界の白。）", "", actor=pc) \
        .shake() \
        .say("narr_9", "（地面は氷に閉ざされ、踏みしめるたびに不吉な軋みを上げる。天井はなく、ただ虚無の闇と、そこから降り注ぐ氷の結晶。）", "", actor=pc) \
        .say("narr_10", "（突如、雪霧の奥から無数の青白い眼光が浮かび上がった。）", "", actor=pc) \
        .say("narr_11", "（それは、体躯が氷の結晶で形成された、異形の魔犬の群れ。彼らが喉を鳴らすたび、大気が結晶化して地面に降り注ぐ。）", "", actor=pc) \
        .say("narr_12", "（中央には、ひと際巨大な影——『零度の咆哮者（ゼロ・ロアラー）』が、獲物を見定めていた。）", "", actor=pc) \
        .say("narr_13", "（その体躯は他の個体の二倍以上。背中には鋭利な氷の棘が無数に生え、吐息だけで周囲の空気を凍らせる。）", "", actor=pc) \
        .start_battle_by_stage("rank_f_trial", master_id="sukutsu_arena_master") \
        .finish()


def add_rank_up_F_result_steps(builder: DramaBuilder, victory_label: str, defeat_label: str, return_label: str):
    """
    Rank F 昇格試験の勝利/敗北ステップを arena_master ビルダーに追加する

    Args:
        builder: arena_master の DramaBuilder インスタンス
        victory_label: 勝利ステップのラベル名
        defeat_label: 敗北ステップのラベル名
        return_label: 結果表示後にジャンプするラベル名
    """
    pc = Actors.PC
    lily = Actors.LILY
    balgas = Actors.BALGAS

    # ========================================
    # Rank F 昇格試験 勝利
    # ========================================
    after_reward_label_f = f"{victory_label}_after_reward"

    builder.step(victory_label) \
        .set_flag("sukutsu_arena_result", 0) \
        .play_bgm("BGM/Lobby_Normal") \
        .say("narr_v1", "（砕け散った氷の破片が砂に混じり、冷気がゆっくりと霧散していく。）", "", actor=pc) \
        .say("narr_v2", "（体温を奪われ、這うようにしてロビーに戻ったあなたを、バルガスが力強く、しかし乱暴に迎える。）", "", actor=pc) \
        .say("balgas_v1", "……ハッ！ 泥を啜ってでも生き残ったか。", "", actor=balgas) \
        .say("narr_v3", "（彼はあなたの肩を乱暴に叩く。その手は、熱を帯びている。）", "", actor=pc) \
        .say("balgas_v2", "いいぜ、その執念深さ。今の無様な姿こそ、このアリーナに相応しい。", "", actor=balgas) \
        .say("balgas_v3", "これで『屑肉』は卒業だ。今日からお前はランクF……泥にまみれても食らいつく『泥犬（Mud Dog）』だ。", "", actor=balgas) \
        .say("lily_v1", "おめでとうございます。報酬を選んでください。", "", actor=lily) \
        .complete_quest(QuestIds.RANK_UP_F)

    # 3択報酬選択
    add_reward_choice(
        builder,
        tier=get_reward_tier_for_rank("F"),
        choice_label_prefix="rup_f_reward",
        after_reward_label=after_reward_label_f,
        lily_actor=lily,
        pc_actor=pc
    )

    builder.step(after_reward_label_f) \
        .say("sys_title", "【システム】称号『泥犬（Mud Dog）』を獲得しました。耐久+3、冷気耐性+5 の加護を得た！", "") \
        .action("eval", param="Elin_SukutsuArena.ArenaManager.GrantRankFBonus();") \
        .set_flag(Keys.RANK, 2) \
        .jump(return_label)

    # ========================================
    # Rank F 昇格試験 敗北
    # ========================================
    builder.step(defeat_label) \
        .set_flag("sukutsu_arena_result", 0) \
        .say("lily_d1", "あらあら……。凍死は、思ったより早かったですね。", "", actor=lily) \
        .say("lily_d2", "死体袋の用意が無駄にならなくて何よりです。……次の方、どうぞ。", "", actor=lily) \
        .jump(return_label)
