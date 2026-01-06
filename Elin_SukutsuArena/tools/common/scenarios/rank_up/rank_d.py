# -*- coding: utf-8 -*-
"""
10_rank_up_D.md - Rank D 昇格試験『銅貨稼ぎの洗礼』
観客の介入が本格化する戦い
"""

from drama_builder import DramaBuilder
from flag_definitions import Keys, Rank, Actors, QuestIds

def define_rank_up_D(builder: DramaBuilder):
    """
    Rank D 昇格試験「銅貨稼ぎの洗礼」
    シナリオ: 10_rank_up_D.md
    """
    # アクター登録
    pc = builder.register_actor(Actors.PC, "あなた", "You")
    lily = builder.register_actor(Actors.LILY, "リリィ", "Lily")
    balgas = builder.register_actor(Actors.BALGAS, "バルガス", "Balgas")

    # ラベル定義
    main = builder.label("main")
    scene1 = builder.label("scene1_announcement")
    choice1 = builder.label("choice1")
    react1_audience = builder.label("react1_audience")
    react1_items = builder.label("react1_items")
    react1_silent = builder.label("react1_silent")
    scene2 = builder.label("scene2_balgas_warning")
    choice2 = builder.label("choice2")
    react2_dodge = builder.label("react2_dodge")
    react2_use = builder.label("react2_use")
    react2_nod = builder.label("react2_nod")
    battle_start = builder.label("battle_start")

    # ========================================
    # シーン1: リリィの宣告
    # ========================================
    builder.step(main) \
        .play_bgm("BGM/Lobby_Normal") \
        .say("narr_1", "（ロビーに戻ったあなたを、リリィが妖艶な笑みで迎える。）", "", actor=pc) \
        .say("narr_2", "（彼女の台帳には、あなたの戦績と共に、新たな「試練」の記録が追加されている。）", "", actor=pc) \
        .jump(scene1)

    builder.step(scene1) \
        .focus_chara(Actors.LILY) \
        .say("lily_1", "……お疲れ様でした。カインさんの魂を巡る選択、興味深く拝見させていただきました。", "", actor=lily) \
        .say("lily_2", "さて、次はRank D『銅貨稼ぎ（Copper Earner）』への昇格試験です。", "", actor=lily) \
        .say("lily_3", "ここからは、ただ敵を倒すだけでは不十分。観客の皆様を『満足』させる必要があります。", "", actor=lily) \
        .say("lily_4", "彼らが退屈すれば、あなたに『プレゼント』が降ってきます。", "", actor=lily) \
        .say("narr_3", "（彼女は指を鳴らす。すると、ロビーの天井から突如、石塊が落下してきた。）", "", actor=pc) \
        .shake() \
        .say("lily_5", "……ふふ、驚きました？ これが『観客の介入』です。", "", actor=lily) \
        .say("lily_6", "戦闘中、あなたの頭上から様々な物が降ってきます。石、薬、武器……時には爆発物も。", "", actor=lily) \
        .say("lily_7", "それらを避けながら、あるいは利用しながら戦う……それがRank Dの『芸』ですよ。", "", actor=lily)

    # プレイヤーの選択肢1
    builder.choice(react1_audience, "観客を止められないのか？", "", text_id="c1_audience") \
           .choice(react1_items, "どんな物が降ってくる？", "", text_id="c1_items") \
           .choice(react1_silent, "（無言で聞く）", "", text_id="c1_silent")

    # 選択肢反応1
    builder.step(react1_audience) \
        .say("lily_r1", "無理です。観客は次元の外側から私たちを見ている存在。手が届きません。……諦めて、楽しませてあげてください。", "", actor=lily) \
        .jump(scene2)

    builder.step(react1_items) \
        .say("lily_r2", "ランダムです。ポーションが降ってくることもあれば、鉄の塊が頭に直撃することも。……運を祈ってくださいね？", "", actor=lily) \
        .jump(scene2)

    builder.step(react1_silent) \
        .say("lily_r3", "……無口ですが、理解はされたようですね。では、バルガスさんからも一言。", "", actor=lily) \
        .jump(scene2)

    # ========================================
    # シーン2: バルガスの実践的助言
    # ========================================
    builder.step(scene2) \
        .play_bgm("BGM/Ominous_Suspense_01") \
        .focus_chara(Actors.BALGAS) \
        .say("narr_4", "（バルガスが近づいてくる。その表情はいつになく真剣だ。）", "", actor=pc) \
        .say("balgas_1", "……おい、銅貨稼ぎ予備軍。", "", actor=balgas) \
        .say("balgas_2", "観客のヤジは、ただの嫌がらせじゃねえ。戦況を一変させる『変数』だ。", "", actor=balgas) \
        .say("balgas_3", "石が降ってきたら、敵に当たるように誘導しろ。薬が降ってきたら、素早く拾って飲め。", "", actor=balgas) \
        .say("balgas_4", "爆発物が降ってきたら……全力で逃げろ。", "", actor=balgas) \
        .say("balgas_5", "大事なのは、『動き続ける』ことだ。止まれば的になる。", "", actor=balgas) \
        .say("balgas_6", "それと……観客を楽しませることも忘れるな。派手に戦えば、良い物が降ってくる確率が上がる。", "", actor=balgas) \
        .say("balgas_7", "……まあ、お前なら大丈夫だろう。行ってこい。", "", actor=balgas)

    # プレイヤーの選択肢2
    builder.choice(react2_dodge, "避けることに集中する", "", text_id="c2_dodge") \
           .choice(react2_use, "落下物を利用してみせる", "", text_id="c2_use") \
           .choice(react2_nod, "（無言で頷く）", "", text_id="c2_nod")

    # 選択肢反応2
    builder.step(react2_dodge) \
        .say("balgas_r1", "賢明だ。まずは生き残ることが最優先だからな。", "", actor=balgas) \
        .jump(battle_start)

    builder.step(react2_use) \
        .say("balgas_r2", "ハッ、強気だな。だが、その意気込みは悪くねえ。", "", actor=balgas) \
        .jump(battle_start)

    builder.step(react2_nod) \
        .say("balgas_r3", "……よし。じゃあ行け。死ぬなよ。", "", actor=balgas) \
        .jump(battle_start)

    # ========================================
    # シーン3: 戦闘開始
    # ========================================
    builder.step(battle_start) \
        .play_bgm("BGM/Battle_Audience_Chaos") \
        .say("narr_5", "（闘技場の門を潜ると、既に観客たちの熱気が空気を震わせている。）", "", actor=pc) \
        .say("narr_6", "（砂地の中央には、今回の対戦相手『次元の剣闘士』が三体、武器を構えて待ち構えていた。）", "", actor=pc) \
        .say("narr_7", "（リリィの声が、魔術的な拡声によって会場全体に響き渡る。）", "", actor=pc) \
        .focus_chara(Actors.LILY) \
        .say("lily_ann1", "……皆様、本日のメインディッシュです！", "", actor=lily) \
        .say("lily_ann2", "新たな『銅貨稼ぎ』候補による、命懸けのサーカスをお楽しみください！", "", actor=lily) \
        .say("narr_8", "（戦いが始まった瞬間、頭上の虚空が紫色に光り、何かが降ってくる音が響いた……！）", "", actor=pc) \
        .shake() \
        .start_battle_by_stage("rank_d_trial", master_id="sukutsu_arena_master") \
        .finish()


def add_rank_up_D_result_steps(builder: DramaBuilder, victory_label: str, defeat_label: str, return_label: str):
    """
    Rank D 昇格試験の勝利/敗北ステップを arena_master ビルダーに追加する

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
    # Rank D 昇格試験 勝利
    # ========================================
    builder.step(victory_label) \
        .set_flag("sukutsu_arena_result", 0) \
        .play_bgm("BGM/Fanfare_Audience") \
        .say("narr_v1", "（最後の敵が倒れた瞬間、観客たちの歓声が一気に爆発した。）", "", actor=pc) \
        .say("narr_v2", "（砂地には、戦闘中に降ってきた無数の物品が散乱している。石塊、割れた薬瓶、曲がった剣……。）", "", actor=pc) \
        .say("narr_v3", "（ロビーに戻ると、リリィが満足げに微笑んでいた。）", "", actor=pc) \
        .focus_chara(Actors.LILY) \
        .say("lily_v1", "……素晴らしい。観客の皆様も、大変お喜びでしたよ。", "", actor=lily) \
        .say("lily_v2", "落下物を巧みに避け、時には利用する。その立ち回り、まさに『銅貨稼ぎ』の名に相応しい。", "", actor=lily) \
        .focus_chara(Actors.BALGAS) \
        .say("narr_v4", "（バルガスが酒瓶を傾けながら近づいてくる。）", "", actor=pc) \
        .say("balgas_v1", "……ケッ、やるじゃねえか。", "", actor=balgas) \
        .say("balgas_v2", "お前は今、ただの『鉄屑』から、観客に媚びを売って生き延びる『銅貨稼ぎ』になった。", "", actor=balgas) \
        .say("balgas_v3", "誇れることじゃねえが……生き残るためには必要なスキルだ。", "", actor=balgas) \
        .focus_chara(Actors.LILY) \
        .say("lily_v3", "では、報酬の授与です。", "", actor=lily) \
        .say("lily_v4", "観客からの投げ銭……小さなコイン12枚とプラチナコイン4枚。それと、戦闘記録として素材を一つ選んでいただけます。", "", actor=lily)

    # 報酬選択肢 (ラベル名に _d サフィックスを付けて衝突を回避)
    reward_stone_d = builder.label("reward_stone_d")
    reward_potion_d = builder.label("reward_potion_d")
    reward_iron_d = builder.label("reward_iron_d")
    reward_end_d = builder.label("reward_end_d")

    builder.choice(reward_stone_d, "石材を頼む", "", text_id="c_reward_stone_d") \
           .choice(reward_potion_d, "ポーションが欲しい", "", text_id="c_reward_potion_d") \
           .choice(reward_iron_d, "鉄の欠片を選ぶ", "", text_id="c_reward_iron_d")

    builder.step(reward_stone_d) \
        .say("lily_rew1_d", "『石材×1』、記録いたしました。落下物の記憶ですね。", "", actor=lily) \
        .action("eval", param="EClass.pc.Pick(ThingGen.Create(\"stone\"));") \
        .jump(reward_end_d)

    builder.step(reward_potion_d) \
        .say("lily_rew2_d", "『ポーション×1』、記録いたしました。……次も、降ってくるといいですね。", "", actor=lily) \
        .action("eval", param="EClass.pc.Pick(ThingGen.Create(\"potion_minor\"));") \
        .jump(reward_end_d)

    builder.step(reward_iron_d) \
        .say("lily_rew3_d", "『鉄の欠片×1』ですね。……実用的です。", "", actor=lily) \
        .action("eval", param="EClass.pc.Pick(ThingGen.Create(\"fragment_iron\"));") \
        .jump(reward_end_d)

    builder.step(reward_end_d) \
        .action("eval", param="for(int i=0; i<12; i++) { EClass.pc.Pick(ThingGen.Create(\"coin\")); } for(int i=0; i<4; i++) { EClass.pc.Pick(ThingGen.Create(\"plat\")); }") \
        .say("lily_v5", "記録完了です。", "", actor=lily) \
        .say("lily_v6", "……それと、今回の戦いで、あなたは観客の『ヤジ』を避けるコツを掴んだようですね。", "", actor=lily) \
        .say("lily_v7", "次からは、もっと酷いものが降ってきます。……覚悟しておいてくださいね？", "", actor=lily) \
        .complete_quest(QuestIds.RANK_UP_D) \
        .set_flag(Keys.RANK, 4) \
        .mod_flag(Keys.REL_LILY, "+", 10) \
        .say("sys_title", "【システム】称号『銅貨稼ぎ（Copper Earner）』を獲得しました。回避+5、運+3 の加護を得た！", "") \
        .action("eval", param="Elin_SukutsuArena.ArenaManager.GrantRankDBonus();") \
        .jump(return_label)

    # ========================================
    # Rank D 昇格試験 敗北
    # ========================================
    builder.step(defeat_label) \
        .set_flag("sukutsu_arena_result", 0) \
        .play_bgm("BGM/Lobby_Normal") \
        .focus_chara(Actors.LILY) \
        .say("lily_d1", "……あらあら、落下物に潰されてしまいましたね。", "", actor=lily) \
        .say("lily_d2", "観客の皆様も、少し期待外れだったようです。", "", actor=lily) \
        .say("lily_d3", "準備が整ったら、また挑戦してください。次はもっと上手く避けられるといいですね。", "", actor=lily) \
        .jump(return_label)
