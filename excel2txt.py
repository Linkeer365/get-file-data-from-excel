import pandas as pd
import os
import time

def do_one_excel(from_dir,excel_name,to_dir):
    # 读取 Excel 文件
    excel_file = from_dir + os.sep + excel_name
    try:
        xls = pd.ExcelFile(excel_file)

        all_data = []
        # 遍历每个 sheet 页
        for sheet_name in xls.sheet_names:
            # 读取每个 sheet 页的数据
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            all_data.append(df)
        
        # 将所有数据合并
        merged_data = pd.concat(all_data)

        # 将合并后的数据写入到一个 txt 文件中
        output_file = to_dir + os.sep +  excel_name.replace(".xlsx",'.txt').replace(".xls",'.txt')
        merged_data.to_csv(output_file, sep='\t', index=False)
    except Exception:
        output_file = to_dir + os.sep + "_ERROR_" + excel_name.replace(".xlsx",'.txt').replace(".xls",'.txt')
        with open(output_file,'w',encoding="utf-8") as f:
            f.write(str(time.time())+"\n")


from_dir = r'E:\lsy-test-code\my-yns\tbl_files2'
to_dir = r'E:\lsy-test-code\my-yns\tbl-txt-files2'

for i in os.listdir(from_dir):
    output_file = to_dir + os.sep +  i.replace(".xlsx",'.txt').replace(".xls",'.txt')
    if os.path.exists(output_file):
        # print("already")
        continue
    else:
        print("Not yet: ",i.replace(".xlsx",'.txt').replace(".xls",'.txt'))
        do_one_excel(from_dir,i,to_dir)