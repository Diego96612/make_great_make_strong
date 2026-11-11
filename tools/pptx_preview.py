"""用 LibreOffice headless 轉 PDF，只渲染指定頁，拼成單張 480px 寬縮圖的格狀圖。
用法：python pptx_preview.py <file> <輸出png> <頁碼...>"""
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

THUMB_W, COLS = 480, 3


def main():
    src, out, pages = Path(sys.argv[1]), Path(sys.argv[2]), [int(p) for p in sys.argv[3:]]
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmp, str(src)],
                       check=True, capture_output=True)
        pdf = Path(tmp) / (src.stem + ".pdf")
        thumbs = []
        for p in pages:
            prefix = Path(tmp) / f"p{p}"
            subprocess.run(["pdftoppm", "-png", "-f", str(p), "-l", str(p), "-scale-to-x", str(THUMB_W),
                            "-scale-to-y", "-1", "-singlefile", str(pdf), str(prefix)], check=True)
            thumbs.append(Image.open(f"{prefix}.png").convert("RGB"))
    th = thumbs[0].height
    cols = min(COLS, len(thumbs))
    rows = (len(thumbs) + cols - 1) // cols
    grid = Image.new("RGB", (cols * THUMB_W + (cols - 1) * 8, rows * th + (rows - 1) * 8), "white")
    for k, im in enumerate(thumbs):
        grid.paste(im, ((k % cols) * (THUMB_W + 8), (k // cols) * (th + 8)))
    grid.save(out)
    print(out)


if __name__ == "__main__":
    main()
