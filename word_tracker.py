import os
import csv
import pandas as pd
from datetime import datetime
import time


def get_org_files(folder):
    """返回指定文件夹中所有 .org 后缀的文件的路径列表"""
    files = []
    for file_name in os.listdir(folder):
        if file_name.endswith(".org"):
            files.append(os.path.join(folder, file_name))
    return files


def get_char_count(file_path):
    """返回指定文件的字符数"""
    with open(file_path, "r", encoding="utf-8") as f:
        return len(f.read())


def get_last_modified_time(df, file_path):
    """返回上一次记录该文件的修改时间"""
    rows = df.loc[df["file_path"] == file_path].tail(1)
    if not rows.empty:
        return datetime.fromisoformat(rows.iloc[0]["modified_time"])
    return None

def get_last_record_time(df, file_path):
    """返回上一次记录该文件的修改时间"""
    rows = df.loc[df["file_path"] == file_path].tail(1)
    if not rows.empty:
        return datetime.fromisoformat(rows.iloc[0]["time"])
    return None


def is_same_hour(dt1, dt2):
    """判断两个时间是否在同一小时内"""
    return dt1.strftime("%Y-%m-%dT%H") == dt2.strftime("%Y-%m-%dT%H")


def update_records(file_path, csv_file_path):
    """更新记录信息并将其写入 CSV 文件中"""
    now = datetime.now().replace(minute=0, second=0, microsecond=0)

    df = pd.DataFrame(columns=["time", "file_path", "modified_time", "char_count"])
    if os.path.exists(csv_file_path) and os.stat(csv_file_path).st_size > 0:
        df = pd.read_csv(csv_file_path)

    last_modified_time = get_last_modified_time(df, file_path)
    current_modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
    last_record_time = get_last_record_time(df, file_path)

    if last_modified_time is not None and current_modified_time <= last_modified_time:
        return

    char_count = get_char_count(file_path)

    if last_record_time is None or not is_same_hour(now, last_record_time):
        df = df.append({
            "time": now.strftime("%Y-%m-%dT%H"),
            "file_path": file_path,
            "modified_time": current_modified_time.isoformat(),
            "char_count": char_count
        }, ignore_index=True)
    else:
        df.loc[(df["time"] == now.strftime("%Y-%m-%dT%H")) & (df["file_path"] == file_path)] = \
            [now.strftime("%Y-%m-%dT%H"), file_path, current_modified_time.isoformat(), char_count]

    df.to_csv(csv_file_path, index=False)

def main():
    org_folder = ("/home/xashes/org/writing")
    tracker_folder = os.path.join(org_folder, "words-tracker")

    if not os.path.exists(tracker_folder):
        os.mkdir(tracker_folder)

    current_month = datetime.now().strftime("%Y-%m")
    csv_file_path = os.path.join(tracker_folder, current_month + ".csv")

    if not os.path.exists(csv_file_path) or os.stat(csv_file_path).st_size == 0:
        with open(csv_file_path, "w", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["time", "file_path", "modified_time", "char_count"])

    for file_path in get_org_files(org_folder):
        update_records(file_path, csv_file_path)

if __name__ == "__main__":
    main()

