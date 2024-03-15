import os
import re
import time

whole_file = r'E:\lsy-test-code\my-yns\finds2.txt'

def do_one_file(from_dir,txt_name):
    file_path = from_dir + os.sep + txt_name
    with open(file_path,'r',encoding="utf-8") as f:
        lines=f.readlines()
    # print("******")
    # print(txt_name)
    with open(whole_file,'a',encoding='utf-8') as f:
        f.write(txt_name+'\n\n')
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
                finds.append(find)
                    # print(find)
        except Exception as e:
            print(e)
            continue
    with open(whole_file,'a',encoding='utf-8') as f:
        f.write('\n\n')

from_dir = r'E:\lsy-test-code\my-yns\tbl-txt-files2'

for i in os.listdir(from_dir):
    do_one_file(from_dir,i)
    # time.sleep(5)
