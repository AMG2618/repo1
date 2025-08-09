import sqlite3

connection = sqlite3.connect('medici.db')

cursor = connection.cursor()

sql_script = """
ALTER TABLE fisiere ADD COLUMN id_cerere_viza INTEGER DEFAULT 0;

"""

cursor.execute(sql_script)
connection.commit()


# cursor.execute("drop table fisiere;")
# connection.commit()

# sql_script = """
# CREATE TABLE fisiere (
# id INTEGER PRIMARY KEY AUTOINCREMENT,
# id_medic INTEGER,
# nume VARCHAR(127) NOT NULL,
# tip VARCHAR(127) NOT NULL,
# continut BLOB,
# emc INTEGER(2) NOT NULL,
# data TEXT,
# id_cerere_viza INTEGER DEFAULT 0,
# FOREIGN KEY (id_medic) REFERENCES medici(id)
#
# );
# """
#
# cursor.execute(sql_script)
# connection.commit()


connection.close()