from agenda import db

groupmembers = db.Table(
    'groupmembers',
    db.Column(
        'person_id',
        db.Integer,
        db.ForeignKey('person.id')),
    db.Column(
        'group_id',
        db.Integer,
        db.ForeignKey('workgroup.id'))
    )

eventgroups = db.Table(
    'eventgroups',
    db.Column(
        'workgroup_id',
        db.Integer,
        db.ForeignKey('workgroup.id')),
    db.Column(
        'event_id',
        db.Integer,
        db.ForeignKey('event.id'))
    )

eventtags = db.Table(
    'eventtags',
    db.Column(
        'tag_id',
        db.Integer,
        db.ForeignKey('tag.id')),
    db.Column(
        'event_id',
        db.Integer,
        db.ForeignKey('event.id'))
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
    name = db.Column(db.String(255))
    info = db.Column(db.String(255))
    date = db.Column(db.DateTime)
    material = db.Column(db.String(255))
    groups = db.relationship('Workgroup', secondary=eventgroups,
                             backref=db.backref('events'))


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    events = db.relationship('Event', secondary=eventtags,
                             backref=db.backref('tags'))
