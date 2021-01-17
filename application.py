from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from flask_assets import Environment, Bundle
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app = Flask(__name__)
app.config["DEBUG"] = True
assets = Environment (app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = b"\x8e\xaa|\x9dK\xfc\x1e\x9c''\xbe \xd7\x85,\xdb"

login_manager = LoginManager()
login_manager.init_app(app)



css2 = Bundle('./css/landing_page_css/css/device-mockups.css', './css/landing_page_css/css/new-age.css',
              './css/landing_page_css/vendor/bootstrap/bootstrap-grid.css', './css/landing_page_css/vendor/fontawesome-free/css/all.css',
              './css/landing_page_css/vendor/simple-line-icons/css/simple-line-icons.css',
             output='gen/landing_page.css')

js2 = Bundle('./javascript/landing_page_js/javascript/landing_page.js', './javascript/landing_page_js/jquery/jquery.js',
              './javascript/landing_page_js/jquery-easing/jquery_easing_compatibility.js',
              './javascript/landing_page_js/js/bootstrap_bundle.js',
             output='gen/landing_page.js')


js = Bundle('./javascript/scripts.js',
            output='gen/script.js')


css = Bundle('./css/styles.css',
            output='gen/styles.css')

assets.register('js_all', js,)
assets.register('css_all', css)

assets.register('css_all2', css2)
assets.register('js_all2', js2)


# MODELS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

claimed_promotion = db.Table('claimed_promotion',
    db.Column('promotion_id', db.Integer, db.ForeignKey('promotion.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)


class InfluencerEmail( db.Model ):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))

    def __init__(self, email):
        self.email = email


class BusinessEmail( db.Model ):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))

    def __init__(self, email):
        self.email = email


class User( UserMixin, db.Model ):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(100))
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    business_name = db.Column(db.String(100))
    industry = db.Column(db.String(100))
    bio = db.Column(db.Text())
    state = db.Column(db.String(50))
    city = db.Column(db.String(50))
    date_of_birth = db.Column(db.String(10))
    role = db.Column(db.String(100))


    # relationships

    social_media = db.relationship( 'SocialMedia', backref='user' )
    promotion = db.relationship( 'Promotion', backref = 'promotion_user')
    claimed_promotion = db.relationship( 'Promotion', secondary=claimed_promotion, backref=db.backref('user', lazy='joined'))
    # initializers

    def __init__(self, email, username, password, fname, lname, business_name, industry, bio, state, city, date_of_birth, role):
        self.email = email
        self.username = username
        self.password = password
        self.fname = fname
        self.lname = lname
        self.business_name = business_name
        self.industry = industry
        self.bio = bio
        self.state = state
        self.city = city
        self.date_of_birth = date_of_birth
        self.role = role


        def is_influencer(self):
            return self.role == "influencer"

        def is_business(self):
            return self.role == "business"

        def is_admin(self):
            return self.role == "admin"


class Promotion( db.Model ):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    image = db.Column(db.String(100))
    description = db.Column(db.Text())
    region = db.Column(db.String(30))
    date_range = db.Column(db.String(25))
    brand = db.Column(db.Text())
    platform = db.Column(db.String(100))
    quantity = db.Column(db.String(100))

    # relationships

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # initializers

    def __init__(self, name, image, description, region, date_range, brand, platform, quantity, promotion_user):
        self.name = name
        self.image = image
        self.description = description
        self.region = region
        self.date_range = date_range
        self.brand = brand
        self.platform = platform
        self.quantity = quantity
        self.promotion_user = promotion_user


class SocialMedia( db.Model ):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(30))
    followers = db.Column(db.String(100))
    engagement_percent = db.Column(db.String(100))
    brand = db.Column(db.Text())
    username = db.Column(db.String(30))

    # relationships

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # initializers

    def __init__(self, platform, followers, engagement_percent, brand, username, user):
        self.platform = platform
        self.followers = followers
        self.engagement_percent = engagement_percent
        self.brand = brand
        self.username = username
        self.user = user






# Controllers

    # Home Route

@app.route("/1")
def home():
    return render_template("indextest.html")

    # Landing Page Routes

@app.route("/", methods=["GET", "POST"])
def influencer_landing():
    if request.method == "POST":

        email = request.form['email']

        newInfluencerEmail = InfluencerEmail(email)

        db.session.add(newInfluencerEmail)
        db.session.commit()

        flash("Thank You For Joining Us, We Will Be Contacting You Very Soon!")
        return redirect("/")

    else:
        return render_template("landing_pages/influencer.html")



@app.route("/landing_page/business", methods=["GET", "POST"])
def business_landing():
    if request.method == "POST":

        email = request.form['email']

        newBusinessEmail = BusinessEmail(email)

        db.session.add(newBusinessEmail)
        db.session.commit()

        flash("Thank You For Joining Us, We Will Be Contacting You Very Soon!")
        return redirect("/landing_page/business")

    return render_template("landing_pages/business.html")



    # Register/Login/Logout Routes

@app.route("/register")
def register():
    return render_template("register.html")


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/user_login', methods=["GET", "POST"])
def user_login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        user = User.query.filter_by(username = username, password = password, role = role).first()

        if role == 'influencer':
            if not user:
                flash("Incorect username or password, please verify and try again.")
                return redirect('/user_login')

            else:
                login_user(user)
                return redirect('/dashboard')

        else:
            if not user:
                flash("Incorect username or password, please verify and try again.")
                return redirect('/user_login')

            else:
                login_user(user)
                return redirect('/dashboard')


    else:
        return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()


    flash("You have successfully logged out!")
    return redirect('/user_login')

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

    #CRUDI User Controllers

        # Index
@app.route("/users")
def all_users():
    allUsers = User.query.all()
    return render_template("dashboard.html", allUsers = allUsers)

        # Create

@app.route("/users/create", methods=["POST"])
def create_user():
    email = request.form.get('email', "")
    username = request.form.get('username', "")
    password = request.form.get('password', "")
    fname = request.form.get('fname', "")
    lname = request.form.get('lname', "")
    business_name = request.form.get('business_name', "")
    industry = request.form.get('industry', "")
    bio = request.form.get('bio', "")
    state = request.form.get('state', "")
    city = request.form.get('city', "")
    date_of_birth = request.form.get('date_of_birth', "")
    role = request.form.get('role', "")

    users = User.query.filter_by(username = username).all()

    is_unique = True

    for user in users:
        if username != user.username:
            is_unique = True
        else:
            is_unique = False
            break

    if is_unique == True:

        newUser = User(email, username, password, fname, lname, business_name, industry, bio, state, city, date_of_birth, role)
        db.session.add(newUser)
        db.session.commit()

        return redirect("/user_login")

    else:
        flash("This username is already in use, please choose a different username.")
        return redirect("/register")

        # Read
@app.route("/users/<id>")
def get_user(id):
    user = User.query.get( int(id) )
    return render_template("dashboard.html", user = user)

        # Update
@app.route("/users/<id>/edit", methods=["GET", "POST"])
def edit_user(id):


    if request.method == "POST":
        user = User.query.get( int(id) )
        user.password = request.form.get('password', "")
        user.bio = request.form.get('bio', "")
        user.state = request.form.get('state', "")
        user.city = request.form.get('city', "")
        db.session.commit()

        return render_template("dashboard.html", user = user)
    else:
        return render_template("edit_user.html", user = user)

        # Delete
@app.route("/users/<id>/delete", methods=["POST"])
def delete_user(id):
    user = User.query.get( int(id) )
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")


    # CRUDI Promotion


@app.route("/promotions")
def all_promotions():
    promotions = current_user.promotion
    allPromotions = Promotion.query.all()
    return render_template("promotion.html", allPromotions = allPromotions, promotions = promotions)

@app.route("/promotions/create", methods=["POST"])
def create_promotion():
    name = request.form.get('name', "")
    image = request.form.get('image', "")
    description = request.form.get('description', "")
    region = request.form.get('region', "")
    date_range = request.form.get('date_range', "")
    brand = request.form.get('brand', "")
    platform = request.form.get('platform', "")
    quantity = request.form.get('quantity', "")


    newPromotion = Promotion(name, image, description, region, date_range, brand, platform, quantity, current_user)
    db.session.add(newPromotion)
    db.session.commit()

    return redirect("/promotions")

@app.route("/promotions/<id>")
def get_promotion(id):
    promotion = Promotion.query.get( int(id) )
    return render_template("promotion.html", promotion = promotion)

@app.route("/promotions/<id>/edit", methods=["GET", "POST"])
def edit_promotion(id):

    if request.method == "POST":
        promotion = Promotion.query.get( int(id) )

        promotion.name = request.form.get('name', "")
        promotion.image = request.form.get('image', "")
        promotion.description= request.form.get('description', "")
        promotion.region = request.form.get('region', "")
        promotion.date_range = request.form.get('date_range', "")
        promotion.brand= request.form.get('brand', "")
        promotion.platform = request.form.get('platform', "")
        promotion.quantity= request.form.get('quantity', "")

        db.session.commit()

        return redirect("/promotions")
    else:
        return redirect("/promotions")

@app.route("/promotions/<id>/delete", methods=["GET"])
def delete_promotion(id):
    promotion = Promotion.query.get( int(id) )
    db.session.delete(promotion)
    db.session.commit()

    return redirect("/promotions")


    # CRUDI Social Media

@app.route("/socialmedia")
def all_socialmedias():
    allSocialmedias = SocialMedia.query.all()
    socialmedias = current_user.social_media


    return render_template("socialmedia.html", socialmedias = socialmedias, allSocialmedias = allSocialmedias)

@app.route("/socialmedia/create", methods=["POST"])
def create_Socialmedia():
    platform = request.form.get('platform', "")
    followers = request.form.get('followers', "")
    engagement_percent = request.form.get('engagement_percent', "")
    brand = request.form.get('brand', "")
    username= request.form.get('username', "")

    #allSocialmedias = SocialMedia.query.all()
    socialmedias = SocialMedia.query.filter_by(platform = platform).filter_by(username = username).all()

    is_unique = True

    for socialmedia in socialmedias:
        if platform != socialmedia.platform and username != socialmedia.username:
            is_unique = True
        else:
            is_unique = False
            break

    if is_unique == True:
        newSocialmedia = SocialMedia(platform, followers, engagement_percent, brand, username, current_user)

        print("----------------")
        print(username)
        print("----------------")
        print(platform)
        print("----------------")


        db.session.add(newSocialmedia)
        db.session.commit()
        return redirect("/socialmedia")

    else:
        flash("This account is registered to another user, please connect a new account.")
        return redirect("/socialmedia")


@app.route("/socialmedia/<id>")
def get_socialmedia(id):
    socialmedia = SocialMedia.query.get( int(id) )
    return render_template("socialmedia.html", socialmedia = socialmedia)

@app.route("/socialmedia/<id>/edit", methods=["GET", "POST"])
def edit_socialmedia(id):
    socialmedia = SocialMedia.query.get( int(id) )

    if request == "POST":
        socialmedia.platform = request.form.get('platform', "")
        socialmedia.followers = request.form.get('followers', "")
        socialmedia.engagement_percent = request.form.get('engagement_percent', "")
        socialmedia.brand = request.form.get('brand', "")

        db.session.commit()
        return render_template("socialmedia.html", socialmedia = socialmedia)
    else:
        return render_template("edit_socialmedia.html", socialmedia = socialmedia)

@app.route("/socialmedia/<id>/delete", methods=["POST"])
def delete_socialmedia(id):
    socialmedia = SocialMedia.query.get( int(id) )
    db.session.delete(socialmedia)
    db.session.commit()
    return redirect("/socialmedia")


    # CRUDI Claimed Promotion

@app.route("/claimedpromotion")
def all_claimedpromotion():
    #allclaimedpromotions = User.query.join(claimed_promotion).join(Promotion).filter
    #((claimed_promotion.c.user_id == User.id) & (claimed_promotion.c.promotion_id == Promotion.id))
    #claimedpromotions = claimed_promotion.query.filter_by(user = current_user)
    claimedpromotions = claimed_promotion.query.filter_by(user_id = current_user).all()
    return render_template("dashboard.html", claimedpromotions = claimedpromotions)

@app.route("/claimedpromotion/<id>/create", methods=["POST"])
def create_claimedpromotion(id):

    claimedpromotion = Promotion.query.get( int(id) )

    print("-------------------------------")
    print("-------------------------------")

    print(claimedpromotion.id)

    print("-------------------------------")

    #newclaimedpromotion = ClaimedPromotion(promotion)

    claimedpromotion.user.append(current_user)
    db.session.commit()
    return redirect("/claimedpromotion")


@app.route("/claimedpromotion/<id>")
def get_claimedpromotion(id):
    claimedpromotion = claimed_promotion.query.get( int(id) )
    return render_template("claimedpromotion.html", claimedpromotion = claimedpromotion)

@app.route("/claimedpromotion/<id>/edit", methods=["GET", "POST"])
def edit_claimedpromotion(id):
    claimedpromotion = claimed_promotion.query.get( int(id) )

    if request == "POST":


        db.session.commit()
        return render_template("claimedpromotion.html", claimedpromotion = claimedpromotion)
    else:
        return render_template("edit_socialmedia.html", claimedpromotion = claimedpromotion)

@app.route("/claimedpromotion/<id>/delete", methods=["POST"])
def delete_claimedpromotion(id):
    claimedpromotion = claimed_promotion.query.get( int(id) )
    db.session.delete(claimedpromotion)
    db.session.commit()
    return redirect("/claimedpromotion")



if __name__ == "__main__":
    app.run()