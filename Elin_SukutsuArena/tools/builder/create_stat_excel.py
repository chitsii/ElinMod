"""
SourceStat.xlsx 生成スクリプト

カスタムConditionをゲームに登録するためのTSVファイルを生成する。
build.batでsofficeによりxlsxに変換される。
"""
import os

# パス設定
BUILDER_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.dirname(BUILDER_DIR)
PROJECT_ROOT = os.path.dirname(TOOLS_DIR)

OUTPUT_JP = os.path.join(PROJECT_ROOT, 'LangMod', 'JP', 'Stat.tsv')
OUTPUT_EN = os.path.join(PROJECT_ROOT, 'LangMod', 'EN', 'Stat.tsv')

# SourceStat のヘッダー列（SourceStat.cs より）
HEADERS = [
    'id', 'alias', 'name_JP', 'name', 'type', 'group', 'curse', 'duration',
    'hexPower', 'negate', 'defenseAttb', 'resistance', 'gainRes', 'elements',
    'nullify', 'tag', 'phase', 'colors', 'element', 'effect', 'strPhase_JP',
    'strPhase', 'textPhase_JP', 'textPhase', 'textEnd_JP', 'textEnd',
    'textPhase2_JP', 'textPhase2', 'gradient', 'invert', 'detail_JP', 'detail'
]

# 型情報（2行目）
TYPES = [
    'int', 'string', 'string', 'string', 'string', 'string', 'string', 'string',
    'int', 'string[]', 'string[]', 'string[]', 'int', 'string[]', 'string[]',
    'string[]', 'int[]', 'string', 'string', 'string[]', 'string[]', 'string[]',
    'string', 'string', 'string', 'string', 'string', 'string', 'string',
    'bool', 'string', 'string'
]

# デフォルト値（3行目）- idは記載している最大値より大きい必要がある
DEFAULTS = {
    'id': '100000',
    'group': 'Neutral',
    'duration': 'p/10',
    'hexPower': '10',
    'elements': '0,1,2,3,4,5,6,7,8,9',
    'gradient': 'condition',
}

# 耐性バフの共通設定
def make_resist_buff(id, alias, name_jp, name_en, element_alias, detail_jp, detail_en):
    """耐性バフConditionの定義を生成"""
    return {
        'id': str(id),
        'alias': alias,
        'name_JP': name_jp,
        'name': name_en,
        'type': 'BaseBuff',  # バニラのBaseBuffクラスを使用（GetPhase=>0でphase配列不要）
        'group': 'Buff',
        'duration': 'p/15+8',
        'phase': '',  # BaseBuffはGetPhase=>0なので不要
        'colors': 'buff',
        'elements': f'{element_alias},50',  # エレメントと値をカンマ区切りで指定
        'textEnd_JP': '#1は耐性の加護を得た。',
        'textEnd': '#1 gains resistance protection.',
        'textPhase2_JP': '#1の耐性の加護が消えた。',
        'textPhase2': "#1's resistance protection fades.",
        'invert': 'TRUE',
        'detail_JP': detail_jp,
        'detail': detail_en,
    }

# カスタムCondition定義
CONDITIONS = [
    # アスタロトの権能
    {
        'id': '10001',
        'alias': 'ConAstarothTyranny',
        'name_JP': '時の独裁',
        'name': 'Tyranny of Time',
        'type': 'Elin_SukutsuArena.Conditions.ConAstarothTyranny',
        'phase': '0,0,0,0,0,0,0,0,0,0',
        'detail_JP': 'アスタロトの権能により、速度が大幅に低下している。',
        'detail': "Your speed is drastically reduced by Astaroth's power.",
    },
    {
        'id': '10002',
        'alias': 'ConAstarothDenial',
        'name_JP': '因果の拒絶',
        'name': 'Denial of Causality',
        'type': 'Elin_SukutsuArena.Conditions.ConAstarothDenial',
        'phase': '0,0,0,0,0,0,0,0,0,0',
        'detail_JP': 'アスタロトの権能により、筋力が大幅に低下している。',
        'detail': "Your strength is drastically reduced by Astaroth's power.",
    },
    {
        'id': '10003',
        'alias': 'ConAstarothDeletion',
        'name_JP': '終焉の削除命令',
        'name': 'Deletion Command of the End',
        'type': 'Elin_SukutsuArena.Conditions.ConAstarothDeletion',
        'phase': '0,0,0,0,0,0,0,0,0,0',
        'detail_JP': 'アスタロトの権能により、魔力が消し去られている。MPが0になる。',
        'detail': "Your magical power is erased by Astaroth's power. MP is reduced to 0.",
    },
    # 個別の耐性バフ（バニラのConResEleパターン）
    make_resist_buff(10011, 'ConSukutsuResCold', '冷気耐性', 'Cold Resistance',
                     'resCold', '冷気への耐性が上昇している。', 'Resistance to cold is increased.'),
    make_resist_buff(10012, 'ConSukutsuResDarkness', '幻惑耐性', 'Darkness Resistance',
                     'resMind', '幻惑への耐性が上昇している。', 'Resistance to mind is increased.'),
    make_resist_buff(10013, 'ConSukutsuResChaos', '混沌耐性', 'Chaos Resistance',
                     'resChaos', '混沌への耐性が上昇している。', 'Resistance to chaos is increased.'),
    make_resist_buff(10014, 'ConSukutsuResSound', '轟音耐性', 'Sound Resistance',
                     'resSound', '轟音への耐性が上昇している。', 'Resistance to sound is increased.'),
    make_resist_buff(10015, 'ConSukutsuResImpact', '衝撃耐性', 'Impact Resistance',
                     'resImpact', '衝撃への耐性が上昇している。', 'Resistance to impact is increased.'),
    make_resist_buff(10016, 'ConSukutsuResCut', '出血耐性', 'Cut Resistance',
                     'resCut', '出血への耐性が上昇している。', 'Resistance to cut is increased.'),
    # PVバフ（痛覚遮断薬用）
    {
        'id': '10020',
        'alias': 'ConSukutsuPVBuff',
        'name_JP': 'PV強化',
        'name': 'PV Buff',
        'type': 'BaseBuff',  # バニラのBaseBuffクラスを使用
        'group': 'Buff',
        'duration': 'p/15+8',
        'phase': '',  # BaseBuffはGetPhase=>0なので不要
        'colors': 'buff',
        'elements': 'PV,30',  # PVを+30
        'textEnd_JP': '#1の防御力が上昇した。',
        'textEnd': "#1's defense is increased.",
        'textPhase2_JP': '#1の防御力が元に戻った。',
        'textPhase2': "#1's defense returns to normal.",
        'invert': 'TRUE',
        'detail_JP': '一時的にPVが上昇している。',
        'detail': 'PV is temporarily increased.',
    },
]


def create_tsv(output_path):
    """Stat.tsv を生成"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    lines = []

    # Row 1: ヘッダー
    lines.append('\t'.join(HEADERS))

    # Row 2: 型情報
    lines.append('\t'.join(TYPES))

    # Row 3: デフォルト値
    default_row = [DEFAULTS.get(h, '') for h in HEADERS]
    lines.append('\t'.join(default_row))

    # Row 4+: データ
    for condition in CONDITIONS:
        row = [str(condition.get(h, '')) for h in HEADERS]
        lines.append('\t'.join(row))

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f'Created: {output_path}')


def main():
    print('Generating Stat.tsv for custom Conditions...')
    create_tsv(OUTPUT_JP)
    create_tsv(OUTPUT_EN)
    print('Done!')


if __name__ == '__main__':
    main()
