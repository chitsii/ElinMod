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
        private string SavePath { get { return Path.Combine(CorePath.RootSave, "Elin_ItemRelocator_Data.json"); } }

        public void Init()
        {
            Load();
        }

        public void Load()
        {
            if (File.Exists(SavePath))
            {
                try
                {
                    string json = File.ReadAllText(SavePath);
                    Profiles = JsonConvert.DeserializeObject<Dictionary<string, RelocationProfile>>(json) ?? new Dictionary<string, RelocationProfile>();
                }
                catch (System.Exception e)
                {
                    Debug.LogError("[Elin_ItemRelocator] Failed to load profiles: " + e);
                }
            }
        }

        public void Save()
        {
            try
            {
                string json = JsonConvert.SerializeObject(Profiles, Formatting.Indented);
                File.WriteAllText(SavePath, json);
            }
            catch (System.Exception e)
            {
                Debug.LogError("[Elin_ItemRelocator] Failed to save profiles: " + e);
            }
        }

        public string GetProfileKey(Thing container)
        {
            if (container == null) return null;
            return string.Format("{0}_{1}", Game.id, container.uid);
        }

        public RelocationProfile GetProfile(Thing container)
        {
            string key = GetProfileKey(container);
            if (key == null) return null;

            RelocationProfile profile;
            if (Profiles.TryGetValue(key, out profile))
            {
                return profile;
            }

            var newProfile = new RelocationProfile { ContainerName = container.Name };
            Profiles[key] = newProfile;
            return newProfile;
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
                     Msg.Say("Container is full.");
                     break;
                 }

                 container.AddThing(t);
                 count++;
             }

             if (count > 0)
             {
                 EClass.pc.PlaySound("grab");
                 Msg.Say(string.Format("Relocated {0} stacks to {1}.", count, container.Name));
             }
             else
             {
                 Msg.Say("No matching items found.");
             }
        }
    }
}
