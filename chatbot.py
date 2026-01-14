from flask import Flask, render_template, request, jsonify
import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nltk.download('wordnet')

app = Flask(__name__)

qa_pairs = {
    "what is python": "Python is a popular programming language used in AI, ML, web development, and automation.",
    "best it course": "Best IT courses include Python, Data Science, AI, Machine Learning, Cloud Computing, and Cyber Security.",
    "what is ai": "AI stands for Artificial Intelligence. It enables machines to think and learn.",
    "what is nlp": "NLP means Natural Language Processing, used for understanding human language.",
    "best career in it": "Top IT careers are Data Scientist, AI Engineer, Cloud Engineer, Cyber Security Expert.",
    "what is web development": "Web development uses HTML, CSS, JavaScript, and backend technologies."
}

lemmer = nltk.stem.WordNetLemmatizer()

def LemNormalize(text):
    return [lemmer.lemmatize(word.lower()) 
            for word in nltk.word_tokenize(text)
            if word not in string.punctuation]

def chatbot_response(user_input):
    user_input = user_input.lower()

    for q in qa_pairs:
        if q in user_input:
            return qa_pairs[q]

    questions = list(qa_pairs.keys())
    questions.append(user_input)

    vectorizer = TfidfVectorizer(tokenizer=LemNormalize, token_pattern=None)
    tfidf = vectorizer.fit_transform(questions)
    vals = cosine_similarity(tfidf[-1], tfidf)

    idx = vals.argsort()[0][-2]
    score = vals.flatten()[-2]

    if score == 0:
        return "I am still learning. Please ask IT-related questions."
    else:
        return qa_pairs[questions[idx]]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_bot_response():
    user_msg = request.json["msg"]
    return jsonify({"reply": chatbot_response(user_msg)})

if __name__ == "__main__":
    app.run(debug=True)
