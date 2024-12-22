import os
from flask import Flask, render_template, request, jsonify
import nltk
from nltk.chat.util import Chat, reflections

# Download the necessary NLTK package
nltk.download('punkt')

app = Flask(__name__)

# Define more general chatbot patterns to handle varied user inputs
patterns = [
    (r'hi|hello|hey', ["Hello! My name is NIETI. How can I assist you today?"
                       ]),
    #college name
    (r'(.*)college name(.*)',
     ['The National Institutes of Engineering, Mysuru.']),
    # Handle general mentions of "admission process" more flexibly
    (r'(.*)admission process(.*)|(.*)admission(.*)', [
        'Candidates need to register for entrance exams like KCET or COMEDK-UCET for BE admission.\nFor Management Quota, registration will be done on the official website of the institute.\nNIE Mysore takes admissions to MCA and MTech programmes is through the Karnataka PGCET conducted by the Karnataka Examination Authority (KEA).\nFor detailed information, visit our official admissions page: (https://nie.ac.in/admission/)'
    ]),
    # Handle general mentions of "fee structure" more flexibly
    (r'(.*)fee(.*)|(.*)fees(.*)|(.*)total cost(.*)', [
        'BE: Total fees for the programme is 10.66 Lakhs(approx).\n Mtech: Total fees for the programme is 1.51 Lakhs(approx).\nMCA: Total fees for the programme is 1.28 Lakhs(approx).\nTo get exact number, Visit: (https://nie.ac.in/admission/)'
    ]),
    #campuses
    (r'(.*)campus(.*)|(.*)campuses(.*)',
     ['NIE has two campuses. NIE North and NIE South.']),

    # Handle general mentions of "courses offered" more flexibly
    (r'(.*)courses(.*)', [
        'NIE offers 3 UG Courses and 1 PG Course at North Campus and 4 UG Courses and 9 PG Courses at South Campus'
    ]),
    # Handle general mentions of "contact" or "contact us" more flexibly
    (r'(.*)contact(.*)', [
        'NIE NORTH\n+91 –6366914772\nnorthcampus@nie.ac.in\n\nNIE SOUTH\n+91 – 63669 14771\nsouthcampus@nie.ac.in'
    ]),
    # Handle general mentions of "location" more flexibly
    (r'(.*)location(.*)', [
        'NIE College is located in Mysuru, Karnataka. Visit the campus at the North Campus for a tour. For location details, check: [Location](https://nie.ac.in/contact-us/)'
    ]),
    #placements
    (r'(.*)placements(.*)|(.*)placement(.*)|(.*)placements Statistics(.*)|(.*)placement Statistics(.*)|(.*)placement Statistic(.*)|(.*)placements Statistic(.*)|(.*)placements Stats(.*)|(.*)placement Stats(.*)',
     [
         'Highest package offered:	INR 56 LPA\nAverage package:INR 9 LPA\nNo. of eligible students: 821\nNo. of students placed: 708\nTotal offers made: 960+\nNo. of Dream offers: 500+\nNo. of companies visited: 348\nPopular recruiters: Dell, Zomato, IBM, Samsung, Infosys'
     ]),
    #activities
    (r'(.*)activities(.*)|(.*)extra-curricular activities(.*)|(.*)clubs(.*)|(.*)extra curricular activities(.*)',
     [
         'NIE offers a range of clubs, including technical ones like OWASP, ONYX, IEEE, and The Byte Club, as well as non-technical options like the Kannada Club and ED-Soc literature Club. Would you like details on any specific club?'
     ]),
    #hostel facilities
    (r'(.*)hostel(.*)|(.*)hostel facilities(.*)', [
        'The Institute has constructed two brand new hostels – one for boys and another one for girls with all modern amenities.',
        'The boys’ hostel building is G+4 floors, with 49 triple accommodations, 2 double accommodations and 4 guest rooms.\nThe girls’ hostel building is G+4 floors, with 40 triple accommodation, 2 double accommodation and 4 guest rooms.'
    ]),

    #seat-matrix
    (r'(.*)seat(.*)|(.*)seat matrix(.*)', [
        'click at the link to get the update: https://nie.ac.in/admission/seat-matrix-updated-2024/'
    ]),

    #faculties
    (r'(.*)faculty(.*)|(.*)faculties(.*)|(.*)faculty details(.*)', [
        'NIE has experienced and supportive faculty members who are dedicated to providing quality education and fostering student growth. click here to get more about this: https://nie.ac.in/faculty-corner/'
    ]),

    #transportation
    (r'(.*)Transport(.*)|(.*)Transportation(.*)', [
        'NIE provides bus facilities for day-scholars and also between the south-campus hostel and north-campus.'
    ]),

    # Handle gratitude in a general way
    (r'(.*) (thanks|thank you)(.*)',
     ['You’re welcome! Let me know if you have more questions.']),
    # Catch-all for unrecognized queries
    (r'(.*)', [
        'Sorry, I didn’t quite understand that. Can you please ask again? or contact southcampus@nie.ac.in or northcampus@nie.ac.in'
    ])
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
