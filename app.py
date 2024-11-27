#A payer is the producer of the item that points were added through - helps bill the payer when rewards are spent
#whats the ask? - REST API that will help keep track of points and point transactions.
# 1) serve it on port 8000
# implement - add, spend, fetch

#import statements
from flask import Flask, request, jsonify
from datetime import datetime
from collections import deque


#setup flask for api connection
app = Flask(__name__)

# helper data structures
transactions= deque() #record of transactions
balances={} #dict to track points per payer

#home screen - just for fun!
@app.route('/')
def home():
    return "Welcome to the Points Management API! Use /add, /spend, or /balance endpoints.", 200


#add
#post api
#success code - 200 OK
@app.route('/add', methods=['POST'])
def add():
    request_data = request.get_json()

    #lets begin by validating our input params
    #sample
    #{  "payer" : "DANNON", "points" : 5000, "timestamp" : "2020-11-02T14:00:00Z" }
    if not request_data or 'payer' not in request_data or 'points' not in request_data or 'timestamp' not in request_data:
        #return error
        #lets assume errors are 400 BAD
        return jsonify({"error": "Input is not valid. 'payer', 'points', and 'timestamp' are required."}), 400
    
    #we have a valid input, extract.
    payer = request_data['payer']
    points = request_data['points']
    timestamp = request_data['timestamp']

    #now lets  validate input values
    try:
        # Validate timestamp format
        timestamp = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        return jsonify({"error": "Invalid timestamp format."}), 400
    
    #lets store the transaction
    transactions.append({"payer": payer, "points": points, "timestamp": timestamp})

    #update the balance
    balances[payer] = balances.get(payer, 0) + points

    #success
    return '', 200  

#spend
#post api
#success code - 200 OK
@app.route('/spend', methods=['POST'])
def spend():
    request_data = request.get_json()

    points_to_spend = request_data.get('points')
    #lets validate our input param and value
    if points_to_spend is None or points_to_spend < 0:
        return 'Invalid points value', 400

    #check if we have enough points
    available_points_points = sum(balances.values())
    if points_to_spend > available_points_points:
        return 'Not enough points', 400

    #lets sort so that we can deduct form oldest transactions based on timestamp
    sorted_transactions = sorted(transactions, key=lambda x: x['timestamp'])

    spend_summary = []
    points_needed = points_to_spend

    for transaction in sorted_transactions:
        if points_needed <= 0:
            break

        payer = transaction['payer']
        points = transaction['points']

        available_points = balances.get(payer, 0)

        if available_points <= 0:
            continue

        points_to_deduct = min(points, points_needed, available_points)

        #deduct the points
        balances[payer] -= points_to_deduct
        transaction['points'] -= points_to_deduct
        points_needed -= points_to_deduct

        #record so that we can return payers from whom we deducted
        existing_entry = next((entry for entry in spend_summary if entry['payer'] == payer), None)
        if existing_entry:
            existing_entry['points'] -= points_to_deduct
        else:
            spend_summary.append({'payer': payer, 'points': -points_to_deduct})

    #final check, it means we couldn't fulfill the spend request
    if points_needed > 0:
        return 'Not enough points after processing transactions', 400

    return jsonify(spend_summary), 200


#get points
#get API
#200 success
@app.route('/balance', methods=['GET'])
def get_balance():
    #as simple as that since we have balances dictionary which is updated whenever points are added or spent.
    return jsonify(balances), 200



#need to run on port 8000
if __name__ == '__main__':
    app.run(port=8000)