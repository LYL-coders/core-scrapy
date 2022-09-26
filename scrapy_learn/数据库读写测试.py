import sqlite3

try:
    con =sqlite3.connect("niuke_info.db")
    cursor =con.cursor()
    # print("%-8s %-16s %-8s %-16s %s" % ("No", "Mark", "Price", "Image", "Note"))
    cursor.execute("select  id,title_name,img,job_detail_infos from  niuke_info_list")
    rows = cursor.fetchall()
    for row in rows:
        print("%-8s  %-16s %s"  %  (row[0],  row[1],  row[2]))
        print(row[0])
        fobj = open('read\\'+row[1].replace("/", "--")+'.jpg', "wb")
        fobj.write(row[2])
        fobj.close()

        fobj = open('read\\' + row[1].replace("/", "--") + '.txt', "w+",encoding='utf-8')
        fobj.write(row[3])
        fobj.close()
    con.close()
except Exception as err:
    print(err)


