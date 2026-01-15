# Sukutsu Arena クエストライン実装TODO

このドキュメントはクエストラインを完成させるために必要な作業を網羅的にまとめたものです。

## 実装状況サマリー

| カテゴリ | 完了 | 未完了 | 進捗 |
|---------|------|--------|------|
| ランクアップ試験 | 7/8 | 1 | 88% |
| ストーリークエスト | 13/14 | 1 | 93% |
| バトルステージ | 12/12 | 0 | 100% |
| バフシステム | 12/12 | 0 | 100% |

---

## 1. ~~【CRITICAL】ランクA昇格試験の実装~~ ✅ 完了

### 1.1 シナリオファイル作成 ✅
- [x] `scenarios/rank_up/rank_a.py` を新規作成
  - 参照: `battle_stages.py` の `rank_a_trial` 定義
  - 敵: `sukutsu_shadow_self` (レベル2500, Mythical)
  - テーマ: 「戦鬼」（影の自己との戦い）
  - 観客の「注目」が生み出した自分の影と戦う

### 1.2 drama_constants.py への追加 ✅
```python
# DramaIds に追加
RANK_UP_A = "rank_up_A"

# DramaNames に追加
RANK_UP_A = f"drama_{DramaIds.RANK_UP_A}"

# ALL_DRAMA_IDS に追加
DramaIds.RANK_UP_A,
```

### 1.3 arena_master.py への追加 ✅
- [x] `rank_up_victory_a` / `rank_up_defeat_a` ラベル追加
- [x] `rank_up_result_a` 結果分岐追加
- [x] `sukutsu_rank_up_trial` フラグ値 `7` の追加（A試験用）
- [x] `start_rank_a` / `start_rank_a_confirmed` ステップ追加
- [x] `add_rank_up_A_result_steps()` の呼び出し追加

### 1.4 ArenaManager.cs への追加 ✅
```csharp
public static void GrantRankABonus()
{
    var pc = EClass.pc;
    if (pc == null) return;

    // 影との戦い報酬
    pc.elements.ModBase(70, 5);   // STR+5
    pc.elements.ModBase(77, 5);   // MAG+5
    pc.elements.ModBase(152, 5);  // DV+5
    pc.elements.ModBase(153, 5);  // PV+5

    Msg.Say("【戦鬼】筋力+5、魔力+5、回避+5、PV+5 を獲得！");
}
```

### 1.5 create_drama_excel.py への追加 ✅
- [x] `rank_up_A` のビルド登録追加

---

## 2. 【HIGH】vs_balgas バトル統合

### 2.1 現状
- `15_vs_balgas.py` は物語のみ、実際の戦闘なし
- `rank_s_trial` バトルステージは存在（sukutsu_balgas_prime, Lv.8000）

### 2.2 実装方針
ストーリー上、バルガスを「殺す/助ける」選択があるため、戦闘後に分岐が必要。

選択肢A: 戦闘を統合する
- [ ] scene3 に `start_battle_by_stage("rank_s_trial")` を追加
- [ ] `add_vs_balgas_result_steps()` 関数を作成
- [ ] arena_master.py にクエストバトル結果ディスパッチを追加
  - `sukutsu_quest_battle = 2` (vs_balgas用)

選択肢B: 現状維持（物語のみ）
- 戦闘は演出として描写し、実際のバトルは発生しない
- この場合、追加作業は不要

**決定事項**: ユーザーに確認が必要

---

## 3. ~~【HIGH】最終決戦バトル統合~~ ✅ 完了

### 3.1 現状 ✅
- `18_last_battle.py` のact4に「プレースホルダー」コメント → バトル統合済み
- `final_astaroth` バトルステージは存在（sukutsu_astaroth, Lv.50000）

### 3.2 実装タスク ✅
- [x] act4 に `start_battle_by_stage("final_astaroth")` を追加
- [x] `add_last_battle_result_steps()` 関数を作成
- [x] arena_master.py にクエストバトル結果ディスパッチを追加
  - `sukutsu_quest_battle = 3` (final_astaroth用)
- [x] 勝利時: act5へ進行（ドラマを継続開始）
- [x] 敗北時: 適切な敗北シーン追加

### 3.3 ArenaManager.cs 追加 ✅
- [x] `GrantLastBattleBonus()` を追加（全ステータス+10、全耐性+10）

---

## 4. ~~【MEDIUM】ランクアップ試験の選択肢追加~~ ✅ 完了

### 4.1 arena_master.py のランクアップ確認 ✅
ランクA試験を追加済み:

```python
# ランクA試験開始確認
builder.step(start_rank_a) \
    .say("rank_up_confirm_a", "『影との戦い』だ。お前自身の影と戦うことになる。覚悟はいいか？", "", actor=vargus) \
    .choice(start_rank_a_confirmed, "挑む", "", text_id="c_confirm_rup_a") \
    .choice(registered_choices, "やめておく", "", text_id="c_cancel_rup") \
    .on_cancel(registered_choices)

# ランクA試験実行
builder.step(start_rank_a_confirmed) \
    .set_flag("sukutsu_rank_up_trial", 7) \
    .say_and_start_drama("……行ってこい。お前の内なる敵を、打ち倒せ。", DramaNames.RANK_UP_A, "sukutsu_arena_master") \
    .jump(end)
```

---

## 5. 【LOW】シナリオ検証・整合性チェック

### 5.1 物語シナリオ確認
- [ ] `01_opening.py` - オープニングの完成度確認
- [ ] `12_makuma.py` - ヌルの記憶チップイベント確認
- [ ] `13_makuma2.py` - 虚空の心臓製作イベント確認

### 5.2 フラグ整合性
- [ ] `Keys.RANK` の値設定（数値 vs 文字列）の統一確認
- [ ] 各クエスト完了時のフラグ設定確認

---

## 6. 【LOW】カスタムキャラクター定義

### 6.1 未定義の敵キャラ
以下のキャラクターIDがbattle_stages.pyで参照されているが、Elinのデフォルトに存在しない可能性:

- `sukutsu_kain_ghost` - カインの亡霊
- `sukutsu_null` - ヌル（暗殺人形）
- `sukutsu_shadow_self` - 影の自己
- `sukutsu_balgas_prime` - 全盛期バルガス
- `sukutsu_astaroth` - アスタロト

### 6.2 実装オプション
- 既存キャラをリネームして使用
- SourceChara に新規定義を追加
- または既存の近い敵（gladiator, dragon等）で代用

---

## 7. ファイル対応表

### シナリオファイル ↔ クエストID ↔ ドラマID

| ファイル | QuestId | DramaId | 状態 |
|----------|---------|---------|------|
| rank_up/rank_g.py | RANK_UP_G | rank_up_G | ✅ 完了 |
| rank_up/rank_f.py | RANK_UP_F | rank_up_F | ✅ 完了 |
| rank_up/rank_e.py | RANK_UP_E | rank_up_E | ✅ 完了 |
| rank_up/rank_d.py | RANK_UP_D | rank_up_D | ✅ 完了 |
| rank_up/rank_c.py | RANK_UP_C | rank_up_C | ✅ 完了 |
| rank_up/rank_b.py | RANK_UP_B | rank_up_B | ✅ 完了 |
| rank_up/rank_a.py | RANK_UP_A | rank_up_A | ✅ **完了** |
| 15_vs_balgas.py | RANK_UP_S | vs_balgas | ⚠️ バトルなし |
| 07_upper_existence.py | UPPER_EXISTENCE | upper_existence | ✅ 完了 |
| 08_lily_private.py | LILY_PRIVATE | lily_private | ✅ 完了 |
| 09_balgas_training.py | BALGAS_TRAINING | balgas_training | ✅ 完了 |
| 16_lily_real_name.py | LILY_REAL_NAME | lily_real_name | ✅ 完了 |
| 17_vs_grandmaster_1.py | VS_GRANDMASTER_1 | vs_grandmaster_1 | ✅ 完了(物語のみ) |
| 18_last_battle.py | LAST_BATTLE | last_battle | ✅ **バトル統合完了** |

---

## 8. 次のアクション（優先順）

1. ~~**rank_a.py 作成** - 最優先、クエストラインの穴を埋める~~ ✅ 完了
2. ~~**18_last_battle.py バトル統合** - エンドコンテンツ完成~~ ✅ 完了
3. **vs_balgas バトル方針決定** - ユーザー確認後
4. ~~**ビルド＆テスト** - `build_all.py` 実行~~ ✅ 完了

---

## 更新履歴

- 2026-01-06: 初版作成、全コード精査完了
- 2026-01-06: ランクA昇格試験実装完了、最終決戦バトル統合完了
