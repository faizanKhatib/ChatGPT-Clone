
from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
import openai



openai.api_key = "API_key"

app = Flask(__name__)
app.config["MONGO_URI"] = "Connection String"
mongo = PyMongo(app)

@app.route("/")
def home():
    chats = mongo.db.chats.find({})
    myChats = [chat for chat in chats]
    return render_template("index.html", myChats = myChats)

@app.route("/api", methods=["GET","POST"])
def qa():
    if request.method == "POST":
        question = request.json.get("question")
        chat = mongo.db.chats.find_one({"question" : question})
        if chat:
            data = {"answer" : f"{chat['answer']}"}
            return jsonify(data)
        else:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=question,
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
                )
            data = {"question": question, "answer": response["choices"][0]["text"]}
            mongo.db.chats.insert_one({"question": question, "answer": response["choices"][0]["text"]})
            return jsonify(data)

    data = {"result": "Thank You! I'm just a AI"}
    return jsonify(data)

app.run(debug=True)
         

        
        