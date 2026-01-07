# クエストシステム設計書

## 概要

このドキュメントは、宿敵アリーナModのクエスト進行システムについて説明します。

## クエスト依存関係管理システム

### 主要コンポーネント

#### 1. `quest_dependencies.py`
クエストの依存関係を定義・管理するモジュール。

**主要クラス:**
- `QuestDefinition`: クエストの定義（ID、種類、前提条件、完了フラグなど）
- `FlagCondition`: フラグ条件（フラグキー、演算子、値）
- `QuestDependencyGraph`: クエスト依存関係グラフ（利用可能クエストの判定、依存関係の検証など）

### クエストタイプ

```python
class QuestType(Enum):
    MAIN_STORY = "main_story"          # メインストーリー
    RANK_UP = "rank_up"                # ランク昇格試験
    SIDE_QUEST = "side_quest"          # サイドクエスト
    CHARACTER_EVENT = "character_event" # キャラクターイベント
    ENDING = "ending"                   # エンディング
```

### クエスト進行フロー

```
01_opening (初回到着)
    ↓
02_rank_up_G (ランクG昇格)
    ↓
03_zek_intro (ゼクとの出会い) [サイド]
    ↓
04_rank_up_F (ランクF昇格)
    ↓
05_1_lily_experiment (リリィの依頼) [サイド]
    ↓
05_2_zek_steal_bottle (瓶すり替え提案) [重要分岐]
    ↓
06_1_rank_up_E (ランクE昇格)
    ↓
06_2_zek_steal_soulgem (カインの魂選択) [重要分岐] → ランクD昇格
    ↓
07_upper_existence (観客の存在)
    ↓
08_lily_private (リリィの私室) [条件: rel.lily >= 40]
    ↓
09_rank_up_C (ランクC昇格・バルガス修行)
    ↓
11_rank_up_B (ランクB昇格・ヌル戦)
    ↓
12_makuma (ヌルの真実、リリィの衣装)
    ↓
13_makuma2 (虚空の心臓製作・清算) [過去の選択が影響]
    ↓
14_rank_up_A (ランクA昇格・影との戦い)
    ↓
15_rank_up_S (ランクS昇格・バルガス戦) [重要分岐: balgas_choice]
    ↓
16_lily_real_name (リリィの真名) [条件: balgas_choice=spared, rel.lily>=50]
    ↓
17_vs_grandmaster_1 (アスタロト初遭遇)
    ↓
18_last_battle (最終決戦) [エンディング分岐: ending]
```

## 重要な分岐ポイント

### 1. 瓶すり替え (05_2_zek_steal_bottle)

**選択肢:**
- `bottle_choice = "refused"`: リリィとの信頼維持
- `bottle_choice = "swapped"`: ゼクとの関係強化、後で発覚

**影響:**
- `13_makuma2` で瓶が暴走 (swapped の場合)
- 告白の選択で `lily_bottle_confession` が設定される:
  - `"confessed"`: 好感度20、信頼再構築フラグ、scenario/16で和解イベント
  - `"blamed_zek"`: 好感度50維持、scenario/16ブロック
  - `"denied"`: 好感度0、敵対フラグ、scenario/16ブロック

### 2. カインの魂 (06_2_zek_steal_soulgem)

**選択肢:**
- `kain_soul_choice = "returned"`: バルガスとの信頼強化
- `kain_soul_choice = "sold"`: ゼクとの関係強化、後で発覚

**影響:**
- `13_makuma2` でバルガスが問い詰める (sold の場合)
- 告白の選択で `kain_soul_confession` が設定される:
  - `"confessed"`: バルガス好感度0、信頼崩壊フラグ、scenario/15で本気、scenario/18協力不可
  - `"lied"`: バルガス好感度30維持、scenario/15特別台詞、scenario/18支援弱体化

### 3. バルガス戦 (15_rank_up_S)

**選択肢:**
- `balgas_choice = "spared"`: バルガス好感度100、scenario/16発生可能
- `balgas_choice = "killed"`: バルガス好感度0、scenario/18でバルガス不在

**影響:**
- scenario/16 (リリィの真名) は `balgas_choice == "spared"` が必須
- scenario/18 の最終決戦での協力者に影響

### 4. エンディング (18_last_battle)

**選択肢:**
- `ending = "return_to_surface"`: 地上への帰還
- `ending = "rebuild_arena"`: ギルド再建
- `ending = "challenge_observers"`: 高次元への挑戦

## フラグ条件の評価

### 利用可能なクエストの判定

`QuestDependencyGraph.get_available_quests()` は以下をチェック:

1. **前提クエスト**: `required_quests` のすべてが完了済みか
2. **フラグ条件**: `required_flags` のすべてが満たされているか
3. **ブロック条件**: 特定のフラグによってブロックされていないか

### フラグ演算子

サポートされる演算子:
- `==`: 等しい
- `!=`: 等しくない
- `>=`: 以上
- `>`: より大きい
- `<=`: 以下
- `<`: より小さい

### 例: リリィの真名イベント

```python
QuestDefinition(
    quest_id="16_lily_real_name",
    required_flags=[
        FlagCondition(Keys.RANK, "==", "S"),
        FlagCondition(Keys.BALGAS_CHOICE, "==", "spared"),
        FlagCondition(Keys.REL_LILY, ">=", 50),
    ],
    required_quests=["15_rank_up_S"],
    ...
)
```

**ブロック条件** (コード内で実装):
- `lily_bottle_confession == "blamed_zek"` または `"denied"`
- `lily_hostile == True`

## C#実装への統合

### 実装されたコンポーネント

本システムは以下のC#コンポーネントで実装されています：

#### 1. **ArenaQuestManager.cs**
クエスト管理の中核クラス。シングルトンパターンで実装。

**主要機能:**
- `Package/quest_definitions.json` からクエスト定義を読み込み
- 現在のフラグ状態と完了済みクエストに基づいて利用可能なクエストを判定
- クエストの開始・完了処理
- フラグ条件の評価（整数・文字列・真偽値）

**主要メソッド:**
```csharp
public List<QuestDefinition> GetAvailableQuests()
public bool IsQuestAvailable(string questId)
public bool StartQuest(string questId)
public void CompleteQuest(string questId)
```

#### 2. **ArenaFlagManager.cs**
フラグ管理クラス。`EClass.player.dialogFlags` のラッパーとして実装済み。

**主要機能:**
- 型安全なフラグアクセス
- Player フラグ（Rank, Karma, 選択肢など）
- Relationship フラグ（Lily, Balgas, Zek）
- シナリオ条件チェック

#### 3. **DramaManager_Patch.cs**
Harmony パッチによる `DramaManager` の拡張。

**追加されたアクション:**
- `modInvoke`: C#メソッドを呼び出す汎用アクション
- `check_quest_available(questId, jumpLabel)`: クエストが利用可能ならジャンプ
- `start_quest(questId)`: クエストを開始
- `complete_quest(questId)`: クエストを完了
- `if_flag(flagKey, operator, value, jumpLabel)`: フラグ条件チェック
- `debug_log_flags()`: フラグ状態をログ出力
- `debug_log_quests()`: クエスト状態をログ出力

### ドラマシステムとの連携

#### Python DSL (drama_builder.py) での使用例

```python
from drama_builder import DramaBuilder
from flag_definitions import Keys

builder = DramaBuilder()
pc = builder.register_actor("pc", "あなた", "You")

main = builder.label("main")
quest_available = builder.label("quest_available")
quest_unavailable = builder.label("quest_unavailable")

builder.step(main) \
    .check_quest_available("01_opening", quest_available) \
    .jump(quest_unavailable)

builder.step(quest_available) \
    .say("text1", "クエストが開始できます", actor=pc) \
    .start_quest("01_opening") \
    .finish()

builder.step(quest_unavailable) \
    .say("text2", "条件を満たしていません", actor=pc) \
    .finish()
```

#### 追加されたDSLメソッド

```python
# クエスト管理
.check_quest_available(quest_id, jump_to)  # 利用可能ならジャンプ
.start_quest(quest_id)                      # クエスト開始
.complete_quest(quest_id)                   # クエスト完了

# フラグ条件（文字列/enum対応）
.if_flag_string(flag, operator, value, jump_to)

# デバッグ
.debug_log_flags()                          # フラグログ出力
.debug_log_quests()                         # クエストログ出力

# 汎用
.mod_invoke(method_call)                    # C#メソッド直接呼び出し
```

## 検証とデバッグ

### 依存関係の検証

```bash
cd tools/common
uv run python quest_dependencies.py
```

以下をチェック:
- 存在しない前提クエストの参照
- 循環依存の有無
- 利用可能なクエストの判定ロジック

### Graphviz可視化

```bash
cd tools/common
uv run python quest_dependencies.py > quest_graph.dot
dot -Tpng quest_graph.dot -o quest_graph.png
```

クエスト依存関係を視覚的に確認できます。

## まとめ

このクエストシステムは以下を提供します:

1. **明確な依存関係**: 各クエストの前提条件が明確に定義されている
2. **フラグベースの分岐**: プレイヤーの選択がフラグに記録され、後のクエストに影響
3. **検証可能性**: Python スクリプトで依存関係を検証できる
4. **拡張性**: 新しいクエストを簡単に追加できる
5. **C#への移植性**: 明確な構造により、C#への実装が容易

## ビルドプロセス

### 自動ビルド統合

`build.bat` でクエスト定義JSONが自動的にエクスポート・配置されます：

```batch
# Quest System Pipeline
echo Exporting Quest Definitions to JSON...
pushd tools\common
uv run python -c "from quest_dependencies import export_quests_to_json; ..."
popd
```

**出力先:**
- `Package/quest_definitions.json` - C#が実行時に読み込むJSON
- ビルド時に `elin_link/Package/` および Steam フォルダにコピー

### 開発ワークフロー

1. **クエスト定義の追加/編集**: `tools/common/quest_dependencies.py` の `QUEST_DEFINITIONS` リストを編集
2. **ビルド実行**: `build.bat` を実行
3. **JSON自動生成**: `Package/quest_definitions.json` が自動生成される
4. **C#が読み込み**: `ArenaQuestManager` が起動時にJSONを読み込み
5. **ゲーム内で動作**: `modInvoke` アクションでクエストシステムが利用可能

### トラブルシューティング

#### クエスト定義が読み込まれない

1. `Package/quest_definitions.json` が存在するか確認
2. ゲームログで `[ArenaQuest] Loaded N quest definitions` を確認
3. JSON構造が正しいか検証（`uv run python tools/common/quest_dependencies.py`）

#### modInvoke が動作しない

1. `DramaManager_Patch.cs` が Harmony でパッチされているか確認
2. ゲームログで `[ArenaModInvoke]` のエラーメッセージを確認
3. ドラマExcelの `action` 列が `modInvoke` になっているか確認

## 今後の拡張

### 実装済み

- ✅ クエスト依存関係システム（Python）
- ✅ JSON エクスポート機能
- ✅ C# クエストマネージャ
- ✅ Harmony パッチによる modInvoke 拡張
- ✅ Python DSL での便利メソッド
- ✅ ビルドプロセス統合

### 今後の課題

1. **セーブ/ロード機能の実装**
   - 完了済みクエストの永続化
   - ゲームセーブデータとの統合

2. **ランタイムクエスト進行**
   - クエストフェーズ管理
   - ジャーナル更新との連携

3. **デバッグUI**
   - クエスト状態の可視化
   - フラグの手動設定ツール
