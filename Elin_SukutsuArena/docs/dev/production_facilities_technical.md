# 生産施設 技術検証レポート

地下闘技場固有の生産施設の実装に関する技術検証結果。

---

## 概要

| 機能 | 実装可能性 | 難易度 | 通貨 |
|------|-----------|--------|------|
| ポーション強化 | ✅ 可能 | 低 | 小さなメダル |
| 呪い装備製造 | ✅ 可能 | 非常に低 | 小さなメダル |
| 魔法スペル習得 | ⚠️ 部分的 | 中〜高 | 小さなメダル |

---

## 1. ポーション強化

### 概要

複数のポーションを消費して、効果が強化されたポーションを作成する。

### 利用API

```csharp
// アイテム作成
Thing potion = ThingGen.CreatePotion(elementId, num);

// 強化値の設定（encLV = 200 で効果2倍）
potion.encLV = 200;  // プロパティ直接設定
potion.SetEncLv(200); // メソッド経由
potion.ModEncLv(50);  // 加算

// アイテム消費
thing.ModNum(-1, notify: true);

// 小さなメダル消費
// アイテムID: "medal"
Thing medal = owner.things.Find("medal");
medal.ModNum(-cost);
```

### 効果倍率の仕組み

`ActEffect.cs:366` にて `Act.powerMod` が効果に乗算される：

```csharp
num4 = num4 * Act.powerMod / 100;
```

### 実装案

#### 方法A: カスタムTrait（推奨）

```csharp
public class TraitEnhancedPotion : TraitPotion
{
    // Powerプロパティをオーバーライドして強化値を反映
    public override int Power => base.Power * (100 + owner.encLV) / 100;
}
```

#### 方法B: 使用時にpowerMod設定

```csharp
// 使用前に設定
Act.powerMod = 100 + potion.encLV;
ActEffect.Proc(effectId, power, blessedState, target);
Act.powerMod = 100; // リセット
```

### 関連ファイル

- `Elin-Decompiled/Elin/TraitPotion.cs` - ポーションTrait
- `Elin-Decompiled/Elin/TraitDrink.cs` - 飲み物基底クラス（OnDrink）
- `Elin-Decompiled/Elin/ActEffect.cs` - 効果処理
- `Elin-Decompiled/Elin/ThingGen.cs` - アイテム生成

---

## 2. 呪い装備製造

### 概要

装備品を呪い状態にする施設。マイナスエンチャントの選別に有用。

### 利用API

```csharp
// 呪い状態の設定
thing.SetBlessedState(BlessedState.Cursed);

// 堕落状態（より強い呪い）
thing.SetBlessedState(BlessedState.Doomed);

// 通常状態に戻す
thing.SetBlessedState(BlessedState.Normal);

// 祝福状態
thing.SetBlessedState(BlessedState.Blessed);

// 現在の状態確認
BlessedState state = thing.blessedState;
bool isCursed = thing.IsCursed;   // Cursed または Doomed
bool isBlessed = thing.IsBlessed;
```

### BlessedState列挙型

```csharp
public enum BlessedState
{
    Doomed = -2,   // 堕落
    Cursed = -1,   // 呪い
    Normal = 0,    // 通常
    Blessed = 1    // 祝福
}
```

### 装備品判定

```csharp
// 装備品かどうか
bool isEquipment = thing.IsEquipment;
bool isEquipmentOrRanged = thing.IsEquipmentOrRangedOrAmmo;

// カテゴリによる判定
bool isWeapon = thing.category.IsChildOf("weapon");
bool isArmor = thing.category.IsChildOf("armor");
```

### 関連ファイル

- `Elin-Decompiled/Elin/Card.cs` - SetBlessedState, blessedState
- `Elin-Decompiled/Elin/ActEffect.cs:1808` - 呪い付与の実装例

---

## 3. 魔法スペル習得

### 概要

プレイヤーが形態と属性を選択して、既存スペルを習得する。

> **注意**: 動的な新規スペル生成は不可。SourceElementで事前定義されたスペルのみ。

### 利用API

```csharp
// スペル習得
chara.GainAbility(elementId, multiplier: 100, origin: null);

// 直接習得（経験値なし）
chara.elements.Learn(elementId, value: 1);

// スペル所持確認
Element spell = chara.elements.GetElement(elementId);
bool hasSpell = spell != null && spell.ValueWithoutLink > 0;
```

### スペルID体系

スペルIDは `形態ID + 属性ID` の形式：

| 形態 | ベースID | 説明 |
|------|----------|------|
| ball_ | 7001 (50100) | 球（範囲） |
| bolt_ | 7002 (50300) | 矢（直線） |
| hand_ | 7003 (50400) | 接触 |
| arrow_ | 7004 (50500) | 矢 |
| funnel_ | 7005 (50600) | 漏斗 |
| miasma_ | 7006 (50700) | 瘴気 |
| weapon_ | 7007 (50800) | 武器付与 |
| puddle_ | 7800 (50900) | 水溜り |
| sword_ | 7008 (51000) | 剣 |
| bit_ | 7009 (51100) | ビット |
| flare_ | 7010 (51200) | フレア |

| 属性 | ID | 例 (ball_) |
|------|-----|-----------|
| Fire | 00 | 50100 |
| Cold | 01 | 50101 |
| Lightning | 02 | 50102 |
| Darkness | 03 | 50103 |
| Mind | 04 | 50104 |
| Poison | 05 | 50105 |
| Nether | 06 | 50106 |
| Sound | 07 | 50107 |
| Nerve | 08 | 50108 |
| Holy | 09 | 50109 |
| Chaos | 10 | 50110 |
| Magic | 11 | 50111 |
| Ether | 12 | 50112 |
| Acid | 13 | 50113 |
| Cut | 14 | 50114 |
| Impact | 15 | 50115 |
| Void | 16 | 50116 |

### スペルID計算例

```csharp
// ball_Fire = 50100
// ball_Cold = 50101
// bolt_Fire = 50300
// arrow_Lightning = 50502

int GetSpellId(string shape, int element)
{
    int baseId = shape switch
    {
        "ball" => 50100,
        "bolt" => 50300,
        "hand" => 50400,
        "arrow" => 50500,
        "funnel" => 50600,
        "miasma" => 50700,
        "weapon" => 50800,
        "puddle" => 50900,
        "sword" => 51000,
        "bit" => 51100,
        "flare" => 51200,
        _ => 50100
    };
    return baseId + element;
}
```

### スペルブック作成

```csharp
// スペルブック作成
Thing spellbook = ThingGen.CreateSpellbook(elementId, num: 1, charge: -1);

// スクロール作成
Thing scroll = ThingGen.CreateScroll(elementId, num: 1);
```

### 関連ファイル

- `Elin-Decompiled/Elin/SPELL.cs` - スペルID定数一覧
- `Elin-Decompiled/Elin/Chara.cs:10076` - GainAbility
- `Elin-Decompiled/Elin/ElementContainer.cs:265` - Learn
- `Elin-Decompiled/Elin/TraitSpellbook.cs` - スペルブック
- `Elin-Decompiled/Elin/SourceElement.cs` - 要素定義

---

## 共通: 小さなメダル通貨

### API

```csharp
// アイテムID
const string MEDAL_ID = "medal";

// 所持数確認
Thing medal = EClass.pc.things.Find(MEDAL_ID);
int count = medal?.Num ?? 0;

// 消費
if (medal != null && medal.Num >= cost)
{
    medal.ModNum(-cost);
    // 処理実行
}

// 付与
Thing newMedal = ThingGen.Create(MEDAL_ID);
newMedal.SetNum(amount);
EClass.pc.Pick(newMedal);
```

---

## 実装優先度

1. **呪い装備製造** - APIがシンプル、即実装可能
2. **ポーション強化** - カスタムTraitが必要だが難易度低
3. **魔法スペル習得** - UI設計が必要、後回し推奨

---

## 参考: 既存の類似実装

- `InvOwnerEnchant.cs` - エンチャント処理
- `InvOwnerChangeMaterial.cs` - 素材変更
- `TraitDrink.cs:100-146` - OnBlend（ポーション合成）
