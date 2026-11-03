# 省 token 方法庫（F 辦公檔案修改、G 寫作）

這份是參考資料，不放進 CLAUDE.md，避免每次請求都重送。


## 使用說明

- 處理 docx、pptx、xlsx、pdf 或寫作任務時，套用本節。
- 「通用方法」只收錄 F、G 兩區用到的 16 條（編號沿用完整版 U01–U50，所以不連號），每條附文獻來源（S 編號）。
- 「專屬技巧」是把通用方法套用到該項工作的具體做法；若技巧本身有直接文獻，會另外標 S 編號。
- 標「—」表示沒有適用的通用方法，屬於一般操作經驗。

## 通用方法

| 編號 | 方法 | 來源 |
|---|---|---|
| U01 | 換到不相關的任務時，用 `/clear` 開新對話，舊歷史不再每次重送 | S2, S3 |
| U15 | 圖片和 PDF 不要累積太多，截圖只截關鍵區域，舊圖不重複貼 | S4 |
| U16 | 寫具體的 prompt：指出檔案、描述症狀、說明「完成」長什麼樣子，避免 AI 大範圍掃描 | S2, S3 |
| U17 | 用 `@路徑` 直接引用檔案，或指定一個現有範本讓 AI 仿照，省去搜尋 | S3 |
| U18 | 提供驗證目標（測試、預期輸出、截圖），讓 AI 自己檢查，減少你回頭要求修正的輪數 | S2, S3 |
| U19 | 複雜任務先用 plan mode 或先列大綱，確認方向再執行，避免整個重做 | S2, S3 |
| U23 | 只讀需要的範圍，例如指定行號、用 head、tail，不載入整份檔案 | S6, S14 |
| U24 | 先看大綱、目錄或索引，再只展開需要的部分 | S6, S15 |
| U28 | 同一份內容只讀一次，重點寫進筆記，之後讀筆記 | S6 |
| U30 | 只輸出差異或局部修改，不重寫整份檔案 | S14, S16 |
| U31 | 回覆精簡，不寫開場白與過程敘述 | S16 |
| U32 | 固定精簡的回報格式（條列、表格、JSON） | S5, S16 |
| U35 | 確定性的工作（排序、轉檔、計算、取代）交給腳本，只回傳結果 | S7, S8 |
| U36 | 大量資料在執行環境裡先篩選、彙總，模型只看結果 | S7 |
| U46 | 可重複的處理寫成腳本放進 skill，執行時腳本本身不進 context | S8 |
| U47 | 重要知識與進度寫進檔案（筆記、索引、待辦），下次先讀檔案，不重新探索 | S6, S16 |

## 資料來源

| 編號 | 來源 |
|---|---|
| S2 | [Manage costs effectively](https://code.claude.com/docs/en/costs)（官方文件） |
| S3 | [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)（官方文件） |
| S4 | [How Claude Code uses prompt caching](https://code.claude.com/docs/en/prompt-caching)（官方文件） |
| S5 | [Run Claude Code programmatically](https://code.claude.com/docs/en/headless)（官方文件） |
| S6 | [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)（Anthropic 工程部落格） |
| S7 | [Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)（Anthropic 工程部落格，範例從約 150,000 降到約 2,000 token） |
| S8 | [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)（Anthropic 工程部落格） |
| S10 | [anthropics/skills](https://github.com/anthropics/skills)（官方 docx、pptx、xlsx、pdf 等 skills） |
| S14 | Yang et al., *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering*, NeurIPS 2024（[arXiv 2405.15793](https://arxiv.org/abs/2405.15793)） |
| S15 | Aider repo map 說明（[fast.io 第三方整理](https://fast.io/resources/aider-context-window/)，非官方來源） |
| S16 | [KINGSTAR-OMEGA/claude-token-optimizer](https://github.com/KINGSTAR-OMEGA/claude-token-optimizer)（社群 skill） |

來源限制：S14 是透過搜尋摘要確認的，這個環境擋住了 arxiv.org，沒有讀到全文；S15 是第三方整理；S16 是社群專案，不是學術或官方來源。

## F. 辦公檔案修改

| # | 工作項目 | 專屬技巧 | 通用方法 |
|---|---|---|---|
| F01 | 新建 Word 文件 | 寫一支 build script 跑一次完成 | U35 |
| F02 | 讀取並擷取 docx 內容 | 轉成帶段落編號的純文字大綱，不讀 XML | U24, U23 |
| F03 | 修改段落文字 | 用段落編號寫 patch，一次套用 | U30 |
| F04 | 尋找取代 | 用腳本取代，只回報命中次數 | U35, U32 |
| F05 | 修改表格內容 | 只 dump 那一張表格 | U23 |
| F06 | 插入或替換圖片 | 指定位置與檔案路徑，不讀圖片內容 | U23 |
| F07 | 加入目錄 | 用 Word 內建目錄欄位，不手動生成 | U35 |
| F08 | 設定標題層級 | 用內建樣式名稱，不逐段設字型 | U30 |
| F09 | 加頁碼 | 用頁碼欄位 | U35 |
| F10 | 加信頭 | 用範本 | U17 |
| F11 | 追蹤修訂 | 只在需要時開，平時關閉以免檔案膨脹 | — |
| F12 | 加註解 | 批次一次加 | U31 |
| F13 | 套用 Word 範本 | 套用範本，不重新設定格式 | U17 |
| F14 | 新建簡報 | build script 加 title、bullets、chart 等 helper | U35 |
| F15 | 擷取投影片文字 | 每個 shape 一行 dump | U24 |
| F16 | 修改投影片文字 | 用 shape_id 對應修改 | U30 |
| F17 | 調整版面 | 只改有問題的頁面 | U23 |
| F18 | 插入圖表 | 把資料交給腳本畫，不手動描述 | U35 |
| F19 | 插入圖片 | 指定檔案路徑 | U23 |
| F20 | 合併簡報 | 用腳本 | U35 |
| F21 | 分割簡報 | 用腳本 | U35 |
| F22 | 套用簡報範本 | 套用範本 | U17 |
| F23 | 修改版面配置 | 先只讀 layout 名稱清單 | U24 |
| F24 | 編寫講者備忘稿 | 只寫需要的頁 | U23 |
| F25 | 處理簡報註解 | 批次處理 | U31 |
| F26 | 轉成 PDF 預覽 | 只渲染改過的頁，低解析度拼成一張，只看一次 | U15 |
| F27 | 開啟並讀取試算表 | 先只看工作表名稱與前 5 列 | U24, U36 |
| F28 | 新增欄位 | 用 pandas 或 openpyxl 腳本 | U35 |
| F29 | 計算公式 | 一條公式套整欄，不逐格寫 | U35 |
| F30 | 修正公式錯誤 | 只列出錯誤的儲存格 | U36 |
| F31 | 格式化 | 對整個範圍套樣式 | U35 |
| F32 | 畫圖表 | 用腳本 | U35 |
| F33 | 清理雜亂資料 | 用腳本，只回報處理筆數 | U35, U36 |
| F34 | 從其他資料來源建立試算表 | 用腳本 | U35 |
| F35 | csv、tsv 格式互轉 | 用腳本 | U35 |
| F36 | 處理含巨集的 xlsm | 非必要不讀巨集程式碼 | U23 |
| F37 | 處理多個工作表 | 指定工作表名稱 | U23 |
| F38 | 樞紐分析 | 用 pandas pivot | U35 |
| F39 | 條件格式 | 用腳本 | U35 |
| F40 | 下拉選單 | 用腳本 | U35 |
| F41 | 擷取 PDF 文字 | 用 pdf 工具擷取 [S10] | U35 |
| F42 | 擷取 PDF 表格 | 用 pdfplumber 等工具 [S10] | U35 |
| F43 | 合併 PDF | 用腳本 | U35 |
| F44 | 分割 PDF | 用腳本 | U35 |
| F45 | 旋轉頁面 | 用腳本 | U35 |
| F46 | 加浮水印 | 用腳本 | U35 |
| F47 | 填寫 PDF 表單 | 用腳本擷取欄位，不把 PDF 載入 context [S8] | U46 |
| F48 | 加密解密 | 用腳本 | U35 |
| F49 | 擷取 PDF 圖片 | 用腳本，不看圖片 | U35 |
| F50 | OCR 掃描檔 | 用 OCR 工具輸出文字，不讓模型看圖 | U35, U15 |

## G. 寫作

| # | 工作項目 | 專屬技巧 | 通用方法 |
|---|---|---|---|
| G01 | 生成文章 | 先給大綱確認，再寫全文 | U19 |
| G02 | 寫心得 | 給重點素材與字數 | U16 |
| G03 | 寫計畫書 | 分章節寫，每章完成就存檔 | U47 |
| G04 | 寫報告 | 數據先整理好再給 | U16 |
| G05 | 寫論文段落 | 只給該段需要的參考資料 | U23 |
| G06 | 寫摘要 | 指定長度 | U16 |
| G07 | 寫 email | 一次給收件人、目的、語氣 | U16 |
| G08 | 寫會議紀錄 | 先用腳本清理逐字稿 | U36 |
| G09 | 寫新聞稿 | 用範本 | U17 |
| G10 | 寫社群貼文 | 一次要多則 | U31 |
| G11 | 寫廣告文案 | 指定字數與版本數 | U16 |
| G12 | 寫產品說明 | 給規格表 | U16 |
| G13 | 寫履歷 | 給條列式經歷 | U16 |
| G14 | 寫自傳 | 給條列式素材 | U16 |
| G15 | 寫求職信 | 只給職缺重點，不貼整頁 | U23 |
| G16 | 寫演講稿 | 指定時長 | U16 |
| G17 | 寫簡報講稿 | 只寫需要的頁 | U23 |
| G18 | 寫故事、小說 | 角色設定存檔，章節之間 `/clear` | U47, U01 |
| G19 | 寫詩 | 指定格式 | U16 |
| G20 | 寫劇本 | 角色與劇情設定存檔 | U47 |
| G21 | 潤飾文句 | 只回改動的地方 | U30 |
| G22 | 修正錯字與文法 | 只列錯誤與修正 | U30 |
| G23 | 改寫語氣 | 給一句範例 | U16 |
| G24 | 縮寫或擴寫 | 指定目標字數 | U16 |
| G25 | 評論並給修改建議 | 限制最多幾點 | U31 |
| G26 | 統一用詞 | 給對照表，用腳本取代 | U35 |
| G27 | 改成條列式 | — | U31 |
| G28 | 中英翻譯 | 只送要翻的段落，固定術語表 | U23, U47 |
| G29 | 繁簡轉換與在地化用語 | 用 OpenCC 等工具轉換，AI 只處理用語 | U35 |
| G30 | 寫標題 | 一次給多個選項 | U31 |
| G31 | 寫大綱 | 先大綱再內文 | U19 |
| G32 | 寫常見問題 | 給問題清單 | U16 |
| G33 | 寫使用手冊 | 從既有註解與文件整理 | U28 |
| G34 | 寫 README | 只給變更內容 | U23 |
| G35 | 寫 release notes | 從 git log 整理 | U36 |
| G36 | 寫技術文件 | 指定讀者程度 | U16 |
| G37 | 寫教學文章 | 用範本 | U17 |
| G38 | 寫比賽提案 | 把評分標準給它當驗證目標 | U18 |
| G39 | 寫申請書 | 依表格欄位逐項 | U32 |
| G40 | 寫公文 | 用範本 | U17 |
| G41 | 寫感謝函、邀請函 | 用範本 | U17 |
| G42 | 寫評論、書評 | 給重點 | U16 |
| G43 | 寫問卷題目 | 指定題型與數量 | U16 |
| G44 | 寫面試題目 | 指定職位與數量 | U16 |
| G45 | 寫介面文案 | 指定字數限制 | U16 |
| G46 | 寫 SEO 文章 | 給關鍵字清單 | U16 |
| G47 | 依範例模仿文風 | 只給一段短範例 | U16 |
| G48 | 寫多個版本供挑選 | 一次輸出 | U31 |
| G49 | 檢查引用與抄襲 | 用工具 | U35 |
| G50 | 依字數限制調整 | 用腳本計算字數 | U35 |
