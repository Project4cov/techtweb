from flask import Flask, render_template, request, redirect, url_for, g
from flask_bootstrap import Bootstrap
import os
import sqlite3 
import sqlite3 as sql
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
import json

DATABASE = 'messages.db'

app = Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'comments.db'),
    SECRET_KEY='development key'
    ))
Bootstrap(app)


app.debug = True

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        
        with db:
            db.execute('CREATE TABLE IF NOT EXISTS messages (messages_id integer primary key,name text,email text,contactnum text,message text)') 
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()



@app.route('/')
@app.route('/techhome.html')
def index():
    return render_template('techhome.html')
    
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')
    
@app.route('/services')
def services():
    return render_template('services.html')
    
@app.route('/previousrepairs')
def previousrepairs():
    return render_template('previousrepairs.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/contactus', methods=["GET", "POST"])
def contactus():
    
    if request.method == "POST":
        
        name = request.form['name']
        email = request.form['email']
        contactnum = request.form['contactnum']
        message = request.form['message']
        
        conn = get_db()
        
        with conn:
            query = 'INSERT INTO messages (name,email,contactnum,message) VALUES(?,?,?,?)'
            conn.execute(query, (name, email, contactnum, message))
        
        
        response = {"message": "Thank you for getting in touch, someone from our team will get into contact shortly"}
        
   
         
        return json.dumps(response)
            
        
    else:
        return render_template('contactus.html')


@app.route('/testimonials')
def testimonials():
    return render_template('testimonials.html')
    

class CommentForm(Form):
    name = StringField('Name:', validators=[DataRequired()])
    comments = TextAreaField('Comments', validators=[DataRequired(), Length(min=5, max=500)])
    submit = SubmitField('Submit')

@app.route('/testimonials', methods=['GET', 'POST'])
def view_form():
    form = CommentForm()
    if form.validate_on_submit():
        name = form.name.data
        comments = form.comments.data
        with sqlite3.connect(app.config['DATABASE']) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO comments_table (name, comments) VALUES (?,?)", (name, comments))
            con.commit()

        return redirect(url_for('list_results'))
    return render_template('form_wtf.html', form=form)

@app.route('/display')
def list_results():
    with sqlite3.connect(app.config['DATABASE']) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM comments_table")
        entries = cur.fetchall()
        return render_template('flask_sqlite.html', entries=entries)
        



if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))



   