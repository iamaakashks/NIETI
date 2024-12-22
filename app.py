import os
from flask import Flask, render_template, request, jsonify
import nltk
from nltk.chat.util import Chat, reflections

# Download the necessary NLTK package
nltk.download('punkt')

app = Flask(__name__)

# Define more general chatbot patterns to handle varied user inputs
patterns = [
    (r'hi|hello|hey',
     ['Hello! How can I help you with your inquiry about NIE College?']),
    (r'(.*)your name(.*)|(.*)name(.*)', [
        'My name is NIETI, a College Inquiry Chatbot at NIE, mysuru. How can I assist you today?'
    ]),
    # Handle general mentions of "admission process" more flexibly
    (r'(.*)admission process(.*)', [
        'Candidates need to register for entrance exams like KCET or COMEDK-UCET for BE admission.\nFor Management Quota, registration will be done on the official website of the institute.\nNIE Mysore takes admissions to MCA and MTech programmes is through the Karnataka PGCET conducted by the Karnataka Examination Authority (KEA). For detailed information, visit our official admissions page: (https://nie.ac.in/admission/)'
    ]),
    # Handle general mentions of "fee structure" more flexibly
    (r'(.*)fee structure(.*)|(.*)fees(.*)|(.*)total cost(.*)', [
        'BE: Total fees for the programme is 10.66 Lakhs.\n Mtech: Total fees for the programme is 10.66 Lakhs.\nMCA: Total fees for the programme is 1.28 Lakhs.\nFor More Details, Visit: (https://nie.ac.in/admission/)'
    ]),
    (r'(.*)about nie(.*)|', [
        'The National Institute of Engineering (NIE), established in the year 1946, is a premier engineering college in Mysuru, Karnataka, India.',
        'NIE is a premier engineering college in Mysuru, Karnataka, India.'
    ]),
    (r'(.*)campus(.*)|(.*)campuses(.*)', [
        'NIE offers 3 UG Courses and 1 PG Course at North Campus and NIE offers 4 UG Courses and 9 PG Courses at South Campus'
    ]),
    # Handle general mentions of "courses offered" more flexibly
    (r'(.*)courses offered(.*)', [
        'NIE has two campuses. NIE North and NIE South.\nNIE College offers a variety of undergraduate and postgraduate courses. Check out our courses page for more details: [Courses Offered](https://nie.ac.in/courses-offered/)'
    ]),
    # Handle general mentions of "contact" or "contact us" more flexibly
    (r'(.*)contact(.*)', [
        'You can contact NIE College through the contact information provided on the website. Here’s the link: [Contact Information](https://nie.ac.in/contact-us/)'
    ]),
    # Handle general mentions of "location" more flexibly
    (r'(.*)location(.*)', [
        'NIE College is located in Mysuru, Karnataka. Visit the campus at the North Campus for a tour. For location details, check: [Location](https://nie.ac.in/contact-us/)'
    ]),
    # Handle gratitude in a general way
    (r'(.*) (thanks|thank you)(.*)',
     ['You’re welcome! Let me know if you have more questions.']),
    # Catch-all for unrecognized queries
    (r'(.*)',
     ['Sorry, I didn’t quite understand that. Can you please ask again?'])
]

# Initialize the chatbot with patterns and reflections
chatbot = Chat(patterns, reflections)


# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')


# Route for chatbot response
@app.route('/get', methods=['GET'])
def get_bot_response():
    user_input = request.args.get('msg')
    return jsonify({'response': chatbot.respond(user_input)})


# Run the app on the appropriate port
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
