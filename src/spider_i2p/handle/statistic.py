import os
import csv

def calculate_packet_type_percentage(src_dir):
    type_dic = {}

    # 遍历目录下的所有文件
    for filename in os.listdir(src_dir):
        if filename.endswith(".csv"):
            csv_file_path = os.path.join(src_dir, filename)
            
            # 打开CSV文件并搜索包含"未知"的行
            with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    # if row[2] == "未知":
                    #     continue
                    if row[2] not in type_dic:
                        type_dic[row[2]] = 1
                    else:
                        type_dic[row[2]] += 1
    print(type_dic)




if __name__ == "__main__":
    calculate_packet_type_percentage("/root/code/spider_i2p/data/flowlog/handled")
