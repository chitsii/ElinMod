using System;
using System.Collections.Generic;
using System.IO;
using Newtonsoft.Json;
using UnityEngine;
using System.Linq;

namespace Elin_ItemRelocator {
    public class RelocatorManager : Singleton<RelocatorManager> {
        public Dictionary<string, RelocationProfile> Profiles = [];

        // Path to Presets folder inside the Mod's folder
        private string PresetPath {
            get {
                // Assuming DLL is in plugins/Elin_ItemRelocator/
                // We want plugins/Elin_ItemRelocator/Presets/
                string pluginPath = Path.GetDirectoryName(System.Reflection.Assembly.GetExecutingAssembly().Location);
                // If the DLL is in _bin or similar during dev, adjust. But usually safe to use relative.
                // Let's ensure directory exists.
                string dir = Path.Combine(pluginPath, "Presets");
                if (!Directory.Exists(dir))
                    Directory.CreateDirectory(dir);
                return dir;
            }
        }

        public void Init() {
            // No persistent load on init anymore
        }

        // Runtime-only profile retrieval
        public RelocationProfile GetProfile(Thing container) {
            if (container is null)
                return new(); // Safe fallback

            string key = GetProfileKey(container);

            if (Profiles.TryGetValue(key, out var profile)) {
                return profile;
            }

            var newProfile = new RelocationProfile { ContainerName = container.Name };
            Profiles[key] = newProfile;
            return newProfile;
        }

        public void SavePreset(string name, RelocationProfile profile) {
            try {
                string path = Path.Combine(PresetPath, name + ".json");
                string json = JsonConvert.SerializeObject(profile, Formatting.Indented);
                File.WriteAllText(path, json);
                Msg.Say(string.Format(RelocatorLang.GetText(RelocatorLang.LangKey.Msg_Saved), name));
            } catch (Exception e) {
                Debug.LogError("[Elin_ItemRelocator] Failed to save preset: " + e);
                Msg.Say("Error saving preset.");
            }
        }

        public RelocationProfile LoadPreset(string name) {
            try {
                string path = Path.Combine(PresetPath, name + ".json");
                if (File.Exists(path)) {
                    string json = File.ReadAllText(path);
                    return JsonConvert.DeserializeObject<RelocationProfile>(json);
                }
            } catch (Exception e) {
                Debug.LogError("[Elin_ItemRelocator] Failed to load preset: " + e);
                Msg.Say("Error loading preset.");
            }
            return null;
        }

        public List<string> GetPresetList() {
            List<string> list = [];
            try {
                if (Directory.Exists(PresetPath)) {
                    var files = new DirectoryInfo(PresetPath).GetFiles("*.json");
                    // Sort by CreationTime ascending (Oldest first, newest last)
                    foreach (var file in files.OrderBy(f => f.CreationTime)) {
                        list.Add(Path.GetFileNameWithoutExtension(file.Name));
                    }
                }
            } catch { }
            return list;
        }

        public void RenamePreset(string oldName, string newName) {
            try {
                string oldPath = Path.Combine(PresetPath, oldName + ".json");
                string newPath = Path.Combine(PresetPath, newName + ".json");

                if (!File.Exists(oldPath))
                    return;

                if (File.Exists(newPath)) {
                    Msg.Say(RelocatorLang.GetText(RelocatorLang.LangKey.Msg_FileExists));
                    return;
                }

                File.Move(oldPath, newPath);
                Msg.Say(string.Format(RelocatorLang.GetText(RelocatorLang.LangKey.Msg_Renamed), newName));
            } catch (Exception e) {
                Debug.LogError("[Elin_ItemRelocator] Failed to rename: " + e);
            }
        }

        public void DeletePreset(string name) {
            try {
                string path = Path.Combine(PresetPath, name + ".json");
                if (File.Exists(path)) {
                    File.Delete(path);
                    Msg.Say(string.Format(RelocatorLang.GetText(RelocatorLang.LangKey.Msg_Deleted), name));
                }
            } catch (Exception e) {
                Debug.LogError("[Elin_ItemRelocator] Failed to delete: " + e);
            }
        }

        public string GetProfileKey(Thing container) {
            if (container is null)
                return null;
            return string.Format("{0}_{1}", Game.id, container.uid);
        }

        private List<Thing> cachedCandidates;


        public void BuildCache(RelocationProfile profile, Thing container) {
            // Master Cache Strategy:
            // ALWAYS gather candidates as if Scope is 'Both' (Inventory + Zone)
            // This allows us to switch scopes dynamically without rebuilding cache.

            // Note: GatherCandidates ignores 'profile.Scope' if we manually aggregate?
            // GatherCandidates uses profile.Scope internally! We must trick it or manually call.

            // Manually gather BOTH scopes
            HashSet<Thing> raw = [];

            // 1. Inventory
            // Actually, GatherCandidates implementation (not shown yet) likely depends on profile.
            // Let's implement GatherCandidates logic directly or assume we can pass a modified profile.
            // Modifying profile is risky if referenced elsewhere.
            // Let's create a temp profile copy or just call GatherCandidates twice?

            // Simplified: GatherCandidates iterates based on Scope.
            // We want 'Both', and we want to include hotbar/equipped items initially (filtered later).
            var tempProfile = new RelocationProfile() {
                Scope = RelocationProfile.FilterScope.Both
            };
            var allCandidates = GatherCandidates(tempProfile, container);

            cachedCandidates = new List<Thing>();
            var seen = new HashSet<Thing>();
            foreach (var t in allCandidates) {
                if (!seen.Add(t))
                    continue;
                // Use comprehensive game logic validation
                if (IsRelocatableCandidate(t, container)) {
                    cachedCandidates.Add(t);
                }
            }
            // Hotbar items are INCLUDED in cache (filtered dynamic)
        }

        public void ClearCache() {
            cachedCandidates = null;
        }

        public IEnumerable<Thing> GetMatches(Thing container, int searchLimit = -1) {
            var profile = GetProfile(container);
            if (profile is null || !profile.Enabled)
                return [];

            // Ensure Cache Exists
            if (cachedCandidates == null) {
                BuildCache(profile, container);
            }

            // Identify Hotbar Items (Dynamic Calculation or Cache?)
            // If checking every frame, calculating hotbar set is cheap enough (few items).
            HashSet<Thing> hotbarItems = [];
            // Always calculate to ensure safety even if hotbar changes.
            foreach (var bar in EClass.player.hotbars.bars) {
                if (bar is null)
                    continue;
                foreach (var page in bar.pages) {
                    foreach (var item in page.items) {
                        if (item is { Thing: not null })
                            hotbarItems.Add(item.Thing);
                    }
                }
            }

            List<Thing> matches = [];

            // Iterate Master Cache
            foreach (var t in cachedCandidates) {
                // Dynamic Filter 1: Scope
                // Check if t belongs to Inventory or Zone based on profile.Scope
                // Actually t.Root works well.
                // Inventory items: Root is PC's thing container.
                // Zone items: Root is Zone's map thing container/floor?

                // Let's use simpler check:
                // GatherCandidates logic for Inventory uses 'EClass.pc.things'.
                // GatherCandidates logic for Zone uses 'EClass._map.things'.

                // If profile.Scope is Inventory, we need to verify t is in Inventory.
                // If profile.Scope is Zone, verify t is in Zone.
                // If Both, accept all.

                if (profile.Scope == RelocationProfile.FilterScope.Inventory) {
                    if (!IsPCOwned(t))
                        continue;
                } else if (profile.Scope == RelocationProfile.FilterScope.ZoneOnly) {
                    if (IsPCOwned(t))
                        continue;
                }

                // Dynamic Filter 2: Hotbar (Always Protect Parents)
                if (hotbarItems.Contains(t))
                    continue;

                // Dynamic Filter 3: Rules
                // Performance Limit Check (Pre-rule or Post-rule? Usually Post-match)
                if (searchLimit > 0 && matches.Count >= searchLimit)
                    break;

                // Rule Check
                if (profile.Rules.Count == 0)
                    continue;

                bool match = false;
                foreach (var rule in profile.Rules) {
                    if (rule.IsMatch(t)) {
                        match = true;
                        break;
                    }
                }
                if (match)
                    matches.Add(t);
            }

            // Apply Sorting
            switch (profile.SortMode) {
            case RelocationProfile.ResultSortMode.PriceAsc:
                matches.Sort((a, b) => a.GetPrice() - b.GetPrice());
                break;
            case RelocationProfile.ResultSortMode.PriceDesc:
                matches.Sort((a, b) => b.GetPrice() - a.GetPrice());
                break;
            case RelocationProfile.ResultSortMode.TotalEnchantMagDesc:
                matches.Sort((a, b) => {
                    // Check common properties first to avoid calculation if possible? No, sockets are small list.
                    // Just sum up
                    int valA = 0;
                    if (a.elements != null && a.elements.dict != null) {
                        foreach (var e in a.elements.dict.Values) {
                            if (e.Value > 0) // Exclude skills linking to attributes to avoid double counting? No, keep simple.
                                valA += e.Value;
                        }
                    }

                    int valB = 0;
                    if (b.elements != null && b.elements.dict != null) {
                        foreach (var e in b.elements.dict.Values) {
                            if (e.Value > 0)
                                valB += e.Value;
                        }
                    }
                    return valB - valA;
                });
                break;

            case RelocationProfile.ResultSortMode.EnchantMagAsc:
            case RelocationProfile.ResultSortMode.EnchantMagDesc:
                // Identify target element IDs from rules
                List<int> targetEleIds = GetTargetEnchantIDs(profile);

                // Sort Function
                matches.Sort((a, b) => {
                    int valA = 0;
                    int valB = 0;
                    foreach (int id in targetEleIds) {
                        valA += a.elements.Value(id);
                        valB += b.elements.Value(id);
                    }
                    if (profile.SortMode == RelocationProfile.ResultSortMode.EnchantMagDesc)
                        return valB - valA;
                    else
                        return valA - valB;
                });
                break;
            case RelocationProfile.ResultSortMode.TotalWeightAsc:
                matches.Sort((a, b) => (a.ChildrenAndSelfWeight * a.Num) - (b.ChildrenAndSelfWeight * b.Num));
                break;
            case RelocationProfile.ResultSortMode.TotalWeightDesc:
                matches.Sort((a, b) => (b.ChildrenAndSelfWeight * b.Num) - (a.ChildrenAndSelfWeight * a.Num));
                break;
            case RelocationProfile.ResultSortMode.UnitWeightAsc:
                matches.Sort((a, b) => a.SelfWeight - b.SelfWeight);
                break;
            case RelocationProfile.ResultSortMode.UnitWeightDesc:
                matches.Sort((a, b) => b.SelfWeight - a.SelfWeight);
                break;
            case RelocationProfile.ResultSortMode.UidAsc:
                matches.Sort((a, b) => a.uid - b.uid);
                break;
            case RelocationProfile.ResultSortMode.UidDesc:
                matches.Sort((a, b) => b.uid - a.uid);
                break;
            case RelocationProfile.ResultSortMode.GenLvlAsc:
                matches.Sort((a, b) => a.genLv - b.genLv);
                break;
            case RelocationProfile.ResultSortMode.GenLvlDesc:
                matches.Sort((a, b) => b.genLv - a.genLv);
                break;
            }

            return matches;
        }

        // Helper to determine if a container is owned by PC (Inventory)
        public bool IsPCOwned(Thing t) {
            if (t == null)
                return false;
            // Use rigorous game API: GetRootCard()
            // If the root owner is the PC, it is in player inventory.
            return t.GetRootCard() == EClass.pc;
        }

        public bool IsRelocatableCandidate(Thing t, Thing container) {
            // Basic Static Checks
            if (t.isDestroyed || t.c_lockedHard)
                return false;
            if (t.c_isImportant)
                return false;
            if (t.placeState == PlaceState.installed)
                return false;

            // CRITICAL SAFETY: Prevent moving the Toolbelt itself (which might be in inventory/slots)
            // Moving internal/system containers can corrupt save data.
            if (t.trait is TraitToolBelt)
                return false;

            // -- Game Logic Checks (InvOwner.cs) --
            bool destIsPC = IsPCOwned(container);

            // 1. Toolbelt check (InvOwner.cs:359)
            if (container.trait is TraitToolBelt)
                return false;

            // 2. Guide check (Skip)

            // 3. Lock check (InvOwner.cs:367)
            if (container.c_lockLv != 0)
                return false;

            // 4. Ability check (InvOwner.cs:371)
            // "Skills cannot be put in shipping bin" (Ability -> Non-PC)
            if (t.trait is TraitAbility && !destIsPC)
                return false;

            // 5. AllowTransfer check (InvOwner.cs:379)
            if (container.isNPCProperty)
                return false;

            // 6. Non-empty Container check (InvOwner.cs:383)
            if (t.IsContainer && t.things.Count > 0 && !destIsPC)
                return false;

            // 7. AllowHold Logic (InvOwner.cs:639)
            if (!t.trait.CanBeDropped)
                return false;
            if (t.isEquipped && t.IsCursed)
                return false;

            // Destination is NOT PC checks
            if (!destIsPC) {
                if (t.id == "money")
                    return false;
                if (t.isGifted || t.isNPCProperty)
                    return false;
            }

            return true;
        }

        public List<int> GetTargetEnchantIDs(RelocationProfile profile) {
            List<int> targetEleIds = [];
            foreach (var r in profile.Rules) {
                if (r.Enabled && r.Enchants != null) {
                    foreach (var term in r.Enchants) {
                        if (string.IsNullOrEmpty(term))
                            continue;

                        // Term format is typically "@Key" or "@Key>=Value"
                        // Key can be Alias or Name
                        string key = term.TrimStart('@');

                        // Strip operators to isolate key
                        string[] ops = [">=", "<=", "!=", ">", "<", "="];
                        foreach (var o in ops) {
                            int idx = key.IndexOf(o);
                            if (idx > 0) { key = key.Substring(0, idx).Trim(); break; }
                        }

                        // Match against Element Name or Alias
                        var sourceEle = EClass.sources.elements.map.Values.FirstOrDefault(e =>
                            (e.alias is not null && e.alias.Equals(key, StringComparison.OrdinalIgnoreCase)) ||
                            (e.GetName().Equals(key, StringComparison.OrdinalIgnoreCase))
                        );
                        if (sourceEle is not null && !targetEleIds.Contains(sourceEle.id))
                            targetEleIds.Add(sourceEle.id);
                    }
                }
            }
            return targetEleIds;
        }





        public void ExecuteRelocation(Thing container) {
            // Unlimited search for execution
            var matches = GetMatches(container, -1).ToList();
            int count = 0;

            foreach (var t in matches) {
                // Double check state
                if (t.isDestroyed || t.c_isImportant || t.placeState == PlaceState.installed)
                    continue;

                if (container.things.IsFull()) {
                    Msg.Say(RelocatorLang.GetText(RelocatorLang.LangKey.Msg_ContainerFull));
                    break;
                }

                container.AddThing(t);
                count++;
            }

            if (count > 0) {
                EClass.pc.PlaySound("grab");
                Msg.Say(string.Format(RelocatorLang.GetText(RelocatorLang.LangKey.Msg_RelocatedResult), count, container.Name));
            } else {
                Msg.Say(RelocatorLang.GetText(RelocatorLang.LangKey.Msg_NoMatchLog));
            }
        }

        public void RelocateSingleThing(Thing t, Thing container) {
            if (t.isDestroyed || t.c_isImportant)
                return;

            // Safety Check
            if (!IsRelocatableCandidate(t, container)) {
                EClass.pc.PlaySound("beep");
                return;
            }

            if (container.things.IsFull()) {
                Msg.Say(RelocatorLang.GetText(RelocatorLang.LangKey.Msg_ContainerFull));
                return;
            }

            container.AddThing(t);
            EClass.pc.PlaySound("grab");
            Msg.Say(string.Format(RelocatorLang.GetText(RelocatorLang.LangKey.Msg_Moved), t.Name));
        }

        private IEnumerable<Thing> GatherCandidates(RelocationProfile profile, Thing container) {
            // Inventory Scope
            if (profile.Scope != RelocationProfile.FilterScope.ZoneOnly) {
                foreach (var t in EClass.pc.things) {
                    if (t == container)
                        continue;
                    yield return t;

                    if (t.IsContainer && t.things is { Count: > 0 }) {
                        foreach (var child in t.things) {
                            if (child == container)
                                continue;
                            yield return child;
                        }
                    }
                }

                // Hotbar items are referenced in body slots or inventory
                foreach (var slot in EClass.pc.body.slots) {
                    if (slot.thing is null || !slot.thing.IsContainer || slot.thing.things.Count == 0)
                        continue;
                    if (slot.thing == container)
                        continue;

                    foreach (var t in slot.thing.things) {
                        if (t == container)
                            continue;
                        yield return t;

                        if (t.IsContainer && t.things is { Count: > 0 }) {
                            foreach (var child in t.things) {
                                if (child == container)
                                    continue;
                                yield return child;
                            }
                        }
                    }
                }
            }

            // Zone Scope
            if (profile.Scope is RelocationProfile.FilterScope.Both or RelocationProfile.FilterScope.ZoneOnly) {
                foreach (var t in EClass._map.things) {
                    if (t == container)
                        continue;
                    yield return t;

                    // Recurse into installed containers
                    if (t.placeState == PlaceState.installed && t.IsContainer && t.things is { Count: > 0 }) {
                        foreach (var child in t.things) {
                            if (child == container)
                                continue;
                            yield return child;
                        }
                    }
                }
            }
        }
    }
}
