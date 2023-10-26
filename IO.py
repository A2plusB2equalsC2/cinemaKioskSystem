import sqlite3 as sql

#houses (no integer primary key,row integer not null,col integer not null)
#films (h integer,name text,date text,time text,taken text, price real)

#conn = sql.connect("datas.db")
#c = conn.cursor()
#c.execute("""
#""")
#conn.commit()
#print(c.fetchall())
#conn.close()

def fetchhouses():
  list = []
  conn = sql.connect("datas.db")
  c = conn.cursor()
  c.execute("""SELECT * FROM houses
  ORDER BY no ASC""")
  conn.commit()
  list = c.fetchall()
  conn.close()
  return list

def fetchfilms():
  list = []
  conn = sql.connect("datas.db")
  c = conn.cursor()
  c.execute("""SELECT * FROM films
  ORDER BY name, h""")
  conn.commit()
  list = c.fetchall()
  conn.close()
  return list

def fetchseats(name,house):
  list = []
  conn = sql.connect("datas.db")
  c = conn.cursor()
  c.execute(f"""SELECT * FROM houses
  WHERE no = {house}
  """)
  conn.commit()
  h = c.fetchall()[0]
  for i in range(h[1]):
    list.append([])
    for j in range(h[2]):
      list[i].append("0")
  c.execute(f"""SELECT taken FROM films
  WHERE h = {house} AND name = '{name}'
  """)
  conn.commit()
  t = c.fetchall()[0][0]
  t = t.split(",")
  t.pop(-1)
  for i in t:
    r = ord(i[0]) - 65
    c = int(i[1:]) - 1
    list[r][c] = "x"
  conn.close()
  return list

def selectseat(name,house,str):
  conn = sql.connect("datas.db")
  c = conn.cursor()
  c.execute(f"""UPDATE films SET taken='{str}'
  WHERE name = '{name}' AND h = {house}
  """)
  conn.commit()
  conn.close()
  return

def newfilm(name,house,date,time,price):
  conn = sql.connect("datas.db")
  c = conn.cursor()
  c.execute(f"""INSERT INTO films VALUES ({house},'{name}','{date}','{time}','',{price})
  """)
  conn.commit()
  conn.close()
  return

def newhouse(no,row,col):
  conn = sql.connect("datas.db")
  c = conn.cursor()
  c.execute(f"""INSERT INTO houses VALUES ({no}, {row}, {col})
  """)
  conn.commit()
  conn.close()
  return

def deletefilm(name,house):
  conn = sql.connect("datas.db")
  c = conn.cursor()
  c.execute(f"""DELETE FROM films 
  WHERE name = '{name}' AND h = {house}
  """)
  conn.commit()
  conn.close()
  return

def deletehouse(no):
  conn = sql.connect("datas.db")
  c = conn.cursor()
  c.execute(f"""DELETE FROM films 
  WHERE h = {no}
  """)
  conn.commit()
  c.execute(f"""DELETE FROM houses 
  WHERE no = {no}
  """)
  conn.commit()
  conn.close()
  return

def checkseats(name,house):
  no = 0
  conn = sql.connect("datas.db")
  c = conn.cursor()
  c.execute(f"""SELECT row,col FROM houses
  WHERE no = {house}
  """)
  conn.commit()
  rc = c.fetchall()[0]
  row = rc[0]
  col = rc[1]
  no = row*col
  c.execute(f"""SELECT taken FROM films
  WHERE h = {house} AND name = '{name}'
  """)
  conn.commit()
  t = c.fetchall()[0][0]
  t = t.split(",")
  t.pop(-1)
  no -= len(t)
  conn.close()
  return no