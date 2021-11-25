import pymysql

# user_info_table
# MYSQL_HOST = 'database-private.cpoaafcf6ree.ap-northeast-2.rds.amazonaws.com'
MYSQL_HOST = 'healers-db-instance-1.cp54nqphq6gx.ap-northeast-2.rds.amazonaws.com'
MYSQL_CONN = pymysql.connect(
    host=MYSQL_HOST,
    port=3306,
    user='healers',
    # passwd='tkrwp911',
    # passwd='Password!',
    passwd='Trillion!',
    db='user_data_schema',
    charset='utf8'
)

def conn_mysqldb():
    if not MYSQL_CONN.open:
        MYSQL_CONN.ping(reconnect=True) # 끊어지면 다시 접속
    return MYSQL_CONN

# def SQL_SELECT():
# 	db_cursor = conn_mysqldb().cursor()
# 	sql = """SELECT id, email, passwd
# 	FROM flask_table"""
# 	db_cursor.execute(sql)
# 	user = db_cursor.fetchall()
# 	if not user:
# 		db_cursor.close()

# 	for e in user:
# 		print(e)
# 	db_cursor.close()

# def SQL_SELECT_LOGIN(email, passwd):
# 	db_cursor = conn_mysqldb().cursor()
# 	sql = """SELECT CONVERT(AES_DECRYPT(email, SHA2('key',256)) using UTF8)
# 	FROM flask_table
# 	WHERE email=%s and passwd=%s"""
# 	db_cursor.execute(sql, email, passwd)
# 	user = db_cursor.fetchall()
# 	if not user:
# 		db_cursor.close()

# 	for e in user:
# 		print(e)
# 	db_cursor.close()

# def SQL_INSERT(username, password):
# 	db = conn_mysqldb()
# 	db_cursor = db.cursor()
# 	sql = """insert into flask_table(email, passwd)
#      		values (SHA2(%s,'256'), AES_ENCRYPT(%s, SHA2(%s,256)))"""
# 	"""
# 	INSERT INTO db_test.flask_table (email, passwd, bloodsugar, bloodtype, height, weight)
# 	VALUES (AES_ENCRYPT('testEmail', SHA2('SALT',256)), 
# 			SHA2('testPasswd',256), 
# 			AES_ENCRYPT('testbloodsugar', SHA2('SALT',256)),
# 			AES_ENCRYPT('testbloodtype', SHA2('SALT',256)), 
# 			AES_ENCRYPT('testheight', SHA2('SALT',256)), 
# 			AES_ENCRYPT('testweight', SHA2('SALT',256)));"""
# 	db_cursor.execute(sql, (username, password, KEY))
# 	db.commit()
# 	db_cursor.close()