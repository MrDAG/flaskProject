from urllib import request

from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from pydantic_core.core_schema import nullable_schema
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    price = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')
@app.route('/accessories')
def accessories():  # put application's code here
    return render_template('accessories.html')

@app.route('/payment')
def payment():
    return render_template('payment.html')


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()

    return render_template("posts.html", articles=articles)

@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)

@app.route('/posts/<int:id>/del')
def post_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении статьи произошла ошибка"


    return render_template("post_detail.html", article=article)

def post_update(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.add(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении статьи произошла ошибка"


    return render_template("post_detail.html", article=article)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.name = request.form['name']
        article.intro = request.form['intro']
        article.text = request.form['text']
        article.price = request.form['price']


        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При редактировании статьи произошла ошибка"
    else:
        return render_template('post_update.html', methods=['POST', 'GET'])

@app.route('/posts/-article', methods=['POST', 'GET'])
def create_article(id):
     if request.method == "POST":
         name = request.form['name']
         intro = request.form['intro']
         text = request.form['text']
         price = request.form['price']

         article = Article(name=name, intro=intro, text=text, price=price)

         try:
             db.session.add(article)
             db.session.commit()
             return redirect('/posts')
         except:
             return "При добавлении статьи произошла ошибка"
     else:
         return render_template('create-article.html', methods=['POST', 'GET'])


@app.route('/')
def hello_world():  # put application's code here
    return "Hello World!"



if __name__ == '__main__':
    app.run(debug=True)
