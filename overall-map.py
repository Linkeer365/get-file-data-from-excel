import os
import re
import time
import pandas as pd
import psycopg2

whole_file = r'E:\lsy-test-code\my-yns\finds2.txt'
error_path=r'E:\lsy-test-code\my-yns\xls-error-log.txt'
error_path2=r'E:\lsy-test-code\my-yns\xls-error-log.txt'



def do_one(site_id,excel_path):

    cur_schema="ynsbom"
    conn = psycopg2.connect(host="localhost",database="linsiyi_yns", user="postgres", password="xm111737",options="-c search_path={}".format(cur_schema))
    cursor=conn.cursor()

    try:
        xls = pd.ExcelFile(excel_path)
        all_data = []
        # 遍历每个 sheet 页
        for sheet_name in xls.sheet_names:
            # 读取每个 sheet 页的数据
            df = pd.read_excel(excel_path, sheet_name=sheet_name)
            all_data.append(df)
        # 将所有数据合并
        merged_data = pd.concat(all_data)
        # 将合并后的数据写入到一个 txt 文件中
        output_file = excel_path.replace(".xlsx",'.txt').replace(".xls",'.txt')
        merged_data.to_csv(output_file, sep='\t', index=False)

        with open(output_file,'r',encoding="utf-8") as f:
            lines=f.readlines()
        with open(whole_file,'a',encoding='utf-8') as f:
            f.write("SITE-ID: {}\n".format(site_id))
            f.write("Output-file: {}\n\n".format(output_file))
        finds=[]
        for each_line in lines:
            pattern = "\s*\d{1,3}\s*(\S+)\s*(\S+)"
            try:
                find = re.findall(pattern,each_line)[0]
                if find in finds:
                    continue
                none_alpha_flag = False
                for each in find:
                    none_alpha_flag = any(c.isalpha() for c in each)
                    # print(none_alpha_flag)
                    if not none_alpha_flag:
                        break
                if none_alpha_flag:
                    with open(whole_file,'a',encoding='utf-8') as f:
                        f.write('\t'.join(find)+'\n')
                        if len(find)==2:
                            row_value = (
                                            site_id.lower(),
                                            output_file.split(os.sep)[-3],
                                            output_file.split(os.sep)[-1].replace(".txt",'').lower(),
                                            find[1].lower(),
                                            find[0]
                                         )
                            try:
                                insert_sql = f"INSERT INTO bom_table_column_desc (site_id,db_table,db_name,col_name,col_desc) VALUES ('{row_value[0]}','{row_value[1]}','{row_value[2]}','{row_value[3]}','{row_value[4]}')"
                                cursor.execute(insert_sql)
                                # 单条直接commit，防止因为有重复pkey导致前面的也commit不了！
                                conn.commit()
                                # print("db run success")
                            except Exception as e:
                                # print(e)
                                with open(error_path,'a',encoding="utf-8") as f:
                                    f.write('DB ERROR:{}\n{}\n'.format(e,excel_path))
                    finds.append(find)
                        # print(find)
            except Exception as e:
                with open(error_path,'a',encoding="utf-8") as f:
                    f.write('RE ERROR:{}\n{}\n'.format(e,excel_path))
                continue
        with open(whole_file,'a',encoding='utf-8') as f:
            f.write('\n\n')
        os.remove(output_file)

    except Exception as e:
        # print(e)
        with open(error_path,'a',encoding="utf-8") as f:
            f.write('XLS ERROR:{}\n{}\n'.format(e,excel_path))
    conn.close()


source_folder = r'E:\lsy-test-code\my-yns\pj0133'



for root, dirs, files in os.walk(source_folder):
    for file in files:
        if file.endswith('.xlsx') or file.endswith('.xls'):
            site_id = root[len(source_folder)+len(os.sep):].split(os.sep)[0]
            do_one(site_id,os.path.join(root,file))
    # time.sleep(5)
