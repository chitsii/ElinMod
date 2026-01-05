"""
15_vs_bulgas.md - 理を拒む者：師匠との最終決戦
Rank S昇格試験 - バルガスとの決戦と慈悲の選択
"""

from drama_builder import DramaBuilder
from flag_definitions import Keys, Actors, FlagValues

def define_vs_balgas(builder: DramaBuilder):
    """
    バルガス戦 - 最終決戦
    シナリオ: 15_vs_bulgas.md
    """
    # アクター登録
    pc = builder.register_actor(Actors.PC, "あなた", "You")
    balgas = builder.register_actor(Actors.BALGAS, "バルガス", "Balgas")
    lily = builder.register_actor(Actors.LILY, "リリィ", "Lily")
    zek = builder.register_actor(Actors.ZEK, "ゼク", "Zek")

    # ラベル定義
    main = builder.label("main")
    scene1 = builder.label("scene1_prime")
    scene2 = builder.label("scene2_lily_prayer")
    scene3 = builder.label("scene3_battle")
    scene4 = builder.label("scene4_refusal")
    choice4 = builder.label("choice4")
    react4_philosophy = builder.label("react4_philosophy")
    react4_rule = builder.label("react4_rule")
    react4_hand = builder.label("react4_hand")
    introspection = builder.label("introspection")
    introspect_greed = builder.label("introspect_greed")
    introspect_battle = builder.label("introspect_battle")
    introspect_void = builder.label("introspect_void")
    introspect_pride = builder.label("introspect_pride")
    introspect_done = builder.label("introspect_done")
    scene5 = builder.label("scene5_bonds")
    reward_choice = builder.label("reward_choice")
    reward_sword = builder.label("reward_sword")
    reward_ether = builder.label("reward_ether")
    reward_mana = builder.label("reward_mana")
    reward_end = builder.label("reward_end")
    final_choice = builder.label("final_choice")
    final_thanks = builder.label("final_thanks")
    final_human = builder.label("final_human")
    final_nod = builder.label("final_nod")
    ending = builder.label("ending")

    # ========================================
    # シーン1: 全盛期の幻影
    # ========================================
    builder.step(main) \
        .play_bgm("BGM/Ominous_Suspense_02") \
        .say("narr_1", "（ロビーの喧騒が消え、冷たい風が吹き抜ける。）", "", actor=pc) \
        .wait(0.5) \
        .say("narr_2", "（バルガスはいつになく整った足取りで、あなたの前に立った。）", "", actor=pc) \
        .wait(0.5) \
        .say("narr_3", "（その手には、ゼクから手に入れたと思わしき、ドクドクと脈打つ紫黒色の薬瓶が握られている。）", "", actor=pc) \
        .jump(scene1)

    builder.step(scene1) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_1", "……おい、黄金の戦鬼。お前はもう、俺の手の届かねえ高みへ行こうとしてやがる。", "", actor=balgas) \
        .wait(1.0) \
        .say("balgas_2", "だがな、アスタロト……あのドラゴンの首を獲るには、圧倒的な『暴力』だけじゃ足りねえ。", "", actor=balgas) \
        .wait(0.5) \
        .say("balgas_3", "俺を、この『全盛期の俺』を越えてみせろ。それができなきゃ、お前はただの強いだけの餌だ。", "", actor=balgas) \
        .wait(0.5) \
        .say("narr_4", "（バルガスは一気に薬を煽った。）", "", actor=pc) \
        .shake() \
        .wait(1.0) \
        .say("narr_5", "（瞬間、彼の全身を覆っていた古い傷跡が消え、萎みかけていた筋肉が鋼のように膨れ上がる。）", "", actor=pc) \
        .wait(0.5) \
        .say("narr_6", "（白髪は黒々とした輝きを取り戻し、放たれる闘気だけでアリーナの石壁に亀裂が入った。）", "", actor=pc) \
        .shake() \
        .wait(1.0) \
        .say("balgas_4", "……あぁ、いい気分だ。これなら、一度くらいはお前を本気で殺しにいける。", "", actor=balgas) \
        .wait(1.0) \
        .say("balgas_5", "来い！ 手加減は無しだ！ 俺を殺すつもりで打ってこい！", "", actor=balgas) \
        .jump(scene2)

    # ========================================
    # シーン2: リリィの絶望と祈り
    # ========================================
    builder.step(scene2) \
        .play_bgm("BGM/Lily_Seductive_Danger") \
        .say("narr_7", "（リリィが震える手で水晶を握りしめている。）", "", actor=pc) \
        .wait(0.5) \
        .say("narr_8", "（その瞳には、事務的な冷徹さは微塵も残っていない。）", "", actor=pc) \
        .focus_chara(Actors.LILY) \
        .say("lily_1", "……馬鹿な人。その薬は、命の火花を一度に使い果たす禁忌の炎……！", "", actor=lily) \
        .wait(1.0) \
        .say("lily_2", "お客様、お願いです。彼を止めて……！ でも、彼を殺さないで……。", "", actor=lily) \
        .wait(0.5) \
        .say("lily_3", "もし彼が死んだら、このアリーナにはもう、私を叱ってくれる人は誰もいなくなってしまうわ……！", "", actor=lily) \
        .wait(1.0) \
        .say("narr_9", "（リリィの頬を涙が伝う。サキュバスが泣いている。あなたは初めて見た。）", "", actor=pc) \
        .jump(scene3)

    # ========================================
    # シーン3: 闘技場：師弟の極致
    # ========================================
    builder.step(scene3) \
        .play_bgm("BGM/Battle_Balgas_Prime") \
        .say("narr_10", "（若き日の姿を取り戻した「伝説の戦士バルガス」との一騎打ち。）", "", actor=pc) \
        .wait(0.5) \
        .say("narr_11", "（彼の動きは重く、速く、そして無駄がない。）", "", actor=pc) \
        .wait(0.5) \
        .say("narr_12", "（かつて教えてもらった技の数々が、今度は殺意を持ってあなたを襲う。）", "", actor=pc) \
        .shake() \
        .wait(1.0) \
        .say("obs_1", "「殺せ！ 師匠を殺せ！」", "", actor=pc) \
        .say("obs_2", "「英雄の魂を捧げろ！」", "", actor=pc) \
        .say("obs_3", "「屠竜者となる儀式だ！」", "", actor=pc) \
        .wait(1.0) \
        .say("lily_voice", "（リリィの懇願の声が、闘技場に響く……「お願い……殺さないで……」）", "", actor=lily) \
        .wait(1.0) \
        .action("eval", param="UnityEngine.Debug.Log(\"[SukutsuArena] TODO: バルガス最終戦 - HP25%未満で一定ターン耐える\");") \
        .jump(scene4)

    # ========================================
    # シーン4: とどめの拒絶
    # ========================================
    builder.step(scene4) \
        .play_bgm("BGM/Emotional_Sorrow_2") \
        .say("narr_13", "（膝をつき、肩で息をするバルガス。）", "", actor=pc) \
        .wait(0.5) \
        .say("narr_14", "（全盛期の輝きが失われ、急速に元の老いた姿へと戻っていく。）", "", actor=pc) \
        .wait(0.5) \
        .say("narr_15", "（上空からは、観客たちの残酷な「処刑」を促す喝采が響き渡る。）", "", actor=pc) \
        .shake() \
        .wait(1.0) \
        .say("obs_void", "「……殺セ。英雄ノ魂ヲ捧ゲ、真ノ『屠竜者』ト成レ……。」", "", actor=pc) \
        .wait(1.0) \
        .say("narr_16", "（あなたは剣を引き、バルガスの喉元に突きつけた刃を下ろす。）", "", actor=pc) \
        .wait(1.0) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_6", "……な、何をしてやがる。……刺せ。それがアリーナの、戦士のケジメだろうが……！", "", actor=balgas) \
        .jump(choice4)

    # プレイヤーの選択肢4
    builder.choice(react4_philosophy, "俺の哲学には、師匠を殺すという項目はない", "", text_id="c4_philosophy") \
           .choice(react4_rule, "アリーナのルールに従うつもりはない。俺がルールだ", "", text_id="c4_rule") \
           .choice(react4_hand, "（無言で手を差し伸べる）", "", text_id="c4_hand")

    # 選択肢反応4
    builder.step(react4_philosophy) \
        .say("balgas_r1", "……ハッ。甘っちょろい野郎だ……。", "", actor=balgas) \
        .jump(introspection)

    builder.step(react4_rule) \
        .say("balgas_r2", "……傲慢な野郎だ。……だが、その傲慢が、俺が求めていた強さなのかもしれねえな……。", "", actor=balgas) \
        .jump(introspection)

    builder.step(react4_hand) \
        .say("balgas_r3", "……無口な野郎だ。……だが、その手は……温かいな……。", "", actor=balgas) \
        .jump(introspection)

    # ========================================
    # 内省：動機に応じた独白（switch_on_flagで安全に分岐）
    # ========================================
    builder.step(introspection) \
        .switch_on_flag(Keys.MOTIVATION, {
            FlagValues.Motivation.GREED: introspect_greed,
            FlagValues.Motivation.BATTLE_LUST: introspect_battle,
            FlagValues.Motivation.NIHILISM: introspect_void,
            FlagValues.Motivation.ARROGANCE: introspect_pride,
        }, fallback=introspect_done)

    # 強欲ルート
    builder.step(introspect_greed) \
        .say("intro_greed", "（あの時、俺は「富と名声」のためにこのアリーナに来た。）", "", actor=pc) \
        .wait(1.0) \
        .say("intro_greed2", "（だが今、俺の手にあるのは金でも権力でもなく……この老いた戦士の命だ。）", "", actor=pc) \
        .wait(0.5) \
        .say("intro_greed3", "（こんなもの、何の得にもならない。……それでも、手放せないんだ。）", "", actor=pc) \
        .jump(introspect_done)

    # 戦闘狂ルート
    builder.step(introspect_battle) \
        .say("intro_battle", "（あの時、俺は「強い奴と戦いたい」とだけ思っていた。）", "", actor=pc) \
        .wait(1.0) \
        .say("intro_battle2", "（目の前の敵を倒し、次の敵へ。それだけでよかった。）", "", actor=pc) \
        .wait(0.5) \
        .say("intro_battle3", "（……だが、バルガスを殺すことは『勝利』じゃない。ただの『喪失』だ。俺は、そんなことのために剣を振ってきたんじゃない。）", "", actor=pc) \
        .jump(introspect_done)

    # 虚無ルート
    builder.step(introspect_void) \
        .say("intro_void", "（あの時、俺には帰る場所がなかった。どこで死のうと同じだと思っていた。）", "", actor=pc) \
        .wait(1.0) \
        .say("intro_void2", "（……だが、今は違う。バルガスがいて、リリィがいて……）", "", actor=pc) \
        .wait(0.5) \
        .say("intro_void3", "（ここには、俺を待っている奴らがいる。もう、虚無に逃げることはできない。）", "", actor=pc) \
        .jump(introspect_done)

    # 傲慢ルート
    builder.step(introspect_pride) \
        .say("intro_pride", "（あの時、俺は「このアリーナも、ドラゴンも支配する」と豪語した。）", "", actor=pc) \
        .wait(1.0) \
        .say("intro_pride2", "（……だが、支配とは何だ？ 命令に従わせることか？ 恐怖で屈服させることか？）", "", actor=pc) \
        .wait(0.5) \
        .say("intro_pride3", "（違う。本当の強さは……弱った者を踏みつけないことだ。バルガスがそれを教えてくれた。）", "", actor=pc) \
        .jump(introspect_done)

    builder.step(introspect_done) \
        .jump(scene5)

    # ========================================
    # シーン5: 新たな絆
    # ========================================
    builder.step(scene5) \
        .play_bgm("BGM/Emotional_Sacred_Triumph_Special") \
        .say("narr_17", "（あなたがバルガスの手を取り、立ち上がらせる。）", "", actor=pc) \
        .wait(1.0) \
        .say("narr_18", "（その瞬間、アリーナ全体を包んでいた不気味な魔力が霧散し、観客たちの声が落胆の溜息へと変わる。）", "", actor=pc) \
        .wait(0.5) \
        .say("narr_19", "（リリィが駆け寄り、泣きながらバルガスに回復魔法を注ぎ込む。）", "", actor=pc) \
        .focus_chara(Actors.LILY) \
        .wait(0.5) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_7", "……ハッ。甘っちょろい野郎だ。……だが、その甘さが、俺がカインに教えてやれなかった『本物の強さ』なのかもしれねえな。", "", actor=balgas) \
        .wait(1.0) \
        .say("balgas_8", "……負けたよ。今日からお前がランクS『屠竜者（Dragon Slayer）』だ。", "", actor=balgas) \
        .wait(0.5) \
        .say("balgas_9", "俺はもう引退だ。これからは、ただの酔いどれの『隠居』として、お前の凱旋をここで待たせてもらうぜ。", "", actor=balgas) \
        .wait(1.0) \
        .say("narr_20", "（リリィは台帳を開き、涙を拭きながら何かを書き込む。）", "", actor=pc) \
        .focus_chara(Actors.LILY) \
        .say("lily_4", "……ありがとう。本当に、ありがとうございます。", "", actor=lily) \
        .wait(0.5) \
        .say("lily_5", "観客からの報酬として、小さなコイン50枚とプラチナコイン30枚。それと、戦闘記録として素材を一つ選んでいただけます。", "", actor=lily) \
        .jump(reward_choice)

    # 報酬選択肢
    builder.choice(reward_sword, "バルガスの剣の欠片を頼む", "", text_id="c_reward_sword") \
           .choice(reward_ether, "エーテルの欠片が欲しい", "", text_id="c_reward_ether") \
           .choice(reward_mana, "魔力の結晶を選ぶ", "", text_id="c_reward_mana")

    builder.step(reward_sword) \
        .say("lily_rew1", "『バルガスの剣の欠片×1』、記録いたしました。……彼の魂が宿る、大切な欠片ですね。", "", actor=lily) \
        .action("eval", param="EClass.pc.Pick(ThingGen.Create(\"fragment_balgas_sword\"));") \
        .jump(reward_end)

    builder.step(reward_ether) \
        .say("lily_rew2", "『エーテルの欠片×1』、記録いたしました。", "", actor=lily) \
        .action("eval", param="EClass.pc.Pick(ThingGen.Create(\"fragment_ether\"));") \
        .jump(reward_end)

    builder.step(reward_mana) \
        .say("lily_rew3", "『魔力の結晶×1』、記録いたしました。", "", actor=lily) \
        .action("eval", param="EClass.pc.Pick(ThingGen.Create(\"gem_mana\"));") \
        .jump(reward_end)

    builder.step(reward_end) \
        .action("eval", param="for(int i=0; i<50; i++) { EClass.pc.Pick(ThingGen.Create(\"coin\")); } for(int i=0; i<30; i++) { EClass.pc.Pick(ThingGen.Create(\"plat\")); }") \
        .say("lily_6", "記録完了です。", "", actor=lily) \
        .wait(0.5) \
        .say("lily_7", "……それと、今回の戦いで、あなたは『理を拒む者』としての称号を獲得しました。", "", actor=lily) \
        .wait(0.5) \
        .say("lily_8", "アリーナの命令を拒絶し、師匠を生かす……ふふ、あなたは本当に、システムの『バグ』ですね。", "", actor=lily) \
        .wait(1.0) \
        .say("narr_21", "（影の中から、ゼクが見つめている。）", "", actor=pc) \
        .focus_chara(Actors.ZEK) \
        .say("zek_1", "……クク。システムの命令を拒絶しましたか。", "", actor=zek) \
        .wait(0.5) \
        .say("zek_2", "面白い。実に面白い。あなたは『黄金』を超え、ついにこの箱庭の『バグ』として完成した。", "", actor=zek) \
        .wait(1.0) \
        .say("zek_3", "さあ、アスタロトはすぐそこです。……あなたのその『慈悲』が、あの孤独な竜に届くのかどうか、見せてもらいましょう。", "", actor=zek) \
        .wait(0.5) \
        .say("narr_22", "（ゼクが影の中へと消えていく。）", "", actor=pc) \
        .jump(final_choice)

    # 最終選択肢
    builder.choice(final_thanks, "バルガス、ありがとう", "", text_id="c_final_thanks") \
           .choice(final_human, "俺は……まだ人間か？", "", text_id="c_final_human") \
           .choice(final_nod, "（無言で頷く）", "", text_id="c_final_nod")

    builder.step(final_thanks) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_r4", "……ハッ、礼はいらねえ。生き残って、アスタロトをぶっ倒せ。", "", actor=balgas) \
        .jump(ending)

    builder.step(final_human) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_r5", "……ああ。少なくとも、まだ仲間を守れるだけの心がある。それが証拠だ。", "", actor=balgas) \
        .jump(ending)

    builder.step(final_nod) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_r6", "……よし。じゃあ行け。俺は、ここで待ってるぜ。", "", actor=balgas) \
        .jump(ending)

    # ========================================
    # 終了処理
    # ========================================
    builder.step(ending) \
        .set_flag(Keys.RANK, 7) \
        .set_flag(Keys.REL_BALGAS, 100) \
        .mod_flag(Keys.REL_LILY, "+", 30) \
        .set_flag(Keys.BALGAS_CHOICE, FlagValues.BalgasChoice.SPARED) \
        .say("sys_title", "【システム】称号『理を拒む者（System Breaker）』を獲得しました。", "", actor=pc) \
        .say("sys_buff", "【システム】バルガスの加護（永続）を獲得しました。", "", actor=pc) \
        .action("eval", param="UnityEngine.Debug.Log(\"[SukutsuArena] TODO: 称号付与 - 状態異常耐性+30%, ピンチ時にバルガス加勢\");") \
        .action("eval", param="UnityEngine.Debug.Log(\"[SukutsuArena] TODO: バフ付与 - 全スキル消費コスト-20%, バルガス幻影加勢\");") \
        .finish()
