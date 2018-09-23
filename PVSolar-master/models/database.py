
import datetime
import sqlite3
import json
import uuid
class Database:

    def __init__(self):
        sqlite_file='my_db.sqlite'
        self.conn = sqlite3.connect(sqlite_file)
        self.cursor = self.conn.cursor()
        

    def energy_detail(self, userid: str, start_datetime : datetime, end_datetime : datetime):
        userid=  'user'+userid+'\n'
        sql = "select * from `energy_30min` where `Usr_ID`=? and `DateTime_c` between ? and ? order by `DateTime_c`"
        self.cursor.execute(sql, (userid, start_datetime.strftime("%Y-%m-%d %H:%M:%S"), end_datetime.strftime("%Y-%m-%d %H:%M:%S")))
        self.conn.commit()
        rows = self.cursor.fetchall()
        '''
        rows=list(rows)
        for i in range(0, len(rows)):
            rows[i]=list(rows[i])
            if rows[i][1] in ['Production', 'FeedIn']:
                rows[i][3]=rows[i][3]/1000 
            rows[i]=tuple(rows[i])
        rows=tuple(rows)
        '''
        sql="select * from `energy_after` where `Usr_ID`=? and `DateTime_c` between ? and ? order by `DateTime_c`"
        self.cursor.execute(sql, (userid, start_datetime.strftime("%Y-%m-%d %H:%M:%S"), end_datetime.strftime("%Y-%m-%d %H:%M:%S")))
        self.conn.commit()
        rows2 = self.cursor.fetchall()

        return rows+rows2
        

    def price_detail(self, start_datetime : datetime, end_datetime : datetime):
        sql = "select * from `price` where `DateTime_c` between ? and ? order by `DateTime_c`"
        self.cursor.execute(sql, (start_datetime.strftime("%Y-%m-%d %H:%M:%S"), end_datetime.strftime("%Y-%m-%d %H:%M:%S")))
        self.conn.commit()
        rows = self.cursor.fetchall()
        
        sql = "select * from `price_after` where `DateTime_c` between ? and ? order by `DateTime_c`"
        self.cursor.execute(sql, (start_datetime.strftime("%Y-%m-%d %H:%M:%S"), end_datetime.strftime("%Y-%m-%d %H:%M:%S")))
        self.conn.commit()
        rows2 = self.cursor.fetchall()

        return rows+rows2

    def dsp_detail(self, start_datetime : datetime, end_datetime : datetime):
        sql = "select * from `dsp` where `DateTime_c` between ? and ? order by `DateTime_c`"
        self.cursor.execute(sql, (start_datetime.strftime("%Y-%m-%d %H:%M:%S"), end_datetime.strftime("%Y-%m-%d %H:%M:%S")))
        self.conn.commit()
        rows = self.cursor.fetchall()

        return rows
        
    def cost_detail(self, userid : str, start_datetime : datetime, end_datetime : datetime):
        userid=  'user'+userid+'\n'
        sql = "select * from `cost` where `Usr_ID`= ? and `DateTime_c` between ? and ? order by `DateTime_c`"
        self.cursor.execute(sql, (userid, start_datetime.strftime("%Y-%m-%d %H:%M:%S"), end_datetime.strftime("%Y-%m-%d %H:%M:%S")))
        self.conn.commit()
        rows = self.cursor.fetchall()

        return rows
    def upload(self, data : str):
        #data="[{\"name\":\"table_energy\",\"value\":[[[\"Consumption\",\"2018-08-17 20:30:00\",1,0.0955],[\"Consumption\",\"2018-08-17 20:30:00\",2,0.9071229467999998],[\"Consumption\",\"2018-08-17 20:30:00\",3,0.0209748942]],[[\"FeedIn\",\"2018-08-17 20:30:00\",1,0],[\"FeedIn\",\"2018-08-17 20:30:00\",2,0],[\"FeedIn\",\"2018-08-17 20:30:00\",3,0.01995971468400001]],[[\"Production\",\"2018-08-17 20:30:00\",1,0.0955],[\"Production\",\"2018-08-17 20:30:00\",2,0.2572388],[\"Production\",\"2018-08-17 20:30:00\",3,0.04134195000000001]],[[\"Purchased\",\"2018-08-17 20:30:00\",1,0],[\"Purchased\",\"2018-08-17 20:30:00\",2,0.6336527465984171],[\"Purchased\",\"2018-08-17 20:30:00\",3,0]],[[\"SelConsumption\",\"2018-08-17 20:30:00\",1,0.107],[\"SelConsumption\",\"2018-08-17 20:30:00\",2,0.016231400201582757],[\"SelConsumption\",\"2018-08-17 20:30:00\",3,0.0209748942]]]},{\"name\":\"table_price\",\"value\":[[\"Price Sell\",\"2018-08-17 20:30:00\",0.23],[\"Price Grid\",\"2018-08-17 20:30:00\",0.09462999999999999],[\"Price FeedIn\",\"2018-08-17 20:30:00\",0.06283670917611807]]},{\"name\":\"table_DSP\",\"value\":[[\"DSP_benefit_before\",\"2018-08-17 20:30:00\",8.354068816980314],[\"DSP_benefit_after\",\"2018-08-17 20:30:00\",10.790874427174499]]},{\"name\":\"table_cost\",\"value\":[[[\"Cost Before\",\"2018-08-17 20:30:00\",1,0],[\"Cost Before\",\"2018-08-17 20:30:00\",2,0.06051383730014883],[\"Cost Before\",\"2018-08-17 20:30:00\",3,-0.0001995971468400001]],[[\"Cost After\",\"2018-08-17 20:30:00\",1,0],[\"Cost After\",\"2018-08-17 20:30:00\",2,0.06051383730014883],[\"Cost After\",\"2018-08-17 20:30:00\",3,-0.001254202786836802]]]}]"
        print('fff')
        print(data)
        json_dic=json.loads(data)
        print(json_dic)
        for each_tabel in json_dic:

            tableName=each_tabel['name']
            tableValue=each_tabel['value']
            if tableName=='table_energy' or tableName=='table_cost':  
                for each_value in tableValue:
                    for each_value2 in each_value:
                        item_id=str(uuid.uuid1())
                        #if tableName=='table_cost' or tableName=='table_energy':
                        if tableName=='table_cost':
                            userName='user'+str(each_value2[2])+'\n'
                            sqlCheck="select * from cost where Datetime_c=?"
                            self.cursor.execute(sqlCheck, [(each_value2[1])])
                            if (len(self.cursor.fetchall())!=0):
                                continue
                            sql="insert into cost (ID, Dtype, Datetime_c, Value_c, Usr_ID) values (?, ?, ?, ?, ?)"

                            self.cursor.execute(sql, (item_id, each_value2[0], each_value2[1],  str(each_value2[3]), userName))
                            self.conn.commit()
                        elif  tableName=='table_energy':  
                            userName='user'+str(each_value2[2])+'\n'
                            sqlCheck="select * from energy_30min where Datetime_c=?"
                            self.cursor.execute(sqlCheck, [(each_value2[1])])
                            if (len(self.cursor.fetchall())!=0):
                                continue
                            sql="insert into energy_30min (ID, Dtype, Datetime_c, Value_c, Usr_ID) values (?, ?, ?, ?, ?)"
                            self.cursor.execute(sql, (item_id, each_value2[0], each_value2[1],  str(each_value2[3]), userName))
                            self.conn.commit()
            elif tableName=='table_price' or tableName=='table_DSP':
                for each_value in tableValue:
                    item_id=str(uuid.uuid1())
                    if tableName=='table_price':
                        sqlCheck="select * from price where Datetime_c=?"
                        self.cursor.execute(sqlCheck, [(each_value[1])])
                        if (len(self.cursor.fetchall())!=0):
                            continue
                        sql="insert into price (ID, Dtype, Datetime_c, Value_c) values (?, ?, ?, ?)"
                        self.cursor.execute(sql, (item_id, each_value[0], each_value[1],  str(each_value[2])))
                        self.conn.commit()
                    elif tableName=='table_DSP':
                        sqlCheck="select * from dsp where Datetime_c=?"
                        self.cursor.execute(sqlCheck, [(each_value[1])])
                        if (len(self.cursor.fetchall())!=0):
                            continue
                        sql="insert into dsp (ID, Dtype, Datetime_c, Value_c) values (?, ?, ?, ?)"
                        self.cursor.execute(sql, (item_id, each_value[0], each_value[1],  str(each_value[2])))
                        self.conn.commit()

        return True


