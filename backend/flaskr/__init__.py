import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    setup=1
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response
        CORS(app, resources={"/": {"origins": "*"}})

    QUESTIONS_PER_PAGE = 10

    def paginate_questions(request, selection):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        qu = [question.format() for question in selection]
        current_questions = qu[start:end]
        return current_questions

    # we have a  GET requests for all  categories.
    @app.route("/categories", methods=["GET"])
    def get_gategories():

        res = Category.query.all()
        if len(res) == 0:
            abort(404)
        current = paginate_questions(request, res)
        d = {}
        for i in current:
            d[str(i["id"])] = str(i["type"])
        print(d)
        return jsonify({"categories": d, "success": True})

    # GET requests for questions per  10 questions
    # returns a list of questions, number of total ...
    @app.route("/questions", methods=["GET"])
    def get_questions():
        qes = Question.query.all()
        qe = paginate_questions(request, qes)

        res = Category.query.all()
        if len(res) == 0:
            abort(404)
        current = paginate_questions(request, res)

        d = {}
        for i in current:
            d[str(i["id"])] = str(i["type"])

        d1 = {}
        l = []
        for i in qes:
            d1["id"] = i.id
            d1["question"] = i.question
            d1["answer"] = i.answer
            d1["difficulty"] = i.difficulty
            d1["category"] = i.category

            l.append(d1)
            d1 = {}

        return jsonify(
            {    "success":True,
                "questions": l,
                "totalQuestions": 100,
                "categories": d,
                "currentCategory": "History",
            }
        )

    # DELETE question with his  ID.
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)
            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "questions": current_questions,
                    "total_questions": len(selection),
                }
            )

        except Exception:
            abort(422)

    """POST a new question, which you must  
    put the  question and answer text and
    category"""
    @app.route("/questions", methods=["POST"])
    def add_question():
        try:
            body = request.get_json()

            if body.get("searchTerm", None):
                return search_team(body.get("searchTerm", None))

            print("ffff")
            new_question = body.get("question", None)
            new_answer = body.get("answer", None)
            new_category = body.get("category", None)
            new_difficulty = body.get("difficulty", None)
            if new_question is None:
                print("none")
                return jsonify({"success": False})
            p = Question(
                question=new_question,
                answer=new_answer,
                category=new_category,
                difficulty=new_difficulty,
            )

            p.insert()
            return jsonify({"success": True})
        except Exception:
            abort(422)

    # POST endpoint to get questions based on a search term
    @app.route("/questions", methods=["POST"])
    def search_team(search):
        print("inside search hiiiiiiiiiiiiiiiiiiiiiiii")
        try:
            questions = Question.query.filter(
                Question.question.ilike(f"%{search}%")
            ).all()
            d = paginate_questions(request, questions)
            print(d)
            return jsonify(
                {
                    "success": True,
                    "questions": d,
                    "total_questions": len(questions),
                    "currentCategory": "Entertainment",
                }
            )
        except Exception:
            abort(422)

    # GET questions based on category.
    @app.route("/categories/<int:cat_id>/questions", methods=["GET"])
    def get_item_by_gat(cat_id):

        res = Question.query.filter(Question.category == str(cat_id)).all()

        cat = Category.query.filter(Category.id == cat_id).one_or_none()
        if cat is None:
            abort(404)
        print(cat.type)
        return jsonify(
            {
                "success": True,
                "questions": [i.format() for i in res],
                "totalQuestions": len(Question.query.all()),
                "currentCategory": cat.type,
            }
        )
    # POST endpoint to for  the quiz, it takes category and previous 
    
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():
      body = request.get_json()
      try:
       prv= body.get('previous_questions')

      
       quiz = body.get('quiz_category')['id']
      
      
       if (prv is None):
              abort(400)

       questions = []
       if quiz == 0 :
         questions = Question.query.filter(Question.id.notin_(prv)).all()
       else:
         category = Category.query.get(quiz)
         if category is None:
          abort(404)
         questions = Question.query.filter(Question.id.notin_(prv),Question.category == quiz).all()
       current_question = None
       if(len(questions)>0):
        index = random.randrange(0, len(questions))
        current_question = questions[index].format()
       return jsonify({
             
              'question':current_question,
             
              })
      except Exception as e:
       abort(400)


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"state": False, "error": 404, "message": "NOT FOUND !!!"}), 404

    @app.errorhandler(500)
    def server_error(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 500,
                    "message": "THRE IS SOME PROBLEM IN SERVER ",
                }
            ),
            500,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 422,
                    "message": "THIS ACTION CAN'T BE PRECESSED",
                }
            ),
            422,
        )

    return app
