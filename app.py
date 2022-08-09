from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from werkzeug.utils import redirect
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///yash.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Hostel(db.Model):
    sid=db.Column(db.Integer, primary_key=True)
    sname=db.Column(db.String(200), nullable=False)
    sbranch=db.Column(db.String(20))
    sroom=db.Column(db.String(5), nullable=False)
    sstatus=db.Column(db.String(10))
    stime=db.Column(db.DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return f"{self.sid} - {self.sname} - {self.sbranch} - {self.sroom} - {self.sstatus} - {self.stime}"

@app.route("/", methods=['GET','POST'])
def hello_world(): 
    if request.method=="POST":
        nid=(request.form['newid'])
        nname=(request.form['newname'])
        nroom=(request.form['newroom'])
        nbranch=(request.form['newbranch'])
        nstatus=(request.form['newstatus'])
        if nid!="":
           hostel = Hostel(sid=int(nid),sname=nname,sroom=nroom,sbranch=nbranch,sstatus=nstatus)
           db.session.add(hostel)
           db.session.commit()
    allhostel=Hostel.query.all()
    return render_template('index.html', allhostel=allhostel)
   

@app.route("/update/<int:sid>", methods=['GET','POST'])
def update(sid):
    if request.method=="POST":
        nid=(request.form['newid'])
        nname=(request.form['newname'])
        nroom=(request.form['newroom'])
        nbranch=(request.form['newbranch'])
        nstatus=(request.form['newstatus'])
        if nid!="":
           hostel = Hostel.query.filter_by(sid=sid).first()
           hostel.sid=nid
           hostel.sname=nname
           hostel.sroom=nroom
           hostel.sbranch=nbranch
           hostel.sstatus=nstatus
           hostel.stime=datetime.now()
           db.session.add(hostel)
           db.session.commit()     
           return redirect("/")

    hostel = Hostel.query.filter_by(sid=sid).first()



    return render_template('update.html', hostel=hostel)



@app.route("/delete/<int:sid>")
def delete(sid):
    hosteld = Hostel.query.filter_by(sid=sid).first()
    print(hosteld)
    db.session.delete(hosteld)
    db.session.commit()
    return redirect("/")



         

if __name__=="__main__":
    app.run(debug=True)
