from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app
from app import db
from app.forms import LoginForm, RegistrationForm, AddPotForm,  AddClayForm, AddGlazeForm, GlazeLayerForm, AddKilnForm, AddFiringProgram, FiringSegmentForm
from wtforms import SubmitField
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Pot, Clay, FiringProgram, Kiln, Glaze, Image, PotGlaze
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from app.utils import allowed_file, get_pot_fields, POT_EXCLUDED_FIELDS, safe_query, set_select_field_choices, prepopulate_select

@app.route('/')
@app.route('/home')
@app.route('/index')
@login_required
def index():
    pots = Pot.query.order_by(Pot.throw_date.asc()).all()
    for pot in pots:
        ordered_glaze_layers = PotGlaze.query.filter_by(pot_id=pot.id).order_by(PotGlaze.display_order).all()
        pot.ordered_glaze_layers = ordered_glaze_layers
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

'''Create a Pot object from the form data.
If there is a pot as a given argument, update the existing pot with new data.'''
def fetch_pot(form, pot=None):
    POT_FIELDS = get_pot_fields(form)
    data = {field: getattr(form, field).data for field in POT_FIELDS}
    additional_data = {'made_with_clay': safe_query(Clay, form.made_with_clay.data), 
                    'bisque_fired_with_program': safe_query(FiringProgram, data['bisque_fire_program_id']),
                    'bisque_fired_with_kiln': safe_query(Kiln, data['bisque_fire_kiln_id']),
                    'glaze_fired_with_program': safe_query(FiringProgram, data['glaze_fire_program_id']),
                    'glaze_fired_with_kiln': safe_query(Kiln, data['glaze_fire_kiln_id'])}
    data.update(additional_data)
    if data['vessel_type']:
        if pot is None:
            pot = Pot(**data)
        else:
            # Update the existing Pot object with the new data
            for key, value in data.items():
                setattr(pot, key, value)
        # Save the used glaze with the number of layers
        number_of_glazes = len(form.used_glazes.data)
        for glaze_layer_index in range(number_of_glazes):
            glaze_layer = form.used_glazes.data[glaze_layer_index]
            glaze = safe_query(Glaze, glaze_layer['glaze'])
            if glaze and glaze_layer['number_of_layers'] > 0:
                pot_glaze = PotGlaze(pot=pot, glaze=glaze, number_of_layers=glaze_layer['number_of_layers'], display_order=glaze_layer_index + 1)
                db.session.add(pot_glaze)
        # Save the images
        print('photophotophotophotophoto')
        print(form.photos.data)
        print('photophotophotophotophoto')
        for photo in form.photos.data:
            if photo and allowed_file(photo.filename):
                filename = secure_filename(photo.filename)
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image = Image(filename=filename, pot=pot)
                db.session.add(image)
                pot.primary_image = filename        
    return pot

'''Filling out the AddPotForm and add a new pot to the database'''
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

    # Show the correct selected choices for select fields from the database
    form.made_with_clay.data = prepopulate_select(pot.made_with_clay)
    form.bisque_fire_program_id.data = prepopulate_select(pot.bisque_fired_with_program)
    form.bisque_fire_kiln_id.data = prepopulate_select(pot.bisque_fired_with_kiln)
    for glaze_index, glaze in enumerate(pot.used_glazes):
        form_glaze = form.used_glazes.entries[glaze_index]
        form_glaze.glaze.data = glaze.glaze_id
    form.glaze_fire_program_id.data = prepopulate_select(pot.glaze_fired_with_program)
    form.glaze_fire_kiln_id.data = prepopulate_select(pot.glaze_fired_with_kiln)
    
    # Photo prepopulation
    if pot.images:
        image_urls = [url_for('static', filename='photos/' + image.filename) for image in pot.images]
        form.photos.process_data(image_urls)
    
    return render_template('pot.html', title='Edit pot', form=form, pot_id=pot_id)

'''AJAX route for adding new glaze layer(s)'''
@app.route('/get_glaze_field/<int:index>')
@login_required
def get_glaze_field(index):
    glaze_layer = GlazeLayerForm(prefix=f'used_glazes-{index}')
    return render_template('glaze_field.html', glaze_layer=glaze_layer, index=index)


@app.route('/get_glaze_choices', methods=['GET'])
@login_required
def get_glaze_choices():
    glaze_choices = [(glaze.id, glaze.get_glaze_name()) for glaze in Glaze.query.all()]
    return jsonify(glaze_choices)


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


@app.route('/viewclays')
@login_required
def view_clays():
    clays = Clay.query.all()
    return render_template('viewclays.html', title='List of clays', clays=clays)
        

@app.route('/showclay/<int:clay_id>')
@login_required
def show_clay(clay_id):
    clay = Clay.query.get(clay_id)
    if clay:
        return render_template('showclay.html', title='Clay {}'.format(clay.get_clay_name()), clay=clay)
    return render_template('404.html')


@app.route('/viewkilns')
@login_required
def view_kilns():
    kilns = Kiln.query.all()
    firing_programs = FiringProgram.query.all()
    program_time = {}
    for program in firing_programs:
        associated_segments = program.associated_segments.all()
        total_time = sum(segment.time_to_reach for segment in associated_segments if segment.time_to_reach)
        hours, minutes = divmod(total_time, 60)
        program_time[program.id] = '{}h {}min'.format(hours, minutes)
    return render_template('viewkilns.html', title='List of kilns', kilns=kilns, firing_programs=firing_programs, program_time=program_time)
        
        
@app.route('/addkiln', methods=['GET', 'POST'])
@login_required
def add_kiln():
    form = AddKilnForm()
    if current_user.is_authenticated and form.validate_on_submit():
        kiln = Kiln(name=form.name.data, brand=form.brand.data, type=next(label for value, label in form.type.choices if value == form.type.data),
                    capacity=form.capacity.data, temp_max=form.temp_max.data, 
                    temp_unit=next(label for value, label in form.temp_unit.choices if value == form.temp_unit.data), 
                    voltage=form.voltage.data + ' kW', controller=form.controller.data)
        db.session.add(kiln)
        db.session.commit()
        flash('A new kiln has been added.')
        return redirect(url_for('index'))
    return render_template('addkiln.html', title='Add new kiln', form=form)


@app.route('/addfiringprogram', methods=['GET', 'POST'])
@login_required
def add_firing_program():
    form = AddFiringProgram()
    
    if current_user.is_authenticated and form.validate_on_submit():
        return redirect(url_for('view_kilns'))
    return render_template('addfiringprogram.html', form=form)


'''AJAX route for adding new firing segment(s))'''
@app.route('/get_segment/<int:index>')
@login_required
def get_segment(index):
    segment = FiringSegmentForm(prefix=f'firing_segments-{index}')
    return render_template('firing_segment.html', segment=segment, segment_index=index)
