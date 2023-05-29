from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User
import openai
import regex as re
import os
from flask_mail import Message
from app import mail
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail


@app.route("/")
def home():
	return render_template("index.html")

potential_matches = {}

@app.route("/dashboard")
@login_required
def dashboard():
    approved_by_users = current_user.approved_by.split(";")[0:-1]
    visited_users = current_user.visited_users.split(';')[0:-1]
    #   for username in approved_by_users:
    #       if (username not in visited_users):
    #         user = User.query.filter_by(username=username).first()
    #         similarity_score = compare_users(user, current_user)
    #         potential_matches.append((user, int(similarity_score)))
    if current_user.username not in potential_matches:
        potential_matches[current_user.username] = []
    if len(potential_matches[current_user.username]) == 0:
        for user in User.query.all():
            if (user.matching_lang == current_user.matching_lang) and (user != current_user) and (user.username not in visited_users):
                similarity_score = compare_users(user, current_user)  
                potential_matches[current_user.username].append((user, int(similarity_score)))

    potential_matches[current_user.username] = sorted(potential_matches[current_user.username], key=lambda x: x[1], reverse=True)
    
    # if len(potential_matches[current_user.username]) > 0:
    #     first_match = potential_matches[current_user.username][0][0]
    #     send_match_email(current_user, first_match)

    empty = False
    user = ""
    similarity_score = 0

    if (len(potential_matches[current_user.username]) == 0):
        empty = True
    else:
        user, similarity_score = potential_matches[current_user.username][0]   

    return render_template("dashboard.html", user=user, similarity_score=similarity_score, empty=empty, isModalOpen=False)

@app.route("/approve_user/<username>")
@login_required
def approve_user(username):
    isModalOpen = False
    approved_by_users = current_user.approved_by.split(";")[0:-1]
    visited_users = current_user.visited_users.split(';')[0:-1]
    other_user = User.query.filter_by(username=username).first()
    if (username in approved_by_users):
        # TODO SEND EMAIL TO BOTH USERS
        flash(f"Congratulations! You matched with {username}")
        current_user.approved_by = current_user.approved_by.replace(username + ";", "")
        isModalOpen = True

        # msg = Message("Match Found!", sender="gitmatched@gmail.com", recipients=[current_user.email])
        # msg.body = f"Congratulations! You matched with {username}"
        # mail.send(msg)

        # msg2 = Message("Match Found!", sender="gitmatched@gmail.com", recipients=[other_user.email])
        # msg2.body = f"Congratulations! You matched with {current_user.username}"
        # mail.send(msg2)

        mail.send_message(
            "Match Found!",
            sender='gitmatched@gmail.com',
            recipients=[current_user.email],
            body=f"Congratulations! You matched with {username}"
        )

        mail.send_message(
            "Match Found!",
            sender='gitmatched@gmail.com',
            recipients=[other_user.email],
            body=f"Congratulations! You matched with {current_user.email}"
        )


    else:
        other_user.approved_by += current_user.username + ";"

    current_user.visited_users += username + ";"
    db.session.add(current_user)
    db.session.add(User.query.filter_by(username=username).first())
    db.session.commit()

    user = User.query.filter_by(username=username).first()
    global potential_matches
    if current_user.username not in potential_matches:
        potential_matches[current_user.username] = []

    potential_matches[current_user.username] = list(filter(lambda x: x[0] != user, potential_matches[current_user.username]))

    empty = False
    user = ""
    similarity_score = 0

    if (len(potential_matches[current_user.username]) == 0):
        empty = True
    else:
        user, similarity_score = potential_matches[current_user.username][0] 

    return render_template("dashboard.html", user=user, similarity_score=similarity_score, empty=empty, isModalOpen=isModalOpen)

@app.route("/reject_user/<username>")
@login_required
def reject_user(username):
    approved_by_users = current_user.approved_by.split(";")[0:-1]
    visited_users = current_user.visited_users.split(';')[0:-1]

    if (username in approved_by_users):
        current_user.approved_by = current_user.approved_by.replace(username + ";", "")

    current_user.visited_users += username + ";"
    db.session.add(current_user)
    db.session.commit()

    user = User.query.filter_by(username=username).first()
    global potential_matches
    if current_user.username not in potential_matches:
        potential_matches[current_user.username] = []

    potential_matches[current_user.username] = list(filter(lambda x: x[0] != user, potential_matches[current_user.username]))

    empty = False
    user = ""
    similarity_score = -1

    if (len(potential_matches[current_user.username]) == 0):
        empty = True
    else:
        user, similarity_score = potential_matches[current_user.username][0] 

    return render_template("dashboard.html", user=user, similarity_score=similarity_score, empty=empty, isModalOpen=False)

class UserSimilarity:
    def __init__(self, user, similarity_score):
        self.user = user
        self.similarity_score = similarity_score

def get_user_similarity():
    users = User.query.all()

    user_similarities = []

    for i in range(len(users)):
        if users[i].username == current_user.username: continue
        similarity_score = compare_users(current_user, users[i])

        current_user_similarity = UserSimilarity(users[i], similarity_score)
        user_similarities.append(current_user_similarity)

    user_similarities.sort(key=lambda x: x.similarity_score, reverse=True)

    return user_similarities

def compare_users(user1, user2):
    openai.api_key = "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"
    prompt = f"From 1-100 exclusive, how similar in terms of logic and coding style is the following code? Use the little information provided to come up with any estimate, and only respond with a number. \n {user1.username}'s code: \n {user1.code_snippet} \n {user2.username}'s code: \n {user2.code_snippet}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    similarity_score = extract_similarity_score(response.choices[0].text)
    return similarity_score

def extract_similarity_score(text):
    pattern = r"(?<!\d)(?!0)(?:[1-9]|[1-9][0-9])(?!\d)"
    match = re.search(pattern, text)
    if match:
        similarity_score = float(match.group(0))
    else:
        similarity_score = 0.0

    return similarity_score

# def send_match_email(user1, user2):
#     # message = Mail(
#     #     from_email='sauravk4@illinis.edu',
#     #     to_emails=user1.email,
#     #     subject='Congratulations! You have a new coding partner match!',
#     #     plain_text_content=f'Congratulations! You have matched with {user2.username}. Please follow up with them at sauravk4@illinois.edu if you are interested in continuing the conversation outside of GitMatched!'
#     # )
#     message = Mail(
#         from_email='gitmatched@example.com',
#         to_emails=user1.email,
#         subject='You have a new match on GitMatched!',
#         plain_text_content=f'Congratulations! You have matched with {user2.username}. Please follow up with them at {user2.email} if you are interested in continuing the conversation outside of GitMatched!')

    # try:
    #     sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    #     response = sg.send(message)
    #     print(response.status_code)
    #     print(response.body)
    #     print(response.headers)
    # except Exception as e:
    #     print(e.message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard')
        return redirect(next_page)
    
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, code_snippet="\n" + form.code_snippet.data, code_snippet_lang=form.code_snippet_lang.data, matching_lang=form.matching_lang.data, visited_users="", approved_by="")
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        # flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.code_snippet = "\n" + form.code_snippet.data
        current_user.code_snippet_lang = form.code_snippet_lang.data
        current_user.matching_lang = form.matching_lang.data
        db.session.commit()
        return redirect(url_for("user", username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.code_snippet.data = current_user.code_snippet
        form.code_snippet_lang.data = current_user.code_snippet_lang
        form.matching_lang.data = current_user.matching_lang

    for i in range(len(potential_matches[current_user.username])):
        user = potential_matches[current_user.username][i][0]
        new_similarity_score = compare_users(user, current_user)  
        potential_matches[current_user.username][i] = (user, int(new_similarity_score))

    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
