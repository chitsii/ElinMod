using UnityEngine;

namespace Elin_SukutsuArena
{
    /// <summary>
    /// 双子の鏡 - 装備時に影の自己をミニオンとして召喚
    /// </summary>
    public class TraitSukutsuTwinMirror : Trait
    {
        /// <summary>
        /// ミニオンUIDを保存するカスタムデータのキー
        /// </summary>
        private const int MINION_UID_KEY = 9901;

        /// <summary>
        /// 召喚したミニオンのUID（セーブ対応：ownerのカスタムデータに保存）
        /// </summary>
        private int SummonedMinionUid
        {
            get => owner?.GetInt(MINION_UID_KEY) ?? 0;
            set => owner?.SetInt(MINION_UID_KEY, value);
        }

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
            int existingUid = SummonedMinionUid;
            if (existingUid != 0)
            {
                var existingMinion = EClass._map.FindChara(existingUid);
                if (existingMinion != null && !existingMinion.isDead)
                {
                    Debug.Log($"[SukutsuArena] Twin Mirror: Minion already exists (uid={existingUid})");
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

            // マスターの能力値をコピー（HP計算に必要）
            CopyMasterStats(shadow, master);

            // マスターの近くに配置
            Point spawnPoint = master.pos.GetNearestPoint(allowBlock: false, allowChara: false);
            if (spawnPoint == null || !spawnPoint.IsValid)
            {
                spawnPoint = master.pos;
            }

            // マップに追加（レンダラー初期化のため、外見コピーより前に行う）
            EClass._zone.AddCard(shadow, spawnPoint);

            // マスターの外見をコピー（マップ追加後に行う）
            CopyMasterAppearance(shadow, master);

            // ミニオンとして設定
            shadow.MakeMinion(master, MinionType.Default);

            // 召喚扱いにする（ゾーン移動時に消える）
            shadow.SetSummon(9999); // 非常に長い持続時間

            // UIDをカスタムデータに保存（セーブ対応）
            SummonedMinionUid = shadow.uid;

            // 演出
            master.PlaySound("spell_buff");
            shadow.PlayEffect("buff");

            // 名前を設定
            shadow.c_altName = $"影の{master.Name}";

            Msg.Say("sukutsu_twin_mirror_summon", master, shadow);
            Debug.Log($"[SukutsuArena] Summoned Shadow Self (uid={shadow.uid}, lv={shadow.LV}) for {master.Name}");
        }

        /// <summary>
        /// マスターの能力値を影にコピー
        /// </summary>
        private void CopyMasterStats(Chara shadow, Chara master)
        {
            try
            {
                // マスターの能力値（elements）を影にコピー
                master.elements.CopyTo(shadow.elements);
                Debug.Log($"[SukutsuArena] TwinMirror: Copied elements from master");

                // HPとMPをフル状態に設定
                shadow.hp = shadow.MaxHP;
                if (shadow.mana != null)
                {
                    shadow.mana.value = shadow.mana.max;
                }

                Debug.Log($"[SukutsuArena] TwinMirror: Shadow stats - HP={shadow.hp}/{shadow.MaxHP}, LV={shadow.LV}");
            }
            catch (System.Exception ex)
            {
                Debug.LogWarning($"[SukutsuArena] TwinMirror: Failed to copy stats: {ex.Message}");
            }
        }

        /// <summary>
        /// マスターの外見（PCC）を影にコピー
        /// </summary>
        private void CopyMasterAppearance(Chara shadow, Chara master)
        {
            Debug.Log($"[SukutsuArena] TwinMirror: Copying master appearance to shadow...");

            try
            {
                // PCCデータをディープコピー（参照コピーだとちらつきの原因になる）
                if (master.pccData != null)
                {
                    shadow.pccData = new PCCData();
                    shadow.pccData.Set(master.pccData);
                    Debug.Log($"[SukutsuArena] TwinMirror: Deep copied pccData");
                }

                // 生物学的情報をコピー
                if (master.bio != null && shadow.bio != null)
                {
                    shadow.bio.SetGender(master.bio.gender);
                    shadow.bio.height = master.bio.height;
                    shadow.bio.weight = master.bio.weight;
                    Debug.Log($"[SukutsuArena] TwinMirror: Copied bio data (gender={master.bio.gender})");
                }

                // スキンIDをコピー
                shadow.idSkin = master.idSkin;

                // レンダラーを再作成（バニラのtogglePCC処理と同様）
                bool wasSynced = shadow.isSynced;
                if (wasSynced && shadow.renderer != null)
                {
                    shadow.renderer.OnLeaveScreen();
                    EClass.scene.syncList.Remove(shadow.renderer);
                }

                // レンダラー再作成
                shadow._CreateRenderer();

                if (wasSynced && shadow.renderer != null)
                {
                    EClass.scene.syncList.Add(shadow.renderer);
                    shadow.renderer.OnEnterScreen();
                }

                Debug.Log($"[SukutsuArena] TwinMirror: Recreated renderer for shadow");
            }
            catch (System.Exception ex)
            {
                Debug.LogWarning($"[SukutsuArena] TwinMirror: Failed to copy appearance: {ex.Message}");
            }
        }

        /// <summary>
        /// 影の自己を解散
        /// </summary>
        private void DismissShadowSelf()
        {
            int minionUid = SummonedMinionUid;
            if (minionUid == 0) return;

            var minion = EClass._map?.FindChara(minionUid);
            if (minion != null && !minion.isDead)
            {
                // 演出
                minion.PlayEffect("vanish");
                minion.PlaySound("identify");

                Msg.Say("sukutsu_twin_mirror_dismiss", minion);

                // 削除
                minion.Destroy();
                Debug.Log($"[SukutsuArena] Dismissed Shadow Self (uid={minionUid})");
            }

            SummonedMinionUid = 0;
        }
    }
}
