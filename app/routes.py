#from app import app
from app import app, db
from app.calc_vref import calc_vref
from flask import render_template, request, jsonify, redirect
from app.study import Study
from wtforms import StringField, DateTimeField, FloatField, IntegerField, validators, HiddenField, FieldList
from flask_wtf import FlaskForm

class StudyForm(FlaskForm):
    name     = StringField('Name', [validators.Required("Please enter study name")])
    date     = DateTimeField('Study Date')
    freq_1H  = IntegerField('1H Frequency', [validators.Required("Please enter 1H frequency after shimming")])
    vref_1H  = FloatField('1H Vref', [validators.Required("Please enter 1H Voltage referance after shimming")])
    freq_31P = IntegerField('31P Frequency', [validators.Required("Please enter 31P frequency after shimming")])
    vref_31P = FloatField('31P Vref')
    meas_arr = HiddenField('meas_arr')

@app.route('/')
def index():
    return redirect(request.base_url + "study?id=new")

@app.route('/study', methods=('GET', 'POST'))
def show_study():
    study_id = request.args.get('id')

    # check if existing study requested
    if (study_id == "new") or (study_id is None):
        study = Study()
    else:
        study = Study.query.get(int(study_id))
    # fetch if in DB

    form = StudyForm(obj=study)
    
    # validate form if POST
    if request.method == 'POST' and form.validate():
       form.populate_obj(study)
       db.session.add(study)
       db.session.commit()
       new_url = request.base_url + "?id=%d"%study.id
       return redirect(new_url)

    if study is not None:
        return render_template('study.html', study=study, form=form)
    else:
        return "Not found"

@app.route('/calc/vref', methods=('GET', 'POST'))
def get_vref():
    data = request.get_json()
    v = data['v']
    a = data['a']
    v_ref, fit_v, fit_a = calc_vref(v,a)
    return jsonify({'v_ref':v_ref, 'v': fit_v, 'a': fit_a })