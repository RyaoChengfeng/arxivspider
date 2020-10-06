import pymysql

while True:
    try:
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='liaocfe',
            port=3306,
            db='bingyanProject0',
        )
        cursor = db.cursor()
        print('成功')
    except Exception as e:
        print(e)
        break
