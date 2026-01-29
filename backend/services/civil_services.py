import json
import os
from services.response_formatter import format_lines

# ---------------- LOAD JSON DATA ----------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "departments",
    "civil.json"
)

with open(DATA_PATH, "r", encoding="utf-8") as f:
    dept_data = json.load(f)

# ================= MAIN SERVICE FUNCTION =================

def get_civil_department_response(intent):

    dept = dept_data.get("department", {})
    hod = dept_data.get("head_of_department", {})
    faculty = dept_data.get("faculty", [])
    vm = dept_data.get("vision_and_mission", {})
    academics = dept_data.get("academic_structure", {})
    syllabus = dept_data.get("syllabus", {})
    activities = dept_data.get("department_activities", [])

    # ---------- DEPARTMENT BASIC ----------
    if intent == "department":
        return format_lines(
            "🏗️ Civil Engineering Department",
            [
                f"Name: {dept.get('name', 'N/A')}",
                f"Short Name: {dept.get('short_name', 'N/A')}",
                f"College: {dept.get('college', 'N/A')}",
                f"Location: {dept.get('location', 'N/A')}",
                f"Program Level: {dept.get('program_level', 'N/A')}",
                f"Branch Code: {dept.get('branch_code', 'N/A')}"
            ],
            "🏫"
        )

    # ---------- HOD ----------
    elif intent == "head_of_department":
        return format_lines(
            "👨‍🏫 Head of the Department",
            [
                f"Name: {hod.get('name', 'N/A')}",
                f"Designation: {hod.get('designation', 'N/A')}",
                f"Qualification: {hod.get('qualification', 'N/A')}",
                f"Profile: {hod.get('profile_url', 'N/A')}"
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
            faculty_lines if faculty_lines else ["Faculty data not available"],
            "📚"
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
            lines if lines else ["Academic data not available"],
            "📖"
        )

    # ---------- SYLLABUS ----------
    elif intent == "syllabus":
        regs = syllabus.get("regulations", [])
        lines = [
            f"{r.get('regulation')} – {r.get('program')} ({r.get('syllabus_link')})"
            for r in regs
        ]
        return format_lines(
            "📄 Syllabus & Regulations",
            lines if lines else ["Syllabus information not available"],
            "🔗"
        )

    # ---------- ACTIVITIES ----------
    elif intent == "department_activities":
        return format_lines(
            "🏃 Department Activities",
            activities if activities else ["Activities not available"],
            "🎉"
        )

    # ---------- FALLBACK ----------
    return "Sorry, I could not find the information you requested."
