import re
import sqlite3
class DataBaseController:
    def __init__(self, conn):
        self.conn=conn
    def read(self,table):
        print("Read")
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM {}".format(table))
        for row in cursor:
            print(row)
        cursor.close()
    def insert_bus(self,veh_no,capacity):
        cursor = self.conn.cursor()
        cursor.execute("""INSERT INTO bus (veh_no, capacity) VALUES (?, ?)""",(veh_no,capacity))
        conn.commit()
        cursor.close()
    def insert_tour(self,tour_id,bus_id,destination,price):
        cursor = self.conn.cursor()
        cursor.execute("""INSERT INTO tour (tour_id,bus_id, destination,unit_price) VALUES (?,?,?,?)""",(tour_id,bus_id,destination,price))
        conn.commit()
        cursor.close()
    def reserve_seat(self,num_seats,bus_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT capacity FROM bus WHERE bus_id={}".format(bus_id))
        capacity=cursor.fetchone()[0]
        cursor.execute("UPDATE bus SET booked_seats={} WHERE bus_id={}".format(num_seats,bus_id))
        conn.commit()
        cursor.close()
    def print_main_table(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT tour_id, destination,unit_price,bus.bus_id,bus.veh_no,bus.capacity,bus.booked_seats  FROM tour INNER JOIN bus ON tour.bus_id = bus.bus_id")
        for row in cursor:
            print(row)
        cursor.close()
    def delete(self,table):
        print("Delete Previous values")
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM {}".format(table))
        cursor.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME={}".format(table))
        conn.commit()
        cursor.close()
        
def Database():
    global conn, cursor
    conn = sqlite3.connect("bus_db.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, username TEXT, password TEXT,email TEXT DEFAULT NULL)")       
    cursor.execute("CREATE TABLE IF NOT EXISTS `bus` (bus_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, veh_no TEXT, capacity INT,booked_seats INTEGER DEFAULT 0)")       
    cursor.execute("CREATE TABLE IF NOT EXISTS `tour` (tour_id INTEGER NOT NULL, bus_id INTEGER NOT NULL, destination TEXT, unit_price INTEGER DEFAULT 0, PRIMARY KEY(tour_id,bus_id), FOREIGN KEY(bus_id) REFERENCES bus(bus_id))")       
    
    cursor.execute("SELECT * FROM `member` WHERE `username` = 'user1' AND `password` = '1234'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO `member` (username, password,email) VALUES('user1', '1234','user1@tour.com')")
        conn.commit()
    #cursor.close()
    return conn


    
def reserve_booking(tour_id,no_adult,no_child):
    cursor = conn.cursor()
    cursor.execute("SELECT bus_id FROM tour WHERE tour_id={}".format(tour_id))
    buses=[]
    for row in cursor:
        buses.append(row[0])
    seats_available=False
    lbl_text.configure(text="")
    for bus_id in buses:
        cursor.execute("SELECT capacity,booked_seats FROM bus WHERE bus_id={}".format(bus_id))
        capacity,reserved_seats=cursor.fetchone()
        if no_adult=='':
            no_adult=0
        if no_child=='':
            no_child=0
        
        no_adult=int(no_adult)
        no_child=int(no_child)
        capacity=int(capacity)
        reserve_seats=int(reserved_seats)
        if reserved_seats+no_adult+no_child<capacity:
            seats_available=True
            cursor = conn.cursor()
            num_seats=no_adult+no_child
            cursor.execute("UPDATE bus SET booked_seats={} WHERE bus_id={}".format(reserved_seats+num_seats,bus_id))
            conn.commit()
            cursor.close()
        if seats_available:
            break
        
    if seats_available==False:
        lbl_text.configure(text="No Seat Available for this tour")
    if no_adult>0 and no_child>0: 
        lbl_text.configure(text="Your booking for tour is confirmed.")
    
    return
    
    
def calculate_fare(tour_id,no_adult,no_child):
    #============================FETCH ENTRIES FROM DB============================
    
    cursor = conn.cursor()
    cursor.execute("SELECT unit_price FROM tour WHERE tour_id={}".format(tour_id))
    uPrice=cursor.fetchone()[0]
    cursor.close()
    
    if no_adult=='':
        no_adult=0
    if no_child=='':
        no_child=0
    total_price=(float(no_adult)*float(uPrice))+(float(no_child)*float(uPrice)*0.5) # 50% discount for children
    print(total_price)
    total_entry.delete(0, "end")
    total_entry.insert(0, total_price)

    
    
def tableGUIwindow():
    global table_gui
    root.withdraw()
    table_gui=Toplevel()
    table_gui.title("Tour Management GUI")
    table_gui.resizable(0,0)
    table_gui.geometry("900x350")
    cursor.execute("SELECT * FROM `member` WHERE `username` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
    #print(cursor.fetchone())
    lbl_title = Label(table_gui, text = "Tour Management System", font=('arial', 10),justify='center')
    lbl_title.place(relx = 0.5, y=10, anchor = CENTER)
    email=cursor.fetchone()[3]
    EMAIL=email
    print(EMAIL)
    labl_text = Label(table_gui,text="current email: "+EMAIL)
    labl_text.grid(row=3, columnspan=2)
    # ================= Create a table================
    my_conn = conn.cursor()
    ####### end of connection ####
    my_conn.execute("SELECT tour_id, destination,unit_price,bus.bus_id,bus.veh_no,bus.capacity,bus.booked_seats  FROM tour INNER JOIN bus ON tour.bus_id = bus.bus_id")
   
    i=5
    header=['tour id','Destination','unit price','bus id','bus no','capacity','booked seats']
    for j in range(len(header)):
        e = Entry(table_gui, background="#94e5ff",justify='center')
        e.grid(row=i, column=j) 
        e.insert(END, header[j])
    i=i+1
    for row in my_conn: 
        for j in range(len(row)):
          
            e = Entry(table_gui, fg='blue',justify='center')
            e.grid(row=i, column=j) 
            e.insert(END, row[j])
            #e.configure(background="#808080")
            #e.configure(state='disabled')

        i=i+1

    b=Button(table_gui,text='Reserve Booking',command=bookUserWindow)
    b.grid(pady=5,row=i+3,column=1)
    b=Button(table_gui,text='Change Password',command=change_password_window)
    b.grid(pady=5,row=i+3,column=2)
    b=Button(table_gui,text='Change Email',command=change_email_window)
    b.grid(pady=5,row=i+3,column=3)
    b=Button(table_gui,text='Log Out',command=Logout)
    b.grid(pady=5,row=i+3,column=4)
    
def bookUserWindow():
    global userWindow
    root.withdraw()
    userWindow=Toplevel()
    userWindow.title("Select a Booking")
    width = 660
    height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.resizable(0, 0)
    userWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    #lbl_home = Label(userWindow, text="Enter booking details", font=('times new roman', 20)).pack()
    #==============================LABELS=========================================
    lbl_tour_id = Label(userWindow, text = "Tour Id:", font=('arial', 14), bd=15)
    lbl_tour_id.grid(row=0, sticky="e")
    lbl_bus_id = Label(userWindow, text = "Number of Adult(s)", font=('arial', 14), bd=15)
    lbl_bus_id.grid(row=1, sticky="e")
    lbl_bus_id = Label(userWindow, text = "Number of Children(s)", font=('arial', 14), bd=15)
    lbl_bus_id.grid(row=2, sticky="e")
    lbl_total_fare=Label(userWindow, text = "Total Fare", font=('arial', 14), bd=15)
    lbl_total_fare.grid(row=3, sticky="e")
    global lbl_text
    lbl_text = Label(userWindow)
    lbl_text.grid(row=7, columnspan=2)

    #==============================ENTRY WIDGETS==================================
    tour_id = Entry(userWindow, font=(10))
    tour_id.grid(row=0, column=1)
    no_adult = Entry(userWindow, font=(10))
    no_adult.grid(row=1, column=1)
    no_child = Entry(userWindow, font=(10))
    no_child.grid(row=2, column=1)
    global total_entry
    total_entry = Entry(userWindow, font=(10))
    total_entry.grid(row=3, column=1)
    total_button=Button(userWindow,width=30,text='Calculate Ticket',command=lambda: calculate_fare(tour_id.get(),no_adult.get(),no_child.get()))
    total_button.grid(pady=15,row=4, column=1)

    b=Button(userWindow,width=30,text='Confirm Booking',command=lambda: reserve_booking(tour_id.get(),no_adult.get(),no_child.get()))
    b.grid(pady=15,row=5, columnspan=2)
    b=Button(userWindow,width=30,text='back',command=BackUser)
    b.grid(pady=15,row=6, columnspan=2)
    

    
    

 
    #btn_back = Button(userWindow, text='Back', command=BackUser).pack(pady=20, fill=X)

def Logout():
    table_gui.destroy()
    Login_screen()
def change_password(cur_pswd,new_paswd):
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM `member` WHERE `username` = ?", (USERNAME.get(),))
    passwd=cursor.fetchone()[0]
    labl_text.configure(text="")
    if cur_pswd==passwd:
        cursor.execute("UPDATE `member` SET `password`=? WHERE `username`=?",(str(new_paswd),str(USERNAME.get())))
        conn.commit()
        cursor.close()
        PASSWORD.set(new_paswd)
        labl_text.configure(text="password has been changed ")
    else:
        labl_text.configure(text="current password did not match")
def change_email(cur_email):
    cursor = conn.cursor()
    labl_text.configure(text="")
    if(re.search(regex,cur_email)):
        cursor.execute("UPDATE `member` SET `email`=? WHERE `username`=?",(str(cur_email),str(USERNAME.get())))
        conn.commit()
        cursor.close()
        EMAIL=cur_email
        labl_text.configure(text="Your email has been changed ")
    else:
        labl_text.configure(text="Entered email is not valid please try again")
def change_email_window():
    global email_window
    email_window=Toplevel()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    email_window.geometry("700x325")
    frame = Frame(email_window, bd=2,  relief=RIDGE)
    frame.pack(side=TOP, fill=X)
    Form = Frame(email_window, height=200)
    Form.pack(side=TOP, pady=20)

    #==============================LABELS=========================================
    lbl_title = Label(email_window, text = "Change Email Window", font=('arial', 15))
    lbl_title.pack(fill=X)
    lbl_email = Label(Form, text = "New email:", font=('arial', 14), bd=15)
    lbl_email.grid(row=1, sticky="e")
    global labl_text
    labl_text = Label(Form)
    labl_text.grid(row=2, columnspan=2)

    #==============================ENTRY WIDGETS==================================
    
    em_ent = Entry(Form, font=(14))
    em_ent.grid(row=1, column=1)

    #==============================BUTTON WIDGETS=================================
    btn_em = Button(Form, text="Change Email", width=45, command= lambda: change_email(em_ent.get()))
    btn_em.grid(pady=15, row=3, columnspan=2)
    btn_em.bind('<Return>', change_email)
def change_password_window():
    global pswd_window
    pswd_window=Toplevel()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    pswd_window.geometry("700x325")
    frame = Frame(pswd_window, bd=2,  relief=RIDGE)
    frame.pack(side=TOP, fill=X)
    Form = Frame(pswd_window, height=200)
    Form.pack(side=TOP, pady=20)

    #==============================LABELS=========================================
    lbl_title = Label(pswd_window, text = "Change Password Window", font=('arial', 15))
    lbl_title.pack(fill=X)
    lbl_username = Label(Form, text = "Current Password:", font=('arial', 14), bd=15)
    lbl_username.grid(row=0, sticky="e")
    lbl_password = Label(Form, text = "New Password:", font=('arial', 14), bd=15)
    lbl_password.grid(row=1, sticky="e")
    global labl_text
    labl_text = Label(Form)
    labl_text.grid(row=2, columnspan=2)

    #==============================ENTRY WIDGETS==================================
    cur_pswd = Entry(Form, show="*", font=(14))
    cur_pswd.grid(row=0, column=1)
    password = Entry(Form, show="*", font=(14))
    password.grid(row=1, column=1)

    #==============================BUTTON WIDGETS=================================
    btn_login = Button(Form, text="Change Password", width=45, command= lambda: change_password(cur_pswd.get(),password.get()))
    btn_login.grid(pady=15, row=3, columnspan=2)
    btn_login.bind('<Return>', change_password)
    
    
def Login_db(event=None):
    #Database()
    if USERNAME.get() == "" or PASSWORD.get() == "":
        lbl_text.config(text="Please complete the required field!", fg="red")
    else:
        cursor = conn.cursor()
       
        cursor.execute("SELECT * FROM `member` WHERE `username` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            Top.destroy()
            
            tableGUIwindow()
            
            #USERNAME.set("")
            #PASSWORD.set("")
            #labl_text.config(text="")
        else:
            labl_text.config(text="Invalid username or password", fg="red")
            USERNAME.set("")
            PASSWORD.set("")   
    cursor.close()
    #conn.close()  
def Login_screen():
    #==============================FRAMES=========================================
    global Top
    Top=Toplevel()
    root.withdraw()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    Top.geometry("%dx%d+%d+%d" % (width, height, x, y))
    frame = Frame(Top, bd=2,  relief=RIDGE)
    frame.pack(side=TOP, fill=X)
    Form = Frame(Top, height=200)
    Form.pack(side=TOP, pady=20)

    #==============================LABELS=========================================
    lbl_title = Label(Top, text = "Python: Tour Management Login", font=('arial', 15))
    lbl_title.pack(fill=X)
    lbl_username = Label(Form, text = "Username:", font=('arial', 14), bd=15)
    lbl_username.grid(row=0, sticky="e")
    lbl_password = Label(Form, text = "Password:", font=('arial', 14), bd=15)
    lbl_password.grid(row=1, sticky="e")
    global labl_text
    labl_text = Label(Form)
    labl_text.grid(row=2, columnspan=2)

    #==============================ENTRY WIDGETS==================================
    username = Entry(Form, textvariable=USERNAME, font=(14))
    username.grid(row=0, column=1)
    password = Entry(Form, textvariable=PASSWORD, show="*", font=(14))
    password.grid(row=1, column=1)
    

    #==============================BUTTON WIDGETS=================================
    btn_login = Button(Form, text="Login", width=45, command=Login_db)
    btn_login.grid(pady=25, row=3, columnspan=2)
    btn_login.bind('<Return>', Login_db)
def BackUser():
    userWindow.destroy()
    table_gui.destroy()
    tableGUIwindow()
    
conn=Database()

dbctrl=DataBaseController(conn)
# Uncomment these lines if you have deleted the database file
# This will reset the database and after running these lines comment them again
 
'''
dbctrl.insert_bus('LXM-100',40)
dbctrl.insert_bus('BS-400',45)
dbctrl.insert_bus('LR-230',30)
dbctrl.insert_bus('FW-786',40)
dbctrl.insert_bus('JXR-567',45)
dbctrl.insert_bus('MN-432',30)
dbctrl.insert_tour(1,3,'MalamJabba',20)
dbctrl.insert_tour(1,2,'MalamJabba',20)
dbctrl.insert_tour(2,1,'Mobali Island',10)
dbctrl.insert_tour(3,2,'Lahore Tour',30)
dbctrl.insert_tour(4,5,'Taxila',5)
dbctrl.insert_tour(5,5,'Lake View',2)
dbctrl.insert_tour(5,4,'Lake View',2)
dbctrl.reserve_seat(3,3)
dbctrl.reserve_seat(23,1)
dbctrl.reserve_seat(45,2)
'''

    
from tkinter import *
root = Tk()
root.title("Python: Tour Management System")
width = 400
height = 280
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
#==============================VARIABLES======================================
USERNAME = StringVar()
PASSWORD = StringVar()
EMAIL=StringVar()
Login_screen()
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
#==============================INITIALIATION==================================
if __name__ == '__main__':
    root.mainloop()
    
    