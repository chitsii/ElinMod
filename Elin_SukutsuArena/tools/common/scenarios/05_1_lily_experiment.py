"""
05_1_lily_experiment.md - リリィの私的依頼『残響の器』
"""

from drama_builder import DramaBuilder
from flag_definitions import Keys, Actors, QuestIds

def define_lily_experiment(builder: DramaBuilder):
    """
    リリィの私的依頼「残響の器」
    シナリオ: 05_1_lily_experiment.md
    """
    # アクター登録
    pc = builder.register_actor(Actors.PC, "あなた", "You")
    lily = builder.register_actor(Actors.LILY, "リリィ", "Lily")

    # ラベル定義
    main = builder.label("main")
    scene1 = builder.label("scene1_request")
    choice1 = builder.label("choice1")
    react1_what = builder.label("react1_what")
    react1_reward = builder.label("react1_reward")
    react1_skill = builder.label("react1_skill")
    scene2 = builder.label("scene2_requirements")
    choice2 = builder.label("choice2")
    react2_accept = builder.label("react2_accept")
    react2_skull = builder.label("react2_skull")
    react2_specs = builder.label("react2_specs")
    scene3 = builder.label("scene3_crafting")
    scene4 = builder.label("scene4_delivery")
    reward_select = builder.label("reward_select")
    reward_mana = builder.label("reward_mana")
    reward_ether = builder.label("reward_ether")
    reward_glass = builder.label("reward_glass")
    reward_end = builder.label("reward_end")
    final_choice = builder.label("final_choice")
    final_accept = builder.label("final_accept")
    final_reward = builder.label("final_reward")
    final_silent = builder.label("final_silent")
    ending = builder.label("ending")

    # ========================================
    # シーン1: 受付嬢の不機嫌な午後
    # ========================================
    builder.step(main) \
        .play_bgm("BGM/Lobby_Normal") \
        .focus_chara(Actors.LILY) \
        .say("narr_1", "（ロビーは相変わらず、異次元の歪みが軋む不快な音に満ちている。）", "", actor=pc) \
        .say("narr_2", "（リリィは眉間に皺を寄せ、羽根ペンを乱暴に机に置いた。その前には、どこか禍々しい幾何学模様が描かれた、古ぼけた設計図が広げられている。）", "", actor=pc) \
        .say("lily_1", "……あぁ、忌々しい。", "", actor=lily) \
        .say("lily_2", "このロビーの『雑音』のせいで、私の大切な研究がちっとも進みません。戦士たちの絶望、観客の哄笑、次元の摩擦音……これらは本来、純粋な『魔力の残滓』として回収されるべきものなのに。", "", actor=lily) \
        .say("narr_3", "（彼女はあなたを見つけ、わずかに目を細める。）", "", actor=pc) \
        .say("lily_3", "ねえ、そこの『泥犬』さん。少しは私に牙以外の役に立つところを見せてくださる？", "", actor=lily) \
        .say("lily_4", "私の研究のために、特別な『実験用具』が必要なのです。……そう、地上の安っぽい職人では形にすることすら叶わない、特別な器が。", "", actor=lily)

    # プレイヤーの選択肢
    builder.choice(react1_what, "どんな器が必要なんだ？", "", text_id="c1_what") \
           .choice(react1_reward, "報酬次第だな", "", text_id="c1_reward") \
           .choice(react1_skill, "俺に製作技術があると思うのか？", "", text_id="c1_skill")

    # 選択肢反応
    builder.step(react1_what) \
        .say("lily_r1", "ふふ、興味を持っていただけましたか。では、詳しくご説明いたしましょう。", "", actor=lily) \
        .jump(scene2)

    builder.step(react1_reward) \
        .say("lily_r2", "まあ、現実的ですこと。ええ、もちろん報酬はお支払いいたしますよ。", "", actor=lily) \
        .jump(scene2)

    builder.step(react1_skill) \
        .say("lily_r3", "……どうでしょうね。試してみなければ分かりませんが、少なくとも期待はしていますよ。", "", actor=lily) \
        .jump(scene2)

    # ========================================
    # シーン2: 技術への要求
    # ========================================
    builder.step(scene2) \
        .play_bgm("BGM/Mystical_Ritual") \
        .say("narr_4", "（リリィは細長い指先で設計図の一点を鋭く指し示した。そこには、内部に複雑な空洞を持つ、特殊な瓶のような構造が描かれている。）", "", actor=pc) \
        .say("lily_5", "必要なのは**『虚空の共鳴瓶』**。ただのガラスや石では、次元の圧力に耐えきれず粉々に砕けてしまうわ。", "", actor=lily) \
        .say("lily_6", "あなたがもし、『石細工』あるいは『ガラス工芸』の心得があるのなら、**黒曜石**か**高品質な水晶**を素材にして、これを作りなさい。", "", actor=lily) \
        .say("lily_7", "素材そのものの品質も重要ですが、何よりあなたの『集中力』が試されます。……ふふ、もし不出来なものを持ち込んだら、その器の代わりにあなたの頭蓋骨を加工して使うことになりますが、よろしいかしら？", "", actor=lily)

    # プレイヤーの選択肢
    builder.choice(react2_accept, "任せてくれ。作ってみせる", "", text_id="c2_accept") \
           .choice(react2_skull, "……頭蓋骨は勘弁してくれ", "", text_id="c2_skull") \
           .choice(react2_specs, "具体的な要求仕様は？", "", text_id="c2_specs")

    # 選択肢反応
    builder.step(react2_accept) \
        .say("lily_r4", "ふふ、自信がおありで結構。では、期待しておりますね。", "", actor=lily) \
        .jump(scene3)

    builder.step(react2_skull) \
        .say("lily_r5", "まあ、ご心配なく。冗談ですよ。……多分。", "", actor=lily) \
        .jump(scene3)

    builder.step(react2_specs) \
        .say("lily_r6", "おや、職人気質ですこと。では、細部までご説明いたしましょう。", "", actor=lily) \
        .jump(scene3)

    # ========================================
    # シーン3: 製作の過程
    # ========================================
    builder.step(scene3) \
        .say("lily_8", "器が完成したら、仕上げに**『ヴォイド・プチの粘液』**で内側をコーティングすること。それでようやく、この異次元の『音』を閉じ込めるための膜が完成します。", "", actor=lily) \
        .say("lily_9", "さあ、作業台へ向かいなさい。あなたがただの暴力装置ではなく、繊細な手先を持つ『創造者』でもあることを、私に証明してみせるのです。", "", actor=lily) \
        .say("lily_10", "……期待はしていませんが、楽しみにはしていますよ？", "", actor=lily) \
        .say("narr_5", "（プレースホルダー：ここで実際の製作処理を行う。黒曜石または水晶、ヴォイド・プチの粘液を消費して『虚空の共鳴瓶』を作成する。）", "", actor=pc) \
        .jump(scene4)

    # ========================================
    # シーン4: 納品と報酬の授与
    # ========================================
    builder.step(scene4) \
        .play_bgm("BGM/Lily_Tranquil") \
        .say("narr_6", "（リリィは差し出された器を目の高さに掲げ、偏光する光を透かして微細な傷一つないかを確認する。）", "", actor=pc) \
        .say("narr_7", "（不意に、彼女の尻尾が満足げに揺れた。）", "", actor=pc) \
        .say("lily_11", "……あら。意外ですね。", "", actor=lily) \
        .say("lily_12", "あんな泥にまみれた手で、これほどまでに滑らかな曲線を描き出すなんて。合格です。これなら、このアリーナに満ちる『死の残響』を存分に吸い取ってくれるでしょう。", "", actor=lily) \
        .say("narr_8", "（彼女は器を丁寧に棚に置き、台帳を開く。）", "", actor=pc) \
        .say("lily_13", "これはお礼です。", "", actor=lily) \
        .say("lily_14", "観客からの報酬として、**小さなコイン7枚**と**プラチナコイン2枚**を台帳に記録いたしました。それと、この器を使って精製した素材を、一つ選んでいただけます。", "", actor=lily)

    # 報酬選択肢
    builder.choice(reward_mana, "魔力の結晶を頼む", "", text_id="c_reward_mana") \
           .choice(reward_ether, "エーテルの欠片が欲しい", "", text_id="c_reward_ether") \
           .choice(reward_glass, "ガラスの破片を選ぶ", "", text_id="c_reward_glass")

    # 報酬選択反応
    builder.step(reward_mana) \
        .say("lily_rew1", "『魔力の結晶×1』、記録いたしました。この器で精製した、純粋な魔力の塊ですよ。", "", actor=lily) \
        .action("eval", param="EClass.pc.Pick(ThingGen.Create(\"magic_stone\"));") \
        .jump(reward_end)

    builder.step(reward_ether) \
        .say("lily_rew2", "『エーテルの欠片×1』、記録いたしました。……慎重にお使いくださいね。", "", actor=lily) \
        .action("eval", param="EClass.pc.Pick(ThingGen.Create(\"crystal\"));") \
        .jump(reward_end)

    builder.step(reward_glass) \
        .say("lily_rew3", "『ガラスの破片×1』ですね。……地味な選択ですが、実用的です。", "", actor=lily) \
        .action("eval", param="EClass.pc.Pick(ThingGen.Create(\"glass\"));") \
        .jump(reward_end)

    # 報酬終了
    builder.step(reward_end) \
        .action("eval", param="for(int i=0; i<7; i++) { EClass.pc.Pick(ThingGen.Create(\"money\")); } for(int i=0; i<2; i++) { EClass.pc.Pick(ThingGen.Create(\"plat\")); }") \
        .say("lily_15", "それと……あなたの技術を評価して、称号も記録しておきました。『繊細な泥犬』。ふふ、あなたは暴力だけではないのですね。", "", actor=lily) \
        .say("lily_16", "これからも、何か特別な依頼があれば、あなたにお願いするかもしれません。……期待していますよ。", "", actor=lily)

    # 最終選択肢
    builder.choice(final_accept, "いつでも頼んでくれ", "", text_id="c_final_accept") \
           .choice(final_reward, "報酬次第だがな", "", text_id="c_final_reward") \
           .choice(final_silent, "（無言で頷く）", "", text_id="c_final_silent")

    # 最終選択肢反応
    builder.step(final_accept) \
        .say("lily_f1", "ふふ、頼もしいこと。では、またお願いいたしますね。", "", actor=lily) \
        .jump(ending)

    builder.step(final_reward) \
        .say("lily_f2", "まあ、現実的ですこと。ええ、もちろんお支払いはしますよ。", "", actor=lily) \
        .jump(ending)

    builder.step(final_silent) \
        .say("lily_f3", "……無口ですが、仕事はきっちりとこなす。良い職人気質ですね。", "", actor=lily) \
        .jump(ending)

    # ========================================
    # 終了処理
    # ========================================
    builder.step(ending) \
        .complete_quest(QuestIds.LILY_EXPERIMENT) \
        .mod_flag(Keys.REL_LILY, "+", 5) \
        .finish()
