# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 12:10:23 2018
plot data in sql database with saspy 
@author: WQQ
"""
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import MySQLdb
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import datetime
from tkcalendar import Calendar, DateEntry
import plotly as py
import plotly.graph_objs as go
import pandas as pd
LARGE_FONT= ("Verdana", 12)
conn=MySQLdb.connect(host="utspv.mysql.database.azure.com", user="sc@utspv", passwd="LQcHRNawH8sMqT6M")
cursor=conn.cursor()
USERS={'site_1': 'pvdata_home1', 'site_2':'pvdata_home1'}
TYPE=['overall_energy', 'FeedIn', 'Purchased', 'Consumption', 'SelfConsumption', 'Production']
MODULES={'battery': 'batteries', 'energy_15min':'energy_15min', 'energy_15min_detailed': 'energy_15min_detailed', 'energy_day': 'energy_day', 
        'energy_day_detailed': 'energy_day_detailed', 'sitepower': 'sitepower', 'sitepower_detailed': 'sitepower_detailed'}
class win_plot(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
 
        
        tk.Tk.wm_title(self, "PV System")
        
        container=tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames={}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):
            frame=F(container, self)
            self.frames[F]=frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)
    def show_frame(self, cont):
        frame=self.frames[cont]
        frame.tkraise()  #raise different frame according to their Z-axis order
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='GhostWhite')
        label = tk.Label(self, text="Visit Reports", font=LARGE_FONT).pack(pady=20, padx=20)
        button = ttk.Button(self, text="Report 1", 
                            command=lambda: controller.show_frame(PageOne)).pack(pady=5)
        button2 = ttk.Button(self, text="Report 2",
                            command=lambda: controller.show_frame(PageTwo)).pack(pady=5)
        button3 = ttk.Button(self, text="Report 3",
                            command=lambda: controller.show_frame(PageThree)).pack(pady=5)
        button4 = ttk.Button(self, text="Report 4",
                            command=lambda: controller.show_frame(PageFour)).pack(pady=5)
#
        pilImage = Image.open("logo.jpg")
        pilImage=pilImage.resize([600, 400])
        img = ImageTk.PhotoImage(pilImage)  
        label=tk.Label(self, image=img)
        label.image=img
        label.pack(pady=20, padx=20)


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        #up
        tk.Frame.__init__(self, parent, bg='Navy')
        label = tk.Label(self, text="Report 1!", font=LARGE_FONT).pack(pady=10, padx=10)
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage)).pack(pady=5)
        button2 = ttk.Button(self, text="Report 2",
                            command=lambda: controller.show_frame(PageTwo)).pack(pady=5)
        if conn==None:
            label2=tk.Label(self, text="connection to database failed").pack()
        else:
            
            #left_history
            user='site_1'
            datatype='overall_energy'
            selected_date='2018-05-01'
            
            f = Figure(figsize=(5,5), dpi=100)

            canvas = FigureCanvasTkAgg(f, self)
            canvas.show()
            canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    
            toolbar = NavigationToolbar2TkAgg(canvas, self)
            toolbar.update()
            canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        
            self.plot_fig(user, datatype, selected_date, f)
            #list_user
            var_user=tk.StringVar()
            lb_user=tk.Listbox(self, fg='Maroon',  font=("Verdana", 10), width=10, height=10, selectmode='BROWSER', listvariable=var_user)
            def update_item_user(event):
                user=lb_user.get(lb_user.curselection())
                self.plot_fig(user, datatype, selected_date, f)
                print('selected user')
            lb_user.bind('<ButtonRelease-1>', update_item_user)
            list_user=USERS.keys()
            for item in list_user:
                lb_user.insert('end', item)
            scrl_user=tk.Scrollbar(self)
            scrl_user.pack(side='right', fill='y')
            lb_user.configure(yscrollcommand=scrl_user.set)
            lb_user.pack(side='right', fill='both')
            scrl_user['command']=lb_user.yview
            
            #select datatype
            
            var_type=tk.StringVar()
            lb_type=tk.Listbox(self, fg='DarkCyan',  font=("Verdana", 10), width=15, height=15, selectmode='BROWSER', listvariable=var_type)
            def update_item_type(event):
                datatype=lb_type.get(lb_type.curselection())
                self.plot_fig(user, datatype, selected_date, f)
                print('selected datatype')
            lb_type.bind('<ButtonRelease-1>', update_item_type)
            list_type=TYPE
            for item in list_type:
                lb_type.insert('end', item)
            scrl_type=tk.Scrollbar(self)
            scrl_type.pack(side='right', fill='y')
            lb_type.configure(yscrollcommand=scrl_type.set)
            lb_type.pack(side='right', fill='both')
            scrl_type['command']=lb_type.yview

            #select date
            
            cal=Calendar(self, font=('Verdana', 10), selectmode='day', cursor='hand1', year=2018, month=5, day=1, width=10, borderwidth=10)
            cal.pack(fill='both', expand=True, side='top', padx=5)
            def update_date():
                selected_date=str(cal.selection_get())
                self.plot_fig(user, datatype, selected_date, f)
                print('selected date')
            bt=tk.Button(self, text='ok',  font=("Verdana", 15), command=update_date).pack()
    
    def plot_fig(self, user, datatype, selected_date, f):
        print('update fig')
        #label_fig=tk.Label(self, text=datatype+' of '+ user + ' in ' + selected_date, font=("Verdana", 12), fg='Plum').pack()
        dateTime_start=selected_date+" 00:00:00"
        dateTime_end=selected_date+" 23:45:00"

        f.suptitle(datatype+' of '+ user + ' in ' + selected_date)
        a = f.add_subplot(111)
        

        if datatype=='overall_energy':
            command="select DateTime_c, Energy from "+ USERS[user]+'.'+ MODULES['energy_15min']+" where DateTime_c>=\""+ \
                dateTime_start+"\" and DateTime_c<=\""+dateTime_end+"\" order by DateTime_c";
        else:
            command="select DateTime_c, Value_c from "+ USERS[user]+'.'+ MODULES['energy_15min_detailed']+" where DateTime_c>=\""+ \
                dateTime_start+"\" and DateTime_c<=\""+dateTime_end+"\" and Type_c=\""+ datatype + "\" order by DateTime_c";
        
        cursor.execute(command)
        conn.commit()
        alldata=cursor.fetchall()
        xx, yy=zip(*alldata)
        x=list(xx)
        y=list(yy)
        a.plot(x, y)
        
        
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='Navy')
        label = tk.Label(self, text="Report 2!", font=LARGE_FONT).pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage)).pack()

        button2 = ttk.Button(self, text="Report 3",
                            command=lambda: controller.show_frame(PageThree)).pack()
        sql ='SELECT `result_demo`.`TimeStamp`,`result_demo`.`FeedIn Price` from `pvdata_home1`.`result_demo`'
        cursor.execute(sql)  
        rows = cursor.fetchall()
        df=pd.DataFrame([[ij for ij in i] for i in rows])
        df.rename(columns={0:'time',1:'price'},inplace=True)
        trace1 = go.Scatter(
                x=df['time'],
                y=df['price'],
                mode = 'line+makers',
                name='lines+makers'
                )
        data=go.Data([trace1])
        layout=go.Layout(title="First Plot", xaxis={'title':'time'}, yaxis={'title':'price'})
        figure2=go.Figure(data=data,layout=layout)
        py.offline.iplot(figure2,filename='user_cost')
        
        
        f = Figure(figsize=(5,3), dpi=100)
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        f.suptitle('ss')
        a = f.add_subplot(111)
        a.plot(df['time'], df['price'])
        
class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='Navy')
        label = tk.Label(self, text="Report 3!", font=LARGE_FONT).pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage)).pack()
        button2 = ttk.Button(self, text="Report 4",
                            command=lambda: controller.show_frame(PageFour)).pack()
        sql ='SELECT `result_demo`.`TimeStamp`,`result_demo`.`user_netcost_before`, `result_demo`.`user_netcost_after` from `pvdata_home1`.`result_demo`'
        cursor.execute(sql)  
        rows = cursor.fetchall()
        df=pd.DataFrame([[ij for ij in i] for i in rows])
        df.rename(columns={0:'time',1:'before',2:'after'},inplace=True)
        f = Figure(figsize=(5,3), dpi=100)
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        f.suptitle('ss')
        a = f.add_subplot(111)
        a.plot(df['time'], df['before'],label='without aggregator')
        a.plot(df['time'], df['after'],label='with aggregator')
        
class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='Navy')
        label = tk.Label(self, text="Report 4!", font=LARGE_FONT).pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage)).pack()
        button2 = ttk.Button(self, text="Report 1",
                            command=lambda: controller.show_frame(PageOne)).pack()
        sql ='SELECT `result_demo`.`TimeStamp`, `result_demo`.`Provider_Bene_before`, `result_demo`.`Provider_Bene_after` from `pvdata_home1`.`result_demo`'
        cursor.execute(sql)  
        rows = cursor.fetchall()
        df=pd.DataFrame([[ij for ij in i] for i in rows])
        df.rename(columns={0:'time',1:'before',2:'after'},inplace=True)
        f = Figure(figsize=(5,3), dpi=100)
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        f.suptitle('ss')
        a = f.add_subplot(111)
        a.plot(df['time'], df['before'],label='without aggregator')
        a.plot(df['time'], df['after'],label='with aggregator')
        
def main():

    showRs=win_plot()
    showRs.mainloop()
#    cursor.close()
#    conn.close()

 
    

