from flask import Flask, render_template , request,session
import sqlite3





def get_db():
    con = sqlite3.connect("fakeNewsUpdated.db")
    con.row_factory = sqlite3.Row
    return con



app = Flask(__name__)


app.secret_key = "Bastion"

@app.route('/')
def random():
    collectedDB= get_db()
    articles= collectedDB.cursor()
    sqlstrings="SELECT content FROM FakeNews ORDER BY random() LIMIT 1"
    articles.execute(sqlstrings)
    fetchedarticle= articles.fetchone()
    dictionaryarticle = dict(fetchedarticle)
    randomarticle = dictionaryarticle["content"]
    print(randomarticle)
    return render_template("Homepage.html",random=randomarticle)

@app.route('/guesser',methods=["GET","POST"])
def guessing():

    if "score" not in session:
        session["score"] = 0

    if "highscore" not in session:
        session["highscore"] = 0

    if "counter" not in session:
        session["counter"] = True

    if session["counter"] == True :
        session["counter"] = False
        if request.form.get("True") == "True":
            verdict = session.get("Verdict")
            randomarticle = session.get("RandomArticle")
            if verdict == "True":
                session["score"] += 1
                return render_template("GuessTheNews.html", verdict="Correct, it was true. To try again press next.",
                                       score=session["score"], random=randomarticle , highscore=session["highscore"])
            else:
                if session["score"] > session["highscore"]:
                    session["highscore"] = session["score"]
                session["score"] = 0
                return render_template("GuessTheNews.html",
                                       verdict="Incorrect, That answer was fake. To try again press next.",
                                       score=session["score"], random=randomarticle , highscore=session["highscore"])
        if request.form.get("Fake") == "Fake":
            verdict = session.get("Verdict")
            randomarticle = session.get("RandomArticle")
            if verdict == "Fake":
                session["score"] += 1
                return render_template("GuessTheNews.html", verdict="Correct, it was fake. To try again press next.",
                                       score=session["score"], random=randomarticle ,highscore=session["highscore"])
            else:
                if session["score"] > session["highscore"]:
                    session["highscore"] = session["score"]
                session["score"] = 0
                return render_template("GuessTheNews.html",
                                       verdict="Incorrect, That answer was true. To try again press next.",
                                       score=session["score"], random=randomarticle , highscore=session["highscore"])

    if request.form.get("Next") == "Next":
        session["counter"] = True
        collectedDB = get_db()
        articles = collectedDB.cursor()
        sqlstrings = "SELECT * FROM FakeNews ORDER BY random() LIMIT 1"
        articles.execute(sqlstrings)
        fetchedarticle = articles.fetchone()
        dictionaryarticle = dict(fetchedarticle)
        randomarticle = dictionaryarticle["content"]
        verdict = dictionaryarticle["realOrFake"]
        session["RandomArticle"] = randomarticle
        session["Verdict"] = verdict

        print(randomarticle)
        return render_template("GuessTheNews.html", random=randomarticle, verdict="", score=session["score"],
                               highscore=session["highscore"])

    else:
        verdict = session.get("Verdict")
        randomarticle = session.get("RandomArticle")
        return render_template("GuessTheNews.html",
                               verdict=verdict,
                               score=session["score"], random=randomarticle, highscore=session["highscore"])




app.run(debug=True)