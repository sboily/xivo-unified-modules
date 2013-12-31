from couchdb.mapping import Document, TextField, IntegerField, DateTimeField
from datetime import datetime

class Messages(Document):
    doc_type = 'messages'

    user_id = IntegerField()
    displayname = TextField()
    organisation_id = IntegerField()
    status = TextField()
    like = IntegerField()
    added = DateTimeField(default=datetime.now)
