# Elin_SukutsuArena 開発ガイド

## CWLドキュメント

CWL（Custom Whatever Loader）の公式ドキュメント：

```
elin_modding/Elin.Docs/articles/100_Mod Documentation/Custom Whatever Loader/JP/
├── 0_README.md              # CWL概要・基本設定
├── API/                     # API拡張
├── Character/               # キャラクター定義
│   └── 1_talks.md           # addDrama_タグ、会話システム
├── Element/                 # 要素定義
├── Other/                   # その他
│   └── 4_drama.md           # ドラマアクション（invoke*, if_flag等）
└── Thing/                   # アイテム定義
```

主要な参照：
- `1_talks.md`: NPCにカスタムダイアログを紐付ける`addDrama_`タグ
- `4_drama.md`: `invoke*`, `if_flag`, `mod_flag`等の拡張アクション

## CWLキャラクタータグ

キャラクター定義（`create_chara_excel.py`）で使用するCWLタグ：

| タグ | 説明 |
|-----|------|
| `addZone_ゾーンID` | 指定ゾーンにキャラクターを生成 |
| `addFlag_StayHomeZone` | ランダム移動を無効化（初期ゾーンに留まる） |
| `addDrama_ドラマファイル名` | **ドラマシートをキャラクターにリンク** |
| `addStock` | 商人の在庫を追加 |
| `humanSpeak` | 人間らしい会話表示（括弧なし） |

### addDrama_ タグの重要性

**このタグがないと、NPCクリック時にゲームのデフォルト会話（`_chara.xlsx`）が表示される。**

```python
# 正しい例（ドラマが読み込まれる）
'tag': f'neutral,addZone_{ZONE_ID},addDrama_drama_sukutsu_receptionist,humanSpeak',

# 誤った例（デフォルト会話になる）
'tag': f'neutral,addZone_{ZONE_ID},humanSpeak',  # addDrama_がない！
```

ドラマファイル名は `drama_` プレフィックスを含める（例: `addDrama_drama_sukutsu_receptionist`）。

## ドラマ演出機能

`drama_builder.py`で使用可能な演出メソッド：

| メソッド | 説明 | パラメータ |
|---------|------|-----------|
| `fade_in(duration, color)` | フェードイン | duration=秒, color="black"/"white" |
| `fade_out(duration, color)` | フェードアウト | duration=秒, color="black"/"white" |
| `set_background(bg_id)` | 背景画像設定 | bg_id=画像名 |
| `glitch()` | グリッチエフェクト | - |
| `shake()` | 画面揺れ | - |
| `focus_chara(chara_id)` | キャラフォーカス | chara_id=キャラID |
| `set_dialog_style(style)` | ダイアログスタイル変更 | "Default"/"Default2"/"Mono" |

### ダイアログスタイル

| スタイル | 説明 |
|---------|------|
| `Default` | 標準ダイアログ |
| `Default2` | 別スタイル |
| `Mono` | モノローグ（キャラ名なし、グレースケール背景） |

**ナレーション用例**:
```python
builder.set_dialog_style("Mono") \
    .say("narr1", "（闘技場に静寂が訪れた...）", actor=pc) \
    .set_dialog_style("Default")  # 通常に戻す
```

### 背景画像の規格

| 項目 | 値 |
|------|-----|
| **推奨サイズ** | 1920 x 1080 px |
| **最小サイズ** | 1280 x 720 px |
| **アスペクト比** | 16:9（必須） |
| **形式** | PNG |

**配置場所**: `Texture/Drama/{画像名}.png`（CWLがTextureフォルダから読み込む）

**使用時**: `set_background("Drama/{画像名}")`

**使用例**:
```python
builder.step(main) \
    .fade_out(duration=0.5, color="black") \
    .set_background("Drama/arena_lobby") \
    .fade_in(duration=1.5, color="black") \
    .say("narr1", "（異次元の闘技場に足を踏み入れた）", actor=pc)
```

## ゲーム本体コード

Elin本体のソースコードは`Elin-Decompiled`以下に配置
```
Elin-Decompiled
```

## Mod構成

```
ElinMod/Elin_SukutsuArena/
├── src/                     # C#ソースコード
│   ├── Plugin.cs            # エントリーポイント（BepInExプラグイン）
│   ├── Commands/            # IArenaCommandの実装
│   ├── Core/                # ArenaContext, DialogFlagsStorage
│   ├── State/               # PlayerState, QuestState等
│   └── Generated/           # 自動生成（ArenaFlags.cs, ArenaQuestData.cs）
│
├── tools/                   # Python生成ツール
│   ├── builder/             # 各種ジェネレーター
│   │   ├── create_chara_excel.py   # SourceChara.xlsx生成
│   │   ├── create_drama_excel.py   # ドラマExcel生成
│   │   ├── create_zone_excel.py    # SourceSukutsu.xlsx生成
│   │   ├── generate_flags.py       # ArenaFlags.cs生成
│   │   └── generate_quest_data.py  # ArenaQuestData.cs生成
│   └── common/              # 共通モジュール
│       ├── drama_builder.py        # ドラマDSL
│       ├── quest_dependencies.py   # クエスト定義
│       ├── battle_stages.py        # バトルステージ定義
│       └── scenarios/              # シナリオ定義（00_*.py）
│
├── LangMod/                 # 言語別データ（JP/EN）
│   └── */
│       ├── SourceChara.xlsx        # キャラクター定義
│       ├── SourceSukutsu.xlsx      # ゾーン定義
│       └── Dialog/Drama/*.xlsx     # ドラマファイル
│
├── Package/                 # 生成されるJSON設定
│   ├── quest_definitions.json
│   └── battle_stages.json
│
├── Texture/                 # テクスチャ
├── Portrait/                # キャラクターポートレート
├── Sound/                   # サウンド/BGM
│
├── elin_link/               # ゲームリンク（ビルド用）
│   └── Package/Elin_SukutsuArena/
│
├── build.bat                # 全体ビルドスクリプト
└── Elin_SukutsuArena.csproj # C#プロジェクト
```

## ビルド方法

### 全体ビルド（推奨）

```batch
cd ElinMod/Elin_SukutsuArena
build.bat
```

- build.bat → Releaseビルド（公開用）
- build.bat debug → DEBUGビルド（テスト用）


### Excel/Python単体ビルド

個別のPythonスクリプトを直接実行：

```bash
cd tools/builder
uv run python create_drama_excel.py   # ドラマExcel
uv run python create_chara_excel.py   # キャラExcel
uv run python generate_flags.py       # C#フラグ
```
※Elinゲームへのデプロイは行われない

### C#単体ビルド

```bash
cd ElinMod/Elin_SukutsuArena
dotnet build -c Release
```
※Elinゲームへのデプロイは行われない

### 個別スクリプト実行

```bash
cd tools

# ドラマExcelのみ再生成
uv run python builder/create_drama_excel.py

# キャラクターExcelのみ再生成
uv run python builder/create_chara_excel.py

# フラグコードのみ再生成
uv run python builder/generate_flags.py
```

## テスト・デバッグ

### バリデーション

```bash
cd tools/common
uv run python validation.py
```

シナリオ定義の整合性をチェック。

### フラグ検証

```bash
cd tools
uv run python builder/validate_scenario_flags.py
```

ドラマファイルで使用されるフラグがC#側で定義されているか検証。

## カスタムアイテム作成のハマりどころ

### SourceStat（カスタムCondition）

カスタムポーションで一時的なバフを付与する場合、`SourceStat.xlsx`（Stat.tsv）でConditionを定義する。

#### id列のデフォルト値

**デフォルト値（3行目）のidは、データ行のid最大値より大きくする必要がある。**

```python
# 正しい例
DEFAULTS = {'id': '100000', ...}  # データ行のidは10001〜10020
CONDITIONS = [{'id': '10001', ...}, {'id': '10020', ...}]

# 誤った例（エラーになる）
DEFAULTS = {'id': '100', ...}  # データ行のidより小さい
```

#### type列の指定

**type列を空にするとCWLが警告を出す。バニラのクラスを指定する。**

```python
# 推奨（警告なし）
'type': 'BaseBuff',  # バニラのBaseBuffクラスを使用

# 非推奨（動作するが警告が出る）
'type': '',  # CWLがaliasをtype名として解決しようとして警告
```

#### phase配列

`BaseCondition.GetPhase()`は`value/10`をインデックスとして使用するため、通常は10要素必要。

```csharp
// バニラの実装
public override int GetPhase()
{
    return base.source.phase[Mathf.Clamp(value, 0, 99) / 10];
}
```

**ただし`BaseBuff`/`BaseDebuff`はGetPhase=>0をオーバーライドしているので、これらを使う場合はphase配列不要。**

```python
# BaseBuffを使う場合
'type': 'BaseBuff',
'phase': '',  # 不要

# カスタムクラスを使う場合
'type': 'MyCustomCondition',
'phase': '0,0,0,0,0,0,0,0,0,0',  # 10要素必要
```

#### elements列で一時的バフ

elements列でエレメント値を一時的に変更できる。

```python
'elements': 'resCold,50',   # 冷気耐性+50
'elements': 'PV,30',        # PV+30
'elements': 'STR,10',       # 筋力+10
```

#### TSV形式とsoffice変換

**直接xlsxを生成するとCWLが読み込めない場合がある。TSVで出力してsofficeで変換する。**

```python
# build.batで自動的にsoffice変換される
OUTPUT_JP = os.path.join(PROJECT_ROOT, 'LangMod', 'JP', 'Stat.tsv')
```

### カスタムTrait（装備効果）

#### OnEquipのonSetOwner引数

**onSetOwner=trueはセーブデータロード時。新規装備時の処理と分ける。**

```csharp
public override void OnEquip(Chara c, bool onSetOwner)
{
    base.OnEquip(c, onSetOwner);

    // セーブロード時は処理をスキップ
    if (onSetOwner) return;

    // EClass._mapがnullの可能性もチェック
    if (EClass._map == null) return;

    // 新規装備時の処理（ミニオン召喚等）
    SummonMinion(c);
}
```

### TraitDrink継承（カスタムポーション）

#### IdEffectのオーバーライド

カスタム効果IDはバニラの`EffectId`列挙型に存在しないため、デフォルト値を返す。

```csharp
public class TraitSukutsuItem : TraitDrink
{
    // 列挙型変換エラーを回避
    public override EffectId IdEffect => global::EffectId.Drink;

    // 独自の効果ID（trait列の2番目パラメータ）
    public string CustomEffectId => GetParam(1) ?? "";

    public override void OnDrink(Chara c)
    {
        switch (CustomEffectId)
        {
            case "my_effect":
                ApplyMyEffect(c);
                break;
            default:
                base.OnDrink(c);
                break;
        }
    }
}
```

#### SourceThingでの指定

```python
# trait列: "名前空間.クラス名,効果ID"
'trait': 'Elin_SukutsuArena.TraitSukutsuItem,frost_ward',
```

## 既知の問題・バックログ

### キャラクターチップ移動問題
**報告日**: 2026-01-11
**状態**: 調査中

**症状**:
アスタロトやバルガスとの戦闘時、キャラクターの実体がキャラクターチップの表示についてきていない。
- キャラチップは最初の位置から動かない
- 実体は透明になって移動している

**影響キャラクター**:
- sukutsu_astaroth（アスタロト）
- sukutsu_balgas_prime（全盛期バルガス）

**調査メモ**:
- `_idRenderData: '@chara'` 設定は正しい（空にするとチップ自体が表示されなくなる）
- 現在の一時的なチップ画像の規格に起因する可能性あり
- ゲームエンジン側またはCWLの描画処理の問題かもしれない

**次のステップ**:
- カスタムチップ画像を正式な規格で作成後に再テスト
