import sqlite3
from sqlite3 import Error

#database = "C:/parser/db/parser.db"
database = "resources/database/parser.db"

def create_connection():
    
    try:
        connection = sqlite3.connect(database)
        return connection
    except Error as e:
        print(e)
        
    return None
 
def create_user(user):
    
    connection = create_connection()
    
    sql = ''' INSERT INTO users (username, password) VALUES(?, ?) '''
    cur = connection.cursor()
    cur.execute(sql, user)
    connection.commit()
    insert_id = cur.lastrowid
    
    connection.close()
    
    return insert_id


def insert_step(step):
    
    connection = create_connection()
    
    sql = ''' INSERT INTO steps (ref_no, date, rem_name, ben_name, ben_bank, ben_br_name, ben_br_code, 
                                pay_mode, ben_ac_num, fc_amount, exch_rate, fc_cur, remit_amt, pay_cur, 
                                valu_dat, rmb_bank, remarks) 
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
    cur = connection.cursor()
    cur.execute(sql, step)
    connection.commit()
    insert_id = cur.lastrowid
    
    connection.close()
    
    return insert_id


def insert_references(refs):
    
    connection = create_connection()
    
    sql = ''' INSERT INTO references (ref_no, date, rem_name, ben_name, ben_bank, ben_br_name, ben_br_code, 
                                pay_mode, ben_ac_num, fc_amount, exch_rate, fc_cur, remit_amt, pay_cur, 
                                valu_dat, rmb_bank, remarks) 
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
    cur = connection.cursor()
    cur.execute(sql, refs)
    connection.commit()
    insert_id = cur.lastrowid
    
    connection.close()
    
    return insert_id
    
    
def select_all():
    
    connection = create_connection()
    
    t = []
    
    cur = connection.cursor()
    cur.execute("SELECT * FROM steps")
    connection.commit()
    rows = cur.fetchall()
    
    connection.close()
 
    for row in rows:
        t.append(list(row))
        
    return t


def login(user):
    
    connection = create_connection()
    
    sql = 'SELECT * from users WHERE username="%s" AND password="%s"'
    cur = connection.cursor()
    
    cur.execute(sql % (user[0], user[1]))
    connection.commit()
    result = cur.fetchone()
    
    connection.close()
    
    if(result is not None):
        return True
    else:
        return False