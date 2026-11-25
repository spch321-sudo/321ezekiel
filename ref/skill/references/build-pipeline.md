# 321 聖經講義 — 六種交付檔的產出管線

## 全景

```
{書卷}_tc.json  ← 唯一真理來源(繁體)
      │
      ├── OpenCC t2s ─────────→ {書卷}_sc.json
      ├── Opus 逐章翻譯 ──────→ {書卷}_en.json
      │
      └── 三份 JSON × 同一模板
              ├─→ tc.html / sc.html / en.html   (App)
              ├─→ *.epub                        (電子書)
              └─→ *.pdf                         (列印)
```

**一支腳本吃 JSON 吐六個檔。** 前期多花兩天做這件事,後面每一卷都在收利息。

---

## 第一步:合併片段

```bash
python scripts/validate_volume.py 啟示錄/
python scripts/assemble.py 啟示錄/ -o 啟示錄/build/啟示錄_tc.json
```

`validate_volume.py` 會擋下:欄位缺漏、`card` 不是 7 張、`t321` 缺軌、`blk` 欄位不全、`star` 超出 0–3、章號不連續、`serm.blocks` 用了 `h`/`p`/`q` 以外的類型。

**錯誤在片段階段抓,比在成品階段抓便宜一百倍。**

---

## 第二步:繁 → 簡

```bash
pip install opencc-python-reimplemented
python scripts/to_simplified.py 啟示錄/build/啟示錄_tc.json 啟示錄/build/啟示錄_sc.json
```

轉換後檢查兩份檔案大小:**應該只差幾十個位元組**。差距明顯變大,表示有人手改了衍生檔,回頭修源頭。

腳本會保留 `grk`(希臘文)不動,並套用 `EXCEPTIONS` 例外表處理一詞多形的字。

---

## 第三步:中 → 英

翻譯是唯一需要語言模型的衍生步驟。逐章進行,不要整卷一次:

```
【任務】321聖經講義英文版|{書卷}第{N}章

【輸入】該章的 tc JSON 片段 + references/writing-style.md 的英文術語表 + glossary_en.json

【輸出】結構完全相同的英文 JSON。只輸出 JSON。

【規則】
1. grk 欄原樣保留,一個字都不改
2. 經文英譯用 ESV,全卷一致
3. key 表頭改為 English | Greek | Translit | Strong's | Root/Formation | Basic Sense | In Context
4. 321 術語照 glossary_en.json,不自創譯法
5. HTML 標籤結構完全保留,只換文字
6. serm.blocks 的 block 數量與類型必須完全對應,不合併不拆分
```

翻完跑一次結構比對,確認 `blk` 區塊數、`serm.blocks` 數、`card` 張數與繁體版完全一致。

---

## 第四步:注入 HTML App

三個語言版共用**同一份模板**,只換 JSON 與 `lang` 屬性。

模板必備的 head 設定(取自現有的啟示錄 App):

```html
<html lang="zh-Hant">           <!-- sc: zh-Hans / en: en -->
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,maximum-scale=5">
<meta name="theme-color" content="#1F4D3D">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="321{書卷}講義">
<link rel="apple-touch-icon" sizes="180x180" href="data:image/png;base64,…">
```

資料以 `<script id="DATA" type="application/json">` 內嵌,渲染邏輯在其後的 `<script>`。
單檔、無外部相依、離線可用——這是這套 App 的設計前提,不要引入 CDN。

```bash
python scripts/assemble.py --inject 啟示錄/build/啟示錄_tc.json template.html -o 321啟示錄講義.html
python scripts/assemble.py --inject 啟示錄/build/啟示錄_sc.json template.html -o sc.html --lang zh-Hans
python scripts/assemble.py --inject 啟示錄/build/啟示錄_en.json template.html -o en.html --lang en
```

---

## 第五步:EPUB

每章拆成獨立 XHTML,不要全卷一個檔——閱讀器會卡。

```
{書卷}.epub
├── mimetype                    (application/epub+zip,不壓縮,必須是第一個項目)
├── META-INF/container.xml
└── OEBPS/
    ├── content.opf             (metadata + manifest + spine)
    ├── toc.ncx                 (EPUB2 相容)
    ├── nav.xhtml               (EPUB3 目錄)
    ├── style.css
    ├── ch01.xhtml … ch22.xhtml
    ├── issues.xhtml
    ├── terrain.xhtml
    └── tracks.xhtml
```

每章 XHTML 的內容順序:章題 → `q` → `sec` 大綱 → `blk` 逐節 → `serm` 講章 → `card` → `t321` → `grp` → `prac` → `safe`。

注意:
- EPUB 的 XHTML 要求**嚴格閉合**,`<br/>` 不能寫成 `<br>`
- 中文字型建議在 CSS 用 `font-family: serif` 讓閱讀器自選,不嵌入字型(會讓檔案暴增)
- `mimetype` 必須是 zip 的第一個項目且用 STORE(不壓縮),否則閱讀器不認

---

## 第六步:PDF

**不要另建排版系統。** 從一份「列印樣式」的 HTML 轉出:

```bash
# 需 pip install weasyprint
python scripts/assemble.py --print 啟示錄/build/啟示錄_tc.json -o print_tc.html
weasyprint print_tc.html 321啟示錄講義_繁體.pdf
```

列印樣式的 CSS 要點:

```css
@page { size: A4; margin: 2cm 1.8cm; }
h1 { page-break-before: always; }        /* 每章新起一頁 */
table, blockquote { page-break-inside: avoid; }
.sermon { page-break-before: always; }
```

---

## 檢查清單

出檔之後,逐項確認:

- [ ] 繁簡兩份 JSON 大小差距在百位元組以內
- [ ] 英文版的 `blk` 區塊數、`serm.blocks` 數與繁體版完全一致
- [ ] 三個 HTML 都能離線開啟,無外部請求
- [ ] EPUB 通過 `epubcheck`
- [ ] PDF 每章都從新頁開始,表格沒有跨頁斷裂
- [ ] 六個檔案的書卷名、章數、版本號一致
