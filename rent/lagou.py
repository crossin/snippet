import requests
import json
from tqdm import trange # pip install trange 进度条
import pymysql
from pymysql import cursors

dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '1234',
            'database': 'lagou',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor
            }
# 创建连接

def get_url(keyword,pn):
    # 浏览器地址栏显示的url
    web_url = "https://www.lagou.com/jobs/list_/p-city_0?px=new" 
    # ajax 请求地址
    headers_url = "https://www.lagou.com/jobs/positionAjax.json?px=new&needAddtionalResult=false"

    headers = {"Accept": "application/json, text/javascript, */*; q=0.01",
               "Referer": web_url,
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
               }
    form_data = {
            "first": "true",
            "pn": "{}".format(pn),
            "kd": "{}".format(keyword)
            }
    # 创建 cookie 对象
    session = requests.Session()
    # 发送请求,获得cookies
    session.get(url=web_url,headers=headers)
    # 传递 cookie
    response = session.post(url=headers_url, headers=headers, data=form_data)

    return response

def total_Count(response):
    html = response.json()
    # print(page)
    total_count = html['content']['positionResult']['totalCount'] # totalCount为总个数
    pn_count = int(total_count)//15 + 1
    # 页数
    print('职位总数{},共{}页'.format(total_count,pn_count))
    return pn_count

def parse_url(response):
    # 创建连接
    con= pymysql.connect(**dbparams)
    with con.cursor() as cursor:   
        json_data = json.loads(response.text)
        results = json_data['content']['positionResult']['result']
        for result in results:
            info = {
                    "positionName" : result["positionName"],
                    "companyFullName" : result["companyFullName"],
                    "companySize" : result["companySize"],
                    "industryField" : result["industryField"],
                    "financeStage" : result["financeStage"],
                    "firstType" : result["firstType"],
                    "skillLables" :str(result["skillLables"]),
                    "positionLables" : str(result["positionLables"]),
                    "createTime" : result["createTime"],
                    "city" : result["city"],
                    "district" : result["district"],
                    "salary" : result["salary"],
                    "workYear" : result["workYear"],
                    "jobNature" : result["jobNature"],
                    "education" :result["education"],
                    "positionAdvantage" : result["positionAdvantage"]
                    }
            sql = """INSERT INTO info(Id, positionName, companyFullName,companySize,
                            industryField,financeStage,firstType,skillLables,positionLables,createTime,city,district,
                            salary,workYear,jobNature,education,positionAdvantage) 
                        VALUES (null,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s)"""
            cursor.execute(sql, (info['positionName'],info['companyFullName'],
                    info['companySize'],info['industryField'],info['financeStage'],info['firstType'],info['skillLables'],
                    info['positionLables'],info['createTime'],info['city'],info['district'],info['salary'],
                    info['workYear'],info['jobNature'],info['education'],info['positionAdvantage']))
            con.commit()
        con.close()
        # 返回结果
        return results
def main():
    # keyword = input('输入城市, 职位或公司, 如果为空，则代表全国各城市职位 \n') #输入搜索内容
    file = open("city.txt",encoding='utf8')
    for city in file.readlines():  # 读取城市, 也可以注释掉这行代码，用关键词输入
        
        keyword=city.strip('\n')
        print(keyword)  
        response = get_url(keyword,pn=1)
        num = total_Count(response)  # 获得数据总个数和页数
        for i in trange(1,int(num)+1): # 实现翻页效果
            response = get_url(keyword, pn=i)
            results = parse_url(response)
            # 测试的时候发现可以得到的总页数，但是最多只能抓取到200页
            # 所以判断如果结果为空就结束循环
            # print(results)
            if results == []:
                break

if __name__ =="__main__":
    main()
