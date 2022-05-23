from flask import Flask, render_template, url_for, request, redirect

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)


class Articl(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    intro=db.Column(db.String(300),nullable=False)
    text=db.Column(db.Text,nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Artical %r>' % self.id

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/post')
def post():
    article=Articl.query.order_by(Articl.date.desc()).all()
    return render_template('post.html',articl=article)


@app.route('/post/<int:id>')
def post_detail(id):
    articl=Articl.query.get(id)
    return render_template('post_deteil.html',articl=articl)

@app.route('/post/<int:id>/delete')
def post_delete(id):
    articl=Articl.query.get_or_404(id)

    try:
        db.session.delete(articl)
        db.session.commit()
        return redirect('/post')
    except:
        return 'При удаление вышла ошибка'
    
    
@app.route('/post/<int:id>/update',methods=['POST','GET'])
def post_update(id):
    articl = Articl.query.get(id)
    if request.method=='POST':
        articl.title=request.form['title']
        articl.intro = request.form['intro']
        articl.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/post')
        except:
            return 'При добавление вышла ошибка'

    else:
        return render_template('post_update.html',articl=articl)


@app.route('/create-artical',methods=['POST','GET'])
def create_Articl():
    if request.method=='POST':
        title=request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        articl=Articl(title=title,intro=intro,text=text)

        print(title)

        try:
            db.session.add(articl)
            db.session.commit()
            return redirect('/post')
        except:
            return 'При добавление вышла ошибка'

    else:
        return render_template('create-artical.html')

if __name__=="__main__":
    app.run(debug=True)
