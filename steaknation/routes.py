from flask import render_template, url_for, redirect, flash, request, abort
from steaknation.forms import (ReservationForm, LoginForm, RegisterForm, DeleteAccountForm,
                               DeleteReservationForm, UpdateAccountForm)
from steaknation import app, db, flask_bcrypt, ADMIN_NAME, ADMIN_PHONE_NUMBER
from steaknation.models import Reservation, User
from datetime import datetime
from flask_login import login_required, login_user, current_user, logout_user


@app.route('/')
@app.route('/home')
def home_page():
    data_list = [
        {
            'img': url_for('static', filename='images/main-menu/img-1.jpg'),
            'heading': "Fine dining experience",
            'data': "Get comfortable in our beautiful restuarant with a modern aesthetic in the middle of the city!",
            'image_source': """The data goes here
                        Photo by Bundo Kim, site: "https://unsplash.com/@bundo?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash" 
                        on Unsplash site: "https://unsplash.com/photos/dining-table-and-chair-set-under-four-lighted-pendant-lamps-Pb9bUzH1nD8?utm_content=
                        creditCopyText&utm_medium=referral&utm_source=unsplash"""
        },
        {
            'img': url_for('static', filename='images/main-menu/img-2.jpg'),
            'heading': "Quality customer service",
            'data': "We pride ourselves in our customer service, come through and see why!",
            'image_source': """Photo by Adrien Olichon, site: "https://unsplash.com/@adrienolichon?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash"
                 on Unsplash, site: "https://unsplash.com/photos/empty-table-and-chairs-inside-building-ZgREXhl8ER0?utm_content=
                 creditCopyText&utm_medium=referral&utm_source=unsplash"""
        }
    ]
    return render_template('home.html', data_list=data_list)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('reservations_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(phone_number=form.phone_number.data).first()
        if user and flask_bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash(f'{user.fullname}: You have successfully logged in!', 'success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('reservations_page'))
        else:
            flash('Incorrect phone number or password. Please check your details.', 'danger')

    return render_template('login.html', form=form, data_list="")


@app.route('/logout', methods=['GET', 'POST'])
def logout_page():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('home_page'))


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        # Create user and add to the database
        if form.email.data != "None@email.com":
            email = form.email.data
        else:
            email = None
        user = User(
            fullname=form.fullname.data,
            phone_number=form.phone_number.data,
            password_hash=flask_bcrypt.generate_password_hash(form.password.data),
            email=email
        )
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered!', 'success')
        return redirect(url_for('login_page'))
    return render_template('register.html', form=form, data_list="")


@app.route('/menu')
def menu_page():
    return render_template('menu.html', data_list="")


@app.route('/reservations', methods=['GET', 'POST'])
@login_required
def reservations_page():
    form = ReservationForm()
    delete_res_form = DeleteReservationForm()
    delete_acc_form = DeleteAccountForm()
    update_account_form = UpdateAccountForm()

    # Creating a new reservation
    if form.validate_on_submit():
        # Create a datetime object from the data given
        dt = datetime.combine(form.date.data, form.time.data)

        # Create a reservation object and save in database
        reservation = Reservation(
            datetime=dt,
            number_of_people=form.num_of_people.data,
            comment=form.comment.data,
            user_phone=current_user.phone_number
        )
        db.session.add(reservation)
        db.session.commit()

        flash("Your reservation was successfully submitted. We will keep in touch. Thank you!", 'success')
        return redirect(url_for('reservations_page'))

    reservations = Reservation.query.filter_by(user_phone=current_user.phone_number).all()
    all_users = User.query.all()
    return render_template('reservations.html', form=form, reservations=reservations, all_users=all_users,
                           delete_res_form=delete_res_form, delete_acc_form=delete_acc_form,
                           update_account=update_account_form, ADMIN_NAME=ADMIN_NAME, ADMIN_PHONE_NUMBER=ADMIN_PHONE_NUMBER)


@app.route('/delete/reservation/<int:reservationID>', methods=['POST'])
def delete_reservation(reservationID):
    reservation = Reservation.query.get_or_404(reservationID)
    if reservation.user_phone != current_user.phone_number:
        abort(403)
    db.session.delete(reservation)
    db.session.commit()
    flash('That reservation has been deleted successfully...', 'success')
    return redirect(url_for('reservations_page'))


@app.route('/delete/account', methods=['POST'])
def delete_account():
    # Delete the account's reservations is any
    reservations = Reservation.query.filter_by(user_phone=current_user.phone_number)
    for reservation in reservations:
        db.session.delete(reservation)
    db.session.delete(current_user)
    db.session.commit()
    logout_user()
    flash('Your account has been deleted successfully!', 'success')
    return redirect(url_for('home_page'))


@app.route('/update/account', methods=['POST'])
def update_account():
    new_email = request.form.get('change_email')
    new_password = request.form.get('change_password')
    if new_email:
        current_user.email = new_email
    if new_password:
        current_user.password_hash = flask_bcrypt.generate_password_hash(new_password)
    if new_email or new_password:
        db.session.commit()
        flash('Your account information has been updated successfully!', 'success')
    return redirect(url_for('reservations_page'))


@app.route('/staff')
def staff_page():
    data_list = [
        {
            'img': url_for('static', filename='images/staff/staff3.jpg'),
            'heading': "Kitchen Staff",
            'data': "Meet the men and women that are the backbone of our fine establishment...",
            'image_source': """https://www.google.com/url?sa=i&url=https%3A%2F%2Forders.co%2Fblog%2
            Frestaurant-management-best-practices%2F&psig=AOvVaw1KKtV3tyZL1tV2KKw_KWlL&ust=1705054413665000&source=
            images&cd=vfe&opi=89978449&ved=0CBMQjRxqGAoTCODhgu6M1YMDFQAAAAAdAAAAABCFAQ"""
        },
        {
            'img': url_for('static', filename='images/staff/staff1.jpg'),
            'heading': "Bar man",
            'data': "George mans the bar... Best in the business!",
            'image_source': """https://t4.ftcdn.net/jpg/06/46/53/71/360_F_646537198_oZ9RTNuUXQfA7XFpVJyTvpFvCge7WOsx.jpg"""
        },
        {
            'img': url_for('static', filename='images/staff/staff2.jpg'),
            'heading': "Waiters",
            'data': "The fine lady and gentleman that will serve you your food!",
            'image_source': """https://static.vecteezy.com/system/resources/previews/030/472/599/large_2x/smiling-male-
            and-female-staff-in-a-restaurant-ai-generated-photo.jpg"""
        }
    ]
    return render_template('staff.html', data_list=data_list)
