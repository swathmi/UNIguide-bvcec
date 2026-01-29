import json
import os
from services.response_formatter import format_lines

# ---------------- LOAD JSON DATA ----------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "departments",
    "aiml.json"
)

with open(DATA_PATH, "r", encoding="utf-8") as f:
    dept_data = json.load(f)

# ================= MAIN SERVICE FUNCTION =================

def get_aiml_department_response(intent):

    # -------- SAFE DATA EXTRACTION --------
    dept = dept_data.get("department", {})
    about = dept_data.get("about_department", {})
    vm = dept_data.get("vision_and_mission", {})
    hod = dept_data.get("head_of_department", {})
    faculty = dept_data.get("faculty", [])
    peo = dept_data.get("peo_po_pso", {})
    academics = dept_data.get("academic_structure", {})
    outcomes = dept_data.get("course_outcomes", {})
    activities = dept_data.get("activities", {})
    placements = dept_data.get("placements", {})

    # ---------- DEPARTMENT BASIC ----------
    if intent == "department":
        return format_lines(
            "🏫 AIML Department Details",
            [
                f"Name: {dept.get('name', 'N/A')}",
                f"Short Name: {dept.get('short_name', 'N/A')}",
                f"College: {dept.get('college', 'N/A')}",
                f"Location: {dept.get('location', 'N/A')}",
                f"Introduced Year: {dept.get('introduced_year', 'N/A')}",
                f"Intake Capacity: {dept.get('intake_capacity', 'N/A')}"
            ],
            "📘"
        )

    # ---------- ABOUT ----------
    elif intent == "about_department":
        lines = [about.get("overview", "Overview not available")]
        lines.extend(about.get("focus_areas", []))
        return format_lines(
            "ℹ️ About the Department",
            lines,
            "📖"
        )

    # ---------- VISION & MISSION ----------
    elif intent == "vision_and_mission":
        lines = ["Vision:", vm.get("vision", "N/A"), "Mission:"]
        lines.extend(vm.get("mission", []))
        return format_lines(
            "🎯 Vision & Mission",
            lines,
            "🌟"
        )

    # ---------- HOD ----------
    elif intent == "head_of_department":
        return format_lines(
            "👨‍🏫 Head of the Department",
            [
                f"Name: {hod.get('name', 'N/A')}",
                f"Designation: {hod.get('designation', 'N/A')}",
                f"Qualification: {hod.get('qualification', 'N/A')}",
                f"Phone: {hod.get('phone', 'N/A')}",
                f"Email: {hod.get('email', 'N/A')}"
            ],
            "🎓"
        )

    # ---------- FACULTY ----------
    elif intent == "faculty":
        faculty_lines = [
            f"{f.get('name')} – {f.get('designation')} ({f.get('qualification')})"
            for f in faculty
        ]
        return format_lines(
            "👩‍🏫 Faculty Members",
            faculty_lines if faculty_lines else ["Faculty details not available"],
            "📚"
        )

    # ---------- PEO | PO | PSO ----------
    elif intent == "peo_po_pso":
        lines = ["PEOs:"]
        lines.extend(peo.get("peos", []))
        lines.append("POs:")
        lines.extend(peo.get("pos", []))
        lines.append("PSOs:")
        lines.extend(peo.get("psos", []))
        return format_lines(
            "📌 PEOs | POs | PSOs",
            lines,
            "🧭"
        )

    # ---------- ACADEMIC STRUCTURE ----------
    elif intent == "academic_structure":
        return format_lines(
            "📚 Academic Structure",
            list(academics.keys()),
            "🗂️"
        )

    # ---------- YEAR-WISE SUBJECTS & LABS ----------
    elif intent in ["year_1", "year_2", "year_3", "year_4"]:
        year_data = academics.get(intent, {})
        lines = []

        for sem, info in year_data.items():
            lines.append(f"{sem.upper()} SUBJECTS:")
            lines.extend(info.get("subjects", []))
            lines.append(f"{sem.upper()} LABS:")
            lines.extend(info.get("labs", []))

        return format_lines(
            f"📘 {intent.replace('_', ' ').upper()} CURRICULUM",
            lines if lines else ["Academic data not available"],
            "📖"
        )

    # ---------- COURSE OUTCOMES ----------
    elif intent == "course_outcomes":
        ai_ml_outcomes = outcomes.get("ai_ml", [])
        return format_lines(
            "🎯 Course Outcomes",
            ai_ml_outcomes if ai_ml_outcomes else ["Outcomes not available"],
            "✅"
        )

    # ---------- ACTIVITIES ----------
    elif intent == "activities":
        return format_lines(
            "🏃 Department Activities",
            [
                "Industrial Visits",
                "Student Clubs",
                "Workshops & Seminars"
            ],
            "🎉"
        )

    elif intent == "industrial_visits":
        visits = activities.get("industrial_visits", {}).get("visits", [])
        visit_lines = [
            f"{v.get('company')} – {v.get('location')} ({v.get('date')})"
            for v in visits
        ]
        return format_lines(
            "🏭 Industrial Visits",
            visit_lines if visit_lines else ["No industrial visits available"],
            "🚌"
        )

    elif intent == "student_clubs":
        return format_lines(
            "👥 Student Clubs",
            activities.get("student_clubs", []),
            "🤝"
        )

    elif intent == "workshops_and_seminars":
        return format_lines(
            "🧑‍💻 Workshops & Seminars",
            ["Conducted regularly by the department"],
            "🛠️"
        )

    # ---------- PLACEMENTS ----------
    elif intent == "placements":
        lines = [f"Training: {placements.get('training', 'N/A')}", "Career Domains:"]
        lines.extend(placements.get("career_domains", []))
        return format_lines(
            "💼 Placements & Career Options",
            lines,
            "🚀"
        )

    # ---------- FALLBACK ----------
    return "Sorry, I could not find the information you requested."
