from flask import Flask, current_app, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from pkg_resources import require
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)



# @app.get('/')
# def index():
#     """renders page to show user title of survey"""
#     return render_template('survey_start.html',
#                         survey = survey)

@app.get('/')
def index():
    """renders page to show user title of survey"""

    return render_template('survey_select.html',
                        surveys = surveys)
                        # surveys = surveys) # list of keys ["satisfaction", "personality"]

@app.post('/begin')
def begin():
    """when user clicks start button, should redirect to questions/0 route"""
    session['responses'] = []
    session['survey'] = request.form.get('survey-dropdown')
    return redirect('/questions/0')

@app.get('/questions/<int:question_num>')
def questions(question_num):
    """generates the question in survey with options for answers"""

    current_question_num = len(session['responses']) #min 29-32

    print(session['survey'])
    breakpoint()
    if current_question_num == len(session['survey'].questions):
        return redirect('/thanks')
    elif question_num != current_question_num:
        flash('Stop that!')
        return redirect(f'/questions/{current_question_num}')
    else:
        question = session['survey'].questions[question_num]
        return render_template('question.html',
                                question = question,
                                )

@app.post('/answer')
def answer():
    """appends answer to responses list and redirects to next question or thank
    you if last question"""

    responses = session['responses']
    responses.append(request.form['answer'])
    session['responses'] = responses
    question_num = len(responses)
    if question_num < len(session['survey'].questions):
        return redirect(f'/questions/{question_num}')
    else:
        return redirect('/thanks')

@app.get('/thanks')
def thanks():
    """renders thank you form for completing survey to user"""

    return render_template('/completion.html')