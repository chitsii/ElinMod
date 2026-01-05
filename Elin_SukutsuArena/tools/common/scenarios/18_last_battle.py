"""
18_last_battle.md - 虚空の王、静寂の断罪
"""

from drama_builder import DramaBuilder
from flag_definitions import Keys, Actors, FlagValues

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

    # ラベル定義
    main = builder.label("main")
    act1 = builder.label("act1_preparations")
    act2 = builder.label("act2_throne_room")
    act3 = builder.label("act3_intervention")
    act4 = builder.label("act4_battle")
    act5 = builder.label("act5_victory")
    act6 = builder.label("act6_return")
    ending_choice = builder.label("ending_choice")
    ending_surface = builder.label("ending_surface")
    ending_rebuild = builder.label("ending_rebuild")
    ending_observers = builder.label("ending_observers")
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
        .say("lily_2", "私の真名……『リリアリス』。この名を知る者がいる限り、私はもう、アスタロト様の命令（システム）には従いません。……明日、王があなたの存在を消そうとしても、私がその因果を繋ぎ止めてみせます。", "", actor=lily) \
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
        .jump(act2)

    # ========================================
    # 第2幕: 虚空の王座
    # ========================================
    builder.step(act2) \
        .play_bgm("BGM/Astaroth_Throne") \
        .say("narr_5", "（翌朝、隠れ家からアリーナへ逆侵攻を開始したあなたたちは、異次元の壁を突き破り、王座の間へと辿り着く。）", "", actor=pc) \
        .say("narr_6", "（そこは、観客席すら存在しない『絶対的な静寂』の空間。アスタロトは、巨大な竜の翼を休め、孤独な王座に腰掛けていた。）", "", actor=pc) \
        .focus_chara(Actors.ASTAROTH) \
        .say("astaroth_1", "……よく来た。バグ（不具合）として生まれ、ついには世界を揺るがす『一億の質量』となった者よ。", "", actor=astaroth) \
        .say("astaroth_2", "ゼク、リリアリス、バルガス……。敗残兵と裏切り者の手を借りて、この私を終わらせに来たか。", "", actor=astaroth) \
        .say("astaroth_3", "だが、知るがいい。王とは、この世界そのもの。私の言葉は『法』であり、私の吐息は『消去』である。お前たちが何を積み上げようと、私が『無』と言えば、それは無になるのだ。", "", actor=astaroth) \
        .jump(act3)

    # ========================================
    # 第3幕: 神罰の解除——仲間の介入
    # ========================================
    builder.step(act3) \
        .play_bgm("BGM/Final_Battle") \
        .say("narr_7", "（戦闘開始直後、アスタロトの『レベル100,000,000』の威圧と共に、三つの極悪なデバフ（権能）があなたを襲う。）", "", actor=pc) \
        .say("narr_8", "（【権能1：時の独裁】——プレイヤーの速度を強制的に1に固定）", "", actor=pc) \
        .say("narr_9", "（【権能2：因果の拒絶】——プレイヤーの全攻撃ダメージを『1』に固定）", "", actor=pc) \
        .say("narr_10", "（【権能3：終焉の削除命令】——ターンごとにプレイヤーのステータスを恒久的に削り取る）", "", actor=pc) \
        .shake() \
        .say("narr_11", "（絶望的なエフェクトが画面を覆う中、仲間たちがそれぞれの覚悟を叫ぶ。）", "", actor=pc) \
        .focus_chara(Actors.ZEK) \
        .say("zek_11", "おっと、私のキューブが黙っていませんよ！ **【時の独裁】、一時的にオーバーライド（上書き）します！**", "", actor=zek) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_4", "鋼の意志を舐めるなよ！ 王の法なんて知るか！ **【因果の拒絶】、俺の魂でこじ開けてやる！**", "", actor=balgas) \
        .focus_chara(Actors.LILY) \
        .say("lily_3", "……真名にかけて命じます。この方の魂は、私のものです！ **【削除命令】、リリアリスの名において拒絶します！**", "", actor=lily) \
        .jump(act4)

    # ========================================
    # 第4幕: レベル1億の激突
    # ========================================
    builder.step(act4) \
        .focus_chara(Actors.ASTAROTH) \
        .say("narr_12", "（権能を封じられたアスタロトの瞳に、初めて『驚愕』と『喜び』が混じる。）", "", actor=pc) \
        .say("astaroth_4", "……ハハッ！ 面白い！ システムの保護なしに、この私と殴り合おうというのか！", "", actor=astaroth) \
        .say("astaroth_5", "よかろう、黄金の戦鬼よ！ 私が背負う『一億の絶望』と、お前が背負う『一億の希望』……どちらが真の理か、ここで決めようではないか！", "", actor=astaroth) \
        .say("narr_13", "（プレースホルダー：ここで実際の戦闘が発生する。）", "", actor=pc) \
        .jump(act5)

    # ========================================
    # 第5幕: 終焉と、はじまり
    # ========================================
    builder.step(act5) \
        .play_bgm("BGM/Victory_Epilogue") \
        .say("narr_14", "（激闘の末、アスタロトの身体が崩れ始める。王座は砕け、アリーナの外壁は剥がれ落ち、そこから美しい『本当の星空』が姿を現した。）", "", actor=pc) \
        .say("astaroth_6", "……見事だ。私は……ただ、この閉じられた孵化器を守るだけの、古い部品に過ぎなかったのかもしれないな。", "", actor=astaroth) \
        .say("astaroth_7", "……リリアリス、バルガス、ゼク。……そして新しき王よ。この世界の重さを、お前たちが分かち合うというのなら……私は、安心して土へ還ろう。", "", actor=astaroth) \
        .say("narr_15", "（アスタロトが柔らかな光となって霧散し、そのレベル（重さ）が残された四人へと分散して吸収されていく。）", "", actor=pc) \
        .focus_chara(Actors.ZEK) \
        .say("zek_12", "……やれやれ。これほどの損失（コスト）を出して、得られた利益は『自由』だけですか。……悪くない取引でしたね。", "", actor=zek) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_5", "ケッ、重てえな。だが、一人で背負うよりはマシだ。……おい、次はどこの酒場へ行く？", "", actor=balgas) \
        .focus_chara(Actors.LILY) \
        .say("lily_4", "……リリアリス、と呼んでくださいね。アリーナはなくなりました。でも、私たちの旅は、これから始まるのですから。", "", actor=lily) \
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
    builder.choice(ending_surface, "地上に戻る。まだやり残したことがある", "", text_id="ending_surface") \
           .choice(ending_rebuild, "ここに残る。この場所を、新しいギルドとして再建する", "", text_id="ending_rebuild") \
           .choice(ending_observers, "まだ戦いは終わっていない。『観客』たちのいる高次元世界へ挑む", "", text_id="ending_observers")

    # エンディングA: 地上への帰還
    builder.step(ending_surface) \
        .focus_chara(Actors.LILY) \
        .say("lily_e1", "……そうですか。では、いつでも戻ってきてくださいね。", "", actor=lily) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_e1", "ハッ、元気でやれよ。俺たちは、ここで待ってるぜ。", "", actor=balgas) \
        .focus_chara(Actors.ZEK) \
        .say("zek_e1", "ふふ、また会いましょう。次は、もっと良い商品を用意しておきますよ。", "", actor=zek) \
        .set_flag(Keys.ENDING, FlagValues.Ending.RETURN_TO_SURFACE) \
        .jump(epilogue)

    # エンディングB: ギルド再建
    builder.step(ending_rebuild) \
        .focus_chara(Actors.LILY) \
        .say("lily_e2", "……ふふ、嬉しいです。では、一緒に新しい場所を作りましょう。", "", actor=lily) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_e2", "ハッ、そうこなくちゃな。さあ、仕事だ。この廃墟を、最高のギルドに変えてやるぜ。", "", actor=balgas) \
        .focus_chara(Actors.ZEK) \
        .say("zek_e2", "ふむ、それなら私が店主を務めましょう。ククッ、繁盛しそうですね。", "", actor=zek) \
        .set_flag(Keys.ENDING, FlagValues.Ending.REBUILD_ARENA) \
        .jump(epilogue)

    # エンディングC: 高次元への挑戦
    builder.step(ending_observers) \
        .focus_chara(Actors.LILY) \
        .say("lily_e3", "……あなたらしいですね。では、私もついていきます。", "", actor=lily) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_e3", "ケッ、まだ戦うつもりか。……いいぜ、付き合ってやる。", "", actor=balgas) \
        .focus_chara(Actors.ZEK) \
        .say("zek_e3", "ふむ、面白そうですね。では、私も同行しましょう。", "", actor=zek) \
        .set_flag(Keys.ENDING, FlagValues.Ending.CHALLENGE_OBSERVERS) \
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
        .say("lily_f1", "ふふ、楽しみです。……リリアリスとして、初めての『デート』ですから。", "", actor=lily) \
        .say("zek_f1", "おや、私も混ぜてくださいよ。……商談という名の、ね。", "", actor=zek) \
        .finish()
