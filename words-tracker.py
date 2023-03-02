import os
import datetime
from tkinter import *
from tkinter import filedialog, messagebox


# 创建 Tkinter 窗口
root = Tk()


# 定义默认文件夹路径和当前监控文件夹路径
default_dir = os.path.expanduser("~")
current_dir = default_dir


# 创建界面控件
frame1 = Frame(root)
frame1.pack(padx=10, pady=10, fill=BOTH)
label1 = Label(frame1, text="监控文件夹：")
label1.pack(side=LEFT)
dir_label = Label(frame1, text=current_dir, width=50)
dir_label.pack(side=LEFT)
select_button = Button(frame1, text="选择文件夹", command=lambda: select_dir())
select_button.pack(side=LEFT, padx=10)

frame2 = Frame(root)
frame2.pack(padx=10, pady=10, fill=BOTH)
label2 = Label(frame2, text="文件名", width=20)
label2.pack(side=LEFT)
label3 = Label(frame2, text="字数", width=20)
label3.pack(side=LEFT)
label4 = Label(frame2, text="扫描时间", width=30)
label4.pack(side=LEFT)
label5 = Label(frame2, text="最后修改时间", width=30)
label5.pack(side=LEFT)

text = Text(root)
text.pack(padx=10, pady=10, fill=BOTH, expand=True)
text.config(state=DISABLED)


# 获取当前日期
today = datetime.datetime.now().strftime("%Y-%m-%d")
log_file = f"{today}.txt"


# 定义字数计数器
word_count = 0


# 选择监控文件夹
def select_dir():
    global current_dir, word_count
    current_dir = filedialog.askdirectory(initialdir=default_dir)
    dir_label.config(text=current_dir)
    word_count = 0
    scan_dir(current_dir)


# 递归扫描文件夹并处理 org 文件
def scan_dir(dir_path):
    global word_count
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        if os.path.isdir(file_path):
            scan_dir(file_path)
        elif file_name.endswith(".org"):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                word_count += len(content.split())
            last_modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M:%S")
            scan_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"{file_name:<20}{len(content.split()):<10}{scan_time:<30}{last_modified_time}\n"
            append_log(log_entry)


# 将记录追加到日志文件中
def append_log(log_entry):
    global log_file
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_entry)
    text.config(state=NORMAL)
    text.insert(END, log_entry)
    text.config(state=DISABLED)


# 显示文件夹中某个文件的字数
def show_word_count(file_name):
    file_path = os.path.join(current_dir, file_name)
    if os.path.isfile(file_path) and file_name.endswith(".org"):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            count = len(content.split())
            messagebox.showinfo("提示", f"{file_name} 的字数为 {count}")
    else:
        messagebox.showerror("错误", "请选择 org 文件")


# 显示整个文件夹的总字数
def show_total_word_count():
    global word_count
    messagebox.showinfo("提示", f"当前监控文件夹 {current_dir} 的总字数为 {word_count}")


# 检查日志文件是否存在，不存在则创建
if not os.path.exists(log_file):
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"{'文件名':<20}{'字数':<10}{'扫描时间':<30}{'最后修改时间'}\n")


# 绑定菜单栏快捷键
root.bind_all("<Control-o>", lambda event: select_dir())
root.bind_all("<Control-s>", lambda event: show_total_word_count())


# 启动 Tkinter 程序
root.mainloop()
