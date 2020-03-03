from flask import render_template, flash, redirect, url_for
from app_package import app, db,mongo
from flask_login import current_user, login_user, logout_user, login_required
from app_package.forms import LoginForm,CreateAccountForm,DeleteAccountForm,DepositeMoneyForm,WithdrawMoneyForm,DeleteConfirmForm
from app_package.model import User
b_id=0
@app.route("/", methods=["GET","POST"])
def index():
    if current_user.is_authenticated:
        return redirect(url_for("menu"))
    else:
        form=LoginForm()
        if form.validate_on_submit():
            user=User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash("Invalid User")
                return redirect(url_for("index"))
            else:
                login_user(user,remember=form.remember_me.data)#like session login_user is an builtin fn 
                return redirect(url_for("menu"))
        else:        
            return render_template("login.html",form=form)
       

@app.route("/menu")  
@login_required
def menu():
      return render_template("menu.html")
     
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index")) 
@app.route("/newaccount",methods=["GET","POST"])
@login_required
def newaccount():
	global b_id
	form=CreateAccountForm()
	if form.validate_on_submit():
		fields=["_id","accno","name","bal","credit","debit","atype"]
		b_id+=1
		credit=0
		debit=0
		
		values=[b_id,form.accno.data,form.name.data,form.bal.data,credit,debit,form.atype.data]
		bank=dict(zip(fields,values))
		bank_col=mongo.db.bank #employees database created
		tmp=bank_col.insert_one(bank)		
		if tmp.inserted_id==b_id:
			flash("account created")
			
			return redirect(url_for("menu"))
		else:
			flash("Problem adding employees")
			return redirect(url_for("logout"))
	else:
		return render_template("new_account.html",form=form)

@app.route("/display_details")
@login_required
def display_details():
	bank_col=mongo.db.bank
	bank=bank_col.find()
	return render_template("display_details.html",bank=bank)

@app.route("/deposite_money",methods=["GET","POST"])
@login_required
def deposite_money():
	form=DepositeMoneyForm()
	if form.validate_on_submit():
		values=dict()
		if form.accno.data!="":values["accno"]=form.accno.data
		if form.amount.data!="":values["credit"]=form.amount.data	
		query={"accno":form.accno.data}
		bank_col=mongo.db.bank
		bank=bank_col.find_one(query)
		d=bank["bal"]
		values["bal"]=d+form.amount.data
		new_data={"$set":values}
		bank_col.update_one(query,new_data)
		flash("cash deposited,balance updated")
		return redirect(url_for("menu"))
	else:
		return render_template("deposite_money.html",form=form)


@app.route("/withdraw_money",methods=["GET","POST"])
@login_required
def withdraw_money():
	form=WithdrawMoneyForm()
	if form.validate_on_submit():
		values=dict()
		if form.accno.data!="":values["accno"]=form.accno.data
		if form.amount.data!="":values["debit"]=form.amount.data	
		query={"accno":form.accno.data}
		bank_col=mongo.db.bank
		bank=bank_col.find_one(query)
		d=bank["bal"]
		p=bank["atype"]
		values["bal"]=d-form.amount.data
		if p=="ordinary" and values["bal"]<10000:
			flash("Below minimum balance,cant withdraw")
			return redirect(url_for("menu"))
		elif  p=="priority" and values["bal"]<50000:                                         
			flash("Below minimum balance,cant withdraw")
			return redirect(url_for("menu"))
		else:
			new_data={"$set":values}
			bank_col.update_one(query,new_data)
			flash("cash withdrawed,balance reducted")
			return redirect(url_for("menu"))
	else:
		return render_template("withdraw.html",form=form)
@app.route("/deleteaccount",methods=["GET","POST"])
@login_required
def deleteaccount():
	form=DeleteAccountForm()
	f2=DeleteConfirmForm()
	if form.validate_on_submit():
		bank_col=mongo.db.bank
		query={"accno":form.accno.data}
		bank=bank_col.find(query)
		return render_template("confirm.html",f2=f2,bank=bank)  
		
	else:
		return render_template("delete_account.html",form=form)
@app.route("/confirm",methods=["GET","POST"])
def confirm():
	f2=DeleteConfirmForm()
	if f2.validate_on_submit():
		bank_col=mongo.db.bank
		query={"accno":f2.accno.data}
		bank_col.delete_one(query)
		flash("Customer deleted")
		return redirect(url_for("menu"))
	else:
		return render_template("confirm.html",f2=f2)
	

