import mysql.connector , hashlib
from tkinter import *
from tkinter import simpledialog
from functools import partial

#Database code
conn=mysql.connector.connect(host='localhost',username='root',password='a&r1342/2000A',database='password_manager')
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS masterpassword(id INTEGER PRIMARY KEY, password TEXT NOT NULL);""")

#ALTER THE TABLE
#cursor.execute("ALTER TABLE Vault MODIFY COLUMN id INT AUTO_INCREMENT PRIMARY KEY DEFAULT NULL;")

cursor.execute("""CREATE TABLE IF NOT EXISTS Vault(id INT AUTO_INCREMENT PRIMARY KEY, Website TEXT NOT NULL, Username TEXT NOT NULL, Password TEXT NOT NULL);""")

#CREATE POPUP
def popUp(text):
    answer = simpledialog.askstring("input string", text)
    #print(answer)
    return answer



#Initiate window
window = Tk()

window.title("Password Maneger")

def firstScreen():
    window.geometry("250x150")

    lbl = Label(window, text="Create Master Passward")
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=20) 
    txt.pack()
    txt.focus()

    lbl1 =Label(window, text="Re-enter Password")
    lbl1.pack()

    txt1 = Entry(window, width=20) 
    txt1.pack()
    txt1.focus()

    lbl2 =Label(window)
    lbl2.pack()


    def savePassword():
        if txt.get() ==txt1.get():
          hashedPassword = txt.get()

          insert_password =("""INSERT INTO masterpassword(password) VALUES (%s)""")               #something worng here due to that data doesn't enter in database table
          cursor.execute(insert_password, [(hashedPassword )])
          conn.commit()

          passwordManager()
        else:
            lbl2.config(text="Password do not match")

    btn = Button(window, text="Save", command=savePassword) 
    btn.pack(pady=10)


def loginScreen():
    window.geometry("350x100")

    lbl = Label(window, text="Enter Master Passward")
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=20, show="*") 
    txt.pack()
    txt.focus()

    lbl1 =Label(window)
    lbl1.pack()

    def getMasterPassword():
        checkHashedPassword = txt.get()
        cursor.execute("SELECT * FROM masterpassword WHERE id=1 AND password = %s",[(checkHashedPassword)])
        return cursor.fetchall()

    def checkPassword():
        #password = "Arnava123"
        match = getMasterPassword()

        if match:  #password == txt.get():
            passwordManager() 
        else:
            txt.delete(0,'end') 
            lbl1.config(text="Wrong Password")

    btn = Button(window, text="Submit", command=checkPassword) 
    btn.pack(pady=10)

def passwordManager():
    for widget in window.winfo_children():
        widget.destroy()


    def addEntry():
        text1 = "Website"
        text2 = "Username"
        text3 = "Password"
                                                #something is wrong here in addEntry due to that data doesn't enter in database table
        Website = popUp(text1) 
        Username = popUp(text2)
        Password = popUp(text3)

        insert_fields = ("INSERT INTO Vault(id,Website,Username,Password) VALUES (%s,%s,%s)")
        cursor.execute(insert_fields, (Website, Username, Password))
        #cursor.executemany("INSERT INTO password_manager. vault ( Website, Username, Password) VALUES ( 'test', 'test', '123');")
        conn.commit()

        passwordManager()

    def removeEntry(input):   
        cursor.execute("DELETE FROM Vault WHERE id = %s", (input,))
        conn.commit()

        passwordManager()


    window.geometry("750x350")    

    #popUp("Whats your name")

    lbl = Label(window, text="Password Manager")
    #lbl.config(anchor=CENTER)
    #lbl.pack()
    lbl.grid(column=1)

    btn = Button(window, text="+", command=addEntry)
    btn.grid(column=1, pady=10)

    lbl = Label(window, text="Website")
    lbl.grid(row=2, column=0, padx=80)
    lbl = Label(window, text="Username")
    lbl.grid(row=2, column=1, padx=80)
    lbl = Label(window, text="Password")
    lbl.grid(row=2, column=2, padx=80)

    cursor.execute("SELECT * FROM Vault")
    if(cursor.fetchall() !=None):
        i=0
    while True:
        cursor.execute("SELECT * FROM Vault")    
        array = cursor.fetchall()

        lbl1 = Label(window,text=(array[i][1]), font=("Helvectica", 12))
        lbl1.grid(column=0,row=i+3)
        lbl1 = Label(window,text=(array[i][2]), font=("Helvectica", 12))
        lbl1.grid(column=1,row=i+3)
        lbl1 = Label(window,text=(array[i][3]), font=("Helvectica", 12))
        lbl1.grid(column=2,row=i+3)

        btn = Button(window, text="Delet", command= partial(removeEntry, array[i][0]))
        btn.grid(column=3, row=i+3, pady=10)

        i=i+1

        cursor.execute("SELECT * FROM Vault")
        if(len(cursor.fetchall())<= i):
            break  



cursor.execute("SELECT * FROM masterpassword")
if cursor.fetchall():
    loginScreen()
else:
    firstScreen() 

window.mainloop()
