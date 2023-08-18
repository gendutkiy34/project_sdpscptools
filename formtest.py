from flask_wtf import FlaskForm
from wtforms import SubmitField,RadioField,DateField,SelectField,StringField,TextAreaField
from wtforms.validators import InputRequired,DataRequired

class FormMt(FlaskForm):
    sdpenv = SelectField('SDP ENVIRONTMENT',
                          choices=[('10.64.30.95:9480', 'SIT'), ('192.168.86.208:9003', 'PROD')],
                          validators=[DataRequired()])
    username = StringField('SYSTEM ID',validators=[DataRequired()])
    passw = StringField('PASSWORD',validators=[DataRequired()])
    sdc = StringField('SHORTCODE',validators=[DataRequired()])
    msisdn = StringField('MSISDN',validators=[DataRequired()])
    msg= TextAreaField('MESSAGE',validators=[DataRequired()])
    dt=DateField('DATE SEND',validators=[DataRequired()])
    submit=SubmitField('Submit')

class FormLog(FlaskForm):
    trxid = StringField('transaction id',validators=[DataRequired()])
    dt=DateField('DATE SEND',validators=[DataRequired()])
    logtype = RadioField('Environment', choices=[('sdp','SDP'),
                                                               ('scp','SCP')])
    submit=SubmitField('Submit')





