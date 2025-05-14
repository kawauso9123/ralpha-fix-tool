# ralpha-fix-tool
# 🧯 RalphaPlus64 SafeLoader

## ✅ 概要

RalphaPlus64使用時に発生する以下の**致命的なファイル破壊バグ**に対処するためのツールです：

- **YCCK形式JPEG** → 読み込み失敗 → 画像が**0バイトに破壊**
- **拡張子偽装（例：WebPを.jpgとして保存）** → 読み込み失敗 → 無反応または処理不能

このツールは、それらの問題を**事前に検出・変換・修正**し、RalphaPlus64での安全な一括処理を可能にします。

---

## ⚙️ 主な機能

- 📂 `D:\展開` 配下の画像をスキャン（拡張子偽装・YCCK検出）
- 🛡 拡張子偽装 → 正しい拡張子に変更
- 🎨 YCCK形式JPEG → PillowでRGB再保存（画質保持）
- 💾 修正前に `D:\TMP\{親フォルダ名}` にバックアップ保存
- 📋 修正内容のCSVログ（`fixed_extensions.csv`）を出力
- 🖥 GUI表示＋進捗バーつき（Tkinter）

---

## 💻 使用方法

1. `fix_image_extensions_gui.py` を実行
2. 対象ファイルが一覧表示される（プレビュー）
3. 「実行して修正」ボタンを押すと処理が始まる

---

## 🔧 必要ライブラリ（requirements.txt）

```txt
Pillow
opencv-python
