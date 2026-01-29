import json
import os
from services.response_formatter import format_lines


# ---------------- LOAD JSON DATA ----------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "college_overview.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    college_data = json.load(f)


# ================= HELPER FUNCTIONS =================

def to_list(text):
    """Converts paragraph text into a list"""
    if isinstance(text, list):
        return text
    if text:
        return [text]
    return []


def format_response(title, points, emoji="🔹"):
    """
    Converts any content into neat
    line-by-line emoji formatted response
    """
    response = f"{title}:\n\n"
    for point in points:
        response += f"{emoji} {point}\n"
    return response.strip()


def get_management_profile(designation):
    members = college_data.get("management", {}).get("members", [])
    for member in members:
        if member.get("designation", "").lower() == designation.lower():
            return {
                "type": "profile_with_text",
                "name": member.get("name", "Not available"),
                "designation": member.get("designation", designation),
                "description": member.get("description", "Information not available"),
                "photo": member.get("photo", "")
            }
    return "⚠️ Information not available."


# ================= MAIN RESPONSE FUNCTION =================

def get_college_overview_response(intent):

    basic = college_data.get("basic_identity", {})

    # -------- BASIC DETAILS --------
    if intent == "COLLEGE_NAME":
        return format_response(
            "🏫 College Name",
            [basic.get("college_name", "Bonam Venkata Chalamayya Engineering College")],
            "📘"
        )

    elif intent == "COLLEGE_SHORT_NAME":
        return format_response(
            "🏷️ College Short Name",
            [basic.get("short_name", "BVCEC")],
            "🔤"
        )

    elif intent == "COLLEGE_CODE":
        return format_response(
            "🏷️ College Code",
            [basic.get("college_code", "Not available")],
            "🔢"
        )

    elif intent == "COLLEGE_TYPE":
        return format_response(
            "🏛️ College Type",
            [basic.get("college_type", "Autonomous Engineering College")],
            "🏢"
        )

    elif intent == "ESTABLISHMENT_YEAR":
        year = basic.get("established_year", "N/A")
        return format_response(
            "📅 Establishment Year",
            [f"Established in {year}"],
            "📌"
        )

    # -------- VISION & MISSION --------
    elif intent == "COLLEGE_VISION":
        vision = college_data.get("vision_mission", {}).get("vision", "")
        return format_response(
            "🎯 College Vision",
            to_list(vision),
            "✨"
        )

    elif intent == "COLLEGE_MISSION":
        mission = college_data.get("vision_mission", {}).get("mission", [])
        return format_response(
            "🚀 College Mission",
            mission,
            "✅"
        )

    # -------- MANAGEMENT (PHOTO CARDS) --------
    elif intent == "CHAIRMAN_DETAILS":
        return get_management_profile("Chairman")

    elif intent == "FORMER_CHAIRMAN_DETAILS":
        return get_management_profile("Former Chairman")

    elif intent == "FOUNDER_DETAILS":
        return get_management_profile("Founder")

    elif intent == "PRINCIPAL_DETAILS":
        return get_management_profile("Principal")

    elif intent == "VICE_PRINCIPAL_DETAILS":
        return get_management_profile("Vice Principal")

    elif intent == "SECRETARY_DETAILS":
        return get_management_profile("Secretary")

    # -------- LOCATION & CONTACT --------
    elif intent == "COLLEGE_LOCATION":
        loc = college_data.get("location", {})
        return format_response(
            "📍 College Location & Address",
            [
                loc.get("address", "Address not available"),
                f"Landmark: {loc.get('landmark', 'N/A')}",
                f"Pincode: {loc.get('pincode', 'N/A')}"
            ],
            "📌"
        )

    elif intent == "COLLEGE_CONTACT":
        contact = college_data.get("contact", {})
        return format_response(
            "📞 Contact Details",
            [
                f"Office Phone: {contact.get('office_phone', 'N/A')}",
                f"Admission Helpline: {contact.get('admission_helpline', 'N/A')}",
                f"Email: {contact.get('official_email', 'N/A')}"
            ],
            "☎️"
        )

    # -------- ACCREDITATION --------
    elif intent == "COLLEGE_ACCREDITATION":
        acc = college_data.get("accreditation_and_approvals", {})
        return format_response(
            "🏅 Accreditation & Approvals",
            [
                acc.get("aicte", "AICTE Approved"),
                acc.get("naac", "NAAC Accredited"),
                acc.get("nba", "NBA Accredited"),
                acc.get("ugc", "UGC Approved")
            ],
            "🎖️"
        )

    # -------- INFRASTRUCTURE --------
    elif intent == "INFRASTRUCTURE":
        infra = college_data.get("campus_and_infrastructure", {}).get("facilities", [])
        return format_response(
            "🏫 Campus Infrastructure & Facilities",
            infra,
            "🏢"
        )

    # -------- CULTURE --------
    elif intent == "COLLEGE_CULTURE":
        culture = college_data.get("culture_and_values", {})
        return format_response(
            "🌱 College Culture & Values",
            [
                culture.get("discipline", "Discipline focused"),
                culture.get("ethics", "Ethical education")
            ],
            "🌟"
        )

    # -------- TIMINGS --------
    elif intent == "COLLEGE_TIMINGS":
        t = college_data.get("college_timings", {})
        return format_response(
            "⏰ College Timings",
            [
                f"Working Days: {t.get('working_days', 'N/A')}",
                f"College Hours: {t.get('college_hours', 'N/A')}"
            ],
            "🕘"
        )
    elif intent == "campus_size":
        c = college_data.get("campus_and_infrastructure", {})
        return format_response(
            "🏫 Campus Size",
            [
                f"Campus Area: {c.get('campus_area', 'N/A')}"
            ],
            "🌿"
        )



    # -------- WHY CHOOSE COLLEGE --------
    elif intent == "WHY_CHOOSE_COLLEGE":
        highlights = college_data.get("why_choose_bvcec", {}).get("highlights", [])
        return format_response(
            "⭐ Why Choose BVCEC",
            highlights,
            "💡"
        )

    return "Sorry, I could not find the information you requested."
