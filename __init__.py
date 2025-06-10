import flask
from flask_wtf import FlaskForm
from wtforms import TextAreaField
from flask_wtf.file import MultipleFileField, FileAllowed, FileRequired
from wtforms import SubmitField
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
import os
import datetime
import json

app = flask.Flask(__name__)

app.config.from_mapping(
    SECRET_KEY='dev')

app.jinja_env.globals.update(reversed=reversed) # Not crucial, but it's nice to have newer stuff on top of the page

approved_jobs_file = "static/job_data.json" # TODO: allow admin to manage jobs

@app.route('/')
def index():
    return flask.render_template('index.html', title='Home')

@app.route('/jobs/')
def list():
    job_list = load_json(approved_jobs_file)
    return job_list

@app.route('/3dprint/submit/', methods=['GET', 'POST'])
def submit_jobs():
    job_data_path = "static/job_data.json"
    class PrintForm(FlaskForm):
        user = TextAreaField('Your user name')
        description = TextAreaField('Describe your print job.')
        files = MultipleFileField(validators=[
            FileRequired(),
            FileAllowed(['stl'], 'Only .stl files!')])
        submit = SubmitField('Upload')
    
    form = PrintForm(CombinedMultiDict((flask.request.files, flask.request.form)))
    basedir = os.path.abspath(os.path.dirname(__file__))
    if form.validate_on_submit():
        for f in form.files.data:
            old_filename = secure_filename(f.filename)
            datestring = ''.join(str(datetime.datetime.now()).split()).split('.')[0]
            new_filename = datestring + "_" + old_filename
            file_path = os.path.join(
                basedir, 'static', new_filename
            )
            f.save(file_path)
            new_job = {
                "approved" : False,
                "date" : str(datetime.datetime.now()),
                "user" : form.user.data,
                "description" : form.description.data,
                "filename" : new_filename
            }
            job_list = load_json(job_data_path)
            job_list.append(new_job)
            save_json(job_list, job_data_path)

        return flask.render_template('submit_jobs.html', title='Submit 3D print jobs', form=form, message = "Upload successful")
    return flask.render_template('submit_jobs.html', title='Submit 3D print jobs', form=form, message = None)

@app.route('/3dprint/manage/')
def admin():
    return flask.render_template('admin.html', title='Manage printer jobs')

@app.route('/memes/submit/', methods=['GET', 'POST'])
def submit_memes():
    meme_data_path = "static/meme_data.json"
    class MemeForm(FlaskForm):
        user = TextAreaField('Your user name')
        photos = MultipleFileField(validators=[
            FileRequired(),
            FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
        submit = SubmitField('Upload')

    form = MemeForm(CombinedMultiDict((flask.request.files, flask.request.form)))
    basedir = os.path.abspath(os.path.dirname(__file__))
    if form.validate_on_submit():
        for f in form.photos.data:  # form.photo.data return a list of FileStorage object
            old_filename = secure_filename(f.filename)
            old_filename, extension = old_filename.split('.')
            extension = '.' + extension
            datestring = ''.join(str(datetime.datetime.now()).split()).split('.')[0]
            new_filename = old_filename + datestring + extension
            file_path = os.path.join(
                basedir, 'static', new_filename
            )
            f.save(file_path)
            new_meme = {
                "approved" : False,
                "date" : str(datetime.datetime.now()),
                "user" : form.user.data,
                "filename" : new_filename
            }
            meme_list = load_json(meme_data_path)
            meme_list.append(new_meme)
            save_json(meme_list, meme_data_path)

        return flask.render_template('submit_memes.html', title='Submit memez', form=form, message = "Upload successful")
    return flask.render_template('submit_memes.html', title='Submit memez', form=form, message = None)

@app.route('/memes/', methods=['GET'])
def list_memes():
    memes = load_json("static/meme_data.json")
    return flask.render_template('list_memes.html', title='Memez pending approval', memes = memes, message = None)

@app.shell_context_processor
def ctx():
    return {"app": app}

def load_json(json_data_path):
    try:
        json_data_file = open(json_data_path, "r")
        json_data = json.load(json_data_file)
        json_data_file.close()
    except(FileNotFoundError):
        json_data = []
    return json_data

def save_json(data, json_data_path):
    json_data_file = open(json_data_path, "w")
    json.dump(data, json_data_file, indent=4)
    json_data_file.close()

"""
if __name__ == "__main__":
    app.run(ssl_context='adhoc')"""