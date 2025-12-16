using System;
using System.Collections.Generic;
using UnityEngine;

namespace Elin_ItemRelocator {
    public enum ConditionType { None, Category, Rarity, Quality, Text, Id, AddButton, Settings, Weight, Material, Bless, Stolen, Enchant }

    public class FilterNode {
        public RelocationRule Rule;     // Level 1: Rule

        // Level 2: Condition Details
        public ConditionType CondType;
        public string CondValue; // ID or Text
        public string DisplayText;

        public bool IsRule { get { return Rule != null && CondType == ConditionType.None; } }
        public bool IsCondition { get { return CondType != ConditionType.None && CondType != ConditionType.AddButton && CondType != ConditionType.Settings; } }
        public bool IsAddButton { get { return CondType == ConditionType.AddButton; } }
        public bool IsSettings { get { return CondType == ConditionType.Settings; } }

        // Override Equals/GetHashCode for Persistence (Expansion State)
        public override bool Equals(object obj) {
            var other = obj as FilterNode;
            if (other == null)
                return false;
            if (IsRule && other.IsRule)
                return Rule == other.Rule; // Identity based on Rule instance
            return base.Equals(obj);
        }
        public override int GetHashCode() {
            if (IsRule)
                return Rule.GetHashCode();
            return base.GetHashCode();
        }
    }
}
