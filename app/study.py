from datetime import datetime
import json
from app import db

class Study(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(40), nullable=False)
    date     = db.Column(db.DateTime, nullable=False)
    freq_1H  = db.Column(db.Integer, nullable=True)
    vref_1H  = db.Column(db.Float, nullable=True)
    freq_X = db.Column(db.Integer, nullable=False)
    vref_X = db.Column(db.Float, nullable=False)
    meas_arr = db.Column(db.String(80), nullable=False)
    #deleted = db.Column(db.Boolean, nullable=False)

    def __init__(self, **kwargs):
        super(Study, self,).__init__(**kwargs)
        self.date = datetime.now()
        #self.deleted = False
        self.set_measurements([[60, 100, 140, 180, 220], [0, 0, 0, 0, 0]])

    def set_measurements(self,measurements):
        self.meas_arr = json.dumps(measurements)
    
    def get_measurements(self,):
        return json.loads(self.meas_arr)


    def __repr__(self):
        return '<Study %r>' % self.name

db.create_all()