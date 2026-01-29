from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# ================= STUDENTS SERVICE =================
from services.students_service import handle_student_query

# ================= INTENT DETECTORS =================
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
from services.rag_service import get_rag_answer
from services.media_service import get_media_response

# ================= DEPARTMENTS =================
# 🔹 CSM (CSE – AIML)
from services.csm_intents import detect_cse_aiml_intent
from services.csm_services import get_cse_aiml_department_response

# 🔹 AIML (Standalone)
from services.aiml_intents import detect_aiml_intent
from services.aiml_services import get_aiml_department_response

# 🔹 CAD (CSE – AIDS)
from services.cad_intents import detect_cad_intent
from services.cad_services import get_cad_department_response

# 🔹 CIVIL
from services.civil_intents import detect_civil_intent
from services.civil_services import get_civil_department_response

# 🔹 CSE CORE
from services.cse_intents import detect_cse_intent
from services.cse_services import get_cse_department_response
# 🔹 ECE
from services.ece_intents import detect_ece_intent
from services.ece_services import get_ece_department_response
# 🔹 EEE
from services.eee_intents import detect_eee_intent
from services.eee_services import get_eee_department_response
# 🔹 IT
from services.it_intents import detect_it_intent
from services.it_services import get_it_department_response
# 🔹 MECH
from services.mech_intents import detect_mech_intent
from services.mech_services import get_mech_department_response




# ================= WEBSITE SEARCH =================

# ================= FLASK APP =================
app = Flask(__name__)
CORS(app)

# ================= DOMAIN KEYWORDS =================
PROGRAM_KEYWORDS = [
    "course", "courses", "program", "programs",
    "ug", "pg", "btech", "mtech",
    "intake", "seats", "capacity",
    "fees", "fee", "package", "salary", "lpa",
    "eligibility", "internship", "placement",
    "syllabus", "curriculum"
]

EVENT_KEYWORDS = [
    "event", "events", "activities",
    "technical activities", "cultural activities", "sports",
    "workshop & seminars",  "guest lecture",
    "hackathon", "symposium",
    "club", "nss", "ncc",
    "career", "alumni","faculty development programs","faculty paper publications",
    "recent activities","latest updates",
    "news", "updates", "recent",
    "poster", "gallery"
]

ADMISSION_KEYWORDS = [
    "admission", "apply", "join",
    "eamcet", "ecet", "management quota",
    "lateral entry", "documents",
    "counseling", "seat allotment",
    "reservation"
]

# ================= DEPARTMENT KEYWORDS =================
CSM_KEYWORDS  = ["csm", "cse aiml"]
AIML_KEYWORDS = ["aiml", "artificial intelligence"]
CAD_KEYWORDS  = ["cad", "aids", "cse aids"]
CE_KEYWORDS   = ["civil", "ce", "civil engineering"]
CSE_KEYWORDS  = ["cse", "computer science"]
ECE_KEYWORDS = ["ece", "electronics", "electronics and communication"]
EEE_KEYWORDS = ["eee", "electrical", "electrical and electronics"]
IT_KEYWORDS = ["it", "information technology"]
MECH_KEYWORDS = ["mech", "mechanical"]

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

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

# ================= CHAT ROUTE =================
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_query = data.get("query", "").strip()

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
            return jsonify({"answer": get_college_overview_response(overview_intent)})
        except Exception:
            return jsonify({"answer": "⚠️ College information temporarily unavailable."})

    # ==================================================
    # 2️⃣ DEPARTMENTS
    # ==================================================

    # 🔹 CSM – CSE AIML
    if any(k in q for k in CSM_KEYWORDS):
        intent = None
        score = 0.0

        intent, score = detect_cse_aiml_intent(q)

        if not intent:
            if " csm faculty" in q or "staff" in q or "teaching" in q:
                intent = "faculty"
            elif "csm hod" in q:
                intent = "head_of_department"

        if intent:
            return jsonify({
                "answer": get_cse_aiml_department_response(intent)
            })


    # 🔹 AIML – Standalone
    if any(k in q for k in AIML_KEYWORDS):
        intent = None
        score = 0.0

        intent, score = detect_aiml_intent(q)

    if not intent:
        if "aiml faculty" in q or "staff" in q or "teaching" in q:
            intent = "faculty"
        elif "aiml hod" in q:
            intent = "head_of_department"

    if intent:
        return jsonify({
            "answer": get_aiml_department_response(intent)
        })

    # 🔹 CAD – CSE AIDS
    if any(k in q for k in CAD_KEYWORDS):
        intent = None
        score = 0.0

        intent, score = detect_cad_intent(q)

    if not intent:
        if "cad faculty" in q or "staff" in q or "teaching" in q:
            intent = "faculty"
        elif "cad hod" in q:
            intent = "head_of_department"

    if intent:
        return jsonify({
            "answer": get_aiml_department_response(intent)
        })

    # 🔹 CIVIL
    if any(k in q for k in CE_KEYWORDS):
        intent = None
        score = 0.0

        intent, score = detect_civil_intent(q)

    if not intent:
        if " civil faculty" in q or "staff" in q or "teaching" in q:
            intent = "faculty"
        elif "civil hod" in q:
            intent = "head_of_department"

    if intent:
        return jsonify({
            "answer": get_civil_department_response(intent)
        })

    # 🔹 CSE CORE (LAST)
    if any(k in q for k in CSE_KEYWORDS):
        intent = None
        score = 0.0

        intent, score = detect_cse_intent(q)

    if not intent:
        if " cse faculty" in q or "staff" in q or "teaching" in q:
            intent = "faculty"
        elif "cse hod" in q:
            intent = "head_of_department"

    if intent:
        return jsonify({
            "answer": get_cse_department_response(intent)
        })
    if any(k in q for k in ECE_KEYWORDS):
        intent = None
        score = 0.0

        intent, score = detect_ece_intent(q)

    if not intent:
        if " ece faculty" in q or "staff" in q or "teaching" in q:
            intent = "faculty"
        elif " ece hod" in q:
            intent = "head_of_department"
        elif "final year" in q:
            intent = "year_4"

    if intent:
        return jsonify({
            "answer": get_ece_department_response(intent)
        })
    if any(k in q for k in EEE_KEYWORDS):
        intent = None
        score = 0.0

        intent, score = detect_eee_intent(q)

    if not intent:
        if " eee faculty" in q or "staff" in q or "teaching" in q:
            intent = "faculty"
        elif " eee hod" in q:
            intent = "head_of_department"
        elif "final year" in q:
            intent = "year_4"

    if intent:
        return jsonify({
            "answer": get_eee_department_response(intent)
        })
    if any(k in q for k in IT_KEYWORDS):
        intent = None
        score = 0.0

        intent, score = detect_it_intent(q)

    if not intent:
        if " it faculty" in q or "staff" in q or "teaching" in q:
            intent = "faculty"
        elif " it hod" in q:
            intent = "head_of_department"
        elif "final year" in q:
            intent = "year_4"

    if intent:
        return jsonify({
            "answer": get_it_department_response(intent)
        })
    if any(k in q for k in MECH_KEYWORDS):
        intent = None
        score = 0.0

        intent, score = detect_mech_intent(q)

    if not intent:
        if " mech faculty" in q or "staff" in q:
            intent = "faculty"
        elif "mech hod" in q:
            intent = "head_of_department"
        elif "placement" in q:
            intent = "placements"

    if intent:
        return jsonify({
            "answer": get_mech_department_response(intent)
        })



    # ==================================================
    # 3️⃣ PROGRAMS
    # ==================================================
    if any(k in q for k in PROGRAM_KEYWORDS):
        prog_intent = detect_courses_programs_intent(q)
        if prog_intent:
            try:
                return jsonify({"answer": get_courses_programs_response(prog_intent)})
            except Exception:
                return jsonify({"answer": "⚠️ Program data unavailable."})

    # ==================================================
    # 4️⃣ ADMISSIONS
    # ==================================================
    if any(k in q for k in ADMISSION_KEYWORDS):
        adm_intent = detect_admission_intent(q)
        if adm_intent:
            try:
                return jsonify({"answer": get_admissions_response(adm_intent)})
            except Exception:
                return jsonify({"answer": "⚠️ Admission data unavailable."})

    # ==================================================
    # 5️⃣ WEBSITE SEARCH
    # ==================================================
    

    # ==================================================
    # 6️⃣ EVENTS
    # ==================================================
        # ==================================================
    # 6️⃣ EVENTS / PLACEMENTS / FDP / RESEARCH
    # ==================================================
    if any(k in q for k in EVENT_KEYWORDS):
        institution_intent = detect_institution_intent(q)
        if institution_intent:
            try:
                return jsonify({
                    "answer": get_institution_response(institution_intent)
                })
            except Exception:
                return jsonify({
                    "answer": "⚠️ Events information temporarily unavailable."
                })

    # ==================================================
    # 7️⃣ STUDENTS
    # ==================================================
    try:
        student_answer = handle_student_query(user_query)
        if student_answer is not None:
            return jsonify({"answer": student_answer})
    except Exception:
        pass
    

    # ==================================================
    # FINAL FALLBACK
    # ==================================================
    return jsonify({
        "answer": (
            "🤖 I can help you with:\n\n"
            "👨‍🎓 Student Details\n"
            "🎓 Courses & Programs\n"
            "🏫 Department Information\n"
            "🎉 Events & Activities\n"
            "📝 Admissions\n\n"
            "👉 Please ask clearly."
        )
    })

# ================= RUN SERVER =================
if __name__ == "__main__":
    app.run(debug=True)
