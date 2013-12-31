from couchdb.design import ViewDefinition
from app.extensions import couchdbmanager
from flask import g
from flask.ext.login import current_user
from models import Messages
from app.models import User

class Social(object):
    def __init__(self):
        self.xmesg = ViewDefinition('docs', 'byauthor',
                                    'function(doc) { emit(doc.author, doc); }')
        couchdbmanager.add_viewdef(self.xmesg)

    def add(self, status):
        xmesg = Messages(user_id=current_user.id, organisation_id=current_user.organisation_id, \
                         displayname=current_user.displayname, status=status)
        xmesg.store(g.couch)

    def list(self):
        xmesg = []
        for msg in self.xmesg(g.couch):
            if msg.value.get('organisation_id') == current_user.organisation_id:
                xmesg.append(msg.value)
        return sorted(xmesg, reverse=True)
