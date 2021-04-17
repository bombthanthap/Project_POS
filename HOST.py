#postest 1234

from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk
from ftplib import FTP
from datetime import date
from datetime import datetime

import os,sys
import random
import time
import math
import smtplib
import tkinter as tk
import csv

from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders


def get_time():
    timeVar = time.strftime("%I:%M:%S %p")
    clock.config(text=timeVar)
    clock.after(200,get_time)

def qExit():
    return root.destroy()

#-------------------- Variable root for TK --------------------#
root = Tk()
root.title(" PROJECT PARKING ")
w=1120
h=680
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

photo = PhotoImage(file = r"D:\workzone\networkProg\projectPOS\New folder\image\car.png")
photoclock = PhotoImage(file = r"D:\workzone\networkProg\projectPOS\New folder\image\cl.png")
photoin = PhotoImage(file = r"D:\workzone\networkProg\projectPOS\New folder\image\in.png")
photoout = PhotoImage(file = r"D:\workzone\networkProg\projectPOS\New folder\image\out.png")
photoall = PhotoImage(file = r"D:\workzone\networkProg\projectPOS\New folder\image\allcar2.png")
##photocar = PhotoImage(file = r"D:\workzone\networkProg\projectPOS\New folder\image\car2.png")

# Resizing image to fit on button
photoimage = photo.subsample(10,10)
photoclockimage = photoclock.subsample(20,20)
photoinimage = photoin.subsample(1,1)
photooutimage = photoout.subsample(1,1)
photoallimage = photoall.subsample(20,20)
##photocarimage = photocar.subsample(3,3)

#CAL POSITION
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)-50

root.geometry('%dx%d+%d+%d' % (w,h,x,y))
root.configure(background = 'bisque2')
#-------------------- HEAD Frame --------------------#
TopTop = Frame(root, bg = 'black',padx=2, pady=2)
TopTop.grid(row=0, column=0) 

Title = Label(TopTop,font=('arial',50,'bold'), text=" PARKING SYSTEM", bd=21,bg='salmon',image = photoimage,compound = LEFT).grid(row=0,column=0)
TopTop.place(relx = 0.5,rely= 0.1,anchor = 'center')

#-------------------- TIME Frame --------------------#
Tops = Frame(root,relief = SUNKEN)
Tops.place(relx = 0.4,rely= 0.245,anchor = 'center')
Tops2 = Frame(root,relief = SUNKEN)
Tops2.place(relx = 0.56,rely= 0.245,anchor = 'center')
today =date.today()

lblInfo = Label(Tops,font=('TH Sarabun New',20,'bold')
            ,text=today,fg = "blue",bd=10,bg="snow",anchor='w')
lblInfo.grid(row=1,column=0)
##time
clock = Label(Tops2,font=('TH Sarabun New',20,'bold'),text=today,fg = "blue",bd=10,bg="Snow",image = photoclockimage,compound = LEFT,anchor='w')
clock.pack()
clock.grid(row=2,column=0)
get_time()

## TIME CURRENT
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
date_time = time.strftime("%d/%m/%Y", t)
#date_time = time.strftime("%Y-%m-%d", t)
print(date_time)
##print("Current time is: "+current_time)
print("********************************")



#-------------------- Connect Server --------------------#
try:
    ftp = FTP('localhost')
    ftp.login(user = 'postest',passwd = '1234')
    print("===== User Conected =====")
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


#-------------------- DEF --------------------#
def getvals(): #write file
    price_value.set(0)
    fee_value.set(0)
    state.set(0)

    try:
        my_file = open('records.csv')
        r = csv.reader(my_file)
        for row in r:
            current_id = int(row[0])
        print("lasted_id =",current_id)
        my_file.close()
    except Exception as e:
        current_id = 0

    print("Submitting form")

    top = Label(root,text ="\nOrder : "+str(current_id+1)+"\nDay : "+date_time+"\n Time-in : "+current_time+"\nCar number : "+carnum_value.get()+"\n Value : "+price_value.get()+"\n Status : "+state.get(),font=('arial',20,))
    top.place(relx = 0.83,rely= 0.52,anchor = 'center')
    
        
    print(f"{str(current_id+1), carnum_value.get() , price_value.get() ,current_time,state.get(),date_time,fee_value.get()}")
    
    with open('records.csv', newline='', mode='a') as f:
        f_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        f_writer.writerow([str(current_id+1), carnum_value.get(), price_value.get(),current_time,state.get(),str(date_time),fee_value.get()])

    #---------  write file to FTP SERVER ---------#    
    filename = 'records.csv'
    ftp.storbinary('STOR '+filename,open(filename,'rb'))
    print("***** Upload records Success *****")
        
    messagebox.showinfo("Record Car parking "," Insert Success ")
    
# not use anymore
def read_id(id):

    b = csv.reader(open('records.csv'))
    lines = list(b)
    for row in lines:
        if(row[0] == id):
            row[4] = 1
            writer = csv.writer(open('records.csv', 'w',newline = ''))
            writer.writerows(lines)
        print(row)
    b.close()

def readfile(id):
    try:
        my_file = open('records.csv')
        r = csv.reader(my_file)
        lines = list(r)
        for row in lines:
            try:
                if(row[0] == id):
                    if(row[4] == '0'):
                        #change status
                        row[4] = 1
                        
                        print('value is : %s' % (row[2]))
                        ## TIME DIFF ##
                        FMT = '%H:%M:%S'
                        tdelta = abs(datetime.strptime(current_time, FMT) - datetime.strptime(row[3], FMT))
                        timedif = tdelta
                        timedif = str(timedif)
                        print('time-in :',row[3])
                        print("Time-out: "+current_time)
                        print('Time diff : ',tdelta)

                        mint = tdelta.seconds//60
                        hour = mint//60
                        if(mint%60 >= 30):
                            hour += 1

                        #price >=1000 free
                        if(int(row[2]) >= 1000):
                            print('value more than 1000 Car parking free')
                            row[6] = 0
                            
                        #print 100-500 1hr free
                        elif(int(row[2]) >= 100):
                            print('free 1 hr')
                            # time > 1 hr u gonna paid
                            if(hour > 1):
                                print('Parking fee',(hour-1)*30)
                                row[6] = (hour-1)*30
                        elif(int(row[2]) < 100):
                            print('Parking fee',(hour)*30)
                            row[6] = (hour)*30
                        writer = csv.writer(open('records.csv', 'w',newline = ''))
                        writer.writerows(lines)
                        
                        top = Label(root,text ="\nOrder : "+str(id)+"\nDay : "+date_time+"\n Time-Dif : "+timedif+"\nCar number : "+row[1]+"\n Value : "+row[2]+"\n Car fee : "+str(row[6]),font=('arial',20,))
                        top.place(relx = 0.83,rely= 0.52,anchor = 'center')
                        return
                    else:
                        print('No more car id')
                        messagebox.showinfo(" Alert "," No car id  ")
                        break
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        print("No file")
        sys.exit(1)
    
    my_file.close()
##    filename = 'records.csv'
##    ftp.storbinary('STOR '+filename,open(filename,'rb'))

    
#--------------------  write file to FTP SERVER --------------------#    
def upload():
    try:
        filename = 'records.csv'
        ftp.storbinary('STOR '+filename,open(filename,'rb'))
        print("***** Upload Success *****")
        messagebox.showinfo(" Update Values "," Update Values Success ")
        read()
    except Exception as e:
        print('error upload')
        print(e)
   
def read():
    try:
        f = open('records.csv')
        csv_f = csv.reader(f)
        for row in csv_f:
            print(row)
    except :
        print('Not file CSV yet')
    f.close()

def enteroutput():
    ##  text form
    top = Label(root, text = "OUT FUNCTION",width=20,height=3,font=('arial',10,'bold'),bg='snow',fg='navy')
    car_id = Label(root, text = "ID",width=10,height=2,font=('arial',10,'bold'),bg='snow',fg='navy')
    car_num = Label(root, text = "Car number",width=10,height=2,font=('arial',10,'bold'),bg='snow',fg='navy')

    ##  pack text
    top.place(relx = 0.5,rely= 0.4,anchor = 'center')
    car_id.place(relx = 0.43,rely= 0.55,anchor = 'center')
    car_num.place(relx = 0.43,rely= 0.65,anchor = 'center')

    ## Entries form
    car_entry = Entry(root, textvariable = carid_value,font=('Arial' ,20, 'bold'))
    num_entry = Entry(root, textvariable = carnum_value,font=('Arial' ,20, 'bold'))

    ## pack Entries 
    car_entry.place(relx = 0.55,rely= 0.55,width=120,height=40,anchor = 'center')
    num_entry.place(relx = 0.55,rely= 0.65,width=120,height=40,anchor = 'center')

    print('****************************************************************************')
    print("Enter output fuction")
    read()

    Button(root,text="Submit", bd = 8,padx=6,pady=6,fg="darkgreen",font=('TH Sarabun New',12,'bold'),width=5,bg="limegreen",command=lambda:readfile(carid_value.get())).place(relx = 0.5,rely= 0.78,anchor = 'center')
    Button(root,text="Upload",padx=6,pady=6,bd=8,fg="royalblue",font=('TH Sarabun New',12,'bold'),width=5,bg="navy" ,command=upload).place(relx = 0.5,rely= 0.88,anchor = 'center')

    

def enterinput():
    print("Current Time =", current_time)
    ##  text form
    top = Label(root, text = "IN FUNCTION",width=20,height=3,font=('arial',10,'bold'),bg='snow',fg='navy')
    car_num = Label(root, text = "Car number",width=10,height=2,font=('arial',10,'bold'),bg='snow',fg='navy')

    ##  pack text
    top.place(relx = 0.5,rely= 0.4,anchor = 'center')
    car_num.place(relx = 0.43,rely= 0.65,anchor = 'center')

    ## Entries form
    num_entry = Entry(root, textvariable = carnum_value,font=('Arial' ,16, 'bold'))

    ## pack Entries 
    num_entry.place(relx = 0.55,rely= 0.65,anchor = 'center',width=120,height=40)

    print('****************************************************************************')
    print("Enter input fuction")
    read()

    Button(root,text="Submit", bd = 8,padx=6,pady=6,fg="darkgreen",font=('TH Sarabun New',12,'bold'),width=5,bg="limegreen" ,command=getvals).place(relx = 0.5,rely= 0.78,anchor = 'center')

def result():
    #current_time = time.strftime("%H:%M:%S", t)
    date_time2 = datetime.now()

    num_in = 0
    num_out = 0
    price = 0
    
    try:
        my_file = open('records.csv')
        r = csv.reader(my_file)
        for row in r:
            b=datetime.strptime(row[5], '%d/%m/%Y')
##            print(date_time2)
##            print(b)
            if (b.day==date_time2.day and b.month==date_time2.month and b.year==date_time2.year):
                #print(date_time2.day)
                #print(b.day)
                num_in+=1
                price += int(row[6])
                if row[4] == "1":
                    num_out+=1
        my_file.close()
    except Exception as e:
        print(e)
        print('error fuc result')
        print('Not file CSV yet')
        
    print('========================================')
    print("Car in : ",num_in)
    print("Car out : ",num_out)
    print("Sum of value : ",price)
    print("Current day : "+date_time)
    print('========================================')
    
    date = date_time.replace("/","-")
    file_name = "Report_" + date
    name = open("%s.txt" %(file_name), "w", encoding = "utf-8")
    name.write("Reort ประจำวันที่ " + date_time +"\n")
    name.write("มีรถเข้าทั้งหมด " + str(num_in) + " คัน" +"\n")
    name.write("มีรถออกทั้งหมด " + str(num_out) + " คัน" +"\n")
    name.write("รวมค่าบริการจอดรถทั้งหมด " + str(price) + " บาท" +"\n")
    name.close()

    try:
        # local file wat want to upload
        with open("%s.txt" %(file_name), "rb") as file:
            # use FTP's STOR command to upload this file
            ftp.storbinary(f"STOR {file_name}.txt", file)

        print(" Export CSV "+date+" success")
        messagebox.showinfo(" Report Car parking "," Insert Report Success ")

        print("Export file %s success" %(file_name))
    except Exception as e:
        print(e)
        print('Cant send file ')
        return 0
    ###send mail###
    try:
        input = open("data.txt")
        sender_address,sender_pass,receiver_address = input.read().split(",")
        input.close()
    except:
        print("File not found")

    try:
        try:
            name = open("%s.txt" %(file_name), "r", encoding = "utf-8")
            
        except:
            print("File not found")

        mail_content = name.read()
        name.close()
        
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = file_name
        message.attach(MIMEText(mail_content, 'plain'))

        #Sent the csv file 
        file_csv = 'records.csv'
        attachment = open(file_csv, "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % file_csv)
        message.attach(p)

        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')
    except Exception as e:
        print(e)
        print('error sent mail')
        print("Can't send mail")
   
    print("*********************************")

def msgbox():
    
    ans = messagebox.askquestion("Confirm","Are you sure?")  
    if ans == 'yes':
        print('send to def result ')
        result()
    else:
        print('Exit')
    
#-------------------- VARIABLE ENTRIES --------------------#
carid_value = StringVar()
carnum_value = StringVar()
price_value = StringVar()
fee_value = StringVar()
state = StringVar()

#-------------------- BUTTON FRAME --------------------#
btnFrame = Frame(root,relief=RIDGE)
btnFrame.grid(row=2, column=0,padx=65,pady=200)

inputFrame = Frame(root,relief=RIDGE)
inputFrame.grid(row=2, column=1)

billFrame = Frame(root,relief=RIDGE)
billFrame.place(x=750,y=200)

leftFrame = Frame(btnFrame , bd=10, width=260, height=475,bg="#2b5797" , relief=RIDGE)
leftFrame.pack()

rightFrame = Frame(billFrame , bd=10, width=350, height=320,bg="white" , relief=RIDGE)
rightFrame.pack()

midFrame = Frame(inputFrame , bd=10, width=340, height=475,bg="#2b5797" , relief=RIDGE)
midFrame.pack()

button_in = Button(root,bd=6,command = enterinput,padx=85,pady=55,background="limegreen",relief=RIDGE,image = photoinimage,compound = LEFT)
button_in.place(x=100,y=235)

button_out = Button(root, bd=6,command=enteroutput,padx=75,pady=50,background="lightcoral",relief=RIDGE,image = photooutimage,compound = LEFT)
button_out.place(x=100,y=375)

button_sum = Button(root,text='SUM', bd=6,command=msgbox,padx=30,pady=20,background="navajowhite",relief=RIDGE,image = photoallimage,compound = LEFT)
button_sum.place(x=100,y=520)


btnExit=Button(padx=3,pady=3,bd=5,fg="red",font=('TH Sarabun New',12,'bold'),width=5,text="Exit",bg="lightcoral",command=qExit).place(relx = 0.82,rely= 0.9,anchor = 'center')

root.resizable(width=False, height=False)
root.mainloop()
