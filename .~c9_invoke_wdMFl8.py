from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# MODELS

class Influencer( db.Model ):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(100))
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    bio = db.Column(db.Text())
    region = db.Column(db.String(50))
    date_of_birth = db.Column(db.String(10))

    # relationships
    #cars = db.relationship( "Car", backref="user" ) #******
   # bids = db.relationship( "Bid", backref="user" ) #******
   # auctions = db.relationship( "Auction", backref="user" ) #******

    def __init__(self, username, password, fname, lname, bio, region, date_of_birth, brand):
        self.username = username
        self.password = password
        self.fname = fname
        self.lname = lname
        self.bio = bio
        self.region = region
        self.date_of_birth = date_of_birth

class Business( db.Model ):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    bio = db.Column(db.Text())
    industry = db.Column(db.String(100))
    region = db.Column(db.String(100))
    
    # relationships
   # parts = db.relationship( "Part", backref="car" ) #******
   # auction = db.relationship( "Auction", backref="car" ) #******
   # user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #******

    def __init__(self, username, password, name, bio, industry, region):
        self.username = username
        self.password = password
        self.name = name
        self.bio = bio
        self.industry = industry
        self.region = region
        
        
        
class Promotion( db.Model ):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(30))
    followers = db.Column(db.String(100))
    engagement_percent = db.Column(db.String(100))
    brand = db.Column(db.Text())



class SocialMedia( db.Model ):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(30))
    followers = db.Column(db.String(100))
    engagement_percent = db.Column(db.String(100))
    brand = db.Column(db.Text())

    # relationships
   # parts = db.relationship( "Part", backref="car" ) #******
   # auction = db.relationship( "Auction", backref="car" ) #******
   # user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #******

    def __init__(self, platform, followers, engagement, bio, industry, region):
        self.username = username
        self.password = password
        self.name = name
        self.bio = bio
        self.industry = industry
        self.region = region

# Controllers

@app.route("/")
def home():
    return render_template("index.html")


# CRUDI - Inlfuencer Controller
@app.route("/influencers")
def all_influencers():
    allInfluencers = Influencer.query.all()
    return render_template("users.html", allInfluencers = allInfluencers)

@app.route("/influencers/create", methods=["POST"])
def create_influencer():
    username = request.form.get('username', "")
    password = request.form.get('password', "")
    fname = request.form.get('fname', "")
    lname = request.form.get('lname', "")
    bio = request.form.get('bio', "")
    region = request.form.get('region', "")
    date_of_birth = request.form.get('date_of_birth', "")


    newInfluencer = Influencer(username, password, fname, lname, bio, region, date_of_birth)
    db.session.add(newInfluencer)
    db.session.commit()

    return redirect("/influencers")

@app.route("/influencers/<id>")
def get_influencer(id):
    influencer = Influencer.query.get( int(id) )
    return render_template("influencer.html", influencer = influencer)

@app.route("/influencers/<id>/edit", methods=["GET", "POST"])
def edit_influencer(id):
    influencer = Influencer.query.get( int(id) )

    if request == "Post":
        influencer.password = request.form.get('password', "")
        influencer.bio = request.form.get('bio', "")
        influencer.region= request.form.get('region', "")
        db.session.commit()
        return render_template("influencer.html", influencer = influencer)
    else:
        return render_template("edit_influencer.html", influencer = influencer)

@app.route("/influencers/<id>/delete", methods=["POST"])
def delete_influencer(id):
    influencer = Influencer.query.get( int(id) )
    db.session.delete(influencer)
    db.session.commit()
    return redirect("/influencers")



    # CRUDI Business

@app.route("/businesses")
def all_businesses():
    allBusinesses = Business.query.all()
    return render_template("business.html", Business = allBusinesses)
@app.route("/businesses/create", methods=["POST"])
def create_business():
    username = request.form.get('username', "")
    password = request.form.get('password', "")
    name = request.form.get('name', "")
    bio = request.form.get('bio', "")
    industry = request.form.get('industry', "")
    region = request.form.get('region', "")


    newBusiness = Business(username, password, name, bio, industry, region)
    db.session.add(newBusiness)
    db.session.commit()
    return redirect("/businesses/")


@app.route("/businesses/<id>")
def get_business(id):
    business = Business.query.get( int(id) )
    return render_template("business.html", Business = Business)

@app.route("/businesses/<id>/edit", methods=["GET", "POST"])
def edit_business(id):
    business = Business.query.get( int(id) )

    if request == "Post":
        business.password = request.form.get('password', "")
        business.name= request.form.get('name', "")
        business.bio = request.form.get('bio', "")
        business.industry = request.form.get('industry', "")
        business.region= request.form.get('region', "")

        db.session.commit()
        return render_template("business.html", Business = Business)
    else:
        return render_template("edit_business.html", Business = Business)

@app.route("/businesses/<id>/delete", methods=["POST"])
def delete_business(id):
    business = Business.query.get( int(id) )
    db.session.delete(business)
    db.session.commit()
    return redirect("/businesses")


if __name__ == "__main__":
    app.run()