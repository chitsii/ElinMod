"""
アリーナマスター用ドラマスクリプト生成 (Refactored)
scenarios.py の定義を使用してExcelを生成する。
"""

import os
import sys

# toolsディレクトリをパスに追加してモジュールをインポート可能にする
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(TOOLS_DIR)

from drama_builder import DramaBuilder
from scenarios import define_arena_master_drama

PROJECT_ROOT = os.path.dirname(TOOLS_DIR)
OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'LangMod', 'JP', 'Dialog', 'Drama', 'drama_sukutsu_arena_master.xlsx')

def main():
    builder = DramaBuilder()

    # シナリオ定義を適用
    define_arena_master_drama(builder)

    # CWLドラマファイルを保存
    # シート名は任意だが、TinyMitaではキャラクターIDを使用している
    builder.save(OUTPUT_PATH, sheet_name="sukutsu_arena_master")

if __name__ == "__main__":
    main()
