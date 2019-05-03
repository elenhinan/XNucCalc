#from app import app
from app import app, db
from app.calc_vref import calc_vref
from flask import render_template, request, jsonify, redirect
from app.study import Study
from wtforms import StringField, DateTimeField, DecimalField, IntegerField, validators, HiddenField, FieldList
from flask_wtf import FlaskForm

class FlexibleDecimalField(DecimalField):
    def process_formdata(self, valuelist):
        if valuelist:
            valuelist[0] = valuelist[0].replace(",", ".")
        return super(FlexibleDecimalField, self).process_formdata(valuelist)

class StudyForm(FlaskForm):
    name     = StringField('Name', [validators.Required("Please enter study name")])
    date     = DateTimeField('Study Date')
    freq_1H  = IntegerField('1H Frequency', [validators.Required("Please enter 1H frequency after shimming")])
    vref_1H  = FlexibleDecimalField('1H Vref', [validators.Required("Please enter 1H Voltage referance after shimming")], places=1)
    freq_X   = IntegerField('X Frequency', [validators.Required("Please enter X frequency after shimming")])
    vref_X   = FlexibleDecimalField('X Vref', places=1)
    meas_arr = HiddenField('meas_arr')
    #deleted  = HiddenField('deleted')


@app.route('/')
def index():
    return redirect(request.base_url + "study?id=new")


@app.route('/list', methods=('GET', 'POST'))
def list_studies():
    # if get
    if request.method == 'POST':
        selected = request.form.getlist("selected")
        for study_id in selected:
            study = Study.query.get(int(study_id))
            db.session.delete(study)
        db.session.commit()
    
    studies = Study.query.order_by(Study.date).all()
    return render_template('list.html', studies=studies)


@app.route('/study', methods=('GET', 'POST'))
def show_study():
    study_id = request.args.get('id')

    # check if existing study requested
    if (study_id == "new") or (study_id is None):
        study = Study()
    else:
        study = Study.query.get(int(study_id))
        if study is None:
            return "Not found"

    # create form
    form = StudyForm(obj=study)
    
    # if POST and form validated
    if form.validate_on_submit():
        form.populate_obj(study)
        db.session.add(study)
        db.session.commit()
        new_url = request.base_url + "?id=%d"%study.id
        return redirect(new_url)

    return render_template('study.html', study=study, form=form)


@app.route('/calc/vref', methods=(['POST']))
def get_vref():
    data = request.get_json()
    v = data['v']
    a = data['a']
    v_ref, fit_v, fit_a = calc_vref(v,a)
    return jsonify({'v_ref':v_ref, 'v': fit_v, 'a': fit_a })

import sys
@app.route('/calc/trend', methods=(['POST']))
def get_trend():
    data = request.get_json()
    selected = data['selected']
    if len(selected):
        results = db.session.query(Study.id, Study.name, Study.vref_1H, Study.vref_X).filter(Study.id.in_(selected)).all()
        response = dict(zip(results[0]._asdict().keys(),[*zip(*results)]))
        return jsonify(response)
    return ""