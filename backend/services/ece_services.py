import json
import os
from services.response_formatter import format_lines

# ---------------- LOAD JSON DATA ----------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "departments",
    "ece.json"
)

with open(DATA_PATH, "r", encoding="utf-8") as f:
    dept_data = json.load(f)

# ================= MAIN SERVICE FUNCTION =================
def get_ece_department_response(intent):

    # ---------- DEPARTMENT ----------
    if intent == "department":
        d = dept_data["department"]
        return format_lines(
            "🏫 ECE Department Details",
            [
                f"Name: {d['name']}",
                f"Short Name: {d['short_name']}",
                f"College: {d['college']}",
                f"Location: {d['location']}",
                f"Introduced Year: {d['introduced_year']}",
                f"Intake Capacity: {d['intake_capacity']}"
            ],
            "📘"
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
                f"Experience: {h['experience']}",
                "Research Interests:"
            ] + h["research_interests"],
            "🎓"
        )

    # ---------- FACULTY ----------
    elif intent == "faculty":
        faculty_lines = [
            f"{f['name']} – {f['designation']} ({f['qualification']})"
            for f in dept_data["faculty"]
        ]
        return format_lines(
            "👩‍🏫 Faculty Members",
            faculty_lines,
            "📚"
        )

    # ---------- ACADEMIC STRUCTURE ----------
    elif intent == "academic_structure":
        return format_lines(
            "📚 Academic Structure",
            list(dept_data["academic_structure"].keys()),
            "🗂️"
        )

    # ---------- YEAR-WISE ----------
    elif intent in ["year_1", "year_2", "year_3", "year_4"]:
        year_data = dept_data["academic_structure"][intent]
        lines = []
        for sem, info in year_data.items():
            lines.append(f"{sem.upper()} SUBJECTS:")
            lines.extend(info["subjects"])
            lines.append(f"{sem.upper()} LABS:")
            lines.extend(info["labs"])

        return format_lines(
            f"📘 {intent.replace('_',' ').upper()} CURRICULUM",
            lines,
            "📖"
        )

    # ---------- STUDENT PROJECTS ----------
    elif intent == "student_projects":
        return format_lines(
            "🛠️ Student Projects",
            dept_data["student_projects"],
            "🚀"
        )

    # ---------- INFRASTRUCTURE ----------
    elif intent == "infrastructure":
        return format_lines(
            "🏗️ Infrastructure & Labs",
            dept_data["infrastructure"],
            "🏭"
        )

    return "Sorry, I could not find the information you requested."
