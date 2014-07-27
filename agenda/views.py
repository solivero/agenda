# -*- coding: utf-8 -*-
from agenda import app, db
from flask import render_template, flash, redirect, url_for, request, g
from .models import Person, Workgroup, Event, Tag
from .forms import Group, EditGroup, NewEvent


@app.before_request
def before_request():
    g.persons = [(p.id, p.name) for p in Person.query.all()]


@app.route('/')
def index():
    name = ''
    if request.args.get('person'):
        person = Person.query.get(request.args.get('person'))
        if person:
            name = person.name
    return render_template('index.html', name=name)


@app.route('/events/', methods=["GET", "POST"])
def events():
    form = NewEvent()
    form.groups.choices = [(g.id, g.name) for g in Workgroup.query.all()]
    if request.method == "POST":
        print request.form
        if form.validate_on_submit():
            event = Event(
                name=form.name.data,
                info=form.info.data,
                date=form.date.data,
                material=form.material.data
                )
            for id in form.groups.data:
                event.groups.append(Workgroup.query.get(id))
            db.session.add(event)
            db.session.commit()
            tags = [tag.strip().lower() for tag in form.tags.data.split(',')]
            for tag in tags:
                db_tag = Tag.query.filter_by(name=tag).first()
                if not db_tag:
                    db_tag = Tag(name=tag)
                db_tag.events.append(event)
                db.session.add(db_tag)
            db.session.commit()
            flash(u"Ny händelse skapad!", 'success')
        else:
            flash(
                u'Kunde inte skapa grupp. Se hjälpmeddelanden', 'danger')
    return render_template('events.html', form=form, events=Event.query.all())


@app.route('/persons')
def persons():
    return render_template('list.html', persons=Person.query.all())


@app.route('/groups/', methods=["GET", "POST"])
def groups():
    form = Group()
    if request.method == "POST":
        if form.validate_on_submit():
            group = Workgroup(name=form.name.data)
            for id in form.persons.data:
                group.persons.append(Person.query.get(id))
            db.session.add(group)
            db.session.commit()
            flash('Ny grupp skapad!', 'success')
        else:
            flash(
                u'Kunde inte skapa grupp. Se hjälpmeddelanden', 'danger')
    return render_template('groups.html',
                           form=form, groups=Workgroup.query.all())


@app.route('/groups/<string:group_name>', methods=["GET", "POST"])
def edit_group(group_name):
    group = Workgroup.query.filter_by(name=group_name).first()
    form = EditGroup()
    if request.method == "POST":
        print request.form
        if 'add' in request.form:
            group.persons.append(Person.query.get(form.person.data))
            db.session.add(group)
            db.session.commit()
            flash(Person.query.get(form.person.data).name +
                  u" är tillagd i gruppen", "success")
        if 'delete' in request.form:
            db.session.delete(group)
            db.session.commit()
            flash('Grupp borttagen', 'success')
            return redirect(url_for('groups'))
        if 'remove' in request.form:
            group.persons.remove(
                Person.query.filter_by(name=request.form['remove']).first())
            db.session.add(group)
            db.session.commit()
    return render_template('edit_group.html', group=group, form=form)
