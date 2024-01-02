from flask import current_app, Blueprint, render_template

indexy = Blueprint('index', __name__)

@indexy.route('/')
@indexy.route('/home')
@indexy.route('/index')
# @login_required
def index():
    
    # Simply render the 'index.html' template
    return render_template('index.html', title='Pottery log')