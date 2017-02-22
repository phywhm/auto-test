#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import MySQLdb
import configuration as CONFIG


class CloudDB(object):
    def __init__(self, host=None, port=3306, user="cloudplayer", passwd="123qwe"):
        if host is None:
            reload(CONFIG)
            self.host = CONFIG.DB_HOST
            self.port = CONFIG.DB_PORT
            self.user = CONFIG.DB_USER
            self.passwd = CONFIG.DB_PASSWD
        else:
            self.host = host
            self.port = port
            self.user = user
            self.passwd = passwd
        self.cur = None


    def __connect_db(self):
        self.conn = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, charset="utf8")

    def __close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def get_instance_id_by_cid(self, cid):
        result = None
        try:
            self.__connect_db()
            self.cur = self.conn.cursor()
            selectsql = "select instance_id from tb_cid_instance_pool where cid=%s" %(cid)
            self.conn.select_db("saas_core")
            """cur.execute 返回的是行数, 可以根据行数进行判断处理"""
            self.cur.execute(selectsql)
            result = self.cur.fetchone()[0]
            return result
        finally:
            self.__close()


    def get_display_info(self, cid):
        result = None
        try:
            self.__connect_db()
            self.cur = self.conn.cursor()
            selectsql = "select params_info from tb_cid_instance_pool where cid=%s" %(cid)
            self.conn.select_db("saas_core")
            self.cur.execute(selectsql)
            result = self.cur.fetchone()[0]
            return result
        finally:
            self.__close()


    def get_games(self):
        result = []
        try:
            self.__connect_db()
            self.cur = self.conn.cursor()
            selectsql = "select app from instance_app"
            self.conn.select_db(CONFIG.PASS_DB)
            self.cur.execute(selectsql)
            for row in self.cur.fetchall():
                result.append(row[0])
            return result
        finally:
            self.__close()


    def get_instance_status_by_cid(self, cid):
        result = None
        try:
            self.__connect_db()
            self.cur = self.conn.cursor()
            selectsql = "select status from tb_cid_instance_pool where cid=%s" %(cid)

            self.conn.select_db("saas_core")
            rows_num = self.cur.execute(selectsql)
            if rows_num >= 1:
                result = self.cur.fetchone()[0]
            print result, rows_num
            return result
        finally:
            self.__close()



    def check_cid_existed(self, cid):
        try:
            self.__connect_db()
            self.cur = self.conn.cursor()
            selectsql = "select cid from tb_cloudplay_info where cid=%s" %(cid)
            self.conn.select_db("saas_auth")
            rows_num = self.cur.execute(selectsql)
            if rows_num:
                return True
            else:
                return False
        finally:
            self.__close()

    def get_key(self, access_key):
        result = None
        try:
            self.__connect_db()
            self.cur = self.conn.cursor()
            selectsql = "select apin_appkey from tb_app_info where apin_appid='%s'" % (access_key)
            self.conn.select_db("saas_auth")
            rows_num = self.cur.execute(selectsql)
            if rows_num >= 1:
                result = self.cur.fetchone()[0]
            return result
        finally:
            self.__close()

    def update_access_limit(self, access_key, limit=1000, current=500):
        try:
            self.__connect_db()
            self.cur = self.conn.cursor()
            selectsql = "update tb_cp_instance_statistics set instance_limit=%s, instance_count=%s where cpid='%s'" %(limit, current, access_key)
            self.conn.select_db("saas_core")
            self.cur.execute(selectsql)
            self.conn.commit()
        finally:
            self.__close()

    def update_config(self, config):
        try:
            self.__connect_db()
            self.cur = self.conn.cursor()
            selectsql = "update tb_config_info set value='%s'" % (config)
            self.conn.select_db("saas_auth")
            self.cur.execute(selectsql)
            self.conn.commit()
        finally:
            self.__close()

    def delete_instance_record(self, cid):
        try:
            self.__connect_db()
            self.cur = self.conn.cursor()
            selectsql = "delete from tb_cid_instance_pool where cid=%s" %(cid)
            self.conn.select_db("saas_core")
            self.cur.execute(selectsql)
            self.conn.commit()
        finally:
            self.__close()

    def get_access_limit(self, access_key):
        result = None
        try:
            self.__connect_db()
            self.cur = self.conn.cursor()
            selectsql = "select instance_count from tb_cp_instance_statistics  where cpid='%s'" %(access_key)
            self.conn.select_db("saas_core")
            self.cur.execute(selectsql)
            result = self.cur.fetchone()[0]
            return result
        finally:
            self.__close()



if __name__ == "__main__":
    mydb =  CloudDB("172.16.2.16")
    print mydb.get_instance_status_by_cid("123")
