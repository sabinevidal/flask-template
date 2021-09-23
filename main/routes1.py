import os
import sys
import imghdr
from . import db
from flask import (
    Flask, render_template,
    request, redirect, url_for,
    abort, flash, jsonify,
    make_response
)
from datetime import datetime as dt
from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

from .models import Example
from .forms import ExampleForm

@app.route('/', methods=['GET'])
def home():
    title = "Welcome!"
    description = "Let's begin..."
    return render_template('app/index.html')

#  ----------------------------------------------------------------
#  Show Examples and example
#  ----------------------------------------------------------------

@app.route('/examples', method=['GET'])
def examples():
    title = "Examples"
    description = "Let's begin..."
    examples = Example.query.all()
    return render_template('main/index.html', examples=examples,
                            title=title, description=description)

@app.route('/examples/<int:example_id', method=['GET'])
def show_example(example_id):
    example = Example.query.filter_by(id=example_id).first()
    title = "Example " + example.name
    description = "Let's begin..."

    details = {
        "id": example.id,
        "name": example.name,
        "email": example.email
    }
    return render_template('main/single.html', example=details,
                            title=title, description=description)

#  Create example
#  ----------------------------------------------------------------
@app.route('/form', methods=['GET'])
def example_form():
    title = "Create Example"
    description = "Let's begin..."
    form = ExampleForm()
    return render_template('main/form.html', form=form,
                            title=title, description=description)

@app.route('/form', methods=['POST'])
def example_create():
    form = ExampleForm()
    name = form.name.data
    email = form.email.data

    new_example = Example(name=name, email=email)

    try:
        new_example.insert()
        flash(request.form['name'] + ' was successfully listed!')
    except Exception as e:
        db.session.rollback()
        print(sys.exc_info())
        flash('A database insertion error occurred. '
                + request.form['name'] + ' could not be listed.')
        print(e)
    finally:
        db.session.close()
    return redirect('main/index.html')

#  Edit example
#  ----------------------------------------------------------------
@app.route('/examples/<int:example_id/edit', method=['GET', 'POST'])
def example_edit(example_id):
    title = "Edit Example"
    description = "Let's begin..."
    form = ExampleForm()
    example = Example.query.filter_by(id=example_id).one_or_none()

    if example is None:
        abort(404)

    if request.method == 'GET':
        example = {
            "id": example.id,
            "name": example.name,
            "email": example.email
        }

        # form placeholders with current data
        form.name.process_data(example['name'])
        form.email.process_data(example['email'])

        return render_template('main/form.html', example=example,
                                title=title, description=description)

    elif request.method == 'POST':
        try:
            example.name = form.name.data
            example.email = form.email.data

            example.update()
        except Exception as e:
            db.session.rollback()
            print(sys.exc_info())
            flash('An error occurred. '
                    + example.name + ' could not be updated.')
            print(e)
        finally:
            db.session.close()

        return redirect(url_for('show_example', example_id=example_id))




#  Delete example
#  ----------------------------------------------------------------
@app.route('/examples/<int:example_id', method=['DELETE'])
def example_delete(example_id):
    example = Example.query.filter(Example.id == example_id).first()
    name = example.name

    try:
        example.delete()
        flash('Example ' + name + ' was successfully deleted.')
    except Exception as e:
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. '
                + example.name + ' could not be deleted.')
        print(e)
    finally:
        db.session.close()

    return redirect('/examples')


# ----------------------------------------------------------------- 
# Error handlers
#  ----------------------------------------------------------------
@app.errorhandler(400)
def bad_request_error(error):
    title = "400 Error"
    description = "Bad request"
    return render_template('main/error.html', title=title,
                            description=description), 400
@app.errorhandler(404)
def not_found_error(error):
    title = "404 Error"
    description = "Resource not found"
    return render_template('main/error.html', title=title,
                            description=description), 404
@app.errorhandler(422)
def unprocessable(error):
    title = "422 Error"
    description = "Unprocessable"
    return render_template('main/error.html', title=title,
                            description=description), 422
@app.errorhandler(500)
def server_error(error):
    title = "500 Error"
    description = "Internal server error"
    return render_template('main/error.html', title=title,
                            description=description), 500

# TODO: finish AuthError

# @app.errorhandler(AuthError)
# def handle_auth_error(ex):
#     message = ex.error['description']
#     response = jsonify(ex.error)
#     response.status_code = ex.status_code
#     print('AUTH ERROR: ', response.get_data(as_text=True))
#     flash(f'{message} Please login.')
#     return redirect('/')
