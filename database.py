# -*- coding: utf-8 -*-
"""
Created on Sun May  9 10:33:08 2021

@author: uidq9030
"""

import pymysql
from datetime import datetime


class database:

   
    
    def __init__(self):
        
        
        self.host = "db-seguin-std.cluster-cghcu111mwnq.us-east-1.rds.amazonaws.com"
        self.username = "uidq9030"
        self.password = "Fmhdtmb452"
        self.dbname = "automon"
        self.conn = None
        
        print('host', self.host)
         
    def open_connection(self):
        
        
        try:
            print('try Open', self.host)
            
            if self.conn is None:
                self.conn = pymysql.connect(
                    host=self.host,
                    user=self.username,
                    password=self.password,
                    database= self.dbname,
                    connect_timeout = 5
                )
                   
        except pymysql.MySQLError as e:
            print('Exception')
       #     logger.error(e)
       #     sys.exit()
        finally:
            print ('Opened')
        #    logger.info('Connection opened successfully.')
        
        
    def close_connection(self):
    
         # disconnect from server
         #db.close()   
         if self.conn:
             self.conn.close()
             self.conn = None    


    def insert_row(self, val):
        
        cmd = """INSERT INTO aiholeandfillettopresults(datetime, 
        serialnumber,nok, ok, score, prediction, cycletime, image, directory, ftp, results1, results2) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        try:
            
            self.open_connection()
            with self.conn.cursor() as cur:
                result = cur.execute(cmd, val)
                self.conn.commit()
                #affected = f"{cur.rowcount} rows affected."
                cur.close()
                return result
            # Execute the SQL command
          #  cursor.execute(cmd, val)
            # Commit your changes in the database
            #self.db.commit()
        except Exception as e:
            # Rollback in case there is any error
            self.db.rollback()
            print ("Exception error insert()",e.args[0])
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None
                print ('Db Closed')   
        
        
            
    def run_query(self, query):
         
        try:
            print('Run Query')
            self.open_connection()
            with self.conn.cursor() as cur:
                if 'SELECT' in query:
                    records = []
                    cur.execute(query)
                    result = cur.fetchall()
                    for row in result:
                        records.append(row)
                    cur.close()
                    return records
                result = cur.execute(query)
                self.conn.commit()
                affected = f"{cur.rowcount} rows affected."
                cur.close()
                return affected
             
        except pymysql.MySQLError as e:
             print('Exception',e.args[0])
            
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None
                print ('Db Closed')
 
    def openclosetest(self):
        
        self.open_connection()
            
        if self.conn:
            self.conn.close()
            self.conn = None
            print('Closed')
    
    

#db = database()

#now = datetime.now()
 
#dt_string = now.strftime('%Y-%m-%d %H:%M:%S')
#val = (dt_string, 123456, 0.6, 0.7, 0.7, 'NOK', 0.4,'test','dirtest',0,'result1 sdfdf','result2 scds')

#data = db.insert_row(val)
#print (data)
#db .openclose()
#query = "SELECT * FROM aiholeandfillettopresults"

#data = db.run_query(query)

#print(data)

#if __name__ == '__main__':
#    print ("main")
#    database()              