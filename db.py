import pymysql


def connect_sql():
    db = pymysql.connect(host='localhost', user='root', password='liaocfe', port=3306, db='bingyanProject0')
    cursor = db.cursor()
    global db, cursor


def excute_sql(sql):
    try:

        cursor.execute(sql)
    except:
        print('failed to connect mysql.')

    try:
        cursor.execute(sql)
        db.commit()
    except:
        self.db.rollback()


def close_sql(self):
    self.db.close()
