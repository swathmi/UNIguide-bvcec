import json
import os
from services.response_formatter import format_lines

# ---------------- LOAD JSON DATA ----------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "departments",
    "cse.json"
)

with open(DATA_PATH, "r", encoding="utf-8") as f:
    dept_data = json.load(f)

# ================= MAIN SERVICE FUNCTION =================

def get_cse_department_response(intent):

    dept = dept_data.get("department", {})
    vm = dept_data.get("vision_mission", {})
    hod = dept_data.get("head_of_department", {})
    faculty = dept_data.get("faculty", [])
    academics = dept_data.get("academic_structure", {})
    visits = dept_data.get("industrial_visits", [])
    sections = dept_data.get("sections", {})   # ✅ NEW (mech style)

    # ---------- DEPARTMENT ----------
    if intent == "department":
        return format_lines(
            "🏫 CSE Department Details",
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

    # ---------- VISION & MISSION ----------
    elif intent == "vision_mission":
        lines = ["Vision:", vm.get("vision", "N/A"), "Mission:"]
        lines.extend(vm.get("mission", []))
        return format_lines("🎯 Vision & Mission", lines, "🌟")

    # ---------- HOD ----------
    elif intent == "head_of_department":
        lines = [
            f"Name: {hod.get('name', 'N/A')}",
            f"Designation: {hod.get('designation', 'N/A')}",
            f"Qualification: {hod.get('qualification', 'N/A')}",
            f"Experience: {hod.get('experience', 'N/A')}",
            "Research Interests:"
        ]
        lines.extend(hod.get("research_interests", []))
        return format_lines("👨‍🏫 Head of the Department", lines, "🎓")

    # ---------- FACULTY ----------
    elif intent == "faculty":
        faculty_lines = [
            f"{f.get('name')} – {f.get('designation')} ({f.get('qualification')})"
            for f in faculty
        ]
        return format_lines("👩‍🏫 Faculty Members", faculty_lines, "📚")

    # ---------- ACADEMIC STRUCTURE ----------
    elif intent == "academic_structure":
        return format_lines(
            "📚 Academic Structure",
            list(academics.keys()),
            "🗂️"
        )

    # ---------- YEAR-WISE ----------
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
            lines,
            "📖"
        )

    # ---------- INDUSTRIAL VISITS ----------
    elif intent == "industrial_visits":
        visit_lines = [
            f"{v.get('company')} – {v.get('location')} ({v.get('date')})"
            for v in visits
        ]
        return format_lines("🏭 Industrial Visits", visit_lines, "🚌")

    # ================= MECH-STYLE SECTIONS =================

    elif intent == "research_and_development":
        return format_lines(
            "🔬 Research & Development",
            ["Research activities and funded projects conducted by the department."],
            "🧪"
        )

    elif intent == "professional_societies":
        return format_lines(
            "🤝 Professional Societies & Activities",
            ["Professional body activities and technical events conducted regularly."],
            "🏛️"
        )

    elif intent == "newsletters":
        return format_lines(
            "📰 Newsletters",
            ["Department newsletters and publications."],
            "📄"
        )

    elif intent == "nba_e_sar":
        return format_lines(
            "📑 NBA E-SAR",
            ["NBA Self-Assessment Reports and accreditation documents."],
            "📘"
        )

    elif intent == "magazines":
        return format_lines(
            "📚 Magazines",
            ["Technical magazines published by the department."],
            "📰"
        )

    elif intent == "industry_interaction":
        return format_lines(
            "🏭 Industry Institution Interaction",
            ["MoUs, expert talks, and industry collaborations."],
            "🔗"
        )

    elif intent == "gallery":
        return format_lines(
            "🖼️ Gallery",
            ["Department event photos and activity gallery."],
            "📸"
        )

    elif intent == "entrepreneurship":
        return format_lines(
            "🚀 Entrepreneurship & Higher Studies",
            ["Guidance for startups, higher education, and career growth."],
            "💡"
        )

    elif intent == "distinguished_alumni":
        return format_lines(
            "🌟 Distinguished Alumni",
            ["Notable alumni and their achievements."],
            "🎖️"
        )

    elif intent == "placements":
        return format_lines(
            "💼 Department Placements",
            ["Placement training, recruiters, and student achievements."],
            "📈"
        )

    elif intent == "academic_audit":
        return format_lines(
            "📝 Academic Audit",
            ["Academic audit reports and quality assurance records."],
            "✔️"
        )

    elif intent == "old_question_papers":
        return format_lines(
            "📂 Old Question Papers",
            ["Previous year question papers for reference."],
            "🗃️"
        )

    # ---------- FALLBACK ----------
    return "Sorry, I could not find the information you requested."
