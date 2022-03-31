import os
import csv
from flask import render_template,request,redirect,url_for
from flask import current_app as app
from .database import db
from .models import Users,Tasks,Trackers
from flask_login import login_user,logout_user,current_user,login_required
from datetime import datetime
import matplotlib.pyplot as plt

type={1:'multiple',2:'boolean',3:'numerical'}

this_path=os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    if(request.method=='POST'):
        username=request.form['username']
        password=request.form['password']
        user=Users.query.filter_by(username=username).first()
        if (user!=None) and (user.password==password):
            login_user(user=user,remember=True)
            return redirect(f'/dashboard/{user.user_id}')
        else:
            return render_template('login.html',warning=1)
    return render_template('login.html',warning=None)
        

@app.route('/register',methods=['GET','POST'])
def register():
    if(request.method=='POST'):
        username=request.form['username']
        pass1=request.form['pass1']
        pass2=request.form['pass2']
        user_exist=Users.query.filter_by(username=username).first()
        if (user_exist==None) and (pass1==pass2):
            new_user=Users(username=username,password=pass1,u_timestamp=datetime.now())
            db.session.add(new_user)
            db.session.commit()
            login_user(user=new_user, remember=True)
            return redirect(f'/dashboard/{new_user.user_id}')
        elif (pass1!=pass2):
            return render_template('register.html',warning='pass')
        elif (user_exist!=None):
            return render_template('register.html',warning='username')
    return render_template('register.html',warning=None)

@app.route('/dashboard/<int:user_id>')
@login_required
def dashboard(user_id):
    user=current_user
    using=Tasks.query.filter_by(tuser_id=user_id).all()
    l=[]
    for i in using:
        if i.ttracker_id in l:
            pass
        else:
            l.append(i.ttracker_id)
    rows=[]
    for i in l:
        tasksp=Tasks.query.filter_by(ttracker_id=i).all()
        t_type=Trackers.query.get(i).type
        if t_type=='multiple':
            f=open('multiple.csv','r')
            r=f.readline().split(',')
            while(r!=''):
                r=f.readline().split(',')
                if int(r[0])==int(i):
                    choices=[r[1],r[2],r[3],r[4]]
                    break
                else:
                    pass
            fory=[0,0,0,0]
            for j in tasksp:
                if(j.value=='choice1'):
                    fory[0]+=1
                if(j.value=='choice2'):
                    fory[1]+=1
                if(j.value=='choice3'):
                    fory[2]+=1
                if(j.value=='choice4'):
                    fory[3]+=1
            fig=plt.figure(figsize=(10,5))
            plt.bar(choices,fory,color='maroon',width=0.4)
            plt.xlabel('Choices')
            plt.ylabel('Number of times clicked')
            plt.savefig(os.path.join(this_path,f'../static/{user_id}_{i}'))
            f.close()
        elif t_type=='numerical':
            forx=[]
            fory=[]
            for j in tasksp:
                forx.append(j.ttimestamp.date())
                fory.append(int(j.value))
            fig=plt.figure(figsize=(10,5))
            plt.plot(forx,fory)
            plt.xlabel('Timestamp')
            plt.ylabel('Value')
            plt.savefig(os.path.join(this_path,f'../static/{user_id}_{i}'))
        elif t_type=='boolean':
            forx=['Yes','No']
            fory=[0,0]
            for j in tasksp:
                if j.value=='yes':
                    fory[0]+=1
                else:
                    fory[0]+=1
            fig=plt.figure(figsize=(10,5))
            plt.bar(choices,fory,color='maroon',width=0.4)
            plt.xlabel('Choices')
            plt.ylabel('Number of times clicked')
            plt.savefig(os.path.join(this_path,f'../static/{user_id}_{i}'))
        rows.append([Trackers.query.get(i).tracker_name,i,])
    return render_template('dashboard.html',user=user,rows=rows,n=len(rows))

@app.route('/alltrackers')
@login_required
def allTrackers(user=current_user):
    info=Trackers.query.all()
    rows=[]
    for i in info:
        u=Users.query.get(i.creator_id)    
        rows.append([i.tracker_name,i.type,u.username,i.no_users,i.tracker_id])
    d=len(rows)
    return render_template('all.html',d=d,rows=rows,user=user)

@app.route('/logout/<int:user_id>')
@login_required
def logout(user_id):
    logout_user()
    return redirect(url_for('login'))

@app.route('/newTracker',methods=['GET','POST'])
@login_required
def newTracker(user=current_user):
    if request.method=='POST':
        type=request.form['type']
        tracker_name=request.form['tracker_name']
        description=request.form['description']
        t_exist=Trackers.query.filter_by(tracker_name=tracker_name).first()
        if(t_exist!=None):
            return render_template('newtracker.html',user=user,warning=1)
        new_tracker=Trackers(tracker_name=tracker_name,creator_id=user.user_id,timestamp=datetime.now(),description=description,type=type)
        db.session.add(new_tracker)
        db.session.commit()
        if(type=="multiple") and (t_exist==None):
            n_tracker=Trackers.query.filter_by(tracker_name=tracker_name).first()
            choice1=request.form['choice1']
            choice2=request.form['choice2']
            choice3=request.form['choice3']
            choice4=request.form['choice4']
            with open('multiple.csv','a',newline='') as f:
                writer=csv.writer(f)
                writer.writerow([n_tracker.tracker_id,choice1,choice2,choice3,choice4])
            return redirect(f'/alltrackers')
        elif(type=="boolean"):
            return redirect(f'/alltrackers')
        elif(type=="numerical"):
            return redirect(f'/alltrackers')
    return render_template('newtracker.html',user=user,warning=None)

@app.route('/feedback',methods=['GET','POST'])
@login_required
def feedback(user=current_user):
    if request.method=='POST':
        text=request.form['feedback']
        f=open('feedback.txt','a')
        f.write(str(user.username)+'\n'+str(datetime)+'\n'+text+'\n\n\n')
        return redirect(f'/dashboard/{user.user_id}')
    return render_template('feedback.html',user=user)

@app.route('/trackerinfo/<int:t_id>')
@login_required
def t_info(t_id,user=current_user):
    tracker=Trackers.query.get(t_id)
    creator=Users.query.get(tracker.creator_id)
    return render_template('t_info.html',user=user,tracker=tracker,creator_n=creator.username)

@app.route('/log/<int:t_id>',methods=['GET','POST'])
@login_required
def log(t_id,user=current_user):
    tracker=Trackers.query.get(t_id)
    if(request.method=='POST'):
        tasksrc=Tasks.query.filter_by(tuser_id=user.user_id).first()
        if tasksrc==None:
            no=tracker.no_users
            tracker.no_users=no+1
        value=request.form['value']
        dt=request.form['datetime']
        note=request.form['note']
        # 2022-03-18T02:06
        time_obj=datetime(year=int(dt[0:4]),month=int(dt[5:7]),day=int(dt[8:10]),hour=int(dt[11:13]),minute=int(dt[14:16]), second=30, microsecond=4548, tzinfo=None)
        new_task=Tasks(ttimestamp=time_obj,ttracker_id=t_id,tuser_id=user.user_id,note=note,value=value)
        db.session.add(new_task)
        db.session.commit()
        return redirect(f'/dashboard/{user.user_id}')
    if(tracker.type=="multiple"):
        with open('multiple.csv','r') as f:
            row = f.readline().split(",")
            while(row!=""):
                row=f.readline().split(",")
                if(int(row[0])==t_id):
                    break
        return render_template('log.html',user=user,tracker=tracker,choices=row)
    return render_template('log.html',user=user,tracker=tracker)

@app.route('/detailedinfo/<int:t_id>')
@login_required
def deets(t_id):
    user=current_user
    tracker=Trackers.query.get(t_id)
    by=Users.query.get(user.user_id)
    taskl=Tasks.query.filter_by(ttracker_id=t_id).all()
    rows=[]
    for i in taskl:
        rows.append([i.ttimestamp.date(),i.ttimestamp.time(),i.value,i.note])
    return render_template('deets.html',tracker=tracker,by=by.username,rows=rows,user=user,n=len(rows))