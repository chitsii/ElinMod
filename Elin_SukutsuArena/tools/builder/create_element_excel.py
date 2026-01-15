# -*- coding: utf-8 -*-
"""
create_element_excel.py - SourceElement.xlsx 自動生成

カスタムフィート（闘志など）をCWL形式のExcelファイルとして生成する。
"""
import os
import csv
import sys

# パス設定
BUILDER_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.dirname(BUILDER_DIR)
PROJECT_ROOT = os.path.dirname(TOOLS_DIR)

# 出力パス
OUTPUT_EN_TSV = os.path.join(PROJECT_ROOT, 'LangMod', 'EN', 'Element.tsv')
OUTPUT_JP_TSV = os.path.join(PROJECT_ROOT, 'LangMod', 'JP', 'Element.tsv')

# SourceElement カラム定義（ヘッダー行）
HEADERS = [
    'id',           # ユニークID (int, 10000以上でカスタム)
    'alias',        # エイリアス (string)
    'name_JP',      # 日本語名 (string)
    'name',         # 英語名 (string)
    'type',         # C#クラス名 (string)
    'group',        # グループ (string)
    'category',     # カテゴリ (string) - フィート一覧表示に必須
    'max',          # 最大レベル (int)
    'cost',         # 習得コスト (int)
    'tag',          # タグ (string[])
    'textPhase_JP', # フェーズテキストJP (string)
    'textPhase',    # フェーズテキストEN (string)
    'textExtra_JP', # 追加テキストJP (string)
    'textExtra',    # 追加テキストEN (string)
]

# 型情報（2行目）
TYPES = [
    'int',          # id
    'string',       # alias
    'string',       # name_JP
    'string',       # name
    'string',       # type
    'string',       # group
    'string',       # category
    'int',          # max
    'int',          # cost
    'string[]',     # tag
    'string',       # textPhase_JP
    'string',       # textPhase
    'string',       # textExtra_JP
    'string',       # textExtra
]

# デフォルト値（3行目）
DEFAULTS = [
    '',             # id
    '',             # alias
    '',             # name_JP
    '',             # name
    '',             # type
    'FEAT',         # group
    'feat',         # category - フィート一覧表示に必須
    '1',            # max
    '0',            # cost
    '',             # tag
    '',             # textPhase_JP
    '',             # textPhase
    '',             # textExtra_JP
    '',             # textExtra
]

# カスタムフィート定義
CUSTOM_FEATS = [
    {
        'id': 10001,
        'alias': 'featArenaSpirit',
        'name_JP': '闘志',
        'name': 'Arena Spirit',
        'type': 'FeatArenaSpirit',
        'group': 'FEAT',
        'category': 'feat',  # フィート一覧表示に必須
        'max': 7,
        'cost': 0,
        'tag': '',
        'textPhase_JP': '闘志',
        'textPhase': 'Arena Spirit',
        'textExtra_JP': '倒れても立ち上がる。それが闘士の本能だ。',
        'textExtra': 'Fall and rise again. That is the instinct of a fighter.',
    },
]


def main():
    print(f'Generating Element TSV from {len(CUSTOM_FEATS)} feat definition(s)...')

    rows = []

    # Row 1: ヘッダー
    rows.append(HEADERS)

    # Row 2: 型情報
    rows.append(TYPES)

    # Row 3: デフォルト値
    rows.append(DEFAULTS)

    # Row 4+: フィートデータ
    for feat in CUSTOM_FEATS:
        row = []
        for header in HEADERS:
            value = feat.get(header, '')
            row.append(value)
        rows.append(row)

    # TSV出力
    write_tsv(OUTPUT_EN_TSV, rows)
    write_tsv(OUTPUT_JP_TSV, rows)

    print(f"Generated {len(CUSTOM_FEATS)} feat(s)")
    print(f"  EN: {OUTPUT_EN_TSV}")
    print(f"  JP: {OUTPUT_JP_TSV}")


def write_tsv(path, row_data):
    """TSVファイル出力"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(row_data)
    print(f'  Created TSV: {path}')


if __name__ == '__main__':
    main()
