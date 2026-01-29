import json
import os

# ================= LOAD DATA =================
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data","departments", "cad.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# ================= HELPERS =================
def format_list(title, items, emoji="🔹"):
    res = f"{title}:\n\n"
    for item in items:
        res += f"{emoji} {item}\n"
    return res.strip()

# ================= MAIN SERVICE =================
def get_cad_department_response(intent):

    dept = data.get("department", {})
    about = data.get("about_department", {})
    vm = data.get("vision_and_mission", {})
    hod = data.get("head_of_department", {})
    faculty = data.get("faculty", [])
    peo = data.get("peo_po_pso", {})
    academics = data.get("academic_structure", {})
    outcomes = data.get("course_outcomes", {})
    activities = data.get("activities", {})
    placements = data.get("placements", {})

    # -------- BASIC --------
    if intent == "department":
        return (
            f"🏫 {dept.get('name')}\n\n"
            f"🎓 College: {dept.get('college')}\n"
            f"📍 Location: {dept.get('location')}\n"
            f"📅 Introduced: {dept.get('introduced_year')}\n"
            f"👥 Intake: {dept.get('intake_capacity')}"
        )

    # -------- ABOUT --------
    elif intent == "about_department":
        lines = [about.get("overview", "")]
        lines += about.get("focus_areas", [])
        return format_list("📘 About CAD Department", lines)

    # -------- VISION & MISSION --------
    elif intent == "vision_and_mission":
        res = f"🎯 Vision:\n✨ {vm.get('vision')}\n\n🚀 Mission:\n"
        for m in vm.get("mission", []):
            res += f"✅ {m}\n"
        return res.strip()

    # -------- HOD --------
    elif intent == "head_of_department":
        return (
            f"👨‍🏫 Head of Department\n\n"
            f"👤 Name: {hod.get('name')}\n"
            f"🎓 Designation: {hod.get('designation')}\n"
            f"📘 Qualification: {hod.get('qualification')}\n"
            f"📧 Email: {hod.get('email')}"
        )

    # -------- FACULTY --------
    elif intent == "faculty":
        lines = [
            f"{f.get('name')} – {f.get('designation')} ({f.get('qualification')})"
            for f in faculty
        ]
        return format_list("👩‍🏫 CAD Faculty Members", lines)

    # -------- PEO / PO / PSO --------
    elif intent == "peo_po_pso":
        res = "🎯 PEOs:\n"
        for p in peo.get("peos", []):
            res += f"🔹 {p}\n"

        res += "\n📘 POs:\n"
        for p in peo.get("pos", []):
            res += f"🔹 {p}\n"

        res += "\n📗 PSOs:\n"
        for p in peo.get("psos", []):
            res += f"🔹 {p}\n"

        return res.strip()

    # -------- ACADEMICS --------
    elif intent == "academic_structure":
        return format_list(
            "📚 CAD Academic Structure",
            [y.replace("_", " ").title() for y in academics.keys()]
        )

    elif intent.startswith("year_"):
        year_data = academics.get(intent, {})
        res = f"📘 {intent.replace('_', ' ').title()} Curriculum:\n\n"

        for sem, sem_data in year_data.items():
            res += f"📗 {sem.replace('_', ' ').title()}:\n"
            for s in sem_data.get("subjects", []):
                res += f"• {s}\n"
            for l in sem_data.get("labs", []):
                res += f"🧪 {l}\n"
            res += "\n"

        return res.strip()

    # -------- COURSE OUTCOMES --------
    elif intent == "course_outcomes":
        return format_list(
            "🎓 CAD Course Outcomes",
            outcomes.get("ai_ml", [])
        )

    # -------- ACTIVITIES --------
    elif intent == "activities":
        res = "🎉 CAD Department Activities:\n\n"

        visits = activities.get("industrial_visits", {}).get("visits", [])
        if visits:
            res += "🏭 Industrial Visits:\n"
            for v in visits:
                res += f"• {v.get('company')} – {v.get('location')} ({v.get('date')})\n"

        clubs = activities.get("student_clubs", [])
        if clubs:
            res += "\n🎯 Student Clubs:\n"
            for c in clubs:
                res += f"• {c}\n"

        return res.strip()

    # -------- PLACEMENTS --------
    elif intent == "placements":
        res = "💼 CAD Placement Details:\n\n"
        res += f"🎯 Training: {placements.get('training')}\n\n"
        res += "🚀 Career Domains:\n"
        for c in placements.get("career_domains", []):
            res += f"• {c}\n"
        return res.strip()

    return "❌ CAD department information not found."
