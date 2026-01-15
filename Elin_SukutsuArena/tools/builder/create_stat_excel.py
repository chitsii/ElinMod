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
# 注意: elementsはデフォルト値を設定しない（カスタムConditionで問題が発生するため）
DEFAULTS = {
    'id': '100000',
    'group': 'Neutral',
    'duration': 'p/10',
    'hexPower': '10',
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
        'duration': '3000',  # 固定3000ターン
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
    # アスタロトの権能（elementsはExcel側で設定）
    {
        'id': '10001',
        'alias': 'ConAstarothTyranny',
        'name_JP': '時の独裁',
        'name': 'Tyranny of Time',
        'type': 'Elin_SukutsuArena.Conditions.ConAstarothTyranny',
        'phase': '0,0,0,0,0,0,0,0,0,0',
        'elements': 'SPD,-1000',  # 速度大幅低下
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
        'elements': 'STR,-1000',  # 筋力大幅低下
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
        'elements': 'MAG,-1000',  # 魔力大幅低下
        'detail_JP': 'アスタロトの権能により、魔力が消し去られている。',
        'detail': "Your magical power is erased by Astaroth's power.",
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
        'duration': '3000',  # 固定3000ターン
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
    # ブースト効果（禁断の覚醒剤用メリット）
    {
        'id': '10021',
        'alias': 'ConSukutsuBoost',
        'name_JP': '覚醒',
        'name': 'Awakening',
        'type': 'Elin_SukutsuArena.Conditions.ConSukutsuBoost',
        'group': 'Buff',
        'duration': '3000',  # 固定3000ターン
        'phase': '0,0,0,0,0,0,0,0,0,0',
        'colors': 'buff',
        'elements': 'STR,30,END,30,DEX,30,SPD,50',  # 複数能力上昇
        'textEnd_JP': '#1は力に目覚めた！',
        'textEnd': '#1 awakens to power!',
        'textPhase2_JP': '#1の覚醒が終わった。',
        'textPhase2': "#1's awakening ends.",
        'invert': 'TRUE',
        'detail_JP': '身体能力が一時的に大幅上昇している。副作用に注意。',
        'detail': 'Physical abilities are temporarily enhanced. Beware of side effects.',
    },
    # 出血効果（禁断の覚醒剤用デメリット）- elementsなし（Tickでダメージ処理）
    {
        'id': '10022',
        'alias': 'ConSukutsuBleed',
        'name_JP': '内出血',
        'name': 'Internal Bleeding',
        'type': 'Elin_SukutsuArena.Conditions.ConSukutsuBleed',
        'group': 'Bad',
        'duration': '3000',  # 固定3000ターン
        'phase': '0,0,0,0,0,0,0,0,0,0',
        'colors': 'debuff',
        'elements': '',  # elementsなし（Tickでダメージ処理）
        'textEnd_JP': '#1は内出血を起こした。',
        'textEnd': '#1 suffers internal bleeding.',
        'textPhase2_JP': '#1の内出血が止まった。',
        'textPhase2': "#1's internal bleeding stops.",
        'detail_JP': '覚醒剤の副作用で内出血している。毎ターンダメージを受ける。',
        'detail': 'Internal bleeding from stimulant side effects. Takes damage every turn.',
    },
    # 毒効果（痛覚遮断薬用デメリット）
    {
        'id': '10023',
        'alias': 'ConSukutsuPoison',
        'name_JP': '薬物中毒',
        'name': 'Drug Poisoning',
        'type': 'Elin_SukutsuArena.Conditions.ConSukutsuPoison',
        'group': 'Bad',
        'duration': '3000',  # 固定3000ターン
        'phase': '0,0,0,0,0,0,0,0,0,0',
        'colors': 'debuff',
        'elements': 'END,-10',  # 耐久低下
        'textEnd_JP': '#1は薬物中毒を起こした。',
        'textEnd': '#1 suffers from drug poisoning.',
        'textPhase2_JP': '#1の薬物中毒が治った。',
        'textPhase2': "#1 recovers from drug poisoning.",
        'detail_JP': '痛覚遮断薬の副作用で中毒状態。自然回復が阻害される。',
        'detail': 'Poisoned by painkiller side effects. Natural regeneration is blocked.',
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
