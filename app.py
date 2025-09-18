from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
app.secret_key = 'your_secure_secret_key'  # Replace with your own secure key

# Predefined questions (15 options)
questions = {
    "1": "Hostel General Information",
    "2": "Events & Notices",
    "3": "Maintenance & Service Requests",
    "4": "Hostel Regulations & Guidelines",
    "5": "Emergency Contacts & Procedures",
    "6": "Mess and Cafeteria Information",
    "7": "Room Allotment & Accommodation",
    "8": "Visitor Policies",
    "9": "Student Welfare Support",
    "10": "Health and Safety",
    "11": "Roommate Guidelines",
    "12": "Security & Surveillance",
    "13": "Hostel Payments & Fees",
    "14": "Hostel Feedback & Complaints",
    "15": "Other Inquiries"
}

# Predefined responses for each question
responses = {
    "1": (
        "<strong>Nek Chand Tower - General Information</strong><br><br>"
        "Nek Chand Tower is the boys’ hostel of Chandigarh University, located at the rear of the campus in Rupnagar, Mohali, Punjab. "
        "It consists of six towers (<strong>NCT-1</strong> to <strong>NCT-6</strong>), with <strong>NCT-6</strong> reserved for international students. "
        "The hostel director, <strong>Mr. Aswani</strong>, operates from <strong>NCT-4</strong>, and every room is a 4-seater. "
        "Facilities include a mess on the ground floor, a gym, laundry services, canteens, and more, ensuring a comfortable student lifestyle.<br>"
        "<strong>Hostel contacts:</strong> <a href='tel:+917527030522'>7527030522</a>, <a href='tel:+918288094318'>8288094318</a><br>"
        "<strong>Medical Dispensary:</strong> <a href='tel:+917087989898'>7087989898</a><br>"
        "<strong>Department of Student Welfare:</strong> <a href='tel:+181002000025'>1800 200 0025</a><br>"
        "<a href='https://www.cuchd.in/student-services/hostel-facility.php' target='_blank'>More Info</a><br>"
        "Best regards, and we hope your stay here is filled with learning, growth, friendships, and unforgettable memories. Welcome to your second home!"
    ),
    "2": (
        "<strong>Events & Notices</strong><br><br>"
        "Today's events include a group study session at <strong>4 PM</strong> in the common room and a movie night at <strong>8 PM</strong>. "
        "Please check the notice board for any updates.<br>"
        "<a href='https://www.cuchd.in/campus-life/cultural.php' target='_blank'>More Events</a>"
    ),
    "3": (
        "<strong>Maintenance & Service Requests</strong><br><br>"
        "If you have any maintenance issues or require services, please submit your request via our online portal or visit the hostel reception for assistance.<br>"
        "<a href='https://www.cuchd.in/assets/upload/procedures-and-policies-for-maintenance.pdf' target='_blank'>Maintenance Requests</a>"
    ),
    "4": (
        "<strong>Hostel Regulations & Guidelines</strong><br><br>"
        "All residents must adhere to the hostel rules: maintain silence after <strong>10 PM</strong>, follow food regulations, and respect common areas. "
        "Please refer to the hostel handbook for complete details.<br>"
        "<a href='https://www.cuchd.in/student-services/hostel-facility.php' target='_blank'>Hostel Rules</a>"
    ),
    "5": (
        "<strong>Emergency Contacts & Procedures</strong><br><br>"
        "In case of emergencies, dial <a href='tel:+18002000025'><strong>1800 200 0025</strong></a> immediately or contact on-duty security at <a href='tel:+917527030522'><strong>7527030522</strong></a>, <a href='tel:+918288094318'><strong>8288094318</strong></a>.<br>"
        "<a href='https://www.cuchd.in/contact/' target='_blank'>Emergency Info</a>"
    ),
    "6": (
        "<strong>Mess and Cafeteria Information</strong><br><br>"
        "The hostel mess serves nutritious meals: breakfast at <strong>7:30 AM</strong>, lunch at <strong>12 PM</strong>, and dinner at <strong>7:30 PM</strong>.<br>"
        "Daily special menus are posted in each tower.<br>"
        "<a href='https://www.cuchd.in/student-services/hostel-facility.php' target='_blank'>Mess Info</a>"
    ),
    "7": (
        "<strong>Room Allotment & Accommodation</strong><br><br>"
        "Room allotment is conducted on a first-come, first-served basis. "
        "If you have any issues regarding your room assignment, please contact the hostel administration.<br>"
        "<a href='https://www.cuchd.in/student-services/hostel-facility.php' target='_blank'>Room Allotment Info</a>"
    ),
    "8": (
        "<strong>Visitor Policies</strong><br><br>"
        "Visitors are allowed from <strong>9 AM to 4 PM</strong>. All guests must sign in at the reception. "
        "Overnight visits require prior approval from hostel management.<br>"
        "<a href='https://www.cuchd.in/student-services/hostel-facility.php' target='_blank'>Visitor Policies</a>"
    ),
    "9": (
        "<strong>Student Welfare Support</strong><br><br>"
        "Reach out to the Department of Student Welfare for counseling, mentoring, and academic help at <a href='tel:+18002000025'><strong>1800 200 0025</strong></a>.<br>"
        "<a href='https://www.cuchd.in/student-services/studen-welfare-services.php' target='_blank'>Student Welfare</a>"
    ),
    "10": (
        "<strong>Health and Safety</strong><br><br>"
        "For any health-related concerns, the medical team is available at the hostel medical dispensary. Please contact <a href='tel:+18002000025'><strong>1800 200 0025</strong></a> for urgent assistance.<br>"
        "<a href='https://www.cuchd.in/student-services/' target='_blank'>Health Info</a>"
    ),
    "11": (
        "<strong>Roommate Guidelines</strong><br><br>"
        "Maintain respect and understanding with your roommates. It’s important to keep your room tidy and communicate clearly about shared responsibilities.<br>"
        "<a href='https://www.cuchd.in/student-services/hostel-facility.php' target='_blank'>Roommate Guidelines</a>"
    ),
    "12": (
        "<strong>Security & Surveillance</strong><br><br>"
        "The hostel is equipped with 24/7 security personnel and CCTV surveillance to ensure the safety and well-being of all residents.<br>"
        "<a href='https://www.cuchd.in/student-services/' target='_blank'>Security Info</a>"
    ),
    "13": (
        "<strong>Hostel Payments & Fees</strong><br><br>"
        "Hostel fees can be paid online through the official Chandigarh University portal. For assistance, contact the hostel administration.<br>"
        "<a href='https://www.cuchd.in/student-services/hostel-facility.php' target='_blank'>Hostel Fees</a>"
    ),
    "14": (
        "<strong>Hostel Feedback & Complaints</strong><br><br>"
        "For any feedback or complaints, please visit the hostel administration office or submit a request via the online portal.<br>"
        "<a href='https://www.cuchd.in/contact/feedback.aspx' target='_blank'>Feedback</a>"
    ),
    "15": (
        "<strong>Other Inquiries</strong><br><br>"
        "If you have other inquiries, feel free to ask, and we will assist you accordingly.<br>"
        "<a href='https://www.cuchd.in/faq/' target='_blank'>Contact Us</a>"
    )
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'reply': 'No message provided.'})
    
    user_message = data['message'].strip()
    
    # Check if the input matches one of the expected options (1-15)
    if user_message in responses:
        bot_message = responses[user_message]
    else:
        # Default message if input is invalid or initial state
        bot_message = "<strong>Welcome to Hostel Assistant Chat!</strong><br><br>"
        bot_message += "Please choose an option by entering a number (1–15):<br>"
        for key, value in questions.items():
            bot_message += f"{key}. {value}<br>"
    
    # Append the menu after each response (this allows the user to pick another option)
    bot_message += "<br><br><strong>Please choose an option by entering a number (1–15):</strong><br>"
    for key, value in questions.items():
        bot_message += f"{key}. {value}<br>"
    
    return jsonify({"reply": bot_message})

if __name__ == "__main__":
    app.run(debug=True)