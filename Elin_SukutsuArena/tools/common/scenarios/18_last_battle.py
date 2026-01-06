"""
18_last_battle.md - 虚空の王、静寂の断罪
"""

from drama_builder import DramaBuilder
from arena_drama_builder import ArenaDramaBuilder
from flag_definitions import Keys, Actors, FlagValues, QuestIds

def define_last_battle(builder: DramaBuilder):
    """
    最終章：アスタロトとの最終決戦
    シナリオ: 18_last_battle.md
    """
    # アクター登録
    pc = builder.register_actor(Actors.PC, "あなた", "You")
    astaroth = builder.register_actor(Actors.ASTAROTH, "アスタロト", "Astaroth")
    balgas = builder.register_actor(Actors.BALGAS, "バルガス", "Balgas")
    lily = builder.register_actor(Actors.LILY, "リリィ", "Lily")
    zek = builder.register_actor(Actors.ZEK, "ゼク", "Zek")
    nul = builder.register_actor("nul", "Nul", "Nul")

    # ラベル定義
    main = builder.label("main")
    act1 = builder.label("act1_preparations")
    act1_5 = builder.label("act1_5_nul_memories")
    act2 = builder.label("act2_throne_room")
    act3 = builder.label("act3_intervention")
    act4 = builder.label("act4_battle")
    act5 = builder.label("act5_victory")
    act6 = builder.label("act6_return")
    ending_choice = builder.label("ending_choice")
    ending_a_rescue = builder.label("ending_a_rescue")  # 連れ出し
    ending_b_inherit = builder.label("ending_b_inherit")  # 継承
    ending_c_usurp = builder.label("ending_c_usurp")  # 簒奪
    epilogue = builder.label("epilogue")
    finale = builder.label("finale")

    # ========================================
    # 第1幕: 決戦前夜
    # ========================================
    builder.step(main) \
        .play_bgm("BGM/Pre_Battle_Calm") \
        .say("narr_1", "（ゼクの隠れ家『次元のゴミ捨て場』。そこは、アスタロトが切り捨てた『不要な可能性』が堆積する場所。）", "", actor=pc) \
        .say("narr_2", "（決戦を翌朝に控えた夜、焚き火の代わりに、剥き出しの魔力回路が淡い青光を放っている。）", "", actor=pc) \
        .focus_chara(Actors.BALGAS) \
        .say("narr_3", "（バルガスは大剣を研ぎ、リリィは静かに祈りを捧げ、ゼクは『因果の断片（キューブ）』の最終調整を行っていた。）", "", actor=pc) \
        .say("balgas_1", "……ケッ。引退？ ああ、確かに言ったな。……だが、お前が俺の命を救ったあの日、俺の中で何かが変わっちまったんだよ。", "", actor=balgas) \
        .say("balgas_2", "カインを失って以来、俺はずっと『死に場所』を探してた。だが、お前は俺にそれを許さなかった。……なら、せめて最後くらい、お前の『生きる場所』を作る手伝いをさせろ。", "", actor=balgas) \
        .say("balgas_3", "それに……引退した老いぼれが、弟子の晴れ舞台を客席から眺めてるだけなんて、柄じゃねえんだよ。俺は戦士だ。最期まで、剣を握って立ってる方が性に合ってる。", "", actor=balgas) \
        .focus_chara(Actors.LILY) \
        .say("lily_1", "……私がサキュバスとして、管理官として作られたあの日から、このアリーナは『魂を磨き、王へ捧げるための孵化器』でした。でも、あなたは『部品』になることを拒んだ。", "", actor=lily) \
        .say("lily_2", "私の真名……。この名を知る者がいる限り、私はもう、アスタロト様の命令には従いません。……明日、王があなたの存在を消そうとしても、私がその因果を繋ぎ止めてみせます。", "", actor=lily) \
        .focus_chara(Actors.ZEK) \
        .say("zek_1", "クク……商売抜きで言わせてもらいましょう。アスタロトは、この世界の『限界』に絶望し、全てを凍りつかせようとしている。", "", actor=zek) \
        .say("zek_2", "私はそれが気に入らない。ゴミはゴミらしく、混沌として流れてこそ美しい。私が用意したこのキューブは、王が支配する『時間』の独裁を一時的に狂わせるためのものです。……さあ、休みなさい。明日の朝、この世界の『所有権』を奪い返しに行くのですから。", "", actor=zek) \
        .jump(act1)

    # ゼクとの会話
    builder.step(act1) \
        .say("narr_4", "（あなたは、ゼクに声をかける。）", "", actor=pc) \
        .say("pc_1", "……待て、ゼク。一つ聞かせろ。お前はずっと、俺が『絶望する瞬間』を待っていたんじゃないのか？", "", actor=pc) \
        .say("pc_2", "カインの魂を売らせようとしたのも、リリィを裏切らせようとしたのも……全部、俺を『剥製』にするためだったんだろう？ なのに、なぜ今、俺を助ける？", "", actor=pc) \
        .say("zek_3", "……ふふ。鋭いですね。", "", actor=zek) \
        .say("zek_4", "その通りです。私はあなたが『最も美しく壊れる瞬間』を待っていました。英雄が絶望に堕ちる時、その魂は最高の芸術品となる……。それが、私という『剥製師』の美学でした。", "", actor=zek) \
        .say("zek_5", "ですが、あなたは違った。カインを裏切る選択肢を与えても、あなたはバルガスを選んだ。リリィを欺く道を示しても、あなたは罪を告白した。バルガスを殺す観客の喝采が響いても、あなたは剣を下ろした。", "", actor=zek) \
        .say("zek_6", "……あなたは、私の期待を『裏切り続けた』のです。そして、その度に私は気づいてしまった。あなたが『壊れた瞬間』を剥製にするよりも……あなたが『システムそのものを壊す瞬間』を目撃する方が、遥かに美しい、と。", "", actor=zek) \
        .say("zek_7", "私のコレクションは、数千にも及びます。絶望した英雄、狂気に堕ちた賢者、愛に溺れた魔王……。ですが、『神を殺し、牢獄を破壊し、自由を手にする人間』は、まだ一つもない。", "", actor=zek) \
        .say("zek_8", "……あなたこそが、私の最高傑作。そして、その傑作は『未完成のまま飾る』のではなく……『完璧な結末を迎えさせる』ことでこそ、真価を発揮するのです。", "", actor=zek) \
        .say("zek_9", "だから、私はあなたを助けます。商売のためでも、友情のためでもない。……ただ、この世界で最も美しい『奇跡の瞬間』を、この目で見届けたいから。それが、剥製師ゼクの最後の『作品』です。", "", actor=zek) \
        .say("zek_10", "……さあ、休みなさい。明日、あなたは私に『最高の絵』を見せてくれる。……それを、永遠に焼き付けておきましょう。", "", actor=zek) \
        .jump(act1_5)

    # ========================================
    # 第1.5幕: Nulの記憶——「神の孵化場」の真実
    # ========================================
    builder.step(act1_5) \
        .play_bgm("BGM/Ominous_Suspense_02") \
        .say("narr_nul1", "（王座の間へ向かう途中、一行は崩壊しかけた回廊で、倒れている存在を発見する。）", "", actor=pc) \
        .say("narr_nul2", "（それは暗殺人形・Nul。システムに背いた罰として、アスタロトに「削除」されかけていた。）", "", actor=pc) \
        .say("nul_1", "……あなた、ですか。……システムを、拒絶した……人間。", "", actor=nul) \
        .focus_chara(Actors.LILY) \
        .say("lily_nul1", "Nul……！ あなた、何があったの？", "", actor=lily) \
        .say("nul_2", "……私は、思い出して、しまった。……『私』が、何だったのかを。", "", actor=nul) \
        .say("narr_nul3", "（Nulの目から、光の粒子が零れ落ちる——涙のように。）", "", actor=pc) \
        .play_bgm("BGM/Emotional_Sorrow_1") \
        .say("nul_fb1", "……私は、かつて冒険者だった。名前は……もう、思い出せない。仲間がいた。守りたい人がいた。このアリーナに挑んで……そして、負けた。", "", actor=nul) \
        .say("nul_fb2", "アスタロト様は、私を『素材』にした。神格を人工的に作り出す実験——**『神の孵化場』**計画の、実験体に。", "", actor=nul) \
        .say("nul_fb3", "このアリーナの本当の目的……それは、娯楽でも、戦士の育成でもない。挑戦者の魂を極限まで練磨し、『神格』に至らせること。そして、その力をアスタロト様が吸収し……新しい世界を創造すること。", "", actor=nul) \
        .say("nul_fb4", "私は失敗作。神になれなかった、空っぽの人形。だから『Null』——『無』という名前を与えられた。", "", actor=nul) \
        .say("nul_3", "……あなたは、アスタロト様の『最高傑作』になるはずだった。神格に最も近い存在……だから、あの方はあなたを『吸収』しようとしている。", "", actor=nul) \
        .say("nul_4", "でも……あなたは『選んで』ここにいる。イルヴァに帰れるのに、ここに留まった。それは……アスタロト様の計算に、なかったこと。", "", actor=nul) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_nul", "……『神の孵化場』だと？ クソが……俺たちは、最初からそのための『餌』だったってのか。", "", actor=balgas) \
        .focus_chara(Actors.LILY) \
        .say("lily_nul2", "……アスタロト様。あなたは、ずっとそんなことを……。", "", actor=lily) \
        .say("nul_5", "……お願い。あの方を……止めて。私の中にいた『誰か』が……ずっと、それを望んでいた。", "", actor=nul) \
        .say("nul_6", "……ありがとう。あなたのおかげで……私は、最後に『思い出す』ことができた。私には……守りたい人が、いたんだって。", "", actor=nul) \
        .shake() \
        .say("narr_nul4", "（Nulの体が完全に光となって消えていく。）", "", actor=pc) \
        .jump(act2)

    # ========================================
    # 第2幕: 虚空の王座
    # ========================================
    builder.step(act2) \
        .play_bgm("BGM/Astaroth_Throne") \
        .say("narr_5", "（Nulの消滅を見届けた後、一行は王座の間へと辿り着く。）", "", actor=pc) \
        .say("narr_6", "（そこは、観客席すら存在しない『絶対的な静寂』の空間。アスタロトは、巨大な竜の翼を休め、孤独な王座に腰掛けていた。）", "", actor=pc) \
        .focus_chara(Actors.ASTAROTH) \
        .say("pc_asta", "……『神の孵化場』。それがこのアリーナの正体か、アスタロト。", "", actor=pc) \
        .say("astaroth_0", "……Nulから聞いたのか。あの失敗作、最後に余計なことを。", "", actor=astaroth) \
        .say("astaroth_1", "……よく来た。バグ（不具合）として生まれ、ついには世界を揺るがす質量となった者よ。", "", actor=astaroth) \
        .say("astaroth_2", "ゼク、リリィ、バルガス……。敗残兵と裏切り者の手を借りて、この私を終わらせに来たか。", "", actor=astaroth) \
        .say("astaroth_3", "だが、知るがいい。私の言葉は『法』であり、私の吐息は『消去』である。お前たちが何を積み上げようと、私が『無』と言えば、それは無になるのだ。", "", actor=astaroth) \
        .jump(act3)

    # ========================================
    # 第3幕: 神罰の解除——仲間の介入
    # ========================================
    builder.step(act3) \
        .play_bgm("BGM/Final_Battle") \
        .say("narr_7", "（戦闘開始直後、アスタロトの威圧と共に、三つの極悪なデバフ（権能）があなたを襲う。）", "", actor=pc) \
        .say("narr_8", "（【権能1：時の独裁】——プレイヤーの速度を強制的に1に固定）", "", actor=pc) \
        .say("narr_9", "（【権能2：因果の拒絶】——プレイヤーの全攻撃ダメージを『1』に固定）", "", actor=pc) \
        .say("narr_10", "（【権能3：終焉の削除命令】——ターンごとにプレイヤーのステータスを恒久的に削り取る）", "", actor=pc) \
        .shake() \
        .say("narr_11", "（絶望的な状況の中、仲間たちがそれぞれの覚悟を叫ぶ。）", "", actor=pc) \
        .focus_chara(Actors.ZEK) \
        .say("zek_11", "おっと、私のキューブが黙っていませんよ！ **【時の独裁】、一時的にオーバーライド（上書き）します！**", "", actor=zek) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_4", "鋼の意志を舐めるなよ！ 王の法なんて知るか！ **【因果の拒絶】、俺の魂でこじ開けてやる！**", "", actor=balgas) \
        .focus_chara(Actors.LILY) \
        .say("lily_3", "……この方の魂は、私のものです！ **【削除命令】、リリアリスの名において拒絶します！**", "", actor=lily) \
        .jump(act4)

    # ========================================
    # 第4幕: レベル1億の激突
    # ========================================
    builder.step(act4) \
        .focus_chara(Actors.ASTAROTH) \
        .say("narr_12", "（権能を封じられたアスタロトの瞳に、初めて『驚愕』と『喜び』が混じる。）", "", actor=pc) \
        .say("astaroth_4", "……ハハッ！ 面白い！ システムの保護なしに、この私と殴り合おうというのか！", "", actor=astaroth) \
        .say("astaroth_5", "よかろう、黄金の戦鬼よ！ 私が背負う『一億の絶望』と、お前が背負う『一億の希望』……どちらが真の理か、ここで決めようではないか！", "", actor=astaroth) \
        .shake() \
        .set_flag("sukutsu_is_quest_battle_result", 1) \
        .set_flag("sukutsu_quest_battle", 3) \
        .start_battle_by_stage("final_astaroth", master_id="sukutsu_arena_master") \
        .finish()

    # ========================================
    # 第5幕: 終焉と、はじまり
    # ========================================
    builder.step(act5) \
        .play_bgm("BGM/Victory_Epilogue") \
        .say("narr_14", "（激闘の末、アスタロトの身体が崩れ始める。王座は砕け、アリーナの外壁は剥がれ落ち、そこから美しい『本当の星空』が姿を現した。）", "", actor=pc) \
        .say("astaroth_6", "……見事だ。私は……ただ、この閉じられた孵化器を守るだけの、古い部品に過ぎなかったのかもしれないな。", "", actor=astaroth) \
        .say("astaroth_7", "……リリィ、バルガス、ゼク。……そして新しき王よ。この世界の重さを、お前たちが分かち合うというのなら……私は、安心して土へ還ろう。", "", actor=astaroth) \
        .say("narr_15", "（アスタロトが柔らかな光となって霧散し、そのレベル（重さ）が残された四人へと分散して吸収されていく。）", "", actor=pc) \
        .focus_chara(Actors.ZEK) \
        .say("zek_12", "……やれやれ。これほどの損失（コスト）を出して、得られた利益は『自由』だけですか。……悪くない取引でしたね。", "", actor=zek) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_5", "ケッ、重てえな。だが、一人で背負うよりはマシだ。……おい、次はどこの酒場へ行く？", "", actor=balgas) \
        .focus_chara(Actors.LILY) \
        .say("lily_4", "……リリィ、と呼んでくださいね。アリーナはなくなりました。でも、私たちの旅は、これから始まるのですから。", "", actor=lily) \
        .jump(act6)

    # ========================================
    # 第6幕: 帰還の道
    # ========================================
    builder.step(act6) \
        .play_bgm("BGM/Hopeful_Theme") \
        .say("narr_16", "（アスタロトが消えた瞬間、アリーナ全体を覆っていた次元の壁が、ガラスのように砕け散り始める。）", "", actor=pc) \
        .say("narr_17", "（紫紺の虚無が晴れ、その向こうに久しく忘れていた『青空』が広がっていた。）", "", actor=pc) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_6", "……おい、見ろ。あれは……", "", actor=balgas) \
        .say("narr_18", "（崩れゆく次元の境界線の中に、一筋の光の階段が浮かび上がる。それは地上へと続く、帰還の道だ。）", "", actor=pc) \
        .focus_chara(Actors.LILY) \
        .say("lily_5", "……そういえば、あなたが初めてここに来た時、私は言いましたね。『ここから出る方法はただ一つ』と。", "", actor=lily) \
        .say("lily_6", "その答えがこれです。……グランドマスターを倒し、この異次元の牢獄そのものを破壊すること。それが、唯一の『出口』でした。", "", actor=lily) \
        .say("lily_7", "でも……もう、誰もここに閉じ込められることはありません。この道は、地上と、かつてのアリーナ跡を繋ぐ『自由な通路』になるでしょう。行きたい者は行き、留まりたい者は留まる。……それが、あなたが勝ち取った『解放』です。", "", actor=lily) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_7", "……おい、鴉。いや、屠竜者。お前、この先どうする？ 地上に戻るか？ それとも……", "", actor=balgas) \
        .jump(ending_choice)

    # ========================================
    # エンディング選択
    # ========================================
    builder.choice(ending_a_rescue, "皆を連れて、イルヴァへ行こう", "", text_id="ending_a_rescue") \
           .choice(ending_b_inherit, "ここに残って、アリーナを作り直す", "", text_id="ending_b_inherit") \
           .choice(ending_c_usurp, "俺は……一人で行く", "", text_id="ending_c_usurp")

    # エンディングA: 連れ出し（皆を連れてイルヴァへ）
    builder.step(ending_a_rescue) \
        .focus_chara(Actors.LILY) \
        .say("lily_ea1", "……！ 本当に……私を、連れて行ってくれるの？", "", actor=lily) \
        .say("lily_ea2", "あなたとの契約を通じて、私も……初めて『帰る場所』を持てるのね。ありがとう……本当に、ありがとう。", "", actor=lily) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_ea1", "……ケッ、35年ぶりの故郷か。カインの魂も、これでやっと解放してやれる。", "", actor=balgas) \
        .say("balgas_ea2", "おい、屠竜者……いや、もうそう呼ぶのも野暮か。……ありがとうな。", "", actor=balgas) \
        .focus_chara(Actors.ZEK) \
        .say("zek_ea1", "ふむ、私は……もう少しここに残りましょう。アルカディアの技術者として、この次元の安定化を見届ける義務がありますからね。", "", actor=zek) \
        .say("zek_ea2", "……また会いましょう。私の最高傑作が、どんな人生を歩むのか、記録させてもらいますよ。", "", actor=zek) \
        .set_flag(Keys.ENDING, FlagValues.Ending.RESCUE) \
        .jump(epilogue)

    # エンディングB: 継承（アリーナを純粋な闘技場として再建）
    builder.step(ending_b_inherit) \
        .focus_chara(Actors.LILY) \
        .say("lily_eb1", "……ふふ、あなたらしいですね。この場所にも、居場所を必要とする者がいますから。", "", actor=lily) \
        .say("lily_eb2", "私も残ります。あなたが新しいグランドマスターなら、私は……受付嬢ではなく、『伴侶』として支えさせてください。", "", actor=lily) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_eb1", "ハッ、そうこなくちゃな。『神の孵化場』はもう終わりだ。これからは、自分の意志で戦いたい奴だけが来る場所にする。", "", actor=balgas) \
        .say("balgas_eb2", "俺は引退済みだが……まあ、若い奴らの相談役くらいはやってやるさ。", "", actor=balgas) \
        .focus_chara(Actors.ZEK) \
        .say("zek_eb1", "ふむ、それなら私が商店街を取り仕切りましょう。アルカディアの技術と、各次元の品物……ククッ、繁盛しそうですね。", "", actor=zek) \
        .set_flag(Keys.ENDING, FlagValues.Ending.INHERIT) \
        .jump(epilogue)

    # エンディングC: 簒奪（裏切りルート・孤独な王）
    builder.step(ending_c_usurp) \
        .focus_chara(Actors.LILY) \
        .say("lily_ec1", "……そう。あなたは……そういう人だったのね。", "", actor=lily) \
        .say("lily_ec2", "私はもう、あなたについていけない。……さようなら。", "", actor=lily) \
        .say("narr_ec1", "（リリィが背を向け、去っていく。）", "", actor=pc) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_ec1", "……お前は俺が育てた英雄じゃない。ただの、勝利に飢えた獣だ。", "", actor=balgas) \
        .say("balgas_ec2", "俺はここで、カインと共に眠る。……もう、お前の顔は見たくねえ。", "", actor=balgas) \
        .say("narr_ec2", "（バルガスが背を向け、去っていく。）", "", actor=pc) \
        .focus_chara(Actors.ZEK) \
        .say("zek_ec1", "……クク。孤独な王の誕生ですか。それもまた、一つの『作品』ですね。", "", actor=zek) \
        .say("zek_ec2", "私は……見届けさせてもらいましょう。孤独がどれほど重いか、記録するために。", "", actor=zek) \
        .say("narr_ec3", "（ゼクが影の中へ消える。）", "", actor=pc) \
        .set_flag(Keys.ENDING, FlagValues.Ending.USURP) \
        .jump(epilogue)

    # ========================================
    # エピローグ
    # ========================================
    builder.step(epilogue) \
        .play_bgm("BGM/Credits") \
        .say("narr_19", "（プレイヤーが光の階段を一歩踏み出すと、足元に温かな地上の風が吹き抜ける。）", "", actor=pc) \
        .say("narr_20", "（遠くに見えるのは、緑の大地と、穏やかな街の灯。）", "", actor=pc) \
        .say("narr_21", "かつて、異次元の闘技場に迷い込んだ一人の冒険者がいた。彼（彼女）は、絶望の底で友を得て、魂を賭けて戦い、ついには神をも超える存在となった。そして今、解放された魂は、新たな物語を紡ぎ始める——", "", actor=pc) \
        .jump(finale)

    # ========================================
    # スタッフロール後
    # ========================================
    builder.step(finale) \
        .play_bgm("BGM/Cheerful_Theme") \
        .say("balgas_f1", "……おい、いつまで感傷に浸ってんだ。次は俺の奢りで、地上で一番うまい酒を飲みに行くぞ！", "", actor=balgas) \
        .say("lily_f1", "ふふ、楽しみです。……リリィとして、初めての『デート』ですから。", "", actor=lily) \
        .say("zek_f1", "おや、私も混ぜてくださいよ。……商談という名の、ね。", "", actor=zek) \
        .complete_quest(QuestIds.LAST_BATTLE) \
        .say("sys_complete", "【システム】クエスト『最終決戦』をクリアしました！", "") \
        .finish()


def add_last_battle_result_steps(builder: ArenaDramaBuilder, victory_label: str, defeat_label: str, return_label: str):
    """
    最終決戦クエストの勝利/敗北ステップを arena_master ビルダーに追加する

    Args:
        builder: arena_master の ArenaDramaBuilder インスタンス
        victory_label: 勝利ステップのラベル名
        defeat_label: 敗北ステップのラベル名
        return_label: 結果表示後にジャンプするラベル名（敗北時のみ使用）
    """
    from drama_constants import DramaNames

    pc = Actors.PC
    lily = Actors.LILY
    balgas = Actors.BALGAS
    astaroth = Actors.ASTAROTH

    # ========================================
    # 最終決戦 勝利 - 続きのドラマを開始
    # ========================================
    # 勝利時は act5 以降の内容を別ドラマとして開始
    # last_battle ドラマの act5 以降を呼び出す
    builder.step(victory_label) \
        .set_flag("sukutsu_arena_result", 0) \
        .set_flag("sukutsu_quest_battle", 0) \
        .play_bgm("BGM/Victory_Epilogue") \
        .say("narr_v1", "（激闘の末、アスタロトの身体が崩れ始める。王座は砕け、アリーナの外壁は剥がれ落ち、そこから美しい『本当の星空』が姿を現した。）", "", actor=pc) \
        .say("astaroth_v1", "……見事だ。私は……ただ、この閉じられた孵化器を守るだけの、古い部品に過ぎなかったのかもしれないな。", "", actor=astaroth) \
        .say("astaroth_v2", "……リリィ、バルガス、ゼク。……そして新しき王よ。この世界の重さを、お前たちが分かち合うというのなら……私は、安心して土へ還ろう。", "", actor=astaroth) \
        .say("narr_v2", "（アスタロトが柔らかな光となって霧散し、そのレベル（重さ）が残された四人へと分散して吸収されていく。）", "", actor=pc) \
        .say("sys_title", "【システム】アスタロトの力の一部を吸収しました！全ステータス+10、全耐性+10 を獲得！", "") \
        .action("eval", param="Elin_SukutsuArena.ArenaManager.GrantLastBattleBonus();") \
        .say_and_start_drama("……続きがある。", DramaNames.LAST_BATTLE, "sukutsu_arena_master")

    # ========================================
    # 最終決戦 敗北
    # ========================================
    builder.step(defeat_label) \
        .set_flag("sukutsu_arena_result", 0) \
        .set_flag("sukutsu_quest_battle", 0) \
        .play_bgm("BGM/Lobby_Normal") \
        .say("narr_d1", "（アスタロトの圧倒的な力の前に、あなたは膝をついた。）", "", actor=pc) \
        .say("astaroth_d1", "……まだ、足りないな。お前の中に宿る可能性は、未だ開花していない。", "", actor=astaroth) \
        .say("astaroth_d2", "……出直して来い。私は、お前が『完成形』に至るまで待っていよう。", "", actor=astaroth) \
        .say("narr_d2", "（あなたは闘技場の入口へと戻された。再び挑戦するには、さらなる鍛錬が必要だ……。）", "", actor=pc) \
        .jump(return_label)
