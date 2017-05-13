from wtforms.validators import DataRequired, Length
from wtforms import Form, TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField

class InputData(Form):
	nim = TextField("Nim:", validators=[validators.required()])
	nama = TextField("Nama:",validators=[validators.required()])
	jurusan = TextField("jurusan")



class LoginAdminForm(Form):
	username = TextField("Username", [validators.Required("Masukan username")])
	password = PasswordField("Passowrd", [validators.Required("Masukan Password")])
	submit = SubmitField("Login")


	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False

		user = User.objects(User.username == self.username)
		if user and user.filter(password = self.password):
			return True
		else:
			return False
class Input(Form):

	"""docstring for Input"""

	def __init__(self, arg):
		super(Input, self).__init__()

		self.arg = arg
		


	