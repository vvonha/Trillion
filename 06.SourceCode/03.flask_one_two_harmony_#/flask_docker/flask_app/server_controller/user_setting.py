from flask_login import UserMixin
from pymysql import NULL
from server_model.mysql import conn_mysqldb
import re

MY_SALT_VALUE = 'SKSHIELDUS'

class User(UserMixin):
    
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def get_id(self):
        return str(self.id)
 
    # +++ Exception (1) +++  
    def rm_vul_str(self, e):
        new_e = re.sub(r"[^a-zA-Z0-9]","",e)
        if e!=new_e or len(e)<=6:
            print('@@@에러:'+new_e)
        else:
            return new_e
        
    @staticmethod
    def get(id):
        print('\n@GET:','get','\n')
        mysql_db = conn_mysqldb()
        mysql_db_cursor = mysql_db.cursor()
        sql = "SELECT * \
                FROM user_data_table \
                WHERE id = %s" % (id)
                
        mysql_db_cursor.execute(sql)
        user = mysql_db_cursor.fetchone()
        if not user:
            return None
    
        user = User(id=user[0], username=user[1], password=user[2])
        return user
    
    @staticmethod
    def find(username):
        print('\nworking....\n')
        mysql_db = conn_mysqldb()
        mysql_db_cursor = mysql_db.cursor()
        
        sql = """SELECT * \
                FROM user_data_table \
                WHERE user = AES_ENCRYPT('%s', '%s')""" % (str(username), MY_SALT_VALUE)
        # sql = """SELECT * \
        #         FROM user_data_table \
        #         WHERE user = '%s'""" % (str(username))
        print(sql)
        mysql_db_cursor.execute(sql)
        user = mysql_db_cursor.fetchone()
        
        if not user:
            return None
        
        user = User(id=user[0], username=user[1], password=user[2])
        return user
    
    @staticmethod
    def search(username, password):
        mysql_db = conn_mysqldb()
        mysql_db_cursor = mysql_db.cursor()
        
        sql = "SELECT * \
                FROM user_data_table \
                WHERE user = '%s' \
                    and pw = '%s'" % (str(username), str(password))
        # sql = "SELECT * \
        #         FROM user_data_table \
        #         WHERE user = '%s' \
        #             and pw = '%s'" % (str(username), str(password))
                    
        mysql_db_cursor.execute(sql)
        user = mysql_db_cursor.fetchone()
        
        if not user:
            return None
        
        user = User(id=user[0], username=user[1], password=user[2])
        return user
    
    @staticmethod
    def examine(username, password):
        mysql_db = conn_mysqldb()
        mysql_db_cursor = mysql_db.cursor()
        
        sql = """SELECT id, AES_DECRYPT(user, '%s'), pw
                FROM user_data_table
                WHERE user = AES_ENCRYPT('%s', '%s')
                and pw = SHA2('%s', 256);""" % (MY_SALT_VALUE, str(username), MY_SALT_VALUE, str(password))
        # sql = """SELECT id, user, pw
        #         FROM user_data_table
        #         WHERE user = '%s'
        #         and pw = '%s'""" % (str(username), str(password))
                
        # print(username, password)
        # print(sql)
        mysql_db_cursor.execute(sql)
        user = mysql_db_cursor.fetchone()
        if not user:
            return None
        # print('user:', user)
        # username = user[1].decode('utf8')
        user = User(id=user[0], username=username, password=user[2])
        print("@HEX_TEST:",username)
        # user = User(id=user[0], username=user[1], password=user[2])
        return user
   
    @staticmethod
    def create(username, password):
        mysql_db = conn_mysqldb()
        mysql_db_cursor = mysql_db.cursor()
                
        sql = """INSERT INTO user_data_table (user, pw)
        VALUES ((AES_ENCRYPT('%s', '%s')), SHA2('%s',256) );""" % (str(username), MY_SALT_VALUE, str(password))
        
        # sql = """INSERT INTO user_data_table (user, pw) \
        #         VALUES ('%s', '%s') """ % (str(username), str(password))
        
        mysql_db_cursor.execute(sql)
        mysql_db.commit()
        
        # 생성된 정보에 대해 find(정보) 전달
        # return User.find(username, password)
        return User.search(username, password)