import os
import shutil
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

# 创建主窗口
root = tk.Tk()
root.title("备份程序")

# 创建列表框控件，用于显示文件夹列表
folder_list = tk.Listbox(root, height=10)
folder_list.pack(padx=10, pady=10)

# 添加按钮回调函数
def add_folder():
    # 弹出选择文件夹对话框
    folder = filedialog.askdirectory(initialdir=os.path.expanduser("~"), title="选择文件夹")
    # 如果选择了文件夹，则将其添加到列表框中
    if folder:
        folder_list.insert(tk.END, folder)

# 删除按钮回调函数
def remove_folder():
    # 获取选中项的索引
    selected = folder_list.curselection()
    # 如果有选中项，则将其从列表框中删除
    if selected:
        folder_list.delete(selected)

# 备份按钮回调函数
def backup():
    # 获取备份目标文件夹
    target_folder = os.path.expanduser("~/backup/")
    # 如果目标文件夹不存在，则创建它
    if not os.path.isdir(target_folder):
        os.mkdir(target_folder)

    # 获取备份列表
    folders = folder_list.get(0, tk.END)
    # 备份每个文件夹
    for folder in folders:
        try:
            # 构造备份目标路径
            basename = os.path.basename(folder)
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            backup_folder = os.path.join(target_folder, f"{basename}_{timestamp}")
            # 判断备份目标路径是否存在
            while os.path.exists(backup_folder):
                # 如果目标路径已存在同名文件夹，则询问用户是覆盖还是跳过
                message = f"目标文件夹 {backup_folder} 已存在，是否要覆盖？"
                result = messagebox.askyesnocancel("确认", message)
                if result is None:
                    # 如果用户选择取消，则直接跳过当前文件夹的备份
                    break
                elif result:
                    # 如果用户选择覆盖，则删除原有的同名文件夹
                    shutil.rmtree(backup_folder)
                else:
                    # 如果用户选择跳过，则直接跳过当前文件夹的备份
                    break
                backup_folder = os.path.join(target_folder, f"{basename}_{timestamp}")
            else:
                # 如果备份目标路径不存在，则备份文件夹
                shutil.copytree(folder, backup_folder)
                # 记录备份信息
                with open(os.path.join(target_folder, "backup.txt"), "a") as f:
                    f.write(f"{folder}\t{timestamp}\n")
        except Exception as e:
            messagebox.showerror("错误", f"备份文件夹 {folder} 时发生错误：{str(e)}")
    # 提示备份完成
    messagebox.showinfo("提示", "备份完成！")

# 创建添加、删除和备份按钮
add_button = tk.Button(root, text="添加", command=add_folder)
add_button.pack(side=tk.LEFT, padx=10)

remove_button = tk.Button(root, text="删除", command=remove_folder)
remove_button.pack(side=tk.LEFT)

backup_button = tk.Button(root, text="备份", command=backup)
backup_button.pack(side=tk.RIGHT, padx=10)

# 显示主窗口
root.mainloop()
