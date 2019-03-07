# -*- coding: utf-8 -*-
import os
import sys
import MySQLdb
import MySQLdb.cursors

project_dir = os.path.abspath(os.path.dirname(__file__))
card = os.path.join(project_dir, "card")
# list = ["birthday.txt", "lantern.txt", "lover.txt", "new_year_eve.txt", "spring.txt"]
# list_type = ["birthday", "lantern", "lover", "new_year_eve", "spring"]
list = ["woman.txt"]
list_type = ["woman"]
conn = MySQLdb.connect('127.0.0.1', 'root', 'root', 'spider', charset="utf8", use_unicode=True)
cursor = conn.cursor()
for index in range(len(list)):
    file_path = os.path.join(card, list[index])
    file = open(file_path, 'r', encoding='utf-8')
    card_type = list_type[index]
    for line in file.readlines():
        sql = """
            insert into cover_wishes(wish_type, wish_content)
            VALUE (%s, %s)
        """
        try:
            cursor.execute(sql, (card_type, line))
            conn.commit()
            print(line)
        except Exception as e:
            print(e)

conn.close()