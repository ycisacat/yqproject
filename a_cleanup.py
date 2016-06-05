__author__ = 'yc'

from crawler.class_save_data import *
import shutil

class Clean(Database):
    def __init__(self):
        Database.__init__(self)

    def clean(self):
        with self.conn:
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            sql1 = "DELETE FROM event"
            sql2 = "Delete from content"
            cur.execute(sql1)
            cur.execute(sql2)
        shutil.rmtree('../yqproject/documents/topic')
        shutil.rmtree('../yqproject/static/sna')

Clean().clean()