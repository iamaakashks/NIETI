import os
from flask import Flask, render_template, request, jsonify
import nltk
from nltk.chat.util import Chat, reflections

#NLTK package
nltk.download('punkt')

app = Flask(__name__)

# general chatbot patterns
patterns = [
    (r'hi|hello|hey', ["Hello! My name is NIETI. How can I assist you today?"
                       ]),
    #college name
    (r'(.*)college name(.*)',
     ['The National Institutes of Engineering, Mysuru.']),
    #about nie
    (r'(.*)about(.*)nie(.*)', [
        'The National Institute of Engineering (NIE), established in the year 1946.',
        'NIE is a grant-in-aid institution and approved by the All India Council for Technical Education (AICTE), New Delhi. NIE got autonomous status from Visvesvaraya Technological University, Belagavi in 2007.  It has been accredited by NAAC.'
    ]),
    #milestones
    (r'(.*)milestone(.*)', [
        "1946->NIE started by a 'three-man army' of retired engineers \n1950->UoM (University of Mysore) Affiliation \n1986->AICTE approval \n1998->VTU Affiliation \n2007->Grant of Autonomy by VTU \n2020->Accreditation by NAAC\n"
    ]),
    #leaders
    (r'(.*)leaders(.*)|(.*)leading(.*)', [
        'Hon. President: Dr. Ranganath M S \nVice President: Mr. Niranjan Simha S \nHon.Secretary: Mr.  UdayShankar S B \nDirector: Mr.  Srinath Batni'
    ]),
    #principal
    (r'(.*)Principal(.*)|(.*)principle(.*)',
     ['Hon. Principal: Dr. Rohini Nagapadma']),
    # Admission process
    (r'(.*)admission process(.*)|(.*)admission(.*)', [
        'Candidates need to register for entrance exams like KCET or COMEDK-UCET for BE admission.\nFor Management Quota, registration will be done on the official website of the institute.\nNIE Mysore takes admissions to MCA and MTech programmes is through the Karnataka PGCET conducted by the Karnataka Examination Authority (KEA).\nFor detailed information, visit our official admissions page: <a href="https://nie.ac.in/admission/">(https://nie.ac.in/admission/</a>)'
    ]),
    #documents required
    (r'(.*)documents(.*)|(.*)documents(.*)required(.*)', [
        '<a href="https://nie.ac.in/wp-content/uploads/2023/08/1st-Year-B.E-Academic-Year-2023-24-with-the-documents-to-be-produced..pdf">https://nie.ac.in/wp-content/uploads/2023/08/1st-Year-B.E-Academic-Year-2023-24-with-the-documents-to-be-produced..pdf</a>'
    ]),
    #departments
    (r'(.*)departments(.*)', [
        'North Campus: Computer Science & Engineering\nInformation Science & Engineering\nComputer Science Engineering (AI & ML)'
    ]),
    #cse departments
    (r'(.*)cse(.*)', [
        'The Department of CS&E and AI&ML  has 9 faculty with Ph.D degrees. The current faculty strength is 34 which includes 5 Professors, 4 Associate Professors, 25 Assistant Professors.'
    ]),
    # Handle general mentions of "fee structure" more flexibly
    (r'(.*)fee(.*)|(.*)fees(.*)|(.*)total cost(.*)', [
        'BE: Total fees for the programme is 10.66 Lakhs(approx).\n Mtech: Total fees for the programme is 1.51 Lakhs(approx).\nMCA: Total fees for the programme is 1.28 Lakhs(approx).\nTo get exact number, Visit: <a href="https://nie.ac.in/admission/">(https://nie.ac.in/admission/)</a>'
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
        'NIE NORTH\n+91 –6366914772\n<a href="northcampus@nie.ac.in">northcampus@nie.ac.in</a>\n\nNIE SOUTH\n+91 – 63669 14771\n<a href="southcampus@nie.ac.in">southcampus@nie.ac.in</a>'
    ]),
    # Handle general mentions of "location" more flexibly
    (r'(.*)location(.*)', [
        'NIE College is located in Mysuru, Karnataka. Visit the campus at the North Campus for a tour. For location details, check: [Location]<a href="https://nie.ac.in/contact-us/">https://nie.ac.in/contact-us/</a>'
    ]),
    #placements
    (r'(.*)placements(.*)|(.*)placement(.*)|(.*)placements Statistics(.*)|(.*)placement Statistics(.*)|(.*)placement Statistic(.*)|(.*)placements Statistic(.*)|(.*)placements Stats(.*)|(.*)placement Stats(.*)',
     [
         'Highest package offered:	INR 56 LPA\nAverage package:INR 9 LPA\nNo. of eligible students: 821\nNo. of students placed: 708\nTotal offers made: 960+\nNo. of Dream offers: 500+\nNo. of companies visited: 348\nPopular recruiters: Dell, Zomato, IBM, Samsung, Infosys \n for more info visit <a href="https://nie.ac.in/placements/">https://nie.ac.in/placements/</a>'
     ]),
    #activities
    (r'(.*)activities(.*)|(.*)extra-curricular activities(.*)|(.*)clubs(.*)|(.*)extra curricular activities(.*)',
     [
         'NIE offers a range of clubs, including technical ones like OWASP, ONYX, IEEE, and The Byte Club, as well as non-technical options like the Kannada Club and ED-Soc literature Club, for more info <a href="https://nie.ac.in/campus-life/#student-activities">https://nie.ac.in/campus-life/#student-activities</a>'
     ]),
    #hostel facilities
    (r'(.*)hostel(.*)|(.*)hostel facilities(.*)', [
        'The Institute has constructed two brand new hostels – one for boys and another one for girls with all modern amenities.',
        'The boys’ hostel building is G+4 floors, with 49 triple accommodations, 2 double accommodations and 4 guest rooms.\nThe girls’ hostel building is G+4 floors, with 40 triple accommodation, 2 double accommodation and 4 guest rooms. for more info <a href="https://nie.ac.in/campus-life/#student-housing">https://nie.ac.in/campus-life/#student-housing</a>'
    ]),

    #vision-mission
    (r'(.*)mission(.*)|(.*)vision(.*)|(.*)vision(.*)mission(.*)', [
        'Vision: To be a globally recognized institution offering value-based technical and scientific education.\nMission: Deliver quality engineering education with strong theoretical and practical foundations.'
    ]),

    #seat-matrix
    (r'(.*)seat(.*)|(.*)seat matrix(.*)', [
        'click at the link to get the update: <a href="https://nie.ac.in/admission/seat-matrix-updated-2024/">https://nie.ac.in/admission/seat-matrix-updated-2024/</a>'
    ]),

    #faculties
    (r'(.*)faculty(.*)|(.*)faculties(.*)|(.*)faculty details(.*)', [
        'NIE has experienced and supportive faculty members who are dedicated to providing quality education and fostering student growth'
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
    bot_response = chatbot.respond(user_input)
    # Replace newlines with <br> to format the output correctly in HTML
    bot_response = bot_response.replace("\n", "<br>")
    return jsonify({'response': bot_response})



# Run the app on the appropriate port
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
