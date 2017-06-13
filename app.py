from flask import Flask, render_template, redirect
from sqlalchemy import create_engine, MetaData
from flask_login import UserMixin, LoginManager, login_user, logout_user
from flask_blogging import SQLAStorage, BloggingEngine, Storage
from flask_sqlalchemy import SQLAlchemy
import os
import requests
import random

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"  # for WTF-forms and login
app.config["BLOGGING_URL_PREFIX"] = "/blog"
app.config["BLOGGING_DISQUS_SITENAME"] = "test"
app.config["BLOGGING_SITEURL"] = "http://localhost:8000"
app.config["BLOGGING_SITENAME"] = "Krishna Kumar"
app.config["FILEUPLOAD_IMG_FOLDER"] = "fileupload"
app.config["FILEUPLOAD_PREFIX"] = "/fileupload"
app.config["FILEUPLOAD_ALLOWED_EXTENSIONS"] = ["png", "jpg", "jpeg", "gif"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['DATABASE_URL']

#export DATABASE_URL="postgresql://localhost/blog"


db = SQLAlchemy(app)
storage = SQLAStorage(db=db)
#db.create_all()

blog_engine = BloggingEngine(app, storage)
login_manager = LoginManager(app)


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

    def get_name(self):
        return "Krishna Kumar"  # typically the user's name

def get_quotes():

    try:
        r = requests.get('http://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=1')
        content_json = r.json()
        content_quote = content_json[0]['content']
        content_author = content_json[0]['title']
        cutovers = ['&#8217;', '<br /> ', '<p>', '</p>']
        for c in cutovers:
            if c in content_quote:
                content_quote = content_quote.replace(c, "'")

        
        clean_content_quote = content_quote[1:-5]
        

    except:
        clean_content_quote = 'This is a random quote beep. This is affirmatively not generated from bot beep.'
        content_author = 'beep bot'

    return clean_content_quote, content_author


def faster_quotes():
    content_dict = {'James Thurber':'All men should strive to learn before they die, what they are running from, and to, and why.',
                    'Abigail Adams':'Learning is not attained by chance, it must be sought for with ardor and attended to with diligence.',
                    'Pablo Picasso':'I am always doing that which I cannot do, in order that I may learn how to do it.',
                    'Don Williams Jr.':'The road of life twists and turns and no two directions are ever the same. Yet our lessons come from the journey, not the destination.',
                    'Benjamin Franklin':'Tell me and I forget. Teach me and I remember. Involve me and I learn.',
                    'Confucius':'Learning without thought is labor lost; thought without learning is perilous.',
                    'John F. Kennedy':'Leadership and learning are indispensable to each other.',
                    'Vivian Greene':"Life isn't about waiting for the storm to pass. It's about learning how to dance in the rain.",
                    }
    choice = random.choice(list(content_dict))
    content_quote = content_dict[choice]
    content_author = choice
    return content_quote, content_author


def get_post_count():
    """ Helper function to get the post count. 
    """
    post_count = Storage.count_posts()
    return post_count

@login_manager.user_loader
@blog_engine.user_loader
def load_user(user_id):
    return User(user_id)


@app.route("/")
def index():
    quote, author = faster_quotes()
    
    return render_template("index.html", quote=quote, author=author)

@app.route("/authentication-is-hard/")
def login():
    user = User("bloguser")
    login_user(user)
    return redirect("/blog/")

@app.route("/logout/")
def logout():
    logout_user()
    return redirect("/")

@app.route("/resume/")
def view_resume():
    return render_template("resume.html")


if __name__ == "__main__":
    app.run(debug=True)