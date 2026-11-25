#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""321聖經講義片段校驗器。

用法:
    python validate_volume.py 啟示錄/            # 校驗整卷片段目錄
    python validate_volume.py 啟示錄_tc.json     # 校驗合併後的完整 DATA

錯誤在片段階段抓，比在成品階段抓便宜一百倍。
"""
import json
import re
import sys
from pathlib import Path

CH_FIELDS = ["n", "t", "sub", "lv", "arc", "q", "truth", "mv", "card",
             "sec", "serm", "self", "t321", "grp", "prac", "safe"]
BLK_FIELDS = ["a", "z", "star", "grk", "lit", "key", "gram", "exp"]
ISSUE_FIELDS = ["id", "t", "r", "ch", "why", "pos", "con", "say", "care"]
TRACK_FIELDS = ["gk", "tr", "gl", "code", "root", "stops", "ins"]
SERM_TYPES = {"h", "p", "q"}
BANNED_TAGS = re.compile(r"<\s*(div|span|h[1-6])\b", re.I)
# class=/style= 只准出現在表格結構裡（Pandoc 產生的 colgroup/thead 會帶）
# dir=/lang= 不受此限——希伯來文引文需要 dir="rtl"
TABLE_ATTR = re.compile(r"\b(class|style)\s*=", re.I)

# 原文字母：希臘文（含擴展區）與希伯來文
GREEK = re.compile(r"[\u0370-\u03FF\u1F00-\u1FFF]")
HEBREW = re.compile(r"[\u0590-\u05FF]")
# 希臘文的重音與呼氣符號：預組合字元或組合附加符號
GK_DIACRITIC = re.compile(r"[\u1F00-\u1FFF\u0300-\u036F\u0384-\u0385\u03AC-\u03CE\u0390\u03B0]")
# 希伯來文母音點（nikkud）與 shin/sin 點
HEB_NIKKUD = re.compile(r"[\u05B0-\u05BD\u05BF\u05C1\u05C2\u05C7]")
STRONGS = re.compile(r"\b([GH])(\d+)\b")
TR_ROW = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S)
TD_CELL = re.compile(r"<t[dh][^>]*>(.*?)</t[dh]>", re.S)


def plain(html):
    return re.sub(r"<[^>]+>", "", html).strip()


# 字義表欄名的各種寫法 → 統一角色。字義表是 5–7 欄的彈性結構，
# 靠欄名認欄，不靠位置——位置會隨欄數變動。
COL_ROLE = {
    "中文": "term", "english": "term",
    "原文": "orig", "greek": "orig", "hebrew": "orig", "original": "orig",
    "音譯": "translit", "translit": "translit", "transliteration": "translit",
    "strong's": "strongs", "strong’s": "strongs", "strongs": "strongs",
    "構詞": "root", "字根／構詞": "root", "字根": "root",
    "root/formation": "root", "root": "root",
    "意義": "sense", "基本字義": "sense", "basic sense": "sense", "sense": "sense",
    "本節語境": "context", "舊約來源／本節語境": "context",
    "in context": "context", "context": "context",
}


def parse_key_table(key_html):
    """回傳 [(欄角色 → 內容)]，表頭認不出來時回傳 None。"""
    rows = [[plain(c) for c in TD_CELL.findall(r)] for r in TR_ROW.findall(key_html)]
    rows = [r for r in rows if r]
    if not rows:
        return None
    header = [COL_ROLE.get(h.strip().lower()) for h in rows[0]]
    if header.count("orig") != 1 or header.count("translit") != 1:
        return None
    return [dict(zip(header, r)) for r in rows[1:] if len(r) == len(header)]


def check_original_language(where, key_html):
    """字義表的原文欄必須用原文字母，音譯欄必須用拉丁轉寫。

    轉寫會丟資訊——ω 與 ο 都可能寫成 o，ח 與 ה 都可能寫成 h。丟了資訊，
    讀者就無法自己去查、去核對，那正是這套講義最不願意造成的依賴。
    """
    parsed = parse_key_table(key_html)
    if parsed is None:
        W(where, "字義表的表頭認不出來。前四欄應為 中文｜原文｜音譯｜Strong's")
        return

    for row in parsed:
        orig = row.get("orig", "")
        translit = row.get("translit", "")
        strongs = row.get("strongs", "")
        root = row.get("root", "")
        w = f"{where}「{row.get('term', '?')}」"

        if not orig and not translit:
            continue
        is_gk, is_heb = bool(GREEK.search(orig)), bool(HEBREW.search(orig))
        if orig and not (is_gk or is_heb):
            E(w, f"原文欄填了拉丁轉寫 {orig!r}——必須用原文字母（ἀρνίον／חֶסֶד）")
            continue

        if translit and (GREEK.search(translit) or HEBREW.search(translit)):
            E(w, "音譯欄應為拉丁轉寫，不是原文字母")

        if is_gk and not GK_DIACRITIC.search(orig):
            W(w, f"希臘文 {orig!r} 缺重音／呼氣符號（應為 ἀποκάλυψις 而非 αποκαλυψις）")
        if is_heb and not HEB_NIKKUD.search(orig):
            W(w, f"希伯來文 {orig!r} 缺母音點（應為 אֱלֹהִים 而非 אלהים）")

        m = STRONGS.search(strongs)
        if strongs and strongs != "—" and not m:
            W(w, f"Strong's 欄 {strongs!r} 不是 G／H + 數字的格式")
        elif m:
            want = "G" if is_gk else "H"
            if m.group(1) != want:
                E(w, f"Strong's 用了 {m.group(1)} 前綴，但原文是"
                     f"{'希臘文' if is_gk else '希伯來文'}，應為 {want}")

        if root and root != "—" and not (GREEK.search(root) or HEBREW.search(root)):
            W(w, f"字根／構詞欄 {root!r} 應用原文字母")
PLAIN_FIELDS = ["q", "truth", "self"]

errs, warns = [], []


def E(where, msg):
    errs.append(f"[錯誤] {where}: {msg}")


def W(where, msg):
    warns.append(f"[提醒] {where}: {msg}")


def check_html(where, html):
    if not isinstance(html, str):
        E(where, f"應為字串，實為 {type(html).__name__}")
        return
    if BANNED_TAGS.search(html):
        E(where, "使用了禁用標籤（div/span/h1-h6）——樣式由模板控制")
    if TABLE_ATTR.search(html) and "<table" not in html:
        E(where, "表格以外的地方不可用 class=/style=（dir= 與 lang= 不在此限）")
    if re.search(r"<br(?!\s*/)\s*>", html):
        E(where, "<br> 必須寫成自閉合的 <br/>（EPUB 的 XHTML 要求嚴格閉合）")


def check_ch(c, where):
    missing = [f for f in CH_FIELDS if f not in c]
    extra = [f for f in c if f not in CH_FIELDS]
    if missing:
        E(where, f"缺少欄位 {missing}")
    if extra:
        E(where, f"多出欄位 {extra}")
    if missing:
        return

    if c["lv"] not in ("A", "B", "C"):
        E(where, f"lv 應為 A/B/C，實為 {c['lv']!r}")

    if not isinstance(c["card"], list) or len(c["card"]) != 7:
        E(where, f"card 必須是 7 張，實為 {len(c.get('card', []))} 張")
    elif not str(c["card"][6]).startswith("最終整合"):
        W(where, "card[6] 應以「最終整合：」起頭（全章的敘事詩體落幕）")

    if set(c.get("t321", {})) != {"k", "g", "p"}:
        E(where, f"t321 必須有且只有 k/g/p 三軌，實為 {sorted(c.get('t321', {}))}")

    if set(c.get("mv", {})) != {"t", "r"}:
        E(where, "mv 必須是 {t, r}")

    if set(c.get("prac", {})) != {"main", "items"}:
        E(where, "prac 必須是 {main, items}")
    elif not 4 <= len(c["prac"]["items"]) <= 5:
        W(where, f"prac.items 建議 4–5 項（對神/對自己/對人/對生活/對使命），實為 {len(c['prac']['items'])}")

    if not 4 <= len(c.get("sec", [])) <= 7:
        W(where, f"sec 建議 4–7 段，實為 {len(c.get('sec', []))}")
    for k, sec in enumerate(c.get("sec", [])):
        if not (isinstance(sec, list) and len(sec) == 2):
            E(f"{where}.sec[{k}]", "每段應為 [經文範圍, 標題]")
        elif "--" not in sec[0] and "-" in sec[0]:
            W(f"{where}.sec[{k}]", f"節號範圍應用雙連字號 --，實為 {sec[0]!r}")

    g = c.get("grp", [])
    if g and len(g) != 5:
        W(where, f"grp 若有題目應為 5 題，實為 {len(g)}")

    if not 7 <= len(c.get("safe", [])) <= 16:
        W(where, f"safe 建議 7–16 條，實為 {len(c.get('safe', []))}")

    for f in PLAIN_FIELDS:
        if isinstance(c.get(f), str) and re.search(r"<[a-zA-Z/]", c[f]):
            E(f"{where}.{f}", "純文字欄位不可含 HTML 標籤")

    s = c.get("serm", {})
    if "pts" not in s:
        E(where, "serm 缺少 pts（三個大點，階段 A 就要定）")
    elif len(s["pts"]) != 3:
        W(where, f"serm.pts 應為 3 個大點，實為 {len(s['pts'])}")


def check_blk(blocks, ch):
    if not isinstance(blocks, list) or not blocks:
        E(f"blk[{ch}]", "應為非空陣列")
        return
    if not 6 <= len(blocks) <= 22:
        W(f"blk[{ch}]", f"區塊數建議 6–22（平均 10），實為 {len(blocks)}")
    prev_z = 0
    for i, b in enumerate(blocks):
        w = f"blk[{ch}][{i}]"
        missing = [f for f in BLK_FIELDS if f not in b]
        extra = [f for f in b if f not in BLK_FIELDS]
        if missing:
            E(w, f"缺少欄位 {missing}")
            continue
        if extra:
            E(w, f"多出欄位 {extra}")
        if not isinstance(b["star"], int) or not 0 <= b["star"] <= 3:
            E(w, f"star 是 0–3 的權重（不是開關），實為 {b['star']!r}")
        if b["a"] > b["z"]:
            E(w, f"a({b['a']}) 大於 z({b['z']})")
        if b["a"] != prev_z + 1:
            W(w, f"節號不連續：上一區塊結束於 {prev_z}，本區塊起於 {b['a']}")
        prev_z = b["z"]
        for f in ("grk", "lit", "key", "gram", "exp"):
            check_html(f"{w}.{f}", b[f])
        if b["key"].strip():
            if "<table" not in b["key"]:
                E(f"{w}.key", "字義表必須是 <table>")
            else:
                if "Strong" not in b["key"]:
                    W(f"{w}.key", "字義表應有 Strong's 欄")
                check_original_language(f"{w}.key", b["key"])

        if b["grk"].strip():
            g, h = GREEK.search(b["grk"]), HEBREW.search(b["grk"])
            if not (g or h):
                E(f"{w}.grk", "原文欄沒有原文字母——不可用拉丁轉寫代替")
            if h and 'dir="rtl"' not in b["grk"]:
                E(f"{w}.grk", '希伯來文引文必須加 dir="rtl"，否則標點會跑到錯誤的一端')
    if not any(b.get("star") == 3 for b in blocks):
        W(f"blk[{ch}]", "沒有 star=3 的全章樞紐區塊")


def check_serm(s, ch):
    w = f"serm[{ch}]"
    if "min" not in s or "blocks" not in s:
        E(w, "必須有 min 與 blocks")
        return
    if not 11 <= s["min"] <= 32:
        W(w, f"min 建議 11–32 分鐘（典型 15），實為 {s['min']}")
    blocks = s["blocks"]
    if not 210 <= len(blocks) <= 400:
        W(w, f"blocks 建議 210–400 個，實為 {len(blocks)}")
    heads = [b for b in blocks if b[0] == "h"]
    if len(heads) != 1:
        E(w, f"整篇只能有 1 個 h 標題，實為 {len(heads)}")
    elif blocks[0][0] != "h":
        E(w, "第一個 block 必須是 h 標題")
    for i, b in enumerate(blocks):
        if not (isinstance(b, list) and len(b) == 2):
            E(f"{w}[{i}]", "每個 block 應為 [類型, 文字]")
        elif b[0] not in SERM_TYPES:
            E(f"{w}[{i}]", f"類型只有 h/p/q，實為 {b[0]!r}")
    chars = sum(len(b[1]) for b in blocks if len(b) == 2)
    if not 3800 <= chars <= 9500:
        W(w, f"講章字數建議 3,800–9,500（典型 4,900），實為 {chars:,}")
    # 講速基準：約每分鐘 300 字。min 與字數對不上，通常是其中一個填錯
    if s["min"] and not 240 <= chars / s["min"] <= 380:
        W(w, f"min={s['min']} 分鐘配 {chars:,} 字＝每分鐘 {chars/s['min']:.0f} 字，"
             f"偏離講速基準（約 300 字／分）")
    ps = [b for b in blocks if b[0] == "p"]
    if ps:
        avg = sum(len(b[1]) for b in ps) / len(ps)
        if avg > 30:
            W(w, f"段落平均 {avg:.0f} 字，偏長（典型 18）。"
                 f"這是講出來的稿，長句在講台上會斷氣")
    qs = [b for b in blocks if b[0] == "q"]
    if blocks and not 0.02 <= len(qs) / len(blocks) <= 0.16:
        W(w, f"q 引用佔比 {len(qs)/len(blocks):.0%}，建議 2–16%（典型 8%）")


def check_issues(issues):
    seen = set()
    for i, x in enumerate(issues):
        w = f"issues[{i}]"
        missing = [f for f in ISSUE_FIELDS if f not in x]
        if missing:
            E(w, f"缺少欄位 {missing}")
            continue
        if x["con"] != []:
            E(w, "con 是保留欄，必須是空陣列")
        if x["id"] in seen:
            E(w, f"id 重複：{x['id']}")
        seen.add(x["id"])
        if not re.fullmatch(r"ISS\d{2}_\d+", x["id"]):
            W(w, f"id 格式應為 ISS + 兩位章號 + _ + 序號，實為 {x['id']!r}")
        if not str(x["t"]).endswith(("？", "?")):
            W(w, "議題標題建議用問句")
        if not x["pos"]:
            E(w, "pos 至少要有一個立場")
        for k, p in enumerate(x["pos"]):
            if not (isinstance(p, list) and len(p) == 3):
                E(f"{w}.pos[{k}]", "每個立場應為 [立場名, \"\", 說明] 三元組")
        if not x.get("care"):
            W(w, "care 從缺。議題不是為了辯論，是為了保護人——盡量補上牧養提醒")


def check_terrain(t):
    pts = t.get("points", [])
    if not 8 <= len(pts) <= 16:
        W("terrain", f"建議取 10–14 個轉折點，實為 {len(pts)}。點太密就看不出形狀")
    for i, p in enumerate(pts):
        w = f"terrain.points[{i}]"
        if not (isinstance(p, list) and len(p) == 5):
            E(w, "應為 [章號, 高度, 0, 標籤, 位置] 五元組")
            continue
        if not 0 <= p[1] <= 100:
            E(w, f"高度應在 0–100，實為 {p[1]}")
        if p[2] != 0:
            E(w, "第三位是保留位，一律 0")
        if p[4] not in ("top", "bot", None):
            E(w, f"位置只有 top/bot/null，實為 {p[4]!r}")
        if p[4] in ("top", "bot") and not p[3]:
            W(w, "標為 top/bot 的點應該有標籤")


def check_tracks(tracks):
    if not 3 <= len(tracks) <= 5:
        W("tracks", f"全卷建議 3–5 條主線字，實為 {len(tracks)}")
    for i, t in enumerate(tracks):
        w = f"tracks[{i}]"
        missing = [f for f in TRACK_FIELDS if f not in t]
        if missing:
            E(w, f"缺少欄位 {missing}")
            continue
        if not 8 <= len(t["stops"]) <= 11:
            W(w, f"stops 建議 8–11 站，實為 {len(t['stops'])}")
        for k, s in enumerate(t["stops"]):
            if not (isinstance(s, list) and len(s) == 3):
                E(f"{w}.stops[{k}]", "每站應為 [經文, 意義, 位置標記] 三元組")
            elif s[2] not in ("top", "bot", ""):
                E(f"{w}.stops[{k}]", f"位置標記只有 top/bot/空字串，實為 {s[2]!r}")
        gk = t.get("gk", "")
        g, h = GREEK.search(gk), HEBREW.search(gk)
        if gk and not (g or h):
            E(w, f"gk 欄填了拉丁轉寫 {gk!r}——必須用原文字母")
        if t.get("tr") and (GREEK.search(t["tr"]) or HEBREW.search(t["tr"])):
            E(w, "tr 欄應為拉丁轉寫，不是原文字母")
        m = STRONGS.search(t.get("code", ""))
        if m and (g or h):
            want = "G" if g else "H"
            if m.group(1) != want:
                E(w, f"code 用了 {m.group(1)} 前綴，與 gk 的字母系統不符，應為 {want}")
        if t.get("root") and not (GREEK.search(t["root"]) or HEBREW.search(t["root"])):
            W(w, f"root 欄 {t['root']!r} 應用原文字母")
        if not t.get("ins"):
            E(w, "ins 不可為空——這個字走完全卷的洞見，是整條軌道的意義所在")


def check_data(d):
    """校驗完整或部分的 DATA 結構。"""
    for c in d.get("ch", []):
        check_ch(c, f"ch[{c.get('n', '?')}]")
    ns = [c.get("n") for c in d.get("ch", [])]
    if ns and ns != list(range(1, len(ns) + 1)):
        E("ch", f"章號應從 1 連續遞增，實為 {ns}")

    for ch, blocks in d.get("blk", {}).items():
        check_blk(blocks, ch)
    for ch, s in d.get("serm", {}).items():
        check_serm(s, ch)
    for ch, t in d.get("txt", {}).items():
        if not isinstance(t, list) or not t:
            E(f"txt[{ch}]", "應為非空的經文字串陣列")

    if "issues" in d:
        check_issues(d["issues"])
    if "terrain" in d:
        check_terrain(d["terrain"])
    if "tracks" in d:
        check_tracks(d["tracks"])

    # 跨區交叉檢查
    chs = {str(c["n"]) for c in d.get("ch", []) if "n" in c}
    if chs:
        for k in ("blk", "serm", "txt"):
            for miss in sorted(chs - set(d.get(k, {})), key=int):
                W(k, f"第 {miss} 章尚未產出")


def load_fragments(root: Path):
    """把片段目錄組成一個 DATA 結構。"""
    d = {"ch": [], "txt": {}, "blk": {}, "serm": {}}
    bp = root / "blueprint.json"
    if bp.exists():
        d.update(json.loads(bp.read_text(encoding="utf-8")))
        d.setdefault("ch", [])
    for sub, key in (("ch", "ch"), ("txt", "txt"), ("blk", "blk"), ("serm", "serm")):
        folder = root / sub
        if not folder.is_dir():
            continue
        for f in sorted(folder.glob("*.json")):
            n = str(int(f.stem))
            obj = json.loads(f.read_text(encoding="utf-8"))
            if key == "ch":
                d["ch"] = [c for c in d["ch"] if str(c.get("n")) != n] + [obj]
            else:
                d[key][n] = obj
    iss = root / "issues.json"
    if iss.exists():
        d["issues"] = json.loads(iss.read_text(encoding="utf-8"))
    d["ch"].sort(key=lambda c: c.get("n", 0))
    return d


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    p = Path(sys.argv[1])
    if p.is_dir():
        d = load_fragments(p)
        print(f"校驗片段目錄：{p}")
    else:
        d = json.loads(p.read_text(encoding="utf-8"))
        print(f"校驗完整 DATA：{p}")

    check_data(d)

    for e in errs:
        print(e)
    for w in warns:
        print(w)

    print()
    print(f"章 {len(d.get('ch', []))} ｜ 解經 {sum(len(v) for v in d.get('blk', {}).values())} 區塊 "
          f"｜ 講章 {len(d.get('serm', {}))} 篇 ｜ 議題 {len(d.get('issues', []))} 條 "
          f"｜ 追蹤字 {len(d.get('tracks', []))} 條")
    print(f"錯誤 {len(errs)} ｜ 提醒 {len(warns)}")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
