import flask
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, StringField, PasswordField, BooleanField
from wtforms.validators import ValidationError, DataRequired
from flask_wtf.file import MultipleFileField, FileAllowed, FileRequired
from wtforms import SubmitField
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
import os
import datetime
import json

from . import admin

app = flask.Flask(__name__)

app.config.from_mapping(
    SECRET_KEY='dev')

login = LoginManager(app)
login.login_view = 'login'

@login.user_loader
def load_user(id):
    return admin.user

job_data_path = "static/job_data.json" # TODO: allow admin to manage jobs
meme_data_path = "static/meme_data.json"

@app.route('/')
def index():
    return flask.render_template('index.html', title='Home')

@app.route('/manage/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for('index'))
    else:
        class LoginForm(FlaskForm):
            username = StringField('Username', validators=[DataRequired()])
            password = PasswordField('Password', validators=[DataRequired()])
            remember_me = BooleanField('Remember Me')
            submit = SubmitField('Sign In')

        form = LoginForm()
        
        if form.validate_on_submit():
            user = admin.user()
            print("check:", form.username.data, form.password.data)
            if not user.check_username(form.username.data) and user.check_password(form.password.data):
                flask.flash('Invalid username or password')
                return flask.redirect(flask.url_for('login'))
            login_user(user, remember=form.remember_me.data)
            flask.flash('Logged in successfully.')
            next_page = flask.request.args.get('next')
            if not next_page or urlsplit(next_page).netloc != '':
                next_page = flask.url_for('index')
            return flask.redirect(next_page)
    return flask.render_template('login.html', title='Sign in to manage content', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return flask.redirect(flask.url_for('index'))

@app.route('/3dprint/')
def list_jobs():
    job_list = load_json(job_data_path)
    return flask.render_template('jobs.html', jobs=job_list, title='Submitted printer jobs')

@app.route('/3dprint/submit/', methods=['GET', 'POST'])
def submit_jobs():
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
                "denied" : False,
                "completed" : False,
                "deleted" : False,
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

@app.route('/memes/submit/', methods=['GET', 'POST'])
def submit_memes():
    
    class MemeForm(FlaskForm):
        user = TextAreaField('Your user name')
        photos = MultipleFileField(validators=[
            FileRequired(),
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
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
                "featured" : None,
                "deleted" : False,
                "date" : str(datetime.datetime.now()),
                "user" : form.user.data,
                "filename" : new_filename
            }
            meme_list = load_json(meme_data_path)
            meme_list.append(new_meme)
            save_json(meme_list, meme_data_path)

        return flask.render_template('submit_memes.html', title='Submit memez', form=form, message = "Upload successful")
    return flask.render_template('submit_memes.html', title='Submit memez', form=form, message = None)

@app.route('/manage/3dprint/', methods=['GET', 'POST'])
def admin_3dprint():
    if current_user.is_authenticated:
        job_list = load_json(job_data_path)
        class ManageJobsForm(FlaskForm):
            approve = SubmitField('Approve')
            deny = SubmitField('Deny')
            complete = SubmitField('Mark completed')
            delete = SubmitField('Delete')
            reset = SubmitField('Reset')
            job = HiddenField()
        form = ManageJobsForm()
        result = flask.request.form
        message = None
        if 'approve' in result.keys():
            job_list[int(result['approve'])]['approved'] = True
            job_list[int(result['approve'])]['denied'] = False
            print(job_list[int(result['approve'])])

        if 'deny' in result.keys():
            job_list[int(result['deny'])]['denied'] = result['reason']
            job_list[int(result['deny'])]['approved'] = False
            print(job_list[int(result['deny'])])

        if 'complete' in result.keys():
            datestring_today = str(datetime.datetime.now()).split()[0]
            job_list[int(result['complete'])]['completed'] = datestring_today
            print(job_list[int(result['complete'])])

        if 'delete' in result.keys():
            job_list[int(result['delete'])]['deleted'] = True
            job_list[int(result['delete'])]['approved'] = False
            print(job_list[int(result['delete'])])

        if 'reset' in result.keys():
            job_list[int(result['reset'])]['approved'] = False
            job_list[int(result['reset'])]['denied'] = False
            job_list[int(result['reset'])]['completed'] = None
            job_list[int(result['reset'])]['deleted'] = None
            print(job_list[int(result['reset'])])

        save_json(job_list, job_data_path)
        return flask.render_template('admin_3dprint.html', jobs=dict(enumerate(job_list)), title='Manage printer jobs')
    else:
        return flask.redirect(flask.url_for('login'))

@app.route('/manage/memes/', methods=['GET', 'POST']) # delete
def admin_memes():
    if current_user.is_authenticated:
        memes = load_json(meme_data_path)
        class ManageMemesForm(FlaskForm):
            approve = SubmitField('Approve')
            feature = SubmitField('Feature')
            disapprove = SubmitField('Disapprove')
            unfeature = SubmitField('Unfeature')
            meme = HiddenField()
        form = ManageMemesForm()
        result = flask.request.form
        message = None
        if 'approve' in result.keys():
            memes[int(result['approve'])]['approved'] = True
            memes[int(result['approve'])]['deleted'] = False
            print(memes[int(result['approve'])])

        if 'feature' in result.keys():
            memes[int(result['feature'])]['approved'] = True
            memes[int(result['feature'])]['deleted'] = False
            memes[int(result['feature'])]['featured'] = "pending"
            print(memes[int(result['feature'])])

        if 'disapprove' in result.keys():
            memes[int(result['disapprove'])]['approved'] = False
            memes[int(result['disapprove'])]['featured'] = None
            print(memes[int(result['disapprove'])])

        if 'unfeature' in result.keys():
            memes[int(result['unfeature'])]['featured'] = None
            memes[int(result['unfeature'])]['approved'] = True
            print(memes[int(result['unfeature'])])

        if 'delete' in result.keys():
            memes[int(result['delete'])]['deleted'] = True
            memes[int(result['delete'])]['featured'] = None
            memes[int(result['delete'])]['approved'] = False
            print(memes[int(result['delete'])])

        save_json(memes, meme_data_path)
        return flask.render_template('admin_memes.html', title='Manage memes', memes = dict(enumerate(memes)), form=form, message = message)
    else: return flask.redirect(flask.url_for('login'))

@app.route('/memes/', methods=['GET'])
def list_memes():
    memes = load_json("static/meme_data.json")
    return flask.render_template('list_memes.html', title='Memez pending approval', memes = memes, message = None)

@app.route('/api/memes/', methods=['GET'])
def meme_api():
    memes = load_json("static/meme_data.json")
    return memes

@app.route('/api/jobs/')
def print_api():
    # TODO: get approved jobs
    all_jobs = load_json(job_data_path)
    return all_jobs

@app.shell_context_processor
def ctx():
    return {"app": app}

@app.template_filter("short_date")
def format_date(date):
    return date[:16]

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