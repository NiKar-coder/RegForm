from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.forms import RegisterForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/")
def journal_works():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return render_template("journal_works.html", title='List of Jobs',
                           jobs=jobs)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm.data:
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="Passwords don't match")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.login.data).first():
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="This user already exists")
        user = User(
            name=form.name.data,
            email=form.login.data,
            address=form.address.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            surname=form.surname.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Registration', form=form)


def main():
    name_db = 'mars_explorer.sqlite'
    db_session.global_init(f"db/{name_db}")

    app.run(port=8080)


if __name__ == '__main__':
    main()
