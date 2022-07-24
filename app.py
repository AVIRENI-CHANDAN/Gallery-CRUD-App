from flask import Flask, request, render_template, send_from_directory, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__, template_folder="views")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Models
# -------------------------------
class Image(db.Model):
    __tablename__ = "Images"
    id = db.Column(db.Integer, primary_key=True)
    ImgName = db.Column(db.String(500), nullable=False)
    ImgURL = db.Column(db.String(500), unique=True, nullable=False)
    ImgDetails = db.Column(db.String(2000))

    def __repr__(self):
        return "<Image %r>" % self.ImgName

    def __str__(self):
        return "{\n\tName: %s,\n\turl: %s,\n\tdetails: %s\n}" % (
            self.ImgName,
            self.ImgURL,
            self.ImgDetails,
        )

    def save(self):
        obj = Image(
            ImgName=self.ImgName, ImgURL=self.ImgURL, ImgDetails=self.ImgDetails
        )
        try:
            db.session.add(obj)
            return db.session.commit()
        except IntegrityError:
            return db.session.flush()

    def update(self, *args, **kwargs):
        self.ImgName = args[0]["ImgName"]
        self.ImgURL = args[0]["ImgURL"]
        self.ImgDetails = args[0]["ImgDetails"]
        return db.session.commit()


# -------------------------------

# Contollers
# -------------------------------
@app.route("/logo")
def favicon():
    return send_from_directory("assets", "favicon.ico")


@app.route("/", methods=["GET", "POST"])
def hello_world():
    print("APPLICATION PATH:",app.root_path)
    if request.method == "GET":
        page = request.args.get("page", 1, type=int)
        print("REQUESTED PAGE NUMBER:", page)
        try:
            objs = Image.query.paginate(page=page, per_page=9)
        except Exception:
            return redirect("/")
        return render_template("read.html", objects=objs)
    if request.method == "POST":
        parameters = request.form
        try:
            obj = Image(
                ImgName=parameters["imgname"],
                ImgURL=parameters["imgurl"],
                ImgDetails=parameters["imgdetails"],
            )
            obj.save()
        except IntegrityError:
            return redirect("/")
        return redirect("/")


@app.route("/show/<int:id>", methods=["GET"])
def showdetails(id):
    obj = Image.query.filter_by(id=id).first()
    return render_template("details.html", obj=obj)


@app.route("/new", methods=["GET"])
def addimage():
    return render_template("newimage.html")


@app.route("/<int:id>/edit", methods=["GET", "POST"])
def editdetails(id):
    if request.method == "GET":
        print("EDITING GET REQUEST")
        obj = Image.query.filter_by(id=id).first()
        return render_template("editimage.html", obj=obj)
    if request.method == "POST":
        parameters = request.form
        Image.query.filter_by(id=id).first().update(
            dict(
                ImgName=parameters["imgname"],
                ImgURL=parameters["imgurl"],
                ImgDetails=parameters["imgdetails"],
            )
        )
        # num_rows_updated = User.query.filter_by(username='admin').update(dict(email='my_new_email@example.com')))
        db.session.commit()
        return redirect("/")


@app.route("/delete/<int:id>", methods=["GET", "POST"])
def deleteimage(id):
    Image.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect("/")


# --------------------------------

# Driver code
if __name__ == "__main__":
    db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
