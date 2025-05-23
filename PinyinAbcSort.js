/*
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

```javascript
// Array of Strings
const testWords = ["bǎoyù", "Bǎoyù", "Bǎoyǔ", "bǎozhàng"];
console.log(pinyinAbcSort(testWords));
console.log(pinyinAbcSort(testWords, null, true)); //reverse

// Array of Dictionaries with default key 'pinyin'
const testDicts = [
    { pinyin: "bǎozhàng", meaning: "guarantee" },
    { pinyin: "Bǎoyǔ", meaning: "Bao Yu (name)" },
    { pinyin: "bǎoyù", meaning: "jade" }
];
console.log(pinyinAbcSort(testDicts, "pinyin"));
console.log(pinyinAbcSort(testDicts, "pinyin", true)); //reverse
```

## History

This was much more difficult than expected, and took much longer than expected. 
But in the end it looks simple, and flies like a SpaceX starship. 🚀
*/

function comparePinyin(w1, w2) {
    const orderedChars = (
        "0123456789aāáǎàAĀÁǍÀbBcCdDeēéěèEĒÉĚÈfFgGhHiīíǐìIĪÍǏÌ" +
        "jJkKlLmMnNoōóǒòOŌÓǑÒpPqQrRsStTuūúǔùUŪÚǓÙ" +
        "üǖǘǚǜÜǕǗǙǛvVwWxXyYzZ'- "
    );

    const WEIGHTS = {};
    for (let i = 0; i < orderedChars.length; i++) {
        WEIGHTS[orderedChars[i]] = i;
    }
    const OFFSET = orderedChars.length;

    // Step 1: Compare lowercase versions first (tones intact)
    const lowerW1 = w1.toLowerCase();
    const lowerW2 = w2.toLowerCase();
    const seq1Lower = Array.from(lowerW1).map(c => WEIGHTS[c] ?? (c.charCodeAt(0) + OFFSET));
    const seq2Lower = Array.from(lowerW2).map(c => WEIGHTS[c] ?? (c.charCodeAt(0) + OFFSET));

    const lenLower = Math.min(seq1Lower.length, seq2Lower.length);
    for (let i = 0; i < lenLower; i++) {
        if (seq1Lower[i] !== seq2Lower[i]) return seq1Lower[i] - seq2Lower[i];
    }
    if (seq1Lower.length !== seq2Lower.length) return seq1Lower.length - seq2Lower.length;

    // Step 2: If lowercase versions are equal, break tie with original case
    const seq1Orig = Array.from(w1).map(c => WEIGHTS[c] ?? (c.charCodeAt(0) + OFFSET));
    const seq2Orig = Array.from(w2).map(c => WEIGHTS[c] ?? (c.charCodeAt(0) + OFFSET));
    const lenOrig = Math.min(seq1Orig.length, seq2Orig.length);
    for (let i = 0; i < lenOrig; i++) {
        if (seq1Orig[i] !== seq2Orig[i]) return seq1Orig[i] - seq2Orig[i];
    }
    return seq1Orig.length - seq2Orig.length;

}

function pinyinAbcSort(items, key = null, reverse = false) {
    // Simplify key: Accept string directly instead of arrow function
    const extractor = typeof key === "string" ? x => x[key] : (key || (x => x));
    const sorted = [...items];
    sorted.sort((a, b) => comparePinyin(extractor(a), extractor(b)));
    return reverse ? sorted.reverse() : sorted;
}
