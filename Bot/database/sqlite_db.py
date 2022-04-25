import sqlite3 as sq

def on_start():
    global db , cur
    db = sq.connect('database.db')
    cur =db.cursor()
    if db:
        print('DB connected')

def get_inf(table_name, param_name=None, param=None):
    if param_name == None:
        res = cur.execute(f'SELECT * FROM {table_name}').fetchall()
    else:
        res = cur.execute(f'SELECT * FROM {table_name} WHERE {param_name}=?',(param,)).fetchall()
    print(res)
    return res

async def add_User(state):
    
    async with state.proxy() as data:
        dt = list(data.values())
        dt.append('student')
        tuple(dt)
        cur.execute(f'INSERT INTO Users (telegram_id,username,name,surname,grade_num,grade_letter,status) VALUES(?,?,?,?,?,?,?)',dt)
        db.commit()

async def add_Event(state):
    
    async with state.proxy() as data:
        dt = list(data.values())
        tuple(dt)
        cur.execute(f'INSERT INTO Events (name,description, date) VALUES(?,?,?)',dt)
        db.commit() 

async def get_Grade(state):
    async with state.proxy() as data:
        print(data)
        dt = list(data.values())
        tuple(dt)
        await cur.execute(f'SELECT * FROM Users WHERE grade_num =? AND grade_letter = ? ', dt)      

if __name__ == "__main__":
    on_start()
    get_inf('Users', 'status','teacher')
    