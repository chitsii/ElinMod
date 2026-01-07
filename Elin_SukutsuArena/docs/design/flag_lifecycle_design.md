# フラグ管理システム設計書

## 目的

フラグをライフサイクル（寿命）に基づいて分類し、不要なフラグの自動クリーンアップを実現する。

---

## フラグ分類

| 分類 | プレフィックス | 削除タイミング | 用途 |
|------|---------------|----------------|------|
| **永続** | `chitsii.arena.{category}.{name}` | 削除しない | ランク、関係値、ストーリー選択 |
| **セッション** | `chitsii.arena.session.{name}` | ダイアログ終了時 | 戦闘結果 |
| **一時** | `chitsii.arena.temp.{name}` | 使用直後 | クエスト分岐ルーティング |

---

## 削除予定フラグ

### 未使用フラグ

| フラグ名 | 理由 |
|----------|------|
| `chitsii.arena.player.karma` | 設定のみで分岐に未使用 |
| `chitsii.arena.player.contribution` | 完全に未使用 |
| `chitsii.arena.player.lily_trust_rebuilding` | 定義のみで未使用 |
| `chitsii.arena.player.current_phase` | debug_battle.pyでのみ使用 |

### 計算可能なため削除

| フラグ名 | 代替方法 |
|----------|----------|
| `chitsii.arena.player.lily_hostile` | `lily_bottle_confession == 2(denied)` で判定 |
| `chitsii.arena.player.balgas_trust_broken` | `kain_soul_confession == 1(lied)` で判定 |

### 汎用バトルシステム削除

| フラグ名 | 理由 |
|----------|------|
| `sukutsu_gladiator` | 汎用バトルシステム廃止 |
| `sukutsu_arena_stage` | 汎用バトルシステム廃止 |

---

## 永続フラグ一覧（最終版）

### プレイヤー状態

| フラグ名 | 型 | 説明 |
|----------|-----|------|
| `chitsii.arena.player.rank` | int (0-8) | 現在のランク |
| `chitsii.arena.player.motivation` | int (0-3) | 動機選択 |

### 関係値

| フラグ名 | 型 | 説明 |
|----------|-----|------|
| `chitsii.arena.rel.lily` | int (0-100) | リリィとの関係値（初期値30） |
| `chitsii.arena.rel.balgas` | int (0-100) | バルガスとの関係値（初期値20） |
| `chitsii.arena.rel.zek` | int (0-100) | ゼクとの関係値（初期値0） |

### ストーリー選択

| フラグ名 | 型 | 説明 |
|----------|-----|------|
| `chitsii.arena.player.bottle_choice` | int | 0=拒否, 1=すり替え |
| `chitsii.arena.player.kain_soul_choice` | int | 0=返却, 1=売却 |
| `chitsii.arena.player.balgas_choice` | int | 0=見逃す, 1=倒す |
| `chitsii.arena.player.lily_bottle_confession` | int | 0=告白, 1=ゼクのせい, 2=否定 |
| `chitsii.arena.player.kain_soul_confession` | int | 0=告白, 1=嘘 |
| `chitsii.arena.player.ending` | int | 0=救出, 1=継承, 2=簒奪 |

### 状態フラグ

| フラグ名 | 型 | 説明 |
|----------|-----|------|
| `chitsii.arena.player.fugitive_status` | bool | 逃亡者状態 |
| `chitsii.arena.player.null_chip_obtained` | bool | ヌルの記憶チップ入手済み |
| `chitsii.arena.player.lily_true_name` | bool | リリィの真名を知っている |

### クエスト完了

| フラグ名 | 型 | 説明 |
|----------|-----|------|
| `sukutsu_quest_done_{questId}` | bool | クエスト完了状態 |

---

## セッションフラグ一覧（統合後）

### 統合前 → 統合後

```
【統合前】
sukutsu_arena_result           # 戦闘結果
sukutsu_is_rank_up_result      # ランクアップ戦か？
sukutsu_is_quest_battle_result # クエスト戦か？
sukutsu_rank_up_trial          # ランクアップ試験番号(1-7)
sukutsu_quest_battle           # クエスト戦番号(1-3)

【統合後】
chitsii.arena.session.battle_type   # 0=通常, 1=ランクアップ, 2=クエスト
chitsii.arena.session.battle_id     # ランクアップ:1-7, クエスト:1-3
chitsii.arena.session.battle_result # 0=なし, 1=勝利, 2=敗北
```

### 最終フラグ一覧

| 新名 | 型 | 説明 |
|------|-----|------|
| `chitsii.arena.session.battle_type` | int | 0=通常, 1=ランクアップ, 2=クエスト |
| `chitsii.arena.session.battle_id` | int | 戦闘識別子 |
| `chitsii.arena.session.battle_result` | int | 0=なし, 1=勝利, 2=敗北 |

---

## 一時フラグ一覧

| 新名 | 型 | 説明 |
|------|-----|------|
| `chitsii.arena.temp.quest_found` | bool | クエスト発見フラグ |
| `chitsii.arena.temp.quest_target` | int | クエスト識別番号 |

---

## 移行計画

### Phase 1: フラグ削除

#### 1-1. flag_definitions.py から削除
```python
# 削除対象
PlayerFlags.karma
PlayerFlags.contribution
PlayerFlags.lily_trust_rebuilding
PlayerFlags.current_phase
PlayerFlags.lily_hostile
PlayerFlags.balgas_trust_broken
```

#### 1-2. シナリオから削除

| ファイル | 削除内容 |
|----------|----------|
| `13_makuma2.py` | `mod_flag(Keys.KARMA, ...)` 3箇所削除 |
| `13_makuma2.py` | `set_flag(Keys.LILY_HOSTILE, ...)` 削除 |
| `13_makuma2.py` | `set_flag(Keys.BALGAS_TRUST_BROKEN, ...)` 削除 |

#### 1-3. C# から代替ロジック追加

```csharp
// ArenaFlagManager.cs に追加
public static bool IsLilyHostile()
{
    // lily_bottle_confession == 2 (denied) で判定
    return GetInt(ArenaFlagKeys.LilyBottleConfession, -1) == 2;
}

public static bool IsBalgasTrustBroken()
{
    // kain_soul_confession == 1 (lied) で判定
    return GetInt(ArenaFlagKeys.KainSoulConfession, -1) == 1;
}
```

---

### Phase 2: 汎用バトルシステム削除

#### 2-1. シナリオから削除

| ファイル | 削除内容 |
|----------|----------|
| `00_arena_master.py` | `battle_prep` 〜 `battle_start_champion` のステップ全削除 |
| `00_arena_master.py` | `random_battle_menu` 関連のステップ削除 |
| `00_arena_master.py` | `add_choices()` から `battle_prep` への選択肢削除 |
| `01_opening.py` | `set_flag("sukutsu_gladiator", 1)` 削除 |
| `01_opening.py` | `set_flag("sukutsu_arena_stage", 1)` 削除 |

#### 2-2. 関連C#コード確認
- `ArenaManager.cs` の汎用バトル関連メソッドがあれば削除

---

### Phase 3: セッションフラグ統合

#### 3-1. 新フラグキー追加

```python
# flag_definitions.py
class SessionKeys:
    BATTLE_TYPE = "chitsii.arena.session.battle_type"
    BATTLE_ID = "chitsii.arena.session.battle_id"
    BATTLE_RESULT = "chitsii.arena.session.battle_result"
```

#### 3-2. シナリオ書き換え

**戦闘開始時（例: rank_g.py）**
```python
# Before
.set_flag("sukutsu_is_rank_up_result", 1)
.set_flag("sukutsu_rank_up_trial", 1)

# After
.set_flag(SessionKeys.BATTLE_TYPE, 1)  # 1=ランクアップ
.set_flag(SessionKeys.BATTLE_ID, 1)    # 1=G
```

**結果判定時（00_arena_master.py）**
```python
# Before
.branch_if("sukutsu_is_rank_up_result", "==", 1, "rank_up_result_check")
.branch_if("sukutsu_is_quest_battle_result", "==", 1, "quest_battle_result_check")

# After
.branch_if(SessionKeys.BATTLE_TYPE, "==", 1, "rank_up_result_check")
.branch_if(SessionKeys.BATTLE_TYPE, "==", 2, "quest_battle_result_check")
```

#### 3-3. 書き換え対象ファイル一覧

| ファイル | 変更内容 |
|----------|----------|
| `00_arena_master.py` | 結果判定ロジック書き換え |
| `rank_up/rank_g.py` | 戦闘開始フラグ書き換え |
| `rank_up/rank_f.py` | 同上 |
| `rank_up/rank_e.py` | 同上 |
| `rank_up/rank_d.py` | 同上 |
| `rank_up/rank_c.py` | 同上 |
| `rank_up/rank_b.py` | 同上 |
| `rank_up/rank_a.py` | 同上 |
| `07_upper_existence.py` | クエスト戦フラグ書き換え |
| `15_vs_balgas.py` | 同上 |
| `18_last_battle.py` | 同上 |

---

### Phase 4: 一時フラグ移行

#### 4-1. シナリオ書き換え

```python
# Before
.set_flag("sukutsu_quest_found", 0)
.set_flag("sukutsu_quest_target_name", 0)

# After
.set_flag(TempKeys.QUEST_FOUND, 0)
.set_flag(TempKeys.QUEST_TARGET, 0)
```

#### 4-2. ArenaDramaActions.cs 書き換え

`SetQuestTargetFlag()` のフラグ名を新名に変更

---

### Phase 5: クリーンアップ実装

#### 5-1. ArenaFlagManager.cs

```csharp
public static void ClearSessionFlags()
{
    if (EClass.player?.dialogFlags == null) return;
    var keys = EClass.player.dialogFlags.Keys
        .Where(k => k.StartsWith("chitsii.arena.session."))
        .ToList();
    foreach (var key in keys)
        EClass.player.dialogFlags.Remove(key);
}

public static void ClearTempFlags()
{
    if (EClass.player?.dialogFlags == null) return;
    var keys = EClass.player.dialogFlags.Keys
        .Where(k => k.StartsWith("chitsii.arena.temp."))
        .ToList();
    foreach (var key in keys)
        EClass.player.dialogFlags.Remove(key);
}
```

#### 5-2. フック追加
- ダイアログ終了時に `ClearSessionFlags()` 呼び出し

---

## フラグ総数比較

| 分類 | 移行前 | 移行後 |
|------|--------|--------|
| 永続 | 21 | 14 |
| セッション | 7 | 3 |
| 一時 | 3 | 2 |
| **合計** | **31** | **19** |

削減率: **39%**
