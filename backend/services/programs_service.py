import json
import os
from services.response_formatter import format_lines

# ---------------- LOAD JSON DATA ----------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "programs_and_courses.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    courses_data = json.load(f)

# ================= MAIN SERVICE FUNCTION =================

def get_courses_programs_response(intent):

    # ---------- ACADEMIC LEVEL ----------
    if intent == "UG_PROGRAMS":
        return format_lines(
            "🎓 Undergraduate Programs (B.Tech)",
            courses_data["academic_levels"]["undergraduate"]["programs"],
            "📘"
        )

    elif intent == "PG_PROGRAMS":
        return format_lines(
            "🎓 Postgraduate Programs (M.Tech)",
            courses_data["academic_levels"]["postgraduate"]["programs"],
            "📗"
        )

    # ---------- COURSE CODES ----------
    elif intent == "UG_COURSE_CODES":
        codes = courses_data["course_codes"]["ug_codes"]
        return format_lines(
            "🏷️ UG Course Codes",
            [f"{k} : {v}" for k, v in codes.items()],
            "🔢"
        )

    elif intent == "PG_COURSE_CODES":
        codes = courses_data["course_codes"]["pg_codes"]
        return format_lines(
            "🏷️ PG Course Codes",
            [f"{k} : {v}" for k, v in codes.items()],
            "🔢"
        )

    # ---------- ELIGIBILITY ----------
    elif intent == "UG_ELIGIBILITY":
        ug = courses_data["eligibility"]["ug_eligibility"]
        return format_lines(
            "✅ UG Eligibility Criteria",
            [
                f"Qualification: {ug['qualification']}",
                f"Required Subjects: {', '.join(ug['required_subjects'])}",
                f"Minimum Percentage: {ug['minimum_percentage']}",
                f"Entrance Exams: {', '.join(ug['entrance_exams'])}"
            ],
            "📌"
        )

    elif intent == "PG_ELIGIBILITY":
        pg = courses_data["eligibility"]["pg_eligibility"]
        return format_lines(
            "✅ PG Eligibility Criteria",
            [
                f"Qualification: {pg['qualification']}",
                f"Minimum Percentage: {pg['minimum_percentage']}",
                f"Entrance Exams: {', '.join(pg['entrance_exams'])}"
            ],
            "📌"
        )

    elif intent == "LATERAL_ENTRY_ELIGIBILITY":
        le = courses_data["eligibility"]["lateral_entry"]
        return format_lines(
            "🔁 Lateral Entry Eligibility",
            [
                f"Qualification: {le['qualification']}",
                f"Admission Year: {le['admission_year']}",
                f"Entrance Exam: {le['entrance_exam']}"
            ],
            "📌"
        )

    # ---------- FEES ----------
    elif intent == "UG_FEES":
        return format_lines(
            "💰 UG Fee Structure",
            courses_data["fee_structure"]["ug_fees"],
            "💸"
        )

    elif intent == "PG_FEES":
        return format_lines(
            "💰 PG Fee Structure",
            courses_data["fee_structure"]["pg_fees"],
            "💸"
        )

    elif intent == "HOSTEL_FEES":
        return format_lines(
            "🏠 Hostel Fee Details",
            courses_data["fee_structure"]["hostel_fees"],
            "🏡"
        )

    elif intent == "SCHOLARSHIP_DETAILS":
        return format_lines(
            "🎓 Scholarship Details",
            courses_data["fee_structure"]["scholarships"],
            "🎯"
        )

    # ---------- INTAKE ----------
    elif intent == "INTAKE_DETAILS":
        intake = courses_data["intake_capacity"]
        return format_lines(
            "📊 Branch-wise Intake Capacity",
            [f"{k} : {v} seats" for k, v in intake.items()],
            "📌"
        )

    # ---------- TEACHING ----------
    elif intent == "TEACHING_METHODS":
        return format_lines(
            "👨‍🏫 Teaching Methodology",
            courses_data["teaching_methodology"]["methods"],
            "📖"
        )

    # ---------- SYLLABUS ----------
    elif intent == "SYLLABUS_STRUCTURE":
        return format_lines(
            "📚 Syllabus & Curriculum Structure",
            courses_data["syllabus_and_curriculum"]["structure"],
            "📘"
        )

    elif intent == "REGULATIONS":
        return format_lines(
            "📜 Academic Regulations",
            courses_data["syllabus_and_curriculum"]["regulations"],
            "📄"
        )

    # ---------- PLACEMENTS ----------
    elif intent == "PLACEMENT_PERCENTAGE":
        return format_lines(
            "📈 Placement Record",
            courses_data["placements"]["placement_percentage"],
            "📊"
        )

    elif intent == "TOP_RECRUITERS":
        return format_lines(
            "🏢 Top Recruiters",
            courses_data["placements"]["top_recruiters"],
            "🏭"
        )

    elif intent == "PACKAGE_DETAILS":
        pkg = courses_data["placements"]["packages"]
        return format_lines(
            "💼 Package Details",
            [
                f"Average Package: {pkg['average_package']}",
                f"Highest Package: {pkg['highest_package']}"
            ],
            "💰"
        )

    elif intent == "INTERNSHIP_DETAILS":
        return format_lines(
            "🧑‍💻 Internship Opportunities",
            courses_data["placements"]["internships"],
            "🛠️"
        )

    # ---------- VALUE ADDED ----------
    elif intent == "TECHNICAL_COURSES":
        return format_lines(
            "🧠 Technical Value Added Courses",
            courses_data["value_added_courses"]["technical"],
            "⚙️"
        )

    elif intent == "SOFT_SKILLS":
        return format_lines(
            "🗣️ Soft Skills Training",
            courses_data["value_added_courses"]["soft_skills"],
            "🌱"
        )

    # ---------- RESEARCH ----------
    elif intent == "RESEARCH_ACTIVITIES":
        return format_lines(
            "🔬 Research & Innovation Activities",
            courses_data["research_and_innovation"]["activities"],
            "🚀"
        )

    # ---------- INDUSTRY ----------
    elif intent == "INDUSTRY_EXPOSURE":
        return format_lines(
            "🏭 Industry Exposure",
            courses_data["industry_exposure"]["activities"],
            "🤝"
        )

    return "Sorry, I could not find the information you requested."
