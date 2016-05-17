from survey import db


class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question_text = db.Column(db.String(200))
    number_of_yes_votes = db.Column(db.Integer, default=0)
    number_of_no_votes = db.Column(db.Integer, default=0)
    number_of_maybe_votes = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer)

    def __init__(self, question_text, category_id, number_of_yes_votes=0, 
                     number_of_no_votes=0, number_of_maybe_votes=0):
        
        self.question_text = question_text

        self.number_of_yes_votes = number_of_yes_votes
        self.number_of_no_votes = number_of_no_votes
        self.number_of_maybe_votes = number_of_maybe_votes
        self.category_id = category_id


    def vote(self, vote_type):
        if vote_type == 'yes':
            self.number_of_yes_votes += 1
        elif vote_type == 'no':
            self.number_of_no_votes += 1
        elif vote_type == 'maybe':
            self.number_of_maybe_votes += 1

        else:
            raise Exception("Invalid vote type")

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def __init__(self, name):
        self.name = name

class MCQuestion(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question_text = db.Column(db.String(200))
    response_text_1 = db.Column(db.String(200))
    response_text_2 = db.Column(db.String(200))
    response_text_3 = db.Column(db.String(200))
    response_text_4 = db.Column(db.String(200))
    number_of_1 = db.Column(db.Integer, default=0)
    number_of_2 = db.Column(db.Integer, default=0)
    number_of_3 = db.Column(db.Integer, default=0)
    number_of_4 = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer)

    def __init__ (self, question_text, response_text_1,response_text_2,response_text_3,response_text_4, category_id, number_of_1=0,number_of_2=0,number_of_3=0,number_of_4=0):
        self.question_text = question_text
        self.response_text_1 = response_text_1
        self.response_text_2 = response_text_2
        self.response_text_3 = response_text_3
        self.response_text_4 = response_text_4
        self.number_of_1 = number_of_1
        self.number_of_2 = number_of_2
        self.number_of_3 = number_of_3
        self.number_of_4 = number_of_4
        self.category_id = category_id

    def vote(self, vote_type):
        if vote_type == '1':
            self.number_of_1 += 1
        elif vote_type == '2':
            self.number_of_2 += 1
        elif vote_type == '3':
            self.number_of_3 += 1
        elif vote_type == '4':
            self.number_of_4 += 1

        else:
            raise Exception("Invalid vote type")


