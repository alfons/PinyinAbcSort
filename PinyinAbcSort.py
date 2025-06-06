"""
# PinyinAbcSort - Sort Hànyǔ Pīnyīn in alphabetical order (fast)

## Description:

Sort Chinese (Hànyǔ) Pīnyīn words into strict alphabetical order.

1. Compare words letter by letter, not syllable by syllable. 
2. Respect diacritics (tone marks) as part of the letter, not merely 
as tiebreaker.

This approach reflects the fact that Hànyǔ Pīnyīn is written using the Latin 
alphabet — the key insight behind this implementation.

## The ordering rules are:

 1. Alphabetical order, including diacritics (tone marks)
 2. Tone marks sorting order 0 < 1 < 2 < 3 < 4 (for example, a < ā < á < ǎ < à)
 3. u before ü, U before Ü
 4. lowercase and mixed-case before uppercase
 5. Separators: apostrophe < hyphen < space

Since no rules for numbers 0–9 were given, numbers sort before letters. All 
other characters sort behind, according to their Unicode value.

This project was initially inspired by by John DeFrancis in ABC Chinese-English 
Dictionary, Page xiii, Reader’s Guide, I. Arrangement of Entries, but sorting
by PinyinAbcSort is much stricter and more straightforward.

Link to Wiki about the differences in word order between PinyinAbcSort and the 
ABC Chinese-English Dictionary: 
[PinyinAbcSort Wiki](https://github.com/alfons/PinyinAbcSort/wiki)

## Credits and Acknowledgements:

 - John DeFrancis (1911-2009): Original Pīnyīn alphabetical word order, in passionate
   acknowledgment of the advocates of writing reform Lù Zhuāngzhāng (陆璋章,
   1854–1928), Lǔ Xùn (鲁迅, 1881–1936), Máo Dùn (Shěn Yànbīng, 茅盾, 沈雁冰,
   1896–1981), Wáng Lì (王力, 1900–1988) and Lù Shūxiāng (吕叔湘, 1904–1998),
   and Zhōu Yǒuguāng (周有光, 1905–2017).
 - Mark Swofford of Banqiao, Taiwan: summarised the rules outlined by John DeFrancis
   on his blog, thus keeping them available to the world.
 - Alfons Grabher: Idea, concept, prompting, testing, and driving the
   development of pinyinAbcSort.
 - Grok (xAI), ChatGPT 4o: Coding the implementation with flair and precision.

## Usage 

```python
# Array of Strings
words = ["bǎozhàng", "Bǎoyǔ", "bǎoyù"]
sorted_words = pinyin_abc_sort(words)
print(sorted_words) 

# Array of Dictionaries
dicts = [
    {"pinyin": "bǎozhàng", "meaning": "guarantee"},
    {"pinyin": "Bǎoyǔ", "meaning": "Bao Yu (name)"},
    {"pinyin": "bǎoyù", "meaning": "jade"}
]
sorted_dicts = pinyin_abc_sort(dicts, key="pinyin")
print(sorted_dicts)

# Reverse Order (Strings)
reverse_words = pinyin_abc_sort(words, reverse=True)
print(reverse_words)  # ['Bǎoyǔ', 'bǎozhàng', 'bǎoyù']

# Reverse Order (Dictionaries)
reverse_dicts = pinyin_abc_sort(dicts, key="pinyin", reverse=True)
print(reverse_dicts)
```

## History

This was much more difficult than expected, and took much longer than expected. 
But in the end it looks simple, and flies like a SpaceX starship. 🚀
"""

from functools import cmp_to_key

def _compare_pinyin(w1, w2):
    # Uppercase letters can be excluded because of the ord(c) + OFFSET fallback
    ordered_chars = "0123456789aāáǎàbcdeēéěèfghiīíǐìjklmnoōóǒòpqrsstuūúǔùüǖǘǚǜvwxyz'- "
    WEIGHTS = {char: i for i, char in enumerate(ordered_chars)}
    OFFSET = len(ordered_chars)  # Offset for unmapped chars

    # Step 1: Convert to lowercase for primary comparison (preserving tones)
    lower_w1 = w1.lower()
    lower_w2 = w2.lower()
    seq1 = [WEIGHTS.get(c, ord(c) + OFFSET) for c in lower_w1]
    seq2 = [WEIGHTS.get(c, ord(c) + OFFSET) for c in lower_w2]
    cmp_lower = (seq1 > seq2) - (seq1 < seq2)

    # Step 2: If lowercase versions are equal, use original strings for case tiebreaker
    if cmp_lower == 0:
        seq1_orig = [WEIGHTS.get(c, ord(c) + OFFSET) for c in w1]
        seq2_orig = [WEIGHTS.get(c, ord(c) + OFFSET) for c in w2]
        return (seq1_orig > seq2_orig) - (seq1_orig < seq2_orig)
    
    return cmp_lower

def pinyin_abc_sort(items, key=None, reverse=False):
    extractor = (lambda x: x[key]) if key else lambda x: x
    items_list = list(items)
    items_list.sort(key=cmp_to_key(lambda a, b: _compare_pinyin(extractor(a), extractor(b))), reverse=reverse)
    return items_list

if __name__ == "__main__":
    test_words = [
        # Tones (all variants)
        "baozi", "bāozi", "báozi", "bǎozi", "bàozi",
        # Case (mixed and full uppercase)
        "bǎozi", "Bǎozi", "BǍOZI",
        # Duplicates
        "bǎozi", "bǎozi", "Bǎozi",
        # U vs Ü
        "lù", "lü", "Lù", "Lǚ",
        # Separators (space, hyphen, apostrophe)
        "bǎo", "bǎo an", "bǎo-an", "bǎo'an",
        # Length and prefix matches
        "bǎozhǎng", "bǎozhàng", "bǎozhàngjiāndū",
        # Alphabetical transitions
        "bǎoyù", "bǎozàng", "bǎpa", "bǎshǐ",
        # Mixed tones and case
        "bǎOYÙ", "Bǎoyù", "bĀozì", "Bǎoyǔ",
        # Edge chars (start/end of alphabet)
        "ǎ", "à", "zǐ", "Zǐ",
        # Separator-heavy
        "bǎo an-xiǎo", "bǎo'an xiǎo",
        # Tricky ü with tones
        "nǚ", "Nǚ", "nǜrén",
        # Hyphens and spaces don’t affect sort order
        "lìgōng", "lǐ-gōng",
        # Odd friends (non-Pīnyīn chars)
        "bǎo#", "bǎo$", "bǎo©"
    ]
    sorted_words = pinyin_abc_sort(test_words, reverse=False)
    print("\n".join(sorted_words))
    dicts = [
    {"pinyin": "bǎozhàng", "meaning": "guarantee"},
    {"pinyin": "Bǎoyǔ", "meaning": "Bao Yu (name)"},
    {"pinyin": "bǎoyù", "meaning": "jade"}
    ]
    sorted_dicts = pinyin_abc_sort(dicts, key="pinyin")
    print(sorted_dicts)
