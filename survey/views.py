from flask import render_template, request, redirect
from survey import app, db
from survey.models import Question, Category, MCQuestion

@app.route('/', methods=['GET'])
def home():
    questions = Question.query.all()
    mcquestions = MCQuestion.query.all()
    context = {'questions':questions, 'mcquestions':mcquestions, 'categories':Category.query.all(),'number_of_questions':len(questions)}
    return render_template('index.html', **context)

#new survey
@app.route('/questions/new', methods=['GET'])
def new_questions():
    context = {'categories':Category.query.all()}
    return render_template('new.html', **context)


#creating a new survey
@app.route('/questions', methods=['POST'])
def create_questions():
    if request.form["question_text"].strip() != "":
        category = request.form["category"]
        mycat = int(category)
        new_question = Question(question_text=request.form["question_text"], category_id = mycat)
        db.session.add(new_question)
        db.session.commit()
        message = "Successfully added a new poll!"
    else:
        message = "Poll question should not be an empty string!"

    context = {'questions': Question.query.all(), 'mcquestions':MCQuestion.query.all(), 'categories':Category.query.all(),'message': message}
    return render_template('index.html', **context)

@app.route('/questions/mc', methods=['POST'])
def create_mc_questions():
    if request.form["question_text"].strip() != "":
        my1 = request.form["response_text_1"]
        my2 = request.form["response_text_2"]
        my3 = request.form["response_text_3"]
        my4 = request.form["response_text_4"]
        category = request.form["category"]
        mycat = int(category)
        new_question = MCQuestion(question_text=request.form["question_text"], response_text_1=my1, response_text_2=my2, response_text_3=my3, response_text_4=my4, category_id=mycat)
        db.session.add(new_question)
        db.session.commit()
        message = "Successfully added a new poll!"
    else:
        message = "Poll question should not be an empty string!"

    context = {'questions': Question.query.all(), 'mcquestions':MCQuestion.query.all(), 'categories':Category.query.all(), 'message': message}
    return render_template('index.html', **context)


#displaying a survey
@app.route('/questions/<int:question_id>', methods=['GET'])
def show_questions(question_id):
    context = {'question': Question.query.get(question_id)}
    return render_template('show.html', **context)


@app.route('/questions/mc/<int:question_id>', methods=['GET'])
def show_mc_questions(question_id):
    context = {'myquestion': MCQuestion.query.get(question_id)}
    return render_template('show_mc.html', **context)


#deleting a survey
@app.route('/questions/<int:question_id>', methods=['POST'])
def delete_questions(question_id):
    question = Question.query.get(question_id)
    db.session.delete(question)
    db.session.commit()
    context = {'questions': Question.query.all(), 'mcquestions':MCQuestion.query.all(), 'categories':Category.query.all(), 'message': 'Successfully deleted'}
    return render_template('index.html', **context)

@app.route('/questions/mc/<int:question_id>', methods=['POST'])
def delete_mc_questions(question_id):
    question = MCQuestion.query.get(question_id)
    db.session.delete(question)
    db.session.commit()
    context = {'questions': Question.query.all(), 'mcquestions':MCQuestion.query.all(), 'categories':Category.query.all(), 'message': 'Successfully deleted'}
    return render_template('index.html', **context)


#new vote form to cast a vote in a survey
@app.route('/questions/<int:question_id>/vote', methods=['GET'])
def new_vote_questions(question_id):
    question = Question.query.get(question_id)
    context = {'question': question}
    return render_template('vote.html', **context)

@app.route('/questions/mc/<int:question_id>/vote', methods=['GET'])
def new_vote_mc_questions(question_id):
    question = MCQuestion.query.get(question_id)
    context = {'myquestion': question}
    return render_template('vote_mc.html', **context)

#casting a vote to a particular choice in a survey
@app.route('/questions/<int:question_id>/vote', methods=['POST'])
def create_vote_questions(question_id):
    question = Question.query.get(question_id)

    if request.form["vote"] in ["yes", "no", "maybe"]:
        question.vote(request.form["vote"])

    db.session.add(question)
    db.session.commit()
    return redirect("/questions/%d" % question.id)

@app.route('/questions/mc/<int:question_id>/vote', methods=['POST'])
def create_vote_mc_questions(question_id):
    question = MCQuestion.query.get(question_id)

    if request.form["vote"] in ["1", "2", "3", "4"]:
        question.vote(request.form["vote"])

    db.session.add(question)
    db.session.commit()
    return redirect("/questions/mc/%d" % question.id)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500