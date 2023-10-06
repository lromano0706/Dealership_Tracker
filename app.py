from flask import (
    Flask,
    render_template_string,
    redirect,
    url_for,
    render_template,
    request,
)
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# from below to have ObjectId work
from bson import ObjectId


# import password from config.py
from config import password


app = Flask(__name__)


uri = f"mongodb+srv://admin-luis:{password}@cluster1.prd6v.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi("1"))
db = client["subaru"]
collection = db["salespeople"]


@app.route("/")
def index():
    documents = list(collection.find({}))
    return render_template("index.html", documents=documents)


@app.route("/create", methods=["POST"])
def create():
    docs = [
        {"first_name": "Ben", "last_name": "Haithmore", "years_at_dealer": 2},
        {"first_name": "Evred", "last_name": "Ramierez", "years_at_dealer": 0},
        {"first_name": "Fio", "last_name": "Cuba", "years_at_dealer": 0},
        {"first_name": "Ashur", "last_name": "Tracy", "years_at_dealer": 5},
    ]
    collection.insert_many(docs)
    message = "Created 4 documents in collection"
    return redirect(url_for("index"))


@app.route("/read", methods=["POST"])
def read():
    output = ""
    results = collection.find()
    for result in results:
        output += str(result) + "<br>"
    return output


@app.route("/update", methods=["POST"])
def update():
    post_id = request.form.get("post_Id")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    years_at_dealer = request.form.get("years_at_dealer")
    update_fields = {}
    if first_name != "":
        update_fields["first_name"] = first_name
    if last_name != "":
        update_fields["last_name"] = last_name
    if years_at_dealer != "":
        update_fields["years_at_dealer"] = years_at_dealer
    if update_fields:
        collection.update_one(
            {"_id": ObjectId(post_id)},
            {"$set": update_fields},
        )

    return redirect(url_for("index"))


@app.route("/delete", methods=["POST"])
def delete():
    delete_selection = request.form.get("delete_selection")
    collection.delete_one({"_id": ObjectId(delete_selection)})
    return redirect(url_for("index"))


@app.route("/delete_all", methods=["POST"])
def delete_all():
    collection.delete_many({})
    message = f"Deleted all documents"
    return redirect(url_for("index"))
    # return render_template("index.html", message=message)


@app.route("/submit", methods=["POST"])
def submit():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    years_at_dealer = request.form.get("years_at_dealer")

    # Insert into MongoDB
    collection.insert_one(
        {
            "first_name": first_name,
            "last_name": last_name,
            "years_at_dealer": years_at_dealer,
        }
    )

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
