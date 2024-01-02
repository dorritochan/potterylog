# Standard library imports
from datetime import datetime
import os, uuid

# Third-party imports
from flask import render_template, flash, redirect, url_for, request, jsonify, current_app, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from flask_cors import cross_origin
from sqlalchemy.exc import DatabaseError
from sqlalchemy import desc
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

# Local application imports
from app import db

app = current_app
from app.forms import (
    LoginForm, RegistrationForm, AddPotForm, AddClayForm, AddGlazeForm,
    GlazeLayerForm, AddKilnForm, AddFiringProgramForm, FiringSegmentForm,
    AddLinkForm, AddCommissionForm
)
from app.models import (
    User, Pot, Clay, FiringProgram, Kiln, Glaze, Image, PotGlaze, 
    ProgramSegment, FiringSegment, FiringProgram, Link, Commission
)
from app.schemas import (
    ClaySchema, PotSchema, GlazeSchema
)
from app.utils import (
    allowed_file, 
    set_pot_select_field_choices,
    safe_query, 
    populate_pot_select_field_data,
    extract_pot_data, extract_glaze_data, extract_clay_data, extract_kiln_data, 
    extract_firing_segment_data, extract_link_data, extract_firing_program_data, extract_commission_data,
    extract_link_from_object, extract_clay_from_object, extract_glaze_from_object, 
    extract_kiln_from_object, extract_firing_program_from_object, extract_commission_from_object, 
    program_firing_time,
    pot_to_dict
)

UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']





@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log in a user to the application.

    This route handles both GET and POST requests. If a user is already authenticated,
    they will be redirected to the index page. For GET requests, it renders the login form.
    For POST requests, it attempts to validate the submitted form data and log in the user.
    If the login is successful, the user is redirected to the index page or the originally
    requested page.

    Returns: 
        - Redirection to 'index' page: If the user is already logged in or 
        after successful login (if the previous page was not found).
        - Redirection to 'login' page: If the form data validation didn't pass.
        - Redirection to the previous page: After successful login.
        - HTML template: Displays the login form for GET requests.
    """
    
    # Redirect to index page if the user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    
    # ===================
    # POST method: Log in the user
    # ===================
    # Validate the form data
    if form.validate_on_submit():
        
        # Try to fetch the user from the database
        user = User.query.filter_by(username=form.username.data).first()
        
        # Check if the user exists and the password is correct
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        # Log in the user
        login_user(user, remember=form.remember_me.data)
        
        # Redirect the user to the previous page or the index
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            return redirect(url_for('index'))
        return redirect(next_page)
    
    # ===================
    # GET method: Render the login form   
    # ===================
    return render_template('login.html', title='Log In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register a new user.

    This route handles both GET and POST requests. If a user is already authenticated,
    they will be redirected to the index page. For GET requests, it renders the registration form.
    For POST requests, it attempts to validate the submitted form data, creates a new user,
    and adds them to the database. Upon successful registration, the user is redirected to the login page.

    Returns: 
        - Redirection to 'index' page: If the user is already logged in.
        - Redirection to 'login' page: After a successful registration.
        - HTML template: Displays the registration form for GET requests or for unsuccessful POST requests.
    """
    
    # Redirect to index page if the user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    
    # ===================
    # POST method: Add a user
    # ===================
    # Validate the form data
    if form.validate_on_submit():
        
        # Create a user based on the form data username and email
        user = User(username=form.username.data, email=form.email.data)
        
        # Set hashed password for the user
        user.set_password_hash(form.password.data)
        
        # Save the new user to the database
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        
        # Redirect to the login page
        return redirect(url_for('login'))
    
    # ===================
    # GET method: Render the registration form
    # ===================
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
@login_required
def logout():
    """
    Log out a logged-in user.
    
    This route handles only GET requests. It logs out a user who is currently logged in
    and then redirects to the index page, which might eventually redirect to the login 
    page since the user is no longer logged in.

    Returns:
        Redirection to 'index' page: After successful logout.
    """
    
    # Log out the currently logged-in user
    logout_user()
    
    # Redirect to the index page
    return redirect(url_for('index'))


def fetch_pot(form, pot=None):
    """
    Create or update a Pot object based on form data.
    
    If a 'pot' argument is given, this function will update the existing pot object with
    new data from the form. Otherwise, it will create a new Pot object from the form data.
    
    Args:
        form (Form): The form containing data to create/update the pot.
        pot (Pot, optional): The Pot object to update. Defaults to None, indicating a new Pot object should be created.
    
    Returns:
        Pot: The created or updated Pot object.
    """
    
    # Extract form data
    data = extract_pot_data(form)

    # Only proceed if vessel type is provided
    if data['vessel_type']:
        
        # Create a new Pot object if none is provided, otherwise update the existing one
        if pot is None:
            pot = Pot(**data)
            # Process and save glazes associated with the pot
            for glaze_layer_index, glaze_layer in enumerate(form.used_glazes.data):
                glaze = safe_query(Glaze, glaze_layer['glaze'])
                if glaze and glaze_layer['number_of_layers'] > 0:
                    pot_glaze = PotGlaze(
                        pot=pot, 
                        glaze=glaze, 
                        number_of_layers=glaze_layer['number_of_layers'], 
                        display_order=glaze_layer_index
                        )
                    
                    db.session.add(pot_glaze)
        else:
            # Update the existing Pot object with the new data
            for key, value in data.items():
                setattr(pot, key, value)
            
            # Glaze layers logic
            glazes_count = len(list(pot.used_glazes))
            order_additional_index = 0
            for glaze_layer_index, glaze_layer in enumerate(form.used_glazes.data):
                glaze = safe_query(Glaze, glaze_layer['glaze'])
                if glaze_layer_index + 1 <= glazes_count:
                    db_pot_glaze = PotGlaze.query.filter_by(pot=pot, display_order=glaze_layer_index).first()
                    # Don't make a new PotGlaze object, but modify the existing ones
                    if glaze and glaze_layer['number_of_layers'] > 0:
                        db_pot_glaze.glaze = glaze
                        db_pot_glaze.number_of_layers = glaze_layer['number_of_layers']
                        db_pot_glaze.display_order = glaze_layer_index+order_additional_index
                    else:
                        # Delete the existing PotGlaze object
                        db.session.delete(db_pot_glaze)
                        order_additional_index -= 1
                else:
                    if glaze and glaze_layer['number_of_layers'] > 0:
                        db_pot_glaze_new = PotGlaze(pot=pot, glaze=glaze, number_of_layers=glaze_layer['number_of_layers'], display_order=glaze_layer_index+order_additional_index)
                        db.session.add(db_pot_glaze_new)     
                    else:
                        order_additional_index -= 1
                        
                
        # Process and save images associated with the pot
        for photo in form.photos.data:
            if photo and allowed_file(photo.filename):
                filename = secure_filename(photo.filename)
                base, ext = os.path.splitext(filename)
                unique_filename = f"{base}_{uuid.uuid4()}{ext}"
                
                photo.save(os.path.join(UPLOAD_FOLDER, unique_filename))
                
                image = Image(filename=unique_filename, pot=pot)
                db.session.add(image)
                
                # Set the primary image for the pot
                pot.primary_image = unique_filename        
                
    return pot


@app.route('/addpot', methods=['GET', 'POST'])
@login_required
def add_pot():
    """
    Handle the creation of a new pot.

    The function presents a form for adding a new pot, validates the submitted data, and
    saves the new pot to the database if the form submission is valid.

    * If the request method is GET: the function renders the form to add a new pot.
    * If the request method is POST and the form validates: 
        - Extracts the pot data from the form.
        - Creates a new pot instance and adds it to the database.
        - Provides feedback to the user upon successful addition.
        - Redirects the user back to the 'index' page.

    Returns:
        render_template: Renders the 'pot.html' template with the form for adding a new pot
            or redirects to the 'index' page after successful addition.
    """
    
    form = AddPotForm()
    
    # Set the choices for the select fields
    set_pot_select_field_choices(form)
    
    # Set the label for the submit button
    form.submit.label.text = 'Add pot'
    
    # Forms for the glaze and clay modals
    glaze_form = AddGlazeForm()
    clay_form = AddClayForm()
    
    # ===================
    # POST method: Add a new pot
    # ===================
    # Validate the form
    if form.validate_on_submit():
        
        # Extract the form data and create a new Pot instance
        pot = fetch_pot(form)
        
        # Add the pot to the database
        db.session.add(pot)
        db.session.commit()
        
        # Show a message upon success
        flash('A new pot has been saved.')
        
        # Redirect to the 'index' page
        return redirect(url_for('index'))
    
    # ===================
    # GET method: Render the pot form
    # ===================
    return render_template('pot.html', title='Add a new pot', form=form, glaze_form=glaze_form, clay_form=clay_form)


@app.route('/editpot/<int:pot_id>', methods=['GET', 'POST'])
@login_required
def edit_pot(pot_id):
    # Fetch the existing pot from the database
    pot = Pot.query.get_or_404(pot_id)
    
    # Pre-populate the form with the existing pot data
    form = AddPotForm(obj=pot)
    
    # Set the choices for the select fields
    set_pot_select_field_choices(form)
    
    # Set the label for the submit button
    form.submit.label.text = 'Update pot'
    
    # Forms the glaze and clay modals
    glaze_form = AddGlazeForm()
    clay_form = AddClayForm()
    
    # ===================
    # POST method: Update pot
    # ===================
    # Validate the form data
    if form.validate_on_submit():
        
        # Extract the form data and update the pot
        pot = fetch_pot(form, pot)
        
        # Update the database 
        db.session.commit()
        
        # Show message upon success
        flash('Pot successfully updated.')
        
        # Redirection to the 'index' page
        return redirect(url_for('index'))
    
    # ===================
    # GET method: Render the pot form with prepopulated data
    # ===================

    # Show the correct selected choices for select fields from the database
    populate_pot_select_field_data(form, pot)

    # Pre-populate the form with the related images
    if pot.images:
        image_urls = [url_for('static', filename='photos/' + image.filename) for image in pot.images]
        form.photos.process_data(image_urls)
    
    # Render the 'pot.html' with pre-populated form data
    return render_template('pot.html', title='Edit pot', form=form, pot_id=pot_id, glaze_form=glaze_form, clay_form=clay_form)


@app.route('/get_glaze_field/<int:layer_index>')
@login_required
def get_glaze_field(layer_index):
    """
    Fetch and render an additional glaze layer field via AJAX.

    This function is triggered by AJAX requests initiated in the pot.js file. 
    Specifically, when a user is on the 'editpot' or 'addpot' page and clicks 
    the #add-glaze-layer button, this function is called to generate and render 
    an additional glaze layer field. The provided layer_index represents the next 
    glaze layer's position.
    
    Args:
        layer_index (int): The position for the new glaze layer field, which is 
        typically the current number of glaze layers incremented by one.

    Returns:
        HTML template: Renders a single glaze layer field based on the provided index.
    """
    # Instantiate a new glaze layer form object with a specified prefix
    glaze_layer = GlazeLayerForm(prefix=f'used_glazes-{layer_index}')
    
    # Render and return the template with the new glaze layer form and its index
    return render_template('glaze_field.html', glaze_layer=glaze_layer, index=layer_index)


@app.route('/get_glaze_choices')
@login_required
def get_glaze_choices():
    """
    Retrieve available glazes and return them in JSON format.
    
    This function provides the list of available glazes as JSON data. It's primarily 
    used to populate the glaze choices in the select field of dynamically added glaze layers.
    The AJAX requests, initiated from the pot.js file when on 'editpot' or 'addpot' pages, 
    trigger this function to fetch the choices after a user clicks the #add-glaze-layer button 
    and the 'get_glaze_field' function adds a new glaze layer field.

    Returns:
        JSON: List of tuples representing glaze choices, where each tuple contains 
        an ID and the associated glaze name.
    """
    # Query all glaze choices and transform them into tuples of (id, name)
    glaze_choices = [(glaze.id, glaze.get_glaze_name()) for glaze in Glaze.query.order_by(Glaze.brand, Glaze.brand_id).all()]
    
    # Return the glaze choices as a JSON response
    return jsonify(glaze_choices)


def add_item_to_db(form, model_class, extraction_function, flash_message):
    """
    Validate the form, extract data, create an instance of a model, and add it to the database.

    This function consolidates the common steps of validating a form, extracting data from it, 
    creating an instance of a database model, saving it to the database, flashing a message, 
    and returning a respective JSON message to the frontend.

    Args:
        form (FlaskForm): An instance of a form class (e.g. AddGlazeForm, AddClayForm) to be validated.
        model_class (db.Model): The class of the database model to be instantiated (e.g., Glaze, Clay).
        extraction_function (Callable[[FlaskForm], Dict[str, Any]]): A function that takes the form 
            as an argument and returns a dictionary of data extracted from the form.
        flash_message (str): The message to be flashed to the user upon successful addition.

    Returns:
        jsonify: A JSON format message, that contains the success status and/or error messages.

    Raises:
        - Exception: If there is en error extracting the form data
        - DatabaseError: If there's any issue while adding the item to the database. 
    """
    
    # Validate the form data
    if form.validate_on_submit():
        try:
            # Get the extraction function from 'utils.py' and extract the form data
            item_data = extraction_function(form)
        except Exception as e:
            # Log the exception for debugging
            app.logger.error(f"Error extracting form data: {e}")
            flash('An error occurred while processing the form. Please try again.')
            return jsonify(success=False, error="Error while extracting the form data")
        
        # Create a new model instance based on the form data
        item = model_class(**item_data)
        
        try:
            # Add the model instance to the database
            db.session.add(item)
            db.session.commit()
        except DatabaseError:
            # Rollback the session in case of an error
            db.session.rollback()
            # Log the error for debugging
            app.logger.error("Error committing to the database.")
            flash('An error occurred while saving to the database. Please try again later.')
            return jsonify(success=False, error="Database error")
        
        # Show the success message
        flash(flash_message)
        
        # Return the JSON success message
        return jsonify(success=True)
    
    response_data = {
        'success': False,
        'errors': form.errors
    }
    return jsonify(response_data)


@app.route('/addlink', methods=['POST'])
@login_required
def add_link():
    
    form = AddLinkForm()
    
    response = add_item_to_db(form, Link, extract_link_data, 'A new link has been saved.')
    return response


@app.route('/addcommission', methods=['POST'])
@login_required
def add_commission():
    
    form = AddCommissionForm()
    
    response = add_item_to_db(form, Commission, extract_commission_data, 'A new commission has been saved.')
    return response


@app.route('/addglaze', methods=['POST'])
@login_required
def add_glaze():
    """
    Add a new glaze to the database.
    
    The functions handles only POST requests.
    After successful form validation, it saves a new glaze to the database and returns a success
    message in JSON format. On failed validation, the form errors are jsonified and sent to the frontend.

    """
    
    form = AddGlazeForm()
    
    response = add_item_to_db(form, Glaze, extract_glaze_data, 'A new glaze has been saved.')
    return response


@app.route('/get_clay_choices')
@login_required
def get_clay_choices():
    """
    Retrieve available clays and return them in JSON format.
    
    This function provides the list of available clays as JSON data. It's primarily 
    used to populate the clay choices in the select field of dynamically handled pages.
    The AJAX requests, initiated from the pot.js file when on 'editpot' or 'addpot' pages, 
    trigger this function to fetch the updated select field choices after a user adds a 
    new clay type.

    Returns:
        JSON: List of tuples representing clay choices, where each tuple contains 
        an ID and the associated clay name.
    """
    # Query all clay choices and transform them into tuples of (id, name)
    clay_choices = [(clay.id, clay.get_clay_name()) for clay in Clay.query.order_by(Clay.brand, Clay.name_id).all()]
    
    # Return the clay choices as a JSON response
    return jsonify(clay_choices)


@app.route('/addclay', methods=['POST'])
@login_required
def add_clay():
    """
    Add a new clay to the database.
    
    This route handles POST requests. 
    After successful form validation, it saves a new clay to the database.
    On a failed validation, the form errors are jsonified and sent to the frontend.

    """
    form = AddClayForm()
    
    response = add_item_to_db(form, Clay, extract_clay_data, 'A new clay has been saved.')
    return response


@app.route('/addkiln', methods=['POST'])
@login_required
def add_kiln():
    """
    Add a new kiln to the database.
    
    This route handles POST requests. 
    After successful form validation, it saves a new kiln to the database.
    On a failed validation, the form errors are jsonified and sent to the frontend.

    """
    form = AddKilnForm()
    
    response = add_item_to_db(form, Kiln, extract_kiln_data, 'A new kiln has been saved.')
    return response


@app.route('/addfiringprogram', methods=['POST'])
@login_required
def add_firing_program():
    """
    Add a new firing program to the database.
    
    This route handles POST requests. 
    After successful form validation, it saves a new firing program to the database.
    On a failed validation, the form errors are jsonified and sent to the frontend.
    """
    
    form = AddFiringProgramForm()
    
    if form.validate_on_submit():
        
        try:
            # Extract the form data
            data = extract_firing_program_data(form)
        except Exception as e:
            # Log the exception for debugging
            app.logger.error(f"Error extracting form data: {e}")
            flash('An error occurred while processing the form. Please try again.')
            return jsonify(success=False, error="Error while extracting the form data")
        
        # Create new firing program instance
        firing_program = FiringProgram(**data)
        
        # Remove empty segments
        firing_segments = [segment for segment in form.firing_segments.data if segment['temp_start'] and segment['temp_end']]
        
        # Check if the entered segments already exist in the database
        for segment_index, segment in enumerate(firing_segments):
            
            # Extract the segment data
            data_segment = extract_firing_segment_data(segment)
            
            db_firing_segment = FiringSegment(**data_segment)
            
            db.session.add(db_firing_segment)
            
            # Create and add program-segment association to the session
            program_segment = ProgramSegment(program=firing_program, segment=db_firing_segment,
                                                segment_order=segment_index)
            
            # Add the firing program to the session and commit
            db.session.add(program_segment)
            
        # Add the firing program to the database
        db.session.add(firing_program)
        db.session.commit()
        
        # Show a message upon success
        flash('The firing program {} has successfully saved.'.format(firing_program.name))
        
        # Return the JSON success message
        return jsonify(success=True)
    
    response_data = {
        'success': False,
        'errors': form.errors
    }
    return jsonify(response_data)


@app.route('/get_segment/<int:segment_index>')
@login_required
def get_segment(segment_index):
    """
    Fetch and render an additional firing segment field via AJAX.

    This function is triggered by AJAX requests initiated in the pot.js file. 
    Specifically, when a user is on the 'add_firing_program' page and clicks 
    the #add-segment button, this function is called to generate and render 
    an additional firing segment field. The provided segment_index represents the next 
    firing segment's position.
    
    Args:
        segment_index (int): The position for the new firing segment field, which is 
        typically the current number of segments incremented by one.

    Returns:
        HTML template: Renders a single segment field based on the provided index.
    """
    # Instantiate a new firing segment form object with a specified prefix
    segment = FiringSegmentForm(prefix=f'firing_segments-{segment_index}')
    
    # Render and return the template with the new firing segment form and its index
    return render_template('firing_segment.html', segment=segment, segment_index=segment_index)


@app.route('/viewglazes')
@login_required
def view_glazes():
    """
    Render a list of all glazes in the database.

    Retrieves all Glaze objects from the database and sends them to the template 
    for display.
    
    Returns:
        HTML template: Renders the list of all glazes.
    """
    glazes = Glaze.query.order_by(Glaze.brand, Glaze.brand_id).all()
    
    # A glaze form for the modal
    glaze_form = AddGlazeForm()
    
    return render_template('viewglazes.html', title='List of glazes', glazes=glazes, glaze_form=glaze_form)


@app.route('/viewlinks')
@login_required
def view_links():
    """
    Render a list of all links in the database.

    Retrieves all LINK objects from the database and sends them to the template 
    for display.
    
    Returns:
        HTML template: Renders the list of all links.
    """
    links = Link.query.order_by(Link.title).all()
    
    # A link form for the modal
    form = AddLinkForm()
    
    return render_template('viewlinks.html', title='Links', form=form, links=links)


@app.route('/viewcommissions')
@login_required
def view_commissions():
    """
    Render a list of all commissions in the database.

    Retrieves all LINK objects from the database and sends them to the template 
    for display.
    
    Returns:
        HTML template: Renders the list of all links.
    """
    commissions = Commission.query.order_by(Commission.deadline.desc()).all()
    
    # A link form for the modal
    form = AddCommissionForm()
    
    return render_template('viewcommissions.html', title='Commissions', form=form, commissions=commissions)


@app.route('/showglaze/<int:glaze_id>')
@login_required
def show_glaze(glaze_id):
    """
    Show the details of a glaze.

    Args:
        glaze_id (int): The ID of a glaze.

    Returns:
        HTML template: Renders the 'showglaze.html' template with the glaze details if found,
            else Flask's default 404 page is returned.
    """
    glaze = Glaze.query.get_or_404(glaze_id)

    # Render the HTML with the glaze details if the glaze has been found.
    # Otherwise show 404.
    return render_template('showglaze.html', title='Glaze {}'.format(glaze.get_glaze_name()), glaze=glaze)


@app.route('/viewclays')
@login_required
def view_clays():
    """
    Render a list of all clays in the database.

    Retrieves all Clay objects from the database and sends them to the template 
    for display.
    
    Returns:
        HTML template: Renders the list of all clays.
    """
    clays = Clay.query.order_by(Clay.brand, Clay.name_id).all()
    
    # A clay form for the modal
    clay_form = AddClayForm()
    
    return render_template('viewclays.html', title='List of clays', clays=clays, clay_form=clay_form)


@app.route('/showclay/<int:clay_id>')
@login_required
def show_clay(clay_id):
    """
    Show the details of a clay.

    Args:
        clay_id (int): The ID of a clay.

    Returns:
        HTML template: Renders the 'showclay.html' template with the clay details if found,
            else Flask's default 404 page is returned.
    """
    clay = Clay.query.get_or_404(clay_id)
    
    # Render the HTML with the clay details if the clay has been found.
    # Otherwise show 404.
    return render_template('showclay.html', title='Clay {}'.format(clay.get_clay_name()), clay=clay)


@app.route('/viewkilns')
@login_required
def view_kilns():
    """
    Render a list of all kilns and firing programs in the database.

    Retrieves all Kiln and FiringProgram objects from the database and sends them to the template 
    for display.
    
    Returns:
        HTML template: Renders the list of all kilns and firing programs.
    """
    # Retrieve all the Kiln objects
    kilns = Kiln.query.all()
    
    # Retrieve all the FiringProgram objects
    firing_programs = FiringProgram.query.all()
    
    # Fetch the kiln form for the modal
    kiln_form = AddKilnForm()
    
    # Fetch the firing program form for the modal
    program_form = AddFiringProgramForm()
    
    # Instantiate the dictionary for the total firing time.
    # The keys of the dictionary are the IDs of the firing programs 
    # and the values are the firing times of the respective programs.
    total_firing_time = {}
    
    # For each firing program, retrieve and set its segments in the correct order (by `segment_order`).
    # This is done by adding a new attribute, `ordered_segments`, to the firing program instance.
    # Note: `program.ordered_segments` and `program.associated_segments` contain the same data but may differ in order.
    for program in firing_programs:
        ordered_segments = ProgramSegment.query.filter_by(program=program).order_by(ProgramSegment.segment_order).all()
        program.ordered_segments = ordered_segments
        
        # Add a new key-value pair with the program ID and the total firing time of the program
        total_firing_time[program.id] = program_firing_time(program)
    
    # Render the template with the list of kilns and firing programs with their respective segments
    return render_template('viewkilns.html', title='List of kilns', kilns=kilns, firing_programs=firing_programs, total_firing_time=total_firing_time, kiln_form=kiln_form, program_form=program_form)



@app.route('/delete_<item_type>/<int:item_id>', methods=['DELETE'])
@login_required
def delete_item(item_type, item_id):
    
    if item_type == 'pot':
        item = Pot.query.get_or_404(item_id)
        
        
    elif item_type == 'link':
        item = Link.query.get_or_404(item_id)
        
    elif item_type == 'clay':
        item = Clay.query.get_or_404(item_id)
        
    elif item_type == 'glaze':
        item = Glaze.query.get_or_404(item_id)
    
    elif item_type == 'kiln':
        item = Kiln.query.get_or_404(item_id)
    
    elif item_type == 'firing-program':
        item = FiringProgram.query.get_or_404(item_id)
    
    elif item_type == 'commission':
        item = Commission.query.get_or_404(item_id)
    
    try:
        db.session.delete(item)
        db.session.commit()
        return jsonify(success=True, message=f'Deleted {item_type} with ID {item_id}')
    except Exception as e:
        app.logger.error(f"Error deleting {item_type}: {e}")
        return jsonify(success=False, message='Internal Server Error'), 500


@app.route('/delete_image_from_pot/<image_source>/<int:pot_id>', methods=['DELETE'])
@login_required
def delete_image_from_pot(image_source, pot_id):
    
    pot = Pot.query.get_or_404(pot_id)
    image = Image.query.filter_by(filename=image_source, pot=pot).first()
    image_name = image.filename
    try:
        db.session.delete(image)
        db.session.commit()

        if pot.primary_image == image_name:
            pot_images = Image.query.filter_by(pot=pot).all()
            last_image = pot_images[-1]
            pot.primary_image = last_image.filename
            db.session.commit()

        return jsonify(success=True, message=f'Deleted image with src {image_source}')
    except Exception as e:
        app.logger.error(f"Error deleting {image}: {e}")
        return jsonify(success=False, message='Internal Server Error'), 500

    
@app.route('/update_<item_type>/<int:item_id>', methods=['PUT'])
@login_required
def update_item(item_type, item_id):
    
    if item_type == 'link':
        form = AddLinkForm()
        item = Link.query.get_or_404(item_id)
        data = extract_link_data(form)
                
    elif item_type == 'clay':
        form = AddClayForm()
        item = Clay.query.get_or_404(item_id)
        data = extract_clay_data(form)
        
    elif item_type == 'glaze':
        form = AddGlazeForm()
        item = Glaze.query.get_or_404(item_id)
        data = extract_glaze_data(form)
    
    elif item_type == 'kiln':
        form = AddKilnForm()
        item = Kiln.query.get_or_404(item_id)
        data = extract_kiln_data(form)
    
    elif item_type == 'commission':
        form = AddCommissionForm()
        item = Commission.query.get_or_404(item_id)
        data = extract_commission_data(form)
    
    elif item_type == 'firing-program':
        form = AddFiringProgramForm()
        item = FiringProgram.query.get_or_404(item_id)
        data = extract_firing_program_data(form)
        segments = ProgramSegment.query.filter_by(program=item).order_by(ProgramSegment.segment_order).all()
        segment_ids = [segment.segment_id for segment in segments]
        segment_count = len(list(segments))
        print(segment_count)
        
        if form.validate_on_submit():
            # Update the existing object with the new data
            for key, value in data.items():
                setattr(item, key, value)
        
            firing_segments = form.firing_segments.data
            #[segment for segment in form.firing_segments.data if segment['temp_start'] and segment['temp_end']]
        
            print(enumerate(firing_segments))
            for segment_index, segment in enumerate(firing_segments):
                # Extract the segment data
                data_segment = extract_firing_segment_data(segment)
                print(data_segment)
                
                if segment_index + 1 <= segment_count:
                    db_firing_segment = FiringSegment.query.get_or_404(segment_ids[segment_index])
                    
                    if segment['temp_start'] and segment['temp_end']:
                        for key, value in data_segment.items():
                            setattr(db_firing_segment, key, value)
                    else:
                        db.session.delete(db_firing_segment)
                else:
                    if segment['temp_start'] and segment['temp_end']:
                        # Create and add program-segment association to the session
                        db_firing_segment = FiringSegment(**data_segment)
                        program_segment = ProgramSegment(program=item, segment=db_firing_segment,
                                                            segment_order=segment_index)
                    
                        # Add the firing program to the session and commit
                        db.session.add(db_firing_segment)
                        db.session.add(program_segment)
                    
            db.session.commit()
            return jsonify(success=True, message=f'Updated {item_type} with ID {item_id}')
        
    if form.validate_on_submit() and item_type != 'firing-program':
        for key, value in data.items():
                setattr(item, key, value)
        db.session.commit()
        return jsonify(success=True, message=f'Updated {item_type} with ID {item_id}')
    
    response_data = {
        'success': False,
        'errors': form.errors
    }
    print(form.errors)
    return jsonify(response_data)
    
    
@app.route('/get_name_<item_type>/<int:item_id>', methods=['GET'])
@login_required
def get_item_name(item_id, item_type):
    
    if item_type == 'pot':
        item = Pot.query.get_or_404(item_id)
        item_name = item.get_pot_name()
    
    elif item_type == 'link':
        link = Link.query.get_or_404(item_id)
        item_name = link.title
        
    elif item_type == 'clay':
        clay = Clay.query.get_or_404(item_id)
        item_name = clay.get_clay_name()
    
    elif item_type == 'glaze':
        glaze = Glaze.query.get_or_404(item_id)
        item_name = glaze.get_glaze_name()
    
    elif item_type == 'kiln':
        kiln = Kiln.query.get_or_404(item_id)
        item_name = kiln.name
    
    elif item_type == 'firing-program':
        firing_program = FiringProgram.query.get_or_404(item_id)
        item_name = firing_program.name
    
    elif item_type == 'commission':
        commission = Commission.query.get_or_404(item_id)
        item_name = commission.get_name()
    
    return jsonify(item_name=item_name)


@app.route('/image_name/', methods=['GET'])
@login_required
def image_name():
    # image_source is in the format /static/photos/<filename>
    image_source = request.args.get('image_source')
    
    end_pos = image_source.find('/static/photos/') + len('/static/photos/')
    item_name = image_source[end_pos:]
    
    return jsonify(item_name=item_name)


@app.route('/get_<item_type>/<int:item_id>', methods=['GET'])
@login_required
def get_item(item_type, item_id):
    
    if item_type == 'link':
        item = Link.query.get_or_404(item_id)
        data = extract_link_from_object(item)
        
    elif item_type == 'clay':
        item = Clay.query.get_or_404(item_id)
        data = extract_clay_from_object(item)
        
    elif item_type == 'glaze':
        item = Glaze.query.get_or_404(item_id)
        data = extract_glaze_from_object(item)
    
    elif item_type == 'kiln':
        item = Kiln.query.get_or_404(item_id)
        data = extract_kiln_from_object(item)
        
    elif item_type == 'firing-program':
        item = FiringProgram.query.get_or_404(item_id)
        data = extract_firing_program_from_object(item)
        
        for segment_index, segment in enumerate(item.associated_segments):
            data.update(extract_firing_segment_data(segment.segment, segment_index))
        
        segment_count = len(list(item.associated_segments))
        data.update(
            {
                'number_of_segments': segment_count
            }
        )
    elif item_type == 'commission':
        item = Commission.query.get_or_404(item_id)
        data = extract_commission_from_object(item)
        print(data)
        
    else:
        return jsonify(error=f"Unrecognized item type: {item_type}"), 400

    return jsonify(**data)


@app.route('/get_pots_old')
@login_required
def get_pots_old():
    
    pots = Pot.query.order_by(Pot.id).all()
    
    for pot in pots:
        ordered_glaze_layers = PotGlaze.query.filter_by(pot_id=pot.id).order_by(PotGlaze.display_order).all()
        pot.ordered_glaze_layers = ordered_glaze_layers
        
    pots_data = [pot_to_dict(pot) for pot in pots]
    return jsonify(pots_data)