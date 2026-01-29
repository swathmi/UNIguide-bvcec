import json
import os
from services.response_formatter import format_lines

# -------- LOAD JSON --------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "departments",
    "mech.json"
)

with open(DATA_PATH, "r", encoding="utf-8") as f:
    dept_data = json.load(f)

# ================= MAIN SERVICE =================
def get_mech_department_response(intent):

    # ---------- DEPARTMENT ----------
    if intent == "department":
        d = dept_data["department"]
        return format_lines(
            "🏫 Mechanical Engineering Department",
            [
                f"Name: {d['name']}",
                f"Short Name: {d['short_name']}",
                f"College: {d['college']}",
                f"Location: {d['location']}"
            ],
            "📘"
        )

    # ---------- PRINCIPAL ----------
    elif intent == "principal":
        p = dept_data["administration"]["principal"]
        return format_lines(
            "🎓 Principal",
            [
                f"Name: {p['name']}",
                f"Designation: {p['designation']}",
                f"Qualification: {p['qualification']}"
            ],
            "👨‍💼"
        )

    # ---------- HOD ----------
    elif intent == "head_of_department":
        h = dept_data["head_of_department"]
        return format_lines(
            "👨‍🏫 Head of the Department",
            [
                f"Name: {h['name']}",
                f"Designation: {h['designation']}",
                f"Qualification: {h['qualification']}",
                f"Profile: {h['profile_page']}"
            ],
            "🎓"
        )

    # ---------- FACULTY ----------
    elif intent == "faculty":
        lines = [
            f"{f['name']} – {f['designation']} ({f['qualification']})"
            for f in dept_data["faculty"]
        ]
        return format_lines(
            "👩‍🏫 Faculty Members",
            lines,
            "📚"
        )

    # ---------- GENERIC WEBSITE SECTIONS ----------
    SECTION_MAP = {
        "research_and_development": "🔬 Research & Development",
        "professional_societies": "🤝 Professional Societies & Activities",
        "newsletters": "📰 Newsletters",
        "nba_e_sar": "📑 NBA E-SAR",
        "magazines": "📖 Magazines",
        "industry_interaction": "🏭 Industry Institution Interaction",
        "gallery": "🖼️ Gallery",
        "entrepreneurship": "🚀 Entrepreneurship & Higher Studies",
        "distinguished_alumni": "🌟 Distinguished Alumni",
        "placements": "💼 Department Placements",
        "academic_audit": "📊 Academic Audit",
        "old_question_papers": "📝 Old Question Papers"
    }

    if intent in SECTION_MAP:
        section = dept_data["sections"].get(intent, {})
        pages = section.get("source_pages", [])
        return format_lines(
            SECTION_MAP[intent],
            pages if pages else ["Information available on department website"],
            "🔗"
        )

    return "Sorry, I could not find the information you requested."
