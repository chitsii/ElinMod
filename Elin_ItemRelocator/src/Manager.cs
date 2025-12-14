using System;
using System.Collections.Generic;
using System.IO;
using Newtonsoft.Json;
using UnityEngine;
using System.Linq;

namespace Elin_ItemRelocator
{
    public class RelocatorManager : Singleton<RelocatorManager>
    {
        public Dictionary<string, RelocationProfile> Profiles = new Dictionary<string, RelocationProfile>();

        // Path to Presets folder inside the Mod's folder
        private string PresetPath
        {
            get
            {
                 // Assuming DLL is in plugins/Elin_ItemRelocator/
                 // We want plugins/Elin_ItemRelocator/Presets/
                 string pluginPath = Path.GetDirectoryName(System.Reflection.Assembly.GetExecutingAssembly().Location);
                 // If the DLL is in _bin or similar during dev, adjust. But usually safe to use relative.
                 // Let's ensure directory exists.
                 string dir = Path.Combine(pluginPath, "Presets");
                 if (!Directory.Exists(dir)) Directory.CreateDirectory(dir);
                 return dir;
            }
        }

        public void Init()
        {
            // No persistent load on init anymore
        }

        // Runtime-only profile retrieval
        public RelocationProfile GetProfile(Thing container)
        {
            if (container == null) return new RelocationProfile(); // Safe fallback

            string key = GetProfileKey(container);

            RelocationProfile profile;
            if (Profiles.TryGetValue(key, out profile))
            {
                return profile;
            }

            var newProfile = new RelocationProfile { ContainerName = container.Name };
            Profiles[key] = newProfile;
            return newProfile;
        }

        public void SavePreset(string name, RelocationProfile profile)
        {
            try
            {
                string path = Path.Combine(PresetPath, name + ".json");
                string json = JsonConvert.SerializeObject(profile, Formatting.Indented);
                File.WriteAllText(path, json);
                Msg.Say(string.Format(RelocatorLang.GetText(RelocatorLang.LangKey.Msg_Saved), name));
            }
            catch (Exception e)
            {
                 Debug.LogError("[Elin_ItemRelocator] Failed to save preset: " + e);
                 Msg.Say("Error saving preset.");
            }
        }

        public RelocationProfile LoadPreset(string name)
        {
             try
             {
                 string path = Path.Combine(PresetPath, name + ".json");
                 if (File.Exists(path))
                 {
                     string json = File.ReadAllText(path);
                     return JsonConvert.DeserializeObject<RelocationProfile>(json);
                 }
             }
             catch (Exception e)
             {
                 Debug.LogError("[Elin_ItemRelocator] Failed to load preset: " + e);
                 Msg.Say("Error loading preset.");
             }
             return null;
        }

        public List<string> GetPresetList()
        {
            List<string> list = new List<string>();
            try
            {
                if (Directory.Exists(PresetPath))
                {
                    foreach (string file in Directory.GetFiles(PresetPath, "*.json"))
                    {
                        list.Add(Path.GetFileNameWithoutExtension(file));
                    }
                }
            }
            catch { }
            return list;
        }

        public void RenamePreset(string oldName, string newName)
        {
            try
            {
                string oldPath = Path.Combine(PresetPath, oldName + ".json");
                string newPath = Path.Combine(PresetPath, newName + ".json");

                if (!File.Exists(oldPath)) return;

                if (File.Exists(newPath))
                {
                    Msg.Say(RelocatorLang.GetText(RelocatorLang.LangKey.Msg_FileExists));
                    return;
                }

                File.Move(oldPath, newPath);
                Msg.Say(string.Format(RelocatorLang.GetText(RelocatorLang.LangKey.Msg_Renamed), newName));
            }
            catch (Exception e)
            {
                Debug.LogError("[Elin_ItemRelocator] Failed to rename: " + e);
            }
        }

        public void DeletePreset(string name)
        {
            try
            {
                string path = Path.Combine(PresetPath, name + ".json");
                if (File.Exists(path))
                {
                    File.Delete(path);
                    Msg.Say(string.Format(RelocatorLang.GetText(RelocatorLang.LangKey.Msg_Deleted), name));
                }
            }
            catch (Exception e)
            {
                Debug.LogError("[Elin_ItemRelocator] Failed to delete: " + e);
            }
        }

        public string GetProfileKey(Thing container)
        {
            if (container == null) return null;
            return string.Format("{0}_{1}", Game.id, container.uid);
        }

        public IEnumerable<Thing> GetMatches(Thing container)
        {
            var profile = GetProfile(container);
            if (profile == null || !profile.Enabled) return new List<Thing>();

            // Determine search scope and candidates
            HashSet<Thing> hotbarItems = new HashSet<Thing>();
            foreach(var bar in EClass.player.hotbars.bars)
            {
                if(bar == null) continue;
                foreach(var page in bar.pages)
                {
                    foreach(var item in page.items)
                    {
                        if(item != null && item.Thing != null)
                        {
                            hotbarItems.Add(item.Thing);
                        }
                    }
                }
            }

            List<Thing> matches = new List<Thing>();

            // Helper to check and add
            Action<Thing> checkAndAdd = (t) => {
                // Performance Limit: Stop if we have enough matches (e.g. 100)
                // Most containers are small (< 50), so 100 is plenty safe.
                if (matches.Count >= 100) return;

                // 1. Exclude self and its contents
                if (t == container) return;
                if (t.parent == container.things) return;

                // 2. Skip Player Important items
                if (t.c_isImportant) return;

                // 3. Exclude non-empty containers
                if (t.IsContainer && t.things.Count > 0) return;

                // 4. Exclude installed furniture (Zone scope)
                if (t.placeState == PlaceState.installed) return;

                // 5. Exclude non-holdable items
                if (!t.trait.CanBeHeld) return;

                // 6. Exclude Equipped Items
                if (t.isEquipped) return;

                // 8. Exclude Hotbar Items
                if (profile.ExcludeHotbar && hotbarItems.Contains(t)) return;

                // Important Logic: If destroyed, skip
                if (t.isDestroyed) return;

                // Check Filters
                if (profile.Filters.Count == 0) return; // Safe: Do not relocate anything if no conditions are set

                if (profile.Filters.Count > 0)
                {
                    bool match = true; // Default to true for AND logic
                    foreach(var filter in profile.Filters)
                    {
                        if (!filter.IsMatch(t)) // If ANY filter fails, reject
                        {
                            match = false;
                            break;
                        }
                    }
                    if (!match) return; // Skip if didn't match all
                }

                matches.Add(t);
            };

            // Layer 1: PC Inventory (Recursive Layer 2)
            foreach(var t in EClass.pc.things)
            {
                checkAndAdd(t);

                // Layer 2: Inside Containers
                if (t.IsContainer && t.things != null && t.things.Count > 0)
                {
                    foreach(var child in t.things)
                    {
                        checkAndAdd(child);
                    }
                }
            }

            // Layer : Equipped Containers (Toolbelt, Backpack, etc)
            // Items in equipped containers are NOT in pc.things, so we must scan body slots.
            // User requested "Toolbelt Exclusion" to mean "Body Slot Exclusion".
            // So if ExcludeHotbar is ON, we skip this entirely.
            if (!profile.ExcludeHotbar)
            {
                foreach(var slot in EClass.pc.body.slots)
                {
                    if (slot.thing == null || !slot.thing.IsContainer || slot.thing.things.Count == 0) continue;

                    // Scan contents of equipped container
                    foreach(var t in slot.thing.things)
                    {
                         checkAndAdd(t);

                         // Recurse one level deep (e.g. Bag inside Toolbelt)
                         if (t.IsContainer && t.things != null && t.things.Count > 0)
                         {
                             foreach(var child in t.things)
                             {
                                 checkAndAdd(child);
                             }
                         }
                    }
                }
            }

            // Zone Scope
            if (profile.Scope == RelocationProfile.FilterScope.Zone)
            {
                foreach(var t in EClass._map.things)
                {
                    checkAndAdd(t);
                }
            }

            // Apply Sorting
            switch (profile.SortMode)
            {
                case RelocationProfile.ResultSortMode.PriceAsc:
                    matches.Sort((a, b) => a.GetPrice() - b.GetPrice());
                    break;
                case RelocationProfile.ResultSortMode.PriceDesc:
                    matches.Sort((a, b) => b.GetPrice() - a.GetPrice());
                    break;
                case RelocationProfile.ResultSortMode.EnchantMagAsc:
                case RelocationProfile.ResultSortMode.EnchantMagDesc:
                    // Identify target element IDs from filters
                    List<int> targetEleIds = new List<int>();
                    foreach(var f in profile.Filters) {
                        if (f.Enabled && !string.IsNullOrEmpty(f.Text)) {
                            string[] searchTerms = f.Text.Split(new char[]{' ', '　'}, StringSplitOptions.RemoveEmptyEntries);
                            foreach(var term in searchTerms) {
                                if (term.StartsWith("@")) {
                                    // Parse term: @Mining>=10 -> Mining
                                    // Handle logic similar to EvaluateAttribute
                                    string key = term.Substring(1);
                                    // Strip operators
                                    string[] ops = new string[]{ ">=", "<=", "!=", ">", "<", "=" };
                                    foreach(var o in ops) {
                                        int idx = key.IndexOf(o);
                                        if (idx > 0) { key = key.Substring(0, idx).Trim(); break; }
                                    }

                                    var sourceEle = EClass.sources.elements.map.Values.FirstOrDefault(e =>
                                        (e.alias != null && e.alias.Equals(key, StringComparison.OrdinalIgnoreCase)) ||
                                        (e.GetName().Equals(key, StringComparison.OrdinalIgnoreCase))
                                    );
                                    if(sourceEle != null) targetEleIds.Add(sourceEle.id);
                                }
                            }
                        }
                    }

                    // Sort Function
                    matches.Sort((a, b) => {
                        int valA = 0;
                        int valB = 0;
                        foreach(int id in targetEleIds) {
                            valA += a.elements.Value(id);
                            valB += b.elements.Value(id);
                        }
                        if (profile.SortMode == RelocationProfile.ResultSortMode.EnchantMagDesc)
                            return valB - valA;
                        else
                            return valA - valB;
                    });
                    break;
            }

            return matches;
        }

        public void ExecuteRelocation(Thing container)
        {
             var matches = GetMatches(container);
             int count = 0;

             foreach (var t in matches)
             {
                 // Double check state
                 if (t.isDestroyed || t.c_isImportant || t.placeState == PlaceState.installed) continue;

                 if (container.things.IsFull())
                 {
                     Msg.Say(RelocatorLang.GetText(RelocatorLang.LangKey.Msg_ContainerFull));
                     break;
                 }

                 container.AddThing(t);
                 count++;
             }

             if (count > 0)
             {
                 EClass.pc.PlaySound("grab");
                 Msg.Say(string.Format(RelocatorLang.GetText(RelocatorLang.LangKey.Msg_RelocatedResult), count, container.Name));
             }
             else
             {
                 Msg.Say(RelocatorLang.GetText(RelocatorLang.LangKey.Msg_NoMatchLog));
             }
        }

        public void RelocateSingleThing(Thing t, Thing container)
        {
             if (t.isDestroyed || t.c_isImportant) return;
             if (container.things.IsFull()) {
                 Msg.Say(RelocatorLang.GetText(RelocatorLang.LangKey.Msg_ContainerFull));
                 return;
             }

             container.AddThing(t);
             EClass.pc.PlaySound("grab");
             Msg.Say(string.Format(RelocatorLang.GetText(RelocatorLang.LangKey.Msg_Moved), t.Name));
        }
    }
}
