from flask import Flask, request, jsonify
from flask_cors import CORS
from mock_data import mock_outlets

app = Flask(__name__)
CORS(app)

@app.route('/verify_email', methods=['POST'])
def verify_email():
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({"error": "Email is required"}), 400
        
    outlet = mock_outlets.get(email)
    if outlet:
        return jsonify({
            "status": "verified",
            "outlet": outlet
        })
    else:
        return jsonify({"error": "Outlet not found"}), 404

@app.route('/update_outlet_name', methods=['POST'])
def update_outlet_name():
    data = request.get_json()
    email = data.get('email')
    new_name = data.get('new_name')
    
    if not all([email, new_name]):
        return jsonify({"error": "Email and new_name are required"}), 400
        
    if email not in mock_outlets:
        return jsonify({"error": "Outlet not found"}), 404
        
    # Update the outlet name
    mock_outlets[email]["name"] = new_name
    
    return jsonify({
        "status": "success",
        "outlet": mock_outlets[email]
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)
