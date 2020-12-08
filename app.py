import flask
import json
#import core
import secrets
import database


app = flask.Flask("app")


db = database.Database()
db.load_db()

count = 0

@app.route("/auth" , methods = ["GET" , "POST"])
def login():


    if flask.request.method == "GET":
        #считываем куки
        q = flask.request.cookies.get('sid')
        
        res = flask.make_response(flask.render_template("login.html"))

        return res

    elif flask.request.method == "POST":
        data = flask.request.form
        auth_user = database.User(data['login'] , data['pass'])
        result = db.auth(auth_user)

        if result[0]:
            response = flask.make_response(flask.redirect(f"/profile/{data['login']}"))
            response.set_cookie('sid' , result[1])
            return response
        else:
            return (result[1])


@app.route("/reg" , methods = ["GET" , "POST"])
def reg():
    if flask.request.method == "GET":
        return flask.render_template("reg.html")

    elif flask.request.method == "POST":
        data = flask.request.form
        print(data)
        new_user = database.User(data['login'] , data['pass'])
        result = db.registration(new_user)
        print("123")
        if result[0]:
            return 'все ок'
        else: 
            return result[1]


#Для тестирования функций
@app.route("/profile/<id>" , methods = ["GET" , "POST"])
def test(id):
    q = flask.request.cookies.get('sid')

    return flask.render_template('profile.html' )  


@app.route("/" , methods = ["GET"])
def index():
    if flask.request.method == "GET":
        
        q = flask.request.cookies.get('sid')

        data = flask.request.args
        if not data:
           #ген случайных wtl
           wtl = ['python' , 'gamer' , 'english']
           #ген случайных wtt
           wtt = ['guitar' , 'singing' , 'drawing']

           return flask.render_template('index.html' , data = {'wtl' : wtl , 'wtt' : wtt})

        #ищем людей с таким навыком
        result = [
        {'name':'Иван' ,'href': '#' },
        {'name':'Иван' ,'href': '#' },
        {'name':'Иван' ,'href': '#' }]

        return flask.render_template('peoples.html' , data = result)  

@app.route("/secret" , methods = ["GET"])
def view():
    db.view()
    return " "

app.run(debug=True)

    # определить логику пропуска данной странички , если обнаружена сессия
    # настроить редирект после регистрации на профиль пользователя