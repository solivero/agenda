from agenda import db

groupmembers = db.Table('groupmembers',
    db.Column('person_id', db.Integer, db.ForeignKey('person.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('workgroup.id'))
)

evenmembers = db.Table('eventmembers',
    db.Column('person_id', db.Integer, db.ForeignKey('person.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)

class Workgroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    persons = db.relationship('Person', secondary=groupmembers,
        backref=db.backref('groups'))

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    date = db.Column(db.DateTime)
    material = db.Column(db.String(255))
    catergory = db.Column(db.String(50))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    icon = db.Column(db.String(40)) ##URI for bootstrap glyphs