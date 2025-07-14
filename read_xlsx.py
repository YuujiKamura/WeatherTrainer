#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel(.xlsx/.xls)ファイルを読み取るスクリプト
"""

import sys
import pandas as pd
import argparse
from pathlib import Path
import io

# Windows環境での日本語出力対応
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def read_excel_file(file_path, sheet_name=None, header=0):
    """
    Excelファイルを読み取り、内容を表示する
    
    Args:
        file_path (str): Excelファイルのパス
        sheet_name (str): シート名（指定しない場合は最初のシート）
        header (int): ヘッダー行の番号（0-indexed）
    """
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"エラー: ファイルが見つかりません: {file_path}")
            return
        
        # Excelファイルを読み込み
        if sheet_name:
            df = pd.read_excel(file_path, sheet_name=sheet_name, header=header)
            print(f"ファイル: {file_path}")
            print(f"シート: {sheet_name}")
        else:
            df = pd.read_excel(file_path, header=header)
            print(f"ファイル: {file_path}")
            print(f"シート: デフォルト（最初のシート）")
        
        print(f"行数: {len(df)}, 列数: {len(df.columns)}")
        print("-" * 50)
        
        # データフレームを表示（日本語文字化け対策）
        try:
            print(df.to_string())
        except UnicodeEncodeError:
            # 文字化けする場合は最初の10行だけ表示
            print("文字エンコーディングの問題により、最初の10行のみ表示:")
            print(df.head(10).to_string(max_colwidth=50))
        
    except Exception as e:
        print(f"エラー: {e}")

def list_sheets(file_path):
    """
    Excelファイルの全シート名を表示する
    
    Args:
        file_path (str): Excelファイルのパス
    """
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"エラー: ファイルが見つかりません: {file_path}")
            return
        
        # シート名一覧を取得
        xl_file = pd.ExcelFile(file_path)
        print(f"ファイル: {file_path}")
        print("利用可能なシート:")
        for i, sheet in enumerate(xl_file.sheet_names):
            print(f"  {i+1}. {sheet}")
            
    except Exception as e:
        print(f"エラー: {e}")

def main():
    parser = argparse.ArgumentParser(description='Excelファイルを読み取るスクリプト')
    parser.add_argument('file_path', help='Excelファイルのパス')
    parser.add_argument('-s', '--sheet', help='読み取るシート名')
    parser.add_argument('-l', '--list', action='store_true', help='シート一覧を表示')
    parser.add_argument('--header', type=int, default=0, help='ヘッダー行の番号（デフォルト: 0）')
    
    args = parser.parse_args()
    
    if args.list:
        list_sheets(args.file_path)
    else:
        read_excel_file(args.file_path, args.sheet, args.header)

if __name__ == "__main__":
    main()