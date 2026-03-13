import pandas as pd
import re

import os

# ================= LOAD EXCEL =================
# Use absolute path relative to this file
current_dir = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(os.path.dirname(current_dir), "data", "students.xlsx")
df = pd.read_excel(DATA_PATH)

# ================= FIELD ALIASES =================
FIELD_ALIASES = {
    "REG_NO": ["REG NO", "REGD NO", "ROLL NO", "HTNO", "HALL TICKET"],

    "NAME": ["NAME", "STUDENT NAME"],

    "BRANCH": ["BRANCH", "DEPARTMENT"],

    "STUDENT_PHONE": [
        "STUDENT PHONE", "STUDENT NUMBER", "MOBILE", "PHONE"
    ],

    "PARENT_PHONE": [
        "PARENT PHONE", "PARENT NUMBER"
    ],

    "PERSONAL_EMAIL": [
        "PERSONAL EMAIL", "MAIL ID", "EMAIL"
    ],

    "DOMAIN_EMAIL": [
        "DOMAIN EMAIL", "COLLEGE MAIL", "OFFICIAL MAIL"
    ],

    "SSC": [
        "SSC", "10TH", "10TH MARKS", "TENTH"
    ],

    "INTER": [
        "INTER", "12TH", "INTER MARKS", "DIPLOMA"
    ],

    "BTECH": [
        "BTECH", "CGPA", "BTECH %", "AGGREGATE"
    ],

    "BACKLOGS": [
        "BACKLOG", "BACKLOGS", "ARREARS"
    ]
}


# ================= HARD BLOCK DOMAINS =================
# Only block specific non-student queries
EXCLUDED_KEYWORDS = [
    "syllabus", "curriculum", "regulation", "r20", "r23", "pdf download",
    "counseling", "admission process", "apply",
    "eamcet", "ecet", "quota", "eligibility", "seat allotment",
    "faculty", "professor", "teacher", "hod", "staff", "department head", "head of", "associate professor", "assistant professor"
]

# ================= COLUMN RENAME =================
COLUMN_RENAME_MAP = {
    "REGD NO": "REG_NO",
    "STDNT PH.NO": "STUDENT_PHONE",
    "PARENT PH.NO": "PARENT_PHONE",
    "PERSONAL MAIL ID": "PERSONAL_EMAIL",
    "DOMAIN MAIL-ID": "DOMAIN_EMAIL",
    "SSC %": "SSC",
    "INTER/DIPLOMA %": "INTER",
    "TOTAL BACKLOGS": "BACKLOGS",
    "B.TECH %": "BTECH"
}

df.rename(columns=COLUMN_RENAME_MAP, inplace=True)
df.columns = df.columns.str.upper()

# ================= UTIL =================
def clean(text):
    return text.upper().strip()

# ================= DETECT WHO =================
def detect_who(text):
    # Strict Reg No search
    reg = re.search(r"\b\d{5}[A-Z]\d{4}\b", text)
    if reg:
        return {"type": "REG_NO", "value": reg.group()}

    # Handle "list of students with name X" pattern
    list_pattern = re.search(r"(?:list|students?).*?(?:with |named? |called )?(\w+)", text, re.IGNORECASE)
    if list_pattern and "LIST" in text.upper():
        search_name = list_pattern.group(1).upper()
        # Find all students with this name part
        matching = df[df["NAME"].str.upper().str.contains(search_name, na=False)]
        if not matching.empty:
            return {"type": "NAME_LIST", "value": search_name}
    
    # Strict name part matching - only if word exactly matches a name part
    words = set(text.upper().split())
    # Remove common generic words from name matching
    generic_words = {"ANY", "THE", "AND", "WHO", "CAN", "LIST", "SHOW", "STUDENT", "RECORDS", "TELL", "DETAILS", "INFO", "IS"}
    words = words - generic_words
    
    for name in df["NAME"].dropna().unique():
        name_parts = set(name.upper().split())
        for part in name_parts:
            if len(part) > 2 and part in words:
                 return {"type": "NAME", "value": name}

    return None

# ================= DETECT CONDITIONS =================
def detect_conditions(text):
    cond = {}

    if "NO BACKLOG" in text or "ZERO BACKLOG" in text:
        cond["BACKLOGS_EQ"] = 0

    m = re.search(r"ABOVE\s+(\d+)", text)
    if m:
        cond["BTECH_GT"] = int(m.group(1))

    # Strict branch matching
    for branch in ["CSM","CSE","AIML","CAD","CE","CIVIL","ECE","EEE","IT","MECH"]:
        if re.search(rf"\b{branch}\b", text):
            cond["BRANCH"] = branch

    return cond

# ================= FORMAT =================
def format_student(s):
    lines = []
    for col in df.columns:
        if str(s[col]).lower() != "nan":
            lines.append(f"{col.replace('_',' ').title()}: {s[col]}")
    return "\n".join(lines)

# ================= MASTER =================
def handle_student_query(query):
    q = query.lower()

    # 🚫 block non-student domains
    if any(word in q for word in EXCLUDED_KEYWORDS):
        return None
    
    # 🚫 Block "who is [name]" when it's likely a faculty query
    # Faculty queries often ask "who is [name]" while student queries ask for name or reg no
    if q.startswith("who is "):
        name_part = q[7:].strip()
        if len(name_part) > 2:
            # Check if this looks like a faculty query (single name or full formal name)
            # Faculty names typically have titles or are formal
            # Student queries are more direct like "ravi" or with context "ravi from cse"
            word_count = len(name_part.split())
            if word_count == 1 and any(title in q for title in ["professor", "prof", "dr", "dr."]):
                return None
            # If it's just "who is [name]" with no other context, likely faculty query
            if word_count == 1 and not any(keyword in q for keyword in ["cse", "civil", "ece", "eee", "mech", "it", "branch", "semester"]):
                return None

    text = clean(query)
    
    who = detect_who(text)
    cond = detect_conditions(text)

    # If no identifying information or conditions, return None to let other services handle it
    if not who and not cond:
        return None

    data = df.copy()

    # ================= FILTER =================
    if who:
        if who["type"] == "REG_NO":
            data = data[data["REG_NO"] == who["value"]]
        elif who["type"] == "NAME":
            data = data[data["NAME"].str.upper() == who["value"].upper()]
        elif who["type"] == "NAME_LIST":
            # Filter by partial name match
            data = data[data["NAME"].str.upper().str.contains(who["value"], na=False)]

    if "BRANCH" in cond and "BRANCH" in data.columns:
        data = data[data["BRANCH"] == cond["BRANCH"]]

    if "BACKLOGS_EQ" in cond:
        data = data[data["BACKLOGS"] == cond["BACKLOGS_EQ"]]

    if "BTECH_GT" in cond:
        data = data[data["BTECH"] > cond["BTECH_GT"]]

    if data.empty:
        return "❌ Student record not found. Please check details."

    # ================= EMAIL =================
    if "mail" in q or "email" in q:
        s = data.iloc[0]
        return (
            f"📧 Personal Email: {s.get('PERSONAL_EMAIL','N/A')}\n"
            f"📧 Domain Email: {s.get('DOMAIN_EMAIL','N/A')}"
        )

    # ================= PHONE =================
    if "student phone" in q or "student number" in q:
        return f"📞 Student Phone: {data.iloc[0]['STUDENT_PHONE']}"

    if "parent phone" in q or "parent number" in q:
        return f"📞 Parent Phone: {data.iloc[0]['PARENT_PHONE']}"

    # ================= COUNT =================
    if "HOW MANY" in text or "COUNT" in text:
        return f"📊 Count: {len(data)}"

    # ================= TOPPER =================
    if "TOPPER" in text or "HIGHEST" in text:
        top = data.sort_values("BTECH", ascending=False).iloc[0]
        return f"🏆 Topper: {top['NAME']} ({top['BTECH']}%)"

    # ================= FIELD =================
    # ================= FIELD (ALIASES) =================
    for field, aliases in FIELD_ALIASES.items():
        for a in aliases:
            if a in text and field in data.columns:
                return f"{field.replace('_',' ').title()}: {data.iloc[0][field]}"


    # ================= MULTI LIST =================
    if len(data) > 1:
        names = "\n".join([f"• {n}" for n in data["NAME"]])
        return (
            f"📋 Students Found: {len(data)}\n{names}\n\n"
            "Please specify the full name for detailed information."
        )

    # ================= FULL PROFILE =================
    if len(data) == 1:
        return format_student(data.iloc[0])
    # ================= NOT FOUND =================
    return "❌ Student record not found. Please check details."

# ==================================================
# 🆕 STUDENT SERVICES (Mental Health, Scholarships, etc.)
# ==================================================
def load_student_json(filename: str):
    """Load JSON from student_services directory"""
    try:
        filepath = os.path.join(os.path.dirname(__file__), '../data/student_services', filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            import json
            return json.load(f)
    except Exception as e:
        return {"error": f"Failed to load {filename}: {str(e)}"}

def get_mental_health_support():
    """Provide mental health and wellness support resources"""
    from response_formatter import format_lines
    
    response = []
    response.append("🏥 BVCEC Counselling Centre")
    response.append("- Confidential & free counseling")
    response.append("- Professional counselors available")
    response.append("- Contact: counselling@bvcec.in")
    response.append("")
    response.append("💪 Mental Wellness Programs")
    response.append("- Peer mentoring groups")
    response.append("- Stress management workshops")
    response.append("- Yoga & meditation sessions (Free)")
    response.append("")
    response.append("🆘 Crisis Support")
    response.append("- 24/7 helpline available")
    response.append("- Off-campus: AASRA 9820466726")
    
    return format_lines("Mental Health & Wellness Support", response, "🧠")

def get_academic_help():
    """Provide academic support resources"""
    from response_formatter import format_lines
    
    response = []
    response.append("📖 Tutoring & Coaching")
    response.append("- Faculty office hours (weekdays)")
    response.append("- Peer tutoring program (Free)")
    response.append("- Online tutoring portals")
    response.append("")
    response.append("📊 Academic Improvement")
    response.append("- Remedial classes for weak subjects")
    response.append("- Study material repository")
    response.append("- Past exam papers archive")
    response.append("")
    response.append("🎓 Backlog Clearance")
    response.append("- Special exams (2x per year)")
    response.append("- Subject re-registration allowed")
    response.append("- Contact: academics@bvcec.in")
    
    return format_lines("Academic Help & Support", response, "📚")

def get_hostel_information():
    """Provide hostel facilities and information"""
    from response_formatter import format_lines
    
    response = []
    response.append("🏘️ ACCOMMODATION TYPES")
    response.append("- Single AC/Non-AC | Twin AC/Non-AC")
    response.append("- Study desk + Locker in each room")
    response.append("")
    response.append("🍽️ MESS FACILITIES")
    response.append("- Breakfast: 6:30-7:30 AM")
    response.append("- Lunch: 12:00-1:00 PM | Dinner: 7:00-8:00 PM")
    response.append("- Vegetarian & Non-veg options")
    response.append("- Special dietary needs: Inform committee")
    response.append("")
    response.append("⚙️ FACILITIES")
    response.append("- 24/7 electricity | High-speed WiFi")
    response.append("- Laundry service (₹5/kg)")
    response.append("- Gym | Sports facilities | Basketball court")
    response.append("")
    response.append("📋 HOW TO APPLY")
    response.append("- Form: Hostel office")
    response.append("- Docs: 10th fee receipt + Parent consent")
    response.append("- Confirmation: Deposit ₹5,000 (refundable)")
    response.append("")
    response.append("📞 Hostel Warden: +91-XXXX-XXXX-XX (9 AM-5 PM)")
    response.append("📧 Email: hostel@bvcec.in")
    
    return format_lines("Hostel Guide & Accommodation", response, "🏨")

def get_scholarships_financial_aid():
    """Provide scholarship and financial aid information"""
    from response_formatter import format_lines
    
    response = []
    response.append("🏆 MERIT-BASED SCHOLARSHIPS")
    response.append("- AICTE Prime Fellowship: ₹2 LPA (auto-allocated)")
    response.append("- BVCEC Merit Awards: ₹5,000-₹20,000/sem")
    response.append("")
    response.append("💳 NEED-BASED SCHOLARSHIPS")
    response.append("- SC/ST/OBC: 50-100% tuition waiver")
    response.append("- EWS Scheme: Partial fee waiver")
    response.append("- Income limit: Check eligibility (family income caps)")
    response.append("")
    response.append("👩‍🎓 WOMEN IN STEM")
    response.append("- ₹10,000/year scholarship")
    response.append("- Eligibility: Female + CGPA ≥ 7.0")
    response.append("")
    response.append("📚 EDUCATION LOANS")
    response.append("- SBI/HDFC/ICICI: 7.5-11.5% interest")
    response.append("- Tenure: 5-7 years after graduation")
    response.append("- Government loans: 6-9% p.a. with subsidy")
    response.append("")
    response.append("📧 Apply: scholar_office@bvcec.edu.in")
    response.append("📍 Room 105, Admin Block | Mon-Fri 10 AM-4 PM")
    
    return format_lines("Scholarships & Financial Aid", response, "💰")

def get_internship_opportunities():
    """Provide internship and career guidance"""
    from response_formatter import format_lines
    
    response = []
    response.append("⏰ INTERNSHIP TIMELINE")
    response.append("- Sem 3-4: Build portfolio & attend talks")
    response.append("- Sem 5: Summer internship (8-12 weeks)")
    response.append("- Sem 6: Post-summer prep & pre-placements")
    response.append("- Sem 7: Final year internship / FTE offers")
    response.append("")
    response.append("🎯 INTERVIEW PREP")
    response.append("- Coding: LeetCode, HackerRank (200+ problems)")
    response.append("- System Design: Study key concepts & mini-projects")
    response.append("- Soft Skills: HR rounds, group discussions")
    response.append("")
    response.append("💡 TOP COMPANIES (Varies by department)")
    response.append("- CSE: Amazon, Microsoft, Google, Goldman Sachs")
    response.append("- AIML: Google AI, Microsoft Azure, JP Morgan")
    response.append("- ECE: TI, Qualcomm, AMD, Bosch")
    response.append("- MECH: Hero MotoCorp, Mahindra, Bosch, Cummins")
    response.append("")
    response.append("💬 Speak to: Placement Cell | placement@bvcec.in")
    
    return format_lines("Internship & Career Opportunities", response, "💼")

def get_exam_countdown():
    """Get exam schedule and countdown"""
    from response_formatter import format_lines
    
    response = []
    response.append("⏳ SEMESTER FINAL EXAMS")
    response.append("📅 Schedule: Nov 20-30 (25 days remaining)")
    response.append("")
    response.append("📝 EXAM STRUCTURE (By Department)")
    response.append("- CSE: 6 papers | AIML: 5 papers + projects")
    response.append("- ECE: 5 papers + lab viva | MECH: 5 papers + design viva")
    response.append("- CIVIL: 5 papers + project viva | IT: 6 papers + lab")
    response.append("")
    response.append("⏱️ SMART TIME MANAGEMENT")
    response.append("- Allocate % to subjects based on difficulty")
    response.append("- Complete assignments & past papers now")
    response.append("- Revision: Focus on formulas & key concepts")
    response.append("")
    response.append("✅ FINAL WEEK STRATEGY")
    response.append("- Day 1-3: Complete all revision")
    response.append("- Day 4-6: Full mock tests under exam conditions")
    response.append("- Day 7: Light review + sleep well!")
    
    return format_lines("Exam Countdown & Preparation", response, "⏰")

def get_clubs_societies():
    """Get information about clubs and societies"""
    from response_formatter import format_lines
    
    response = []
    response.append("💻 TECHNICAL CLUBS")
    response.append("- Code Crusaders: Competitive programming (Wed 4 PM)")
    response.append("- RoboVision: Robotics & IoT (Thu 5 PM)")
    response.append("- WebWeavers: Full-stack web dev (Mon 3:30 PM)")
    response.append("- DataMorphs: ML & AI (Fri 4 PM)")
    response.append("")
    response.append("🎭 CULTURAL CLUBS")
    response.append("- Dramatix: Theater & acting")
    response.append("- Rhythmica: Music & band (Oct Fest)")
    response.append("- Footloose: Dance (Mon/Wed 6 PM)")
    response.append("- Artistry Hub: Painting & design")
    response.append("")
    response.append("⚽ SPORTS")
    response.append("- Indoor: Basketball, Table Tennis, Badminton, Chess")
    response.append("- Outdoor: Cricket, Football, Kabaddi, Volleyball")
    response.append("- Practice: Mon-Fri 5-7 PM")
    response.append("- Sports Fest: February (all sports)")
    response.append("")
    response.append("🏢 PROFESSIONAL BODIES")
    response.append("- IEEE: Tech talks, certifications (₹300/year)")
    response.append("- ACM: Contests, research (₹500/year)")
    response.append("")
    response.append("✨ Join Multiple Clubs! | Contact: affairs@bvcec.in")
    
    return format_lines("Clubs, Societies & Co-Curricular", response, "🎭")

def get_learning_resources():
    """Provide learning and skill development resources"""
    from response_formatter import format_lines
    
    response = []
    response.append("💻 CODING & DSA")
    response.append("- LeetCode: DSA + system design practice")
    response.append("- HackerRank: Language practice & contests")
    response.append("- CodeChef: Competitive programming")
    response.append("- GeeksforGeeks: Interview prep by topic")
    response.append("")
    response.append("📊 DATA SCIENCE & ML")
    response.append("- Coursera: Andrew Ng ML Specialization")
    response.append("- Kaggle: Datasets + competitions")
    response.append("- DataCamp: SQL, Python, Statistics")
    response.append("")
    response.append("🎨 WEB & DESIGN")
    response.append("- Frontend Masters: Advanced web design")
    response.append("- MDN Web Docs: Web standards (Free)")
    response.append("- Figma: UI/UX design tools")
    response.append("")
    response.append("📚 RECOMMENDED BOOKS")
    response.append("- 'Cracking the Coding Interview' - Gayle Laakmann")
    response.append("- 'System Design Interview' - Alex Xu")
    response.append("- 'Clean Code' - Robert Martin")
    response.append("- 'Introduction to Algorithms' (CLRS)")
    response.append("")
    response.append("🧠 RESEARCH & INNOVATION")
    response.append("- Propose ideas to mentors")
    response.append("- BVCEC Research Cell: research@bvcec.in")
    response.append("- Publish papers → Scholarships!")
    
    return format_lines("Learning & Development Resources", response, "📚")

def handle_students_services_query(intent: str, query: str = ""):
    """Route student services queries to appropriate handlers"""
    from response_formatter import format_lines
    
    handlers = {
        "mental_health": get_mental_health_support,
        "academic_help": get_academic_help,
        "hostel_information": get_hostel_information,
        "scholarships_financial_aid": get_scholarships_financial_aid,
        "internship_preparation": get_internship_opportunities,
        "exam_preparation": get_exam_countdown,
        "clubs_and_societies": get_clubs_societies,
        "extra_curricular_resources": get_learning_resources,
        "general_student_services": lambda: format_lines(
            "Student Services Available", 
            [
                "🎓 Mental Health Support",
                "📖 Academic Help",
                "🏨 Hostel Information",
                "💰 Scholarships & Financial Aid",
                "💼 Internship & Career Guidance",
                "⏰ Exam Preparation",
                "🎭 Clubs & Societies",
                "📚 Learning Resources",
                "Please ask for specific details on any of these!"
            ],
            "🎓"
        )
    }
    
    handler = handlers.get(intent, handlers["general_student_services"])
    return handler()