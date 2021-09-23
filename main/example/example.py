import sys
from main.__init__ import db
from flask import (
    Flask, render_template,
    request, redirect, url_for,
    abort, flash, jsonify,
    make_response,
    Blueprint
)
from datetime import datetime as dt
from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy

from main.models import Example
from main.forms import ExampleForm

# Blueprint Configuration
example_bp = Blueprint(
    'example_bp', __name__,
    template_folder='templates'
)

#  ----------------------------------------------------------------
#  Show Examples and example

@example_bp.route('/examples', methods=['GET'])
def examples():
    title = "Examples"
    description = "Let's begin..."
    examples = Example.query.all()
    return render_template('main/index.html', examples=examples,
                            title=title, description=description)

@example_bp.route('/examples/<int:example_id>', methods=['GET'])
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

#  ----------------------------------------------------------------
#  Create example

@example_bp.route('/form', methods=['GET'])
def example_form():
    title = "Create Example"
    description = "Let's begin..."
    form = ExampleForm()
    return render_template('main/form.html', form=form,
                            title=title, description=description)

@example_bp.route('/form', methods=['POST'])
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

#  ----------------------------------------------------------------
#  Edit example

@example_bp.route('/examples/<int:example_id>/edit', methods=['GET', 'POST'])
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

#  ----------------------------------------------------------------
#  Delete example

@example_bp.route('/examples/<int:example_id>', methods=['DELETE'])
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

