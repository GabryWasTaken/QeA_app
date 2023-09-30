from flask import Flask , render_template, url_for, g , request, session , redirect
from database import get_db , connect_db
import hashlib
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24) #Genera una stringa di 24 caratteri unicode
#Questa stringa appena generata sarà l'identificativo della sessione dell'utente appena loggato

@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def index():
    user = get_session_user()
    db = get_db()
    result= 1
    cur = db.execute('''SELECT questions.id,questions.question_text, askers.username AS asker_name, experts.username AS expert_name
                     FROM questions 
                     JOIN users AS askers ON askers.id = questions.asked_by_id
                     JOIN users AS experts ON experts.id = questions.expert_id
                     WHERE questions.answer_text IS NOT NULL
                     ''')
    result = cur.fetchall()

    return render_template("home.html",user=user,result=result)

@app.route('/answer/<question_id>', methods=["GET","POST"])
def answer(question_id):
    db = get_db()
    user = get_session_user()
    if not user:
        return redirect(url_for('index'))
    
    if user['expert'] == 0:
        return redirect(url_for('index'))

    if request.method == 'POST':
        db.execute("UPDATE questions SET answer_text = ? WHERE id = ?",[request.form['answer'],question_id])
        db.commit()
        return redirect(url_for('unanswered'))

    quest_cur = db.execute("SELECT id,question_text FROM questions WHERE id = ?",[question_id])
    question = quest_cur.fetchone()

    return render_template("answer.html",user=user,question=question)

@app.route('/login' , methods=['GET','POST'])
def login():
    user = get_session_user()
    if request.method == 'POST':
        db = get_db()
        name = request.form['inputName']
        encoded_pass= hashlib.sha256(request.form['inputPassword'].encode())
        encoded_pass=encoded_pass.hexdigest()
        cur = db.execute("SELECT username,password FROM users where username = ?",[name])
        result = cur.fetchone()

        #Try catch inserito per evitare  TypeError in caso di credenziali errate
        try:
            check_name = result['username'] 
            check_pass = result['password']
        except TypeError:
            check_pass = None
            check_name = None

        if name == check_name and encoded_pass == check_pass:
            session['user'] = result['username']
            return redirect(url_for('index'))
        else:
            return render_template("login.html",user=user,check="NO_USER")
    return render_template("login.html",user=user,check=None)

@app.route('/register' , methods=["GET","POST"])
def register():
    user = get_session_user()
    if request.method == 'POST':
        db = get_db()
        encoded_pass= hashlib.sha256(request.form['inputPassword'].encode())
        encoded_pass=encoded_pass.hexdigest()
        name = request.form["inputName"]
        cur = db.execute("SELECT username FROM users WHERE username = ?",[name])
        result = cur.fetchone()

        try:
            check_name = result['username']
        except TypeError:
            check_name = None

        if check_name != name:
            db.execute('''INSERT INTO users (username,password,expert,admin) 
                                VALUES (?,?,?,?)''',[name,encoded_pass,'0','0'])
            db.commit()
            session['user'] = name
            return redirect(url_for('index'))
        elif check_name == name:
            return render_template("register.html",user=user,check="USER_ALREDY_EXIST")
        #Per settare admin il primo utente eseguire la query -> UPDATE users SET admin = '1' WHERE id = 1;

    return render_template("register.html",user=user,check=None)

@app.route('/question/<question_id>')
def question(question_id):
    user = get_session_user()
    db = get_db()

    cur = db.execute('''SELECT 
                     questions.id,questions.question_text,questions.answer_text,askers.username AS asker_name, experts.username AS expert_name
                     FROM questions 
                     JOIN users AS askers ON askers.id = questions.asked_by_id
                     JOIN users AS experts ON experts.id = questions.expert_id
                     WHERE questions.id = ?
                     ''',[question_id])
    result = cur.fetchone()



    return render_template("question.html",user=user,result=result)

@app.route('/ask', methods=["GET","POST"])
def ask():
    user = get_session_user()
    db = get_db()
    cur = db.execute("SELECT * FROM users WHERE expert = True")
    expert_list = cur.fetchall()

    if request.method == "POST":
        if user:
            db.execute('''INSERT INTO questions (question_text,asked_by_id,expert_id) 
                                VALUES (?,?,?)''',[request.form['textArea'],user['id'],request.form['expert']])
            db.commit()
            return render_template("ask.html",user=user,expert_list=expert_list,check=None)
        else:
            return render_template("ask.html",user=user,expert_list=expert_list,check="NO_LOGIN")
        
    return render_template("ask.html",user=user,expert_list=expert_list,check=None)

@app.route('/unanswered')
def unanswered():
    user = get_session_user()
    db = get_db()
    if not user:
        redirect(url_for('login'))
    
    if user['expert'] == 0:
        redirect(url_for('index'))

    questions_cur = db.execute('''SELECT 
            questions.id, questions.question_text , users.username
            FROM questions 
            JOIN users ON users.id = questions.asked_by_id
            WHERE questions.answer_text IS NULL AND questions.expert_id = ?
            ''',[user['id']])
    questions = questions_cur.fetchall()
    return render_template("unanswered.html",user=user,questions=questions,check=None)


@app.route('/users')
def users():
    user = get_session_user()
    db = get_db()
    if not user:
        return redirect(url_for("login"))
    
    if user['admin'] == 0:
        return redirect(url_for("index"))

    cur = db.execute("SELECT * FROM users")
    result = cur.fetchall()

    return render_template("users.html",user=user,users=result)

@app.route("/logout")
def logout():
    user = get_session_user()
    session['user'] = None
    return redirect(url_for('index'))

def get_session_user():
    db = get_db()
    result_user = None
    if 'user' in session:
        user = session['user']
        cur = db.execute("SELECT * FROM users where username = ?",[user])        
        result_user = cur.fetchone()
    return result_user

@app.route('/promote/<user_id>')
def promote(user_id):
    try:
        user = session['user']
    except:
        user = None
    db = get_db()
    cur = db.execute('SELECT * FROM users WHERE username = ? ',[user])
    res = cur.fetchone()
    try:
        check_admin = res['admin']
    except:
        check_admin = None

    if check_admin == True:
        db.execute("UPDATE users SET expert = 1 WHERE id = ? ",[user_id])
        db.commit()
        return redirect(url_for('users'))
    else:
        return redirect(url_for('users'))

@app.route('/demote/<user_id>')
def demote(user_id):
    try:
        user = session['user']
    except:
        user = None
    db = get_db()
    cur = db.execute('SELECT * FROM users WHERE username = ? ',[user])
    res = cur.fetchone()
    try:
        check_admin = res['admin']
    except:
        check_admin = None

    if check_admin == True:
        db.execute("UPDATE users SET expert = 0 WHERE id = ? ",[user_id])
        db.commit()
        return redirect(url_for('users'))
    else:
        return redirect(url_for('users'))


if __name__ == '__main__':
    app.run(debug=True)