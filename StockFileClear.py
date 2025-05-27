import os

def delete_files_in_path(folder_path, suffix):
    """
    删除指定路径下所有指定后缀名的文件。
    :param folder_path: 目标文件夹路径
    :param suffix: 目标文件后缀（如".json"）
    """
    count = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(suffix):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    count += 1
                except Exception as e:
                    print(f"删除文件失败: {file_path}, 错误: {e}")
    print(f"已删除{count}个{suffix}文件。")

if __name__ == "__main__":
    folder = r"E:\stock_json"  # 修改为你的目标路径
    ext = ".json"              # 修改为你的目标后缀
    delete_files_in_path(folder, ext)
