from sys import argv
from agenda import app, db
from agenda.models import Person

commands = ['run', 'initdb', 'persons']
if len(argv) == 1:
    for command in commands:
        print command
else:
    if argv[1] == "run":
        app.run()

    elif argv[1] == "initdb":
        print "Database Reset"
        db.drop_all()
        db.create_all()

    elif argv[1] == "persons":
        f = open("namn.txt")
        for name in f.readlines():
            p = Person(name=unicode(name[:-1], encoding="utf8"))
            db.session.add(p)
        db.session.commit()
    else:
        print "Unknown command"
        for command in commands:
            print command
