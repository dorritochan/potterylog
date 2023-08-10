from flask import render_template, flash, redirect, url_for, request
from app import app
from app import db
from app.forms import LoginForm, RegistrationForm, AddPotForm,  AddClayForm, AddGlazeForm
from wtforms import SubmitField
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Pot, Clay, FiringProgram, Kiln, Glaze
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from app.utils import allowed_file, get_pot_fields, POT_EXCLUDED_FIELDS, safe_query, set_select_field_choices

@app.route('/')
@app.route('/home')
@app.route('/index')
@login_required
def index():
    pots = Pot.query.order_by(Pot.throw_date.asc()).all()
    return render_template('index.html', title='Pottery log', pots=pots)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # POST method
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            return redirect(url_for('index'))
        return redirect(next_page)
    # GET method    
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password_hash(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return(redirect(url_for('login')))
    return render_template('register.html', title='Register', form=form)
    

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


def fetch_pot(form, pot=None):
    POT_FIELDS = get_pot_fields(form)
    data = {field: getattr(form, field).data for field in POT_FIELDS}
    additional_data = {'made_with_clay': safe_query(Clay, form.made_with_clay.data), 
                    'bisque_fired_with_program': safe_query(FiringProgram, data['bisque_fire_program_id']),
                    'bisque_fired_with_kiln': safe_query(Kiln, data['bisque_fire_kiln_id']),
                    'used_glazes': [safe_query(Glaze, id) for id in form.used_glazes.data],
                    'glaze_fired_with_program': safe_query(FiringProgram, data['glaze_fire_program_id']),
                    'glaze_fired_with_kiln': safe_query(Kiln, data['glaze_fire_kiln_id'])}
    data.update(additional_data)
    if data['made_with_clay']:
        if pot is None:
            pot = Pot(**data)
        else:
            # Update the existing Pot object with the new data
            for key, value in data.items():
                setattr(pot, key, value)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(photo_path)
            pot.photo_filename = filename
            
    return pot

@app.route('/addpot', methods=['GET', 'POST'])
@login_required
def add_pot():
    form = AddPotForm()
    
    # Set the choices for the select fields
    set_select_field_choices(form)
    
    # Set the label for the submit button
    form.submit.label.text = 'Add pot'
    
    # POST
    if request.method == 'POST' and current_user.is_authenticated and form.validate_on_submit():
        pot = fetch_pot(form)
        db.session.add(pot)
        db.session.commit()
        flash('A new pot has been saved.')
        return redirect(url_for('index'))
    # GET
    return render_template('pot.html', title='Add a new pot', form=form)


@app.route('/editpot/<int:pot_id>', methods=['GET', 'POST'])
@login_required
def edit_pot(pot_id):
    # Fetch the existing pot from the database
    pot = Pot.query.get_or_404(pot_id)
    
    # Populate the form with the existing pot data
    form = AddPotForm(obj=pot)
    
    # Prepopulate select fields
    set_select_field_choices(form)
    
    # Set the label for the submit button
    form.submit.label.text = 'Update pot'
    
    # POST
    if request.method == 'POST' and current_user.is_authenticated and form.validate_on_submit():
        print('Form validated')
        pot = fetch_pot(form, pot)
        db.session.commit()
        flash('Pot successfully updated.')
        return redirect(url_for('index'))
    
    # GET
    # Show the correct choices for select fields
    form.made_with_clay.data = pot.made_with_clay.id
    form.bisque_fire_program_id.data = pot.bisque_fired_with_program.id
    form.bisque_fire_kiln_id.data = pot.bisque_fired_with_kiln.id
    form.used_glazes.data = [glaze.id for glaze in pot.used_glazes]
    form.glaze_fire_program_id.data = pot.glaze_fired_with_program.id
    form.glaze_fire_kiln_id.data = pot.glaze_fired_with_kiln.id
    
    # Photo prepopulation
    if pot.photo_filename is not None:
        form.photo.process_data(url_for('static', filename='photos/' + pot.photo_filename))
    
    return render_template('pot.html', title='Edit pot', form=form)

@app.route('/addclay', methods=['GET', 'POST'])
@login_required
def add_clay():
    form = AddClayForm()
    if current_user.is_authenticated and form.validate_on_submit():
        clay = Clay(brand=form.brand.data, color=form.color.data, temp_min=form.temp_min.data, 
                    temp_max=form.temp_max.data, 
                    temp_unit=next(label for value, label in form.temp_unit.choices if value == form.temp_unit.data), 
                    grog_percent=form.grog_percent.data, grog_size_max=form.grog_size_max.data)
        db.session.add(clay)
        db.session.commit()
        flash('A new clay has been added.')
        return(redirect(url_for('add_pot')))
    return render_template('addclay.html', title='Add new clay', form=form)


@app.route('/addglaze', methods=['GET', 'POST'])
@login_required
def add_glaze():
    form = AddGlazeForm()
    if current_user.is_authenticated and form.validate_on_submit():
        glaze = Glaze(brand=form.brand.data, name=form.name.data, color=form.color.data, 
                    temp_min=form.temp_min.data, temp_max=form.temp_max.data, 
                    temp_unit=next(label for value, label in form.temp_unit.choices if value == form.temp_unit.data),
                    brand_id=form.brand_id.data, glaze_url=form.glaze_url.data)
        db.session.add(glaze)
        db.session.commit()
        flash('A new glaze has been added.')
        return redirect(url_for('index'))
    return render_template('addglaze.html', title='Add new glaze', form=form)


@app.route('/viewglazes')
@login_required
def view_glazes():
    glazes = Glaze.query.all()
    return render_template('viewglazes.html', title='List of glazes', glazes=glazes)
        

@app.route('/showglaze/<int:glaze_id>')
@login_required
def show_glaze(glaze_id):
    glaze = Glaze.query.get(glaze_id)
    if glaze:
        return render_template('showglaze.html', title='Glaze {}'.format(glaze.get_glaze_name()), glaze=glaze)
    return render_template('404.html')