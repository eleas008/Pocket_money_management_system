import sqlite3
import tkinter as tk
from tkinter import ttk
import datetime
from tkinter import messagebox

total=0
with sqlite3.connect('pocket_money_management.db') as connection:
    cursor=connection.cursor()
    cursor.execute('create table if not exists pocket_money (id integer primary key autoincrement, date timestamp, catagory text,amount real,description text,total real)')
    connection.commit()
    print("Table created successfully")

def load_total():
    global total
    with sqlite3.connect('pocket_money_management.db') as connection:
        cursor = connection.cursor()
        cursor.execute('select total from pocket_money order by id desc limit 1')
        row = cursor.fetchone()
        total = row[0] if row and row[0] is not None else 0
    update_total_label()
   
def add_data(date,catagory,amount,description):
    global total
    with sqlite3.connect('pocket_money_management.db') as connection:
        cursor=connection.cursor()
        cursor.execute('select total from pocket_money order by id desc limit 1')
        row=cursor.fetchone()
        total= row[0] if row and row[0] is not None else 0
    
        if catagory=='Income':
            total=total+float(amount)
        else:
            total=total-float(amount)
        cursor.execute('insert into pocket_money(date,catagory,amount,description,total) values(?,?,?,?,?)' ,(date,catagory,amount,description,total) )
        connection.commit()
    update_total_label()
    load_data()


def update_total_label():
    total_label.config(text=f"Total Amount: {total:.2f}")

def delete_data():
    global total
    selected_item=tree.focus()
    if selected_item:
        row_values = tree.item(selected_item)["values"]
        if row_values:
            row_id=row_values[0]
            amount = row_values[3] 
            catagory = row_values[2]
            with sqlite3.connect('pocket_money_management.db') as connection:
               cursor=connection.cursor()
               cursor.execute('delete from pocket_money where id=?',(row_id,))
               connection.commit()
            if catagory == 'Income':
                total -= float(amount)
            else:
                total += float(amount)
            tree.delete(selected_item)
            update_total_label()
            load_data()
    else:
        messagebox.showinfo('Warning','Please select a row to delete')

def load_data():
    for row in tree.get_children():
        tree.delete(row)
    with sqlite3.connect('pocket_money_management.db') as connection:
        cursor=connection.cursor()
        cursor.execute('select * from pocket_money')
        rows=cursor.fetchall()
        for row in rows:
            tree.insert('','end',values=row)

root=tk.Tk()
root.title('Pocket Money Management')
root.geometry('650x500')
root.config(bg="light blue") 
root.resizable(False, False)

label1=tk.Label(root,text='Amount',font=('Times New Roman',16),bg='light blue')
label1.grid(row=0,column=0,padx=10,pady=10)
amount=tk.Entry(root,font=('Times New Roman',16))
amount.grid(row=0,column=1,padx=10,pady=10)

label2=tk.Label(root,text='Catagory',font=('Times New Roman',16),bg='light blue')
label2.grid(row=1,column=0,padx=10,pady=10)
catagory=tk.StringVar()
catagory.set('Income')
catagory_dropdown=ttk.Combobox(root,textvariable=catagory,values=('Income','Expense'),font=('Times New Roman',16))
catagory_dropdown.grid(row=1,column=1,padx=10,pady=10)

label3=tk.Label(root,text='Description',font=('Times New Roman',16),bg='light blue')
label3.grid(row=2,column=0,padx=10,pady=10)
description=tk.Entry(root,font=('Times New Roman',16))
description.grid(row=2,column=1,padx=10,pady=10)

btn1=tk.Button(root,text='Add data',font=('Times New Roman',16),command=lambda: add_data(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),catagory.get(),float(amount.get()),description.get()),bg='blue',fg='white')
btn1.grid(row=3,column=0,padx=10,pady=10)

btn2=tk.Button(root,text='Delete data',font=('Times New Roman',16),command=delete_data,bg='red',fg='white')
btn2.grid(row=3,column=1,padx=10,pady=10)

total_label=tk.Label(root,text=f"Total Amount: {total:.2f}",font=('Times New Roman',16),bg='light blue')
total_label.grid(row=3,column=2,padx=10,pady=10)

columns=('ID','Date','Catagory','Amount','Description','Total')
tree=ttk.Treeview(root,columns=columns,show='headings')
for col in columns:
    tree.heading(col,text=col)
    tree.column(col,minwidth=0,width=100)
tree.grid(row=4,column=0,columnspan=6,padx=10,pady=10)

load_data()
load_total()
root.mainloop()




