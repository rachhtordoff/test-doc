from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, RadioField, DateTimeField, IntegerField, validators, TextField, SubmitField, FieldList, FormField, HiddenField
from wtforms.validators import DataRequired

class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class InitialSetup(Form):
    onetofour = RadioField('How many applicants?', choices=[(1,'One'),(2,'Two')])
    firsttime1 = RadioField('Are you a first time buyer?', choices=[(True,'Yes'),(False,'No')])
    firsttime2 = RadioField('Are you a first time buyer?', choices=[(True,'Yes'),(False,'No')])
    surname1 = StringField('Surname', validators=[DataRequired()])
    surname2 = StringField('Surname', validators=[DataRequired()])
    forenames1 = StringField('Forenames', validators=[DataRequired()])
    forenames2 = StringField('Forenames', validators=[DataRequired()])
    foundahouse = RadioField('Have you found a property?', choices=[('true','Yes'),('false','No')])
    submit = SubmitField('Submit')

class Addresses(Form):
    #address section
    id = HiddenField('Id')
    currentaddress = StringField('Current Address', validators=[DataRequired()])
    currentpostcode = StringField('Current Postcode', validators=[DataRequired()])
    currentdatemoved = DateTimeField('Date Moved To Address', format='%d/%m/%y', validators=[DataRequired()])
    status = RadioField('Residential Status', choices=[('owner', 'Owner'), ('tenant', 'Tenant'), ('parents', 'Living with parents')])

class AboutMe(Form):
    #basic section
    title = RadioField('Title', choices=[('mr', 'Mr'), ('miss', 'Miss'), ('mrs', 'Mrs'), ('ms', 'Ms')])
    surname = StringField('Surname', validators=[DataRequired()])
    forenames = StringField('Forenames', validators=[DataRequired()])
    dob = DateTimeField('Date Of Birth', format='%d/%m/%y', validators=[DataRequired()])
    gender = RadioField('Gender', choices=[('female', 'Female'), ('male', 'Male')])
    dateofmarriage = DateTimeField('Date Of Marriage', format='%d/%m/%y')
    maidenname = StringField('Maiden Name', validators=[DataRequired()])
    dependantname = StringField('Dependant Name', validators=[DataRequired()])
    dependantdob = DateTimeField('Dependant Date Of Birth', format='%d/%m/%y', validators=[DataRequired()])
    will = RadioField('Have you got a will?', choices=[('yes','Yes'),('no','No')])
    smoker = RadioField('Are you a smoker?', choices=[('yes','Yes'),('no','No')])
    #contact section
    home = IntegerField('Home', [validators.NumberRange(min=0, max=10)])
    work = IntegerField('Work', [validators.NumberRange(min=0, max=10)])
    mobile = IntegerField('Mobile', [validators.NumberRange(min=0, max=10)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    #job section
    jobtitle = StringField('Job Title', validators=[DataRequired()])
    employername = StringField('Name of Employer', validators=[DataRequired()])
    employeraddress = StringField('Employer Address', validators=[DataRequired()])
    employerpostcode = StringField('Employer Postcode', validators=[DataRequired()])
    startdate = DateTimeField('Start Date', format='%d/%m/%y', validators=[DataRequired()])
    basicwage = IntegerField('Basicwage', [validators.Length(min=2, max=6)])
    ot = IntegerField('Overtime')
    other = IntegerField('Other')
    selfemployedincome = IntegerField('Net Income')
    selfemployedyear = DateTimeField('Year', format='%d/%m/%y')
    retirementage = DateTimeField('Retirment Age', format='%d/%m/%y', validators=[DataRequired()])
    pensions = StringField('Pension Previsions', [validators.Length(min=2, max=35)])
    pensioncosts = IntegerField('Pension Monthly Costs', [validators.Length(min=2, max=35)])
    sickpay = RadioField('Are you paid if off sick?', choices=[('yes','Yes'),('no','No')])
    sickpaydetails = StringField('Sick Pay Details')
    additionaldetails = StringField('Additional Income')
    #subforms
    addresses = FieldList(FormField(Addresses))


class FinanceDetails(Form):
    #current mortgages
    currentmortgagelender= StringField('Current Mortgage Lender', validators=[DataRequired()])
    named = RadioField('Is this application joint?', choices=[('yes','Yes'),('no','No')])
    accountno = IntegerField('Account Number', [validators.Length(min=6, max=6)])
    monthlypayments = IntegerField('Monthly Payments', [validators.Length(min=1, max=8)])
    amountoutstanding = IntegerField('Amount Outstanding', [validators.Length(min=1, max=8)])
    rate = IntegerField('Rate', [validators.Length(min=1, max=8)])
    dealenddate = DateTimeField('Year', format='%d/%m/%y', validators=[DataRequired()])
    #current debts
    debtlender= StringField('Debt Lender', validators=[DataRequired()])
    debtnamed = RadioField('Is this debt joint?', choices=[('yes','Yes'),('no','No')])
    repaidmortgage = RadioField('Is this debt repaid with mortgage?', choices=[('yes','Yes'),('no','No')])
    #other
    assets1 = StringField('Savings and Investments', [validators.Length(min=0, max=35)])
    assets2 = StringField('Life protection', [validators.Length(min=0, max=35)])
    creditissues = StringField('Credit Issues', [validators.Length(min=0, max=35)])

class PropertyDetails(Form):
    #Property Details
    propertyaddress =  StringField('Property Address', validators=[DataRequired()])
    bedrooms = IntegerField('Bedrooms', [validators.Length(min=1, max=15)])
    bathrooms = IntegerField('Bathrooms', [validators.Length(min=1, max=8)])
    garage = RadioField('Garage', choices=[('yes','Yes'),('no','No')])
    parking = RadioField('Parking', choices=[('yes','Yes'),('no','No')])
    yearofbuild = DateTimeField('Year', format='%d/%m/%y', validators=[DataRequired()])
    propertytype = RadioField('Property Type', choices=[('det','Detached'),('semi','Semi-detached'),('terr','Terranced'),('flat','Flat')])
    freeholdorleasehold = RadioField('Freehold or Leasehold?', choices=[('freeholder','Freeholder'),('leasehold','Leasehold')])
    leaseend = DateTimeField('Lease end date', format='%d/%m/%y', validators=[DataRequired()])
    servicecharge = IntegerField('Service Charge', [validators.Length(min=1, max=15)])
    groundrent = IntegerField('Grount Rent', [validators.Length(min=1, max=15)])
    cashprice = IntegerField('Cash Price', [validators.Length(min=1, max=15)])
    idealpaymentdate = DateTimeField('Ideal Payment Date', format='%d/%m/%y', validators=[DataRequired()])
    #solicitor Details
    solicitorname = StringField('Solicitor Name', validators=[DataRequired()])
    solicitorfirm = StringField('Solicitor Firm Name', validators=[DataRequired()])
    solicitoraddress = StringField('Solicitor Address', validators=[DataRequired()])
    solicitorphone = IntegerField('Solicitor Number', [validators.Length(min=11, max=15)])
    #agents detaisl
    agentname = StringField('Agent Name', validators=[DataRequired()])
    agentfirmname= StringField('Agent Firm Name', validators=[DataRequired()])
    agentaddress = StringField('Agent Address', validators=[DataRequired()])
    agentphone = IntegerField('Agent Number', [validators.Length(min=11, max=15)])
    #costing Details
    sellprice = IntegerField('Sell Price', [validators.Length(min=2, max=10)])
    monthlybudget = IntegerField('Monthly Budget', [validators.Length(min=2, max=5)])
    EstateAgencyfees = IntegerField('Estate Agency Fees', [validators.Length(min=2, max=5)])
    Solicitorfees = IntegerField('Solicitor Fees', [validators.Length(min=2, max=5)])
    notes = TextField('Additional Notes', [validators.Length(min=0, max=35)])
