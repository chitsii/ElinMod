"""
オープニングドラマ「虚無の呼び声」生成スクリプト
scenarios.py の定義を使用してExcelを生成する。
"""

import os
import sys

# toolsディレクトリをパスに追加してモジュールをインポート可能にする
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(TOOLS_DIR)

from drama_builder import DramaBuilder
from scenarios import define_opening_drama

PROJECT_ROOT = os.path.dirname(TOOLS_DIR)
OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'LangMod', 'JP', 'Dialog', 'Drama', 'drama_sukutsu_opening.xlsx')

def main():
    builder = DramaBuilder()
    define_opening_drama(builder)

    # シート名は任意だが、ユニークなものが安全
    builder.save(OUTPUT_PATH, sheet_name="opening")

if __name__ == "__main__":
    main()
