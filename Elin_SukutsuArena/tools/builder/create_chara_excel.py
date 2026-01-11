import openpyxl
import os
import csv

# パス設定
# パス設定
BUILDER_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.dirname(BUILDER_DIR)
PROJECT_ROOT = os.path.dirname(TOOLS_DIR)
SamplePath = r'c:\Users\tishi\programming\elin_modding\CWL_AddLocation_Example\LangMod\EN\SourceSSS.xlsx'
OUTPUT_EN_TSV = os.path.join(PROJECT_ROOT, 'LangMod', 'EN', 'Chara.tsv')
OUTPUT_JP_TSV = os.path.join(PROJECT_ROOT, 'LangMod', 'JP', 'Chara.tsv')

print(f'Reading sample file from: {SamplePath}')

sample_wb = openpyxl.load_workbook(SamplePath)
sample_ws = sample_wb['Chara']

# Row 1-3 (Header, Type, Default) Copy
header_map = {}
cols = sample_ws.max_column

rows = []
for r in range(1, 4):
    row_data = []
    for c in range(1, cols + 1):
        cell_val = sample_ws.cell(row=r, column=c).value
        # 1行目ならヘッダーマップ作成
        if r == 1:
            header_map[c-1] = cell_val
        row_data.append(cell_val if cell_val is not None else "")
    rows.append(row_data)

# 'Author' カラムが存在しない場合、強制的に追加
if 'Author' not in header_map.values():
    print("Adding missing 'Author' column...")
    new_col_idx = len(header_map)
    header_map[new_col_idx] = 'Author'

    # Header行に追加
    rows[0].append('Author')
    # Type行, Default行に追加 (空文字)
    rows[1].append('')
    rows[2].append('')

    # colsを更新
    cols += 1

# Helper
def create_npc_row(npc_def):
    row = [""] * cols  # 更新されたcolsを使用
    for k, v in npc_def.items():
        found = False
        for col_idx, col_name in header_map.items():
            if col_name == k:
                row[col_idx] = v
                found = True
                break
        if not found:
            # authorなどはここで処理済みのはずだが、もしヘッダーになければ警告
             print(f"WARNING: Field '{k}' not found in headers!")
    return row

npcs = []

# ===== NPC定義 =====
# bio format: 性別(m/f) / バージョン(固定ID) / 身長 / 体重 / 性格 | 髪色 | 肌色
# _idRenderData: @chara (PCCシステムを使用、Texture/ID.pngが自動ロードされる)
# tiles: バニラのフォールバックタイルID (カスタム画像が見つからない時に使用)
# idText: テキストID (同じIDのテキストファイルが参照される)
#
# CWL タグ仕様:
# - addZone_ゾーンID: 指定ゾーンにキャラクターを生成
# - addFlag_StayHomeZone: ランダム移動を無効化（初期ゾーンに留まる）
# - addDrama_テーブル名: ドラマシートをリンク
# - humanSpeak: 人間らしい会話表示（括弧なし）
# - addStock: 商人の在庫を追加

ZONE_ID = 'sukutsu_arena'  # カスタムゾーンID

# キャラクターレンダリング用デフォルト設定
# _idRenderData: 'chara' = バニラキャラスプライトシートを使用
# tiles: タイルID（バニラキャラのスプライト位置）

# 1. リリィ (サキュバス / 女性 / 受付嬢)
npcs.append({
    'id': 'sukutsu_receptionist',
    'Author': 'tishi.elin.sukutsu_arena',
    'name_JP': 'リリィ',
    'name': 'Lily',
    'aka_JP': '魅惑の受付嬢',
    'aka': 'Charming Receptionist',
    'race': 'succubus',
    'job': 'shopkeeper',
    '_idRenderData': '@chara',
    'tiles': 340,  # succubus female
    'LV': 50,
    'hostility': 'Friend',
    'bio': 'f/1001/165/52/sexy',
    'idText': 'sukutsu_receptionist',
    # CWL タグ: ゾーン生成、ランダム移動無効、商人在庫、人間らしい会話
    'tag': f'neutral,addZone_{ZONE_ID},addFlag_StayHomeZone,addStock,humanSpeak',
    'trait': 'Merchant',
    'quality': 4,
    'chance': 0,
})

# 2. バルガス (人間 / 男性 / アリーナマスター)
npcs.append({
    'id': 'sukutsu_arena_master',
    'Author': 'tishi.elin.sukutsu_arena',
    'name_JP': 'バルガス',
    'name': 'Vargus',
    'aka_JP': '百戦の覇者',
    'aka': 'Champion of Hundred Battles',
    'race': 'human',
    'job': 'warrior',
    '_idRenderData': '@chara',
    'tiles': 0,  # human male warrior
    'LV': 70,
    'hostility': 'Friend',
    'bio': 'm/1002/185/90/stern',
    'idText': 'sukutsu_arena_master',
    # CWL タグ: ゾーン生成、ランダム移動無効、ドラマリンク、人間らしい会話
    'tag': f'neutral,addZone_{ZONE_ID},addFlag_StayHomeZone,addDrama_drama_sukutsu_arena_master,humanSpeak',
    'quality': 4,
    'chance': 0,
})

# 3. グランドマスター (ドラゴン / 男性 / チャンピオン)
npcs.append({
    'id': 'sukutsu_grand_master',
    'Author': 'tishi.elin.sukutsu_arena',
    'name_JP': 'グランドマスター',
    'name': 'Grand Master',
    'aka_JP': '竜鱗の王者',
    'aka': 'Dragon Scale Champion',
    'race': 'dragon',
    'job': 'warrior',
    '_idRenderData': '@chara',
    'tiles': 168,  # dragon
    'LV': 100,
    'hostility': 'Friend',
    'bio': 'm/1003/210/150/proud',
    'idText': 'sukutsu_grand_master',
    # CWL タグ: ゾーン生成、ランダム移動無効
    'tag': f'neutral,addZone_{ZONE_ID},addFlag_StayHomeZone',
    'quality': 5,
    'chance': 0,
})

# 4. 怪しい商人 (ミュータント / 性別不明 / 商人)
npcs.append({
    'id': 'sukutsu_shady_merchant',
    'Author': 'tishi.elin.sukutsu_arena',
    'name_JP': '怪しい商人',
    'name': 'Shady Merchant',
    'aka_JP': '闇市の支配者',
    'aka': 'Lord of Black Market',
    'race': 'mutant',
    'job': 'merchant',
    'LV': 60,
    'hostility': 'Friend',
    'tiles': 807,
    '_idRenderData': '@chara',
    'bio': 'm/1004/170/65/sly',
    'idText': 'sukutsu_shady_merchant',
    # CWL タグ: ゾーン生成、ランダム移動無効、商人在庫、ドラマリンク、人間らしい会話
    'tag': f'neutral,addZone_{ZONE_ID},addFlag_StayHomeZone,addStock,addDrama_drama_sukutsu_shady_merchant,humanSpeak',
    'trait': 'Merchant',
    'quality': 4,
    'chance': 0,
})

# 5. デバッグマスター (開発テスト用 / 各バトルに直接アクセス可能)
npcs.append({
    'id': 'sukutsu_debug_master',
    'Author': 'tishi.elin.sukutsu_arena',
    'name_JP': '観測者',
    'name': 'Observer',
    'aka_JP': '次元の記録者',
    'aka': 'Dimensional Recorder',
    'race': 'spirit',
    'job': 'wizard',
    '_idRenderData': '@chara',
    'tiles': 478,  # spirit/wisp
    'LV': 999,
    'hostility': 'Friend',
    'bio': 'n/1005/160/0/mysterious',
    'idText': 'sukutsu_debug_master',
    # CWL タグ: ゾーン生成、ランダム移動無効、ドラマリンク、人間らしい会話
    'tag': f'neutral,addZone_{ZONE_ID},addFlag_StayHomeZone,addDrama_drama_debug_menu,humanSpeak',
    'quality': 5,
    'chance': 0,
})

# ===== ストーリーバトル用敵キャラクター =====
# これらはアリーナゾーンには配置せず、バトル時に動的にスポーンさせる

# 6. 虚空のウーズ (Rank G昇格試験 / 混沌ブレススライム群)
# lore: 次元の狭間で変異したスライム、混沌ブレスを吐く
npcs.append({
    'id': 'sukutsu_void_ooze',
    'Author': 'tishi.elin.sukutsu_arena',
    'name_JP': '虚空のウーズ',
    'name': 'Void Ooze',
    'aka_JP': '混沌の落とし子',
    'aka': 'Child of Chaos',
    'race': 'slime',
    'job': 'warrior',
    '_idRenderData': '@chara',
    'tiles': 296,  # slime
    'LV': 15,  # Tier1初戦: Lv.1-100
    'hostility': 'Enemy',
    'bio': 'n/2001/50/30/mindless',
    'idText': 'sukutsu_void_ooze',
    # 能力: 混沌ブレス、混沌免疫
    'mainElement': 'Chaos',
    'elements': 'resChaos/100',  # 混沌免疫（ブレス自爆防止）
    'actCombat': 'breathe_Chaos/30',  # 30%確率で混沌ブレス
    'tag': 'boss',
    'quality': 3,
    'chance': 0,
})

# 7. 霜牙の魔犬 (Rank F昇格試験 / 古代種・氷・透明魔犬)
# lore: 古代種の魔犬、氷ブレスと透明化で獲物を狩る
npcs.append({
    'id': 'sukutsu_frost_hound',
    'Author': 'tishi.elin.sukutsu_arena',
    'name_JP': '霜牙の魔犬',
    'name': 'Frostfang Hound',
    'aka_JP': '凍える牙',
    'aka': 'Freezing Fang',
    'race': 'hound',
    'job': 'warrior',
    '_idRenderData': '@chara',
    'tiles': 254,  # hound
    'LV': 45,  # Tier1中盤: Lv.1-100
    'hostility': 'Enemy',
    'bio': 'n/2002/120/80/predator',
    'idText': 'sukutsu_frost_hound',
    # 能力: 古代種、透明化、氷ブレス、鈍足魔法、氷免疫
    'mainElement': 'Cold',
    'elements': 'invisibility/1,featElder/1,resCold/100',  # 透明化、古代種、氷免疫
    'actCombat': 'breathe_Cold/40,SpSpeedDown/20',  # 氷ブレス40%、鈍足20%
    'tag': 'boss',
    'quality': 4,
    'chance': 0,
})

# 8. 訓練用バルガス (バルガス訓練クエスト / 手加減バージョン)
# lore: 「お前の足を一歩でも動かしてみせろ」
# 全力ではないが、それでも歴戦の覇者
npcs.append({
    'id': 'sukutsu_balgas_training',
    'Author': 'tishi.elin.sukutsu_arena',
    'name_JP': 'バルガス',
    'name': 'Balgas',
    'aka_JP': '百戦の覇者',
    'aka': 'Champion of Hundred Battles',
    'race': 'human',
    'job': 'warrior',
    '_idRenderData': '@chara',
    'tiles': 0,  # human male warrior
    'LV': 200,  # 手加減バージョン
    'hostility': 'Enemy',
    'bio': 'm/1002/185/90/stern',
    'idText': 'sukutsu_balgas_training',
    # 能力: 物理特化（手加減）
    'mainElement': 'Cut',
    'elements': 'featElder/1,resCut/60,resImpact/60',
    'actCombat': 'breathe_Cut/30,breathe_Impact/20',
    'tag': 'boss',
    'quality': 4,
    'chance': 0,
})

# 9. 全盛期バルガス (Rank S昇格試験 / 若返った最強の戦士)
# lore: 68歳の現在はLv.85、全盛期（30代）はLv.120相当
# 「若返りの薬」使用条件は「真に命を賭けた戦いの場」でのみ
# 純粋な「武の極致」。魔法もブレスも使わず、剣と体術のみで全てを圧倒する
npcs.append({
    'id': 'sukutsu_balgas_prime',
    'Author': 'tishi.elin.sukutsu_arena',
    'name_JP': '全盛期のバルガス',
    'name': 'Balgas at His Prime',
    'aka_JP': '鉄血の覇者',
    'aka': 'Iron-Blooded Champion',
    'race': 'human',
    'job': 'warrior',
    '_idRenderData': '@chara',
    'tiles': 0,  # human male warrior
    'LV': 8000,  # Tier3: Lv.1,000-10,000
    'hostility': 'Enemy',
    'bio': 'm/1002/188/95/stern',
    'idText': 'sukutsu_balgas_prime',
    # 能力: 物理特化、8部位連撃、高物理耐性
    'mainElement': 'Cut',
    'elements': 'featElder/1,featBodyParts/8,resCut/80,resImpact/80,resFire/40,resCold/40,resLightning/40,resMind/60,resNerve/60',
    'actCombat': 'breathe_Cut/45,breathe_Impact/35,SpHero/10',
    'tag': 'boss',
    'quality': 5,
    'chance': 0,
})

# 7. アスタロト (最終ボス / 竜神 / グランドマスターの真の姿)
# lore: イルヴァの神々と同格の竜神、Lv.100,000,000（システム上限）
# 滅びた次元「カラドリウス」の唯一の生存者、アリーナ創設者
# 3,000年間、観客の「注目」を力に変換してきた
npcs.append({
    'id': 'sukutsu_astaroth',
    'Author': 'tishi.elin.sukutsu_arena',
    'name_JP': 'アスタロト',
    'name': 'Astaroth',
    'aka_JP': '虚空の竜神',
    'aka': 'Dragon God of the Void',
    'race': 'dragon',
    'job': 'warrior',
    '_idRenderData': '@chara',
    'tiles': 168,  # dragon
    'LV': 50000,  # エンドコンテンツ: 次元深度
    'hostility': 'Enemy',
    'bio': 'm/1003/350/500/proud',
    'idText': 'sukutsu_astaroth',
    # 能力: 全属性攻撃、12部位、ほぼ全属性耐性（聖のみ弱点）
    'mainElement': 'Void',
    'elements': 'featElder/1,featBodyParts/12,resVoid/100,resChaos/80,resNether/80,resMagic/80,resDarkness/80,resFire/60,resCold/60,resLightning/60,resPoison/60,resAcid/60,resSound/60,resNerve/80,resMind/80,resHoly/40,resCut/50,resImpact/50',
    'actCombat': 'breathe_Void/40,breathe_Chaos/30,breathe_Nether/25,hand_Magic/35,SpGravity/15,SpBane/10',
    'tag': 'boss,undead',
    'quality': 5,
    'chance': 0,
})

# 10. カインの亡霊 (Rank E昇格試験 / バルガスの元副官)
# lore: 次元の狭間で変異したカオスシェイプ
# 記憶を失い、戦闘本能だけが残った異形の存在
npcs.append({
    'id': 'sukutsu_kain_ghost',
    'Author': 'tishi.elin.sukutsu_arena',
    'name_JP': '錆びついた英雄カイン',
    'name': 'Rusted Hero Cain',
    'aka_JP': '忘れられた副団長',
    'aka': 'Forgotten Vice-Captain',
    'race': 'chaos',  # ghost から chaos に変更
    'job': 'warrior',
    '_idRenderData': '@chara',
    'tiles': 458,  # ghost (fallback)
    'LV': 90,  # Tier1最終: Lv.1-100
    'hostility': 'Enemy',
    'bio': 'm/1006/180/0/melancholic',
    'idText': 'sukutsu_kain_ghost',
    # 能力: 多属性攻撃、追加部位
    'elements': 'featBodyParts/5',  # 手の部位追加
    'actCombat': 'breathe_Acid/25,breathe_Cut/25,hand_Nether/30',  # 酸25%、出血25%、地獄30%
    'tag': 'boss,undead',
    'quality': 4,
    'chance': 0,
})

# 9. ヌル (Rank B昇格試験 / 暗殺人形 / 人造生命体)
# lore: 「神の孵化場」計画の失敗作、アリーナの「清掃係」
# 透明化 + 分裂能力で数で圧倒する暗殺者
npcs.append({
    'id': 'sukutsu_null',
    'Author': 'tishi.elin.sukutsu_arena',
    'name_JP': 'Nul',
    'name': 'Null',
    'aka_JP': '虚無の処刑人',
    'aka': 'Void Executioner',
    'race': 'machine',
    'job': 'thief',
    '_idRenderData': '@chara',
    'tiles': 536,  # machine/robot
    'LV': 800,  # Tier2最終: Lv.100-1,000
    'hostility': 'Enemy',
    'bio': 'f/1007/165/45/emotionless',
    'idText': 'sukutsu_null',
    # 能力: 透明化、分裂、虚無攻撃、沈黙
    'mainElement': 'Void',
    'elements': 'invisibility/1,featSplit/1,featElder/1,resVoid/80,resNether/60,resMagic/40,resNerve/100,resMind/100',
    'actCombat': 'hand_Void/45,SpInvisibility/25,SpSilence/15',
    'tag': 'boss',
    'quality': 4,
    'chance': 0,
})

# 10. 影のドッペルゲンガー (Rank A昇格試験 / プレイヤーの影)
# lore: 観客の「注目」がプレイヤーの影から生み出した存在
# プレイヤーの全てを知り、全てを模倣する
# Note: 影の自己はC#コードでPCの外見をコピーするため、tilesは仮の値
npcs.append({
    'id': 'sukutsu_shadow_self',
    'Author': 'tishi.elin.sukutsu_arena',
    'name_JP': '影の自己',
    'name': 'Shadow Self',
    'aka_JP': '映し身',
    'aka': 'Mirror Image',
    'race': 'shade',
    'job': 'warrior',
    '_idRenderData': '@chara',
    'tiles': 460,  # shade (fallback, C# will copy PC appearance)
    'LV': 2500,  # Tier3前半: Lv.1,000-10,000
    'hostility': 'Enemy',
    'bio': 'n/1008/170/60/sinister',
    'idText': 'sukutsu_shadow_self',
    # 試練ボス: プレイヤーの影
    'tag': 'boss,undead',
    'quality': 4,
    'chance': 0,
})

# 11. グリード (Rank D昇格試験 / 観客の代弁者)
# lore: かつてCランク「闘技場の鴉」の一員だった剣士
# 観客の「注目」に魅せられ、自ら観客の力を体に取り込もうとした
# 結果、肉体は半ば「観客」に乗っ取られ、今は観客の意志を代弁する傀儡
npcs.append({
    'id': 'sukutsu_greed',
    'Author': 'tishi.elin.sukutsu_arena',
    'name_JP': 'グリード',
    'name': 'Greed',
    'aka_JP': '観客の代弁者',
    'aka': 'Voice of the Audience',
    'race': 'human',
    'job': 'warrior',
    '_idRenderData': '@chara',
    'tiles': 0,  # human male warrior
    'LV': 150,  # Tier2入口: Lv.100-1,000
    'hostility': 'Enemy',
    'bio': 'm/2003/175/70/possessed',
    'idText': 'sukutsu_greed',
    # 能力: 轟音+混沌ブレス、弱体魔法
    'mainElement': 'Sound',
    'elements': 'resSound/50,resChaos/30,resMagic/60,featElder/1',
    'actCombat': 'breathe_Sound/35,breathe_Chaos/25,SpWeakness/15',
    # AI: シルバーベルのように逃げ回り、黒天使のように罵倒する
    'AI_Calm': '4,30',
    'AI_Combat': 'ActInsult,ActEscape/5',
    'tag': 'boss',
    'quality': 4,
    'chance': 0,
})

# ===== Cランク: 闘技場の鴉（3体ボス）=====
# lore: かつてSランク「屠竜者」を目指した3人の挑戦者
# Bランク以上に進めず、今は番人として闘技場に縛られている

# 12. クロウ（影）- 元盗賊ギルドのエース
npcs.append({
    'id': 'sukutsu_crow_shadow',
    'Author': 'tishi.elin.sukutsu_arena',
    'name_JP': 'クロウ',
    'name': 'Crow',
    'aka_JP': '影の鴉',
    'aka': 'Crow of Shadows',
    'race': 'human',
    'job': 'thief',
    '_idRenderData': '@chara',
    'tiles': 2,  # human male thief
    'LV': 350,  # Tier2中盤
    'hostility': 'Enemy',
    'bio': 'm/2004/170/60/silent',
    'idText': 'sukutsu_crow_shadow',
    # 能力: 透明化、闇属性攻撃、地獄攻撃
    'mainElement': 'Darkness',
    'elements': 'invisibility/1,resDarkness/60,resNether/40',
    'actCombat': 'hand_Darkness/40,SpInvisibility/20,hand_Nether/30',
    'tag': 'boss',
    'quality': 4,
    'chance': 0,
})

# 13. レイヴン（刃）- 元戦士ギルドのチャンピオン
npcs.append({
    'id': 'sukutsu_raven_blade',
    'Author': 'tishi.elin.sukutsu_arena',
    'name_JP': 'レイヴン',
    'name': 'Raven',
    'aka_JP': '刃の鴉',
    'aka': 'Raven of Blades',
    'race': 'human',
    'job': 'warrior',
    '_idRenderData': '@chara',
    'tiles': 0,  # human male warrior
    'LV': 400,  # Tier2中盤
    'hostility': 'Enemy',
    'bio': 'm/2005/185/90/fierce',
    'idText': 'sukutsu_raven_blade',
    # 能力: 物理特化、追加部位、斬撃/衝撃ブレス
    'mainElement': 'Cut',
    'elements': 'featElder/1,resCut/50,resImpact/40,featBodyParts/2',
    'actCombat': 'breathe_Cut/40,breathe_Impact/30',
    'tag': 'boss',
    'quality': 4,
    'chance': 0,
})

# 14. カラス（毒）- 元錬金術師
npcs.append({
    'id': 'sukutsu_karasu_venom',
    'Author': 'tishi.elin.sukutsu_arena',
    'name_JP': 'カラス',
    'name': 'Karasu',
    'aka_JP': '毒の鴉',
    'aka': 'Crow of Venom',
    'race': 'mutant',
    'job': 'wizard',
    '_idRenderData': '@chara',
    'tiles': 807,  # mutant
    'LV': 450,  # Tier2中盤
    'hostility': 'Enemy',
    'bio': 'f/2006/160/50/cunning',
    'idText': 'sukutsu_karasu_venom',
    # 能力: 毒/酸ブレス、元素の傷跡
    'mainElement': 'Poison',
    'elements': 'resPoison/100,resAcid/60',
    'actCombat': 'breathe_Poison/50,breathe_Acid/30,SpWeakResEle/15',
    'tag': 'boss',
    'quality': 4,
    'chance': 0,
})


for npc in npcs:
    rows.append(create_npc_row(npc))

def write_tsv(path, row_data):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(row_data)
    print(f'Created TSV: {path}')

write_tsv(OUTPUT_EN_TSV, rows)
write_tsv(OUTPUT_JP_TSV, rows)
