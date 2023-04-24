import mysql.connector
import requests

# 连接数据库
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123456",
  database="kaoyanbang"
)

# 获取游标
mycursor = mydb.cursor()
# 插入字典数据
data = {"name": "John", "age": 36}
sql = "INSERT INTO customers (name, age) VALUES (%s, %s)"
val = (data["name"], data["age"])
mycursor.execute(sql, val)
# 提交事务
mydb.commit()
# 输出插入的数据的主键
print("Inserted record with ID:", mycursor.lastrowid)

url = "http://www.jjmeinv.com/s.asp?act=topic&keyword=%B8%A3%C0%FB%BC%A7"
headers = {
}

response = requests.get(url).text