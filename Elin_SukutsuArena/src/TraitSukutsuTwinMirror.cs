using UnityEngine;

namespace Elin_SukutsuArena
{
    /// <summary>
    /// 双子の鏡 - 装備時に影の自己をミニオンとして召喚
    /// </summary>
    public class TraitSukutsuTwinMirror : Trait
    {
        /// <summary>
        /// 召喚したミニオンのUID（解除時に削除するため）
        /// </summary>
        private int summonedMinionUid = 0;

        /// <summary>
        /// 装備時：影の自己を召喚
        /// </summary>
        public override void OnEquip(Chara c, bool onSetOwner)
        {
            base.OnEquip(c, onSetOwner);

            // セーブデータロード時（onSetOwner=true）は召喚しない
            // ミニオンは別途セーブ/ロードされる
            if (onSetOwner) return;

            // マップがまだ初期化されていない場合はスキップ
            if (EClass._map == null) return;

            // 既に召喚済みなら何もしない
            if (summonedMinionUid != 0)
            {
                var existingMinion = EClass._map.FindChara(summonedMinionUid);
                if (existingMinion != null && !existingMinion.isDead)
                {
                    Debug.Log($"[SukutsuArena] Twin Mirror: Minion already exists (uid={summonedMinionUid})");
                    return;
                }
            }

            // ミニオン召喚
            SummonShadowSelf(c);
        }

        /// <summary>
        /// 装備解除時：ミニオンを削除
        /// </summary>
        public override void OnUnequip(Chara c)
        {
            base.OnUnequip(c);

            // 召喚したミニオンを削除
            DismissShadowSelf();
        }

        /// <summary>
        /// 影の自己を召喚
        /// </summary>
        private void SummonShadowSelf(Chara master)
        {
            if (master == null || EClass._map == null) return;

            // 影の自己のキャラクターID（battle_stages.pyで定義済み）
            string shadowId = "sukutsu_shadow_self";

            // キャラクター生成
            Chara shadow = CharaGen.Create(shadowId);
            if (shadow == null)
            {
                Debug.LogWarning($"[SukutsuArena] Failed to create shadow self ({shadowId})");
                return;
            }

            // レベルをマスターに合わせる
            shadow.SetLv(master.LV);

            // マスターの近くに配置
            Point spawnPoint = master.pos.GetNearestPoint(allowBlock: false, allowChara: false);
            if (spawnPoint == null || !spawnPoint.IsValid)
            {
                spawnPoint = master.pos;
            }

            // マップに追加
            EClass._zone.AddCard(shadow, spawnPoint);

            // ミニオンとして設定
            shadow.MakeMinion(master, MinionType.Default);

            // 召喚扱いにする（ゾーン移動時に消える）
            shadow.SetSummon(9999); // 非常に長い持続時間

            // UIDを保存
            summonedMinionUid = shadow.uid;

            // 演出
            master.PlaySound("spell_buff");
            shadow.PlayEffect("buff");

            Msg.Say("sukutsu_twin_mirror_summon", master, shadow);
            Debug.Log($"[SukutsuArena] Summoned Shadow Self (uid={shadow.uid}, lv={shadow.LV}) for {master.Name}");
        }

        /// <summary>
        /// 影の自己を解散
        /// </summary>
        private void DismissShadowSelf()
        {
            if (summonedMinionUid == 0) return;

            var minion = EClass._map?.FindChara(summonedMinionUid);
            if (minion != null && !minion.isDead)
            {
                // 演出
                minion.PlayEffect("vanish");
                minion.PlaySound("identify");

                Msg.Say("sukutsu_twin_mirror_dismiss", minion);

                // 削除
                minion.Destroy();
                Debug.Log($"[SukutsuArena] Dismissed Shadow Self (uid={summonedMinionUid})");
            }

            summonedMinionUid = 0;
        }
    }
}
