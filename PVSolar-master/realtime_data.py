# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 14:55:26 2018

@author: WQQ
"""

import MySQLdb
import datetime
import time

import numpy as np
import uuid
import re


def loop(cursor, conn):
    tables=['cost', 'dsp', 'energy_30min', 'price']
    
            
    currTime=datetime.datetime.strptime("2018-05-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    count=0
    total=47
        
    def deleteData():
        print('deleting')
        for table in tables:
            sql="delete from pvdata."+ table +" where Datetime_c between \'2018-05-01 00:00:00\' and \'2018-05-02 00:00:00\'"
            cursor.execute(sql)
            conn.commit()
            
    def insertData(alldata, table):
        if len(alldata) == 0:
            return
        
        for data in alldata:
            if len(data)==4:  #no user_ID
                sql="insert into pvdata."+ table +" (ID, Dtype, Datetime_c, Value_c) values (%s, %s, %s, %s)"
                cursor.execute(sql, (data[0], data[1], data[2], str(data[3]))) #.strftime("%Y-%m-%d %H:%M:%S")
                conn.commit()
            elif len(data)==5:
                sql="insert into pvdata."+ table +" (ID, Dtype, Datetime_c, Value_c, Usr_ID) values (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (data[0], data[1], data[2], str(data[3]), data[4]))
                conn.commit()


                
    deleteData()
    while count<=total:
      
        print('Get data at %s, processing', currTime.strftime("%Y-%m-%d %H:%M:%S"))
        

        table = 'energy_30min'
        sql="select * from pvdata.energy_30min_future where dateTime_c = \'"+ currTime.strftime("%Y-%m-%d %H:%M:%S") +"\'"
        cursor.execute(sql)
        conn.commit()
        alldata_energy=cursor.fetchall()
        #model
        insertData(alldata_energy, table)
        #check
        sql="select count(*) from pvdata.energy_30min"
        cursor.execute(sql)
        conn.commit()
        alldata=cursor.fetchall()
        print(alldata)
        
        
        table = 'price'
        sql="select * from pvdata.price_future where dateTime_c = \'"+ currTime.strftime("%Y-%m-%d %H:%M:%S") +"\'"
        cursor.execute(sql)
        conn.commit()
        alldata_price=cursor.fetchall()
        #model
        insertData(alldata_price, table)
        #check
        sql="select count(*) from pvdata.price"
        cursor.execute(sql)
        conn.commit()
        alldata=cursor.fetchall()
        print(alldata)
        
        #'''
        scale_rate = 0+40*0.01;
        AQ_min = 1/100;
        AQ_max = 0.1733;# which should be computed by server by prctile(RRP,99)/1000;
        Net_Purchase_min = -145.897490802083;# which should be computed by server by min( sum(Fake_Purchased,2) - sum(Fake_FeedIn,2));
        Net_Purchase_max = 0; # which should be computed by serve by max( sum(Fake_Purchased,2) - sum(Fake_FeedIn,2));
        Net_Purchase_range = Net_Purchase_max - Net_Purchase_min;

        # input for this time point
        timestamp = alldata_energy[0][2] # TimeStamp from any table
        user = ['user1\n','user2\n','user3\n'] # UserId
        # obtain FeedIn and Purchased of all users
        data = np.array(alldata_energy)
        dtype = data[:,1]
        value = data[:,3].astype(np.float)
        index_f = (dtype=='FeedIn')
        index_p = (dtype=='Purchased')
        userid_f = data[index_f,4]
        userid_p = data[index_p,4]
        if (userid_f==userid_p).all():
            FeedIn = value[index_f]
            Purchased = value[index_p]
            userid = userid_f   
            #FeedIn = np.array([3.85798079030000,	2.44575689489000,	2.08391803255000]);
            #Purchased = np.array([3.56806775079000,	2.19059255015000,	1.87507013092000]);
            SumPurchased = np.array([48.8151589513824,62.9918105222459,37.7017349426707,8.03780861577394,4.33976431520484,1.58192693391499,1.61067034136860,3.16251331649835,1.75737585723928,1.75369958915228,1.62690315509288,1.30840891552204,3.67843211904717,45.8662698745820,24.4912465647763,61.8029594378762,307.065603223986,239.862557279634,62.8551582573023,6.87582326171498,591.879777909027,1158.45594907866,1282.16144636815,1280.17908195847,1292.81913685958,1106.64576692953,1212.38278230956,1154.05509928587,879.726727328865,851.833905166791,711.475821022976,530.759069300600,323.353870516561,175.556557613119,143.283981962203,219.521224929475,134.189471750596,98.4086607626385,124.571393966336,147.158178510400,293.556874676598,107.759926994051,111.810964475887,96.4707225600055,83.7718324694369,394.167985879476,165.717927616069,168.472083945483])
            SumFeedIn = np.array([93.1382336708669,109.638664862180,79.3449108328915,39.3791132677787,31.1909127000448,24.2657805308656,23.8438402550048,28.6981110538529,24.3867587040967,26.1186307257915,26.4571539930127,23.4368698772370,29.8906882842486,89.5573624927841,63.8128439824400,109.461992492360,376.988749207871,302.944091207692,109.756195567943,37.8696492600785,676.410352345201,1273.26242331149,1403.99190236696,1401.41479369873,1414.50998443808,1217.55580237256,1330.78731386529,1268.44659015600,979.392653426086,951.773689686848,803.514522512657,611.576549683880,392.451225522830,233.567663002764,200.668178515490,281.425342737560,189.473654216905,150.170945196746,179.023779617699,202.836999877506,359.698325516712,160.696073250510,165.880631375197,150.122847542355,134.162257978915,467.875850593651,222.153885876625,227.077314487378])
            SumPurchased_point = SumPurchased[count]
            SumFeedIn_point = SumFeedIn[count]

        # obtain price
        data_p = np.array(alldata_price)
        p_dtype = data_p[:,1]
        p_value = data_p[:,3].astype(np.float)
        AP = p_value[(p_dtype=='Price_Sell')]#0.54; # Price_Sell from Price table
        Q = p_value[(p_dtype=='Price_FeedIn')]#0.1237;# Price_FeedIn from Price table
        Price_Grid = p_value[(p_dtype=='Price_Grid')]# Price_Grid from Price table
    
        #compute output of this time point
        #before aggregator
        user_netcost_before = AP*Purchased - AQ_min*FeedIn
        
        Provider_ren_before = AP * SumFeedIn_point
        #Provider_cost_before = Price_Grid* np.max((0,(np.sum(FeedIn) - SumPurchased_point))) + AQ_min*np.sum(FeedIn) #wrong
        Provider_cost_before = Price_Grid* np.max((0,(SumPurchased_point-SumFeedIn_point))) + AQ_min*SumFeedIn_point
        Provider_Bene_before = Provider_ren_before - Provider_cost_before
        
        #Pricing model
        try:
            Net_FeedIn
        except NameError:
            Net_FeedIn = 0
            
        Net_FeedIn = np.max((0,Net_FeedIn+SumFeedIn_point-SumPurchased_point))
        Q = AQ_min+ (SumPurchased_point - SumFeedIn_point - Net_Purchase_min)/Net_Purchase_range*(AQ_max-AQ_min)
        
        #after aggregator
        user_netcost_after = AP*Purchased - Q*FeedIn
        
        Provider_ren_after = AP * SumFeedIn_point
        Provider_cost_after = Price_Grid* np.max((0,(SumPurchased_point - np.sum(Net_FeedIn)))) + Q*np.sum(FeedIn)
        Provider_Bene_after = (1+scale_rate)*(Provider_ren_before - Provider_cost_before)
        #item_id=str(uuid.uuid1())
        alldata_DSP = ((str(uuid.uuid1()),'Benefit_after',timestamp,Provider_Bene_after),(str(uuid.uuid1()),'Benefit_before',timestamp,Provider_Bene_before))
        alldata_cost = ()
        for u in user:
            index_u = (userid==u)
            before = (str(uuid.uuid1()),'Cost_before',timestamp,user_netcost_before[index_u],u)
            alldata_cost = alldata_cost+(before,)
            after = (str(uuid.uuid1()),'Cost_after',timestamp,user_netcost_after[index_u],u)
            alldata_cost = alldata_cost+(after,)
            #'''
        # add tabel DSP
        insertData(alldata_DSP, 'dsp')
        # add table cost
        insertData(alldata_cost, 'cost')
        
        #next time period    
        count=count+1
        currTime=currTime+datetime.timedelta(minutes=30)
        print(count, total)
        if count==total:
            count=0
            currTime=datetime.datetime.strptime("2018-05-01 00:00:00", "%Y-%m-%d %H:%M:%S")
            deleteData()
                
            
        
        
if __name__=='__main__':    
    conn=MySQLdb.connect(host="utspv.mysql.database.azure.com", user="sc@utspv", passwd="LQcHRNawH8sMqT6M")
    #conn.autocommit=True  #not support
    cursor=conn.cursor()
    loop(cursor, conn)
    
        #close database
    cursor.close()
    conn.close()
    