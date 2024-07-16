import re
from tkinter import *
import math
import time
from tkinter import ttk
from datetime import date
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import openpyxl, xlrd, pathlib
import pandas as pd
import numpy as np
import sqlite3
import xlsxwriter
from pathlib import Path
import os
from db import *

data = Database(db='blessed.db')

count = 0
selected_rowid = 0

dx = Tk()

dx.geometry("1300x666+25+3")
dx.rowconfigure(0, weight=1)
dx.columnconfigure(0, weight=1)
dx.title("OMOBUWA BLESSED ADEOYE SOLUTION")

################################ICON ########################
icon = ImageTk.PhotoImage(file="img/78.png")
dx.iconphoto(False, icon)
dx.resizable(0, 0)

a = Frame(dx, bg='green')
b = Frame(dx, bg='cadetblue')
c = Frame(dx)
d = Frame(dx)
e = Frame(dx, bg='magenta')
login = Frame(dx)
bmi = Frame(dx)
admin = Frame(dx)
reg_User = Frame(dx, bg='white')

for frame in (a, b, c, d, e, login, bmi, admin, reg_User):
    frame.grid(row=0, column=0, sticky='nsew')


def show_me(frame):
    frame.tkraise()


# show_me(reg_User)

show_me(login)

# show_me(admin)


Admin_Username = StringVar()
Admin_Password = StringVar()


# ====================== ADMIN LOGIN
def AdminUser():
    adminuser = Admin_Username.get()
    adminpasscode = Admin_Password.get()

    if adminuser == "" or adminpasscode == "":
        messagebox.showerror("error", "Few Data is Missing \n Please complete the form ")

    else:
        conn = sqlite3.connect('blessed.db')

        c = conn.cursor()
        c.execute(""" CREATE TABLE IF NOT EXISTS AdminTable ( AdminUsername TEXT, AdminPassword TEXT)""")
        c.execute("SELECT * FROM AdminTable WHERE AdminUsername=? AND AdminPassword=?", (adminuser, adminpasscode))

        if c.fetchone() is not None:
            conn.commit()
            conn.close()
            m = f' WELCOME  {adminuser} '

            show_me(reg_User)
            messagebox.showinfo('success', m)

        else:
            messagebox.showerror('Error', 'Invalid Username or Password')


a_login = Frame(admin, width=400, height=550)

h_img1 = PhotoImage(file='img/78.png')
Label(a_login, image=h_img1).place(x=150, y=20)


def AU_on_enter(e):
    adminuser.delete(0, 'end')


def AU_on_leave(e):
    if adminuser.get() == '':
        adminuser.insert(0, 'Username')


adminuser = Entry(a_login, textvariable=Admin_Username, width=25, fg='blue', bg='white', border=0,
                  font=('Microsoft YaHei UI Light', 15, 'bold'))
adminuser.place(x=50, y=180)
adminuser.insert(0, 'Username')
adminuser.bind("<FocusIn>", AU_on_enter)
adminuser.bind("<FocusOut>", AU_on_leave)

U_frame = Frame(a_login, width=295, height=2, bg='gold')
U_frame.place(x=50, y=207)


def AP_on_enter(e):
    adminpasscode.delete(0, 'end')


def AP_on_leave(e):
    if adminpasscode.get() == '':
        adminpasscode.insert(0, 'Password')


adminpasscode = Entry(a_login, textvariable=Admin_Password, width=25, fg='blue', show='*', bg='#fff', border=0,
                      font=('Microsoft YaHei UI Light', 12, 'bold'))
adminpasscode.place(x=50, y=257)

adminpasscode.insert(0, 'Password')
adminpasscode.bind("<FocusIn>", AP_on_enter)
adminpasscode.bind("<FocusOut>", AP_on_leave)

Frame(a_login, width=295, height=2, bg='gold').place(x=50, y=280)

Button(a_login, command=AdminUser, activeforeground='green', activebackground='#fff', text='ADMIN LOGIN', bg='green',
       fg='white', font='Roboto 11 bold').place(x=150, y=300)

a_login.place(x=450, y=30)

h_img2 = PhotoImage(file='img/34.png')
Button(admin, command=lambda: show_me(login), image=h_img2).place(x=10, y=10)


# ================= GLOBAL FUNCTIONS

def deleteRow():
    global selected_rowid
    data.removeDx(selected_rowid)
    refreshData()
    messagebox.showinfo('SUCCESS', 'SUCCESSFULLY DELETED')
    clear()


def select_record(event):
    global selected_rowid
    selected = dx_tr.focus()
    val = dx_tr.item(selected, 'values')

    try:
        selected_rowid = val[0]
        Diagnosis.set(val[1])
        Code.set(val[2])
        male_less_than_1_yr.set(val[3])
        female_less_than_1_yr.set(val[4])
        male_1_14.set(val[5])
        female_1_14.set(val[6])
        male_15_44.set(val[7])
        female_15_44.set(val[8])
        male_45_64.set(val[9])
        female_45_64.set(val[10])
        male_65_above.set(val[11])
        female_65_above.set(val[12])
        male_total.set(val[13])
        female_total.set(val[14])
        Grand_total.set(val[15])

    except Exception as ep:
        pass


# ============================== REGISTERING USER BY ADMIN  Reg_User LABELS =======================

# FUNCTIONS FOR REGISTERING USERS DATABASE CRUD

con = sqlite3.connect('blessed.db')
cur = con.cursor()


def connection():
    cur.execute(
        "CREATE TABLE IF NOT EXISTS userTable(login_Id INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT, Password TEXT)"
    )
    con.commit()


def save_user():
    connection
    try:

        if loginId.get() == "" or uName.get() == "" or uPassword.get() == "":
            messagebox.showerror("ERROR", "All Field are Required", parent=reg_User)
        else:
            cur.execute(
                "SELECT * FROM userTable WHERE login_Id=?", (loginId.get(),)
            )
            row = cur.fetchone()
            if row is not None:
                messagebox.showerror("Error", "ID Already Exists, Try a Different one", parent=reg_User)
            else:
                cur.execute("INSERT INTO userTable (login_Id , Username, Password) VALUES (?,?,?)",
                            (
                                loginId.get(),
                                uName.get(),
                                uPassword.get()
                            )
                            )
                con.commit()
                messagebox.showinfo("SUCCESS", "USER CREATED SUCCESSFULLY", parent=reg_User)
                clear_user()
                show_user()

    except Exception as ex:
        messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=reg_User)
        clear_user()


def clear_user():
    loginId.set("")
    uName.set("")
    uPassword.set("")
    show_user()


def show_user():
    connection
    try:
        cur.execute(
            "SELECT * FROM userTable"
        )
        rows = cur.fetchall()
        reg_tree.delete(*reg_tree.get_children())
        for row in rows:
            reg_tree.insert('', END, values=row)

    except Exception as ex:
        messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=reg_User)


def get_user(ev):
    f = reg_tree.focus()
    content = (reg_tree.item(f))
    row = content["values"]

    loginId.set(row[0])
    uName.set(row[1])
    uPassword.set(row[2])


def update_user():
    connection
    try:
        if loginId.get() == "":
            messagebox.showerror("Error", "ID Number  Required", parent=reg_User)
        else:
            cur.execute("SELECT * FROM userTable WHERE login_Id=?", (loginId.get(),))
            row = cur.fetchone()
            if row == None:
                messagebox.showerror("Error", " Invalid ID Number", parent=reg_User)

            else:
                cur.execute(
                    "UPDATE userTable SET Username=?, Password=?  WHERE login_Id=?",
                    (
                        uName.get(),
                        uPassword.get(),
                        loginId.get()
                    )
                )
                con.commit()
                messagebox.showinfo("SUCCESS", "USER UPDATED SUCCESSFULLY")
                clear_user()
                show_user()

    except Exception as ex:

        messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=reg_User)


def delete_user():
    connection
    try:
        if loginId.get() == "":
            messagebox.showerror("Error", "ID Number is required", parent=reg_User)

        else:
            cur.execute(
                "SELECT * FROM userTable WHERE login_Id=?",
                (loginId.get(),)

            )
            row = cur.fetchone()
            if row is None:
                messagebox.showerror("Error", "Invalid ID Number", parent=reg_User)

            else:
                CosM = messagebox.askyesno("CONFIRM", "Do You want to Delete?", parent=reg_User)
                if CosM == True:
                    cur.execute(
                        "DELETE FROM userTable WHERE login_Id=?",
                        (loginId.get(),)
                    )
                    con.commit()
                    messagebox.showinfo("Delete", "USER SUCCESSFULLY DELETED", parent=reg_User)
                    clear_user()
                    show_user()
    except Exception as ex:
        messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=reg_User)


lbl_title = Label(reg_User, text='USER REGISTRATION FORM', width=75, font=' Arial 20 bold ', bg='#0f4d7d',
                  fg='white')
lbl_title.place(x=5, y=5)

frame1 = Frame(reg_User, width=450, height=300, bg='gold')

lbl_userNo = Label(frame1, width=15, text='ID No:', fg='#0f4d7d', font='Roboto 10 bold', bg='gold')
lbl_userNo.place(x=3, y=5)

lbl_userNo = Label(frame1, width=15, text='Username:', fg='#0f4d7d', font='Roboto 10 bold', bg='gold')
lbl_userNo.place(x=3, y=35)

lbl_userNo = Label(frame1, width=15, text='Password:', fg='#0f4d7d', font='Roboto 10 bold', bg='gold')
lbl_userNo.place(x=3, y=65)

loginId = StringVar()
uName = StringVar()
uPassword = StringVar()

# ============= Reg_User ENTRIES =================================

txt_id = Entry(frame1, textvariable=loginId, font='Roboto 12 bold', width=17).place(x=150, y=5)
txt_name = Entry(frame1, textvariable=uName,  font='Roboto 12 bold', width=17).place(x=150, y=35)
txt_pass = Entry(frame1, textvariable=uPassword,show='*', font='Roboto 12 bold', width=17).place(x=150, y=65)

# ============= Reg_User Buttons =================================

btn_add_user = Button(frame1, text="Add User", command=save_user, width=13, font='Roboto 12 bold',
                      activebackground='white',
                      activeforeground='#2196f3', bg='#2196f3', fg='white', cursor='hand2')
btn_add_user.place(x=120, y=97)

btn_update_user = Button(frame1, text="Update User", command=update_user, width=13, font='Roboto 12 bold',
                         activebackground='white',
                         activeforeground='#4caf50', bg='#4caf50', fg='white', cursor='hand2')
btn_update_user.place(x=290, y=97)

btn_delete_user = Button(frame1, text="Delete User", command=delete_user, font='Roboto 12 bold',
                         activebackground='white', width=13,
                         activeforeground='red', bg='red', fg='white', cursor='hand2')
btn_delete_user.place(x=200, y=140)

frame1.place(x=1, y=200)

# ======================== USERS  TREEVIEW FRAME START
frame2 = Frame(reg_User, bd=3, bg='magenta', relief=RIDGE)

h_img3 = PhotoImage(file='img/34.png')
Button(reg_User, command=lambda: show_me(login), bg='gold', image=h_img3).place(x=35, y=9)

# ===================== SCROLLBAR ============
scrolly = Scrollbar(frame2, orient=VERTICAL)
scrollx = Scrollbar(frame2, orient=HORIZONTAL)

# ================= CREATING TABLE VIEW
reg_tree = ttk.Treeview(frame2, columns=('loginId', "uName", "uPassword"), yscrollcommand=scrolly.set,
                        xscrollcommand=scrollx.set)
scrollx.pack(side=BOTTOM, fill=X)
scrolly.pack(side=RIGHT, fill=Y)
scrollx.config(command=reg_tree.xview)
scrolly.config(command=reg_tree.yview)

# ==================== TREE HEADING
# reg_tree.heading("oid", text="ROW ID", anchor=CENTER)
reg_tree.heading("loginId", text="ID", anchor=CENTER)
reg_tree.heading("uName", text="USERNAME", anchor=CENTER)
reg_tree.heading("uPassword", text="PASSWORD", anchor=CENTER)

# ===== tREE COLUMNS============
reg_tree["show"] = "headings"
# reg_tree.column("oid", width=100, anchor=CENTER)
reg_tree.column("loginId", width=100, anchor=CENTER)
reg_tree.column("uName", width=200, anchor=CENTER)
reg_tree.column("uPassword", width=200, anchor=CENTER)

reg_tree.pack(fill=BOTH, expand=1)

reg_tree.bind("<ButtonRelease-1>", get_user)

show_user()

frame2.place(x=480, y=100, width=750, height=500)

connection()


# ========================= USER LOGIN


def clock_update():
    hours = int(time.strftime("%I"))
    minutes = int(time.strftime("%M"))
    seconds = int(time.strftime("%S"))

    # Updating Second hand per second
    seconds_x = seconds_hand_len * math.sin(math.radians(seconds * 6)) + center_x
    seconds_y = -1 * seconds_hand_len * math.cos(math.radians(seconds * 6)) + center_y
    lf1.coords(seconds_hand, center_x, center_y, seconds_x, seconds_y)

    # Updating Minute hand per second
    minutes_x = minutes_hand_len * math.sin(math.radians(minutes * 6)) + center_x
    minutes_y = -1 * minutes_hand_len * math.cos(math.radians(minutes * 6)) + center_y
    lf1.coords(minutes_hand, center_x, center_y, minutes_x, minutes_y)

    # Updating Second hand per second
    hours_x = hours_hand_len * math.sin(math.radians(hours * 30)) + center_x
    hours_y = -1 * hours_hand_len * math.cos(math.radians(hours * 30)) + center_y
    lf1.coords(hours_hand, center_x, center_y, hours_x, hours_y)

    login.after(1000, clock_update)


# ######################################## LOGIN #############################################

# ======================== CLOCK FRAME =========================
lf1 = Canvas(login, width=490, height=575, bg='gold')
# lf1.pack(expand=True, fill='both')
lf1.place(x=50, y=5)
# =========== CREATING THE BACKGROUND =========================
lf1_bg = PhotoImage(file='img/ck.png')
lf1.create_image(250, 250, image=lf1_bg)

# ============= Creating Clock Hand =============
center_x = 250
center_y = 250
seconds_hand_len = 75
minutes_hand_len = 60
hours_hand_len = 45

# Drawing Clock Hand
# Second Hand
seconds_hand = lf1.create_line(200, 200, 200 + seconds_hand_len, 200 + seconds_hand_len, width=1.5, fill='red')

# Minutes Hand
minutes_hand = lf1.create_line(200, 200, 200 + minutes_hand_len, 200 + minutes_hand_len, width=2, fill='blue')

# Hours Hand
hours_hand = lf1.create_line(200, 200, 200 + hours_hand_len, 200 + hours_hand_len, width=2, fill='green')

clock_update()

# ================================= LOGIN FRAME =======================


# ==== Clear Login Form
lf2 = Frame(login, width=600, height=575)

# Label(lf2, text='Username')
# ======= LOGIN PAGE




# ============== SIGN IN
def Signin():
    user = Username.get()
    passcode = Password.get()

    if user == "" or passcode == "":
        messagebox.showerror("error", "Few Data is Missing \n Please complete the form ")

    else:
        conn = sqlite3.connect('blessed.db')

        c = conn.cursor()
        c.execute(""" CREATE TABLE IF NOT EXISTS userTable ( Username TEXT, Password TEXT)""")
        c.execute("SELECT * FROM userTable WHERE Username=? AND Password=?", (user, passcode))

        if c.fetchone() is not None:
            conn.commit()
            conn.close()
            m = f' WELCOME  {user} '
            show_me(a)
            messagebox.showinfo('success', m)
        else:
            messagebox.showerror('Error', 'Invalid Username or Password')


def U_on_enter(e):
    user.delete(0, 'end')


def U_on_leave(e):
    if user.get() == '':
        user.insert(0, 'Username')


Username = StringVar()
Password = StringVar()

user = Entry(lf2, textvariable=Username, width=25, fg='blue', bg='white', border=0,
             font=('Microsoft YaHei UI Light', 15, 'bold'))
user.place(x=150, y=180)
user.insert(0, 'Username')
user.bind("<FocusIn>", U_on_enter)
user.bind("<FocusOut>", U_on_leave)

U_frame = Frame(lf2, width=295, height=2, bg='gold')
U_frame.place(x=145, y=207)


def P_on_enter(e):
    passcode.delete(0, 'end')


def P_on_leave(e):
    if passcode.get() == '':
        passcode.insert(0, 'Password')


Button(lf2, command=lambda: show_me(admin), text='Password', bg='blue', fg='gold', font='Helvetica 13 bold').place(
    x=165, y=220)

passcode = Entry(lf2, textvariable=Password, width=25, fg='blue', show='*', bg='#fff', border=0,
                 font=('Microsoft YaHei UI Light', 12, 'bold'))
passcode.place(x=150, y=257)

passcode.insert(0, 'Password')
passcode.bind("<FocusIn>", P_on_enter)
passcode.bind("<FocusOut>", P_on_leave)

Frame(lf2, width=295, height=2, bg='gold').place(x=145, y=280)

h_img1 = PhotoImage(file='img/78.png')
Label(lf2, image=h_img1).place(x=200, y=40)

h_img = PhotoImage(file='img/hims.png')
Label(lf2, image=h_img).place(x=60, y=40)

uch = PhotoImage(file='img/uch.png')
Label(lf2, image=uch).place(x=340, y=40)

Button(lf2, text='Sign In', command=Signin, bg='blue', activebackground='yellow', activeforeground='blue', fg='gold',
       font='Roboto 12 bold').place(x=300, y=300)

lf2.place(x=550, y=5)

# ================== DISEASE PATTERN ============


Label(a, text="DISEASE PATTERN / MORBIDITY REPORT ", font="arial 20 bold", height=1, bg="white", fg='green').pack(
    side=TOP, fill=X)

logo = PhotoImage(file="img/34.png")
logomi = Button(a, bg="gold", image=logo, width=150, command=lambda: show_me(b))
logomi.place(x=7, y=5)

###############################################################
Date = IntVar()
today = date.today()
d1 = today.strftime("%d/%m/%Y")
date_entry = Label(a, textvariable=Date, bg='gold', fg='blue', font="arial 11 bold", width=10, bd=2)
date_entry.place(x=1000, y=5)

Date.set(d1)
############################################### DISEASE PATTERN LABEL ###############################################
Label(a, text="DIAGNOSIS", bg='green', fg='white', font="Roboto 15 bold ", width=15).place(x=20, y=70)
Label(a, text="CODE", bg='green', fg='white', font="Roboto 15 bold ", width=15).place(x=750, y=70)
Label(a, text="MALE", bg='green', fg='white', font="Roboto 20 bold").place(x=200, y=140)
Label(a, text="FEMALE", bg='green', fg='white', font="Roboto 20 bold").place(x=350, y=140)
Label(a, text="< 1 yr", bg='green', fg='white', font="Roboto 20 bold").place(x=100, y=170)
Label(a, text="1 - 14 ", bg='green', fg='white', font="Roboto 20 bold").place(x=100, y=220)
Label(a, text="15 - 44", bg='green', fg='white', font="Roboto 20 bold").place(x=100, y=270)
Label(a, text="45 - 64", bg='green', fg='white', font="Roboto 20 bold").place(x=100, y=320)
Label(a, text="65 + ", bg='green', fg='white', font="Roboto 20 bold").place(x=100, y=370)
Label(a, text="TOTAL", bg='green', fg='white', font="Roboto 20 bold").place(x=100, y=490)
Label(a, text="GRAND TOTAL", bg='green', fg='red', font="Roboto 20 bold").place(x=100, y=540)
Label(a, text="Table Name", bg='gold', fg='red', font="Roboto 20 bold").place(y=320, x=500)


########################################### DISEASE PATTERN FUNCTION #####################################################################


def calculate():
    global male_total
    global female_total
    a = male_less_than_1_yr.get()
    b = female_less_than_1_yr.get()
    c = male_1_14.get()
    d = female_1_14.get()
    e = male_15_44.get()
    f = female_15_44.get()
    g = male_45_64.get()
    h = female_45_64.get()
    i = male_65_above.get()
    j = female_65_above.get()

    total_male = int(a + c + e + g + i)
    total_female = int(b + d + f + h + j)
    g_t = int(total_male + total_female)
    male_total.set(int(total_male))
    female_total.set(int(total_female))
    Grand_total.set(int(g_t))


def clear():
    Diagnosis.set('')
    Code.set('')
    male_less_than_1_yr.set('')
    female_less_than_1_yr.set('')
    male_1_14.set('')
    female_1_14.set('')
    male_15_44.set('')
    female_15_44.set('')
    male_45_64.set('')
    female_45_64.set('')
    male_65_above.set('')
    female_65_above.set('')
    male_total.set('')
    female_total.set('')
    Grand_total.set('')



def exportToExcel():
    global selected_rowid
    dbs = ds.get()
    con = sqlite3.connect('blessed.db')
    cursor = con.execute(
        'SELECT Diagnosis, Code, male_less_than_1_yr, female_less_than_1_yr, male_1_14, female_1_14, male_15_44, female_15_44, male_45_64, female_45_64, male_65_above, female_65_above, male_total, female_total, Grand_total from disease'
    )
    all_data = cursor.fetchall()
    with pd.ExcelWriter(os.path.join(Path.home(), dbs + ".xlsx"), engine="xlsxwriter",
                        options={'strings_to_number': True, 'strings_to_formulas': False}) as writer:

        try:
            df = pd.read_sql(
                'SELECT Diagnosis, Code, male_less_than_1_yr, female_less_than_1_yr, male_1_14, female_1_14, male_15_44, female_15_44, male_45_64, female_45_64, male_65_above, female_65_above, male_total, female_total, Grand_total from disease',
                con
            )
            df.to_excel(writer, sheet_name='DISEASE PATTERN', header=True, index=False)
            messagebox.showinfo('SUCCESS', f'SUCCESSFULLY EXPORTED TO {dbs} ')
            ds.set('')

        except Exception as ep:
            messagebox.showerror('Error', ep)


def convert_text(*args):
    Diagnosis.set(str(Diagnosis.get().title()))
    Code.set(str(Code.get().title()))
    ds.set(str(ds.get().title()))


def saveDx():
    global data

    if Diagnosis.get() == "" or Diagnosis.get() == ' ' or Code.get() == "" or Code.get() == ' ' or male_less_than_1_yr.get() == "" or male_less_than_1_yr.get() == ' ' or female_less_than_1_yr.get() == "" or female_less_than_1_yr.get() == ' ' or male_1_14.get() == "" or male_1_14.get() == ' ' or female_1_14.get() == "" or female_1_14.get() == ' ' or male_15_44.get() == "" or male_15_44.get() == ' ' or female_15_44.get() == "" or female_15_44.get() == ' ' or male_45_64.get() == "" or male_45_64.get() == ' ' or female_45_64.get() == "" or female_45_64.get() == ' ' or male_65_above.get() == "" or male_65_above.get() == ' ' or female_65_above.get() == "" or female_65_above.get() == ' ':
        messagebox.showerror('error', 'ALL field required')



    else:
        data.c.execute('SELECT * FROM disease WHERE Diagnosis="{}"'.format(dxs))
        if data.c.fetchone() is None:
            calculate()
            data.insertDx(dxs=Diagnosis.get(),
                          code=Code.get(),
                          m_l_1=male_less_than_1_yr.get(),
                          fm_l_1=female_less_than_1_yr.get(),
                          m_1_14=male_1_14.get(),
                          fm_1_14=female_1_14.get(),
                          m_15_44=male_15_44.get(),
                          fm_15_44=female_15_44.get(),
                          m_45_64=male_45_64.get(),
                          fm_45_64=female_45_64.get(),
                          m_65_above=male_65_above.get(),
                          fm_65_above=female_65_above.get(),
                          m_t=male_total.get(),
                          f_t=female_total.get(),
                          t_grand=Grand_total.get())
            m = '  SUCCESSFULLY ADDED to DATABASE\n FORTUNE 2024'
            messagebox.showinfo('success', m)

            # view_dx()
            get_dx()
            clear()
        else:
            messagebox.showerror('Error', 'This Diagnosis exists in the Database')


def fetch_records():
    global count
    f = data.fetchRecord("SELECT rowid, * FROM disease ")

    for rec in f:
        dx_tr.insert(parent='', index='end',
                     iid=count, values=(
                rec[0], rec[1], rec[2], rec[3], rec[4], rec[5],
                rec[6], rec[7], rec[8], rec[9], rec[10], rec[11],
                rec[12], rec[13], rec[14], rec[15]
            )
                     )

        count += 1

    dx_tr.after(400, refreshData)


def refreshData():
    for x in dx_tr.get_children():
        dx_tr.delete(x)
    fetch_records()


def edit_dx():
    global selected_rowid
    con = sqlite3.connect('blessed.db')

    c = con.cursor()
    calculate()
    c.execute("""
                UPDATE disease SET
                Diagnosis = :dxs,
                Code = :code,
                male_less_than_1_yr = :m_l_1,
                female_less_than_1_yr = :fm_l_1,
                male_1_14 = :m_1_14,
                female_1_14 = :fm_1_14,
                male_15_44 = :m_15_44,
                female_15_44 = :fm_15_44 ,
                male_45_64 = :m_45_64,
                female_45_64 = :fm_45_64,
                male_65_above = :m_65_above,
                female_65_above = :fm_65_above,
                male_total = :m_t,
                female_total = :f_t,
                Grand_total = :t_grand
                
                WHERE oid = :oid """,

              {
                  'dxs': Diagnosis.get(),
                  'code': Code.get(),
                  'm_l_1': male_less_than_1_yr.get(),
                  'fm_l_1': female_less_than_1_yr.get(),
                  'm_1_14': male_1_14.get(),
                  'fm_1_14': female_1_14.get(),
                  'm_15_44': male_15_44.get(),
                  'fm_15_44': female_15_44.get(),
                  'm_45_64': male_45_64.get(),
                  'fm_45_64': female_45_64.get(),
                  'm_65_above': male_65_above.get(),
                  'fm_65_above': female_65_above.get(),
                  'm_t': male_total.get(),
                  'f_t': female_total.get(),
                  't_grand': Grand_total.get(),
                  'oid': selected_rowid

              }
              )

    con.commit()
    con.close()
    messagebox.showinfo('SUCCESS', 'SUCCESSFULLY UPDATED\n FORTUNE 2024')
    clear()
    dx_tr.after(400, refreshData)


def droptable():
    try:
        CosM = messagebox.askyesno("CONFIRM", "Do You want to DROP DATABASE TABLE ?", parent=a)
        if CosM == True:
            data.bhuwah()
            messagebox.showinfo('Success', 'DATABASE TABLE SUCCESSFULLY DROPPED ')
    except Exception as e:
        messagebox.showerror('Error', e)


############################################### DISEASE PATTERN ENTRY ###############################################

Diagnosis = StringVar()
Code = StringVar()
male_less_than_1_yr = IntVar()
female_less_than_1_yr = IntVar()
male_1_14 = IntVar()
female_1_14 = IntVar()
male_15_44 = IntVar()
female_15_44 = IntVar()
male_45_64 = IntVar()
female_45_64 = IntVar()
male_65_above = IntVar()
female_65_above = IntVar()
male_total = IntVar()
female_total = IntVar()
Grand_total = IntVar()

dx_list = [
    'Cholera',
    'Typhoid',
    'paratyphoid fevers',
    'Shigellosis',
    'Amoebiasis',
    'Diarrhoea',
    'gastroenteritis',
    'Other intestinal infectious diseases',
    'Respiratory tuberculosis',
    'Other tuberculosis',
    'Plague',
    'Brucellosis',
    'Leprosy',
    'Tetanus neonatorum',
    'Other tetanus',
    'Diphtheria',
    'Whooping cough',
    'Meningococcal infection',
    'Septicaemia',
    'Other bacterial diseases',
    'Congenital syphilis',
    'Early syphilis',
    'Other syphilis',
    'Gonococcal infection',
    'Sexually transmitted chlamydial diseases',
    'Other infections with a predominantly sexual mode of transmission',
    'Relapsing fever',
    'Trachoma',
    'Typhus fever',
    'Acute poliomyelitis',
    'Rabies',
    'Viral encephalitis',
    'Yellow fever',
    'Other arthropod-borne viral fevers and viral haemorrhage fevers',
    'Herpes-viral infection',
    'Varicella and zoster',
    'Measles',
    'Rubella',
    'Acute hepatitis B',
    'Other viral diseases',
    'Human immunodeficiency virus [HIV] diseases',
    'Mumps',
    'Other viral diseases',
    'Mycoses',
    'Malaria',
    'Leishmaniasis',
    'Trypanosomiasis',
    'Schistosomiasis',
    'Other fluke infections',
    'Echinococcosis',
    'Dracunculiasis',
    'Onchocerciasis',
    'Filariasis',
    'Hookworm diseases',
    'Other helminthiases',
    'Sequelae of tuberculosis',
    'Sequelae of poliomyelitis',
    'Sequelae of leprosy',
    'Other infectious and parasitic diseases',
    'Malignant neoplasm of lip, oral cavity and pharynx',
    'Malignant neoplasm of oesophagus',
    'Malignant neoplasm of stomach',
    'Malignant neoplasm of colon',
    'Malignant neoplasm of rectosigmoid junction, rectum, anus and anal canal',
    'Malignant neoplasm of liver and intrahepatic bile duct',
    'Malignant neoplasm of pancreas',
    'Other malignant neoplasm of digestive organs',
    'Malignant neoplasm of larynx',
    'Malignant neoplasm of trachea, bronchus and lungs',
    'Other malignant neoplasm of respiratory and intrathoracic organs',
    'Malignant neoplasm of bone and articular cartilage',
    ' Malignant melanoma of skin',
    'Other malignant neoplasm of skin',
    'Malignant neoplasm of mesothelial and soft tissue',
    'Malignant neoplasm of breast',
    'Malignant neoplasm of cervix uteri',
    'Malignant neoplasm of other and unspecified parts of uterus',
    'Other malignant neoplasm of female genital organs',
    'Malignant neoplasm of prostate',
    'Other malignant neoplasm of male genital organs',
    'Malignant neoplasm of bladder',
    'Other malignant neoplasm of  urinary tract',
    'Malignant neoplasm of eye and adnexa',
    'Malignant neoplasm of brain',
    'Malignant neoplasm of other parts of the central nervous system',
    'Malignant neoplasm of other, ill-defined, secondary, unspecified and multiple sites',
    'Hodgkin’s diseases',
    'Non-Hodgkin’s lymphoma',
    'Leukaemia',
    'Other malignant neoplasm of lymphoid, haematopoietic and related tissue',
    'Carcinoma in situ of cervix uteri',
    'Benign neoplasm of skin',
    'Benign neoplasm of breast',
    'Leiomyoma of uterus',
    'Benign neoplasm of uterus',
    'Benign neoplasm of urinary organs',
    'Benign neoplasm of brain and other parts of central nervous system',
    'Other in situ and benign neoplasm and neoplasm of uncertain and unknown behaviour',
    'Iron deficiency anaemia',
    'Other anaemias',
    'Haemorrhagic conditions and other diseases of blood and blood forming organs',
    'Certain disorders involving the immune mechanism',
    'Iodine-deficiency-related thyroid disorders',
    'Thyrotoxicosis',
    'Other disorders of thyroid',
    'Diabetes mellitus',
    'Malnutrition',
    'Vitamin A deficiency',
    'Other vitamin deficiencies',
    'Sequelae of malnutrition and other nutritional deficiencies',
    'Obesity',
    'Other disorders of pancreatic Internal Secretion',
    'Volume depletion',
    'Other endocrine, nutritional and metabolic disorders',
    'Dementia',
    'Mental and behavioural disorders due to use of alcohol',
    'Mental and behavioural disorder due to use of alcohol',
    'Schizophrenia, schizotypal, and delusional disorders',
    'Mood [affective] disorders',
    'Neurotic, stress-related, and somatoform disorders',
    'Mental retardation',
    'Other mental and behavioural disorders',
    'Inflammatory diseases of the central nervous system',
    'Parkinson’s diseases',
    'Alzheimer’s diseases',
    'Multiple sclerosis',
    'Epilepsy',
    'Migraine and other headache syndromes',
    'Transient cerebral ischaemic attacks and related syndromes',
    'Nerve, nerve root and plexus disorders',
    'Cerebral palsy and other paralytic syndromes',
    'Other diseases of the nervous system',
    'Inflammation of eyelid',
    'Conjunctivitis and other disorders of conjunctiva',
    'Keratitis and other disorders of sclera and cornea',
    'Cataract and other disorder of lens',
    'Retinal detachments and breaks',
    'Glaucoma',
    'Strabismus',
    'Disorders of refraction and accommodation',
    'Blindness and low vision',
    'Other diseases of eye and adnexa',
    'Otitis media end other disorders of middle ear and mastoid',
    'Hearing loss',
    'Other diseases of the ear and mastoid tissue',
    'Acute rheumatic fever',
    'Chronic rheumatic heart diseases',
    'Essential (primary) hypertension',
    'Other hypertensive diseases',
    'Acute myocardial infraction',
    'Other ischaemic heart diseases',
    'Pulmonary embolism',
    'Conduction disorders and cardiac arrhythmias',
    'Heart failure',
    'Other heart diseases',
    'Intracranial haemorrhage',
    'Cerebral infraction',
    'Stroke, not specified as haemorrhage or infraction',
    'Other cerebrovascular diseases',
    'Atherosclerosis',
    'Other peripheral vascular diseases',
    'Arterial embolism and thrombosis',
    'Other diseases of artery, arterioles and capillaries',
    'Phlebitis, thrombophlebitis, venous embolism and thrombosis',
    'Varicose veins of lower extremities',
    'Haemorrhoids',
    'Other diseases of circulatory system',
    'Acute pharyngitis and acute tonsillitis',
    'Acute laryngitis and tracheitis',
    'Other acute upper respiration infections',
    'Influenza',
    'Pneumonia',
    'Acute bronchitis and acute bronchiolitis',
    'Chronic sinusitis',
    'Other diseases of nose and nasal sinuses',
    'Chronic diseases of tonsils and adenoids',
    'Other diseases of upper respiratory tract',
    'Bronchitis, emphysema and other chronic obstructive pulmonary diseases',
    'Asthma',
    'Bronchiectasis',
    'Pueumoconiosis',
    'Other diseases of the respiratory system',
    'Dental caries',
    'Other disorders of teeth and supporting structures',
    'Other diseases of oral cavity, salivary gland and jaws',
    'Gastric and duodenal ulcer',
    'Gastrititis and duodenitis',
    'Other diseases of the oesophagus, stomach and duodenum',
    'Diseases of appendix',
    'Inguinal hernia',
    'Other hernia',
    'Crohn’s disease and ulcerative colitis',
    'Paralytic ileus and intestinal obstruction without hernia',
    'Diverticular disease of intestine',
    'Other disease if intestine and peritoneum',
    'Alcoholic liver diseases',
    'Other diseases of liver',
    'Cholelithiasis and cholecystitis',
    'Acute pancreatitis and other diseases of the pancreas',
    'Other disease of the digestive system',
    'Infections of the skin and subcutaneous tissue',
    'Other diseases of the skin and subcutaneous',
    'Rheumatoid arthritis and other inflammatory  polyarthropathies',
    'Arthrosis',
    'Acquired deformities of limbs',
    'Other disorders of joints',
    'Systemic connective tissue disorders',
    'Cervical and other intervertebral disc disorders',
    'Other dorsophathies',
    'Soft tissues disorders',
    'Disorder of bone density and structure',
    'Osteomyelitis',
    'Other diseases of the musculoskeletal system and connective tissue',
    'Acute and rapidly progressive nephritic syndromes',
    'Other glomerular disease',
    'Renal tubule-interstitial diseases',
    'Renal failure',
    'Urolithiasis',
    'Cystitis',
    'Other diseases of the urinary system',
    'Hyperplasia of prostate',
    'Other disorders of prostate',
    'Hydrocele and spermatocele',
    'Redundant prepuce, phimosis and paraphimosis',
    'Other diseases of the male genital organs',
    'Disorders of the breast',
    'Salpingitis and oophoritis',
    'Inflammatory disease of cervix uteri',
    'Other inflammatory diseases of female pelvic organs',
    'Endometriosis',
    'Female genital prolapsed',
    'Non inflammatory disorders of the ovary, fallopian tube and broad ligament',
    'Disorders of menstruation',
    'Menopausal and other perimenopausal disorders',
    'Female infertility',
    'Other disorders of genitourinary tract',
    'Spontaneous abortion',
    'Medical abortion',
    'Other pregnancies with abortive outcome',
    'Oedema, proteinuria and hypertensive disorders in pregnancy, childbirth and the puerperium',
    'Placenta praevia, premature separation of placenta and antepartum haemorrhage',
    'Other maternal care related to foetus and amniotic cavity and possible delivery problems',
    'Obstructed labour',
    'Postpartum haemorrhage',
    'Other complications of pregnancy and delivery',
    'Single spontaneous delivery',
    'Complications predominantly related to the puerperium and other obstetric conditions, not elsewhere classified',
    'Foetus and new-born affected by maternal factors and by complications of pregnancy, labour and delivery',
    'Slow foetal growth, foetal malnutrition and disorders related to short gestation and low birth weight',
    'Birth trauma',
    'Intrauterine hypoxia and birth asphyxia',
    'Other respiratory disorders originating in the perinatal period',
    'Congenital infectious and parasitical diseases',
    'Other infections specific to the perinatal period',
    'Haemolytic disease of foetus and new-born',
    'Other conditions originating in the perinatal period',
    'Spina bifida',
    'Other congenital malformations of the nervous system',
    'Congenital malformations of the circulatory system',
    'Cleft lip and cleft palate',
    'Absence, atresia and stenosis of small intestine',
    'Other congenital malformations of digestive system',
    'Undescended testicle',
    'Other malformations of the genitourinary system',
    'Congenital deformities of hip',
    'Congenital deformities of feet',
    'Other congenital malformations and deformations of the musculoskeletal system',
    'Other congenital malformation',
    'Chromosomal abnormalities, not elsewhere classified',
    'Abdominal and pelvic pain',
    'Fever of unknown origin',
    'Senility',
    'Other symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified',
    'Fracture of skull and facial bones',
    'Fracture of neck, thorax or pelvis',
    'Fracture of femur',
    'Fractures of other limb bones',
    'Fractures involving multiple body regions',
    'Dislocations, sprains, strains of specified and multiple body regions',
    'Injury of the eye and orbit',
    'Intracranial injury',
    'Injury of other internal organs',
    'Crushing injuries and traumatic amputations of specified and multiple body regions',
    'Other injuries of specifies, unspecified and multiple body regions',
    'Effects of foreign body entering through natural orifice',
    'Burns and corrosions',
    'Poisoning by drugs and biological substances',
    'Toxic effects of substances chiefly nonmedical as to source',
    'Maltreatment syndrome',
    'Other and unspecified effects of external courses',
    'Certain early complications of trauma and complications of surgical and medical care, not elsewhere classified',
    'Sequelae of injuries, poisoning and of other consequences of external causes',
    'Transport Accident',
    'Falls',
    'Exposure to in animate mechanical forces',
    'Assault',
    'All other external causes',
    'Person encountering health services for examination and investigation',
    'Asymptomatic human immunodeficiency virus [HIV] infection status',
    'Other persons with potential health hazards related to communicable disease',
    'Contraceptive management',
    'Antenatal screening and other supervision of pregnancy',
    'Live-born infants according to place of birth',
    'Postpartum care and examination',
    'Persons encountering health services for specific procedures and healthcare',
    'Persons encountering health services for other reasons',
    'SARS'
]


def my_dx_up(my_widget):
    a = my_widget.widget
    index = int(a.curselection()[0])
    value = a.get(index)
    Diagnosis.set(value)
    l1.delete(0, END)


dxs = Entry(a, textvariable=Diagnosis, bg='white', fg='green', font="Roboto 15 bold", width=50)
dxs.place(x=185, y=70)

Diagnosis.trace('w', convert_text)

l1 = Listbox(a, bg='green', justify=CENTER, font='Roboto 12 bold', height=2, fg='white', highlightcolor='green',
             width=100,
             relief='flat')
l1.place(x=25, y=100)

l1.bind("<<ListboxSelect>>", my_dx_up)


def get_dx(*args):
    search_dx = dxs.get()
    l1.delete(0, END)
    for x in dx_list:
        # if (re.search(search_str, x, re.IGNORECASE)):
        if re.match(search_dx, x, re.IGNORECASE):
            l1.insert(END, x)


Diagnosis.trace('w', get_dx)

code = Entry(a, textvariable=Code, bg='white', fg='green', font="Roboto 15 bold", width=7)
code.place(x=890, y=70)

Code.trace('w', convert_text)

m_l_1 = Entry(a, textvariable=male_less_than_1_yr, bg='white', fg='green', font="Roboto 15 bold", width=7)
m_l_1.place(x=200, y=170)
fm_l_1 = Entry(a, textvariable=female_less_than_1_yr, bg='white', fg='green', font="Roboto 15 bold", width=9)
fm_l_1.place(x=350, y=170)

m_1_14 = Entry(a, textvariable=male_1_14, bg='white', fg='green', font="Roboto 15 bold", width=7)
m_1_14.place(x=200, y=220)

fm_1_14 = Entry(a, textvariable=female_1_14, bg='white', fg='green', font="Roboto 15 bold", width=9)
fm_1_14.place(x=350, y=220)

m_15_44 = Entry(a, textvariable=male_15_44, bg='white', fg='green', font="Roboto 15 bold", width=7)
m_15_44.place(x=200, y=270)

fm_15_44 = Entry(a, textvariable=female_15_44, bg='white', fg='green', font="Roboto 15 bold", width=9)
fm_15_44.place(x=350, y=270)

m_45_64 = Entry(a, textvariable=male_45_64, bg='white', fg='green', font="Roboto 15 bold", width=7)
m_45_64.place(x=200, y=320)

fm_45_64 = Entry(a, textvariable=female_45_64, bg='white', fg='green', font="Roboto 15 bold", width=9)
fm_45_64.place(x=350, y=320)

m_65_above = Entry(a, textvariable=male_65_above, bg='white', fg='green', font="Roboto 15 bold", width=7)
m_65_above.place(x=200, y=370)

fm_65_above = Entry(a, textvariable=female_65_above, bg='white', fg='green', font="Roboto 15 bold", width=9)
fm_65_above.place(x=350, y=370)

m_t = Entry(a, textvariable=male_total, bg='white', fg='green', font="Roboto 15 bold", width=7)
m_t.place(x=200, y=490)

f_t = Entry(a, textvariable=female_total, bg='white', fg='green', font="Roboto 15 bold", width=9)
f_t.place(x=350, y=490)

g_total = Entry(a, textvariable=Grand_total, bg='red', fg='white', font="Roboto 15 bold", width=15)
g_total.place(x=350, y=540)

ds = StringVar()
dbs = Entry(a, textvariable=ds, bg='white', fg='green', font="Roboto 20 bold", width=15)
dbs.place(y=320, x=680)

ds.trace('w', convert_text)

############################################### DISEASE PATTERN BUTTONS #####################################################

l = PhotoImage(file="img/78.png")
log = Label(a, bg='green', image=l, width=150)
log.place(x=1000, y=38)

# r = Signin.Username

# Label(a, bg='green',text=r, font='Roboto 10 bold', fg='white').place(y=38, x=1100)

cal_btn = Button(a, text="CALCULATE", command=calculate, width=19, font="arial 15 bold", fg="gold", bg="red")
cal_btn.place(x=200, y=410)

save_btn = Button(a, command=saveDx, text="SAVE", width=19, font="arial 12 bold", fg="white", bg="blue")
save_btn.place(x=10, y=600)

update_btn = Button(a, command=edit_dx, text="UPDATE", width=19, font="arial 12 bold", bg="gold", fg="blue")
update_btn.place(x=950, y=600)

del_btn = Button(a, command=deleteRow, text="DELETE", width=19, font="arial 12 bold", bg="cadetblue", fg="red")
del_btn.place(x=500, y=600)

exit_btn = Button(a, text="LOGOUT", width=19, command=lambda: show_me(login), font="arial 12 bold", bg="magenta",
                  fg="white")
exit_btn.place(x=720, y=600)

clear_btn = Button(a, text="REFRESH DATA", command=clear, width=19, font="arial 12 bold", bg="#215846",
                   fg="white")
clear_btn.place(x=250, y=600)

export = Button(a, command=exportToExcel, text='EXPORT TABLE TO EXCEL', bg='yellow', fg='blue',
                activebackground='blue', activeforeground='yellow',
                font='Roboto 17 bold')
export.place(y=315, x=930)

dp = Button(a, command=droptable, text='DROP DATABASE TABLE', bg='red', fg='white',
            activebackground='white', activeforeground='red',
            font='Roboto  15 bold')
dp.place(y=370, x=730)

# ============================ DISEASE PATTERN TREEVIEW
Dx_tr_frame = Frame(a, bd=3, relief=RIDGE)

Dx_tr_frame.place(x=480, y=155, width=800, height=150)

# ==================== Dx_tr_frame SCROLLBAR

dx_scrolly = Scrollbar(Dx_tr_frame, orient=VERTICAL)
dx_scrollx = Scrollbar(Dx_tr_frame, orient=HORIZONTAL)

# ================== CREATING Dx_tr_frame TABLEVIEW=========================
dx_tr = ttk.Treeview(Dx_tr_frame, columns=('oid', 'Diagnosis', 'Code', 'male_less_than_1_yr',
                                           'female_less_than_1_yr', 'male_1_14', 'female_1_14',
                                           'male_15_44', 'female_15_44', 'male_45_64', 'female_45_64',
                                           'male_65_above', 'female_65_above', 'male_total', 'female_total',
                                           'Grand_total'),
                     yscrollcommand=dx_scrolly.set, xscrollcommand=dx_scrollx.set
                     )
dx_scrollx.pack(side=BOTTOM, fill=X)
dx_scrolly.pack(side=RIGHT, fill=Y)
dx_scrollx.config(command=dx_tr.xview)
dx_scrolly.config(command=dx_tr.yview)

dx_tr.heading('oid', text='RowID', anchor=CENTER)
dx_tr.heading('Diagnosis', text='DIAGNOSIS', anchor=CENTER)
dx_tr.heading('Code', text='ICD NO', anchor=CENTER)
dx_tr.heading('male_less_than_1_yr', text='M < 1', anchor=CENTER)
dx_tr.heading('female_less_than_1_yr', text='F < 1', anchor=CENTER)
dx_tr.heading('male_1_14', text='M 1-14', anchor=CENTER)
dx_tr.heading('female_1_14', text='F 1-14', anchor=CENTER)
dx_tr.heading('male_15_44', text='M 15-44', anchor=CENTER)
dx_tr.heading('female_15_44', text='F 15-44', anchor=CENTER)
dx_tr.heading('male_45_64', text='M 45-64', anchor=CENTER)
dx_tr.heading('female_45_64', text='F 45-64', anchor=CENTER)
dx_tr.heading('male_65_above', text='M > 65', anchor=CENTER)
dx_tr.heading('female_65_above', text='F > 65', anchor=CENTER)
dx_tr.heading('male_total', text='M TOTAL', anchor=CENTER)
dx_tr.heading('female_total', text='F TOTAL', anchor=CENTER)
dx_tr.heading('Grand_total', text='GRAND TOTAL', anchor=CENTER)

dx_tr["show"] = "headings"
dx_tr.column("oid", width=50, anchor=CENTER)
dx_tr.column("Diagnosis", width=300, anchor=CENTER)
dx_tr.column("Code", width=50, anchor=CENTER)
dx_tr.column("male_less_than_1_yr", width=50, anchor=CENTER)
dx_tr.column("female_less_than_1_yr", width=50, anchor=CENTER)
dx_tr.column("male_1_14", width=50, anchor=CENTER)
dx_tr.column("female_1_14", width=50, anchor=CENTER)
dx_tr.column("male_15_44", width=50, anchor=CENTER)
dx_tr.column("female_15_44", width=50, anchor=CENTER)
dx_tr.column("male_45_64", width=50, anchor=CENTER)
dx_tr.column("female_45_64", width=50, anchor=CENTER)
dx_tr.column("male_65_above", width=50, anchor=CENTER)
dx_tr.column("female_65_above", width=50, anchor=CENTER)
dx_tr.column("male_total", width=50, anchor=CENTER)
dx_tr.column("female_total", width=50, anchor=CENTER)
dx_tr.column("Grand_total", width=100, anchor=CENTER)

dx_tr.pack(fill=BOTH, expand=1)  # to make the Treeview show

#
dx_tr.bind("<ButtonRelease-1>", select_record)
#
# # STYLING 4 TREEVIEW

style = ttk.Style()
style.theme_use("default")
style.map("Treeview")

fetch_records()

dx.mainloop()
