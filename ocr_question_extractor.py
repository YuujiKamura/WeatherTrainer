#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
気象予報士試験PDFから指定した問題をOCRで抽出するスクリプト
"""

import sys
import os
import re
from pathlib import Path

# DocumentAIOCRモジュールのパスを追加
sys.path.append(r'C:\Users\yuuji\app_pdfocr')

from ocr_tools.document_ai_ocr import DocumentAIOCR

def extract_question_text(all_text, question_num):
    """
    全テキストから指定した問題番号の問題文を抽出する
    
    Args:
        all_text (str): OCRで抽出した全テキスト
        question_num (int): 抽出したい問題番号
    
    Returns:
        tuple: (問題が見つかったかどうか, 問題文)
    """
    lines = all_text.split('\n')
    question_found = False
    question_text = ""
    
    # 問題番号のパターンを複数用意
    patterns = [
        f"問{question_num}",
        f"問 {question_num}",
        f"問{question_num:02d}",  # 01, 02のようなゼロ埋め
        f"問 {question_num:02d}"
    ]
    
    for i, line in enumerate(lines):
        # いずれかのパターンにマッチするかチェック
        if any(pattern in line for pattern in patterns):
            question_found = True
            # 問題文を抽出（次の問題まで、または最大30行まで）
            for j in range(i, min(i + 30, len(lines))):
                question_text += lines[j] + "\n"
                # 次の問題番号が見つかったら終了
                next_num = question_num + 1
                next_patterns = [
                    f"問{next_num}",
                    f"問 {next_num}",
                    f"問{next_num:02d}",
                    f"問 {next_num:02d}"
                ]
                if j > i and any(pattern in lines[j] for pattern in next_patterns):
                    break
            break
    
    return question_found, question_text

def main():
    # コマンドライン引数の処理
    if len(sys.argv) < 2:
        print("使用方法: python ocr_question_extractor.py <問題番号> [PDFファイルパス]")
        print("例: python ocr_question_extractor.py 13")
        print("例: python ocr_question_extractor.py 5 過去問一般/i62gakka(ippan).pdf")
        return
    
    try:
        question_num = int(sys.argv[1])
    except ValueError:
        print("問題番号は数値で指定してください")
        return
    
    # PDFファイルパスの設定
    if len(sys.argv) >= 3:
        pdf_path = sys.argv[2]
    else:
        pdf_path = "過去問一般/i63gakka(ippan).pdf"  # デフォルト
    
    if not os.path.exists(pdf_path):
        print(f"PDFファイルが見つかりません: {pdf_path}")
        return
    
    # DocumentAI OCRを初期化
    ocr = DocumentAIOCR()
    
    try:
        print(f"PDFをOCR処理中: {pdf_path}")
        # PDFからテキストを抽出
        ocr_results, expiry_date = ocr.extract_text_and_expiry_date_from_pdf(pdf_path)
        
        if not ocr_results:
            print("OCR処理に失敗しました")
            return
        
        print(f"OCR処理完了。{len(ocr_results)}ページ処理されました。")
        
        # 全ページのテキストを結合
        all_text = ""
        for page_num, page_data in ocr_results.items():
            if "elements" in page_data:
                for element in page_data["elements"]:
                    all_text += element.get("text", "") + "\n"
        
        # 指定した問題を抽出
        question_found, question_text = extract_question_text(all_text, question_num)
        
        if question_found:
            print(f"\n=== 問{question_num} ===")
            print(question_text)
            print(f"\n=== 問{question_num}の抽出完了 ===")
        else:
            print(f"問{question_num}が見つかりませんでした。")
            print("\n利用可能な問題番号を確認するため、全テキストの一部を表示します：")
            # 問題番号らしきパターンを抽出
            problem_lines = []
            for line in all_text.split('\n'):
                if re.search(r'問\s*\d+', line):
                    problem_lines.append(line.strip())
            
            if problem_lines:
                print("見つかった問題番号:")
                for line in problem_lines[:10]:  # 最初の10個まで表示
                    print(f"  {line}")
            else:
                print("問題番号のパターンが見つかりませんでした。")
                print("全テキストの最初の1000文字:")
                print(all_text[:1000])
            
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 