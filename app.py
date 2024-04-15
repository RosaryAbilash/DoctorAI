from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_session import Session
import joblib
import model


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'DoctorAI'
app.config['SESSION_TYPE'] = 'filesystem'  # Use filesystem for session storage
db = SQLAlchemy(app)
Session(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'kioskdocai@gmail.com'
app.config['MAIL_PASSWORD'] = 'laxinbzjvgndxcmo'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)
selected_symptoms = []
sender = 'kioskdocai@gmail.com'

# p = "D:\AI Kiosk\CODE\Sprint_1\symptom_suggestion_model.joblib"
# Load the trained symptom suggestion model
# symptom_suggestion_model = joblib.load('suggest_symptoms_function.joblib')


class User(db.Model):
    # __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    mobile = db.Column(db.String(15), unique=True, nullable=False)



@app.route('/debug_session')
def debug_session():
    print(session)
    return 'Session data printed in the console'

@app.route('/clear_session')
def clear_session():
    session.clear()
    print(session)
    return "SESSION CLEARED SUCCESSFULLY...."

@app.route('/')
def landing_page():
    return render_template('landing_page.html')

@app.route('/voice')
def voice():
    return render_template("voice_test.html")


@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/users')
def users():
    # Query all users from the database
    all_users = User.query.all()
    return render_template('users.html', users=all_users)
    
@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/emergency_connect')
def emergency_connect():
    send_alert()
    return render_template('emergency_connect.html')



def send_alert():
    msg = Message("Emergency - DoctorAI Patient Waiting in room", sender=sender, recipients=['rosaryabilash@gmail.com'])
    msg.body="Meeting Link 'https://meet.google.com/ajh-xcwt-ukv'"
    mail.send(msg)

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    mobile = request.form['mobile']
    new_user = User(name=name, age=age, gender=gender, mobile=mobile)
    db.session.add(new_user)
    db.session.commit()
    # Redirect to signin page after successful registration
    return redirect(url_for('signin'))

@app.route('/signin_process', methods=['POST'])
def signin_process():
    mobile = request.form['mobile']
    # You might want to implement actual authentication logic here
    # For simplicity, let's assume a user is signed in successfully if the mobile number exists in the database
    user = User.query.filter_by(mobile=mobile).first()
    if user:
        # Create a session for the user
        session['user'] = {
            'id': user.id,
            'name': user.name,
            'age': user.age,
            'gender': user.gender,
            'mobile': user.mobile
        }
        # Redirect to the dashboard page after successful sign-in
        return redirect(url_for('dashboard'))
    else:
        return "Sign in failed. Mobile number not found."


@app.route('/consultation_history')
def consultation_history():
    # Implement the Consultation History feature logic here
    return "Consultation History Page"

@app.route('/logout')
def logout():
    # You can implement actual logout logic here (clearing session, etc.)
    session.clear()
    return redirect(url_for('landing_page'))

@app.route('/dashboard')
def dashboard():
    # Assume user is logged in, and user data is available in the session
    user = session.get('user')
    if user:
        return render_template('dashboard.html', user=user)
    else:
        # Redirect to the landing page if user is not logged in
        # return redirect(url_for('landing_page'))
        return render_template('dashboard.html', user=user)

def check_session_data():
    if 'health_data' not in session:
        session['health_data'] = {
            'systolic': "",
            'diastolic': "",
            'pulse': "",
            'height': "",
            'weight': ""
        }

@app.route('/begin_health_assessment')
def begin_health_assessment():
    # Check if session data exists before resetting
    check_session_data()
    
    # Redirect to the BP measurement page
    return redirect(url_for('bp_measurement'))


@app.route('/bp_measurement', methods=['GET', 'POST'])
def bp_measurement():
    check_session_data()
    if request.method == 'POST':
        
        # Check if the 'systolic' and 'diastolic' keys exist in the form data
        if 'systolic' in request.form and 'diastolic' in request.form:
            session['health_data']['systolic'] = request.form['systolic']
            session['health_data']['diastolic'] = request.form['diastolic']
            print(session['health_data'])
        else:
            # Handle the case where the keys are not present (e.g., form data is not submitted correctly)
            return "Invalid form data. Please make sure to submit systolic and diastolic values."
        # Redirect to the next measurement page (pulse measurement)
        return redirect(url_for('pulse_measurement'))

    return render_template('health_assessment_bp.html')

@app.route('/pulse_measurement', methods=['GET', 'POST'])
def pulse_measurement():
    check_session_data()
    if request.method == 'POST':
        session['health_data']['pulse'] = request.form['pulse']
        print(session['health_data'])
        
        return redirect(url_for('temperature_measurement'))

    return render_template('health_assessment_pulse.html')

@app.route('/temperature_measurement', methods=['GET', 'POST'])
def temperature_measurement():
    check_session_data()

    if request.method == 'POST':
        session['health_data']['body_temperature'] = request.form['body_temperature']
        print(session['health_data'])
        return render_template('health_assessment_height_weight.html')

    return render_template('health_assessment_temperature.html')

@app.route('/height_weight_measurement', methods=['GET', 'POST'])
def height_weight_measurement():
    check_session_data()
    if request.method == 'POST':
        session['health_data']['height'] = request.form['height']
        session['health_data']['weight'] = request.form['weight']
        # Process the collected health data (store in the database, perform analysis, etc.)
        # For now, let's just display a summary
        summary = session['health_data']
        bmi = calculate_bmi(int(summary['height']), int(summary['weight']))
        return render_template('health_assessment_summary.html', summary=summary, bmi=bmi)
    return render_template('health_assessment_height_weight.html')

def calculate_bmi(height, weight):
    if height > 0 and weight > 0:
        # Convert height to meters
        height_meters = height / 100
        # Calculate BMI using the original formula: weight (kg) / (height (m))^2
        bmi = weight / (height ** 2)
        # Round BMI to two decimal places
        return round(bmi, 2)*10
    else:
        # Handle case where height or weight is zero or negative
        return None


@app.route('/health_assessment_summary', methods=['GET'])
def health_assessment_summary():
    # Retrieve the health data from the session
    summary = session.get('health_data', {})
    # Calculate BMI if height and weight are available
    print("??????")
    bmi = calculate_bmi(summary['height'], summary['weight'])
    print("ffffff")
    return render_template('health_assessment_summary.html', summary=summary, bmi=bmi)



# @app.route('/begin_preliminary_diagnosis')
# def begin_preliminary_diagnosis():
#     session['selected_symptoms'] = []
#     session['symptom_count'] = 0
#     session['severity'] = []
#     # Get the common symptoms from your dataset or wherever they are stored
#     common_symptoms = ['Fever', 'coughing', 'Headache', 'Fatigue', 'Diarrhea', 'runny nose', 'Nausea', 'Vomiting', 'Headache', 'Muscle Ache', 'Shortness of Breath', 'Joint Pain', 'Dizziness', 'Sore Throat', 'Stomach Pain', 'Skin Rash', 'Chest Pain', 'Eye Irritation', 'Frequent Urination']
#     return render_template('preliminary_diagnosis.html', common_symptoms=common_symptoms)


@app.route('/begin_preliminary_diagnosis')
def begin_preliminary_diagnosis():
    session['selected_symptoms'] = []
    session['symptom_count'] = 0
    session['severity'] = []
    body_parts = ['head', 'neck', 'chest', 'arms', 'abdomen', 'pelvis', 'back', 'buttocks', 'legs']
    return render_template('select_body_part1.html', body_parts=body_parts)


@app.route('/body_part', methods=['POST'])
def body_part():
    selected_body = request.form.get('selectedSymptom')
    body_parts = []
    if selected_body == 'head':
        body_parts = ['scalp', 'fore head', 'eyes','nose','ears','mouth']
    elif selected_body == 'neck':
        body_parts = ['throat'] 
    elif selected_body == 'chest':
        body_parts = ['upper chest and breast','sternum'] 
    elif selected_body == 'arms':
        body_parts = ['shoulder', 'hand',] 
    elif selected_body == 'abdomen':
        body_parts = ['upper abdomen', 'epigastric'] 
    elif selected_body == 'pelvis':
        body_parts = ['hip', 'genitals'] 
    elif selected_body == 'back':
        body_parts = ['upper back', 'lower back'] 
    elif selected_body == 'buttocks':
        body_parts = ['Rectum'] 
    elif selected_body == 'legs':
        body_parts = ['Thigh', 'leg'] 
    
    return render_template('select_body_part.html', body_parts=body_parts)



@app.route('/symptoms_body_part', methods=['POST'])
def symptoms_body_part():
    selected_body_part = request.form.get('selectedSymptom')
    common_symptoms = []
    if selected_body_part == 'scalp':
        common_symptoms = ['hair loss', 'headache', 'dry damp skin']
    
    
    elif selected_body_part == 'fore head':
        common_symptoms = ['fatigue', 'fever', 'headache', 'aching']
    
    
    elif selected_body_part == 'eyes':
        common_symptoms = ['watery eye', 'redness eye', 'swelling around eye', 'dry eye', 'inflamed eye','drooping eyelid', 'blindness one eye',  'eye pain',  'burning redness eye',   'eye strain',  'temporary fleeting vision one eye', 'non painful cyst middle eyelid', 'nearsightedness', 'distant object appear blurry', 'close object appear blurry', 'blurred vision']
    
    
    elif selected_body_part == 'nose':
        common_symptoms = ['runny nose', 'trouble breathing nose',  'post nasal drip', 'loss smell', 'sensitivity smell', 'breathing problem']
    
    
    elif selected_body_part == 'ears':
        common_symptoms = ['itchy ear', 'ear pain','pain around ear',  'hearing loss', 'sensitivity sound']
    
    
    elif selected_body_part == 'mouth':
        common_symptoms = [ 'mouth ulcer', 'dry mouth', 'trouble opening mouth', 'mouth sore', 'bleeding gum', 'gum disease', 'tooth loss', 'vomiting', 'nausea vomiting', 'coughing', 'decreased taste', 'loose teeth', 'change taste']
    
    
    elif selected_body_part == 'throat':
        common_symptoms = ['large lymph node', 'swollen lymph node',  'enlarged lymph node neck', 'sore throat',  'enlarged thyroid', 'prolonged cough']
    
    
    elif selected_body_part == 'upper chest and breast':
        common_symptoms = ['newly inverted nipple', 'fluid nipple','chest discomfort', 'chest tightness', 'sharp chest pain', 'shortness breath', 'lump breast', 'red scaly patch skin breast', 'tender breast', 'change breast shape', 'localized breast pain redness', 'heartburn', 'ringing ear heartbeat', 'fast heart rate', 'chest discomfort', 'chest tightness', 'sharp chest pain', 'shortness breath', 'low blood pressure']
    
    
    elif selected_body_part == 'sternum':
        common_symptoms = ['heartburn', 'ringing ear heartbeat', 'fast heart rate', 'chest discomfort', 'chest tightness', 'sharp chest pain', 'shortness breath', 'low blood pressure']
    
    
    elif selected_body_part == 'shoulder':
        common_symptoms = ['weak muscle', 'muscle weakness', 'stiff muscle', 'muscle joint pain', 'sudden loss muscle strength']
    
    
    elif selected_body_part == 'hand':
        common_symptoms = ['painful tender outer part elbow','sore wrist', 'swelling hand foot', 'tingling hand foot','weak grip', 'skin peeling', 'pale skin', 'skin blister', 'weakness limb', 'half ring finger', 'tingling thumb']


    elif selected_body_part == 'upper abdomen':
        common_symptoms = ['gas','stomach pain', 'enlarged spleen', 'bloating', 'severe pain lower back abdomen', 'swelling abdomen', 'vomiting', 'constipation', 'increased breathing rate', 'bad breath', 'jaundice', 'gas', 'poor appetite', 'decreased appetite', 'ulcer', 'abdominal cramp', 'fullness', 'dehydration']

    
    elif selected_body_part == 'epigastric':
        common_symptoms = ['gas','diarrhea', 'diarrhea mixed blood', 'difficulty eating', 'nausea vomiting weight loss dehydration occur', 'nausea', 'nausea vomiting', 'heartburn']


    elif selected_body_part == 'hip':
        common_symptoms = ['weak muscle', 'muscle weakness', 'stiff muscle', 'muscle joint pain', 'sudden loss muscle strength']
    


    elif selected_body_part == 'genitals':
        common_symptoms = ['blood urine', 'dark urine', 'discharge penis', 'missed period', 'period vigorous shaking', 'painful heavy period', 'frequent urination', 'burning urination', 'needing urinate often', 'feeling need urinate right away', 'infertility', 'testicular pain', 'vaginal bleeding', 'vaginal discharge', 'white patch vaginal discharge', 'bad smelling vaginal discharge']


    elif selected_body_part == 'upper back':
        common_symptoms = ['pain going leg lower back', 'severe pain lower back abdomen', 'better sitting worse lying']

    elif selected_body_part == 'lower back':
        common_symptoms = ['pain going leg lower back', 'severe pain lower back abdomen', 'better sitting worse lying']

    elif selected_body_part == 'Rectum':
        common_symptoms = ['blood stool']

    elif selected_body_part == 'Thigh':
        common_symptoms = ['weak muscle', 'muscle weakness', 'stiff muscle', 'muscle joint pain', 'sudden loss muscle strength']
    

    elif selected_body_part == 'leg':
        common_symptoms = ['muscle cramp',' painful blister lower leg', 'sore arm leg', 'bowed leg', 'leg swelling', 'weakness numbness affected leg', 'pain going leg lower back', 'painful joint base big toe']


    

    return render_template('body_symptoms_display.html', selected_body_part=selected_body_part, common_symptoms=common_symptoms)



@app.route('/preliminary_diagnosis', methods=['GET', 'POST'])
def preliminary_diagnosis():
    if 'prev_suggestions' not in session:
        session['prev_suggestions'] = []

    if request.method == 'POST':
        selected_symptom = request.form['selectedSymptom']
        selected_severity = request.form['selectedSeverity']

        print("0000000000000000000000000000")
        print(selected_severity, selected_symptom)
        # Store the selected symptom and severity in session
        session['selected_symptoms'].append((selected_symptom, selected_severity))
        session['symptom_count'] += 1
        session['severity'].append(selected_severity)

        # If the symptom count is less than the maximum allowed iterations
        if session['symptom_count'] < 5:  # Adjust the maximum iterations as needed
            # Get suggestions for additional symptoms based on selected symptoms
            print("++++++", selected_symptom, "++++++")
            suggested_symptoms = model.suggest_symptoms([selected_symptom])
            # suggested_symptoms = model.suggest_symptoms([test])

            
            # Check for convergence based on similarity threshold and change in suggestions
            similarity_threshold = 0.5  # Example threshold (adjust as needed)
            change_threshold = 0.2      # Example threshold (adjust as needed)
            
            if len(set(suggested_symptoms).intersection(session['prev_suggestions'])) > similarity_threshold * len(session['prev_suggestions']):
                if len(set(suggested_symptoms).difference(session['prev_suggestions'])) < change_threshold * len(session['prev_suggestions']):
                    # Convergence reached, perform final diagnosis
                    # diagnosis_result = "Final diagnosis result"
                    # return render_template('diagnosis_results.html', diagnosis_result=diagnosis_result)
                    return redirect(url_for('diagnosis_results'))


            # Update previous suggestions for next iteration
            session['prev_suggestions'] = suggested_symptoms

            return render_template('preliminary_diagnosis.html', common_symptoms=suggested_symptoms)
        else:
            # If maximum iterations reached, perform final diagnosis and display results
            # diagnosis_result = "Final diagnosis result"
            # return render_template('diagnosis_results.html', diagnosis_result=diagnosis_result)
            return redirect(url_for('diagnosis_results'))

    # If it's a GET request, render the page with common symptoms for all diseases
    common_symptoms = ['Fever', 'Cough', 'Headache', 'Fatigue']  # Example common symptoms
    return render_template('preliminary_diagnosis.html', common_symptoms=common_symptoms)



Dmodel = joblib.load('trained_model.joblib')

# Other routes and functions...

@app.route('/diagnosis_results')
def diagnosis_results():
    # Get selected symptoms from session
    selected_symptoms = [symptom[0] for symptom in session['selected_symptoms']]
    severity = session['severity']
    most_sever = max(set(severity), key=severity.count)
    
    # Make predictions using the model
    predictions = Dmodel.predict_proba(selected_symptoms)

    # Get the top three predicted diseases along with their probabilities
    top_three_indices = predictions.argsort()[:, -3:][0][::-1]
    top_three_diseases = Dmodel.classes_[top_three_indices]
    top_three_probabilities = predictions[0][top_three_indices]

    # Combine diseases and probabilities into a list of dictionaries
    results = [{'disease': disease, 'probability': round(probability * 100, 2)} for disease, probability in zip(top_three_diseases, top_three_probabilities)]
    print(severity)
    return render_template('diagnosis_results.html', results=results, most_sever=most_sever)

if __name__ == '__main__':
    app.run(debug=True)