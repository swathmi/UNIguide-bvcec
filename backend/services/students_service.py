import pandas as pd
import re

# ================= LOAD EXCEL =================
DATA_PATH = "data/students.xlsx"
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
EXCLUDED_KEYWORDS = [
    "syllabus","curriculum","regulation","r20","r23","pdf","download",
    "counseling","admission","apply","process",
    "eamcet","ecet","management","quota",
    "eligibility","seat","allotment",
    "placement","placed","company","package","lpa",
    "event","events","poster","image","photo","gallery",
    "update","news","recent","achievers","day",
    "principal","hod","faculty","department",
    "college","aicte","naac"
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
    reg = re.search(r"\b\d{5}[A-Z]\d{4}\b", text)
    if reg:
        return {"type": "REG_NO", "value": reg.group()}

    for name in df["NAME"].dropna().unique():
        if name.upper() in text:
            return {"type": "NAME", "value": name}

    # fuzzy name (single word)
    for name in df["NAME"].dropna().unique():
        for part in name.upper().split():
            if part in text:
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

    for branch in ["CSM","CSE","AIML","CAD","CE","CIVIL"]:
        if branch in text:
            cond["BRANCH"] = branch

    return cond

# ================= FORMAT =================
def format_student(s):
    lines = []
    for col in df.columns:
        lines.append(f"{col.replace('_',' ').title()}: {s[col]}")
    return "\n".join(lines)

# ================= MASTER =================
def handle_student_query(query):
    q = query.lower()

    # 🚫 block non-student domains
    if any(word in q for word in EXCLUDED_KEYWORDS):
        return None

    text = clean(query)
    data = df.copy()

    who = detect_who(text)
    cond = detect_conditions(text)

    # ================= FILTER =================
    if who:
        if who["type"] == "REG_NO":
            data = data[data["REG_NO"] == who["value"]]
        elif who["type"] == "NAME":
            data = data[data["NAME"] == who["value"]]

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
        names = "\n".join([f"• {n}" for n in data["NAME"].head(5)])
        return f"📋 Students Found: {len(data)}\n{names}"

    # ================= FULL PROFILE =================
    return format_student(data.iloc[0]) 