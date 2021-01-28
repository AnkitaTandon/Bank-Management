import tkinter as tk
from tkinter import messagebox
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Ankita@227",
  database="bank",
  buffered=True
)

mycursor = mydb.cursor()

def is_number(s):
    try:
        float(s)
        return 1
    except ValueError:
        return 0

def check_acc_nmb(num):
	try:
		sql_desc="desc "+num
		mycursor.execute(sql_desc)
	except:
		messagebox.showinfo("Account number error","Invalid Credentials!\nTry Again!")
		return 0
	return 

def home_return(master):
	master.destroy()
	Main_Menu()

def write(master,name,oc,pin):
	
	if( (is_number(name)) or (is_number(oc)==0) or (is_number(pin)==0)or name==""):
		messagebox.showinfo("Error","Invalid Credentials\nPlease try again.")
		master.destroy()
		return 

	sql_acc="select max(acc_no) from accounts"
	mycursor.execute(sql_acc)
	accnt_no = mycursor.fetchall()[0][0]+1

	sql_ins="insert into accounts values (%s)"
	val=(accnt_no,)
	mycursor.execute(sql_ins,val)
	
	accnt_no="D"+str(accnt_no)
	sql_create="create table "+ accnt_no + " (pin int primary key, oc int, name varchar(20))"
	mycursor.execute(sql_create)


	sql_ins="insert into " + accnt_no +" values (%s,%s,%s)"
	val=(pin,oc,name)
	mycursor.execute(sql_ins,val)

	sql_create="create table " + accnt_no +"rec (Date_Time datetime, credit int, debit int, balance int)"
	mycursor.execute(sql_create)

	sql_ins="insert into " + accnt_no +"rec values (sysdate(),%s,%s,%s)"
	val=(oc ,0, oc)
	mycursor.execute(sql_ins,val)
	mydb.commit()
	messagebox.showinfo("Details","Your Account Number is:" + accnt_no)
	master.destroy()
	return

def crdt_write(master,amt,accnt,name):

	if(is_number(amt)==0):
		messagebox.showinfo("Error","Invalid Credentials\nPlease try again.")
		master.destroy()
		return 

	sql_sel="select pin from "+accnt
	mycursor.execute(sql_sel)
	pin= mycursor.fetchall()[0][0]

	sql_sel="select oc from "+accnt
	mycursor.execute(sql_sel)
	camt= mycursor.fetchall()[0][0]

	amt=int(amt)
	cb=amt+camt

	sql_del ="delete from "+accnt
	mycursor.execute(sql_del)

	sql_ins="insert into "+accnt+" values (%s,%s,%s)"
	val=(pin,cb,name)
	mycursor.execute(sql_ins,val)

	sql_ins="insert into "+accnt+"rec values (sysdate(),%s,%s,%s)"
	val=(amt,0,cb)
	mycursor.execute(sql_ins,val)
	mydb.commit()
	messagebox.showinfo("Operation Successfull!!","Amount Credited Successfully!!")
	master.destroy()
	return

def debit_write(master,amt,accnt,name):

	if(is_number(amt)==0):
		messagebox.showinfo("Error","Invalid Credentials\nPlease try again.")
		master.destroy()
		return 
			
	sql_sel="select pin from "+accnt
	mycursor.execute(sql_sel)
	pin= mycursor.fetchall()[0][0]

	sql_sel="select oc from "+accnt
	mycursor.execute(sql_sel)
	camt= mycursor.fetchall()[0][0]

	if(int(amt)>camt):
		messagebox.showinfo("Error!!","You dont have that amount left in your account\nPlease try again.")
	else:
		amt=int(amt)
		cb=camt-amt
		
		sql_del ="delete from "+accnt
		mycursor.execute(sql_del)

		sql_ins="insert into "+accnt+ " values (%s,%s,%s)"
		val=(pin,cb,name)
		mycursor.execute(sql_ins,val)

		sql_ins="insert into "+accnt+ "rec values (sysdate(),%s,%s,%s)"
		val=(0, amt, cb)
		mycursor.execute(sql_ins,val)

		mydb.commit()
		messagebox.showinfo("Operation Successfull!!","Amount Debited Successfully!!")
		master.destroy()
		return

def Cr_Amt(accnt,name):
	creditwn=tk.Tk()
	creditwn.geometry("600x300")
	creditwn.title("Credit Amount")
	creditwn.configure(bg="orange")
	fr1=tk.Frame(creditwn,bg="blue")
	l_title=tk.Message(creditwn,text="UNITED BANK",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="black",justify="center",anchor="center")
	l_title.config(font=("Courier","50","bold"))
	l_title.pack(side="top")
	l1=tk.Label(creditwn,relief="raised",text="Enter Amount to be credited: ")
	e1=tk.Entry(creditwn,relief="raised")
	l1.pack(side="top")
	e1.pack(side="top")
	b=tk.Button(creditwn,text="Credit",relief="raised",command=lambda:crdt_write(creditwn,e1.get().strip(),accnt,name))
	b.pack(side="top")
	creditwn.bind("<Return>",lambda x:crdt_write(creditwn,e1.get(),accnt,name))

def De_Amt(accnt,name):
	debitwn=tk.Tk()
	debitwn.geometry("600x300")
	debitwn.title("Debit Amount")	
	debitwn.configure(bg="orange")
	fr1=tk.Frame(debitwn,bg="blue")
	l_title=tk.Message(debitwn,text="UNITED BANK",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="black",justify="center",anchor="center")
	l_title.config(font=("Courier","50","bold"))
	l_title.pack(side="top")
	l1=tk.Label(debitwn,relief="raised",text="Enter Amount to be debited: ")
	e1=tk.Entry(debitwn,relief="raised")
	l1.pack(side="top")
	e1.pack(side="top")
	b=tk.Button(debitwn,text="Debit",relief="raised",command=lambda:debit_write(debitwn,e1.get(),accnt,name))
	b.pack(side="top")
	debitwn.bind("<Return>",lambda x:debit_write(debitwn,e1.get(),accnt,name))

def disp_bal(accnt):
	sql_sel="select oc from "+accnt
	mycursor.execute(sql_sel)
	bal= mycursor.fetchall()[0][0]
	messagebox.showinfo("Balance",bal)

def disp_tr_hist(accnt):
	disp_wn=tk.Tk()
	disp_wn.geometry("900x600")
	disp_wn.title("Transaction History")
	disp_wn.configure(bg="orange")
	fr1=tk.Frame(disp_wn,bg="blue")
	l_title=tk.Message(disp_wn,text="UNITED BANK",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="black",justify="center",anchor="center")
	l_title.config(font=("Courier","50","bold"))
	l_title.pack(side="top")
	fr1=tk.Frame(disp_wn)
	fr1.pack(side="top")
	l1=tk.Message(disp_wn,text="Your Transaction History:",padx=100,pady=20,width=1000,bg="blue",fg="orange",relief="raised")
	l1.pack(side="top")
	fr2=tk.Frame(disp_wn)
	fr2.pack(side="top")

	sql_sel="select * from "+accnt+"rec"
	mycursor.execute(sql_sel)
	myresult=mycursor.fetchall()

	for line in myresult:
		l=tk.Message(disp_wn,anchor="w",text=line,relief="raised",width=2000)
		l.pack(side="top")
	mydb.commit()
	b=tk.Button(disp_wn,text="Quit",relief="raised",command=disp_wn.destroy)
	b.pack(side="top")	

def logged_in_menu(accnt,name):
	rootwn=tk.Tk()
	rootwn.geometry("1600x500")
	rootwn.title("UNITED BANK-"+name)
	rootwn.configure(background='orange')
	fr1=tk.Frame(rootwn)
	fr1.pack(side="top")
	l_title=tk.Message(rootwn,text="SIMPLE BANKING\n SYSTEM",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="black",justify="center",anchor="center")
	l_title.config(font=("Courier","50","bold"))
	l_title.pack(side="top")
	label=tk.Label(text="Logged in as: "+name,relief="raised",bg="black",fg="white",anchor="center",justify="center")
	label.pack(side="top")
	img2=tk.PhotoImage(file="credit.gif")
	myimg2=img2.subsample(2,2)
	img3=tk.PhotoImage(file="debit.gif")
	myimg3=img3.subsample(2,2)
	img4=tk.PhotoImage(file="balance1.gif")
	myimg4=img4.subsample(2,2)
	img5=tk.PhotoImage(file="transaction.gif")
	myimg5=img5.subsample(2,2)
	b2=tk.Button(image=myimg2,command=lambda: Cr_Amt(accnt,name))
	b2.image=myimg2
	b3=tk.Button(image=myimg3,command=lambda: De_Amt(accnt,name))
	b3.image=myimg3
	b4=tk.Button(image=myimg4,command=lambda: disp_bal(accnt))
	b4.image=myimg4
	b5=tk.Button(image=myimg5,command=lambda: disp_tr_hist(accnt))
	b5.image=myimg5
	
	img6=tk.PhotoImage(file="logout.gif")
	myimg6=img6.subsample(2,2)
	b6=tk.Button(image=myimg6,relief="raised",command=lambda: logout(rootwn))
	b6.image=myimg6

	b2.place(x=100,y=150)
	b3.place(x=100,y=220)
	b4.place(x=900,y=150)
	b5.place(x=900,y=220)
	b6.place(x=500,y=400)
	
def logout(master):
	
	messagebox.showinfo("Logged Out","You Have Been Successfully Logged Out!!")
	master.destroy()
	Main_Menu()

def check_log_in(master,name,acc_num,pin):
	if(check_acc_nmb(acc_num)==0):
		master.destroy()
		Main_Menu()
		return
	'''
	sql_sel="select name,pin from"+acc_num
	mycursor.execute(sql_sel)
	name_pin=mycursor.fetchall()[0]
	if name_pin[0]!=name or name_pin[1]!=pin:
			messagebox.showinfo("Error","Invalid Credentials\nPlease try again.")
			master.destroy()
			Main_Menu()
	'''
	if( (is_number(name))  or (is_number(pin)==0) ):
		messagebox.showinfo("Error","Invalid Credentials\nPlease try again.")
		master.destroy()
		Main_Menu()
	else:
		master.destroy()
		logged_in_menu(acc_num,name)

def log_in(master):
	master.destroy()
	loginwn=tk.Tk()
	loginwn.geometry("600x300")
	loginwn.title("Log in")
	loginwn.configure(bg="orange")
	tk.Frame(loginwn,bg="blue")
	l_title=tk.Message(loginwn,text="UNITED BANK",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="black",justify="center",anchor="center")
	l_title.config(font=("Courier","50","bold"))
	l_title.pack(side="top")
	l1=tk.Label(loginwn,text="Enter Name:",relief="raised")
	l1.pack(side="top")
	e1=tk.Entry(loginwn)
	e1.pack(side="top")
	l2=tk.Label(loginwn,text="Enter account number:",relief="raised")
	l2.pack(side="top")
	e2=tk.Entry(loginwn)
	e2.pack(side="top")
	l3=tk.Label(loginwn,text="Enter your PIN:",relief="raised")
	l3.pack(side="top")
	e3=tk.Entry(loginwn,show="*")
	e3.pack(side="top")
	b=tk.Button(loginwn,text="Submit",command=lambda: check_log_in(loginwn, e1.get().strip(), e2.get().strip(), e3.get().strip()))
	b.pack(side="top")
	b1=tk.Button(text="HOME",relief="raised",bg="black",fg="white",command=lambda: home_return(loginwn))
	b1.pack(side="top")
	loginwn.bind("<Return>",lambda x:check_log_in(loginwn,e1.get().strip(),e2.get().strip(),e3.get().strip()))
	
def Create():
	
	crwn=tk.Tk()
	crwn.geometry("600x300")
	crwn.title("Create Account")
	crwn.configure(bg="orange")
	fr1=tk.Frame(crwn,bg="blue")
	l_title=tk.Message(crwn,text="UNITED BANK",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="black",justify="center",anchor="center")
	l_title.config(font=("Courier","50","bold"))
	l_title.pack(side="top")
	l1=tk.Label(crwn,text="Enter Name:",relief="raised")
	l1.pack(side="top")
	e1=tk.Entry(crwn)
	e1.pack(side="top")
	l2=tk.Label(crwn,text="Enter opening credit:",relief="raised")
	l2.pack(side="top")
	e2=tk.Entry(crwn)
	e2.pack(side="top")
	l3=tk.Label(crwn,text="Enter desired PIN:",relief="raised")
	l3.pack(side="top")
	e3=tk.Entry(crwn,show="*")
	e3.pack(side="top")
	b=tk.Button(crwn,text="Submit",command=lambda: write(crwn,e1.get().strip(),e2.get().strip(),e3.get().strip()))
	b.pack(side="top")
	crwn.bind("<Return>",lambda x:write(crwn,e1.get().strip(),e2.get().strip(),e3.get().strip()))
	return

def Main_Menu():
	
	rootwn=tk.Tk()
	rootwn.geometry("1600x500")
	rootwn.title("UNITED Bank")
	rootwn.configure(background='orange')
	fr1=tk.Frame(rootwn)
	fr1.pack(side="top")
	bg_image = tk.PhotoImage(file ="pile1.gif")
	x = tk.Label (image = bg_image)
	x.place(y=-400)
	l_title=tk.Message(text="SIMPLE BANKING\n SYSTEM",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="black",justify="center",anchor="center")
	l_title.config(font=("Courier","50","bold"))
	l_title.pack(side="top")
	imgc1=tk.PhotoImage(file="new.gif")
	imglo=tk.PhotoImage(file="login.gif")
	imgc=imgc1.subsample(2,2)
	imglog=imglo.subsample(2,2)

	b1=tk.Button(image=imgc,command=Create)
	b1.image=imgc
	b2=tk.Button(image=imglog,command=lambda: log_in(rootwn))
	b2.image=imglog
	img6=tk.PhotoImage(file="quit.gif")
	myimg6=img6.subsample(2,2)

	b6=tk.Button(image=myimg6,command=rootwn.destroy)
	b6.image=myimg6
	b1.place(x=800,y=300)
	b2.place(x=800,y=200)	
	b6.place(x=920,y=400)

	rootwn.mainloop()

Main_Menu()
