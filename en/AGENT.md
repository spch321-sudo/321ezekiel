# 翻譯包工作說明（一位譯者一包）

工作目錄 /home/claude/321ezekiel。你負責翻譯一個包 Pxxx（中文 → 英文）。

1. 先讀 en/GLOSSARY.md（術語與格式規則，必須照用）與 en/EXAMPLES.md（耶利米書中英對照，學口吻與處理方式）。
2. `python3 scripts/en_units.py show Pxxx` 印出本包全部單位（`@@id@@` 行＋原文）。用 Read 讀 en/in/Pxxx.txt 亦可。
3. 把譯文寫到 en/out/Pxxx.txt：每個單位保留 `@@id@@` 單獨一行，下一行起是英文譯文。檔案很大，可分段寫（第一段用 Write，其後用 Bash `cat >> en/out/Pxxx.txt <<'EOF'` 追加）；每段都要是完整的單位，不要切斷單位。**只能寫自己的包檔，不准動其他任何檔案**；暫存檔放 /tmp/Pxxx_*/（每包獨立目錄，避免互蓋）。
4. 引經：照 GLOSSARY 第一節，用 `python3 scripts/web.py "Ezek 37:14"` 查 WEB 再引；一次可查多段（多個參數）。
5. 寫完跑 `python3 scripts/en_units.py check Pxxx`，必須印出「✓ 通過」；不通過就依訊息修到通過（缺 id、殘留漢字或「」、HTML 標籤不一致、希伯來文走樣、數字經節掉了…）。
5b. 希伯來文表格若被 check 擋下（母音點順序走樣），不要手改：跑 `python3 scripts/en_units.py fixheb Pxxx` 自動還原成原文，再 check。
6. 不要偷懶、不要省略、不要概括：每個單位都完整翻譯；段落、列點、標籤與原文一一對應。
7. 回報一行：包號、單位數、英文字數、有無 NOTE。
