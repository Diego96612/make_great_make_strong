"""每個非空 shape 輸出一行：shape_id、type、name、前 40 字；表格逐格輸出。
用法：python pptx_dump.py <file> [slide 頁碼...]"""
import sys
from pptx import Presentation


def main():
    path, pages = sys.argv[1], {int(p) for p in sys.argv[2:]}
    prs = Presentation(path)
    for i, slide in enumerate(prs.slides, 1):
        if pages and i not in pages:
            continue
        print(f"--- slide {i} ---")
        for sh in slide.shapes:
            if sh.has_table:
                for r, row in enumerate(sh.table.rows):
                    for c, cell in enumerate(row.cells):
                        if cell.text.strip():
                            print(f"{sh.shape_id}\ttable[{r},{c}]\t{sh.name}\t{cell.text.strip()[:40]}")
            elif sh.has_text_frame and sh.text_frame.text.strip():
                text = sh.text_frame.text.strip().replace("\n", " / ")
                print(f"{sh.shape_id}\t{sh.shape_type}\t{sh.name}\t{text[:40]}")
            elif sh.shape_type is not None and not sh.has_text_frame:
                print(f"{sh.shape_id}\t{sh.shape_type}\t{sh.name}\t")


if __name__ == "__main__":
    main()
