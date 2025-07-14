
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## リポジトリ概要

これは気象予報士試験の個人学習用リポジトリです。以下の内容が含まれています：

- 過去問題集とその解答（0 過去問zip/, 過去問一般/, 過去問実技/, 過去問専門/）
- 学習進捗を追跡するExcelファイルとGoogleスプレッドシート
- 参考資料と気象現象の記録
- PDFから問題を抽出するPython OCRスクリプト

## 主要コマンド

### OCR問題抽出スクリプトの実行
```bash
python ocr_question_extractor.py <問題番号> [PDFファイルパス]
```

実行例：
```bash
# デフォルトPDFから問13を抽出
python ocr_question_extractor.py 13

# 特定のPDFから問5を抽出
python ocr_question_extractor.py 5 過去問一般/i62gakka(ippan).pdf
```

## ディレクトリ構造

- **0 申請用紙/**: 試験申込書類と関連文書
- **0 過去問zip/**: 試験回別の過去問アーカイブ（cwfe_XX_zフォルダ）
- **過去問一般/**: 学科一般の過去問と学習資料
- **過去問実技/**: 実技試験の過去問と演習資料
- **過去問専門/**: 学科専門の過去問
- **実地、印象的だった気象現象/**: 注目すべき気象現象の記録
- **気象予報士試験問題集/**: 問題集と参考資料
- **tmp_imgs/**: 画像処理用一時ファイル

## 主要ファイル

- `ocr_question_extractor.py`: PDF試験問題からOCRで特定問題を抽出するPythonスクリプト
- `※気象予報士試験.code-workspace`: VS Codeワークスペース設定
- 複数のExcelファイル: 学習進捗とスコア管理用
- `i63gakka(ippan)_visual_elements.json`: 試験問題のOCR処理結果

## アーキテクチャ

### OCR問題抽出スクリプト
メインスクリプト（`ocr_question_extractor.py`）は`C:\Users\yuuji\app_pdfocr`にある外部OCRモジュールに依存。機能：

1. DocumentAI OCRを使用してPDF試験問題からテキスト抽出
2. 複数パターン（問X, 問 X, 問XXなど）で特定問題番号を検索
3. 次の問題が見つかるまで問題文を抽出（最大30行）
4. 対象が見つからない場合は利用可能な問題番号を表示

### ファイル組織
以下の構造化されたアプローチに従う：
- 試験回と種類別に整理された過去問
- 科目別に分離された学習資料
- Excelスプレッドシートによる進捗追跡
- 分析用に別途保存された視覚要素と画像

## 依存関係

OCRスクリプトの要件：
- Python 3.x
- `C:\Users\yuuji\app_pdfocr`の外部OCRツールモジュール
- PDF文字抽出用DocumentAIOCRクラス

## 使用パターン

このリポジトリは主に以下の用途で使用：
1. 各科目の過去問学習
2. 集中学習用PDF問題の抽出
3. 学習進捗とスコアの追跡
4. 気象現象と天気パターンの分析
5. トピックと試験回別の参考資料整理