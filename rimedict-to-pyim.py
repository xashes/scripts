import os
import tkinter as tk
from tkinter import filedialog, messagebox
import yaml

# 创建 Tkinter 窗口
root = tk.Tk()


# 创建 GUI 控件
def create_widgets():
    # 源文件选择框
    source_file_frame = tk.Frame(root)
    source_file_frame.pack(pady=5)
    source_file_label = tk.Label(source_file_frame, text="选择源文件:")
    source_file_label.pack(side=tk.LEFT)
    global source_file_entry
    source_file_entry = tk.Entry(source_file_frame, width=50)
    source_file_entry.pack(side=tk.LEFT)
    source_file_button = tk.Button(source_file_frame, text="浏览...", command=select_source_file)
    source_file_button.pack(side=tk.LEFT)

    # 目标文件选择框
    target_file_frame = tk.Frame(root)
    target_file_frame.pack(pady=5)
    target_file_label = tk.Label(target_file_frame, text="选择目标文件:")
    target_file_label.pack(side=tk.LEFT)
    global target_file_entry
    target_file_entry = tk.Entry(target_file_frame, width=50)
    target_file_entry.pack(side=tk.LEFT)
    target_file_entry.insert(0, get_default_target_file())
    target_file_button = tk.Button(target_file_frame, text="浏览...", command=select_target_file)
    target_file_button.pack(side=tk.LEFT)

    # 预览和转换按钮
    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)
    preview_button = tk.Button(button_frame, text="预览", command=preview)
    preview_button.pack(side=tk.LEFT, padx=10)
    convert_button = tk.Button(button_frame, text="转换", command=convert)
    convert_button.pack(side=tk.LEFT)

# 获取默认目标文件名
def get_default_target_file():
    home_dir = os.path.expanduser("~")
    default_dir = os.path.join(home_dir, ".spacemacs.d", "dict")
    if not os.path.isdir(default_dir):
        messagebox.showerror("错误", "文件夹不存在！")
    source_file = source_file_entry.get()
    target_file = os.path.join(default_dir, os.path.splitext(os.path.basename(source_file))[0] + ".pyim")
    return target_file


# 打开文件对话框并选择源文件
def select_source_file():
    filetypes = (("YAML files", "*.yaml"), ("All files", "*.*"))
    default_dir = os.path.join(os.path.expanduser("~"), ".spacemacs.d", "dict")
    source_file = filedialog.askopenfilename(initialdir=default_dir, title="选择源文件", filetypes=filetypes)
    source_file_entry.delete(0, tk.END)
    source_file_entry.insert(0, source_file)
    target_file_entry.delete(0, tk.END)
    target_file_entry.insert(0, get_default_target_file())


# 打开文件对话框并选择目标文件
def select_target_file():
    filetypes = (("Python files", "*.pyim"), ("All files", "*.*"))
    target_file = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="选择目标文件", filetypes=filetypes)
    target_file_entry.delete(0, tk.END)
    target_file_entry.insert(0, target_file)

# 预览转换后的内容
def preview():
    source_file = source_file_entry.get()
    if not os.path.isfile(source_file):
        messagebox.showerror("错误", "源文件不存在！")
    elif not source_file.endswith(".yaml"):
        messagebox.showerror("错误", "源文件不是 YAML 文件！")
    else:
        try:
            with open(source_file, "r", encoding="utf-8") as f:
                lines = []
                skip_lines = True
                for line in f:
                    line = line.strip()
                    if line.startswith("..."):
                        skip_lines = False
                        continue
                    if skip_lines:
                        continue
                    parts = line.split()
                    if len(parts) != 2:
                        continue
                    wubi_key, value = parts
                    converted_line = f"wubi/{value} {wubi_key}\n"
                    lines.append(converted_line)
                    if len(lines) >= 5:
                        break

            # 创建预览窗口
            preview_window = tk.Toplevel(root)
            preview_window.title("预览")
            preview_window.geometry("500x300")

            # 显示转换后的内容
            preview_text = tk.Text(preview_window, font=("LXGW WenKai", 12))
            preview_text.pack(fill=tk.BOTH, expand=True)
            preview_text.insert(tk.END, ";;; -*- coding: utf-8-unix -*-\n")
            preview_text.insert(tk.END, "".join(lines))

        except Exception as e:
            messagebox.showerror("错误", str(e))
# 转换文件格式
def convert():
    source_file = source_file_entry.get()
    if not os.path.isfile(source_file):
        messagebox.showerror("错误", "源文件不存在！")
    elif not source_file.endswith(".yaml"):
        messagebox.showerror("错误", "源文件不是 YAML 文件！")
    else:
        try:
            with open(source_file, "r", encoding="utf-8") as f1:
                lines = []
                skip_lines = True
                for line in f1:
                    line = line.strip()
                    if line.startswith("..."):
                        skip_lines = False
                        continue
                    if skip_lines:
                        continue
                    parts = line.split()
                    if len(parts) != 2:
                        continue
                    value, wubi_key = parts
                    converted_line = f"wubi/{wubi_key} {value}\n"
                    lines.append(converted_line)

            target_file = target_file_entry.get() or get_default_target_file()
            with open(target_file, "w", encoding="utf-8") as f2:
                f2.write(";;; -*- coding: utf-8-unix -*-\n")
                f2.writelines(lines)

            messagebox.showinfo("成功", "转换完成！")

        except Exception as e:
            messagebox.showerror("错误", str(e))

# 启动 GUI 程序
if __name__ == '__main__':
    root.title("转换词库文件格式")
    root.geometry("600x250")
    create_widgets()
    root.mainloop()
