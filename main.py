from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Blog:beproductive@localhost:8889/Blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(2000))

    def __init__(self, name, body):
        self.name = name
        self.body = body

    def is_valid(self):
        
        if self.name and self.body:
            return True
        else:
            return False    

@app.route('/blog', methods=['POST', 'GET'])
def index():
    
    Blogs=Blog.query.all()
    return render_template('todos.html',title="Blog", Blogs=Blogs)



@app.route('/newpost', methods=['GET'])
def add_newpost():
      
    return render_template('newpost.html',title="Add a Blog Entry")

@app.route('/newpost', methods=['POST'])
def post_newpost():
    
    if request.method == 'POST':
        title_newblog = request.form['title_newblog']
        body_newblog = request.form['body_newblog']
        add_newblog = Blog(title_newblog,body_newblog )
        
        
        if add_newblog.is_valid():
            db.session.add(add_newblog)
            db.session.commit()
            Blogs=Blog.query.all()
            
            url = "/post?id=" + str(add_newblog.id)
            return redirect(url)
        else: 
            return render_template('newpost.html',title="Add a Blog Entry", error_body_newblog='please fill the body', error_title_newblog='please fill the title')    

@app.route('/post')
def post():
        
        blog_id = request.args.get('id')
        blog = Blog.query.get(blog_id)
        return render_template('post.html', blog=blog)
        
        


if __name__ == '__main__':
    app.run()