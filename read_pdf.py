#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDFファイルを読み取るスクリプト
"""

import sys
import argparse
from pathlib import Path
import io

# Windows環境での日本語出力対応
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

try:
    import fitz  # PyMuPDF
    PDF_AVAILABLE = True
except ImportError:
    try:
        import PyPDF2
        PDF_AVAILABLE = True
        USE_PYPDF2 = True
    except ImportError:
        PDF_AVAILABLE = False

def read_pdf_with_pymupdf(file_path, page_start=0, page_end=None):
    """PyMuPDFでPDFを読み取り"""
    doc = fitz.open(file_path)
    text = ""
    
    if page_end is None:
        page_end = len(doc)
    
    for page_num in range(page_start, min(page_end, len(doc))):
        page = doc[page_num]
        text += f"\n--- ページ {page_num + 1} ---\n"
        text += page.get_text()
    
    doc.close()
    return text

def read_pdf_with_pypdf2(file_path, page_start=0, page_end=None):
    """PyPDF2でPDFを読み取り"""
    text = ""
    
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        if page_end is None:
            page_end = len(reader.pages)
        
        for page_num in range(page_start, min(page_end, len(reader.pages))):
            page = reader.pages[page_num]
            text += f"\n--- ページ {page_num + 1} ---\n"
            text += page.extract_text()
    
    return text

def read_pdf_file(file_path, page_start=0, page_end=None, max_chars=5000):
    """
    PDFファイルを読み取り、内容を表示する
    
    Args:
        file_path (str): PDFファイルのパス
        page_start (int): 開始ページ（0-indexed）
        page_end (int): 終了ページ（指定しない場合は最後まで）
        max_chars (int): 最大表示文字数
    """
    if not PDF_AVAILABLE:
        print("エラー: PDFライブラリがインストールされていません")
        print("以下のコマンドでインストールしてください:")
        print("pip install PyMuPDF  # または pip install PyPDF2")
        return
    
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"エラー: ファイルが見つかりません: {file_path}")
            return
        
        print(f"ファイル: {file_path}")
        
        # PyMuPDFを優先して使用
        if 'fitz' in sys.modules:
            text = read_pdf_with_pymupdf(file_path, page_start, page_end)
            print("ライブラリ: PyMuPDF")
        else:
            text = read_pdf_with_pypdf2(file_path, page_start, page_end)
            print("ライブラリ: PyPDF2")
        
        if page_end:
            print(f"ページ範囲: {page_start + 1} - {page_end}")
        else:
            print(f"開始ページ: {page_start + 1}")
        
        print("-" * 50)
        
        # 文字数制限
        if len(text) > max_chars:
            text = text[:max_chars] + f"\n\n... (残り {len(text) - max_chars} 文字は省略されました)"
        
        print(text)
        
    except Exception as e:
        print(f"エラー: {e}")

def main():
    parser = argparse.ArgumentParser(description='PDFファイルを読み取るスクリプト')
    parser.add_argument('file_path', help='PDFファイルのパス')
    parser.add_argument('-s', '--start', type=int, default=0, help='開始ページ（1から始まる）')
    parser.add_argument('-e', '--end', type=int, help='終了ページ')
    parser.add_argument('-m', '--max-chars', type=int, default=5000, help='最大表示文字数（デフォルト: 5000）')
    
    args = parser.parse_args()
    
    # ページ番号を0-indexedに変換
    page_start = max(0, args.start - 1) if args.start > 0 else 0
    page_end = args.end if args.end else None
    
    read_pdf_file(args.file_path, page_start, page_end, args.max_chars)

if __name__ == "__main__":
    main()