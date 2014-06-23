from flask_wtf import Form
from wtforms.fields import TextField, DateField, SelectMultipleField, SelectField, SubmitField, DateTimeField, TextAreaField
from wtforms.validators import Required, Length, ValidationError
from models import Person, Workgroup

class Unique(object):
    """ validator that checks field uniqueness """
    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        if not message:
            message = u'This element already exists'
        self.message = message

    def __call__(self, form, field):        
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)


class Group(Form):
    name = TextField(label="Gruppens namn", validators=[Required(), Length(min=3, max=30), Unique(Workgroup, Workgroup.name, message="Gruppen finns redan")])
    persons = SelectMultipleField(u'Gruppens medlemmar', choices=[(p.id, p.name) for p in Person.query.all()], coerce=int, validators=[Required()])
    submit = SubmitField()

class EditGroup(Form):
    person = SelectField(u"V\u00E4lj klasskamrat", choices=[(p.id, p.name) for p in Person.query.all()], coerce=int)
    add = SubmitField()
    delete = SubmitField()

class Event(Form):
    title = TextField(u"Namn", validators=[Required(), Length(min=3, max=30)])
    datetime = DateTimeField()
    material = TextAreaField('Material')
    category = TextField('Kategorier')