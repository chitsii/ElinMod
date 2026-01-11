"""
15_vs_bulgas.md - 理を拒む者：師匠との最終決戦
Rank S昇格試験 - バルガスとの決戦と慈悲の選択
"""

from arena_drama_builder import ArenaDramaBuilder
from drama_builder import DramaBuilder
from flag_definitions import Keys, Actors, FlagValues, QuestIds

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
    scene1_5 = builder.label("scene1_5_flashback")
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
        .say("narr_2", "（バルガスはいつになく整った足取りで、あなたの前に立った。）", "", actor=pc) \
        .say("narr_3", "（その手には、ゼクから手に入れたと思わしき、ドクドクと脈打つ紫黒色の薬瓶が握られている。）", "", actor=pc) \
        .jump(scene1)

    builder.step(scene1) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_1", "……おい、黄金の戦鬼。お前はもう、俺の手の届かねえ高みへ行こうとしてやがる。", "", actor=balgas) \
        .say("balgas_2", "だがな、それでもアスタロト……あの竜神は、別格なんだ。", "", actor=balgas) \
        .say("balgas_2_1", "だからこそ、ここで俺が試金石になってやる。おまえを倒すために、対戦させてもらう。冗談じゃねえぞ。", "", actor=balgas) \
        .say("balgas_3", "俺を、この『全盛期の俺』を越えてみせろ。それができなきゃ、お前は犠牲になっちまうだけだ。", "", actor=balgas) \
        .say("narr_4", "（バルガスは一気に薬を煽った。）", "", actor=pc) \
        .shake() \
        .say("narr_5", "（瞬間、彼の全身を覆っていた古い傷跡が消え、萎みかけていた筋肉が鋼のように膨れ上がる。）", "", actor=pc) \
        .say("narr_6", "（白髪は黒々とした輝きを取り戻し、放たれる闘気だけでアリーナの石壁に亀裂が入った。）", "", actor=pc) \
        .shake() \
        .say("balgas_4", "……あぁ、いい気分だ。これなら、一度くらいはお前を本気で『殺し』にいける。", "", actor=balgas) \
        .say("balgas_5", "来い！ 手加減は無しだ！ 殺すつもりで打ってこい！", "", actor=balgas) \
        .jump(scene1_5)

    # ========================================
    # シーン1.5: 回想——鉄血団の記憶
    # ========================================
    builder.step(scene1_5) \
        .play_bgm("BGM/Emotional_Sorrow_1") \
        .say("narr_fb1", "（——35年前、ノースティリス。）", "", actor=pc) \
        .say("narr_fb2", "（若き日のバルガスが、傭兵団「鉄血団」を率いていた頃の記憶。）", "", actor=pc) \
        .say("balgas_fb1", "おい、ガキ。俺の懐に手を突っ込もうってのか？", "", actor=balgas) \
        .say("narr_fb3", "（10歳の孤児——後のカインは、バルガスの財布を盗もうとして捕まった。痩せこけた体、汚れた衣服、しかしその目だけは諦めていなかった。）", "", actor=pc) \
        .say("kain_fb1", "……殺すなら殺せよ。どうせ、誰も俺のことなんか……", "", actor=pc) \
        .say("balgas_fb2", "……盗むしかなかったんだろう。なら、正しく戦う術を教えてやる。明日から俺の部下だ。飯は食わせてやる。その代わり、死ぬほど鍛えてやるからな。", "", actor=balgas) \
        .say("narr_fb4", "（——18年後。カインは鉄血団の副団長となった。バルガスの右腕として、誰よりも信頼された戦士。）", "", actor=pc) \
        .say("kain_fb2", "団長、次の依頼……『禁断の遺跡』の調査だそうです。報酬は破格ですが、嫌な予感がします。", "", actor=pc) \
        .say("balgas_fb3", "……嫌な予感ってのは当たるもんだ。だが、団員たちの冬越しの金がいる。行くしかねえだろ。", "", actor=balgas) \
        .say("kain_fb3", "……分かりました。俺がしんがりを務めます。", "", actor=pc) \
        .say("balgas_fb4", "馬鹿野郎。お前は俺の後継者だ。死ぬんじゃねえぞ。", "", actor=balgas) \
        .play_bgm("BGM/Ominous_Suspense_02") \
        .shake() \
        .say("narr_fb5", "（——遺跡の奥で、次元の裂け目が開いた。団員たちが次々と狭間に引きずり込まれていく。）", "", actor=pc) \
        .say("kain_fb4", "団長……俺を、置いていけ……！ でないと、あんたまで……！", "", actor=pc) \
        .say("narr_fb6", "（カインは罠で重傷を負い、動けなかった。バルガスはカインを背負い、狭間の中を彷徨った。）", "", actor=pc) \
        .say("balgas_fb5", "馬鹿野郎……！ お前を置いていけるか……！ ", "", actor=balgas) \
        .shake() \
        .say("narr_fb7", "（しかし、カインの体は限界を迎えていた。アスタロトに「拾われた」時、カインは既に息絶えていた。）", "", actor=pc) \
        .play_bgm("BGM/Ominous_Suspense_02") \
        .say("narr_fb8", "（——回想が終わり、現在に戻る。）", "", actor=pc) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_fb6", "……俺はあの時、カインを救えなかった。あいつの魂は今も、このアリーナのどこかで彷徨ってやがる。", "", actor=balgas) \
        .say("balgas_fb7", "だがな、お前は違う。お前は帰れるんだ。イルヴァに、生きている世界に。……だからこそ、俺は本気でお前を試す。中途半端な強さじゃ、アスタロトには勝てねえ。", "", actor=balgas) \
        .say("balgas_fb8", "カインに教えてやれなかったことを、今度こそお前に叩き込んでやる……！", "", actor=balgas) \
        .jump(scene2)

    # ========================================
    # シーン2: リリィの絶望と祈り
    # ========================================
    builder.step(scene2) \
        .play_bgm("BGM/Lily_Seductive_Danger") \
        .say("narr_7", "（リリィが震える手で水晶を握りしめている。）", "", actor=pc) \
        .say("narr_8", "（その瞳には、事務的な冷徹さは微塵も残っていない。）", "", actor=pc) \
        .focus_chara(Actors.LILY) \
        .say("lily_1", "……馬鹿な人。それは、命の火花を浪費する禁忌の薬……！", "", actor=lily) \
        .say("lily_2", "お願いです。彼を止めて……！", "", actor=lily) \
        .say("lily_3", "もし彼が死んだら、このアリーナにはもう、私を叱ってくれる人は誰もいなくなってしまうわ……！", "", actor=lily) \
        .jump(scene3)

    # ========================================
    # シーン3: 闘技場：師弟の極致 → バトル開始
    # ========================================
    builder.step(scene3) \
        .play_bgm("BGM/Battle_Balgas_Prime") \
        .say("narr_10", "（若き日の姿を取り戻した「伝説の戦士バルガス」との一騎打ち。）", "", actor=pc) \
        .say("narr_11", "（彼の動きは重く、速く、そして無駄がない。）", "", actor=pc) \
        .say("narr_12", "（教えてもらった技が、今度は殺意を持ってあなたを襲う。）", "", actor=pc) \
        .shake() \
        .say("obs_1", "観客「...殺せ！ ...師匠を殺せ！」", "", actor=pc) \
        .say("obs_2", "観客「...魂を捧げろ！」", "", actor=pc) \
        .say("lily_voice", "（リリィの小さな懇願の声が、あなたの耳に届く。「お願い……殺さないで……」）", "", actor=lily) \
        .set_flag("sukutsu_quest_battle", 2) \
        .start_battle_by_stage("rank_s_trial", master_id="sukutsu_arena_master") \
        .finish()

    # ========================================
    # シーン4: とどめの拒絶
    # ========================================
    builder.step(scene4) \
        .play_bgm("BGM/Emotional_Sorrow_2") \
        .say("narr_13", "（膝をつき、肩で息をするバルガス。）", "", actor=pc) \
        .say("narr_14", "（全盛期の輝きが失われ、急速に元の老いた姿へと戻っていく。）", "", actor=pc) \
        .say("narr_15", "（上空からは、観客たちの残酷な「処刑」を促す喝采が響き渡る。）", "", actor=pc) \
        .shake() \
        .say("obs_void", "「……殺セ。英雄ノ魂ヲ捧ゲ、真ノ『屠竜者』ト成レ……。」", "", actor=pc) \
        .say("narr_16", "（あなたは剣を引き、バルガスの喉元に突きつけた刃を下ろす。）", "", actor=pc) \
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
    # 内省：動機に応じた独白
    # ========================================
    # Motivation: 0=GREED, 1=BATTLE_LUST, 2=NIHILISM, 3=ARROGANCE
    builder.step(introspection) \
        .switch_flag(Keys.MOTIVATION, [
            introspect_greed,   # 0: 強欲
            introspect_battle,  # 1: 戦闘狂
            introspect_void,    # 2: 虚無
            introspect_pride,   # 3: 傲慢
            introspect_done,    # fallback
        ])

    # 強欲ルート
    builder.step(introspect_greed) \
        .say("intro_greed", "（あの時、俺は「富と名声」のためにこのアリーナに来た。）", "", actor=pc) \
        .say("intro_greed2", "（だが今、俺の手にあるのは金でも権力でもなく……この老いた戦士の命だ。）", "", actor=pc) \
        .say("intro_greed3", "（こんなもの、何の得にもならない。……それでも、手放せないんだ。）", "", actor=pc) \
        .jump(introspect_done)

    # 戦闘狂ルート
    builder.step(introspect_battle) \
        .say("intro_battle", "（あの時、俺は「強い奴と戦いたい」とだけ思っていた。）", "", actor=pc) \
        .say("intro_battle2", "（目の前の敵を倒し、次の敵へ。それだけでよかった。）", "", actor=pc) \
        .say("intro_battle3", "（……だが、バルガスを殺すことは『勝利』じゃない。ただの『喪失』だ。俺は、そんなことのために剣を振ってきたんじゃない。）", "", actor=pc) \
        .jump(introspect_done)

    # 虚無ルート
    builder.step(introspect_void) \
        .say("intro_void", "（あの時、俺には帰る場所がなかった。どこで死のうと同じだと思っていた。）", "", actor=pc) \
        .say("intro_void2", "（……だが、今は違う。バルガスがいて、リリィがいて……）", "", actor=pc) \
        .say("intro_void3", "（ここには、俺を待っている奴らがいる。もう、虚無に逃げることはできない。）", "", actor=pc) \
        .jump(introspect_done)

    # 傲慢ルート
    builder.step(introspect_pride) \
        .say("intro_pride", "（あの時、俺は「このアリーナも、ドラゴンも支配する」と豪語した。）", "", actor=pc) \
        .say("intro_pride2", "（……だが、支配とは何だ？ 命令に従わせることか？ 恐怖で屈服させることか？）", "", actor=pc) \
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
        .say("narr_18", "（その瞬間、アリーナ全体を包んでいた不気味な魔力が霧散し、観客たちの声が落胆の溜息へと変わる。）", "", actor=pc) \
        .say("narr_19", "（リリィが駆け寄り、泣きながらバルガスに回復魔法を注ぎ込む。）", "", actor=pc) \
        .focus_chara(Actors.LILY) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_7", "……ハッ。甘っちょろい野郎だ。……だが、その甘さが、俺がカインに教えてやれなかった『本物の強さ』なのかもしれねえな。", "", actor=balgas) \
        .say("balgas_8", "……負けたよ。今日からお前がランクS『屠竜者（Dragon Slayer）』だ。", "", actor=balgas) \
        .say("balgas_9", "俺はもう引退だ。これからは、ただの酔いどれの『隠居』として、お前の凱旋をここで待たせてもらうぜ。", "", actor=balgas) \
        .say("narr_20", "（リリィは台帳を開き、涙を拭きながら何かを書き込む。）", "", actor=pc) \
        .focus_chara(Actors.LILY) \
        .say("lily_4", "……ありがとう。本当に、ありがとうございます。", "", actor=lily) \
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
        .say("lily_7", "……それと、今回の戦いで、あなたは『理を拒む者』としての称号を獲得しました。", "", actor=lily) \
        .say("lily_8", "アリーナの命令を拒絶し、師匠を生かす……ふふ、あなたは本当に、システムの『バグ』ですね。", "", actor=lily) \
        .say("narr_21", "（影の中から、ゼクが見つめている。）", "", actor=pc) \
        .focus_chara(Actors.ZEK) \
        .say("zek_1", "……クク。システムの命令を拒絶しましたか。", "", actor=zek) \
        .say("zek_2", "面白い。実に面白い。あなたは『黄金』を超え、ついにこの箱庭の『バグ』として完成した。", "", actor=zek) \
        .say("zek_3", "さあ、アスタロトはすぐそこです。……あなたのその『慈悲』が、あの孤独な竜に届くのかどうか、見せてもらいましょう。", "", actor=zek) \
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
    # 終了処理（見逃しルート）
    # ========================================
    builder.step(ending) \
        .set_flag(Keys.RANK, 8) \
        .set_flag(Keys.BALGAS_CHOICE, FlagValues.BalgasChoice.SPARED) \
        .complete_quest(QuestIds.RANK_UP_S) \
        .say("sys_title", "【システム】称号『理を拒む者（System Breaker）』を獲得しました。", "") \
        .say("sys_buff", "【システム】『戦鬼の証』を獲得しました。筋力+5、耐久+5、各種耐性+5 の加護を得た！", "") \
        .action("eval", param="Elin_SukutsuArena.ArenaManager.GrantVsBalgasBonus();") \
        .finish()


def add_vs_balgas_result_steps(builder: ArenaDramaBuilder, victory_label: str, defeat_label: str, return_label: str):
    """
    バルガス戦の勝利/敗北ステップを arena_master ビルダーに追加する

    Args:
        builder: arena_master の ArenaDramaBuilder インスタンス
        victory_label: 勝利ステップのラベル名
        defeat_label: 敗北ステップのラベル名
        return_label: 結果表示後にジャンプするラベル名
    """
    pc = Actors.PC
    lily = Actors.LILY
    balgas = Actors.BALGAS

    # 勝利後の選択ラベル
    post_victory_choice = builder.label("vs_balgas_post_victory_choice")
    spare_balgas = builder.label("vs_balgas_spare")
    kill_balgas = builder.label("vs_balgas_kill")
    killed_ending = builder.label("vs_balgas_killed_ending")

    # ========================================
    # 勝利: 選択肢表示
    # ========================================
    builder.step(victory_label) \
        .set_flag("sukutsu_arena_result", 0) \
        .set_flag("sukutsu_quest_battle", 0) \
        .play_bgm("BGM/Emotional_Sorrow_2") \
        .say("narr_v1", "（膝をつき、肩で息をするバルガス。）", "", actor=pc) \
        .say("narr_v2", "（全盛期の輝きが失われ、急速に元の老いた姿へと戻っていく。）", "", actor=pc) \
        .say("narr_v3", "（上空からは、観客たちの残酷な「処刑」を促す喝采が響き渡る。）", "", actor=pc) \
        .shake() \
        .say("obs_void", "「……殺セ。英雄ノ魂ヲ捧ゲ、真ノ『屠竜者』ト成レ……。」", "", actor=pc) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_v1", "……な、何をしてやがる。……刺せ。それがアリーナの、戦士のケジメだろうが……！", "", actor=balgas) \
        .jump(post_victory_choice)

    # 選択肢: 見逃す or 殺す
    builder.choice(spare_balgas, "（武器を下ろし、手を差し伸べる）", "", text_id="c_spare_balgas") \
           .choice(kill_balgas, "（観客の命令に従い、とどめを刺す）", "", text_id="c_kill_balgas")

    # ========================================
    # 見逃すルート: 慈悲の選択
    # ========================================
    spare_choice = builder.label("vs_balgas_spare_choice")
    react_philosophy = builder.label("vs_balgas_react_philosophy")
    react_rule = builder.label("vs_balgas_react_rule")
    react_hand = builder.label("vs_balgas_react_hand")
    spare_ending = builder.label("vs_balgas_spare_ending")

    builder.step(spare_balgas) \
        .say("narr_s1", "（あなたは剣を引き、バルガスの喉元に突きつけた刃を下ろす。）", "", actor=pc) \
        .say("balgas_s1", "……な、何をしてやがる。……刺せ。それがアリーナの、戦士のケジメだろうが……！", "", actor=balgas) \
        .jump(spare_choice)

    # 選択肢: なぜ見逃すのか
    builder.choice(react_philosophy, "俺の哲学には、師匠を殺すという項目はない", "", text_id="c_spare_philosophy") \
           .choice(react_rule, "アリーナのルールに従うつもりはない。俺がルールだ", "", text_id="c_spare_rule") \
           .choice(react_hand, "（無言で手を差し伸べる）", "", text_id="c_spare_hand")

    builder.step(react_philosophy) \
        .say("balgas_rp", "……ハッ。甘っちょろい野郎だ……。", "", actor=balgas) \
        .jump(spare_ending)

    builder.step(react_rule) \
        .say("balgas_rr", "……傲慢な野郎だ。……だが、その傲慢が、俺が求めていた強さなのかもしれねえな……。", "", actor=balgas) \
        .jump(spare_ending)

    builder.step(react_hand) \
        .say("balgas_rh", "……無口な野郎だ。……だが、その手は……温かいな……。", "", actor=balgas) \
        .jump(spare_ending)

    builder.step(spare_ending) \
        .play_bgm("BGM/Emotional_Sacred_Triumph_Special") \
        .say("narr_s2", "（あなたがバルガスの手を取り、立ち上がらせる。）", "", actor=pc) \
        .say("narr_s3", "（リリィが駆け寄り、泣きながらバルガスに回復魔法を注ぎ込む。）", "", actor=pc) \
        .focus_chara(Actors.LILY) \
        .say("lily_s1", "……ありがとう。本当に、ありがとうございます。", "", actor=lily) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_s2", "……ハッ。甘っちょろい野郎だ。……だが、その甘さが、俺がカインに教えてやれなかった『本物の強さ』なのかもしれねえな。", "", actor=balgas) \
        .say("balgas_s3", "……負けたよ。今日からお前がランクS『屠竜者（Dragon Slayer）』だ。", "", actor=balgas) \
        .complete_quest(QuestIds.RANK_UP_S_BALGAS_SPARED) \
        .say("sys_title_s", "【システム】称号『理を拒む者（System Breaker）』を獲得しました。", "") \
        .say("sys_buff_s", "【システム】『戦鬼の証』を獲得しました。筋力+5、耐久+5、各種耐性+5 の加護を得た！", "") \
        .action("eval", param="Elin_SukutsuArena.ArenaManager.GrantVsBalgasBonus();") \
        .finish()

    # ========================================
    # 殺すルート: 観客に従う
    # ========================================
    builder.step(kill_balgas) \
        .play_bgm("BGM/Ominous_Suspense_02") \
        .shake() \
        .say("narr_k1", "（あなたは剣を振り下ろした。）", "", actor=pc) \
        .say("narr_k2", "（バルガスは最後まで、あなたを見つめていた。その瞳には……失望と、どこか安堵のような光があった。）", "", actor=pc) \
        .say("narr_k3", "（観客席から、狂喜の叫びが轟く。「魂を捧げよ！ 屠竜者よ！」）", "", actor=pc) \
        .shake() \
        .say("narr_k4", "（リリィが悲鳴を上げて駆け寄るが、もう遅い。）", "", actor=pc) \
        .focus_chara(Actors.LILY) \
        .say("lily_k1", "……バルガスさん……！ どうして……！", "", actor=lily) \
        .say("lily_k2", "（リリィはあなたを見る。その瞳には、恐怖と悲しみが入り混じっている。）", "", actor=pc) \
        .say("lily_k3", "……あなたは……観客に魂を売ったのね……。", "", actor=lily) \
        .jump(killed_ending)

    builder.step(killed_ending) \
        .complete_quest(QuestIds.RANK_UP_S_BALGAS_KILLED) \
        .say("sys_title_k", "【システム】称号『観客の傀儡（Audience's Puppet）』を獲得しました。", "") \
        .say("sys_buff_k", "【システム】『血塗られた称号』を獲得しました。筋力+10、魔力+10……しかし、何かを失った気がする。", "") \
        .action("eval", param="Elin_SukutsuArena.ArenaManager.GrantVsBalgasBonus();") \
        .finish()

    # ========================================
    # 敗北
    # ========================================
    builder.step(defeat_label) \
        .set_flag("sukutsu_arena_result", 0) \
        .set_flag("sukutsu_quest_battle", 0) \
        .play_bgm("BGM/Lobby_Normal") \
        .focus_chara(Actors.LILY) \
        .say("lily_d1", "……バルガスさんには、まだ勝てなかったようですね。", "", actor=lily) \
        .say("lily_d2", "でも、生きているだけで十分です。彼は本気であなたを試したのですから。", "", actor=lily) \
        .say("lily_d3", "準備が整ったら、また挑戦してください。", "", actor=lily) \
        .finish()
