"""
DramaBuilder - CWL ドラマファイル生成用ビルダークラス

CWL (Custom Whatever Loader) のドラマファイル形式に準拠した
Excel ファイルを生成するためのビルダーパターン実装。

フォーマット仕様は docs/cwl_drama_format.md を参照。
"""

import openpyxl
import os
from typing import Optional, List, Union, Dict, Any, Set

# CWL準拠ヘッダー (if2なし、version/text列あり)
HEADERS = ['step', 'jump', 'if', 'action', 'param', 'actor', 'version', 'id', 'text_JP', 'text_EN', 'text']


class DramaLabel:
    """ステップラベルを表すクラス"""
    def __init__(self, key: str):
        self.key = key
    def __str__(self):
        return self.key


class DramaActor:
    """アクターを表すクラス"""
    def __init__(self, key: str):
        self.key = key
    def __str__(self):
        return self.key


class DramaBuilder:
    """
    CWLドラマファイルを構築するビルダークラス。

    使用例:
        drama = DramaBuilder()
        pc = drama.register_actor("pc", "プレイヤー", "Player")
        npc = drama.register_actor("master", "マスター", "Master")

        lbl_main = drama.label("main")
        drama.step(lbl_main)
        drama.say("greet", "こんにちは", actor=npc)
        drama.finish()

        drama.save("drama.xlsx", sheet_name="master")
    """

    def __init__(self) -> None:
        self.entries: List[Dict[str, Any]] = []
        self.actors: Dict[str, Dict[str, str]] = {}
        self.registered_steps: Set[str] = set()
        self._current_step: Optional[str] = None

    def _resolve_key(self, obj: Union[str, DramaLabel, DramaActor]) -> str:
        """オブジェクトからキーを取得"""
        if isinstance(obj, (DramaLabel, DramaActor)):
            return obj.key
        return obj

    def register_actor(self, actor_id: str, name_jp: str, name_en: str = "") -> DramaActor:
        """アクターを登録"""
        self.actors[actor_id] = {'jp': name_jp, 'en': name_en or name_jp}
        return DramaActor(actor_id)

    def label(self, key: str) -> DramaLabel:
        """ラベルを作成"""
        return DramaLabel(key)

    def step(self, step_label: Union[str, DramaLabel]) -> 'DramaBuilder':
        """
        新しいステップを開始。
        CWL形式では、step行は step列のみを含み、内容は次の行から。
        """
        key = self._resolve_key(step_label)
        self.registered_steps.add(key)
        self._current_step = key
        # step行を追加（step列のみ）
        self.entries.append({'step': key})
        return self

    def say(self, text_id: str, text_jp: str, text_en: str = "",
            actor: Union[str, DramaActor] = None) -> 'DramaBuilder':
        """テキスト行を追加"""
        actor_key = self._resolve_key(actor) if actor else None
        entry = {
            'id': text_id,
            'text_JP': text_jp,
            'text_EN': text_en or text_jp,
        }
        if actor_key:
            entry['actor'] = actor_key
        self.entries.append(entry)
        return self

    def choice(self, jump_to: Union[str, DramaLabel], text_jp: str,
               text_en: str = "", text_id: str = "") -> 'DramaBuilder':
        """選択肢を追加"""
        key = self._resolve_key(jump_to)
        entry = {
            'action': 'choice',
            'jump': key,
            'text_JP': text_jp,
            'text_EN': text_en or text_jp,
        }
        if text_id:
            entry['id'] = text_id
        self.entries.append(entry)
        return self

    def jump(self, jump_to: Union[str, DramaLabel]) -> 'DramaBuilder':
        """指定ステップにジャンプ"""
        key = self._resolve_key(jump_to)
        self.entries.append({'jump': key})
        return self

    def branch_if(self, flag: str, operator: str, value: int,
                  jump_to: Union[str, DramaLabel],
                  actor: Union[str, DramaActor] = None) -> 'DramaBuilder':
        """
        条件分岐。invoke* + if_flag を使用。
        """
        key = self._resolve_key(jump_to)
        actor_key = self._resolve_key(actor) if actor else 'pc'
        entry = {
            'action': 'invoke*',
            'param': f'if_flag({flag}, {operator}{value})',
            'jump': key,
            'actor': actor_key,
        }
        self.entries.append(entry)
        return self

    def set_flag(self, flag: str, value: int = 1) -> 'DramaBuilder':
        """フラグを設定"""
        self.entries.append({
            'action': 'setFlag',
            'param': f'{flag},{value}',
        })
        return self

    def mod_flag(self, flag: str, operator: str, value: int,
                 actor: Union[str, DramaActor] = None) -> 'DramaBuilder':
        """フラグを変更 (invoke* mod_flag)"""
        actor_key = self._resolve_key(actor) if actor else 'pc'
        self.entries.append({
            'action': 'invoke*',
            'param': f'mod_flag({flag}, {operator}{value})',
            'actor': actor_key,
        })
        return self

    def action(self, action_name: str, param: str = None,
               jump: Union[str, DramaLabel] = None,
               actor: Union[str, DramaActor] = None) -> 'DramaBuilder':
        """汎用アクションを追加"""
        entry = {'action': action_name}
        if param:
            entry['param'] = param
        if jump:
            entry['jump'] = self._resolve_key(jump)
        if actor:
            entry['actor'] = self._resolve_key(actor)
        self.entries.append(entry)
        return self

    def on_cancel(self, jump_to: Union[str, DramaLabel]) -> 'DramaBuilder':
        """キャンセル時の動作を設定"""
        key = self._resolve_key(jump_to)
        self.entries.append({'action': 'cancel', 'jump': key})
        return self

    def finish(self) -> 'DramaBuilder':
        """ドラマを終了"""
        self.entries.append({'action': 'end'})
        return self

    def play_sound(self, sound_id: str) -> 'DramaBuilder':
        """効果音を再生"""
        self.entries.append({'action': 'sound', 'param': sound_id})
        return self

    def play_bgm(self, bgm_id: str) -> 'DramaBuilder':
        """BGMを再生"""
        self.entries.append({'action': 'bgm', 'param': bgm_id})
        return self

    def wait(self, seconds: float) -> 'DramaBuilder':
        """待機"""
        self.entries.append({'action': 'wait', 'param': str(seconds)})
        return self

    def effect(self, effect_id: str) -> 'DramaBuilder':
        """エフェクトを再生"""
        self.entries.append({'action': effect_id})
        return self

    def build(self) -> List[Dict[str, Any]]:
        """エントリーリストを返す（検証なし）"""
        return self.entries

    def save(self, filepath: str, sheet_name: str = "main") -> None:
        """
        CWL準拠のExcelファイルとして保存。

        Args:
            filepath: 出力ファイルパス
            sheet_name: シート名（キャラクターIDなどを推奨）
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = sheet_name

        # Row 1: Headers
        for col, header in enumerate(HEADERS, 1):
            ws.cell(row=1, column=col, value=header)

        # Row 2-5: 空行（CWL形式に準拠）

        # Row 6+: Data
        row = 6
        for entry in self.entries:
            for col, header in enumerate(HEADERS, 1):
                value = entry.get(header)
                if value is not None:
                    ws.cell(row=row, column=col, value=value)
            row += 1

        wb.save(filepath)
        print(f"Created: {filepath} (sheet: {sheet_name})")
