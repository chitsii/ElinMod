"""
SourceSukutsu.xlsx 生成スクリプト (StrangeSpellShop準拠版)
CWL用のZoneデータをExcelファイルとして生成する。
"""
from openpyxl import Workbook
import os

def create_source_xlsx():
    wb = Workbook()

    # デフォルトシートを「Zone」にリネーム
    ws = wb.active
    ws.title = "Zone"

    # ヘッダー行 (Row 0 in 0-indexed, Row 1 in Excel)
    # StrangeSpellShopの構造を完全に踏襲
    headers = [
        "id", "parent", "name_JP", "name", "type", "LV", "chance", "faction",
        "value", "idProfile", "idFile", "idBiome", "idGen", "idPlaylist", "tag",
        "cost", "dev", "image", "pos", "questTag", "textFlavor_JP", "textFlavor",
        "detail_JP", "detail"
    ]

    # 型定義行 (Row 1 in 0-indexed, Row 2 in Excel)
    types = [
        "string", "string", "string", "string", "string", "int", "int", "string",
        "int", "string", "string[]", "string", "string", "string", "string[]",
        "int", "int", "string", "int[]", "string[]", "string", "string",
        "string", "string"
    ]

    # デフォルト値行 (Row 2 in 0-indexed, Row 3 in Excel)
    # 多くのフィールドは空で、typeのみ"Zone"、LV=1、chance=100、dev=0など
    defaults = [
        None, None, None, None, "Zone", 1, 100, None,
        None, None, None, "Plain", None, None, None,
        None, 0, "default", None, None, None, None,
        None, None
    ]

    # データ行 (Row 3 in 0-indexed, Row 4 in Excel)
    # 巣窟アリーナの定義
    zone_data = [
        "sukutsu_arena",           # id
        "ntyris",                  # parent (ニティリス地方に配置)
        "巣窟アリーナ",              # name_JP
        "Sukutsu Arena",           # name
        "Zone_SukutsuArena",       # type (カスタムゾーンクラス名。名前空間なしでOKかも)
        "50",                      # LV (文字列として)
        "100",                     # chance (文字列として)
        None,                      # faction
        "100",                     # value (文字列として)
        None,                      # idProfile
        "sukutsu_arena",           # idFile (マップファイル名。Maps/sukutsu_arena.zに対応)
        "Plain",                   # idBiome
        None,                      # idGen
        None,                      # idPlaylist
        "unique,global",           # tag (カンマ区切り文字列)
        "0",                       # cost
        "0",                       # dev
        "default",                 # image (マップアイコン?)
        "34,-24,0",                # pos (X,Y,MapIndex。パルミア(34,-25)の南)
        None,                      # questTag
        "熱狂と興奮が渦巻く、地下闘技場への入り口。",  # textFlavor_JP
        "The entrance to the underground arena.",    # textFlavor
        "アリーナへの入り口",         # detail_JP
        "Entrance to the arena"    # detail
    ]

    # Excelに書き込み
    ws.append(headers)
    ws.append(types)
    ws.append(defaults)
    ws.append(zone_data)

    # 出力先ディレクトリ
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    # JP と EN 両方に出力
    for lang in ["JP", "EN"]:
        output_dir = os.path.join(project_root, "LangMod", lang)
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "SourceSukutsu.xlsx")
        wb.save(output_path)
        print(f"Generated: {output_path}")

if __name__ == "__main__":
    create_source_xlsx()
