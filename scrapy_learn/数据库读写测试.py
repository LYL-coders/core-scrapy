import sqlite3

try:
    con =sqlite3.connect("test.db")
    cursor =con.cursor()
    # print("%-8s %-16s %-8s %-16s %s" % ("No", "Mark", "Price", "Image", "Note"))
    cursor.execute("select  id,title_name,img from  test")
    rows = cursor.fetchall()
    for row in rows:
        print("%-8s  %-16s %s"  %  (row[0],  row[1],  row[2]))
        print(row[0])
        fobj = open('read\\'+row[1].replace("/", "--")+'.jpg', "wb")
        fobj.write(row[2])
        fobj.close()
    con.close()
except Exception as err:
    print(err)


