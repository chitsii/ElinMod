# -*- coding: utf-8 -*-
"""
11_rank_up_C.md - Rank C 昇格試験『闘技場の鴉』
英雄の残党との戦い
"""

from drama_builder import DramaBuilder
from flag_definitions import Keys, Rank

def define_rank_up_C(builder: DramaBuilder):
    """
    Rank C 昇格試験「闘技場の鴉」
    シナリオ: 11_rank_up_C.md
    """
    # アクター登録
    pc = builder.register_actor("pc", "あなた", "You")
    lily = builder.register_actor("sukutsu_receptionist", "リリィ", "Lily")
    balgas = builder.register_actor("sukutsu_arena_master", "バルガス", "Balgas")

    # ラベル定義
    main = builder.label("main")
    scene1 = builder.label("scene1_heroes")
    choice1 = builder.label("choice1")
    react1_who = builder.label("react1_who")
    react1_strong = builder.label("react1_strong")
    react1_silent = builder.label("react1_silent")
    scene2 = builder.label("scene2_balgas_grief")
    choice2 = builder.label("choice2")
    react2_mercy = builder.label("react2_mercy")
    react2_necessary = builder.label("react2_necessary")
    react2_nod = builder.label("react2_nod")
    battle_start = builder.label("battle_start")

    # ========================================
    # シーン1: 堕ちた英雄たち
    # ========================================
    builder.step(main) \
        .play_bgm("BGM/Ominous_Suspense_01") \
        .say("narr_1", "（ロビーの空気が重い。）", "", actor=pc) \
        .say("narr_2", "（バルガスは珍しく酒瓶を手にせず、険しい表情で闘技場の門を見つめている。）", "", actor=pc) \
        .say("narr_3", "（リリィも、いつもの妖艶な笑みを消し、羊皮紙を静かに整理していた。）", "", actor=pc) \
        .jump(scene1)

    builder.step(scene1) \
        .focus_chara("sukutsu_arena_master") \
        .say("balgas_1", "……おい、銅貨稼ぎ。", "", actor=balgas) \
        .say("balgas_2", "次の試験は……俺にとっても、お前にとっても、辛いもんになる。", "", actor=balgas) \
        .say("balgas_3", "対戦相手は『堕ちた英雄たちの残党』だ。", "", actor=balgas) \
        .say("balgas_4", "……かつて、俺と一緒に地獄を這いずり回った仲間たちだ。カインのように、このアリーナに魂を食い尽くされ、ただの戦闘人形と化した連中だ。", "", actor=balgas) \
        .say("narr_4", "（彼は拳を握りしめる。）", "", actor=pc) \
        .say("balgas_5", "あいつらは、もう『人間』じゃねえ。だが……俺にとっては、今でも仲間だ。", "", actor=balgas) \
        .say("balgas_6", "お前が戦うのは、そんな連中だ。……覚悟はあるか？", "", actor=balgas)

    # プレイヤーの選択肢1
    builder.choice(react1_who, "どんな相手だ？", "", text_id="c1_who") \
           .choice(react1_strong, "強いのか？", "", text_id="c1_strong") \
           .choice(react1_silent, "（無言で聞く）", "", text_id="c1_silent")

    # 選択肢反応1
    builder.step(react1_who) \
        .say("balgas_r1", "……剣士、弓使い、魔導師。俺たちが誇った『黄金のトライアングル』だ。", "", actor=balgas) \
        .jump(scene2)

    builder.step(react1_strong) \
        .say("balgas_r2", "ああ。カインよりも、もっと強い。……だが、お前なら勝てる。", "", actor=balgas) \
        .jump(scene2)

    builder.step(react1_silent) \
        .say("balgas_r3", "……まあ、黙って聞いててくれ。続きがある。", "", actor=balgas) \
        .jump(scene2)

    # ========================================
    # シーン2: バルガスの悲痛な願い
    # ========================================
    builder.step(scene2) \
        .play_bgm("BGM/Emotional_Sorrow") \
        .say("narr_5", "（バルガスは深く息を吐く。）", "", actor=pc) \
        .say("balgas_7", "……頼む。あいつらを、この地獄から解放してやってくれ。", "", actor=balgas) \
        .say("balgas_8", "俺には……もう、仲間を救う力がねえ。だが、お前なら……お前ならできる。", "", actor=balgas) \
        .say("narr_6", "（リリィが近づいてくる。）", "", actor=pc) \
        .focus_chara("sukutsu_receptionist") \
        .say("lily_1", "……お客様。", "", actor=lily) \
        .say("lily_2", "彼らは『英雄』でした。ですが、今は……ただの『記憶』です。", "", actor=lily) \
        .say("lily_3", "あなたがどれほど優しく戦っても、彼らに意識は戻りません。", "", actor=lily) \
        .say("lily_4", "……ですが、倒すことで、彼らの魂はこの牢獄から解放されます。", "", actor=lily) \
        .say("lily_5", "これは、慈悲の戦いです。……準備はよろしいですか？", "", actor=lily)

    # プレイヤーの選択肢2
    builder.choice(react2_mercy, "……慈悲か。分かった", "", text_id="c2_mercy") \
           .choice(react2_necessary, "必要なことなら、やる", "", text_id="c2_necessary") \
           .choice(react2_nod, "（無言で頷く）", "", text_id="c2_nod")

    # 選択肢反応2
    builder.step(react2_mercy) \
        .say("lily_r4", "……ええ。あなたなら、きっと。", "", actor=lily) \
        .jump(battle_start)

    builder.step(react2_necessary) \
        .say("lily_r5", "……強い方ですね。では、お任せします。", "", actor=lily) \
        .jump(battle_start)

    builder.step(react2_nod) \
        .say("lily_r6", "……無口ですが、覚悟は決まったようですね。", "", actor=lily) \
        .jump(battle_start)

    # ========================================
    # シーン3: 戦闘開始
    # ========================================
    builder.step(battle_start) \
        .play_bgm("BGM/Battle_RankC_Heroic_Lament") \
        .say("narr_7", "（闘技場の門を潜ると、砂地の中央に三つの影が立っていた。）", "", actor=pc) \
        .say("narr_8", "（錆びついた鎧を纏う剣士、ボロボロのローブを羽織る魔導師、折れた弓を持つ弓使い。）", "", actor=pc) \
        .say("narr_9", "（彼らの瞳には光がなく、ただ機械的に武器を構えている。）", "", actor=pc) \
        .say("narr_10", "（だが、その動きには……かつての『誇り』の残滓が、微かに残っているように見えた。）", "", actor=pc) \
        .shake() \
        .say("obs_1", "（観客の声：「……堕ちた英雄たちか。哀れだな」）", "", actor=pc) \
        .say("obs_2", "（観客の声：「賭けは『新人が感情に飲まれて敗北』で」）", "", actor=pc) \
        .say("obs_3", "（観客の声：「いや、この新人は……冷静に戦うだろう」）", "", actor=pc) \
        .say("narr_11", "（バルガスの声が、遠くから聞こえる。）", "", actor=pc) \
        .focus_chara("sukutsu_arena_master") \
        .say("balgas_echo", "……頼んだぞ。", "", actor=balgas) \
        .start_battle(5, is_rank_up=True, master_id="sukutsu_arena_master") \
        .finish()


def add_rank_up_C_result_steps(builder: DramaBuilder, victory_label: str, defeat_label: str, return_label: str):
    """
    Rank C 昇格試験の勝利/敗北ステップを arena_master ビルダーに追加する

    Args:
        builder: arena_master の DramaBuilder インスタンス
        victory_label: 勝利ステップのラベル名
        defeat_label: 敗北ステップのラベル名
        return_label: 結果表示後にジャンプするラベル名
    """
    pc = "pc"
    lily = "sukutsu_receptionist"
    balgas = "sukutsu_arena_master"

    # ========================================
    # Rank C 昇格試験 勝利
    # ========================================
    builder.step(victory_label) \
        .set_flag("sukutsu_arena_result", 0) \
        .play_bgm("BGM/Emotional_Sacred_Triumph_Special") \
        .say("narr_v1", "（最後の英雄が倒れた瞬間、その体が光の粒子となって消えていく。）", "", actor=pc) \
        .say("narr_v2", "（彼らの顔に、一瞬だけ……安堵の表情が浮かんだように見えた。）", "", actor=pc) \
        .say("narr_v3", "（静寂の中、ロビーに戻ると、バルガスが背を向けたまま待っている。）", "", actor=pc) \
        .focus_chara("sukutsu_arena_master") \
        .say("balgas_v1", "……終わったか。", "", actor=balgas) \
        .say("narr_v4", "（彼はゆっくりと振り返る。その目には涙の跡。）", "", actor=pc) \
        .say("balgas_v2", "……ありがよ。", "", actor=balgas) \
        .say("balgas_v3", "あいつらは、お前のおかげでようやく……この地獄から出られた。", "", actor=balgas) \
        .say("balgas_v4", "お前は今、ただの『銅貨稼ぎ』じゃねえ。", "", actor=balgas) \
        .say("balgas_v5", "死肉を喰らい、戦場を飛び回り、そして仲間の魂を救う……『闘技場の鴉（Arena Crow）』だ。", "", actor=balgas) \
        .say("narr_v5", "（リリィが近づいてくる。）", "", actor=pc) \
        .focus_chara("sukutsu_receptionist") \
        .say("lily_v1", "……素晴らしい戦いでした。", "", actor=lily) \
        .say("lily_v2", "観客の皆様も、あなたの『慈悲』に感動されていたようです。", "", actor=lily) \
        .say("lily_v3", "では、報酬の授与です。", "", actor=lily) \
        .say("lily_v4", "観客からの祝福……小さなコイン15枚とプラチナコイン6枚。それと、英雄たちが遺した素材を一つ選んでいただけます。", "", actor=lily)

    # 報酬選択肢 (ラベル名に _c サフィックスを付けて衝突を回避)
    reward_sword_c = builder.label("reward_sword_c")
    reward_scroll_c = builder.label("reward_scroll_c")
    reward_steel_c = builder.label("reward_steel_c")
    reward_end_c = builder.label("reward_end_c")

    builder.choice(reward_sword_c, "錆びた剣の欠片を頼む", "", text_id="c_reward_sword_c") \
           .choice(reward_scroll_c, "古い魔導書の断片が欲しい", "", text_id="c_reward_scroll_c") \
           .choice(reward_steel_c, "鋼鉄の欠片を選ぶ", "", text_id="c_reward_steel_c")

    builder.step(reward_sword_c) \
        .say("lily_rew1_c", "『錆びた剣の欠片×1』、記録いたしました。英雄の記憶ですね。", "", actor=lily) \
        .action("eval", param="EClass.pc.Pick(ThingGen.Create(\"fragment_rusty_sword\"));") \
        .jump(reward_end_c)

    builder.step(reward_scroll_c) \
        .say("lily_rew2_c", "『古い魔導書の断片×1』、記録いたしました。……かつての知識の残滓です。", "", actor=lily) \
        .action("eval", param="EClass.pc.Pick(ThingGen.Create(\"scroll_ancient\"));") \
        .jump(reward_end_c)

    builder.step(reward_steel_c) \
        .say("lily_rew3_c", "『鋼鉄の欠片×1』ですね。……実用的です。", "", actor=lily) \
        .action("eval", param="EClass.pc.Pick(ThingGen.Create(\"steel\"));") \
        .jump(reward_end_c)

    builder.step(reward_end_c) \
        .action("eval", param="for(int i=0; i<15; i++) { EClass.pc.Pick(ThingGen.Create(\"coin\")); } for(int i=0; i<6; i++) { EClass.pc.Pick(ThingGen.Create(\"plat\")); }") \
        .say("lily_v5", "記録完了です。", "", actor=lily) \
        .say("lily_v6", "……あなたは今、このアリーナで生き残るための『鋼の心』を手に入れました。", "", actor=lily) \
        .say("lily_v7", "次は、さらなる試練が待っています。……準備が整ったら、また声をかけてくださいね？", "", actor=lily) \
        .complete_quest("09_rank_up_C") \
        .set_flag(Keys.RANK, 5) \
        .mod_flag(Keys.REL_BALGAS, "+", 25) \
        .mod_flag(Keys.REL_LILY, "+", 10) \
        .say("sys_title", "【システム】称号『闘技場の鴉（Arena Crow）』を獲得しました。", "", actor=pc) \
        .action("eval", param="UnityEngine.Debug.Log(\"[SukutsuArena] TODO: 称号付与処理 - クリティカル率+10%, 敵撃破時SP微回復\");") \
        .jump(return_label)

    # ========================================
    # Rank C 昇格試験 敗北
    # ========================================
    builder.step(defeat_label) \
        .set_flag("sukutsu_arena_result", 0) \
        .play_bgm("BGM/Lobby_Normal") \
        .focus_chara("sukutsu_arena_master") \
        .say("balgas_d1", "……チッ。", "", actor=balgas) \
        .say("balgas_d2", "まだ、お前には早かったか。", "", actor=balgas) \
        .say("balgas_d3", "……準備が整ったら、また来い。あいつらは、待ってる。", "", actor=balgas) \
        .jump(return_label)
