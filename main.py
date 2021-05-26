import codecs
from random import random
import calendar
from flask import *
from flask.app import setupmethod
import mysql.connector
import datetime
import os
conn=mysql.connector.connect(host="localhost",user="root",password="Root",database="cms",auth_plugin="mysql_native_password")
cur=conn.cursor(buffered=True)
app = Flask(__name__)
app.secret_key="abc"
app.config['UPLOAD_FOLDER'] = 'C:\\Users\\safezone\\Desktop\\finalprj\\templates\\notice\\files'
DOWNLOAD_DIRECTORY = 'C:\\Users\\safezone\\Desktop\\finalprj\\templates\\notice\\cfiles'
@app.route('/logout')
def logout():
    session.pop('userid')
    session.pop('user')
    session.pop('userrole')
    
    return main.login()
@app.route('/downloadnotice/<file>')
def down(file):
    print(file)
    return send_from_directory(DOWNLOAD_DIRECTORY, file, as_attachment=True)
class adminnotice:
    @app.route("/tnotice")
    def notice():
        st="maintemp/admin_main.html"
        return render_template(st,temp="/noticeicon")
    @app.route("/noticeicon")
    def show_noticemain():
        st="maintemp/"+session['userrole']+"main.html"
        return render_template("notice/addnotice.html")
    @app.route("/addnewnote",methods=['POST'])
    def add_notice():
        date=request.form['date']
        title=request.form['title']
        description=request.form['description']
        eventtype=request.form['eventtype']
        file=request.files['event_file']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))
        event_file=file.filename
        print(event_file)
        timing=str(datetime.datetime.now())
        sql="insert into notice(date,name,details,category,file,timestamp)values(%s,%s,%s,%s,%s,%s);"
        val=(date,title,description,eventtype,event_file,timing)
        cur.execute(sql,val)
        conn.commit()
        return view_notice.show_notice()
class hostel:
    @app.route("/addhroom")
    def addroom():
        st="maintemp/admin_main.html"
        return render_template(st,temp="/addroomicon")
    @app.route("/addroomicon")
    def addroomicon():
        st="maintemp/"+session['userrole']+"main.html"
        return render_template("facilities/addroom.html")
    @app.route("/addnewroom",methods=['POST'])
    def adnewroom():
        addroom=request.form['addroom']
        sql="insert into hroom(room_no,status) values(%s,'no');"
        val=(addroom,)
        cur.execute(sql,val)
        conn.commit()
        return hostel.addroomicon()
    
    @app.route("/addhmess")
    def addmess():
        st="maintemp/admin_main.html"
        return render_template(st,temp="/addmessicon")
    @app.route("/addmessicon")
    def addmessicon():
        st="maintemp/"+session['userrole']+"main.html"
        return render_template("facilities/addmess.html")
    @app.route("/addmessroom",methods=['POST'])
    def admessroom():
        breakfast=request.form['breakfast']
        print(breakfast.split(','))
        lunch=request.form['lunch']
        print(lunch.split(','))
        dinner=request.form['dinner']
        print(dinner.split(','))
        
        return hostel.addmessicon()
class adminacc:
    @app.route("/Accounts")
    def acc():
        st="maintemp/admin_main.html"
        return render_template(st,temp="/acc")
    @app.route("/acc")
    def show_Acc():
        st="maintemp/"+session['userrole']+"main.html"
        return render_template("accounts/fee.html")
    @app.route("/fee_det",methods=['POST'])
    def feee_det(regno=''):
        if(regno==''):
            regno=request.form['Registration_Number']
        sql="select course,branch,frname,lname from student where reg_no=%s;"
        val=(regno,)
        cur.execute(sql,val)
        cb=cur.fetchall()
        print(cb)
        sql="select fess from coursereg where course_name=%s and branch=%s;"
        val=(cb[0][0],cb[0][1])
        cur.execute(sql,val)
        cf=cur.fetchall()
        print("pp",cf)
        data=[cb[0][0],cb[0][1],cb[0][2]+cb[0][2],regno]
        print(data)
        sql="select * from fees where regno=%s;"
        val=(regno,)
        cur.execute(sql,val)
        fees=cur.fetchall()
        
        t=[]
        h=[]
        a=[]
        for i in fees:
            if(i[3]=='t'):
                t.append(int(i[2]))
            elif(i[3]=='h'):
                h.append(int(i[2]))
            elif(i[3]=='a'):
                a.append(int(i[2]))
        print(sum(t),sum(h),sum(a))
        sa=sum(a)
        ha=sum(a)
        ta=sum(a)
        icf=int(cf[0][0])
        print(icf)
        return render_template("accounts/viewfees.html",cf=icf,a=sa,h=ha,t=ta,dataa=data)
    @app.route("/TAccounts")
    def tacc():
        st="maintemp/admin_main.html"
        return render_template(st,temp="/tacc")
    @app.route("/tacc")
    def show_tAcc():
        st="maintemp/"+session['userrole']+"main.html"
        return render_template("accounts/feet.html")
    @app.route("/HAccounts")
    def hacc():
        st="maintemp/admin_main.html"
        return render_template(st,temp="/hacc")
    @app.route("/hacc")
    def show_hcc():
        st="maintemp/"+session['userrole']+"main.html"
        return render_template("accounts/feeh.html")
    @app.route("/AAccounts")
    def aacc():
        st="maintemp/admin_main.html"
        return render_template(st,temp="/aacc")
    @app.route("/aacc")
    def show_aAcc():
        st="maintemp/"+session['userrole']+"main.html"
        return render_template("accounts/feea.html")
    
class adminplacement:
    @app.route("/Addcompany")
    def Addcompany():
        st="maintemp/admin_main.html"
        return render_template(st,temp="/Addcompanyicon")
    @app.route("/Addcompanyicon")
    def show_Addcompanymain():
        st="maintemp/"+session['userrole']+"main.html"
        sql="select branch from coursereg;"
        cur.execute(sql)
        es=cur.fetchall()
        lenes=len(es)
        return render_template("placement/Addcompany.html",es=lenes,dataes=es)
    @app.route("/addnewcmp",methods=['POST'])
    def adcmp():
        cmpname=request.form['cmpname']
        role=request.form['role']
        abc=request.form.getlist('eligiblestream')
        ten=request.form['ten']
        twl=request.form['twl']
        diploma=request.form['diploma']
        gap=request.form['gap']
        description=request.form['description']
        stre=str(abc)
        sql="insert into company(name,es,ten,tw,diploma,gap,descc,role) values(%s,%s,%s,%s,%s,%s,%s,%s);"
        val=(cmpname,stre,ten,twl,diploma,gap,description,role)
        cur.execute(sql,val)
        conn.commit()
        return adminplacement.show_Addcompanymain()

    @app.route("/adddrive")
    def adddrive():
        st="maintemp/admin_main.html"
        return render_template(st,temp="/adddriveicon")
    @app.route("/adddriveicon")
    def show_adddrivemain():
        st="maintemp/"+session['userrole']+"main.html"
        sql="select name from company;"
        cur.execute(sql)
        es=cur.fetchall()
        lenes=len(es)
        return render_template("placement/adddrive.html",es=lenes,dataes=es)
    @app.route("/addnewdrive",methods=['POST'])
    def addrivecmp():
        abc=request.form['eligiblestream']
        sql="select id from company where name=%s;"
        val=(abc,)
        cur.execute(sql,val)
        a=cur.fetchall()
        print(a[0][0])
        date=request.form['date']
        time=request.form['time']
        venue=request.form['venue']
        strr=a[0][0]
        sql="insert into companydrive(cid,eventdate,eventtime,venue) values(%s,%s,%s,%s);"
        val=(strr,date,time,venue)
        cur.execute(sql,val)
        conn.commit()
        print(a[0][0],date,time,venue)
        return adminplacement.show_adddrivemain()

    @app.route("/eligible_stu")
    def eligible():
        st="maintemp/admin_main.html"
        return render_template(st,temp="/eligibleicon")
    @app.route("/eligibleicon")
    def eligiblemain():
        st="maintemp/"+session['userrole']+"main.html"
        sql="select name from company;"
        cur.execute(sql)
        es=cur.fetchall()
        lenes=len(es)
        return render_template("placement/eligible.html",es=lenes,dataes=es)
    
    @app.route("/listecmp",methods=['POST'])
    def eligiblelistmain():
        st="maintemp/"+session['userrole']+"main.html"
        eligiblestream=request.form['eligiblestream']
        sql="select * from company where name=%s;"
        val=(eligiblestream,)
        cur.execute(sql,val)
        a=cur.fetchall()
        c=list(a[0][2])
        b="select reg_no,frname,lname,gender,course,branch from student "
        d=[]
        for i in c:
            if(i.isalpha()):
                d.append(i)
        for i in range(len(d)):
            
            if(i==0 and len(d)==1):
                b=b+"where branch='"+d[i]+"' "
            elif(i==0):
                b=b+"where branch='"+d[i]+"' or "
            elif(i!=len(d)-1):
                b=b+"branch='"+d[i]+"' or "
            else:
                b=b+"branch='"+d[i]+"' "
        
        b=b+"AND ten >= "+str(a[0][3])+" AND tw >= "+str(a[0][4])+" AND dip >= "+str(a[0][5])+" order by branch;"
        b=str(b)
        cur.execute(b)
        stu=cur.fetchall()
        print(b)
        lstu=len(stu)

        return render_template("placement/list.html",stud=stu,lstud=lstu)
class att:
    @app.route("/Attendance")
    def att():
        st="maintemp/admin_main.html"
        return render_template(st,temp="/course_attt")
    @app.route("/course_attt")
    def add_course_attt():

        sql="select course_name,branch,sem from coursereg;"
        cur.execute(sql)
        cr=cur.fetchall()
        print(cr)
        return render_template("academics/attselcourse.html",course=cr,lenc=len(cr))
    @app.route("/Yr_attt",methods=["POST"])
    def add_yr_attt():
        course=request.form.to_dict('bg')
        course_br=(course['bg'])
        course=course_br.split("'")
        print(course[1])
        print(course[3])
        print(course[5])
        return render_template("academics/attselsem.html",sem=int(course[5]),course=course[1],branch=course[3])
   
    @app.route("/Generate_attt",methods=["POST"])
    def add_attt():
        cours=request.form['course']
        branc=request.form['branch']
        semi=request.form['sem']
        sem=int(semi)
        tem=0
        if(sem==1 or sem==2):
            tem=(datetime.date.today().year)
        if(sem==3 or sem==4):
            tem=(datetime.date.today().year-1)
        if(sem==5 or sem==6):
            tem=(datetime.date.today().year-2)
        if(sem==7 or sem==8):
            tem=(datetime.date.today().year-3)
        if(sem==9 or sem==10):
            tem=(datetime.date.today().year-4)
        sql="select frname,lname,reg_no from student where jy=%s and course=%s and branch=%s;"
        val=(tem,cours,branc)
        cur.execute(sql,val)
        cb=cur.fetchall()
        print(cb)
        return render_template("academics/atttendance.html",sem=sem,data=cb,lend=len(cb))
    
    @app.route("/addpa",methods=['POST'] )
    def pa():
        date=request.form['date']
        time=request.form['time']
        lenno=request.form['lenno']
        sem=request.form['sem']
        abbs=[]
        rns=[]
        for i in range(0,int(lenno)):
            semi="att["+str(i)+"]"
            att=request.form[semi]
            semio="rno["+str(i)+"]"
            rno=request.form[semio]
            sql="insert into ap(regno,ap,sem,date,time) value(%s,%s,%s,%s,%s)"
            val=(att,rno,sem,date,time)
            cur.execute(sql,val)
            if(att=='a'):
                abbs.append(att)
                rns.append(rno)
        conn.commit()
        return render_template('academics/viewatt.html',abbs=abbs,rns=rns,lena=len(abbs))

    @app.route("/ATt_set")
    def attset():
        st="maintemp/admin_main.html"
        return render_template(st,temp="/set_attt")
    @app.route("/set_attt")
    def add_atttser():
        b=['','08:00-09:00','09:00-10:00','10:00-11:00','11:00-12:00','12:00-13:00','13:00-14:00','14:00-15:00']
        a=['Monday','Tuesday','Wednesday','Thrusday','Friday','Saturday']
        return render_template("academics/ex.html",day=a,time=b)

class tt:
    @app.route("/Generate_tt")
    def tt():
        st="maintemp/admin_main.html"
        return render_template(st,temp="/Generate_ttt")
    @app.route("/Generate_ttt")
    def add_ttt():
        b=['','08:00-09:00','09:00-10:00','10:00-11:00','11:00-12:00','12:00-13:00','13:00-14:00','14:00-15:00']
        a=['Monday','Tuesday','Wednesday','Thrusday','Friday','Saturday']
        return render_template("academics/timetable.html",day=a,time=b)
    @app.route("/Tt_set")
    def ttset():
        st="maintemp/admin_main.html"
        return render_template(st,temp="/set_ttt")
    @app.route("/set_ttt")
    def add_tttser():
        b=['','08:00-09:00','09:00-10:00','10:00-11:00','11:00-12:00','12:00-13:00','13:00-14:00','14:00-15:00']
        a=['Monday','Tuesday','Wednesday','Thrusday','Friday','Saturday']
        return render_template("academics/timetableset.html",day=a,time=b)
    
class rms:
    @app.route("/AResult")
    def rsm():
        st="maintemp/admin_main.html"
        return render_template(st,temp="/rsm")
    @app.route("/rsm")
    def show_rsm(a=''):
        b=''
        if(a!=''):
            b=True
        st="maintemp/"+session['userrole']+"main.html"
        return render_template("result/rm.html",ab=a,b=b)
    @app.route("/rms",methods=['POST'])
    def show_rms():
        regno=request.form['Registration_Number']
        sql="select branch,course,frname,lname from student where reg_no=%s;"
        val=(regno,)
        cur.execute(sql,val)
        cb=cur.fetchall()
        print(cb)
        
        sql="select sem,id from coursereg where branch=%s and course_name=%s;"
        val=(cb[0][0],cb[0][1])
        cur.execute(sql,val)
        cf=cur.fetchall()
        print(cf)
        sem=int(cf[0][0])
        id=int(cf[0][1])
        return render_template("result/rms.html",a=sem,r=regno,idd=id)
    
    @app.route("/rmrs",methods=['POST'])
    def show_rmrs():
        
        sem=request.form['Registration_Number']
        regno=request.form['regno']
        idd=request.form['id']
        
        sql="select * from codereg where crid=%s and sem=%s;"
        val=(idd,sem)
        cur.execute(sql,val)
        cb=cur.fetchall()
        lencbb=(len(cb))
        print(cb)
        return render_template("result/rmrs.html",a=sem,r=regno,lencb=lencbb,sb=cb)
    @app.route("/addrmrs",methods=['POST'])
    def addrmrs():
        regno=request.form['reggno']
        sem=request.form['sem']
        cbkilen=request.form['cbkilen']
        mode=request.form['mode']
        for i in range(int(cbkilen)):
            summ="sb"+str(i)
            summm="sb"+str(i)+"n"
            a=request.form[summ]
            c=request.form[summm]
            print(a,c)
            sql="insert into result(regno,sem,subject,mode,marks) values(%s,%s,%s,%s,%s);"
            val=(regno,sem,a,mode,c)
            cur.execute(sql,val)
            conn.commit()
        k="Result Added Successfully"
        return rms.show_rsm(k)
class vrms:
    @app.route("/VResult")
    def vrsm():
        st="maintemp/admin_main.html"
        return render_template(st,temp="/vrsm")
    @app.route("/vrsm")
    def vshow_rsm(a=''):
        b=''
        if(a!=''):
            b=True
        st="maintemp/"+session['userrole']+"main.html"
        return render_template("result/vrm.html",ab=a,b=b)
    @app.route("/vrms",methods=['POST'])
    def vshow_rms():
        regno=request.form['Registration_Number']
        sql="select course,branch,frname,lname from student where reg_no=%s;"
        val=(regno,)
        cur.execute(sql,val)
        cb=cur.fetchall()
        print(cb)
        
        sql="select sem,id from coursereg where course_name=%s and branch=%s;"
        val=(cb[0][0],cb[0][1])
        cur.execute(sql,val)
        cf=cur.fetchall()
        print(cf)
        sem=int(cf[0][0])
        id=int(cf[0][1])
        return render_template("result/vrms.html",a=sem,r=regno,idd=id)

    
    @app.route("/vrmrs",methods=['POST'])
    def vshow_rmrs():
        
        sem=request.form['Registration_Number']
        regno=request.form['regno']
        idd=request.form['id']
        
        sql="select * from result where regno=%s and sem=%s;"
        val=(regno,sem)
        cur.execute(sql,val)
        cb=cur.fetchall()
        lencbb=(len(cb))
        print(cb)
        b=[]
        c=[]
        for i in cb:
            if i[3] in b:
                d=b.index(i[3])
                e=c[d]
                c.pop(d)
                c.insert(d,e+int(i[5]))
                print(e)
            else:
                b.append(i[3])
                c.append(int(i[5]))

        print(b,c)
        gg=len(b)
        return render_template("result/vrmrs.html",a=sem,r=regno,lenb=gg,b=b,c=c)
class Student:
    @app.route("/add_student")  
    def addStudent():
        st="maintemp/admin_main.html"
        return render_template(st,temp="/stu")

    @app.route("/stu")
    def add_stu():
        sql="select distinct branch,course_name from coursereg;"
        cur.execute(sql)
        cb=cur.fetchall()
        print(cb)
        conn.commit()
        return render_template('adduser/addstu_form.html',cblen=len(cb),cbb=cb)

    
class Placement:
    @app.route("/add_placement")  
    def addPlacement():
        st="maintemp/admin_main.html"
        return render_template(st,temp="/pla")

    @app.route("/pla")
    def add_pla():
        return render_template('adduser/addpla_form.html')

class Faculty:
    @app.route("/add_faculty")  
    def addFaculty():
        st="maintemp/admin_main.html"
        return render_template(st,temp="/fac")

    @app.route("/fac")
    def add_fac():
        return render_template('adduser/addfac_form.html')
        
class viewwuser:
    @app.route("/view_users")  
    def vu():
        st="maintemp/admin_main.html"
        return render_template(st,temp="/vuu")

    @app.route("/vuu")
    def show_vu():
        sql="select * from users;"
        cur.execute(sql)
        cb=cur.fetchall()
        print(cb)
        return render_template('adduser/viewuser.html',cblen=len(cb),cbb=cb)
class Warden:
    @app.route("/add_warden")  
    def addWarden():
        st="maintemp/admin_main.html"
        return render_template(st,temp="/war")
        
    @app.route("/war")
    def add_war():
        return render_template('adduser/addwar_form.html')

class Accounts:
    @app.route("/add_accounts")  
    def addAccounts():
        st="maintemp/admin_main.html"
        return render_template(st,temp="/acc")
        
    @app.route("/acc")
    def add_acc():
        return render_template('adduser/addacc_form.html')
class Transport:
    @app.route("/add_transport")    
    def addTransport():
        st="maintemp/admin_main.html"
        return render_template(st,temp="/tra")
        
    @app.route("/tra")
    def add_tra():
        return render_template('adduser/addtra_form.html')
class Library:
    @app.route("/addbook")  
    def addLibrary():
        st="maintemp/admin_main.html"
        return render_template(st,temp="/abook")
    @app.route("/abook")
    def addbook():
        sql1="select publication from book_publication;"
        cur.execute(sql1)
        datap=cur.fetchall()
        lendataA=len(datap)
        sql1="select author from book_author;"
        cur.execute(sql1)
        dataa=cur.fetchall()
        lendataB=len(dataa)
        return render_template('library/addbook.html',datapp=datap,dataaa=dataa,lendataAp=lendataA,lendataBa=lendataB)
    @app.route("/addbookk",methods=['POST'])
    def addbookk():
        bname=request.form['bname']
        bauthor=request.form['bauthor']
        bedition=request.form['bedition']
        bpublisher=request.form['bpublisher']
        stock=0
        issue=0
        sql1="select * from library;"
        cur.execute(sql1)
        data=cur.fetchall()
        code=(data[-1][-1]+1)
        sql="insert into library(bname,bauthor,bedition,bpublisher,book_stock,issue,code) values(%s,%s,%s,%s,%s,%s,%s);"
        val=(bname,bauthor,bedition,bpublisher,stock,issue,code)
        cur.execute(sql,val)
        conn.commit()
        return("Book Added Successfully and Book Number is "+str(code))
    @app.route("/viewbook")  
    def viewLibrary():
        st="maintemp/admin_main.html"
        return render_template(st,temp="/vbook")
    @app.route("/vbook")
    def viewbook():
        sql1="select publication from book_publication;"
        cur.execute(sql1)
        datap=cur.fetchall()
        lendataA=len(datap)
        sql1="select author from book_author;"
        cur.execute(sql1)
        dataa=cur.fetchall()
        lendataB=len(dataa)
        sql1="select bname,code from library;"
        cur.execute(sql1)
        bname=cur.fetchall()
        lenBname=len(dataa)
        return render_template('library/viewbook.html',datapp=datap,dataaa=dataa,bdata=bname,lenBnamep=lenBname,lendataAp=lendataA,lendataBa=lendataB)
    
    @app.route("/searchbook",methods=['POST'])
    def searchbook():
        bname=request.form['bname']
        bauthor=request.form['bauthor']
        bpublisher=request.form['bpublisher']
        bcode=request.form['bcode']
        print(len(bname),len(bauthor),len(bpublisher),len(bcode))
        c="select * from library "
        b="where "
        a=""
        e=0
        if(len(bname)!=0):
            e=1
            a=a+"bname = '"+bname+"' "
        if(len(bauthor)!=0):
            e=1
            a=a+"bauthor = '"+bauthor+"' "
        if(len(bpublisher)!=0):
            e=1
            a=a+"bpublisher = '"+bpublisher+"' "
        if(len(bcode)!=0):
            e=1
            a=a+"code = '"+bcode+"' "

        dd=""
        if(e==1):
            dd=(c+b+a+";")
        else:
            dd=(c+";")
        cur.execute(dd)
        data=cur.fetchall()
        print(data)
        return render_template("library/showbook.html",t=len(data),c=data)
    @app.route("/addauthor")  
    def addauthor():
        st="maintemp/admin_main.html"
        return render_template(st,temp="/aauthor")
    @app.route("/aauthor")
    def aauthor():
        sql1="select author from book_author;"
        cur.execute(sql1)
        data=cur.fetchall()
        print(data)
        lendataA=len(data)
        return render_template('library/bookauthor.html',dataa=data,lendata=lendataA)
    @app.route("/addingauthor",methods=['POST'])
    def addingauthor():
        bauthor=request.form['bauthor']
        sql="insert into book_author(author) values(%s);"
        val=(bauthor,)
        cur.execute(sql,val)
        conn.commit()
        return Library.aauthor()
    @app.route("/addpublisher")  
    def addpublisher():
        st="maintemp/admin_main.html"
        return render_template(st,temp="/apublisher")
    @app.route("/apublisher")
    def apublisher():
        sql1="select publication from book_publication;"
        cur.execute(sql1)
        data=cur.fetchall()
        print(data)
        lendataA=len(data)
        return render_template('library/bookpublisher.html',dataa=data,lendata=lendataA)
    @app.route("/addingpublisher",methods=['POST'])
    def addingpublisher():
        bauthor=request.form['bpublisher']
        sql="insert into book_publication(publication) values(%s);"
        val=(bauthor,)
        cur.execute(sql,val)
        conn.commit()
        return Library.apublisher()
    @app.route("/stockviewbook")  
    def stockviewLibrary():
        st="maintemp/admin_main.html"
        return render_template(st,temp="/stockvbook")
    @app.route("/stockvbook")
    def stockviewbook():
        return render_template('library/viewstock.html')
    @app.route("/stockaddbook")  
    def stockaddLibrary():
        st="maintemp/admin_main.html"
        return render_template(st,temp="/stockabook")
    @app.route("/stockabook")
    def stockaddbook():
        return render_template('library/addstock.html')
class add_sturoles:
    @app.route("/addsturole",methods=['POST'])
    def add_stu_role():
        f_n=request.form['f_n']
        l_n=request.form['l_n']
        date=request.form['date']
        fatn=request.form['fatn']  
        fatnum=request.form['fatnum']
        focc=request.form['focc']
        mname=request.form['mname']
        mnum=request.form['mnum']
        mocc=request.form['mocc']
        address=request.form['address']
        city=request.form['city']
        State=request.form['state']
        phno=request.form['phno']
        customRadio=request.form['customRadio']
        aano=request.form['aano']
        course=request.form['course']
        branch=request.form['branch']
        bg=request.form['bg']
        ten=request.form['ten']
        tenb=request.form['tenb']
        tw=request.form['tw']
        twb=request.form['twb']
        diploma=request.form['diploma']
        du=request.form['du']
        Bachelor=request.form['Bachelor']
        bu=request.form['bu']
        role=request.form['role']
        year=request.form['year']
        sql="select id from users;"
        cur.execute(sql)
        id=cur.fetchall()
        userid=role+"@"+f_n+l_n+str(id[-1][0]+1)
        sql="insert into parents(stuis,Fathername,father_occ,mothername,motherocc,mobno) values(%s,%s,%s,%s,%s,%s);"
        val=(userid,fatn,focc,mname,mocc,fatnum)
        cur.execute(sql,val)
        conn.commit()
        name=f_n+l_n
        rolec="Parent"
        sql="insert into users(name,user_id,passwd,role)values(%s,%s,%s,%s);"
        val=(name,fatnum,date,rolec)
        cur.execute(sql,val)
        conn.commit()
        
        sql="select idparents from parents where stuis=%s;"
        val=(userid,)
        cur.execute(sql,val)
        pid=cur.fetchall()
        parid=(pid[-1][0])
        sql="insert into student(frname,lname,dob,p_id,address,city,state,mob_no,gender,aadhar,course,branch,bg,reg_no,ten,tenb,tw,twb,dip,dm,bd,buc,jy) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        val=(f_n,l_n,date,parid,address,city,State,phno,customRadio,aano,course,branch,bg,userid,ten,tenb,tw,twb,diploma,du,Bachelor,bu,year)
        cur.execute(sql,val)
        conn.commit()
        pas=role+"@123"
        sql="insert into users(name,user_id,passwd,role)values(%s,%s,%s,%s);"
        val=(name,userid,pas,role)
        cur.execute(sql,val)
        conn.commit()
        return Student.add_stu()

class add_roles:
    @app.route("/addnewrole",methods=['POST'])
    def add_role():
        f_n=request.form['f_n']
        l_n=request.form['l_n']
        date=request.form['date']
        Qualification=request.form['Qualification']
        salary=request.form['salary']
        customRadio=request.form['customRadio']
        aano=request.form['aano']
        bg=request.form['bg']
        role=request.form['role']
        sql="select id from users;"
        cur.execute(sql)
        id=cur.fetchall()
        sql="insert into role(fname,lname,dob,qualification,salary,gender,aano,bg,role)values(%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        val=(f_n,l_n,date,Qualification,salary,customRadio,aano,bg,role)
        cur.execute(sql,val)
        userid=role+"@"+f_n+l_n+str(id[-1][0]+1)
        password=role+"@123"
        name=f_n+l_n
        sql="insert into users(name,user_id,passwd,role)values(%s,%s,%s,%s);"
        val=(name,userid,password,role)
        cur.execute(sql,val)
        conn.commit()
        if(role=="Warden"):
            return Warden.add_war()
        elif(role=="Placement"):
            return Placement.add_pla()
        elif(role=="Accounts"):
            return Accounts.add_acc()
        elif(role=="Transport"):
            return Transport.add_tra()
        elif(role=="Library"):
            return Library.add_lib()
        elif(role=="Faculty"):
            return Faculty.add_fac()

class view_notice:
    @app.route("/notice")
    def view_notice():
        st="maintemp/"+session['userrole']+"_main.html"
        return render_template(st,temp="/shownotice")
    @app.route("/shownotice")
    def show_notice():
        sql="select id,date,name,details,category,file from notice order by id desc;"
        cur.execute(sql)
        data=cur.fetchall()
        print(data)
        st="maintemp/"+session['userrole']+"main.html"
        return render_template("notice/viewnotice.html",t=len(data),c=data)

class addcourse:

    @app.route("/courseadd")
    def course():
        dst="maintemp/admin_main.html"
        return render_template(dst,temp="/coursevie")
        
    @app.route("/coursevie")
    def coursevie():
        return render_template('course/course.html')

    @app.route("/addcoursesem",methods=['POST'])
    def addcoursesem():
        coursename=request.form['cname']
        year=request.form['year']
        sem=request.form['sem']
        branchname=request.form['branchname']
        yff=request.form['yf']
        print(coursename,year,sem,branchname)
        sql="insert into coursereg(course_name,year,sem,branch,fess)values(%s,%s,%s,%s,%s);"
        val=(coursename,year,sem,branchname,yff)
        cur.execute(sql,val)
        conn.commit()
        sql="select id from coursereg where course_name=%s and year=%s and sem=%s and branch=%s and fess=%s;"
        val=(coursename,year,sem,branchname,yff)
        cur.execute(sql,val)
        ages=(cur.fetchall()[-1][0])
        dst="maintemp/admin_main.html"
        return render_template('course/coursesem.html',crid=ages,semm=int(sem))
    @app.route("/addnosem",methods=['POST'])
    def addcoursenosem():
        g=[]
        sem=request.form['sem']
        crid=request.form['cridd']
        seem=int(sem)
        for i in range(1,seem+1):
            semi="sem"+str(i)
            semi=request.form[semi]
            g.append(int(semi))
        print(crid)
        return render_template('course/courseseem.html',tg=g,slen=g,semm=seem,cridd=crid)
    @app.route("/addsubsem",methods=['POST'])
    def addcoursesubsem():
        tt=request.form['tt']
        crid=request.form['crid']
        print(crid)
        a=list(tt)
        print(a)
        b=[]
        for i in a:
            if(ord(i)>=48 and ord(i)<=57):
                b.append(i)
        for i in range(len(b)):
            for j in range(int(b[i])):
                semm="sem"+str(i+1)
                summ="sem"+str(i+1)+"sub"+str(j+1)
                a=request.form[semm]
                c=request.form[summ]
                sql="insert into codereg(crid,subject,sem) values(%s,%s,%s);"
                val=(crid,c,a)
                cur.execute(sql,val)
                conn.commit()

        return "hello"
    
class main():
    @app.route("/")
    def index():
        return render_template('welcomescreen.html')
    @app.route("/login")
    def login():
        return render_template('login.html',error="All Fields are Manodatry")
    @app.route('/addlogin',methods=['POST'])
    def hello_world():
        if(request.method=='POST'):
            a=request.form['userid']
            b=request.form['passcode']
            sql="select role,name,user_id from users where user_id=%s and passwd=%s;"
            val=a,b
            cur.execute(sql,val)
            gg=cur.fetchall()
            print(len(gg))
            if(len(gg)==1):
                print(gg)
                session['userid']=gg[0][2]
                session['user']=gg[0][1]
                session['userrole']=gg[0][0]
                print(session)
                st="maintemp/"+gg[0][0]+"_main.html"
                print(st)
                return render_template(st)
                    
            else:
                erro="The User Id and Password is Incorrect"
                return render_template('login.html',error=erro)
            
        return "Hello"

app.run(debug=True,host="0.0.0.0")