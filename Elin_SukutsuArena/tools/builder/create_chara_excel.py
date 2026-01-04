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



for npc in npcs:
    rows.append(create_npc_row(npc))

def write_tsv(path, row_data):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(row_data)
    print(f'Created TSV: {path}')

write_tsv(OUTPUT_EN_TSV, rows)
write_tsv(OUTPUT_JP_TSV, rows)
