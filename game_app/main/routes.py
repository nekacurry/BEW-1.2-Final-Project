from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from game_app.models import System, Game, User
from game_app.main.forms import GameForm, SystemForm
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt

main = Blueprint('main', __name__)

from game_app import app, db

@main.route('/')
def homepage():
    all_systems = System.query.all()
    print(all_systems)
    return render_template('home.html', all_systems=all_systems)

@main.route('/new_system', methods=['GET', 'POST'])
@login_required
def new_system():

    form = SystemForm()

    if form.validate_on_submit():
      new_system = System(
        name = form.name.data,
        purchased = form.purchased.data,
        added_by = current_user
      )
      db.session.add(new_system)
      db.session.commit()
      flash('New system added to collection!')
      return redirect(url_for('main.system_detail', system_id=new_system.id))

    return render_template('new_system.html', form=form)

@main.route('/new_game', methods=['GET', 'POST'])
@login_required
def new_item():

    form = GameForm()

    if form.validate_on_submit():
      new_game = Game(
        title = form.title.data,
        genre = form.genre.data,
        photo_url = form.photo_url.data,
        purchased = form.purchased.data,
        system = form.system.data,
        added_by = current_user
      )
      db.session.add(new_game)
      db.session.commit()
      flash('New game added to collection!')
      return redirect(url_for('main.game_detail', item_id=new_item.id))

    return render_template('new_game.html', form=form)

@main.route('/system/<system_id>', methods=['GET', 'POST'])
@login_required
def store_detail(system_id):
    system = System.query.get(system_id)
   
    form = SystemForm(obj=system)

    if form.validate_on_submit():
      system.name = form.name.data,
      system.purchased = form.purchased.data
      
      db.session.add(system)
      db.session.commit()
      flash('System updated!')
      return redirect(url_for('main.system_detail', store_id=system.id))

    system = System.query.get(system_id)
    return render_template('system_detail.html', system=system, form=form)