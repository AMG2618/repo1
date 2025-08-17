# get schema of table fisiere from medici.db
import sqlite3
connection= sqlite3.connect('medici.db')
cursor = connection.cursor()
cursor.execute("PRAGMA table_info(fisiere);")
schema = cursor.fetchall()
# print schema details
for column in schema:
    print(f"Column: {column[1]}, Type: {column[2]}, Not Null: {column[3]}, Default: {column[4]}, Primary Key: {column[5]}")
connection.close()
#
# cursor.execute("PRAGMA table_info(medici);")
# schema = cursor.fetchall()
# # print schema details
# for column in schema:
#     print(f"Column: {column[1]}, Type: {column[2]}, Not Null: {column[3]}, Default: {column[4]}, Primary Key: {column[5]}")
# connection.close()
