import mysql.connector
import datetime
from tabulate import tabulate

db = input("Enter name of your database :")

mydb=mysql.connector.connect(host='localhost',user='root',passwd='sahil9087')
mycursor=mydb.cursor()
sql="CREATE DATABASE if not exists "+db
mycursor.execute(sql)
mydb.commit()
print("Database created successfully..")
mycursor = mydb.cursor()
mycursor.execute('use '+db)
tablename = input ("Name of the table to be created :")
query = "create table if not exists "+tablename+"\
(Applicant_no integer primary key,\
Name char(15),\
IFSC integer unique,\
Credit float Default'0.0',\
Debit float Default'0.0',\
Balance float Default'0.0',\
City char(10),\
Branch integer)"
print("Table "+tablename+" created successfully...")
mycursor.execute(query)

while True:
    print('\n\n\n')
    print("*"*159)
    print('\t\t\t\ti. Adding customer records')
    print('\t\t\t\t2. For displaying record of all the customers')
    print('\t\t\t\t3. For displaying record of a particular customer')
    print('\t\t\t\t4. For deleting records of all customers')
    print('\t\t\t\t5. For deleting a record of a particular customer')
    print('\t\t\t\t6. For modification in a record')
    print('\t\t\t\t7. For displaying passbook')
    print('\t\t\t\t8. For displaying passbook for all the customers in a particular branch')
    print('\t\t\t\t9. For displaying passbook of a particular customers')
    print('\t\t\t\t10.For exit')
    print('Enter choice...', end='' )
    choice = int(input())
    if choice==1:
        try:
            print("Enter Customer information...")
            ano=int(input("Enter application number :"))
            name=input("Enter name :")
            ifsc=int(input("Enter IFSC code :"))
            c=float(input("Enter amount credited :"))
            d=float(input("Enter amount debited :"))
            b=float(input("Enter  account balance :"))
            city=input("Enter city name :")
            branch=int(input("Enter branch code :"))
            rec=(ano,name,ifsc,c,d,b,city,branch)
            query='insert into '+tablename+' values(%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(query,rec)
            mydb.commit()
            print("Record added successfully !")
        except Exception as e:
            print("Something went wrong !!!")

    elif choice==2:
        try:
            query='select * from '+tablename
            mycursor.execute(query)
            print(tabulate(mycursor,headers=['Applicant_no','Name','IFSC','Credit','Debit','Balance','City','Branch'],tablefmt='fancy_grid'))
            '''myrecords=mycursor.fetchall()
            For rec in myrecords:
            print(rec)'''
        except:
            print("Something went wrong !!!")

    elif choice==3:
        try:
            en=input("Enter applicant no. of the record to be displayed...")
            query='select * from '+tablename+' where Applicant_no='+en
            mycursor.execute(query)
            myrecord=mycursor.fetchone()
            print("\n\nRecord of Apllicant no.:"+en)
            print(myrecord)
            y=mycursor.rowcount
            if y==-1:
                print("Nothing to display")
        except:
            print("Something went wrong !!!")

    elif choice==4:
        try:
            ch=input("Do you want to delete all the records [Y/N] :")
            if ch.upper=='Y':
                mycursor.execute('Delete from '+tablename)
                mydb.commit()
                print("All the records are deleted...")
        except:
            print("Something went wrong !!!")

    elif choice==5:
        try:
            en=input("Enter applicant no. of the record to be deleted...")
            query='delete from '+tablename+' where Applicant_no='+en
            mycursor.execute(query)
            mydb.commit()
            x=mycursor.rowcount
            if x>0:
                print("Deletion done")
            else:
                print("Something went wrong !!!")
        except:
            print("Something went wrong !!!")

    elif choice==6:
        try:
            en=input("Enter applicant no. of the record to be modified...")
            query='select * from '+tablename+' where Applicant_no='+en
            mycursor.execute(query)
            myrecord=mycursor.fetchone()
            x=mycursor.rowcount
            if x==-1:
                print("Applicant no. not exist")
            else:
                mname=myrecord[1]
                mcity=myrecord[6]
                mbranch=myrecord[7]
                print("Applicant no.  :",myrecord[0])
                print("Name           :",myrecord[1])
                print("IFSC           :",myrecord[2])
                print("Credit         :",myrecord[3])
                print("Debit          :",myrecord[4])
                print("Balance        :",myrecord[5])
                print("City           :",myrecord[6])
                print("Branch         :",myrecord[7])
                print('-'*15)
                print("Type value to modify below or just press enter for no change")
                p=input("Enter name")
                if len(p)>0:
                    uName=p
                q=input("Enter city")
                if len(q)>0:
                    uCity=q
                r=input("Enter branch")
                if len(r)>0:
                    uBranch=r
                query='update '+tablename+' set Name= '+" ' "+uName+" ' "+' , '+' City= '+" ' "+uCity+" ' "+' , '+' Branch= '+" ' "+uBranch+" ' "+' where Applicant_no= '+en
                mycursor.execute(query)
                mydb.commit()
                print('Record , modified')
        except:
            print("Something went wrong !!!")

    elif choice==7:
        try:
            query='select * from '+tablename
            mycursor.execute(query)
            myrecords=mycursor.fetchall()
            print("\n\n\n")
            print('+'*159)
            print("\n\t\t\t\t\t\t\tPassbook\n")
            print('+'*159)
            now=datetime.datetime.now()
            print("Current date and time :",end='')
            print(now.strftime("%y~%m~%d %H:%M:%S"))
            print('-'*159)
            print('Applicant_no','Name','IFSC','Credit','Debit','Balance','City','Branch')
            print('-'*159)
            for rec in myrecords:
                print(rec)
            print("-"*159)
            print("-"*159)
        except:
            print("Something went wrong !!!")

    elif choice==8:
        try:
            a=input("Enter branch code :")
            query="select * from "+tablename+" where Branch="+a
            mycursor.execute(query)
            '''now=datetime.datetime.now()
            print("\n\n\n")
            print('*'*159)
            print("Passbook",center(90))
            print('*'*159)
            print("Current date and time :",end='')
            print(now.strftime("%y~%m~%d %H:%M:%S"))
            myrecords=mycursor.fetchall()
            for rec in myrecords:
                print(rec)
                #'%~4d %~15s %~10s %~8.2s %~8.2f %~8.2f %~9.2f %~8.2f %~9.2f'%
            print("*"*95)'''
            now=datetime.datetime.now()
            print("\n\n\n\t\t\tPassbook")
            print("Current date and time :",end='')
            print(now.strftime("%y~%m~%d %H:%M:%S"))
            data=mycursor.fetchall()
            for i in data:
                print(i)
        except:
            print("Something went wrong !!!")

    elif choice==9:
        try:
            en=input("Enter applicant no. of the record to display passbook...")
            query='select * from '+tablename+' where Applicant_no='+en
            mycursor.execute(query)
            now=datetime.datetime.now()
            print("\n\n\n\t\t\tPassbook")
            print("Current date and time :",end='')
            print(now.strftime("%y~%m~%d %H:%M:%S"))
            data=mycursor.fetchone()
            print(data)
            #print(tabulate(mycursor, headers=['Applicant_no','Name','IFSC','Credit','Debit','Balance','City','Branch'],tablefmt='fancy_grid'))
        except Exception as e:
            print("Something went wrong !!!",e)

    elif choice==10:
        break
    else:
        print("Wrong Choice")
