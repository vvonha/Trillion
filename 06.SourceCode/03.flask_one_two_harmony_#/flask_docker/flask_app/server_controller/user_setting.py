from flask_login import UserMixin
from pymysql import NULL
from server_model.mysql import conn_mysqldb

MY_SALT_VALUE = 'SKSHIELDUS'

class User(UserMixin):
    
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def get_id(self):
        return str(self.id)
 
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
                WHERE user = '%s'""" % (str(username))
        # sql = "SELECT * \
        #         FROM user_data_table \
        #         WHERE user = '%s' \
        #             and pw = '%s'" % (str(username), str(password))
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
        
        # sql = """SELECT AES_ENCRYPT('%s', 'SKSHIELDUS'), AES_ENCRYPT('%s', SHA2('SKSHIELDUS',256)) \
        #         FROM user_data_table;""" % (str(username), str(password))
        # sql = """SELECT AES_DECRYPT(user, 'SKSHIELDUS'), AES_DECRYPT(pw, SHA2('SKSHIELDUS',256))
        #             FROM user_data_table
        #             WHERE user = AES_ENCRYPT('%s', 'SKSHIELDUS')
        #             and pw = AES_ENCRYPT('%s', SHA2('SKSHIELDUS',256));""" % (str(username), str(password))
        # sql = "SELECT id, UNHEX(AES_DECRYPT(user, 'SKSHIELDUS')), pw \
        #         FROM user_data_table \
        #         WHERE user = AES_ENCRYPT('%s', 'SKSHIELDUS') \
        #         and pw = SHA2('%s',256);" % (str(username), str(password))
        sql = """SELECT id, user, pw
                FROM user_data_table
                WHERE user = '%s'
                and pw = '%s'""" % (str(username), str(password))
                
        # print(username, password)
        # print(sql)
        mysql_db_cursor.execute(sql)
        user = mysql_db_cursor.fetchone()
        if not user:
            return None
        # print('user:', user)
        # username = user[1].decode('utf8')
        # user = User(id=user[0], username=username, password=user[2])
        user = User(id=user[0], username=user[1], password=user[2])
        return user
    
    # @staticmethod
    # def examine(username, password):
    #     mysql_db = conn_mysqldb()
    #     mysql_db_cursor = mysql_db.cursor()
    #     sql = "SELECT * \
    #             FROM user_info_table \
    #             WHERE username = '%s' \
    #                 and password = '%s'" % (str(username), str(password))
    #     mysql_db_cursor.execute(sql)
    #     user = mysql_db_cursor.fetchone()
    #     if not user:
    #         return None
        
    #     user = User(id=user[0], username=user[1], password=user[2])
    #     return user
    
        "INSERT INTO db_test.flask_table (email, password, bloodsugar, bloodtype, height, weight)\
        VALUES (AES_ENCRYPT('testEmail', SHA2('SALT',256)), \
                SHA2('testpassword',256), \
                AES_ENCRYPT('testbloodsugar', SHA2('SALT',256)),\
                AES_ENCRYPT('testbloodtype', SHA2('SALT',256)), \
                AES_ENCRYPT('testheight', SHA2('SALT',256)), \
                AES_ENCRYPT('testweight', SHA2('SALT',256)));"
   
    @staticmethod
    def create(username, password):
        mysql_db = conn_mysqldb()
        mysql_db_cursor = mysql_db.cursor()
        # sql = """INSERT INTO user_data_table (user, pw) \
        #         VALUES (AES_ENCRYPT("%s", "%s"), AES_ENCRYPT("%s", SHA2("%s",256)) )""" % (str(username), MY_SALT_VALUE, str(password), MY_SALT_VALUE)
        sql = """INSERT INTO user_data_table (user, pw) \
                VALUES ('%s', '%s') """ % (str(username), str(password))
        mysql_db_cursor.execute(sql)
        mysql_db.commit()
        
        # 생성된 정보에 대해 find(정보) 전달
        # return User.find(username, password)
        return User.search(username, password)