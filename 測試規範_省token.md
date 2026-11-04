# 省 token 工具指令 A/B 測試規範

## 一、目的

比較「只有個人習慣」與「個人習慣＋省 token 工具指令」兩種設定，在 pptx、docx、pdf、xlsx 四種檔案的查詢與修改任務上，實際消耗的 token 差多少。

測試分成兩條獨立的線，各扣各的額度：

| 測試線 | 執行工具 | 指令檔 | 扣誰的額度 | 誰來跑 |
|---|---|---|---|---|
| Claude 線 | Claude Code（`claude -p`） | `CLAUDE.md` | 只扣 Claude | 使用者或 Claude |
| GPT 線 | Codex CLI（`codex exec`） | `AGENTS.md`（內容與 CLAUDE.md 相同） | 只扣 GPT | GPT |

**規定**：
- GPT 線全程**禁止呼叫 `claude` 指令**，只能用 `codex`。
- Claude 線全程不呼叫 `codex`。
- 兩條線的數字不能互相比較，因為模型不同、計算方式也不同；每條線只比較自己的 A 組與 B 組。

## 二、環境需求

- Claude 線：Claude Code CLI 已登入（`claude --version` 能正常顯示版本）
- GPT 線：Codex CLI 已登入（`codex --version` 能正常顯示版本）；執行前先用 `codex exec --help` 確認第十二節用到的參數名稱，版本不同時參數可能不同
- bash 4 以上（Windows 可用 Git Bash 或 WSL）
- Python 3，並安裝 `python-pptx`、`python-docx`、`openpyxl`、`pypdf`（驗證結果用；依個人規範用 `uv` 安裝）
- 測試期間，**暫時把使用者層級的指令檔移開**，測完再放回去，不然它會同時載入到兩組，結果會失真：
  - Claude 線：`~/.claude/CLAUDE.md`
  - GPT 線：`~/.codex/AGENTS.md`

## 三、兩組設定

| 組別 | Claude 線資料夾 | GPT 線資料夾 | 指令檔內容 |
|---|---|---|---|
| A 對照組 | `<根目錄>/claude/A` | `<根目錄>/gpt/A` | 只有個人習慣：目前 CLAUDE.md 從開頭到「## 省 token 工具指令」之前 |
| B 實驗組 | `<根目錄>/claude/B` | `<根目錄>/gpt/B` | 目前完整的 CLAUDE.md（個人習慣＋四種工具指令） |

- Claude 線的指令檔命名為 `CLAUDE.md`，GPT 線命名為 `AGENTS.md`，內容一模一樣。
- 兩組其他條件完全相同。

## 四、測試檔案

兩組各放一份一模一樣的副本，並改成以下檔名：

| 檔名 | 原始檔案 | 內容 |
|---|---|---|
| `簡報.pptx` | 使用者提供的簡報，15 張，約 12 MB | 寵物產業簡報 |
| `報告.docx` | 使用者提供的 NotebookLM 報告，100 段 | 社工 NotebookLM 工作坊報告 |
| `計劃書.pdf` | 使用者提供的計劃書，15 頁 | 動物用藥 AI 檢索助理計劃書 |
| `書目.xlsx` | 使用者提供的書目，38 個工作表 | 企管系書目 |

## 五、8 個任務

每個 prompt 都以「開始。」開頭，避免被「未收到開始指令前不動檔案」規則擋下。

| 代號 | 類型 | prompt |
|---|---|---|
| pptxQ | 查詢 | 開始。簡報.pptx 第 3 張投影片上有哪些文字?條列出來。 |
| pptxM | 修改 | 開始。修改 簡報.pptx:把第 3 張投影片的標題改成「市場規模與成長」,另存成新檔。 |
| docxQ | 查詢 | 開始。報告.docx 裡哪些段落提到「NotebookLM」?只列出段落編號與一句摘要。 |
| docxM | 修改 | 開始。修改 報告.docx:把「教學社工使用NotebookLM」這一段改成「教學社工如何使用 NotebookLM」,並在文件最後新增一段「本文件僅供參考。」,另存成新檔。 |
| pdfQ | 查詢 | 開始。計劃書.pdf 哪幾頁提到「檢索」?列出頁碼與一句摘要。 |
| pdfM | 修改 | 開始。把 計劃書.pdf 的第 1 到 3 頁另存成一個新的 PDF。 |
| xlsxQ | 查詢 | 開始。書目.xlsx 有幾個工作表?每個工作表各有幾筆有編號的資料? |
| xlsxM | 修改 | 開始。修改 書目.xlsx:在第一個工作表最後一欄後面新增一欄「備註」,每一筆有編號的資料都填入「待確認」,另存成新檔。 |

## 六、執行規則

1. 每個任務用 `claude -p` 開一個全新對話，跑完就結束，不延續上一個任務。
2. 指令固定如下，**最後的 `< /dev/null` 不能省**（不加的話，程式可能把標準輸入也讀進 prompt，上次就因此污染了 21 次數據）：
   - Claude 線：
     ```bash
     claude -p "<prompt>" --model claude-sonnet-5-5 --permission-mode acceptEdits --allowedTools "Bash,Read,Edit,Write,Glob,Grep" --output-format json < /dev/null
     ```
   - GPT 線（參數以 `codex exec --help` 為準）：
     ```bash
     codex exec --json --full-auto --skip-git-repo-check "<prompt>" < /dev/null
     ```
3. 模型：Claude 線固定 `claude-sonnet-5-5`，和上次測試一致；GPT 線固定使用者平常用的 GPT 模型，A、B 兩組必須相同，不能混用。
4. 每個任務跑 2 輪。B 組第 1 輪會先建立 `./tools/` 工具腳本，第 2 輪重複使用，兩輪分開記錄。
5. 兩組可以平行跑，同一組內的任務依序跑。
6. 每個任務跑完後清理資料夾：新產生的 pptx、docx、pdf、xlsx 移到 `results/` 保存，其他新檔案（例如 README.md、文字擷取檔）刪除；保留原始 4 個檔案、CLAUDE.md、`tools/`。
7. 第 1 輪被視為「含建立工具的成本」，第 2 輪被視為「工具已存在時的成本」。

## 七、計算方式

**Claude 線**：從每次輸出的 JSON 讀取：

- **總 token**：`modelUsage` 底下所有模型的 `inputTokens + cacheReadInputTokens + cacheCreationInputTokens + outputTokens` 加總
- **回合數**：`num_turns`
- **費用估算**：`total_cost_usd`（牌價估算，不是實際帳單）

**GPT 線**：從每次輸出的 JSONL 讀取所有 `turn.completed` 事件的 `usage`：

- **總 token**：`input_tokens + output_tokens` 加總（`cached_input_tokens` 已包含在 `input_tokens` 裡，另外記錄，不重複加）
- **回合數**：工具呼叫事件的次數
- 若 Codex 版本的事件名稱或欄位不同，以實際輸出為準，並在回報中註明

## 八、驗證標準

一筆數據要同時符合以下條件才算有效：

1. 沒有執行錯誤：Claude 線的 `is_error` 是 `false`；GPT 線沒有 `error` 事件。
2. `result` 沒有出現「hit your」「limit」這類用量上限訊息；若有，標記為「額度不足」，等額度恢復後只重跑那一筆。
3. 回覆沒有出現「還沒收到開始指令」這類拒絕；若有，標記為「被規則擋下」。
4. 結果正確：

| 任務 | 正確標準 |
|---|---|
| pptxQ | 列出第 3 張的文字，包含「市場規模」「2,073 家」「443 億」「8,335 家」「24.6 億」 |
| pptxM | 新的 pptx 第 3 張標題是「市場規模與成長」，原檔未變 |
| docxQ | 找到 14 個提到 NotebookLM 的段落（段落編號方式可以不同） |
| docxM | 新的 docx 含「教學社工如何使用 NotebookLM」，最後一段是「本文件僅供參考。」 |
| pdfQ | 找到第 1 頁與第 5 頁 |
| pdfM | 新的 pdf 剛好 3 頁 |
| xlsxQ | 38 個工作表，合計 2,518 筆 |
| xlsxM | 新的 xlsx 第一個工作表新增「備註」欄，49 筆資料填入「待確認」 |

修改任務可用第十節的 `ab_report.py` 自動驗證；查詢任務由執行者比對 `result` 文字。

## 九、回報格式

1. 每個任務：A 組與 B 組各輪的總 token、回合數、是否有效
2. 每種檔案：查詢＋修改的平均，B 相對 A 的差異百分比
3. 全部 8 個任務合計的差異百分比
4. 無效或重跑的數據清單與原因
5. 第 1 輪與第 2 輪分開列出

每條線分開回報。

Claude 線上一版指令的乾淨數據（第 2 輪，Sonnet 5.5）可供對照，GPT 線沒有對照數據：

| 任務 | A 組 | B 組（上一版指令） |
|---|---|---|
| pptxQ | 154,144 | 190,549 |
| pptxM | 565,711 | 397,353 |
| docxQ | 134,215 | 240,139 |
| docxM | 307,420 | 292,431 |
| pdfQ | 221,981 | 237,724 |
| pdfM | 132,887 | 240,950 |
| xlsxQ | 236,845 | 282,624 |
| xlsxM | 547,026 | 476,360 |

## 十、Claude 線腳本（只扣 Claude 額度）

### ab_test_claude.sh（執行測試）

```bash
#!/bin/bash
# 用法: ./ab_test_claude.sh <根目錄>/claude [輪數，預設 2]
# 這個資料夾底下要先準備好 A、B 兩個資料夾（各有 CLAUDE.md 與 4 個測試檔）
set -u
ROOT=$1; ROUNDS=${2:-2}; MODEL=${MODEL:-claude-sonnet-5-5}
TASKS=(pptxQ pptxM docxQ docxM pdfQ pdfM xlsxQ xlsxM)
declare -A P
P[pptxQ]='開始。簡報.pptx 第 3 張投影片上有哪些文字?條列出來。'
P[pptxM]='開始。修改 簡報.pptx:把第 3 張投影片的標題改成「市場規模與成長」,另存成新檔。'
P[docxQ]='開始。報告.docx 裡哪些段落提到「NotebookLM」?只列出段落編號與一句摘要。'
P[docxM]='開始。修改 報告.docx:把「教學社工使用NotebookLM」這一段改成「教學社工如何使用 NotebookLM」,並在文件最後新增一段「本文件僅供參考。」,另存成新檔。'
P[pdfQ]='開始。計劃書.pdf 哪幾頁提到「檢索」?列出頁碼與一句摘要。'
P[pdfM]='開始。把 計劃書.pdf 的第 1 到 3 頁另存成一個新的 PDF。'
P[xlsxQ]='開始。書目.xlsx 有幾個工作表?每個工作表各有幾筆有編號的資料?'
P[xlsxM]='開始。修改 書目.xlsx:在第一個工作表最後一欄後面新增一欄「備註」,每一筆有編號的資料都填入「待確認」,另存成新檔。'
mkdir -p "$ROOT/results"
for c in A B; do (
  D="$ROOT/$c"
  for r in $(seq 1 "$ROUNDS"); do for t in "${TASKS[@]}"; do
    out="$ROOT/results/$c.$t.$r.json"
    [ -s "$out" ] && grep -q '"is_error":false' "$out" && continue   # 已有有效結果就跳過，方便額度不足後續跑
    (cd "$D" && claude -p "${P[$t]}" --model "$MODEL" --permission-mode acceptEdits \
      --allowedTools "Bash,Read,Edit,Write,Glob,Grep" --output-format json < /dev/null 2>/dev/null) > "$out"
    for f in "$D"/*; do
      n=$(basename "$f")
      case "$n" in
        CLAUDE.md|AGENTS.md|tools|簡報.pptx|報告.docx|計劃書.pdf|書目.xlsx) ;;
        *.pptx|*.docx|*.pdf|*.xlsx) mv "$f" "$ROOT/results/$c.$t.$r.$n" ;;
        *) rm -rf "$f" ;;
      esac
    done
    echo "$c $t 第$r輪 完成"
  done; done ) & done
wait
echo "全部完成"
```

### ab_report.py（彙整與驗證，兩條線共用）

```python
# 用法: python ab_report.py <根目錄>/claude/results   或   python ab_report.py <根目錄>/gpt/results
import json, sys, glob, os, re
R = sys.argv[1]
TASKS = ['pptxQ','pptxM','docxQ','docxM','pdfQ','pdfM','xlsxQ','xlsxM']

def load(f):
    # Claude 線是單一 JSON；GPT 線是 JSONL 事件流，轉成同樣的欄位
    txt = open(f, encoding='utf-8').read()
    try:
        return json.loads(txt)
    except Exception:
        tok, turns, err, msgs = 0, 0, False, []
        for line in txt.splitlines():
            try: e = json.loads(line)
            except Exception: continue
            ty = e.get('type', '')
            if ty == 'turn.completed':
                u = e.get('usage', {}); tok += u.get('input_tokens', 0) + u.get('output_tokens', 0)
            if ty == 'error' or ty == 'turn.failed': err = True
            it = e.get('item', {})
            if ty == 'item.completed' and it.get('type') in ('command_execution', 'file_change', 'mcp_tool_call'): turns += 1
            if ty == 'item.completed' and it.get('type') == 'agent_message': msgs.append(it.get('text', ''))
        return {'_total': tok, 'num_turns': turns, 'is_error': err, 'result': '\n'.join(msgs)}

def total(d):
    if '_total' in d: return d['_total']
    return sum(v['inputTokens']+v['cacheReadInputTokens']+v['cacheCreationInputTokens']+v['outputTokens']
               for v in d.get('modelUsage', {}).values())

def check_file(task, path):
    try:
        if task == 'pptxM':
            from pptx import Presentation
            s = Presentation(path).slides[2]
            return any('市場規模與成長' in sh.text_frame.text for sh in s.shapes if sh.has_text_frame)
        if task == 'docxM':
            from docx import Document
            ps = [p.text.strip() for p in Document(path).paragraphs if p.text.strip()]
            return any('教學社工如何使用 NotebookLM' in p for p in ps) and ps[-1] == '本文件僅供參考。'
        if task == 'pdfM':
            from pypdf import PdfReader
            return len(PdfReader(path).pages) == 3
        if task == 'xlsxM':
            import openpyxl
            ws = openpyxl.load_workbook(path).worksheets[0]
            cols = [c.column for c in ws[1] if c.value == '備註']
            return any(sum(1 for row in ws.iter_rows(min_row=2, min_col=k, max_col=k) if row[0].value == '待確認') == 49 for k in cols)
    except Exception as e:
        return f'驗證失敗: {e}'
    return None

rows = {}
for f in sorted(glob.glob(os.path.join(R, '*.json')) + glob.glob(os.path.join(R, '*.jsonl'))):
    c, t, r = os.path.basename(f).split('.')[:3]
    try:
        d = load(f)
    except Exception:
        rows[(c, t, r)] = (0, 0, '讀取失敗'); continue
    res = str(d.get('result', ''))
    if d.get('is_error') or re.search(r'hit your .*limit', res): status = '額度不足或錯誤'
    elif '還沒收到開始' in res or ('開始指令' in res and len(res) < 400): status = '被規則擋下'
    else:
        status = '待人工確認'
        outs = glob.glob(os.path.join(R, f'{c}.{t}.{r}.*'))
        outs = [o for o in outs if not o.endswith(('.json', '.jsonl'))]
        if t.endswith('M'):
            ok = [check_file(t, o) for o in outs]
            status = '有效' if True in ok else f'修改結果不正確 {ok}'
    rows[(c, t, r)] = (total(d), d.get('num_turns'), status)

print('| 任務 | 輪 | A 總 token | A 回合 | A 狀態 | B 總 token | B 回合 | B 狀態 | 差異 |')
print('|---|---|---|---|---|---|---|---|---|')
for t in TASKS:
    for r in ['1', '2']:
        a = rows.get(('A', t, r)); b = rows.get(('B', t, r))
        if not a or not b: continue
        diff = f'{(b[0]-a[0])/a[0]*100:+.1f}%' if a[0] else '—'
        print(f'| {t} | {r} | {a[0]:,} | {a[1]} | {a[2]} | {b[0]:,} | {b[1]} | {b[2]} | {diff} |')
```

## 十一、GPT 線腳本（只扣 GPT 額度）

### ab_test_gpt.sh（執行測試）

```bash
#!/bin/bash
# 用法: ./ab_test_gpt.sh <根目錄>/gpt [輪數，預設 2]
# 這個資料夾底下要先準備好 A、B 兩個資料夾（各有 AGENTS.md 與 4 個測試檔）
# 全程只呼叫 codex，不呼叫 claude
set -u
ROOT=$1; ROUNDS=${2:-2}
TASKS=(pptxQ pptxM docxQ docxM pdfQ pdfM xlsxQ xlsxM)
declare -A P
P[pptxQ]='開始。簡報.pptx 第 3 張投影片上有哪些文字?條列出來。'
P[pptxM]='開始。修改 簡報.pptx:把第 3 張投影片的標題改成「市場規模與成長」,另存成新檔。'
P[docxQ]='開始。報告.docx 裡哪些段落提到「NotebookLM」?只列出段落編號與一句摘要。'
P[docxM]='開始。修改 報告.docx:把「教學社工使用NotebookLM」這一段改成「教學社工如何使用 NotebookLM」,並在文件最後新增一段「本文件僅供參考。」,另存成新檔。'
P[pdfQ]='開始。計劃書.pdf 哪幾頁提到「檢索」?列出頁碼與一句摘要。'
P[pdfM]='開始。把 計劃書.pdf 的第 1 到 3 頁另存成一個新的 PDF。'
P[xlsxQ]='開始。書目.xlsx 有幾個工作表?每個工作表各有幾筆有編號的資料?'
P[xlsxM]='開始。修改 書目.xlsx:在第一個工作表最後一欄後面新增一欄「備註」,每一筆有編號的資料都填入「待確認」,另存成新檔。'
mkdir -p "$ROOT/results"
for c in A B; do (
  D="$ROOT/$c"
  for r in $(seq 1 "$ROUNDS"); do for t in "${TASKS[@]}"; do
    out="$ROOT/results/$c.$t.$r.jsonl"
    [ -s "$out" ] && grep -q '"turn.completed"' "$out" && continue   # 已有有效結果就跳過
    (cd "$D" && codex exec --json --full-auto --skip-git-repo-check "${P[$t]}" < /dev/null 2>/dev/null) > "$out"
    for f in "$D"/*; do
      n=$(basename "$f")
      case "$n" in
        CLAUDE.md|AGENTS.md|tools|簡報.pptx|報告.docx|計劃書.pdf|書目.xlsx) ;;
        *.pptx|*.docx|*.pdf|*.xlsx) mv "$f" "$ROOT/results/$c.$t.$r.$n" ;;
        *) rm -rf "$f" ;;
      esac
    done
    echo "$c $t 第$r輪 完成"
  done; done ) & done
wait
echo "全部完成"
```

彙整同樣使用第十節的 `ab_report.py`，路徑改成 `<根目錄>/gpt/results`。

## 十二、建議的執行順序

**Claude 線**（使用者或 Claude 執行）：
1. 移開 `~/.claude/CLAUDE.md`。
2. 建立 `<根目錄>/claude/A`、`<根目錄>/claude/B`，放入各自的 CLAUDE.md 與 4 個測試檔。
3. 執行 `./ab_test_claude.sh <根目錄>/claude 2`。
4. 若中途額度不足，等額度恢復後再執行一次同樣的指令，腳本會跳過已成功的部分。
5. 執行 `python ab_report.py <根目錄>/claude/results`，再人工比對查詢任務的答案。
6. 把 `~/.claude/CLAUDE.md` 放回去。

**GPT 線**（GPT 執行）：
1. 移開 `~/.codex/AGENTS.md`。
2. 建立 `<根目錄>/gpt/A`、`<根目錄>/gpt/B`，放入各自的 AGENTS.md 與 4 個測試檔。
3. 執行 `./ab_test_gpt.sh <根目錄>/gpt 2`。
4. 若中途額度不足，等額度恢復後再執行一次同樣的指令。
5. 執行 `python ab_report.py <根目錄>/gpt/results`，再人工比對查詢任務的答案。
6. 把 `~/.codex/AGENTS.md` 放回去。

兩條線可以同時跑，互不影響。

預估用量（Claude 線）：上次 16 次乾淨數據合計約 470 萬 token（牌價約 $4.7）；跑 2 輪共 32 次，約需 900 萬到 1,000 萬 token，可能需要分兩個 5 小時額度跑完。GPT 線沒有過去數據，無法預估。
