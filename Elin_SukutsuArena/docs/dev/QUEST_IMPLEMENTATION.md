# Quest System Implementation Summary

## 概要

Sukutsu Arena Mod にクエスト依存関係管理システムを実装しました。
Python でクエスト定義を管理し、JSON 経由で C# に渡し、ランタイムでクエストの進行を制御します。

## アーキテクチャ

```
Python (ビルド時)              C# (ランタイム)
─────────────────              ─────────────────
quest_dependencies.py    →     ArenaQuestManager.cs
  ↓ JSON export                  ↓ Load JSON
Package/                       Quest definitions in memory
quest_definitions.json           ↓ Check availability
                              DramaManager_Patch.cs
                                ↓ modInvoke action
                              Drama Excel (CWL)
                                ↓ Execute
                              ゲーム内でクエスト進行
```

## 実装されたファイル

### C# コンポーネント

#### 1. `src/ArenaQuestManager.cs` (新規作成)
- **役割**: クエスト管理の中核クラス
- **機能**:
  - `Package/quest_definitions.json` を読み込み
  - フラグ条件に基づいて利用可能なクエストを判定
  - クエストの開始・完了処理
  - 完了時にフラグを自動設定
- **主要メソッド**:
  ```csharp
  public List<QuestDefinition> GetAvailableQuests()
  public bool IsQuestAvailable(string questId)
  public bool StartQuest(string questId)
  public void CompleteQuest(string questId)
  ```

#### 2. `src/DramaManager_Patch.cs` (新規作成)
- **役割**: DramaManager に modInvoke アクションを追加
- **Harmony パッチ**: `DramaManager.Play()` の Prefix
- **追加アクション**:
  - `check_quest_available(questId, jumpLabel)` - クエストが利用可能ならジャンプ
  - `start_quest(questId)` - クエスト開始
  - `complete_quest(questId)` - クエスト完了
  - `if_flag(flagKey, operator, value, jumpLabel)` - フラグ条件分岐（文字列対応）
  - `debug_log_flags()` - デバッグ用フラグログ
  - `debug_log_quests()` - デバッグ用クエストログ

#### 3. `src/ArenaFlagManager.cs` (既存)
- **役割**: フラグ管理（既に実装済み）
- **機能**: `EClass.player.dialogFlags` のラッパー

### Python コンポーネント

#### 4. `tools/common/quest_dependencies.py` (更新)
- **追加機能**: `export_quests_to_json()` 関数
- **出力**: `Package/quest_definitions.json`
- **内容**: 19個のクエスト定義（依存関係、フラグ条件、完了フラグ等）

#### 5. `tools/common/drama_builder.py` (更新)
- **追加メソッド**:
  ```python
  .mod_invoke(method_call)                      # 汎用C#メソッド呼び出し
  .check_quest_available(quest_id, jump_to)     # クエスト利用可能性チェック
  .start_quest(quest_id)                        # クエスト開始
  .complete_quest(quest_id)                     # クエスト完了
  .if_flag_string(flag, operator, value, jump_to)  # 文字列フラグ条件
  .debug_log_flags()                            # フラグログ
  .debug_log_quests()                           # クエストログ
  ```

### ビルドスクリプト

#### 6. `build.bat` (更新)
- **追加パイプライン**: Quest System Pipeline
- **処理内容**:
  1. `quest_dependencies.py` から JSON をエクスポート
  2. `Package/quest_definitions.json` を生成
  3. ビルド時に `elin_link/Package/` と Steam フォルダにコピー

### ドキュメント

#### 7. `QUEST_SYSTEM.md` (更新)
- C# 実装の詳細を追加
- ビルドプロセスの説明を追加
- トラブルシューティング情報を追加

#### 8. `QUEST_IMPLEMENTATION.md` (本ファイル)
- 実装の全体像を説明

## データフロー

### ビルド時

1. `build.bat` 実行
2. Quest System Pipeline で `quest_dependencies.py` の `export_quests_to_json()` を呼び出し
3. `Package/quest_definitions.json` に 19 個のクエスト定義を出力
4. C# コンパイル
5. 配置時に JSON も一緒にコピー

### ゲーム起動時

1. `ArenaQuestManager` シングルトンが初期化
2. `Package/quest_definitions.json` を読み込み
3. 19 個のクエスト定義がメモリに格納
4. `DramaManager_Patch` が Harmony により適用

### ドラマ実行時

1. Drama Excel が `action=modInvoke` の行を実行
2. `DramaManager_Patch` がインターセプト
3. `param` を解析してメソッド名と引数を取得
4. 対応する C# メソッドを呼び出し
   - 例: `check_quest_available(01_opening, quest_start)`
5. `ArenaQuestManager.IsQuestAvailable("01_opening")` をチェック
6. 利用可能なら `manager.Goto("quest_start")` でジャンプ

## 使用例

### Python DSL でのクエスト制御

```python
from drama_builder import DramaBuilder
from flag_definitions import Keys

builder = DramaBuilder()
pc = builder.register_actor("pc", "あなた", "You")
lily = builder.register_actor("sukutsu_receptionist", "リリィ", "Lily")

main = builder.label("main")
quest_start = builder.label("quest_start")
not_ready = builder.label("not_ready")

# メインステップ: クエストが利用可能かチェック
builder.step(main) \
    .say("lily_1", "ようこそ、闘技場へ！", actor=lily) \
    .check_quest_available("01_opening", quest_start) \
    .jump(not_ready)

# クエスト開始
builder.step(quest_start) \
    .say("lily_2", "それでは、オープニングクエストを開始します", actor=lily) \
    .start_quest("01_opening") \
    .play_bgm("BGM/opening") \
    .finish()

# 条件未達成
builder.step(not_ready) \
    .say("lily_3", "まだ準備ができていないようですね", actor=lily) \
    .finish()

# ビルド
builder.save("../../LangMod/EN/Drama/quest_example.xlsx", "lily")
```

### 生成される Drama Excel

| step | jump | if | action | param | actor | text_JP |
|------|------|----|----|-------|-------|---------|
| main | | | | | sukutsu_receptionist | ようこそ、闘技場へ！ |
| | | | modInvoke | check_quest_available(01_opening, quest_start) | pc | |
| | not_ready | | | | | |
| quest_start | | | | | sukutsu_receptionist | それでは、オープニングクエストを開始します |
| | | | modInvoke | start_quest(01_opening) | pc | |
| | | | eval | ... (BGM再生コード) | | |
| | | | end | | | |

## 技術的な詳細

### JSON スキーマ

```json
{
  "questId": "01_opening",
  "questType": "main_story",
  "dramaId": "opening",
  "displayNameJP": "異次元の闘技場への到着",
  "displayNameEN": "Arrival at the Dimensional Arena",
  "description": "プレイヤーがアリーナに到着し、リリィとバルガスに出会う",
  "requiredFlags": [
    {
      "flagKey": "chitsii.arena.player.rank",
      "operator": "==",
      "value": "unranked"
    }
  ],
  "requiredQuests": [],
  "completionFlags": {
    "chitsii.arena.player.rank": "unranked",
    "chitsii.arena.rel.lily": 30
  },
  "branchChoices": [],
  "blocksQuests": [],
  "priority": 1000
}
```

### フラグ条件の評価

`ArenaQuestManager.CheckFlagCondition()` は以下の演算子をサポート:
- `==`, `!=`: 等価比較（整数、文字列、真偽値）
- `>=`, `>`, `<=`, `<`: 大小比較（整数のみ）

例:
```python
# 整数比較
{"flagKey": "chitsii.arena.rel.lily", "operator": ">=", "value": 50}

# 文字列比較（enum）
{"flagKey": "chitsii.arena.player.rank", "operator": "==", "value": "S"}

# 真偽値比較
{"flagKey": "chitsii.arena.player.fugitive_status", "operator": "==", "value": true}
```

## 今後の拡張可能性

### 1. セーブ/ロード統合

完了済みクエストをセーブデータに保存:

```csharp
// セーブ時
public void OnSave(SaveData data) {
    data.SetString("arena_completed_quests",
        string.Join(",", completedQuests));
}

// ロード時
public void OnLoad(SaveData data) {
    var saved = data.GetString("arena_completed_quests", "");
    completedQuests = new HashSet<string>(saved.Split(','));
}
```

### 2. ジャーナル統合

クエストをゲーム内ジャーナルに表示:

```csharp
public void SyncToJournal() {
    foreach (var quest in GetAvailableQuests()) {
        var journalQuest = new Quest {
            name = quest.DisplayNameJP,
            detail = quest.Description,
            phase = 0
        };
        EClass.player.quests.Add(journalQuest);
    }
}
```

### 3. デバッグUI

F9 キーでクエスト状態を表示:

```csharp
void Update() {
    if (Input.GetKeyDown(KeyCode.F9)) {
        ShowQuestDebugUI();
    }
}
```

## まとめ

この実装により、以下が実現されました：

✅ **シングルソースの真実**: Python でクエスト定義を管理、JSON 経由で C# に渡す
✅ **型安全なアクセス**: C# でクエストとフラグを型安全に扱える
✅ **自動ビルド統合**: `build.bat` 一発でクエストJSONが生成・配置される
✅ **ドラマとの連携**: `modInvoke` アクションで Drama から直接クエスト制御
✅ **デバッグ機能**: ログ出力でクエスト状態を確認可能
✅ **拡張性**: 新しいクエストを `QUEST_DEFINITIONS` に追加するだけ

次のステップは、実際のシナリオファイルでこのシステムを活用し、
プレイヤーの進行に応じて動的にクエストを提示することです。
