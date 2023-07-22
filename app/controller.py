from flask import render_template, flash, redirect, url_for, request
from app import app
from app import db
from app.forms import LoginForm, RegistrationForm, AddPotForm, AddClayForm, AddGlazeForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Pot, Clay, FiringProgram, Kiln, Glaze
from werkzeug.urls import url_parse
from datetime import datetime

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


@app.route('/addpot', methods=['GET', 'POST'])
@login_required
def add_pot():
    form = AddPotForm()
    if current_user.is_authenticated and form.validate_on_submit():
        clay = Clay.query.get(form.clay_type.data)
        bisque_fire_program_id = form.bisque_fired_with_program.data
        bisque_program = FiringProgram.query.get(bisque_fire_program_id)
        bisque_fire_kiln_id = form.bisque_fired_with_kiln.data
        bisque_kiln = Kiln.query.get(bisque_fire_kiln_id)
        used_glazes = [Glaze.query.get(id) for id in form.used_glazes.data]
        glaze_fire_program_id = form.glaze_fired_with_program.data
        glaze_program = FiringProgram.query.get(glaze_fire_program_id)
        glaze_fire_kiln_id = form.glaze_fired_with_kiln.data
        glaze_kiln = Kiln.query.get(glaze_fire_kiln_id)
        if clay and bisque_program and bisque_kiln and glaze_program and glaze_kiln:
            pot = Pot(vessel_type=form.vessel_type.data, made_with_clay = clay, author=form.author.data, 
                    throw_date=form.throw_date.data, throw_weight=form.throw_weight.data, 
                    throw_height=form.throw_height.data, throw_width=form.throw_width.data,
                    throw_notes=form.throw_notes.data, trim_date=form.trim_date.data,
                    trim_weight=form.trim_weight.data, trim_surface_treatment=form.trim_surface_treatment.data,
                    trim_notes=form.trim_notes.data, bisque_fire_start=form.bisque_fire_start.data,
                    bisque_fire_program_id=bisque_fire_program_id,
                    bisque_fired_with_program=bisque_program, bisque_fire_kiln_id=bisque_fire_kiln_id,
                    bisque_fired_with_kiln=bisque_kiln,
                    bisque_fire_end=form.bisque_fire_end.data, bisque_fire_open=form.bisque_fire_open.data,
                    bisque_fire_notes=form.bisque_fire_notes.data, 
                    glaze_date=form.glaze_date.data, used_glazes = used_glazes, glaze_notes=form.glaze_notes.data,
                    glaze_fire_start=form.glaze_fire_start.data,
                    glaze_fire_program_id=glaze_fire_program_id, glaze_fire_kiln_id=glaze_fire_kiln_id,
                    glaze_fired_with_kiln=glaze_kiln,
                    glaze_fired_with_program=glaze_program, 
                    glaze_fire_end=form.glaze_fire_end.data, glaze_fire_open=form.glaze_fire_open.data,
                    glaze_fire_notes=form.glaze_fire_notes.data)
            db.session.add(pot)
            db.session.commit()
            flash('A new pot has been saved.')
            return redirect(url_for('index'))
    return render_template('addpot.html', title='Add new pot', form=form)


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
        return redirect(url_for('add_pot'))
    return render_template('addglaze.html', title='Add new glaze', form=form)


@app.route('/viewglazes')
@login_required
def view_glazes():
    glazes = Glaze.query.all()
    return render_template('viewglazes.html', title='List of glazes', glazes=glazes)
        