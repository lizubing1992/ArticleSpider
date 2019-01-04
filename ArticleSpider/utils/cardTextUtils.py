# -*- coding: utf-8 -*-
import MySQLdb
import MySQLdb.cursors


class UploadText(object):
    def db_connection(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'root', 'spider', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def execute_no_query(self, command_text, parameters=None):
        effectRow = 0
        try:
            self.db_connection()
            effectRow = self.cursor.execute(command_text, parameters)
        except Exception as e:
            print(e)
        finally:
            self.cursor.close()
            return effectRow

    def db_close(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
