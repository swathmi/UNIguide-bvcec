import json
import os
from services.response_formatter import format_lines

# ---------------- LOAD JSON DATA ----------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "departments",
    "csm.json"
)

with open(DATA_PATH, "r", encoding="utf-8") as f:
    dept_data = json.load(f)

# ================= MAIN SERVICE FUNCTION =================

def get_cse_aiml_department_response(intent):

    # ---------- DEPARTMENT BASIC ----------
    if intent == "department":
        d = dept_data["department"]
        return format_lines(
            "🏫 CSM / CSE-AIML Department Details",
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

    # ---------- ABOUT ----------
    elif intent == "about_department":
        a = dept_data["about_department"]
        return format_lines(
            "ℹ️ About the Department",
            [a["overview"]] + a["focus_areas"],
            "📖"
        )

    # ---------- VISION & MISSION ----------
    elif intent == "vision_and_mission":
        vm = dept_data["vision_and_mission"]
        return format_lines(
            "🎯 Vision & Mission",
            ["Vision:", vm["vision"], "Mission:"] + vm["mission"],
            "🌟"
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
                f"Phone: {h['phone']}",
                f"Email: {h['email']}"
            ],
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

    # ---------- PEO PO PSO ----------
    elif intent == "peo_po_pso":
        p = dept_data["peo_po_pso"]
        return format_lines(
            "📌 PEOs | POs | PSOs",
            ["PEOs:"] + p["peos"] + ["POs:"] + p["pos"] + ["PSOs:"] + p["psos"],
            "🧭"
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
            f"📘 {intent.replace('_', ' ').upper()} CURRICULUM",
            lines,
            "📖"
        )

    # ---------- COURSE OUTCOMES ----------
    elif intent == "course_outcomes":
        outcomes = dept_data["course_outcomes"]["ai_ml"]
        return format_lines(
            "🎯 Course Outcomes",
            outcomes,
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
        visits = dept_data["activities"]["industrial_visits"]["visits"]
        return format_lines(
            "🏭 Industrial Visits",
            [
                f"{v['company']} – {v['location']} ({v['date']})"
                for v in visits
            ],
            "🚌"
        )

    elif intent == "student_clubs":
        return format_lines(
            "👥 Student Clubs",
            dept_data["activities"]["student_clubs"],
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
        p = dept_data["placements"]
        return format_lines(
            "💼 Placements & Career Options",
            [
                f"Training: {p['training']}",
                "Career Domains:"
            ] + p["career_domains"],
            "🚀"
        )

    # ==================================================
    # 🔥 NEW: WEBSITE SECTIONS (ADDED ONLY) 🔥
    # ==================================================

    elif intent == "research_and_development":
        links = (
    dept_data
    .get("activities", {})
    .get("sections", {})
    .get("research_and_development", {})
    .get("source_pages", [])
)

        return format_lines(
            "🔬 Research & Development",
            links,
            "🧪"
        )

    elif intent == "department_placements":
        links = (
    dept_data
    .get("activities", {})
    .get("sections", {})
    .get("department_placements", {})
    .get("source_pages", [])
)

        return format_lines(
            "📊 Department Placements",
            links,
            "📈"
        )

    elif intent == "gallery":
        links = (
    dept_data
    .get("activities", {})
    .get("sections", {})
    .get("gallery", {})
    .get("source_pages", [])
        )

        
        return format_lines(
            "🖼️ Department Gallery",
            links,
            "📸"
        )

    return "Sorry, I could not find the information you requested."
