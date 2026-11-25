#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""321聖經講義合併器：片段 → 完整 DATA JSON → HTML App。

用法:
    # 合併片段目錄成完整 DATA
    python assemble.py 啟示錄/ -o 啟示錄/build/啟示錄_tc.json

    # 把 DATA 注入 HTML 模板，產出單檔 App
    python assemble.py --inject 啟示錄_tc.json template.html -o 321啟示錄講義.html
    python assemble.py --inject 啟示錄_sc.json template.html -o sc.html --lang zh-Hans --title 321啟示录讲义

    # 從既有的 App HTML 抽出 DATA（逆向既有成品用）
    python assemble.py --extract 321啟示錄講義.html -o 啟示錄_tc.json
"""
import argparse
import json
import re
import sys
from pathlib import Path

MARK = '<script id="DATA" type="application/json">'
KEYS = ["ch", "txt", "blk", "serm", "issues", "terrain", "tracks"]


def assemble(root: Path) -> dict:
    """把片段目錄組成完整 DATA。"""
    d = {"ch": [], "txt": {}, "blk": {}, "serm": {},
         "issues": [], "terrain": {"points": []}, "tracks": []}

    bp = root / "blueprint.json"
    if bp.exists():
        blueprint = json.loads(bp.read_text(encoding="utf-8"))
        for k in KEYS:
            if k in blueprint:
                d[k] = blueprint[k]
        d.setdefault("ch", [])

    # 章層片段覆蓋藍圖骨架（階段 D 補齊階段 A 留下的欄位）
    ch_dir = root / "ch"
    if ch_dir.is_dir():
        base = {str(c.get("n")): c for c in d["ch"]}
        for f in sorted(ch_dir.glob("*.json")):
            obj = json.loads(f.read_text(encoding="utf-8"))
            n = str(obj.get("n", int(f.stem)))
            merged = {**base.get(n, {}), **obj}
            # serm 的 pts 來自藍圖，不可被階段 D 覆蓋掉
            if "serm" in base.get(n, {}) and "serm" in obj:
                merged["serm"] = {**base[n]["serm"], **obj["serm"]}
            base[n] = merged
        d["ch"] = [base[k] for k in sorted(base, key=int)]

    for sub in ("txt", "blk", "serm"):
        folder = root / sub
        if not folder.is_dir():
            continue
        for f in sorted(folder.glob("*.json")):
            d[sub][str(int(f.stem))] = json.loads(f.read_text(encoding="utf-8"))

    iss = root / "issues.json"
    if iss.exists():
        d["issues"] = json.loads(iss.read_text(encoding="utf-8"))

    d["ch"].sort(key=lambda c: c.get("n", 0))
    return {k: d[k] for k in KEYS}


def extract(html_path: Path) -> dict:
    html = html_path.read_text(encoding="utf-8")
    i = html.find(MARK)
    if i < 0:
        sys.exit(f"找不到 {MARK}，這不像是 321 講義 App")
    j = html.find("</script>", i)
    return json.loads(html[i + len(MARK):j].strip())


def inject(data: dict, template: Path, lang: str | None, title: str | None) -> str:
    html = template.read_text(encoding="utf-8")
    i = html.find(MARK)
    if i < 0:
        sys.exit(f"模板缺少 {MARK} 佔位標記")
    j = html.find("</script>", i)
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    # </script> 出現在資料裡會提前關閉標籤
    payload = payload.replace("</", "<\\/")
    html = html[:i + len(MARK)] + "\n" + payload + "\n" + html[j:]

    if lang:
        html = re.sub(r'<html\s+lang="[^"]*"', f'<html lang="{lang}"', html, count=1)
    if title:
        html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1, flags=re.S)
        for attr in ("apple-mobile-web-app-title", "application-name"):
            html = re.sub(rf'(<meta name="{attr}" content=")[^"]*(")',
                          rf"\g<1>{title}\g<2>", html, count=1)
    return html


def main():
    ap = argparse.ArgumentParser(description="321聖經講義合併器")
    ap.add_argument("source", help="片段目錄／DATA JSON／App HTML")
    ap.add_argument("template", nargs="?", help="--inject 時的 HTML 模板")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--inject", action="store_true", help="把 DATA 注入 HTML 模板")
    ap.add_argument("--extract", action="store_true", help="從 App HTML 抽出 DATA")
    ap.add_argument("--lang", help="html lang 屬性：zh-Hant / zh-Hans / en")
    ap.add_argument("--title", help="App 標題")
    a = ap.parse_args()

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    if a.extract:
        d = extract(Path(a.source))
        out.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    elif a.inject:
        if not a.template:
            sys.exit("--inject 需要指定 HTML 模板")
        d = json.loads(Path(a.source).read_text(encoding="utf-8"))
        out.write_text(inject(d, Path(a.template), a.lang, a.title), encoding="utf-8")
    else:
        d = assemble(Path(a.source))
        out.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        missing = [str(c["n"]) for c in d["ch"] if str(c["n"]) not in d["blk"]]
        if missing:
            print(f"提醒：第 {'、'.join(missing)} 章尚無解經區塊")

    print(f"已寫出 {out}（{out.stat().st_size:,} 位元組）")
    if not a.inject and not a.extract:
        print(f"章 {len(d['ch'])} ｜ 解經 {sum(len(v) for v in d['blk'].values())} 區塊 "
              f"｜ 講章 {len(d['serm'])} 篇 ｜ 議題 {len(d['issues'])} 條")


if __name__ == "__main__":
    main()
