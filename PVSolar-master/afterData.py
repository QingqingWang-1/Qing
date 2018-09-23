# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 19:31:47 2018

@author: WQQ
"""

import MySQLdb
import datetime
import time

import numpy as np
import uuid

path_file={'energy_after':'C:\WQQ\PV Project\data\data-consumptionAfter.txt', 'price_after':'C:\WQQ\PV Project\data\priceAfter.txt'}
def insertAfterData(cursor, conn):
    print('energy...')
    with open(path_file['energy_after']) as f:
        for line in f:
            content=[elt for elt in line.split(';')]
            item_id=str(uuid.uuid1())
            currTime=datetime.datetime.strptime(content[1], "%Y-%m-%d %H:%M:%S")
            if (datetime.datetime(2018,5,1,6,0,0) - currTime).total_seconds()>0:  #before 6, keep
                value_c=content[2]
            elif (datetime.datetime(2018,5,1,14,0,0) - currTime).total_seconds()>0: #6-10
                value_c=max(0, float(content[2])-50)
                value_c=str(value_c)
            elif (datetime.datetime(2018,5,1,17,0,0) - currTime).total_seconds()>0:
                value_c=max(0, float(content[2])+50)
                value_c=str(value_c)
            elif (datetime.datetime(2018,5,1,22,0,0) - currTime).total_seconds()>0:
                value_c=max(0, float(content[2])-30)
                value_c=str(value_c)
            elif (datetime.datetime(2018,5,1,23,0,0) - currTime).total_seconds()>0:
                value_c=max(0, float(content[2])+30)
                value_c=str(value_c)
            else:
                value_c=content[2]
            type_c='consumption_after'            
            sql="insert into pvdata.energy_after (ID, Dtype, Datetime_c, Value_c, Usr_ID) values (%s, %s, %s, %s, %s)"
            
            cursor.execute(sql, (item_id, type_c, content[1], value_c, content[3]))
            conn.commit()
    print('price')
    with open(path_file['price_after']) as f:
        for line in f:
            content=[elt for elt in line.split(';')]
            item_id=str(uuid.uuid1())
            currTime=datetime.datetime.strptime(content[1], "%Y-%m-%d %H:%M:%S")
            value_c=str(max(0, float(content[2])-0.05))
                          
            sql="insert into pvdata.price_after (ID, Dtype, Datetime_c, Value_c) values (%s, %s, %s, %s)"
            
            cursor.execute(sql, (item_id, 'Grid_price_after', content[1], value_c))
            conn.commit()
    

if __name__=='__main__':    
    conn=MySQLdb.connect(host="utspv.mysql.database.azure.com", user="sc@utspv", passwd="LQcHRNawH8sMqT6M")
    cursor=conn.cursor()
    insertAfterData(cursor, conn)
    cursor.close()
    conn.close()
