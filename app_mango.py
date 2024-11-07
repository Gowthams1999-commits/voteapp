from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from urllib.parse import quote_plus

app = Flask(__name__)

# Replace with your MongoDB connection string
username = quote_plus("somu")
password = quote_plus("VGVzdEAyMDI0Cg==")
uri = f"mongodb://{username}:{password}@mongo-service:27017/"
mongo_client = MongoClient(uri)  # Initialize MongoClient
db = mongo_client['voting_db']  # Replace with your database name
votes_collection = db['votes']   # Replace with your collection name

# Initialize votes in MongoDB if not already set
if votes_collection.count_documents({}) == 0:
    votes_collection.insert_one({"Virat": 0, "Dhoni": 0})

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    option = data.get('option')
    if option in ["Virat", "Dhoni"]:
        votes_collection.update_one({}, {'$inc': {option: 1}})
        return jsonify({"message": "Vote counted", "votes": get_votes()}), 200
    return jsonify({"message": "Invalid option"}), 400

@app.route('/results', methods=['GET'])
def results():
    return jsonify(get_votes())

@app.route('/reset', methods=['POST'])
def reset():
    votes_collection.update_one({}, {'$set': {"Virat": 0, "Dhoni": 0}})
    return jsonify({"message": "Votes have been reset", "votes": get_votes()}), 200

def get_votes():
    votes = votes_collection.find_one()
    # Exclude '_id' field and convert values to int
    return {key: int(value) for key, value in votes.items() if key != '_id'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

