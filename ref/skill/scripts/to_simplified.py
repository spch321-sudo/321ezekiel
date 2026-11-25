#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""繁 → 簡轉換：321聖經講義 DATA JSON。

    pip install opencc-python-reimplemented
    python to_simplified.py 啟示錄_tc.json 啟示錄_sc.json

永遠不要用語言模型做這件事。模型轉換會漂移、會順手改字、不可重跑。
希臘文與希伯來文欄位（grk）原樣保留，不進轉換器。
"""
import json
import sys
from pathlib import Path

# 不進轉換器的欄位：原文一個字都不能動
SKIP_FIELDS = {"grk", "tr", "gk", "code", "root", "id"}

# OpenCC 之後的例外修正：一詞多形、和合本專用寫法
# 鍵是 OpenCC 轉出來的、要改掉的字串；值是正確的簡體寫法
EXCEPTIONS = {
    # 在這裡累積例外。一次修好，永遠適用。
    # 例：「乾」在「乾旱」轉成「干旱」正確，但在「乾坤」應保留。
    # "干坤": "乾坤",
}


def load_converter():
    try:
        from opencc import OpenCC
    except ImportError:
        sys.exit("需要 OpenCC：pip install opencc-python-reimplemented")
    return OpenCC("t2s")


def convert(node, cc, key=None):
    if isinstance(node, str):
        if key in SKIP_FIELDS:
            return node
        s = cc.convert(node)
        for wrong, right in EXCEPTIONS.items():
            s = s.replace(wrong, right)
        return s
    if isinstance(node, dict):
        return {k: convert(v, cc, k) for k, v in node.items()}
    if isinstance(node, list):
        return [convert(v, cc, key) for v in node]
    return node


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    cc = load_converter()

    data = json.loads(src.read_text(encoding="utf-8"))
    out = convert(data, cc)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    a, b = src.stat().st_size, dst.stat().st_size
    print(f"{src.name} {a:,} → {dst.name} {b:,}（差 {abs(a-b):,} 位元組）")
    if abs(a - b) > 2000:
        print("提醒：兩份檔案大小差距偏大。純字符轉換應該只差幾十到幾百位元組——")
        print("      若差距明顯，通常表示有人手改了衍生檔，請回頭修正繁體源頭。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
