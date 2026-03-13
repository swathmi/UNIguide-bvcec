from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
import secrets
from datetime import datetime, timedelta
from authlib.integrations.flask_client import OAuth
from llm_service import call_llm
import random
import logging
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
from flask_mail import Mail, Message






# ================= DATABASE & AUTH =================
app = Flask(__name__)
# Load environment variables from backend/.env (if present)
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))



# Prefer environment values when available
app.config['MAIL_SERVER'] = os.environ.get("MAIL_SERVER")
app.config['MAIL_PORT'] = int(os.environ.get("MAIL_PORT"))
app.config['MAIL_USE_TLS'] = os.environ.get("MAIL_USE_TLS") == "True"
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")

app.config['MAIL_DEFAULT_SENDER'] = (
    "Swathmi - UNIGuide AI",
    os.environ.get("MAIL_USERNAME")
)

mail = Mail(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'SQLALCHEMY_DATABASE_URI',
    'sqlite:///uniguide_users.db'
)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ================= OAUTH (Google) =================
oauth = OAuth(app)

# Check if Google credentials are set, if not create a dummy config to prevent errors
google_client_id = os.environ.get('GOOGLE_CLIENT_ID', 'NOT_SET')
google_client_secret = os.environ.get('GOOGLE_CLIENT_SECRET', 'NOT_SET')

oauth.register(
    name='google',
    client_id=google_client_id,
    client_secret=google_client_secret,
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v2/',
    client_kwargs={'scope': 'openid email profile'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
)

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    reset_token = db.Column(db.String(255), unique=True, nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)
    profile_image = db.Column(db.String(200), nullable=True)
    role = db.Column(db.String(20), default="student")
    otp = db.Column(db.String(6))
    otp_expiry = db.Column(db.DateTime)




    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    

    def generate_otp(self):
        otp = str(random.randint(100000, 999999))
        self.otp = otp
        self.otp_expiry = datetime.utcnow() + timedelta(minutes=5)
        return otp



class ChatSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('chat_session.id'))
    message = db.Column(db.Text)
    response = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    
    

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# Initialize CORS
CORS(app)

# ================= STUDENTS SERVICE =================
from services.students_service import handle_student_query

# ================= INTENT DETECTORS =================
# Lazy loaded in chat() function to avoid TensorFlow import issues
from services.programs_intents import detect_courses_programs_intent
from services.college_overview_intents import detect_college_overview_intent
from services.admissions_intents import detect_admission_intent
from services.events_intents import detect_institution_intent

# ================= SERVICE FUNCTIONS =================
from services.programs_service import get_courses_programs_response
from services.college_overview_service import get_college_overview_response
from services.admissions_service import get_admissions_response

# ================= EVENTS =================
from services.events_intents import detect_institution_intent
from services.events_services import get_institution_response


# ================= RAG + MEDIA =================
from services.media_service import get_media_response

# ================= DEPARTMENTS =================
# Lazy loaded in chat() function
from services.csm_intents import detect_cse_aiml_intent
from services.csm_services import get_cse_aiml_department_response
from services.aiml_intents import detect_aiml_intent
from services.aiml_services import get_aiml_department_response
from services.cad_intents import detect_cad_intent
from services.cad_services import get_cad_department_response
from services.civil_intents import detect_civil_intent
from services.civil_services import get_civil_department_response
from services.cse_intents import detect_cse_intent
from services.cse_services import get_cse_department_response
from services.ece_intents import detect_ece_intent
from services.ece_services import get_ece_department_response
from services.eee_intents import detect_eee_intent
from services.eee_services import get_eee_department_response
from services.it_intents import detect_it_intent
from services.it_services import get_it_department_response
from services.mech_intents import detect_mech_intent
from services.mech_services import get_mech_department_response
from services.placement_intents import detect_placement_intent
from services.placement_services import get_placement_response




# ================= WEBSITE SEARCH =================

# ================= DOMAIN KEYWORDS =================
PROGRAM_KEYWORDS = [
    "course", "courses",
    "ug program", "pg program", "degree program", "course structure",
    "btech", "mtech", "bachelor", "master",
    "intake", "seats", "capacity",
    "fees", "fee", "package", "salary", "lpa",
    "eligibility", "internship",
    "syllabus", "curriculum", "course details"
]

EVENT_KEYWORDS = [
    "event", "events", "activities",
    "technical activities", "cultural activities", "sports",
    "workshop & seminars",  "guest lecture",
    "hackathon", "symposium",
    "club", "nss", "ncc",
    "career", "alumni", "faculty paper publications",
    "recent activities",
    "news", "poster", "gallery"
]

ADMISSION_KEYWORDS = [
    "admission", "apply", "join",
    "eamcet", "ecet", "management quota",
    "lateral entry", "documents",
    "counseling", "seat allotment",
    "reservation"
]

# ================= DEPARTMENT KEYWORDS =================
CSM_KEYWORDS  = ["csm", "cse aiml", "csm staff", "csm faculty"]
AIML_KEYWORDS = ["aiml", "artificial intelligence"]
CAD_KEYWORDS  = ["cad", "aids", "cse aids"]
CE_KEYWORDS   = ["civil", "ce", "civil engineering"]
CSE_KEYWORDS  = ["cse", "computer science"]
ECE_KEYWORDS = ["ece", "electronics", "electronics and communication"]
EEE_KEYWORDS = ["eee", "electrical", "electrical and electronics"]
IT_KEYWORDS = ["it", "information technology"]
MECH_KEYWORDS = ["mech", "mechanical"]

# ================= PLACEMENT KEYWORDS =================
PLACEMENT_KEYWORDS = [
    "placement", "training", "material", "aptitude", "reasoning",
    "programming", "java", "python", "sql",
    "company", "infosys", "tcs", "wipro", "accenture",
    "attendance", "circular", "faculty development",
    "notes", "resources", "materials", "language", "coding",
    "placement resources", "placement materials", "placement program",
    "c language", "c programming", "java programming", "python programming",
    "aptitude materials", "quantitative", "logical", "verbal", "english",
    "circulars", "updates", "announcements", "fdp", "development programs",
    "company placements", "placed", "recruitment", "tcs placement",
    "programming language", "programming notes", "language tutorial"
]

# ================= ROUTES =================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/features")
def features():
    return render_template("features.html")

@app.route("/student-services")
def student_services():
    return render_template("student-services.html")

@app.route("/contact")
def contact():
    return render_template("contact.html") 

@app.route("/profile")
@login_required
def profile():
    sessions = ChatSession.query.filter_by(
        user_id=current_user.id
    ).order_by(ChatSession.created_at.desc()).all()

    return render_template("profile.html", sessions=sessions)


@app.route("/admin")
@login_required
def admin_dashboard():
    if current_user.role != "admin":
        return "Access Denied", 403

    users = User.query.all()
    sessions = ChatSession.query.all()
    messages = ChatMessage.query.all()

    return render_template(
        "admin.html",
        users=users,
        sessions=sessions,
        messages=messages
    )




# ================= AUTHENTICATION ROUTES =================
@app.route("/signup", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.get_json()
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()
        
        if not name or not email or not password:
            return jsonify({"error": "All fields required"}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already registered"}), 400
        
        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print("===== SIGNUP SUCCESS =====")
        print("Sending mail to:", email)

        

        try:
            msg = Message(
                subject="Welcome to UNIGuide AI 🎉",
                recipients=[email]
            )

            msg.body = f"""
Hi {name},

Your account has been successfully created in UNIGuide AI.

You can now login and explore the chatbot.

Thank you,
Swathmi
UNIGuide AI
"""
            mail.send(msg)
            print("✅ Welcome email sent successfully")

        except Exception as e:
            print("❌ Email sending failed:", e)
        
        login_user(user)
        return jsonify({"success": True, "user": {"name": user.name, "email": user.email}})
    
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return jsonify({"error": "Invalid email or password"}), 401
        
        login_user(user)
        return jsonify({"success": True, "user": {"name": user.name, "email": user.email}})
    
    return render_template("login.html")


@app.route('/login/google')
def login_google():
    # Check if Google credentials are configured
    if google_client_id == 'NOT_SET' or google_client_secret == 'NOT_SET':
        return jsonify({
            "error": "Google OAuth not configured. Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables."
        }), 503
    
    try:
        redirect_uri = url_for('auth_google_callback', _external=True)
        return oauth.google.authorize_redirect(redirect_uri)
    except Exception as e:
        print(f"[ERROR] Google OAuth redirect failed: {str(e)}")
        return jsonify({"error": f"OAuth configuration error: {str(e)}"}), 500

@app.route("/upload-profile", methods=["POST"])
@login_required
def upload_profile():
    file = request.files.get("image")
    if file:
        filename = file.filename
        upload_folder = os.path.join("static", "uploads")
        os.makedirs(upload_folder, exist_ok=True)

        file.save(os.path.join(upload_folder, filename))
        current_user.profile_image = filename
        db.session.commit()

    return redirect(url_for("chat_page"))

@app.route("/change-password", methods=["POST"])
@login_required
def change_password():
    data = request.get_json()
    new_password = data.get("password")

    if len(new_password) < 6:
        return jsonify({"error": "Password too short"}), 400

    current_user.set_password(new_password)
    db.session.commit()

    return jsonify({"success": True})



@app.route('/auth/google')
def auth_google_callback():
    try:
        token = oauth.google.authorize_access_token()
    except Exception as e:
        print(f"[ERROR] Google OAuth token retrieval failed: {str(e)}")
        return jsonify({"error": "Failed to authenticate with Google"}), 403

    resp = oauth.google.get('userinfo')
    user_info = resp.json()
    email = user_info.get('email')
    name = user_info.get('name') or user_info.get('given_name') or (email.split('@')[0] if email else 'GoogleUser')

    if not email:
        return redirect(url_for('chat_page'))

    user = User.query.filter_by(email=email).first()
    if not user:
        # create user with random password (not used for OAuth)
        user = User(name=name, email=email)
        user.set_password(os.urandom(16).hex())
        db.session.add(user)
        db.session.commit()

    login_user(user)
    return redirect(url_for('chat_page'))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))



@app.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    email = data.get("email", "").strip()

    if not email:
        return jsonify({"error": "Email is required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        # Security reason – don't reveal email existence
        return jsonify({"success": True, "message": "If email exists, OTP sent"}), 200

    # Generate OTP
    # Generate OTP
    otp = user.generate_otp()
    db.session.commit()

    # Send OTP Email
    msg = Message(
        subject="UNIGuide AI - Password Reset OTP",
        recipients=[email]
    )

    msg.body = f"""
    Hi {user.name},

    Your OTP for password reset is:

    {otp}

    This OTP is valid for 5 minutes.

    If you did not request this, please ignore this email.

    - Swathmi
    UNIGuide AI
    """

    mail.send(msg)
    return jsonify({"success": True, "message": "OTP sent successfully"}), 200


    # TEMP: Print OTP in terminal (testing)
    
@app.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.get_json()
    email = data.get("email")
    otp = data.get("otp")

    user = User.query.filter_by(email=email).first()


    if not user or not user.otp or user.otp != otp:
        return jsonify({"message": "Invalid OTP"}), 400
    if not user.otp_expiry or datetime.utcnow() > user.otp_expiry:
        return jsonify({"message": "OTP expired"}), 400


    return jsonify({"message": "OTP verified"}), 200

@app.route("/reset-password-otp", methods=["POST"])
def reset_password_otp():
    data = request.get_json()
    email = data.get("email")
    new_password = data.get("new_password")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "User not found"}), 400

    user.set_password(new_password)

    # Clear OTP
    user.otp = None
    user.otp_expiry = None

    db.session.commit()

    return jsonify({"message": "Password reset successful"}), 200




@app.route("/user_info")
@login_required
def user_info():
    return jsonify({
        "name": current_user.name,
        "email": current_user.email,
        "first_letter": current_user.name[0].upper()
    })






# ================= CHAT ROUTE =================
# CHAT PAGE (UI)
# 🔹 Get Messages of a Session
# ================= CHAT PAGE =================
@app.route("/api/new_chat", methods=["POST"])
@login_required
def new_chat():
    session = ChatSession(
        user_id=current_user.id,
        title="New Chat"
    )
    db.session.add(session)
    db.session.commit()

    return jsonify({"session_id": session.id})
@app.route("/api/sessions")
@login_required
def get_sessions():
    sessions = ChatSession.query.filter_by(
        user_id=current_user.id
    ).order_by(ChatSession.created_at.desc()).all()

    return jsonify([
        {"id": s.id, "title": s.title}
        for s in sessions
    ])

@app.route("/chat", methods=["GET"])
@login_required
def chat_page():
    return render_template("chatbot.html")
@app.route("/learning-resources")
def learning_resources():
    return render_template("learning_resources.html")

@app.route("/api/session/<int:session_id>")
@login_required
def get_session_messages(session_id):
    messages = ChatMessage.query.filter_by(
        session_id=session_id
    ).order_by(ChatMessage.timestamp.asc()).all()

    import json
    response_data = []

    for m in messages:
        res = m.response
        try:
            res = json.loads(res)
        except:
            pass

        response_data.append({
            "message": m.message,
            "response": res
        })

    return jsonify(response_data)

# 🔹 Rename Chat Session
@app.route("/api/rename_session/<int:id>", methods=["POST"])
@login_required
def rename_session(id):
    data = request.get_json()

    session = ChatSession.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first()

    if session:
        session.title = data.get("title")
        db.session.commit()
        return jsonify({"success": True})

    return jsonify({"error": "Session not found"}), 404


# 🔹 Delete Chat Session
@app.route("/api/delete_session/<int:id>", methods=["DELETE"])
@login_required
def delete_session(id):
    session = ChatSession.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first()

    if session:
        ChatMessage.query.filter_by(session_id=id).delete()
        db.session.delete(session)
        db.session.commit()
        return jsonify({"success": True})

    return jsonify({"error": "Not found"}), 404
import requests
from flask import Response

@app.route('/proxy_pdf')
def proxy_pdf():
    pdf_url = request.args.get("url")

    if not pdf_url:
        return "No URL provided", 400

    try:
        r = requests.get(pdf_url)
        return Response(
            r.content,
            content_type='application/pdf'
        )
    except Exception as e:
        return "Failed to load PDF", 500





# CHAT API (AJAX / FETCH)
@app.route("/api/chat", methods=["POST"])
@login_required
def chat_api():
    

    # Lazy imports to avoid TensorFlow loading on app startup
    # from services.programs_intents import detect_courses_programs_intent
    # from services.programs_service import get_courses_programs_response
    # from services.college_overview_intents import detect_college_overview_intent
    # from services.college_overview_service import get_college_overview_response
    # from services.admissions_intents import detect_admission_intent
    # from services.admissions_service import get_admissions_response
    # from services.events_intents import detect_institution_intent
    # from services.events_services import get_institution_response
    # from services.placement_intents import detect_placement_intent
    # from services.placement_services import get_placement_response
    # from services.csm_intents import detect_cse_aiml_intent
    # from services.csm_services import get_cse_aiml_department_response
    # from services.aiml_intents import detect_aiml_intent
    # from services.aiml_services import get_aiml_department_response
    # from services.cad_intents import detect_cad_intent
    # from services.cad_services import get_cad_department_response
    # from services.civil_intents import detect_civil_intent
    # from services.civil_services import get_civil_department_response
    # from services.cse_intents import detect_cse_intent
    # from services.cse_services import get_cse_department_response
    # from services.ece_intents import detect_ece_intent
    # from services.ece_services import get_ece_department_response
    # from services.eee_intents import detect_eee_intent
    # from services.eee_services import get_eee_department_response
    # from services.it_intents import detect_it_intent
    # from services.it_services import get_it_department_response
    # from services.mech_intents import detect_mech_intent
    # from services.mech_services import get_mech_department_response
    # from services.students_service import handle_student_query
    
    data = request.get_json(force=True)
    import json

    def save_chat(session_id, question, answer):
        chat_session = ChatSession.query.filter_by(
            id=session_id,
            user_id=current_user.id
        ).first()

        if not chat_session:
            return

        # Auto title
        if chat_session.title == "New Chat":
            chat_session.title = question[:30]
            db.session.commit()

        # 🔥 FIX: Convert dict to JSON string
        if isinstance(answer, dict):
            answer_to_store = json.dumps(answer)
        else:
            answer_to_store = answer

        new_message = ChatMessage(
            session_id=chat_session.id,
            message=question,
            response=answer_to_store
        )

        db.session.add(new_message)
        db.session.commit()

    user_query = data.get("message", "").strip()

    if not user_query:
        return jsonify({"answer": "Please ask a valid question."})

    q = user_query.lower()

    intent = None

    # ==================================================
    # 0️⃣ MEDIA HANDLER
    # ==================================================
    try:
        media_answer = get_media_response(user_query)
        if media_answer:
            return jsonify({"answer": media_answer})
    except Exception:
        pass

    # ==================================================
    # 1️⃣ COLLEGE OVERVIEW
    # ==================================================
    overview_intent = detect_college_overview_intent(q)
    if overview_intent:
        try:
            answer = get_college_overview_response(overview_intent)
            save_chat(data.get("session_id"), user_query, answer)
            return jsonify({"answer": answer})
        except Exception as e:
            print("COLLEGE OVERVIEW ERROR:", e)
            return jsonify({"answer": "⚠️ College information temporarily unavailable."})

    # ==================================================
    # 1.5️⃣ PLACEMENT & TRAINING (BEFORE DEPARTMENTS to avoid substring conflicts)
    # ==================================================
    if any(k in q for k in PLACEMENT_KEYWORDS):
        placement_intent, placement_score = detect_placement_intent(q)
        if placement_intent:
            try:
                answer = get_placement_response(placement_intent)
                save_chat(data.get("session_id"), user_query, answer)
                return jsonify({"answer": answer})
            except Exception:
                return jsonify({"answer": "⚠️ Placement data unavailable."})

    # ==================================================
    
    # ==================================================
    # 2️⃣ DEPARTMENTS
    # ==================================================

    # 🔹 CSM – CSE AIML
    if any(k in q for k in CSM_KEYWORDS):
        intent = None
        score = 0.0

        intent, score = detect_cse_aiml_intent(q)

        if not intent:
            if "faculty" in q or "staff" in q or "teaching" in q or "professors" in q or "teachers" in q:
                intent = "faculty"
            elif "hod" in q or "head" in q:
                intent = "head_of_department"

        if intent:
            answer = get_cse_aiml_department_response(intent)
            save_chat(data.get("session_id"), user_query, answer)
            return jsonify({"answer": answer})


    # 🔹 AIML – Standalone
    if any(k in q for k in AIML_KEYWORDS):
        intent = None
        score = 0.0

        intent, score = detect_aiml_intent(q)

        if not intent:
            if "faculty" in q or "staff" in q or "teaching" in q or "professors" in q or "teachers" in q:
                intent = "faculty"
            elif "hod" in q or "head" in q:
                intent = "head_of_department"

        if intent:
            answer = get_aiml_department_response(intent)
            save_chat(data.get("session_id"), user_query, answer)
            return jsonify({"answer": answer})

    # 🔹 CAD – CSE AIDS
    if any(k in q for k in CAD_KEYWORDS):
        intent = None
        score = 0.0

        intent, score = detect_cad_intent(q)

        if not intent:
            if "faculty" in q or "staff" in q or "teaching" in q or "professors" in q or "teachers" in q:
                intent = "faculty"
            elif "cad hod" in q:
                intent = "head_of_department"

        if intent:
            answer = get_cad_department_response(intent)
            save_chat(data.get("session_id"), user_query, answer)
            return jsonify({"answer": answer})


    # 🔹 CIVIL
    if any(k in q for k in CE_KEYWORDS):
        intent = None
        score = 0.0

        intent, score = detect_civil_intent(q)

        if not intent:
            if "faculty" in q or "staff" in q or "teaching" in q or "professors" in q or "teachers" in q:
                intent = "faculty"
            elif "hod" in q or "head" in q:
                intent = "head_of_department"

        if intent:
            answer = get_civil_department_response(intent)
            save_chat(data.get("session_id"), user_query, answer)
            return jsonify({"answer": answer})

    # 🔹 CSE CORE (LAST)
    if any(k in q for k in CSE_KEYWORDS):
        intent = None
        score = 0.0

        intent, score = detect_cse_intent(q)

        if not intent:
            if "faculty" in q or "staff" in q or "teaching" in q or "professors" in q or "teachers" in q:
                intent = "faculty"
            elif "hod" in q or "head" in q:
                intent = "head_of_department"

        if intent:
            answer = get_cse_department_response(intent)
            save_chat(data.get("session_id"), user_query, answer)
            return jsonify({"answer": answer})

            

    if any(k in q for k in ECE_KEYWORDS):
        intent = None
        score = 0.0

        intent, score = detect_ece_intent(q)

        if not intent:
            if "faculty" in q or "staff" in q or "teaching" in q or "professors" in q or "teachers" in q:
                intent = "faculty"
            elif "hod" in q or "head" in q:
                intent = "head_of_department"
            elif "final year" in q:
                intent = "year_4"

        if intent:
            answer = get_ece_department_response(intent)
            save_chat(data.get("session_id"), user_query, answer)
            return jsonify({"answer": answer})


    if any(k in q for k in EEE_KEYWORDS):
        intent = None
        score = 0.0

        intent, score = detect_eee_intent(q)

        if not intent:
            if "faculty" in q or "staff" in q or "teaching" in q or "professors" in q or "teachers" in q:
                intent = "faculty"
            elif "hod" in q or "head" in q:
                intent = "head_of_department"
            elif "final year" in q:
                intent = "year_4"

        if intent:
            answer = get_eee_department_response(intent)
            save_chat(data.get("session_id"), user_query, answer)
            return jsonify({"answer": answer})


    if any(k in q for k in IT_KEYWORDS):
        intent = None
        score = 0.0

        intent, score = detect_it_intent(q)

        if not intent:
            if "faculty" in q or "staff" in q or "teaching" in q or "professors" in q or "teachers" in q:
                intent = "faculty"
            elif "hod" in q or "head" in q:
                intent = "head_of_department"
            elif "final year" in q:
                intent = "year_4"

        if intent:
            answer = get_it_department_response(intent)
            save_chat(data.get("session_id"), user_query, answer)
            return jsonify({"answer": answer})


    if any(k in q for k in MECH_KEYWORDS):
        intent = None
        score = 0.0

        intent, score = detect_mech_intent(q)

        if not intent:
            if "faculty" in q or "staff" in q or "teaching" in q or "professors" in q or "teachers" in q:
                intent = "faculty"
            elif "hod" in q or "head" in q:
                intent = "head_of_department"
            elif "placement" in q:
                intent = "placements"

        if intent:
            answer = get_mech_department_response(intent)
            save_chat(data.get("session_id"), user_query, answer)
            return jsonify({"answer": answer})




    # ==================================================
    # 3️⃣ PROGRAMS
    # ==================================================
    if any(k in q for k in PROGRAM_KEYWORDS):
        prog_intent = detect_courses_programs_intent(q)
        if prog_intent:
            try:
                answer = get_courses_programs_response(prog_intent)
                save_chat(data.get("session_id"), user_query, answer)
                return jsonify({"answer": answer})
            except Exception:
                return jsonify({"answer": "⚠️ Program data unavailable."})

    # ==================================================
    # 4️⃣ ADMISSIONS
    # ==================================================
    if any(k in q for k in ADMISSION_KEYWORDS):
        adm_intent = detect_admission_intent(q)
        if adm_intent:
            try:
                answer = get_admissions_response(adm_intent)
                save_chat(data.get("session_id"), user_query, answer)
                return jsonify({"answer": answer})
            except Exception:
                return jsonify({"answer": "⚠️ Admission data unavailable."})

    # ==================================================
    # 5️⃣ WEBSITE SEARCH
    # ==================================================
    

    # ==================================================
    # 6️⃣ EVENTS / PLACEMENTS / FDP / RESEARCH
    # ==================================================
    if any(k in q for k in EVENT_KEYWORDS):
        institution_intent = detect_institution_intent(q)
        if institution_intent:
            try:
                answer = get_institution_response(institution_intent)
                save_chat(data.get("session_id"), user_query, answer)
                return jsonify({"answer": answer})
            except Exception:
                return jsonify({
                    "answer": "⚠️ Events information temporarily unavailable."
                })

    # ==================================================
    # 7️⃣ STUDENTS
        # ==================================================
        # ==================================================
    # 7️⃣ STUDENTS
    # ==================================================
    try:
        student_answer = handle_student_query(user_query)
        if student_answer and "I can help you with" not in student_answer:
            save_chat(data.get("session_id"), user_query, student_answer)
            return jsonify({"answer": student_answer})

    except Exception:
        pass

    # ==================================================
    # 🔥 FINAL FALLBACK: LLM (MUST BE AT SAME INDENT LEVEL)
    # ==================================================
    try:
        print("[LLM] fallback triggered:", user_query)
        llm_answer = call_llm(user_query)

        # ✅ SAVE CHAT TO DATABASE
        # ✅ SAVE CHAT TO DATABASE
        if current_user.is_authenticated:
            session_id = data.get("session_id")

            # 🔒 Validate session belongs to current user
            chat_session = ChatSession.query.filter_by(
                id=session_id,
                user_id=current_user.id
            ).first()

            if chat_session:
                new_message = ChatMessage(
                    session_id=chat_session.id,
                    message=user_query,
                    response=llm_answer
                )
                db.session.add(new_message)
                db.session.commit()


        return jsonify({"answer": llm_answer})

    except Exception as e:
        print("LLM ERROR:", e)
        return jsonify({"answer": "Sorry, something went wrong."})


# ================= RUN SERVER =================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=False)


