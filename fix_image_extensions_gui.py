# -*- coding: utf-8 -*-
"""
📦 拡張子偽装修正 + YCCK JPEG修復（バックアップ）+ GUI進捗バー + CSV出力
"""

from pathlib import Path
from PIL import Image
import shutil
import csv
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

# === 設定 ===
ROOT_DIR = Path(r"D:\展開")
BACKUP_ROOT = Path(r"D:\TMP")
CSV_LOG_PATH = BACKUP_ROOT / "fixed_extensions.csv"
VALID_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".tif", ".tiff"}
FORMAT_TO_EXT = {
    "jpeg": ".jpg",
    "png": ".png",
    "webp": ".webp",
    "bmp": ".bmp",
    "gif": ".gif",
    "tiff": ".tif",
}
REPAIRABLE_MODES = {"CMYK"}

# === スキャン ===
def scan_files():
    rename_list = []
    for file in ROOT_DIR.rglob("*"):
        if not file.is_file() or file.suffix.lower() not in VALID_EXTS:
            continue
        try:
            with Image.open(file) as img:
                actual_format = img.format.lower()
                expected_ext = FORMAT_TO_EXT.get(actual_format)
                current_ext = file.suffix.lower()
                if expected_ext and current_ext != expected_ext:
                    new_path = file.with_suffix(expected_ext)
                    rename_list.append((file, new_path, "拡張子修正"))
                elif current_ext in {".jpg", ".jpeg"} and img.mode in REPAIRABLE_MODES:
                    rename_list.append((file, file, "YCCK修復"))
        except Exception:
            continue
    return rename_list

# === GUI表示 + 実行処理 ===
def show_gui(rename_list):
    root = tk.Tk()
    root.title("画像修正プレビュー")
    root.geometry("900x550")

    label = tk.Label(root, text="以下のファイルが修正対象です：")
    label.pack()

    text_area = scrolledtext.ScrolledText(root, wrap=tk.NONE, width=120, height=25)
    for old, new, reason in rename_list:
        line = f"{old} -> {new.name if old != new else '[上書き]'} [{reason}]\n"
        text_area.insert(tk.END, line)
    text_area.pack()

    x_scroll = tk.Scrollbar(root, orient="horizontal", command=text_area.xview)
    x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
    text_area.config(xscrollcommand=x_scroll.set)

    # === 進捗バー ===
    progress = ttk.Progressbar(root, orient="horizontal", length=800, mode="determinate")
    progress.pack(pady=10)
    progress["maximum"] = len(rename_list)
    progress["value"] = 0

    def execute():
        errors = []
        ext_log = []

        for idx, (old, new, reason) in enumerate(rename_list, 1):
            try:
                if reason == "拡張子修正" and old != new:
                    ext_log.append([str(old), old.suffix, new.suffix])
                    old.rename(new)

                elif reason == "YCCK修復":
                    parent_name = old.parent.name
                    backup_folder = BACKUP_ROOT / parent_name
                    backup_folder.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(old, backup_folder / old.name)

                    with Image.open(old) as img:
                        img = img.convert("RGB")
                        img.save(old, format="JPEG", quality=95)

            except Exception as e:
                errors.append(f"{old} : {e}")

            progress["value"] = idx
            root.update_idletasks()

        if ext_log:
            try:
                with CSV_LOG_PATH.open("w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["file_path", "old_ext", "new_ext"])
                    writer.writerows(ext_log)
            except Exception as e:
                errors.append(f"CSV出力エラー: {e}")

        if errors:
            messagebox.showerror("一部失敗", "\n".join(errors))
        else:
            messagebox.showinfo("完了", "すべての修正が完了しました。")
        root.destroy()

    button = tk.Button(root, text="実行して修正", command=execute)
    button.pack(pady=5)

    root.mainloop()

# === メイン ===
if __name__ == "__main__":
    planned = scan_files()
    if planned:
        show_gui(planned)
    else:
        tk.Tk().withdraw()
        messagebox.showinfo("処理不要", "修正対象となるファイルはありませんでした。")
