from flask import Flask, jsonify, request
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('notes',
                        user='mbp',
                        password='12345',
                        host='localhost',
                        port=5432)


class BaseModel(Model):
    class Meta:
        database = db


class Note(BaseModel):
    title = CharField()
    date = DateField()
    description = CharField()


db.connect()
db.drop_tables([Note])
db.create_tables([Note])

Note(title='grocery',
     date=datetime.date(2022, 4, 25),
     description='get apples'
     ).save()
Note(title='homework',
     date=datetime.date(2022, 4, 26),
     description='finish project 6'
     ).save()
Note(title='dutues',
     date=datetime.date(2022, 4, 28),
     description='do laundry'
     ).save()

app = Flask(__name__)


@app.route('/note/', methods=['GET', 'POST'])
@app.route('/note/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None
             ):
    if request.method == 'GET':
        if id:
            return jsonify(model_to_dict(Note.get(Note.id == id)))
        else:
            noteList = []
            for note in Note.select():
                noteList.append(model_to_dict(note))
            return jsonify(noteList)

    if request.method == 'PUT':
        update_note = request.get_json()
        query = Note.update(update_note).where(Note.id == id)
        query.execute()
        return 'UPDATE request'

    if request.method == 'POST':
        new_note = dict_to_model(Note, request.get_json())
        new_note.save()
        return jsonify({"success": True})

    if request.method == 'DELETE':
        note = Note.get(Note.id == id)
        note.delete_instance()
        return 'DELETE request'



app.run(debug=True, port=9000)
