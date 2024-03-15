import os
import shutil

# 源文件夹路径
source_folder = r"E:\lsy-test-code\my-yns\pj0133"

# 目标文件夹路径
destination_folder = r"E:\lsy-test-code\my-yns\tbl-files3"

# 遍历源文件夹
for root, dirs, files in os.walk(source_folder):
    print('root:',root)
    print('dirs:',dirs)
    print('files:',files)
    continue
    for file in files:
        if file.endswith(".xls") or file.endswith(".xlsx"):  # 检查文件是否为Excel文件
            source_file_path = os.path.join(root, file)
            new_head = root.split(os.sep)[-2]
            print(new_head)
            new_file_name = new_head + '_TTBBLL_' + file  # 新文件名，可以根据需要自定义命名规则

            # 复制文件到目标文件夹并重命名
            shutil.copy(source_file_path, os.path.join(destination_folder, new_file_name))
            print("Excel文件复制并重命名完成")
            # break
    # break

print("Excel文件复制并重命名完成")
