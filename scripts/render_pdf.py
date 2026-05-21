"""
render_pdf.py - Render a PDF (pitch deck / CIM) to one PNG per page for visual analysis.

Why this exists:
  On Windows the Claude Code Read tool fails on PDFs (`pdftoppm` is not installed).
  Investor decks and CIMs are also graphics-heavy, so plain text extraction (PyPDF2)
  misses most slides and can be actively misleading (hidden template text layers,
  e.g. lorem ipsum sitting behind real content). Rendered page images are the
  source of truth - Read the PNGs this script produces.

Usage:
  python render_pdf.py "C:\\path\\to\\deck.pdf"
  python render_pdf.py "C:\\path\\to\\deck.pdf" --out "C:\\some\\dir" --dpi 150

Requires: pymupdf (auto-installed on first run if missing).
"""
import argparse
import os
import subprocess
import sys
import tempfile


def ensure_pymupdf():
    """Install pymupdf on first use if it is not already available."""
    try:
        import pymupdf  # noqa: F401
    except ImportError:
        print("pymupdf not found - installing via pip...", flush=True)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--quiet", "pymupdf"]
        )


def main():
    parser = argparse.ArgumentParser(
        description="Render a PDF to one PNG per page for visual analysis."
    )
    parser.add_argument("pdf", help="Path to the PDF file")
    parser.add_argument(
        "--out",
        help="Output directory (default: <system temp>\\<pdf name>_pages)",
    )
    parser.add_argument(
        "--dpi", type=int, default=130, help="Render resolution in DPI (default: 130)"
    )
    args = parser.parse_args()

    pdf_path = os.path.abspath(args.pdf)
    if not os.path.isfile(pdf_path):
        sys.exit(f"ERROR: file not found: {pdf_path}")

    ensure_pymupdf()
    import pymupdf

    base = os.path.splitext(os.path.basename(pdf_path))[0]
    out_dir = (
        os.path.abspath(args.out)
        if args.out
        else os.path.join(tempfile.gettempdir(), f"{base}_pages")
    )
    os.makedirs(out_dir, exist_ok=True)

    doc = pymupdf.open(pdf_path)
    page_count = len(doc)
    pad = max(2, len(str(page_count)))
    for i, page in enumerate(doc):
        png_path = os.path.join(out_dir, f"p{i + 1:0{pad}d}.png")
        page.get_pixmap(dpi=args.dpi).save(png_path)
    doc.close()

    print(f"Rendered {page_count} page(s) at {args.dpi} DPI to:")
    print(f"  {out_dir}")
    print(
        f"Now Read the page images: "
        f"p{'1'.zfill(pad)}.png ... p{str(page_count).zfill(pad)}.png"
    )


if __name__ == "__main__":
    main()
