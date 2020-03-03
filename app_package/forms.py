from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,IntegerField
from wtforms.validators import DataRequired,EqualTo
from app_package.model import User
class LoginForm(FlaskForm):
	username=StringField("Username",validators=[DataRequired()]) 
	password=PasswordField("Password",validators=[DataRequired()])
	remember_me=BooleanField("Remember Me")
	submit=SubmitField("Sign in")


def validate_username(self,username):
	user=User.query.filter_by(username=username.data).first()
	if user is not None:
		raise ValidationError("Username exists,choose another one")

class CreateAccountForm(FlaskForm):
	
	name=StringField("Name:",validators=[DataRequired()])
	accno=IntegerField("Accountnumber:",validators=[DataRequired()])
	bal=IntegerField("Balance:",validators=[DataRequired()])
	atype=StringField("Priority type:",validators=[DataRequired()])
	
	submit=SubmitField("Create account")

class DeleteAccountForm(FlaskForm):
	accno=IntegerField("Account number of the account",validators=[DataRequired()])
	submit=SubmitField("Delete account")

class DepositeMoneyForm(FlaskForm):
	
	accno=IntegerField("Accountnumber:",validators=[DataRequired()])
	amount=IntegerField("Amount to be deposited:",validators=[DataRequired()])
	submit=SubmitField("Deposite")

class WithdrawMoneyForm(FlaskForm):
	
	accno=IntegerField("Accountnumber:",validators=[DataRequired()])
	amount=IntegerField("Amount to be withdrawed:",validators=[DataRequired()])
	submit=SubmitField("Withdraw")

class DeleteConfirmForm(FlaskForm):
	accno=IntegerField("Account number of the account",validators=[DataRequired()])
	name=StringField("name")
	bal=IntegerField("Balance")
	submit=SubmitField("Confirm")
