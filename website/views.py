from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Weather, User
from . import db
import json
import geocoder
from env import geocoder_key

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/features', methods=['GET', 'POST'])
@login_required
def features():
    if request.method == 'POST':
        location = request.form.get('location')
        pollen = request.form.get('pollen')
        air_quality = request.form.get('airquality')
        forecast = request.form.get('forecast')
        solar = request.form.get('solar')
        phone_number = request.form.get('phonenumber')
        phone_provider = request.form.get('phoneprovider')

        user_location = geocoder.bing(location, key=geocoder_key[0])
        location_json = user_location.json

        if location_json == None:
            flash('Invalid city, try again.', category='error')
        elif len(phone_number) != 10:
            flash('Phone number must be 10 digits long, try again.', category='error')
        elif phone_provider == None:
            flash('Must pick a cell phone provider.', category='error')
        else:
            curr_phone_number = Weather.query.filter_by(phone_number=phone_number).first()
            if curr_phone_number:
                flash('Phone number already exists, try again.', category='error')
            else:
                new_features = Weather(city=location, lat=location_json['lat'], long=location_json['lng'], pollen=pollen, air_quality=air_quality, forecast=forecast, solar=solar, phone_number=phone_number, phone_provider=phone_provider, user_id=current_user.id)
                db.session.add(new_features)
                db.session.commit()
                flash('Features added!', category='success')
                values = Weather.query.all()

                with open('website\static\smsService.txt', 'w') as f:
                    for val in values:
                        f.write(val.city)
                        f.write('#')
                        f.write(val.lat)
                        f.write('#')
                        f.write(val.long)
                        f.write('#')
                        if val.pollen == None:
                            f.write('None')
                            f.write('#')
                        else:
                            f.write(val.pollen)
                            f.write('#')
                        if val.air_quality == None:
                            f.write('None')
                            f.write('#')
                        else:
                            f.write(val.air_quality)
                            f.write('#')
                        if val.forecast == None:
                            f.write('None')
                            f.write('#')
                        else:
                            f.write(val.forecast)
                            f.write('#')
                        if val.solar == None:
                            f.write('None')
                            f.write('#')
                        else:
                            f.write(val.solar)
                            f.write('#')
                        f.write(val.phone_number)
                        f.write('#')
                        f.write(val.phone_provider)
                        f.write('*')   # End of user

    
    return render_template('features.html', user=current_user)


@views.route('/about')
def about():
    return render_template("about.html", user=current_user)



def clear_data(session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clearing:')
        print(table)
        session.execute(table.delete())
    session.commit()



    
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteID = note['noteID']
    note = Note.query.get(noteID)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})








@views.route('/view')
def view():
    # f = db.session.get(Weather,1)
    # db.session.delete(f)
    # db.session.commit()

    clear_data(db.session)

    # values=Weather.query.all()
    # users = User.query.all()
    # print(users)
    # print(values)

    return render_template('view.html', user=current_user)