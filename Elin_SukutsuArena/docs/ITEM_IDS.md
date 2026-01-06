# アイテムID リファレンス

1165	potion	エーテル抗体のポーション
lovepotion	potion	媚薬
blood_angel	potion	堕天使の血
rod_wish	rod	願いの杖
goodness	ingredient	この耐えがたい世界に残された最後の僅かな良心
rune_free	無法のルーン	　
medal	小さなメダル








---

## ThingGen.Create() の使用例

```csharp
// 単一アイテム
EClass.pc.Pick(ThingGen.Create("plat"));

// 複数アイテム
for(int i=0; i<10; i++) {
    EClass.pc.Pick(ThingGen.Create("money"));
}

// 報酬セット例
for(int i=0; i<10; i++) { EClass.pc.Pick(ThingGen.Create("money")); }
for(int i=0; i<3; i++) { EClass.pc.Pick(ThingGen.Create("plat")); }

// 貴重品（小さなメダル）
EClass.pc.Pick(ThingGen.Create("medal"));

// カジノチップ10枚
for(int i=0; i<10; i++) { EClass.pc.Pick(ThingGen.Create("casino_coin")); }
```

---

## 参考リンク

- [Ylvapedia - Currencies](https://ylvapedia.wiki/wiki/Elin:Currencies)
- [Ylvapedia - Materials](https://ylvapedia.wiki/wiki/Elin:Materials)
- [願いでおすすめのアイテム](https://mazimenigame.com/elin-wish/)
- [Steam New Player's Guide](https://steamcommunity.com/sharedfiles/filedetails/?id=3358083554)




