
STANDARD_FACES_DICT = {
    "happy": "(◕‿◕)", "happy2": "(•‿‿•)", "sad": "(╥☁╥ )", "excited": "(ᵔ◡◡ᵔ)",
    "thinking": "(￣ω￣)", "love": "(♥‿‿♥)", "surprised": "(◉_◉)", "grateful": "(^‿‿^)",
    "motivated": "(☼‿‿☼)", "bored": "(-__-)", "sleeping": "( -_-)zZ",
    "sleeping_pwn": "(⇀‿‿↼)", "awakening": "(≖‿‿≖)", "observing": "( ⚆⚆)",
    "intense": "(°▃▃°)", "cool": "(⌐■_■)", "chill": "(▰˘◡˘▰)", "hype": "(╯°□°）╯",
    "hacker": "[■_■]", "smart": "(✜‿‿✜)", "broken": "(☓‿‿☓)", "debug": "(#__#)",
    "angry": "(╬ಠ益ಠ)", "crying": "(ಥ﹏ಥ)", "proud": "(๑•̀ᴗ•́)و", "nervous": "(°△°;)",
    "confused": "(◎_◎;)", "mischievous": "(◕‿↼)", "wink": "(◕‿◕✿)", "dead": "(✖_✖)",
    "shock": "(◯△◯)", "suspicious": "(¬_¬)", "smug": "(￣‿￣)", "cheering": "\\(◕◡◕)/",
    "celebrate": "★(◕‿◕)★", "dizzy": "(⊙๖⊙)", "lonely": "(ب__б)", "demotivated": "(≖__≖)"
}

for name, k in STANDARD_FACES_DICT.items():
    print(f"{name:15}: {len(k)} chars | {k}")

max_len = max(len(k) for k in STANDARD_FACES_DICT.values())
print(f"\nFinal Max Length: {max_len}")
