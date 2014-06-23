from agenda import app, db
from flask import render_template, flash, redirect, url_for, request, g
from .models import Person, Workgroup
from .forms import Group, EditGroup, Event

@app.before_request
def before_request():
    g.persons = [(p.id, p.name) for p in Person.query.all()]

@app.route('/')
def index():
    name = ''
    if request.args.get('person'):
        person = Person.query.get(request.args.get('person'))
        if person:
            name=person.name
    return render_template('index.html', name=name)

@app.route('/events/')
def events():
    form = Event()
    return render_template('new_event.html', form=form)

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
            flash(u'Kunde inte skapa grupp. Se hj\u00E4lpmeddelanden', 'danger')
    return render_template('groups.html', form=form, groups=Workgroup.query.all())

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
            flash(Person.query.get(form.person.data).name + u" \u00E4r tillagd i gruppen", "success")
        if 'delete' in request.form:
            db.session.delete(group)
            db.session.commit()
            flash('Grupp borttagen', 'success')
            return redirect(url_for('groups'))
        if 'remove' in request.form:
            group.persons.remove(Person.query.filter_by(name=request.form['remove']).first())
            db.session.add(group)
            db.session.commit()
    return render_template('edit_group.html', group=group, form=form)
