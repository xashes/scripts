import tkinter as tk
from tkinter import filedialog, messagebox, font
from PIL import Image
import os

output_dir = '~/Pictures/models'
image_dir = '~/Pictures/AI'

class App:
    def __init__(self, master):
        self.master = master
        self.filename = None
        self.comment = ""
        self.directory = os.getcwd()
        self.default_dir = os.path.expanduser(output_dir)
        if not os.path.isdir(self.default_dir):
            os.makedirs(self.default_dir)
        self.create_widgets()

    def create_widgets(self):
        self.select_file_button = tk.Button(self.master, text="Choose Image", command=self.select_file)
        self.select_file_button.pack()

        self.comment_label = tk.Label(self.master, text="Insert Comment：")
        self.comment_label.pack()

        self.comment_entry = tk.Text(self.master, width=40, height=10)
        self.comment_entry.pack()

        self.save_button = tk.Button(self.master, text="Save", command=self.save)
        self.save_button.pack()

    def select_file(self):
        # 弹出文件选择框
        options = {
            'initialdir': os.path.expanduser(image_dir),
            'filetypes': (("所有文件", "*.*"),),
        }
        filename = filedialog.askopenfilename(**options)

        # 更新按钮文本
        if filename:
            self.select_file_button.config(text="已选择：" + filename)
            self.filename = filename

    def save(self):
        if not self.filename:
            messagebox.showerror("错误", "请选择要保存的文件！")
            return

        self.comment = self.comment_entry.get("1.0", tk.END).strip()
        if not self.comment:
            messagebox.showerror("错误", "请输入注释！")
            return

        directory = filedialog.askdirectory(initialdir=self.default_dir, title="选择文件夹")
        if not directory:
            return

        # 创建新文件夹并保存图片和注释
        folder_name = os.path.basename(self.filename).split(".")[0]
        folder_path = os.path.join(directory, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        with open(os.path.join(folder_path, "comment.txt"), "w") as f:
            f.write(self.comment)

        image = Image.open(self.filename)
        image.save(os.path.join(folder_path, os.path.basename(self.filename)))

        # 清空注释框中的文本
        self.comment_entry.delete("1.0", tk.END)

        messagebox.showinfo("提示", "保存成功！")

root = tk.Tk()
app = App(root)
root.mainloop()
