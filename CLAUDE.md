# WeatherTrainer

ClaudeCodeと学ぶ予報士試験2025

気象予報士試験の個人学習管理システム

## 概要

WeatherTrainerは気象予報士試験の効率的な学習をサポートするツールセットです。PDFからの問題・図版抽出、Excelによる学習管理、Claudeを活用した解説作成を行います。

## 主な機能

### 📚 学習管理
- 過去問題の体系的な整理・管理
- Excelによる学習進捗とスコアの追跡
- 問題解説の記録・蓄積

### 🔍 PDF問題抽出
PDFから直接問題文を読み取り・抽出
```bash
# PDFから直接問題を読み取り
python read_pdf.py 過去問一般/i63gakka(ippan).pdf -s 1 -e 5

# 特定ページの内容を表示
python read_pdf.py 過去問一般/i63gakka(ippan).pdf -s 3 -e 3 -m 2000
```

### 🖼️ 図版抽出
PDFから問題に関連する画像・図表を自動抽出
```bash
python extract_pdf_images.py
```

### 📊 Excel連携
- 学習記録の読み書き
- 成績データの管理・分析
- 間違った問題の特定

### 🤖 Claude解説生成
- 間違った問題をClaudeに提示
- 文字起こしと詳細解説の作成
- 理解を深めるための対話的学習

## ディレクトリ構成

```
WeatherTrainer/
├── 問題解説/                    # 問題別解説マークダウン
├── 気象予報士_学科一般_解答記録.md # 学習記録
├── read_pdf.py                  # PDF直接読み取りツール（メイン）
├── extract_pdf_images.py        # PDF図版抽出
├── read_xlsx.py                 # Excel読み取りツール
├── ocr_question_extractor.py    # OCR問題抽出（レガシー・参考用）
└── CLAUDE.md                    # Claude Code設定
```

## 使用方法

### 1. PDF問題抽出（メイン手法）
```bash
# PDFファイル全体を読み取り
python read_pdf.py 過去問一般/i63gakka(ippan).pdf

# 特定ページ範囲を読み取り
python read_pdf.py 過去問一般/i63gakka(ippan).pdf -s 1 -e 5

# 表示文字数を制限
python read_pdf.py 過去問一般/i63gakka(ippan).pdf -s 3 -e 3 -m 2000
```

### 2. 図版抽出
```bash
python extract_pdf_images.py
```

### 3. Excel学習記録管理
```bash
python read_xlsx.py  # 学習データの読み取り・分析
```

### 4. Claude解説作成
1. Excelから間違った問題を特定
2. `read_pdf.py`で問題文を抽出
3. 問題文と図版をClaudeに提示
4. 文字起こしと解説を依頼
5. 解説を`問題解説/`フォルダに保存

### レガシー機能（参考）
```bash
# OCR版問題抽出（現在は使用していない）
python ocr_question_extractor.py 13
python ocr_question_extractor.py 5 過去問一般/i62gakka(ippan).pdf
```

## 学習の流れ

1. **問題抽出**: PDFから直接問題と図版を抽出
2. **解答実行**: 問題を解いてExcelに記録
3. **間違い分析**: Excelで間違った問題を特定
4. **Claude解説**: 間違った問題をClaudeに提示して解説作成
5. **復習管理**: 解説を参考に理解を深め、再挑戦

## 技術要件

- Python 3.x
- PyMuPDF または PyPDF2（PDF読み取り用）
- Excel操作機能
- Claude Code（解説作成用）

## ライセンス

個人学習用。過去問等の著作権に配慮した利用をお願いします。