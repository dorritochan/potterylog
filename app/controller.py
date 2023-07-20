from flask import render_template, flash, redirect, url_for, request
from app import app
from app import db
from app.forms import LoginForm, RegistrationForm, AddPotForm, AddClayForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Pot, Clay
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
        clay = Clay.query.filter_by(id=form.clay_type.data).first()
        if clay:
            pot = Pot(vessel_type=form.vessel_type.data, clay_type=clay.id, author=form.author.data, \
                throw_date=form.throw_date.data)
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
                    temp_max=form.temp_max.data, temp_unit=form.temp_unit.data, 
                    grog_percent=form.grog_percent.data, grog_size_max=form.grog_size_max.data)
        db.session.add(clay)
        db.session.commit()
        flash('A new clay has been added.')
        return(redirect(url_for('index')))
    return render_template('addclay.html', title='Add new clay', form=form)
        