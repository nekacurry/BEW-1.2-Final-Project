from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from game_app.models import System, Game, User
from game_app.forms import GameForm, SystemForm, SignUpForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt

main = Blueprint('main', __name__)

from game_app import app, db

@main.route('/')
def homepage():
    all_systems = Systems.query.all()
    print(all_systems)
    return render_template('home.html', all_systems=all_systems)

@main.route('/new_system', methods=['GET', 'POST'])
@login_required
def new_system():

    form = SystemForm()

    if form.validate_on_submit():
      new_system = System(
        title = form.title.data,
        purchased = form.purchased.data,
        added_by = current_user
      )
      db.session.add(new_system)
      db.session.commit()
      flash('New system added to collection!')
      return redirect(url_for('main.system_detail', system_id=new_system.id))

    return render_template('new_system.html', form=form)