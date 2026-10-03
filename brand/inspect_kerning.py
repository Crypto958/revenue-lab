#!/usr/bin/env python3
"""Inspect Inter's own designed kerning for the wordmark pairs.

Hand-guessed kerning is a guess. Inter's type designer already optimised these
pairs, so read the real values and only override where a wordmark specifically
needs it.
"""
from fontTools.ttLib import TTFont

F = "brand/fonts/inter-extract/extras/ttf/Inter-SemiBold.ttf"
font = TTFont(F)
cmap = font.getBestCmap()
upm = font["head"].unitsPerEm

print("upm:", upm)
print("has legacy 'kern' table:", "kern" in font)
print("has GPOS:", "GPOS" in font)

found = {}
gpos = font.get("GPOS")
if gpos and gpos.table and gpos.table.LookupList:
    for lookup in gpos.table.LookupList.Lookup:
        if lookup.LookupType != 2:
            continue
        for sub in lookup.SubTable:
            cls = sub.__class__.__name__
            fmt = getattr(sub, "Format", None)
            if cls == "PairPos" and fmt == 1:
                for i, first in enumerate(sub.Coverage.glyphs):
                    for rec in sub.PairSet[i].PairValueRecord:
                        v = rec.Value1.XAdvance if rec.Value1 else 0
                        found[(first, rec.SecondGlyph)] = v
            elif cls == "PairPos" and fmt == 2:
                for first, ps in zip(sub.Coverage.glyphs, sub.PairSet):
                    for rec in ps.PairValueRecord:
                        v = rec.Value1.XAdvance if rec.Value1 else 0
                        found[(first, rec.SecondGlyph)] = v
            # PairPos is sometimes wrapped in an Extension subtable
            elif cls == "ExtensionSubst" or hasattr(sub, "ExtSubTable"):
                inner = getattr(sub, "ExtSubTable", None)
                if inner is not None and inner.__class__.__name__ == "PairPos":
                    if getattr(inner, "Format", None) == 1:
                        for i, first in enumerate(inner.Coverage.glyphs):
                            for rec in inner.PairSet[i].PairValueRecord:
                                v = rec.Value1.XAdvance if rec.Value1 else 0
                                found[(first, rec.SecondGlyph)] = v

print("kerning pairs recovered:", len(found))

word = "UrbanLoop"
names = [cmap[ord(c)] for c in word]
print("glyphs:", names)

print("\n=== Inter's designed kerning for our sequence ===")
for a, b, ga, gb in zip(word, word[1:], names, names[1:]):
    v = found.get((ga, gb), 0)
    print(f"  {a}+{b}  ({ga} / {gb}):  {v:>6} units  = {v/upm:+.4f} em")
