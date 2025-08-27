using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Xml.Linq;

using HarmonyLib;
using UnityEngine;

using static ActPlan;

namespace Elin_Mod
{
	[HarmonyPatch]
	public class NewRangedModManager : Singleton<NewRangedModManager>
	{
		const string c_ElemName_ElemIDStart = "itukiyu_modEX_IDStart";
		const string c_ElemName_ElemIDEnd = "itukiyu_modEX_IDEnd";
		const string c_ElemName_ElemIDStartOld = "itukiyu_modEX_IDStartOld";
		const string c_ElemName_ElemIDEndOld = "itukiyu_modEX_IDEndOld";

		public int ElemIDStart { get; private set; } = 0;
		public int ElemIDEnd { get; private set; } = 0;


		public int ElemIDStartOld { get; private set; } = 0;
		public int ElemIDEndOld { get; private set; } = 0;



		int[] m_ElemIndexToAliasHashes;
		int[] m_ElemIndexToIDs;

		Dictionary<int,SourceElement.Row> m_NewModElemRows;
		NewRangedModBase[] m_NewMods;







		public void OnStartCore() {
			m_NewMods = new NewRangedModBase[] {
				new NewRangedMod_Elements(),
				new NewRangedMod_Barrel()
			};
			
			// データ読み込み.
			var elems = EClass.sources.elements;
			var elemsMap = elems.map;
			SourceElementNew elemNews = ScriptableObject.CreateInstance<SourceElementNew>();
			ModUtil.ImportExcel(CommonUtil.GetResourcePath("tables/add_datas.xlsx"), "elements", elemNews);
			
			foreach ( var itr in elemNews.map) {
				SourceElement.Row tmp = null;
				if ( elemsMap.TryGetValue( itr.Key, out tmp )) {
					DebugUtil.LogError( $"[Elin_ExGunMods] conflict element elemID!!!! --> elemID={itr.Key}  baseName={tmp.name}  newModName={itr.Value.name} " );
					continue;
				}

				elems.rows.Add(itr.Value);
			}
		}

		/// <summary>
		/// ゲーム開始直前に呼ばれる.
		/// </summary>
		public void OnLoadTableAfter() {
			// SourceManager::Init()後の処理はここ.
			// ゲーム中の全Elementのハッシュテーブルを作っておく.
			var elems = EClass.sources.elements;
			var elemsMap = elems.map;
			m_ElemIndexToAliasHashes = new int[elemsMap.Count];
			m_ElemIndexToIDs = new int[elemsMap.Count];
			int idx = 0;
			foreach (var itr in elemsMap) {
				m_ElemIndexToAliasHashes[idx] = itr.Value.alias.GetHashCode();
				m_ElemIndexToIDs[idx] = itr.Value.id;
				++idx;
			}

			// 追加パーツ群の管理.
			ElemIDStart = GetElement(c_ElemName_ElemIDStart).id;
			ElemIDEnd = GetElement(c_ElemName_ElemIDEnd).id;
			ElemIDStartOld = GetElement(c_ElemName_ElemIDStartOld).id;
			ElemIDEndOld = GetElement(c_ElemName_ElemIDEndOld).id;
			m_NewModElemRows = new Dictionary<int, SourceElement.Row>();
			foreach (var itr in elemsMap) {
				if (itr.Key < ElemIDStart)
					continue;
				if (itr.Key > ElemIDEnd)
					continue;
				m_NewModElemRows.Add(itr.Key, itr.Value);
			}

			foreach (var itr in m_NewMods)
				itr.Initialize();
		}


		public SourceElement.Row GetElement( string alias ) {
			int searchHash = alias.GetHashCode();
			int idx = 0;
			foreach ( var itr in EClass.sources.elements.map ) {
				if (m_ElemIndexToAliasHashes[idx] == searchHash ) {
					return itr.Value;
				}
				++idx;
			}
			return null;
		}

		public SourceElement.Row GetElement( int id ) {
			return EClass.sources.elements.map[id];
		}

		public bool IsNewRangeModIDBand( int id ) {
			if (id < ElemIDStart)
				return false;
			if (id > ElemIDEnd)
				return false;
			return true;
		}

		public bool IsNewRangeModID( int id ) {
			if (!IsNewRangeModIDBand(id))
				return false;
			return m_NewModElemRows.ContainsKey(id);
		}

		public static int ElemToSocketData( int id, int lv ) {
			return id * 1000 + lv;
		}

		public static ( int id, int lv ) SocketDataToElem( long socketData ) {
			return ( (int)( socketData / 1000 ), (int)( socketData % 1000 ) );
		}

		public static (int id, int lv) SocketDataToElem(int socketData) {
			return SocketDataToElem((long)socketData);
		}


		public static long FixNewRangeSocketData(int rawSocketData) {
			// 2025/08/27追加.
			// オーバーフローIDを正しいIDに治す...
			if (rawSocketData > 0) {
				return rawSocketData;
			}

			uint asUnsigned = unchecked((uint)rawSocketData);
			ulong recovered = asUnsigned;
			return (long)recovered;
		}

		public static bool IsOldVerRangeElemID( int elemID ) {
			if (elemID < Instance.ElemIDStartOld || elemID > Instance.ElemIDEndOld) {
				return false;
			}
			return true;
		}

		public static int FixNewRangeElemID(int elemID) {
			if (!IsOldVerRangeElemID(elemID)) {
				return elemID;
			}
			string s = elemID.ToString();
			int idx = s.IndexOf("00");
			if (idx >= 0)
				s = s.Substring(0, idx) + "0" + s.Substring(idx + 2);
			int ret = 0;
			if (int.TryParse(s, out ret))
				elemID = ret;
			return elemID;
		}


		public bool Uninstall() {
			Exception eTmp = null;
			bool isError = false;
			try {
				// グローバルに登録されているカード群全てに対して削除要求していく.
				foreach (var itr in EClass.game.cards.globalCharas)
					_UninstallThings(itr.Value.things);

				// 全マップの配置物も漁っていく.
				foreach (var itr in EClass.game.spatials.map) {
					_UninstallSpatial(itr.Value);
				}
			}
			catch ( Exception e ) {
				isError = true;
				eTmp = e;
			}
			finally {
				if ( isError ) {
					var textMng = ModTextManager.Instance;
					var reportPath = CommonUtil.CreateErrorReport();
					textMng.SetUserData(0, reportPath);
					var bodyText = textMng.GetText(eTextID.Config_UninstallError);
					GameUtil.OpenDialog_1Button(bodyText, textMng.GetText(eTextID.Yes), () => {
						EClass.game.GotoTitle(false);
					});
				} else {
					EClass.game.Save(true);
				}
			}

			return !isError;
		}

		void _UninstallSpatial( Spatial spatial ) {
			try {
				var zone = spatial as Zone;
				if (zone != null) {
					var things = zone?.map?.things;
					if (things != null) {
						for (int i = 0; i < things.Count; ++i) {
							_UninstallThing(things[i]);
						}
					}
				}

				foreach (var child in spatial.children)
					_UninstallSpatial(child);
			}
			catch ( Exception e) {
				throw e;
			}
		}
		
		void _UninstallThings( ThingContainer things ) {
			if (things == null)
				return;
			try {
				for (int i = 0; i < things.Count; ++i) {
					var childs = things[i].things;
					_UninstallThings(childs);
					if (_UninstallThing(things[i]))
						--i;
				}
			} catch ( Exception e ) {
				throw e;
			}
		}

		bool _UninstallThing( Thing thing ) {
			if (thing == null)
				return false;
			if (thing.isDestroyed)
				return false;
			try {
				var mod = thing.trait as TraitModRanged;
				if (mod != null) {
					// こちらで追加したパーツだったら削除.
					bool isNewMod = m_NewModElemRows.ContainsKey(mod.source.id);
					if (isNewMod)
						thing.Destroy();
					return isNewMod;
				} else {
					// 装備かもしれないのでソケットとエンチャントを調べ、こちらの追加した物が入ってたら取り除く.
					foreach (var itr in m_NewModElemRows) {
						if (thing.sockets != null) {
							for (int i = 0; i < thing.sockets.Count; ++i) {
								var socketElem = SocketDataToElem(thing.sockets[i]);
								if (socketElem.id != itr.Key)
									continue;
								thing.elements?.ModBase(socketElem.id, -socketElem.lv);
								thing.sockets[i] = 0;
							}
						}

						// ModBaseで-lvしてるから必要ないか？.
						var elem = thing.elements?.GetElement(itr.Key);
						if (elem == null)
							continue;
						thing.elements?.Remove(itr.Key);
					}
					return false;
				}
			} catch ( Exception e) {
				throw e;
			}
		}




		// 保険処理.
		// バージョンアップでthingのelements.list に値が入っていないが、
		// ソケットには存在する、
		// というデータが発生した際のセーフティー処理.
		// セーブデータのロード時に該当のデータが存在したら強制的にelementを付与する.
		static List<int> s_TmpElementsListElemIDs;
		static List<(int,int)> s_TmpSocketElements;
		[HarmonyPatch(typeof(Card), "_OnDeserialized")]
		[HarmonyPostfix]
		public static void Postfix_OnDeserialized(Card __instance, StreamingContext context) {
			if (__instance == null)
				return;
			// 2025/08/27追加.
			// なにかの変更でsocketsの格納値が1000倍されるようになった.
			// そのせいでギリギリを攻めていたうちのID群がオーバーフローするようになった(最悪).
			// なのでセーブデータデシリアライズ時に古いIDと新しいIDを置き換えるように対処する.
			// 
			// いきなり1000掛けに治すのはまあ最悪良いとしてもですよ、大体もともとの設計でこういう正規化はボカァよくないと思うんですよ.
			// Mod推奨してるならせめてintじゃなくてlongとかにしようよ.
			

			// IDを差し替えたパーツ群の対処.
			// マジめんどい.
			var trait = __instance.trait as TraitMod;
			if (trait != null) {
				int old = __instance.refVal;
				__instance.refVal = FixNewRangeElemID(__instance.refVal);
				if ( old != __instance.refVal)
					DebugUtil.LogWarning($"!!! Convert TraitMod : {__instance.id} : {old} -> {__instance.refVal}");
			}

			// 以降はソケットにのみ対処.
			if (__instance.sockets == null || __instance.sockets.Count <= 0)
				return;
			if (__instance.elements == null || __instance.elements.list == null)
				return;
			if (s_TmpElementsListElemIDs == null) {
				s_TmpElementsListElemIDs = new List<int>(100);
				s_TmpSocketElements = new List<(int, int)>(100);
			}
			s_TmpSocketElements.Clear();

			// ソケット内のこちらで追加したパーツの情報を収集.
			for (int i = 0; i < __instance.sockets.Count; ++i) {
				if (__instance.sockets[i] == 0)
					continue;
				(int id, int lv) socketElem;

				// 2025/08/27追加.
				// オーバーフローしている古いソケットデータを置き換える.
				if (__instance.sockets[i] < 0 ) {
					var trueSocketData = FixNewRangeSocketData(__instance.sockets[i]);
					socketElem = SocketDataToElem(trueSocketData);
					if (IsOldVerRangeElemID(socketElem.id)) {
						// 他のModの溢れてるもんは知らん.
						int newElemID = FixNewRangeElemID(socketElem.id);

						// 古いのを全削除.
						var oldElem = __instance.elements.GetElement(socketElem.id);
						if (oldElem != null)
							__instance.elements.ModBase(socketElem.id, -socketElem.lv);
						var old = __instance.sockets[i];
						__instance.sockets[i] = ElemToSocketData(newElemID, socketElem.lv);

						DebugUtil.LogWarning($"!!! Convert RangeElement Data : {__instance.id} : {socketElem.id}, {old} --> {newElemID}, {__instance.sockets[i]}");
					}
				}

				socketElem = SocketDataToElem(__instance.sockets[i]);
				if (socketElem.id == 0)
					continue;

				if (!Instance.IsNewRangeModID(socketElem.id))
					continue;

				s_TmpSocketElements.Add(socketElem);
			}

			// 存在していないelementをチェック.
			ElementContainer elem = __instance.elements;
			if (elem.list != null) {
				s_TmpElementsListElemIDs.Clear();
				for (int i = 0; i < elem.list.Count; i += 5) {
					s_TmpElementsListElemIDs.Add(elem.list[i]);
				}
				for (int i = 0; i < s_TmpSocketElements.Count; ++i) {
					var socketElem = s_TmpSocketElements[i];
					// 2025/08/27追加.
					if (socketElem.Item1 < 0)
						continue;
					if (s_TmpElementsListElemIDs.Contains(socketElem.Item1))
						continue;
					// 存在していない場合はSetBaseで付与.
					DebugUtil.LogWarning($"[Warning!]Parts in socket are not included in elements.list  elemID={socketElem.Item1}");
					__instance.elements.SetBase(socketElem.Item1, socketElem.Item2);
				}
			}
			s_TmpSocketElements.Clear();
			s_TmpElementsListElemIDs.Clear();
		}


#if false
		[HarmonyPatch(typeof(Thing), "WriteNote")]
		[HarmonyPrefix]
		public static void Test(UINote n, Action<UINote> onWriteNote = null, IInspect.NoteMode mode = IInspect.NoteMode.Default, Recipe recipe = null, Thing __instance = null) {

			if (__instance.sockets != null) {
				foreach (int socket in __instance.sockets) {
					DebugUtil.LogError($"{__instance.id} : {socket} : {socket / 1000} : {socket % 1000}");
				}
			}
		}
#endif
	}
}
