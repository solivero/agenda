# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms.fields import TextField, SelectMultipleField, SelectField, \
    SubmitField, DateField, TextAreaField
from wtforms.validators import Required, Length, ValidationError
from models import Person, Workgroup, Event


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
    name = TextField(label="Gruppens namn", validators=[Required(), Length(
        min=3, max=30),
        Unique(Workgroup, Workgroup.name, message="Gruppen finns redan")])
    persons = SelectMultipleField(
        u'Gruppens medlemmar',
        coerce=int,
        validators=[Required()])
    submit = SubmitField()


class EditGroup(Form):
    person = SelectField(
        u"Välj klasskamrat",
        coerce=int)
    add = SubmitField()
    delete = SubmitField()


class NewEvent(Form):
    name = TextField(
        "Namn",
        validators=[
            Required(),
            Length(min=3, max=30),
            Unique(
                Event,
                Event.name,
                message=u"Händelsen finns redan"
                )
        ])
    info = TextAreaField("Info")
    date = DateField("Datum", validators=[Required()])
    groups = SelectMultipleField(
        u"Grupper som är delaktiga i händelsen",
        coerce=int,
        validators=[Required()])
    material = TextAreaField(
        'Material', description=u"Länkar till användbart material med mera")
    tags = TextField('Taggar', description=u"""Skriv gärna ämne eller liknande.
         Separera med kommatecken""")