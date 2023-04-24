import requests
import mysql.connector
import copy

header = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}


cnx = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123456",
  database="kaoyanbang"
)

cursor = cnx.cursor()

cursor.execute("DESCRIBE school_depart")
fields_school_depart = [f[0] for f in cursor.fetchall()]
del fields_school_depart[0]

cursor.execute("DESCRIBE depart_special")
fields_depart_special = [f[0] for f in cursor.fetchall()]
del fields_depart_special[0]

sql = "SELECT id,school_id FROM school_list;"
cursor.execute(sql)

result = cursor.fetchall()
# 解析查询结果并转换为字典
school_data = []
for row in result:
    # 将每一行数据转换为字典形式
    d = dict(zip([x[0] for x in cursor.description], row))
    school_data.append(d)

total = 1056
count = 0

for s_item in school_data:
    s_item={}
    s_item['school_id'] = 1551
    try:
        url = f"https://static.kaoyan.cn/json/school/{s_item['school_id']}/planSpecial.json"
        r = requests.get(url=url, headers=header)
        json_data = r.json()
        
        for key_name in json_data["data"]:
            if key_name == 'syl_jianshe':
                update_sql = f"UPDATE school_list SET syl_jianshe = %s WHERE school_id = %s;"
                # print( update_sql, tuple([str("|".join(json_data["data"][key_name])),s_item['school_id']]))
                cursor.execute(
                    update_sql, tuple([str("|".join(json_data["data"][key_name])), s_item['school_id']]))
            if key_name == 'master_degree':
                for depart_item in json_data["data"][key_name]:
                    d_item = copy.deepcopy(depart_item)
                    del d_item["special_list"]
                    f = d_item.items()
                    insert_sql_school_depart = f"INSERT INTO school_depart (school_id,depart_id,depart_name) VALUES (%s,%s,%s)"
                    value_depart_item = tuple([v for k, v in f])
                    # print(insert_sql_school_depart, tuple([s_item['school_id']])+value_depart_item)
                    cursor.execute(
                        insert_sql_school_depart, tuple([s_item['school_id']])+value_depart_item)
                    for spe_item in depart_item['special_list']:
                        sp = spe_item.items()
                        insert_sql_depart_special = f"INSERT INTO depart_special (depart_id,spe_id,code,name) VALUES (%s,%s,%s,%s)"
                        value_spe_item = tuple([v for k, v in sp])
                        # print(insert_sql_depart_special,tuple([depart_item['depart_id'],spe_item['spe_id'],spe_item['code'],spe_item['name']]))
                        cursor.execute(
                            insert_sql_depart_special, tuple([depart_item['depart_id'], spe_item['spe_id'], spe_item['code'], spe_item['name']]))
        cnx.commit()
        # count = count + 1
        # jindu = round((count / total)*100, 2)
        # print("count:", count)
        # print("当前进度:", jindu, "%")
    except Exception as e:
        break
        file = open("err.log", "a")
        # 向文件中写入一段文本
        file.write(f"error_info:{e}.\n")
        file.write(f"school_id:{s_item['school_id']}\n")
        # 刷新文件缓冲区
        file.flush()
        # 关闭文件
        file.close()


cursor.close()
cnx.close()
print("完成")
