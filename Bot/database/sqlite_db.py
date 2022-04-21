import sqlite3 as sq

def on_start():
    global db , cur
    db = sq.connect('database.db')
    cur =db.cursor()
    if db:
        print('DB connected')

async def get_inf(table_name, param_name=None, param=None):
    try:
        if param_name == None:
            res = cur.execute(f'SELECT * FROM {table_name}').fetchall()
        else:
            res = cur.execute(f'SELECT * FROM {table_name} WHERE {param_name}={param}').fetchall()
        print(res)
        return res
    except:
        pass

def add_User(state):
    try:
        with state.proxy as data:
            cur.execute(f'INSERT INTO Users VALUES(?,?,?,?,?,?,?,?)',tuple(data.values).append('student'))
    except:
        pass        
