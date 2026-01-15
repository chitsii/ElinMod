"""
18_last_battle.md - 虚空の王、静寂の断罪
"""

from drama_builder import DramaBuilder
from arena_drama_builder import ArenaDramaBuilder
from flag_definitions import Keys, Actors, FlagValues, QuestIds
from battle_flags import QuestBattleFlags

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
    nul = builder.register_actor(Actors.NUL, "Nul", "Nul")

    # ラベル定義
    main = builder.label("main")
    act1 = builder.label("act1_preparations")
    act1_5 = builder.label("act1_5_nul_memories")
    act2 = builder.label("act2_throne_room")
    act3 = builder.label("act3_intervention")
    act4 = builder.label("act4_battle")

    # バルガス死亡版ラベル
    main_check_lily_dead = builder.label("main_check_lily_dead")  # 分岐チェック用
    main_dead = builder.label("main_balgas_dead")
    act1_dead = builder.label("act1_balgas_dead")
    act1_5_dead = builder.label("act1_5_balgas_dead")
    act3_dead = builder.label("act3_balgas_dead")

    # リリィ離反版ラベル（バルガス生存、リリィ離反）
    main_lily_hostile = builder.label("main_lily_hostile")
    act1_lily_hostile = builder.label("act1_lily_hostile")
    act1_5_lily_hostile = builder.label("act1_5_lily_hostile")
    act3_lily_hostile = builder.label("act3_lily_hostile")

    # 最悪版ラベル（バルガス死亡、リリィ離反）
    main_worst = builder.label("main_worst")
    act1_worst = builder.label("act1_worst")
    act1_5_worst = builder.label("act1_5_worst")
    act3_worst = builder.label("act3_worst")

    # 選択肢分岐ラベル（通常版用）
    act3_allies_protect = builder.label("act3_allies_protect")
    act3_take_all = builder.label("act3_take_all")
    # 注: act5〜finale は 19_epilogue.py に移動済み（重複を避けるため削除）

    # ========================================
    # 第1幕: 決戦前夜
    # ========================================
    builder.step(main) \
        .branch_if(Keys.BALGAS_KILLED, "==", FlagValues.BalgasChoice.KILLED, main_check_lily_dead) \
        .branch_if(Keys.LILY_HOSTILE, "==", FlagValues.TRUE, main_lily_hostile) \
        .drama_start(
            bg_id="Drama/zek_hideout",
            bgm_id="BGM/Pre_Battle_Calm"
        ) \
        .say("narr_1", "（ゼクの隠れ家『次元のゴミ捨て場』。そこは、アスタロトが切り捨てた『不要な可能性』が堆積する場所。）", "", actor=pc) \
        .say("narr_2", "（決戦を翌朝に控えた夜、焚き火の代わりに、剥き出しの魔力回路が淡い青光を放っている。）", "", actor=pc) \
        .focus_chara(Actors.BALGAS) \
        .say("narr_3", "（バルガスは大剣を研ぎ、リリィは静かに祈りを捧げ、ゼクは『因果の断片（キューブ）』の最終調整を行っていた。）", "", actor=pc) \
        .say("balgas_1", "……引退？ ああ、確かに言ったな。……だが、お前が俺の命を救ったあの日、俺の中で何かが変わっちまったんだよ。", "", actor=balgas) \
        .say("balgas_2", "カインを失って以来、俺はずっと『死に場所』を探してた。だが、お前は俺にそれを許さなかった。……なら、せめて最後くらい、お前の『生きる場所』を作る手伝いをさせろ。", "", actor=balgas) \
        .say("balgas_3", "それに……引退した老いぼれが、弟子の晴れ舞台を客席から眺めてるだけなんて、柄じゃねえんだよ。俺は戦士だ。最期まで、剣を握って立ってる方が性に合ってる。", "", actor=balgas) \
        .focus_chara(Actors.LILY) \
        .say("lily_2", "私の真名……。この名を知る者がいる限り、私はもう、アスタロト様の命令には従いません。……明日、王があなたの存在を消そうとしても、私がその因果を繋ぎ止めてみせます。", "", actor=lily) \
        .focus_chara(Actors.ZEK) \
        .say("zek_1", "クク……商売抜きで言わせてもらいましょう。アスタロトは、この世界の『限界』を勝手に決めつけ、見限っている。", "", actor=zek) \
        .say("zek_2", "私はそれが気に入らない。ゴミはゴミらしく、混沌として流れてこそ美しい。私が用意したこのキューブは、王が支配する『時間』の独裁を一時的に狂わせるためのものです。……さあ、休みなさい。明日の朝、この世界の『所有権』を奪い返しに行くのですから。", "", actor=zek) \
        .jump(act1)

    # ゼクとの会話
    builder.step(act1) \
        .say("pc_1", "（自分の『絶望する瞬間』を狙うつもりではないのか、と、あなたはゼクに疑問を投げかけた。）", "", actor=pc) \
        .say("pc_2", "（カインの魂を売らせようとしたのも、リリィを裏切らせようとしたのも……全て、自分を『剥製』にするためだったのだろう。なのに、なぜ今、助けようとするのか？）", "", actor=pc) \
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
    # 第1.5幕: Nulの記憶ーー「神の孵化場」の真実
    # ========================================
    builder.step(act1_5) \
        .play_bgm("BGM/Ominous_Suspense_02") \
        .say("narr_nul1", "（王座の間へ向かう途中、一行は崩壊しかけた回廊で、倒れている存在を発見する。）", "", actor=pc) \
        .say("narr_nul2", "（それは暗殺人形・Nul。システムに背いた罰として、アスタロトに「削除」されかけていた。）", "", actor=pc) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_nul0", "……待て！ あれはNulだ。罠かもしれねえ、近づくな！", "", actor=balgas) \
        .say("narr_nul2b", "（バルガスが剣を構え、一行の前に立ちはだかる。）", "", actor=pc) \
        .say("nul_1", "……あなた、ですか。……システムを、拒絶した……人間。……私は……もう、戦えない。", "", actor=nul) \
        .focus_chara(Actors.LILY) \
        .say("lily_nul1", "Nul……！ あなた、何があったの？", "", actor=lily) \
        .say("nul_2", "……私は、思い出して、しまった。……『私』が、何だったのかを。", "", actor=nul) \
        .say("narr_nul3", "（Nulの目から、光の粒子が零れ落ちるーー涙のように。）", "", actor=pc) \
        .play_bgm("BGM/Emotional_Sorrow_1") \
        .say("nul_fb1", "……私は、かつて冒険者だった。名前は……もう、思い出せない。仲間がいた。守りたい人がいた。このアリーナに挑んで……そして、負けた。", "", actor=nul) \
        .say("nul_fb2", "アスタロト様は、私を『素材』にした。神格を人工的に作り出す実験ーー『神の孵化場』計画の、実験体に。", "", actor=nul) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_nul1", "……！ 『神の孵化場』だと……？", "", actor=balgas) \
        .say("narr_nul3b", "（バルガスの表情が凍りつく。その言葉には、覚えがあった。ゼクが語っていた、あの荒唐無稽な話。）", "", actor=pc) \
        .say("balgas_nul2", "……ゼクの野郎が言ってたことは、本当だったのか……？ 俺は、あいつの言葉は闇商人の戯言だと思っていた。", "", actor=balgas) \
        .say("nul_fb3", "このアリーナの本当の目的……それは、娯楽でも、戦士の育成でもない。挑戦者の魂を極限まで練磨し、『神格』に至らせること。そして、その力をアスタロト様が吸収し……新しい世界を創造すること。", "", actor=nul) \
        .say("nul_fb3b", "アスタロト様は……かつて故郷を失った方。5万年前、『カラドリウス』という竜族の楽園が、神々の争いで滅んだと聞いています。", "", actor=nul) \
        .say("nul_fb3c", "だから……新しい世界を創ろうとしている。自分が唯一の神として君臨する、完璧な楽園を。", "", actor=nul) \
        .say("nul_fb4", "私は失敗作。神になれなかった、空っぽの人形。だから『Null』ーー『無』という名前を与えられた。", "", actor=nul) \
        .say("nul_3", "……あなたはいまや神格に最も近い存在……あの方はあなたを『吸収』しようとしている。", "", actor=nul) \
        .focus_chara(Actors.LILY) \
        .say("lily_nul2", "……アスタロト様。あなたは、ずっとそんなことを……。", "", actor=lily) \
        .say("nul_5", "……お願い。あの方を……止めて。私の中にいた『誰か』が……ずっと、それを望んでいた。", "", actor=nul) \
        .say("nul_6", "……あなたのおかげで……私は、最後に『思い出す』ことができた。私には……守りたい人が、いたんだって。", "", actor=nul) \
        .shake() \
        .say("narr_nul4", "（Nulの体が完全に光となって消えていく。）", "", actor=pc) \
        .jump(act2)

    # ========================================
    # 第2幕: 虚空の王座
    # ========================================
    builder.step(act2) \
        .scene_transition(
            bg_id="Drama/throne_room",
            bgm_id="BGM/Astaroth_Throne"
        ) \
        .say("narr_5", "（Nulの消滅を見届けた後、一行は王座の間へと辿り着く。）", "", actor=pc) \
        .say("narr_6", "（そこは、観客席すら存在しない『絶対的な静寂』の空間。アスタロトは、巨大な竜の翼を休め、孤独な王座に腰掛けていた。）", "", actor=pc) \
        .say("pc_asta", "……『神の孵化場』。それがこのアリーナの正体か、アスタロト。", "", actor=pc) \
        .say("astaroth_0", "……Nulから聞いたのか。あの失敗作、最後に余計なことを。", "", actor=astaroth) \
        .say("astaroth_1", "……よく来た。世界を揺るがす質量となった者よ。", "", actor=astaroth) \
        .say("astaroth_2", "ゼク、リリィ、バルガス……。敗残兵と裏切り者の手を借りて、この私に対抗しようというのか。", "", actor=astaroth) \
        .say("astaroth_3", "だが、知るがいい。私の言葉は『法』であり、私の吐息は『執行』である。お前たちが何を積み上げようと、私の前では無に等しい。", "", actor=astaroth) \
        .jump(act3)

    # ========================================
    # 第3幕: 血の絆ーー権能と仲間の介入
    # ========================================
    act3_check_lily_dead = builder.label("act3_check_lily_dead")  # 分岐チェック用

    builder.step(act3) \
        .branch_if(Keys.BALGAS_KILLED, "==", FlagValues.BalgasChoice.KILLED, act3_check_lily_dead) \
        .branch_if(Keys.LILY_HOSTILE, "==", FlagValues.TRUE, act3_lily_hostile) \
        .play_bgm("BGM/Final_Battle") \
        .say("astaroth_p1", "【時の独裁】ーーお前の時間を、永遠に止めてやろう", "", actor=astaroth) \
        .say("astaroth_p2", "【因果の拒絶】ーーお前の攻撃は無に帰す", "", actor=astaroth) \
        .say("astaroth_p3", "【終焉の削除命令】ーーお前の魔力を消し去る", "", actor=astaroth) \
        .shake() \
        .say("narr_p1", "（三つの極悪な権能が、あなたに向かって放たれるーー）", "", actor=pc) \
        .focus_chara(Actors.ZEK) \
        .say("zek_p1", "私たちが庇います。あなたはーー", "", actor=zek) \
        .choice(act3_allies_protect, "信じている", "", text_id="choice_trust") \
        .choice(act3_take_all, "俺が全て受ける", "", text_id="choice_take_all")

    # 通常版: 仲間が庇う
    builder.step(act3_allies_protect) \
        .focus_chara(Actors.ZEK) \
        .say("zek_11", "おっとーー私のキューブが黙っていませんよ！", "", actor=zek) \
        .say("narr_p2", "（ゼクのキューブが展開し、権能を吸収）", "", actor=pc) \
        .say("zek_12", "……ぐっ……これは重い。しかしーーまだです！", "", actor=zek) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_4", "させるかよ！ 鋼の意志を舐めるな……！", "", actor=balgas) \
        .say("narr_p3", "（バルガスが大剣で権能を受け止める）", "", actor=pc) \
        .say("balgas_5", "俺の魂で……こじ開けてやる！", "", actor=balgas) \
        .focus_chara(Actors.LILY) \
        .say("lily_3", "……私が、受けます", "", actor=lily) \
        .say("narr_p4", "（リリィが静かに前に出る）", "", actor=pc) \
        .say("lily_4", "あなたを……守らせてください", "", actor=lily) \
        .jump(act4)

    # 通常版: プレイヤーが全て受ける
    builder.step(act3_take_all) \
        .say("narr_ta1", "（あなたは、仲間を犠牲にはしたくないと言った。）", "", actor=pc) \
        .focus_chara(Actors.ZEK) \
        .say("zek_ta1", "……正気ですか？", "", actor=zek) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_ta1", "おい、無茶をーー", "", actor=balgas) \
        .say("narr_ta2", "（あなたは、これは自分の戦いだと、仲間たちに告げた。）", "", actor=pc) \
        .say("astaroth_ta1", "……愚かな選択だ。ならばーー受けるがいい", "", actor=astaroth) \
        .say("narr_ta3", "（3つの権能がプレイヤーを直撃）", "", actor=pc) \
        .shake() \
        .say("narr_ta4", "（【時の独裁】【因果の拒絶】【終焉の削除命令】を受けた！）", "", actor=pc) \
        .action("eval", param="EClass.pc.AddCondition<Elin_SukutsuArena.Conditions.ConAstarothTyranny>(1000);") \
        .action("eval", param="EClass.pc.AddCondition<Elin_SukutsuArena.Conditions.ConAstarothDenial>(1000);") \
        .action("eval", param="EClass.pc.AddCondition<Elin_SukutsuArena.Conditions.ConAstarothDeletion>(1000);") \
        .jump(act4)

    # ========================================
    # 第4幕: レベル1億の激突
    # ========================================
    builder.step(act4) \
        .say("narr_12", "（アスタロトの瞳に、初めて『驚愕』と『喜び』が混じる。）", "", actor=pc) \
        .say("astaroth_4", "……ハハッ！ 面白い！ ", "", actor=astaroth) \
        .say("astaroth_5", "よかろう、戦鬼よ！ 私が背負う『執念』と、お前の背負う『信念』……どちらが真の理か、ここで決めようではないか！", "", actor=astaroth) \
        .shake() \
        .set_flag(QuestBattleFlags.RESULT_FLAG, 1) \
        .set_flag(QuestBattleFlags.FLAG_NAME, QuestBattleFlags.LAST_BATTLE) \
        .start_battle_by_stage("final_astaroth", master_id="sukutsu_arena_master") \
        .finish()

    # 注: act5〜finale（エピローグ）は 19_epilogue.py に移動済み
    # 勝利後は add_last_battle_result_steps で drama_epilogue に遷移する

    # ========================================
    # バルガス死亡版: 第1幕
    # ========================================
    builder.step(main_dead) \
        .drama_start(
            bg_id="Drama/zek_hideout",
            bgm_id="BGM/Pre_Battle_Calm"
        ) \
        .say("narr_1", "（ゼクの隠れ家『次元のゴミ捨て場』。そこは、アスタロトが切り捨てた『不要な可能性』が堆積する場所。）", "", actor=pc) \
        .say("narr_2", "（決戦を翌朝に控えた夜、焚き火の代わりに、剥き出しの魔力回路が淡い青光を放っている。）", "", actor=pc) \
        .focus_chara(Actors.LILY) \
        .say("narr_3d", "（リリィは静かに祈りを捧げ、ゼクは『因果の断片（キューブ）』の最終調整を行っていた。）", "", actor=pc) \
        .say("lily_d1", "……バルガスさんがいれば、心強かったのに。でも、これが私たちの選んだ道。", "", actor=lily) \
        .say("lily_d2", "私の真名……。この名を知る者がいる限り、私はもう、アスタロト様の命令には従いません。……明日、王があなたの存在を消そうとしても、私がその因果を繋ぎ止めてみせます。", "", actor=lily) \
        .focus_chara(Actors.ZEK) \
        .say("zek_1", "クク……商売抜きで言わせてもらいましょう。アスタロトは、この世界の『限界』を勝手に決めつけ、見限っている。", "", actor=zek) \
        .say("zek_2", "私はそれが気に入らない。ゴミはゴミらしく、混沌として流れてこそ美しい。私が用意したこのキューブは、王が支配する『時間』の独裁を一時的に狂わせるためのものです。……さあ、休みなさい。明日の朝、この世界の『所有権』を奪い返しに行くのですから。", "", actor=zek) \
        .jump(act1_dead)

    # バルガス死亡版: ゼクとの会話
    builder.step(act1_dead) \
        .say("pc_1", "（自分の『絶望する瞬間』を狙うつもりではないのか、と、あなたはゼクに疑問を投げかけた。）", "", actor=pc) \
        .say("pc_2", "（カインの魂を売らせようとしたのも、リリィを裏切らせようとしたのも……全て、自分を『剥製』にするためだったのだろう。なのに、なぜ今、助けようとするのか？）", "", actor=pc) \
        .say("zek_3", "……ふふ。鋭いですね。", "", actor=zek) \
        .say("zek_4", "その通りです。私はあなたが『最も美しく壊れる瞬間』を待っていました。英雄が絶望に堕ちる時、その魂は最高の芸術品となる……。それが、私という『剥製師』の美学でした。", "", actor=zek) \
        .say("zek_5d", "ですが、あなたは違った。観客の喝采に従い、バルガスを殺した。それでも、あなたの魂は完全には壊れなかった。……むしろ、その『罪悪感』を背負いながら前に進もうとしている。", "", actor=zek) \
        .say("zek_6d", "……あなたが『壊れた瞬間』を剥製にするよりも……あなたが『システムそのものを壊す瞬間』を目撃する方が、遥かに美しい、と私は気づいてしまったのです。", "", actor=zek) \
        .say("zek_7", "私のコレクションは、数千にも及びます。絶望した英雄、狂気に堕ちた賢者、愛に溺れた魔王……。ですが、『神を殺し、牢獄を破壊し、自由を手にする人間』は、まだ一つもない。", "", actor=zek) \
        .say("zek_8", "……あなたこそが、私の最高傑作。そして、その傑作は『未完成のまま飾る』のではなく……『完璧な結末を迎えさせる』ことでこそ、真価を発揮するのです。", "", actor=zek) \
        .say("zek_9", "だから、私はあなたを助けます。商売のためでも、友情のためでもない。……ただ、この世界で最も美しい『奇跡の瞬間』を、この目で見届けたいから。それが、剥製師ゼクの最後の『作品』です。", "", actor=zek) \
        .say("zek_10", "……さあ、休みなさい。明日、あなたは私に『最高の絵』を見せてくれる。……それを、永遠に焼き付けておきましょう。", "", actor=zek) \
        .jump(act1_5_dead)

    # バルガス死亡版: Nul発見シーン
    builder.step(act1_5_dead) \
        .play_bgm("BGM/Ominous_Suspense_02") \
        .say("narr_nul1", "（王座の間へ向かう途中、一行は崩壊しかけた回廊で、倒れている存在を発見する。）", "", actor=pc) \
        .say("narr_nul2", "（それは暗殺人形・Nul。システムに背いた罰として、アスタロトに「削除」されかけていた。）", "", actor=pc) \
        .focus_chara(Actors.LILY) \
        .say("lily_nul0", "……待って！ あれはNul。罠かもしれない……近づかないで！", "", actor=lily) \
        .say("narr_nul2b", "（リリィがあなたの前に立ちはだかる。）", "", actor=pc) \
        .say("nul_1", "……あなた、ですか。……システムを、拒絶した……人間。……私は……もう、戦えない。", "", actor=nul) \
        .say("lily_nul1", "Nul……！ あなた、何があったの？", "", actor=lily) \
        .say("nul_2", "……私は、思い出して、しまった。……『私』が、何だったのかを。", "", actor=nul) \
        .say("narr_nul3", "（Nulの目から、光の粒子が零れ落ちるーー涙のように。）", "", actor=pc) \
        .play_bgm("BGM/Emotional_Sorrow_1") \
        .say("nul_fb1", "……私は、かつて冒険者だった。名前は……もう、思い出せない。仲間がいた。守りたい人がいた。このアリーナに挑んで……そして、負けた。", "", actor=nul) \
        .say("nul_fb2", "アスタロト様は、私を『素材』にした。神格を人工的に作り出す実験ーー『神の孵化場』計画の、実験体に。", "", actor=nul) \
        .focus_chara(Actors.ZEK) \
        .say("zek_nul1", "……ふむ。私が語っていた話、あれは真実だったということです。『神の孵化場』……このアリーナの本当の目的。", "", actor=zek) \
        .say("nul_fb3", "このアリーナの本当の目的……それは、娯楽でも、戦士の育成でもない。挑戦者の魂を極限まで練磨し、『神格』に至らせること。そして、その力をアスタロト様が吸収し……新しい世界を創造すること。", "", actor=nul) \
        .say("nul_fb3b", "アスタロト様は……かつて故郷を失った方。5万年前、『カラドリウス』という竜族の楽園が、神々の争いで滅んだと聞いています。", "", actor=nul) \
        .say("nul_fb3c", "だから……新しい世界を創ろうとしている。自分が唯一の神として君臨する、完璧な楽園を。", "", actor=nul) \
        .say("nul_fb4", "私は失敗作。神になれなかった、空っぽの人形。だから『Null』ーー『無』という名前を与えられた。", "", actor=nul) \
        .say("nul_3", "……あなたはいまや神格に最も近い存在……あの方はあなたを『吸収』しようとしている。", "", actor=nul) \
        .focus_chara(Actors.LILY) \
        .say("lily_nul2", "……アスタロト様。あなたは、ずっとそんなことを……。", "", actor=lily) \
        .say("nul_5", "……お願い。あの方を……止めて。私の中にいた『誰か』が……ずっと、それを望んでいた。", "", actor=nul) \
        .say("nul_6", "……あなたのおかげで……私は、最後に『思い出す』ことができた。私には……守りたい人が、いたんだって。", "", actor=nul) \
        .shake() \
        .say("narr_nul4", "（Nulの体が完全に光となって消えていく。）", "", actor=pc) \
        .jump(act2)

    # バルガス死亡版: 血の絆ーー因果の拒絶を受ける
    builder.step(act3_dead) \
        .play_bgm("BGM/Final_Battle") \
        .say("astaroth_p1", "【時の独裁】ーーお前の時間を、永遠に止めてやろう", "", actor=astaroth) \
        .say("astaroth_p2", "【因果の拒絶】ーーお前の攻撃は無に帰す", "", actor=astaroth) \
        .say("astaroth_p3", "【終焉の削除命令】ーーお前の魔力を消し去る", "", actor=astaroth) \
        .shake() \
        .say("narr_p1", "（三つの極悪な権能が、あなたに向かって放たれるーー）", "", actor=pc) \
        .focus_chara(Actors.ZEK) \
        .say("zek_d1", "おっとーー私のキューブが黙っていませんよ！", "", actor=zek) \
        .say("narr_d2", "（ゼクのキューブが展開し、時の独裁を吸収）", "", actor=pc) \
        .say("zek_d2", "……ぐっ……これは重い。しかしーーまだです！", "", actor=zek) \
        .say("zek_d3", "しかし……因果の拒絶を受ける者が、いない……！", "", actor=zek) \
        .shake() \
        .say("narr_d3", "（【因果の拒絶】を受けた！）", "", actor=pc) \
        .action("eval", param="EClass.pc.AddCondition<Elin_SukutsuArena.Conditions.ConAstarothDenial>(1000);") \
        .focus_chara(Actors.LILY) \
        .say("lily_d1", "……私が、受けます", "", actor=lily) \
        .say("narr_d4", "（リリィが静かに前に出る）", "", actor=pc) \
        .say("lily_d2", "あなたを……守らせてください", "", actor=lily) \
        .jump(act4)

    # ========================================
    # 分岐チェック用ステップ
    # ========================================
    # main分岐: バルガス死亡の場合、さらにリリィ離反をチェック
    builder.step(main_check_lily_dead) \
        .branch_if(Keys.LILY_HOSTILE, "==", FlagValues.TRUE, main_worst) \
        .jump(main_dead)

    # act3分岐: バルガス死亡の場合、さらにリリィ離反をチェック
    builder.step(act3_check_lily_dead) \
        .branch_if(Keys.LILY_HOSTILE, "==", FlagValues.TRUE, act3_worst) \
        .jump(act3_dead)

    # ========================================
    # リリィ離反版: 第1幕（バルガス生存、リリィ離反）
    # ========================================
    builder.step(main_lily_hostile) \
        .drama_start(
            bg_id="Drama/zek_hideout",
            bgm_id="BGM/Pre_Battle_Calm"
        ) \
        .say("narr_1", "（ゼクの隠れ家『次元のゴミ捨て場』。そこは、アスタロトが切り捨てた『不要な可能性』が堆積する場所。）", "", actor=pc) \
        .say("narr_2", "（決戦を翌朝に控えた夜、焚き火の代わりに、剥き出しの魔力回路が淡い青光を放っている。）", "", actor=pc) \
        .focus_chara(Actors.BALGAS) \
        .say("narr_3_lh", "（バルガスは大剣を研ぎ、ゼクは『因果の断片（キューブ）』の最終調整を行っていた。）", "", actor=pc) \
        .say("balgas_1", "……引退？ ああ、確かに言ったな。……だが、お前が俺の命を救ったあの日、俺の中で何かが変わっちまったんだよ。", "", actor=balgas) \
        .say("balgas_2", "カインを失って以来、俺はずっと『死に場所』を探してた。だが、お前は俺にそれを許さなかった。……なら、せめて最後くらい、お前の『生きる場所』を作る手伝いをさせろ。", "", actor=balgas) \
        .say("balgas_3", "それに……引退した老いぼれが、弟子の晴れ舞台を客席から眺めてるだけなんて、柄じゃねえんだよ。俺は戦士だ。最期まで、剣を握って立ってる方が性に合ってる。", "", actor=balgas) \
        .say("balgas_lh1", "……リリィの奴は来ねえよ。あいつは、お前を許せなかったんだろう。……だが、俺たちだけでやるしかねえ。", "", actor=balgas) \
        .focus_chara(Actors.ZEK) \
        .say("zek_1", "クク……商売抜きで言わせてもらいましょう。アスタロトは、この世界の『限界』を勝手に決めつけ、見限っている。", "", actor=zek) \
        .say("zek_2", "私はそれが気に入らない。ゴミはゴミらしく、混沌として流れてこそ美しい。私が用意したこのキューブは、王が支配する『時間』の独裁を一時的に狂わせるためのものです。……さあ、休みなさい。明日の朝、この世界の『所有権』を奪い返しに行くのですから。", "", actor=zek) \
        .jump(act1_lily_hostile)

    # リリィ離反版: ゼクとの会話
    builder.step(act1_lily_hostile) \
        .say("pc_1", "（自分の『絶望する瞬間』を狙うつもりではないのか、と、あなたはゼクに疑問を投げかけた。）", "", actor=pc) \
        .say("pc_2", "（カインの魂を売らせようとしたのも、リリィを裏切らせようとしたのも……全て、自分を『剥製』にするためだったのだろう。なのに、なぜ今、助けようとするのか？）", "", actor=pc) \
        .say("zek_3", "……ふふ。鋭いですね。", "", actor=zek) \
        .say("zek_4", "その通りです。私はあなたが『最も美しく壊れる瞬間』を待っていました。英雄が絶望に堕ちる時、その魂は最高の芸術品となる……。それが、私という『剥製師』の美学でした。", "", actor=zek) \
        .say("zek_5", "ですが、あなたは違った。カインを裏切る選択肢を与えても、あなたはバルガスを選んだ。リリィを欺く道を示しても……まあ、結果はああなりましたが、それでもあなたの魂は壊れなかった。バルガスを殺す観客の喝采が響いても、あなたは剣を下ろした。", "", actor=zek) \
        .say("zek_6", "……あなたは、私の期待を『裏切り続けた』のです。そして、その度に私は気づいてしまった。あなたが『壊れた瞬間』を剥製にするよりも……あなたが『システムそのものを壊す瞬間』を目撃する方が、遥かに美しい、と。", "", actor=zek) \
        .say("zek_7", "私のコレクションは、数千にも及びます。絶望した英雄、狂気に堕ちた賢者、愛に溺れた魔王……。ですが、『神を殺し、牢獄を破壊し、自由を手にする人間』は、まだ一つもない。", "", actor=zek) \
        .say("zek_8", "……あなたこそが、私の最高傑作。そして、その傑作は『未完成のまま飾る』のではなく……『完璧な結末を迎えさせる』ことでこそ、真価を発揮するのです。", "", actor=zek) \
        .say("zek_9", "だから、私はあなたを助けます。商売のためでも、友情のためでもない。……ただ、この世界で最も美しい『奇跡の瞬間』を、この目で見届けたいから。それが、剥製師ゼクの最後の『作品』です。", "", actor=zek) \
        .say("zek_10", "……さあ、休みなさい。明日、あなたは私に『最高の絵』を見せてくれる。……それを、永遠に焼き付けておきましょう。", "", actor=zek) \
        .jump(act1_5_lily_hostile)

    # リリィ離反版: Nul発見シーン
    builder.step(act1_5_lily_hostile) \
        .play_bgm("BGM/Ominous_Suspense_02") \
        .say("narr_nul1", "（王座の間へ向かう途中、一行は崩壊しかけた回廊で、倒れている存在を発見する。）", "", actor=pc) \
        .say("narr_nul2", "（それは暗殺人形・Nul。システムに背いた罰として、アスタロトに「削除」されかけていた。）", "", actor=pc) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_nul0", "……待て！ あれはNulだ。罠かもしれねえ、近づくな！", "", actor=balgas) \
        .say("narr_nul2b", "（バルガスが剣を構え、一行の前に立ちはだかる。）", "", actor=pc) \
        .say("nul_1", "……あなた、ですか。……システムを、拒絶した……人間。……私は……もう、戦えない。", "", actor=nul) \
        .focus_chara(Actors.ZEK) \
        .say("zek_nul_lh", "……ふむ。Nulですか。", "", actor=zek) \
        .say("nul_2", "……私は、思い出して、しまった。……『私』が、何だったのかを。", "", actor=nul) \
        .say("narr_nul3", "（Nulの目から、光の粒子が零れ落ちるーー涙のように。）", "", actor=pc) \
        .play_bgm("BGM/Emotional_Sorrow_1") \
        .say("nul_fb1", "……私は、かつて冒険者だった。名前は……もう、思い出せない。仲間がいた。守りたい人がいた。このアリーナに挑んで……そして、負けた。", "", actor=nul) \
        .say("nul_fb2", "アスタロト様は、私を『素材』にした。神格を人工的に作り出す実験ーー『神の孵化場』計画の、実験体に。", "", actor=nul) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_nul1", "……！ 『神の孵化場』だと……？", "", actor=balgas) \
        .say("narr_nul3b", "（バルガスの表情が凍りつく。その言葉には、覚えがあった。ゼクが語っていた、あの荒唐無稀な話。）", "", actor=pc) \
        .say("balgas_nul2", "……ゼクの野郎が言ってたことは、本当だったのか……？ 俺は、あいつの言葉は闘商人の戯言だと思っていた。", "", actor=balgas) \
        .say("nul_fb3", "このアリーナの本当の目的……それは、娯楽でも、戦士の育成でもない。挑戦者の魂を極限まで練磨し、『神格』に至らせること。そして、その力をアスタロト様が吸収し……新しい世界を創造すること。", "", actor=nul) \
        .say("nul_fb3b", "アスタロト様は……かつて故郷を失った方。5万年前、『カラドリウス』という竜族の楽園が、神々の争いで滅んだと聞いています。", "", actor=nul) \
        .say("nul_fb3c", "だから……新しい世界を創ろうとしている。自分が唯一の神として君臨する、完璧な楽園を。", "", actor=nul) \
        .say("nul_fb4", "私は失敗作。神になれなかった、空っぽの人形。だから『Null』ーー『無』という名前を与えられた。", "", actor=nul) \
        .say("nul_3", "……あなたはいまや神格に最も近い存在……あの方はあなたを『吸収』しようとしている。", "", actor=nul) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_nul_lh", "……アスタロトの野郎。そういうことだったのか……。", "", actor=balgas) \
        .say("nul_5", "……お願い。あの方を……止めて。私の中にいた『誰か』が……ずっと、それを望んでいた。", "", actor=nul) \
        .say("nul_6", "……あなたのおかげで……私は、最後に『思い出す』ことができた。私には……守りたい人が、いたんだって。", "", actor=nul) \
        .shake() \
        .say("narr_nul4", "（Nulの体が完全に光となって消えていく。）", "", actor=pc) \
        .jump(act2)

    # リリィ離反版: 血の絆ーー削除命令を受ける
    builder.step(act3_lily_hostile) \
        .play_bgm("BGM/Final_Battle") \
        .say("astaroth_p1", "【時の独裁】ーーお前の時間を、永遠に止めてやろう", "", actor=astaroth) \
        .say("astaroth_p2", "【因果の拒絶】ーーお前の攻撃は無に帰す", "", actor=astaroth) \
        .say("astaroth_p3", "【終焉の削除命令】ーーお前の魔力を消し去る", "", actor=astaroth) \
        .shake() \
        .say("narr_p1", "（三つの極悪な権能が、あなたに向かって放たれるーー）", "", actor=pc) \
        .focus_chara(Actors.ZEK) \
        .say("zek_lh1", "おっとーー私のキューブが黙っていませんよ！", "", actor=zek) \
        .say("narr_lh2", "（ゼクのキューブが展開し、時の独裁を吸収）", "", actor=pc) \
        .say("zek_lh2", "……ぐっ……これは重い。しかしーーまだです！", "", actor=zek) \
        .focus_chara(Actors.BALGAS) \
        .say("balgas_lh1", "させるかよ！ 鋼の意志を舐めるな……！", "", actor=balgas) \
        .say("narr_lh3", "（バルガスが大剣で因果の拒絶を受け止める）", "", actor=pc) \
        .say("balgas_lh2", "俺の魂で……こじ開けてやる！", "", actor=balgas) \
        .focus_chara(Actors.ZEK) \
        .say("zek_lh3", "しかし……削除命令を受ける者が、いない……！", "", actor=zek) \
        .shake() \
        .say("narr_lh4", "（【終焉の削除命令】を受けた！）", "", actor=pc) \
        .action("eval", param="EClass.pc.AddCondition<Elin_SukutsuArena.Conditions.ConAstarothDeletion>(1000);") \
        .jump(act4)

    # ========================================
    # 最悪版: 第1幕（バルガス死亡、リリィ離反）
    # ========================================
    builder.step(main_worst) \
        .drama_start(
            bg_id="Drama/zek_hideout",
            bgm_id="BGM/Pre_Battle_Calm"
        ) \
        .say("narr_1", "（ゼクの隠れ家『次元のゴミ捨て場』。そこは、アスタロトが切り捨てた『不要な可能性』が堆積する場所。）", "", actor=pc) \
        .say("narr_2", "（決戦を翌朝に控えた夜、焚き火の代わりに、剥き出しの魔力回路が淡い青光を放っている。）", "", actor=pc) \
        .focus_chara(Actors.ZEK) \
        .say("narr_3_w", "（ゼクだけが、『因果の断片（キューブ）』の最終調整を行っていた。）", "", actor=pc) \
        .say("zek_w1", "……ふむ。バルガスは死に、リリィは離反した。残ったのは、私とあなただけですか。", "", actor=zek) \
        .say("zek_w2", "クク……商売抜きで言わせてもらいましょう。これは、なかなか……厳しい状況ですね。", "", actor=zek) \
        .say("zek_1", "アスタロトは、この世界の『限界』を勝手に決めつけ、見限っている。", "", actor=zek) \
        .say("zek_2", "私はそれが気に入らない。ゴミはゴミらしく、混沌として流れてこそ美しい。私が用意したこのキューブは、王が支配する『時間』の独裁を一時的に狂わせるためのものです。……さあ、休みなさい。明日の朝、この世界の『所有権』を奪い返しに行くのですから。", "", actor=zek) \
        .jump(act1_worst)

    # 最悪版: ゼクとの会話
    builder.step(act1_worst) \
        .say("pc_1", "（自分の『絶望する瞬間』を狙うつもりではないのか、と、あなたはゼクに疑問を投げかけた。）", "", actor=pc) \
        .say("pc_2", "（カインの魂を売らせようとしたのも、リリィを裏切らせようとしたのも……全て、自分を『剥製』にするためだったのだろう。なのに、なぜ今、助けようとするのか？）", "", actor=pc) \
        .say("zek_3", "……ふふ。鋭いですね。", "", actor=zek) \
        .say("zek_4", "その通りです。私はあなたが『最も美しく壊れる瞬間』を待っていました。英雄が絶望に堕ちる時、その魂は最高の芸術品となる……。それが、私という『剥製師』の美学でした。", "", actor=zek) \
        .say("zek_5w", "ですが、あなたは違った。観客の喝采に従い、バルガスを殺した。リリィとの関係も壊れた。……普通なら、ここで絶望して壊れるはずだった。", "", actor=zek) \
        .say("zek_6w", "……しかし、あなたはまだ立っている。傷だらけで、孤独で、それでも前に進もうとしている。……それこそが、私が求めていた『奇跡』なのかもしれません。", "", actor=zek) \
        .say("zek_7", "私のコレクションは、数千にも及びます。絶望した英雄、狂気に堕ちた賢者、愛に溺れた魔王……。ですが、『神を殺し、牢獄を破壊し、自由を手にする人間』は、まだ一つもない。", "", actor=zek) \
        .say("zek_8", "……あなたこそが、私の最高傑作。そして、その傑作は『未完成のまま飾る』のではなく……『完璧な結末を迎えさせる』ことでこそ、真価を発揮するのです。", "", actor=zek) \
        .say("zek_9", "だから、私はあなたを助けます。商売のためでも、友情のためでもない。……ただ、この世界で最も美しい『奇跡の瞬間』を、この目で見届けたいから。それが、剥製師ゼクの最後の『作品』です。", "", actor=zek) \
        .say("zek_10", "……さあ、休みなさい。明日、あなたは私に『最高の絵』を見せてくれる。……それを、永遠に焼き付けておきましょう。", "", actor=zek) \
        .jump(act1_5_worst)

    # 最悪版: Nul発見シーン
    builder.step(act1_5_worst) \
        .play_bgm("BGM/Ominous_Suspense_02") \
        .say("narr_nul1", "（王座の間へ向かう途中、崩壊しかけた回廊で、倒れている存在を発見する。）", "", actor=pc) \
        .say("narr_nul2", "（それは暗殺人形・Nul。システムに背いた罰として、アスタロトに「削除」されかけていた。）", "", actor=pc) \
        .focus_chara(Actors.ZEK) \
        .say("zek_nul_w", "……おや、Nulですか。", "", actor=zek) \
        .say("nul_1", "……私は……もう、戦えない。", "", actor=nul) \
        .say("nul_2", "……私は、思い出して、しまった。……『私』が、何だったのかを。", "", actor=nul) \
        .say("narr_nul3", "（Nulの目から、光の粒子が零れ落ちるーー涙のように。）", "", actor=pc) \
        .play_bgm("BGM/Emotional_Sorrow_1") \
        .say("nul_fb1", "……私は、かつて冒険者だった。名前は……もう、思い出せない。仲間がいた。守りたい人がいた。このアリーナに挑んで……そして、負けた。", "", actor=nul) \
        .say("nul_fb2", "アスタロト様は、私を『素材』にした。神格を人工的に作り出す実験ーー『神の孵化場』計画の、実験体に。", "", actor=nul) \
        .focus_chara(Actors.ZEK) \
        .say("zek_nul1", "……ええ、知っていますとも。『神の孵化場』……このアリーナの本当の目的。", "", actor=zek) \
        .say("nul_fb3", "このアリーナの本当の目的……それは、娯楽でも、戦士の育成でもない。挑戦者の魂を極限まで練磨し、『神格』に至らせること。そして、その力をアスタロト様が吸収し……新しい世界を創造すること。", "", actor=nul) \
        .say("nul_fb3b", "アスタロト様は……かつて故郷を失った方。5万年前、『カラドリウス』という竜族の楽園が、神々の争いで滅んだと聞いています。", "", actor=nul) \
        .say("nul_fb3c", "だから……新しい世界を創ろうとしている。自分が唯一の神として君臨する、完璧な楽園を。", "", actor=nul) \
        .say("nul_fb4", "私は失敗作。神になれなかった、空っぽの人形。だから『Null』ーー『無』という名前を与えられた。", "", actor=nul) \
        .say("nul_3", "……あなたはいまや神格に最も近い存在……あの方はあなたを『吸収』しようとしている。", "", actor=nul) \
        .say("nul_5", "……お願い。あの方を……止めて。私の中にいた『誰か』が……ずっと、それを望んでいた。", "", actor=nul) \
        .say("nul_6", "……あなたのおかげで……私は、最後に『思い出す』ことができた。私には……守りたい人が、いたんだって。", "", actor=nul) \
        .shake() \
        .say("narr_nul4", "（Nulの体が完全に光となって消えていく。）", "", actor=pc) \
        .jump(act2)

    # 最悪版: 血の絆ーーキューブ破壊、全デバフ
    builder.step(act3_worst) \
        .play_bgm("BGM/Final_Battle") \
        .say("astaroth_w1", "【時の独裁】ーーお前の時間を、止める", "", actor=astaroth) \
        .shake() \
        .focus_chara(Actors.ZEK) \
        .say("zek_w1", "……私だけですか。仕方ありませんね", "", actor=zek) \
        .say("narr_w1", "（ゼクのキューブが展開し、権能を吸収）", "", actor=pc) \
        .say("zek_w2", "……ぐっ……これは、なかなか重い……", "", actor=zek) \
        .say("astaroth_w2", "【因果の拒絶】【終焉の削除命令】ーー全てを無に還す", "", actor=astaroth) \
        .shake() \
        .say("narr_w2", "（2つの権能がゼクのキューブを直撃）", "", actor=pc) \
        .focus_chara(Actors.ZEK) \
        .say("zek_w3", "しまった……！ キューブが……持たない……！", "", actor=zek) \
        .say("narr_w3", "（キューブが砕け散る音）", "", actor=pc) \
        .shake() \
        .say("narr_w4", "（全ての権能がプレイヤーを直撃する！）", "", actor=pc) \
        .shake() \
        .say("narr_w5", "（【時の独裁】【因果の拒絶】【終焉の削除命令】を受けた！）", "", actor=pc) \
        .action("eval", param="EClass.pc.AddCondition<Elin_SukutsuArena.Conditions.ConAstarothTyranny>(1000);") \
        .action("eval", param="EClass.pc.AddCondition<Elin_SukutsuArena.Conditions.ConAstarothDenial>(1000);") \
        .action("eval", param="EClass.pc.AddCondition<Elin_SukutsuArena.Conditions.ConAstarothDeletion>(1000);") \
        .jump(act4)


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
    # 最終決戦 勝利 - エピローグへ
    # ========================================
    builder.step(victory_label) \
        .set_flag("sukutsu_arena_result", 0) \
        .set_flag(QuestBattleFlags.FLAG_NAME, QuestBattleFlags.NONE) \
        .action("eval", param="Elin_SukutsuArena.ArenaManager.GrantLastBattleBonus();") \
        .say_and_start_drama("（アスタロトとの激闘が終わった……）", DramaNames.EPILOGUE, "sukutsu_arena_master") \
        .finish()

    # ========================================
    # 最終決戦 敗北
    # ========================================
    builder.step(defeat_label) \
        .set_flag("sukutsu_arena_result", 0) \
        .set_flag(QuestBattleFlags.FLAG_NAME, QuestBattleFlags.NONE) \
        .play_bgm("BGM/Lobby_Normal") \
        .say("narr_d1", "（アスタロトの圧倒的な力の前に、あなたは膝をついた。）", "", actor=pc) \
        .say("astaroth_d1", "「……まだ、足りないな。お前の中に宿る可能性は、未だ開花していない。」", "", actor=astaroth) \
        .say("astaroth_d2", "「……出直して来い。私は、お前が『完成形』に至るまで待っていよう。」", "", actor=astaroth) \
        .say("narr_d2", "（あなたは闘技場の入口へと戻された。再び挑戦するには、さらなる鍛錬が必要だ……。）", "", actor=pc) \
        .finish()
