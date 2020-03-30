# from tqdm import tqdm
# import time
# import pymysql
# from pymysql import cursors


# dbparams = {
#             'host': '127.0.0.1',
#             'port': 3306,
#             'user': 'root',
#             'password': '1234',
#             'database': 'ziroom',
#             'charset': 'utf8',
#             'cursorclass': cursors.DictCursor
#             }
# # 创建连接
# con= pymysql.connect(**dbparams)
# try:
#     with con.cursor() as cursor:
#         sql="SELECT id, picture,num_1,num_2,num_3,num_4 FROM tj"
#         cursor.execute(sql)
#         result=cursor.fetchall()
#         for data in tqdm(result):
#             try:
#                 Id = data['id']
#                 picture = str(data['picture'])
#                 price1= data['num_1']
#                 price2 = data['num_2']
#                 price3 = data['num_3']
#                 price4 = data['num_4']
#                 if price3 ==10 and price4 ==10:
#                     price = picture[price1] + picture[price2]

#                 elif price3 !=10 and price4 == 10:
#                     price = picture[price1] + picture[price2] +picture[price3]
                    
#                 else:
#                     price = picture[price1] + picture[price2] +picture[price3] + picture[price4]
                    
#                 print(Id)
#                 print(price)
#                 sql1 = "update tj set price = {} where id = {}".format(price,Id)
#                 print(sql1)
#                 cursor.execute(sql1)
#                 con.commit()
#             except Exception as e:
#                 print(Id)
#                 print(e)

# finally:
#     con.close()

