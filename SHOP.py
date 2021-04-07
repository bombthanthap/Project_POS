#posshop 1234

from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk
from ftplib import FTP
from datetime import date

import os,sys
import random
import time
import math
import smtplib
import tkinter as tk

import csv


#-------------------- Connect Server and download csv from Server --------------------#
try:
    ftp = FTP('localhost')
    ftp.login(user = 'posshop',passwd = '1234')
    print("===== SHOPPING Connected =====")
    try:
        filename = 'records.csv'
        localfile = open(filename,'wb')
        ftp.retrbinary('RETR '+filename,localfile.write,1024)
        localfile.close()
    except:
        print('======== No file on ftp server ========')
        print('======== Plz check this file ========')

except:
    print("IP or user or passwd wrong can't connected")
    sys.exit(1)

    
def get_time():
    timeVar = time.strftime("%I:%M:%S %p")
    clock.config(text=timeVar)
    clock.after(200,get_time)

def qExit():
    root.destroy()
    
#-------------------- read csv to Server --------------------#
def readfile_id(id,price):
    try:
        my_file = open('records.csv')
        r = csv.reader(my_file)
        lines = list(r)
        for row in lines:
            if(row[0] == id):
                row[2] = int(row[2])+int(price)
                writer = csv.writer(open('records.csv', 'r+',newline = ''))
                writer.writerows(lines)
                print("------- Sum success -------")
                messagebox.showinfo(" Sum Values "," Sum Values Success ")
                break
            
            #else:
                #print("------- No ID longer -------")
                #print("------- Plz check ID again -------")
                #messagebox.showinfo(" Warnning "," No ID longer ")

        my_file.close()
        
    except Exception as e:
        print(e)
        print("No ID")

#--------------------  show data in CSV --------------------#    
def show():
    try:
        f = open('records.csv')
        csv_f = csv.reader(f)
        for row in csv_f:
            print(row)
        print("**********************************************")
    except:
        print('Not file CSV yet')
    f.close()

#--------------------  write file to FTP SERVER --------------------#    
def upload():
    try:
        filename = 'records.csv'
        ftp.storbinary('STOR '+filename,open(filename,'rb'))
        print("***** Upload Success *****")
        messagebox.showinfo(" Update Values "," Update Values Success ")
        show()
    except Exception as e:
        print('error upload')
        print(e)
   
        
#-------------------- Variable root for TK --------------------#
root = Tk()
root.title(" PROJECT SHOPPING ")
w=435
h=550
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()


#CAL POSITION
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)-50

root.geometry('%dx%d+%d+%d' % (w,h,x,y))
root.configure(background = 'bisque2')

#-------------------- BG --------------------#


# Add image file
bg = PhotoImage(file = r"D:\workzone\networkProg\projectPOS\New folder\image\bg.png")

# Create Canvas
canvas1 = Canvas( root, width = 600,height = 600)

canvas1.pack(fill = "both", expand = True)

# Display image
canvas1.create_image( 0, 0, image = bg,anchor = "nw")

# Creating a photoimage object to use image
photo = PhotoImage(file = r"D:\workzone\networkProg\projectPOS\New folder\image\cl.png")

# Resizing image to fit on button
photoimage = photo.subsample(20,20)

# here, image option is used to
# set image on button
# compound option is used to align
# image on LEFT side of button
#Button(root, image = photoimage,compound = LEFT).place(relx = 0.83,rely= 0.8,anchor = 'center')



#-------------------- HEAD Frame --------------------#
TopTop = Frame(canvas1, bg = 'black',padx=2, pady=2)
TopTop.grid(row=0, column=0) 

Title = Label(TopTop,font=('arial',40,'bold'), text=" SHOPPING ", bd=1,bg='salmon').grid(row=0,column=0)
TopTop.place(relx = 0.5,rely= 0.18,anchor = 'center')

#-------------------- TIME Frame --------------------#
Tops = Frame(root,relief = SUNKEN)
Tops.place(relx = 0.25,rely= 0.3,anchor = 'center')
Tops2 = Frame(root,relief = SUNKEN)
Tops2.place(relx = 0.7,rely= 0.3,anchor = 'center')
today =date.today()

lblInfo = Label(Tops,font=('TH Sarabun New',20,'bold')
            ,text=today,fg = "blue",bd=10,bg="snow",anchor='w')
lblInfo.grid(row=1,column=0)
##time
clock = Label(Tops2,font=('TH Sarabun New',20,'bold'),text=today,fg = "blue",bd=10,bg="Snow",image = photoimage,compound = LEFT,anchor='w')
clock.pack()
clock.grid(row=2,column=0)
get_time()

'''
## TIME CURRENT
now = datetime.now()
current_time = now.strftime("%H:%M")
##print("Current time is: "+current_time)
print("********************************")
'''
#-------------------- VARIABLE ENTRIES --------------------#
carid_value = StringVar()
carnum_value = StringVar()
price_value = StringVar()

#-------------------- MID Frame --------------------#
'''
inputFrame = Frame(root,relief=RIDGE)
inputFrame.place(x=125,y=225)

midFrame = Frame(inputFrame , bd=10, width=340, height=475,bg="gray" , relief=RIDGE)
midFrame.pack()
'''
##  text form
top = Label(root, text = "SHOPPING FUNCTION",width=20,height=3,font=('arial',10,'bold'),bg='snow',fg='navy')
car_id = Label(root, text = "ID",width=10,height=2,font=('arial',10,'bold'),bg='snow',fg='navy')
car_num = Label(root, text = "Car number",width=10,height=2,font=('arial',10,'bold'),bg='snow',fg='navy')
price = Label(root, text = "Price",width=10,height=2,font=('arial',10,'bold'),bg='snow',fg='navy')

##  pack text
top.place(relx = 0.5,rely= 0.43,anchor = 'center')
car_id.place(relx = 0.35,rely= 0.558,anchor = 'center')
car_num.place(relx = 0.35,rely= 0.658,anchor = 'center')
price.place(relx = 0.35,rely= 0.758,anchor = 'center')

## Entries form
car_entry = Entry(root, textvariable = carid_value,font=('Arial' ,20, 'bold'))
num_entry = Entry(root, textvariable = carnum_value,font=('Arial' ,20, 'bold'))
price_entry = Entry(root, textvariable = price_value,font=('Arial' ,20, 'bold'))

## pack Entries 
car_entry.place(relx = 0.6,rely= 0.5585,width=120,height=40,anchor = 'center')
num_entry.place(relx = 0.6,rely= 0.6585,width=120,height=40,anchor = 'center')
price_entry.place(relx = 0.6,rely= 0.7585,width=120,height=40,anchor = 'center')





## config btn for sum and update to ftp server
Button(root,text="Submit",padx=6,pady=6,bd=5,fg="darkgreen",font=('TH Sarabun New',12,'bold'),width=5,bg="limegreen",command=lambda:readfile_id(carid_value.get(),price_value.get())).place(relx = 0.6,rely= 0.9,anchor = 'center')
Button(root,text="Upload",padx=6,pady=6,bd=5,fg="royalblue",font=('TH Sarabun New',12,'bold'),width=5,bg="navy" ,command=upload).place(relx = 0.4,rely= 0.9,anchor = 'center')
btnExit=Button(padx=3,pady=3,bd=3,fg="red",font=('TH Sarabun New',10,'bold'),width=5,text="Exit",bg="lightcoral",command=qExit).place(relx = 0.9,rely= 0.93,anchor = 'center')


#------------ Run show csv on start this program ------------#
show()

root.resizable(width=False, height=False)
root.mainloop()
