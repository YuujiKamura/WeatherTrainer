#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDFから画像を抽出し、特定ページをPNG画像として保存するスクリプト
"""

import sys
import fitz  # PyMuPDF
from pathlib import Path
import argparse

def extract_page_as_image(pdf_path, page_num, output_dir="extracted_images", dpi=150):
    """
    PDFの特定ページを画像として抽出
    
    Args:
        pdf_path (str): PDFファイルのパス
        page_num (int): ページ番号（1から始まる）
        output_dir (str): 出力ディレクトリ
        dpi (int): 解像度
    """
    try:
        # PDFを開く
        doc = fitz.open(pdf_path)
        
        # ページ番号を0ベースに変換
        page_index = page_num - 1
        
        if page_index >= len(doc) or page_index < 0:
            print(f"エラー: ページ {page_num} は存在しません（全{len(doc)}ページ）")
            return None
        
        # ページを取得
        page = doc[page_index]
        
        # 解像度設定（DPIを指定）
        mat = fitz.Matrix(dpi/72, dpi/72)  # 72 DPI がデフォルト
        
        # ページを画像として取得
        pix = page.get_pixmap(matrix=mat)
        
        # PDF名でサブフォルダを作成
        pdf_name = Path(pdf_path).stem
        output_path = Path(output_dir) / pdf_name
        output_path.mkdir(parents=True, exist_ok=True)
        
        # ファイル名を生成
        image_file = output_path / f"{pdf_name}_page{page_num}.png"
        
        # 画像を保存
        pix.save(str(image_file))
        
        print(f"画像を保存しました: {image_file}")
        print(f"解像度: {pix.width} x {pix.height} pixels")
        
        doc.close()
        return str(image_file)
        
    except Exception as e:
        print(f"エラー: {e}")
        return None

def extract_multiple_pages(pdf_path, start_page, end_page, output_dir="extracted_images", dpi=150):
    """
    複数ページを一括で画像抽出
    """
    extracted_files = []
    
    for page_num in range(start_page, end_page + 1):
        image_file = extract_page_as_image(pdf_path, page_num, output_dir, dpi)
        if image_file:
            extracted_files.append(image_file)
    
    return extracted_files

def main():
    parser = argparse.ArgumentParser(description='PDFから画像を抽出するスクリプト')
    parser.add_argument('pdf_path', help='PDFファイルのパス')
    parser.add_argument('-p', '--page', type=int, help='抽出するページ番号（1から始まる）')
    parser.add_argument('-s', '--start', type=int, help='開始ページ')
    parser.add_argument('-e', '--end', type=int, help='終了ページ')
    parser.add_argument('-d', '--dpi', type=int, default=150, help='解像度（DPI、デフォルト: 150）')
    parser.add_argument('-o', '--output', default='extracted_images', help='出力ディレクトリ')
    
    args = parser.parse_args()
    
    if not Path(args.pdf_path).exists():
        print(f"エラー: ファイルが見つかりません: {args.pdf_path}")
        return
    
    if args.page:
        # 単一ページ抽出
        extract_page_as_image(args.pdf_path, args.page, args.output, args.dpi)
    elif args.start and args.end:
        # 複数ページ抽出
        extract_multiple_pages(args.pdf_path, args.start, args.end, args.output, args.dpi)
    else:
        print("ページ番号（-p）または範囲（-s と -e）を指定してください")

if __name__ == "__main__":
    main()