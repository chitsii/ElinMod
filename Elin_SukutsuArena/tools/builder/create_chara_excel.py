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
    '_idRenderData': '',
    'bio': 'm/1004/170/65/sly',
    'idText': 'sukutsu_shady_merchant',
    # CWL タグ: ゾーン生成、ランダム移動無効、商人在庫
    'tag': f'neutral,addZone_{ZONE_ID},addFlag_StayHomeZone,addStock',
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
    'tag': f'neutral,addZone_{ZONE_ID},addFlag_StayHomeZone,addDrama_drama_debug_battle,humanSpeak',
    'quality': 5,
    'chance': 0,
})

# ===== ストーリーバトル用敵キャラクター =====
# これらはアリーナゾーンには配置せず、バトル時に動的にスポーンさせる

# 6. 全盛期バルガス (Rank S昇格試験 / 若返った最強の戦士)
# lore: 68歳の現在はLv.85、全盛期（30代）はLv.120相当
# 「若返りの薬」使用条件は「真に命を賭けた戦いの場」でのみ
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
    # 敵キャラ: ゾーン配置なし、ランダム出現なし
    'tag': 'boss',
    'quality': 5,
    'chance': 0,
})

# 7. アスタロト (最終ボス / 竜神 / グランドマスターの真の姿)
# lore: イルヴァの神々と同格の竜神、Lv.100,000,000（システム上限）
# 滅びた次元「カラドリウス」の唯一の生存者、アリーナ創設者
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
    # 最終ボス: ゾーン配置なし
    'tag': 'boss,undead',
    'quality': 5,
    'chance': 0,
})

# 8. カインの亡霊 (Rank E昇格試験 / バルガスの元副官)
# lore: 生前Lv.60、残留思念としてLv.40相当だが、Tier1最終関門として強化
# 鉄血団元副団長、バルガスが息子のように愛した存在
npcs.append({
    'id': 'sukutsu_kain_ghost',
    'Author': 'tishi.elin.sukutsu_arena',
    'name_JP': '錆びついた英雄カイン',
    'name': 'Rusted Hero Cain',
    'aka_JP': '忘れられた副団長',
    'aka': 'Forgotten Vice-Captain',
    'race': 'ghost',
    'job': 'warrior',
    '_idRenderData': '@chara',
    'tiles': 458,  # ghost
    'LV': 90,  # Tier1最終: Lv.1-100
    'hostility': 'Enemy',
    'bio': 'm/1006/180/0/melancholic',
    'idText': 'sukutsu_kain_ghost',
    # 試練ボス: ゾーン配置なし
    'tag': 'boss,undead',
    'quality': 4,
    'chance': 0,
})

# 9. ヌル (Rank B昇格試験 / 暗殺人形 / 人造生命体)
# lore: 「神の孵化場」計画の失敗作、アリーナの「清掃係」
# 透明化して一撃で仕留める暗殺者
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
    # 試練ボス: ゾーン配置なし、暗殺者タイプ
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

# 11. ヴォイド・プチ (Rank G昇格試験 / 入門者の最初の試練)
# 混沌のブレスを吐く、混沌属性に免疫かつメタル999フィートを持つプチ
# 普通のプチとは異なり、非常に硬く混沌属性の攻撃を行う
# elements仕様:
#   - 959/20 = 混沌耐性20 (レベル4 = 免疫相当)
#   - 1218/999 = メタルフィート999 (全耐性大幅上昇、非常に硬い)
#   - 50210/10 = 混沌ブレス レベル10
npcs.append({
    'id': 'sukutsu_void_putty',
    'Author': 'tishi.elin.sukutsu_arena',
    'name_JP': 'ヴォイド・プチ',
    'name': 'Void Putty',
    'aka_JP': '虚無の粘体',
    'aka': 'Void Slime',
    'race': 'putit',
    'job': 'predator',
    '_idRenderData': '',
    'tiles': 269,  # putit
    'LV': 5,  # Tier1初期: Lv.1-10
    'hostility': 'Enemy',
    'bio': 'n/1009/50/30/',
    'idText': 'sukutsu_void_putty',
    # 特殊能力: 混沌耐性免疫(959/20)、メタルフィート(1218/999)、混沌ブレス(50210/10)
    'elements': '959/20,1218/999,50210/10',
    # 戦闘行動: 混沌ブレス
    'actCombat': 'breathe_Chaos',
    # 試練ボス: ゾーン配置なし
    'tag': 'boss',
    'quality': 2,
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
