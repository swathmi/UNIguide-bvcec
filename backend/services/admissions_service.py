import json
import os
from services.response_formatter import format_lines

# ---------------- LOAD JSON DATA ----------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "admissions.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    admissions_data = json.load(f)


# ================= MAIN SERVICE FUNCTION =================

def get_admissions_response(intent):

    # ---------- DEGREE LEVEL ----------
    if intent == "DEGREES_OFFERED":
        return format_lines(
            "🎓 Degrees Offered",
            admissions_data["degrees_offered"],
            "🔹"
        )

    # ---------- ADMISSION OVERVIEW ----------
    elif intent == "ADMISSION_OVERVIEW":
        return format_lines(
            "📘 Admission Overview",
            admissions_data["admission_overview"],
            "🔹"
        )

    elif intent == "ADMISSION_MODES":
        return format_lines(
            "📌 Admission Modes",
            admissions_data["admission_modes"],
            "🔹"
        )

    # ---------- BTECH ----------
    elif intent == "BTECH_ADMISSION_PROCESS":
        return format_lines(
            "🎓 B.Tech Admission Process",
            admissions_data["btech_admission_process"],
            "🔹"
        )

    elif intent == "BTECH_ELIGIBILITY":
        return format_lines(
            "✅ B.Tech Eligibility",
            admissions_data["btech_eligibility"],
            "🔹"
        )

    elif intent == "BTECH_ENTRANCE_EXAM":
        return format_lines(
            "📝 B.Tech Entrance Exam",
            admissions_data["btech_entrance_exam"],
            "🔹"
        )

    elif intent == "BTECH_COUNSELING":
        return format_lines(
            "🧾 B.Tech Counseling",
            admissions_data["btech_counseling"],
            "🔹"
        )

    # ---------- LATERAL ENTRY ----------
    elif intent == "LATERAL_ENTRY_OVERVIEW":
        return format_lines(
            "🔁 Lateral Entry Admission",
            admissions_data["lateral_entry_overview"],
            "🔹"
        )

    elif intent == "LATERAL_ENTRY_ELIGIBILITY":
        return format_lines(
            "✅ Lateral Entry Eligibility",
            admissions_data["lateral_entry_eligibility"],
            "🔹"
        )

    elif intent == "LATERAL_ENTRY_ENTRANCE_EXAM":
        return format_lines(
            "📝 Lateral Entry Entrance Exam",
            admissions_data["lateral_entry_entrance_exam"],
            "🔹"
        )

    # ---------- MANAGEMENT QUOTA ----------
    elif intent == "MANAGEMENT_QUOTA_OVERVIEW":
        return format_lines(
            "🏫 Management Quota Overview",
            admissions_data["management_quota_overview"],
            "🔹"
        )

    elif intent == "MANAGEMENT_QUOTA_ELIGIBILITY":
        return format_lines(
            "✅ Management Quota Eligibility",
            admissions_data["management_quota_eligibility"],
            "🔹"
        )

    elif intent == "MANAGEMENT_QUOTA_PROCESS":
        return format_lines(
            "📄 Management Quota Process",
            admissions_data["management_quota_process"],
            "🔹"
        )

    # ---------- IMPORTANT DATES ----------
    elif intent == "IMPORTANT_ADMISSION_DATES":
        return format_lines(
            "📅 Important Admission Dates",
            admissions_data["important_admission_dates"],
            "🔹"
        )

    # ---------- DOCUMENTS ----------
    elif intent == "DOCUMENTS_REQUIRED_MANDATORY":
        return format_lines(
            "📂 Mandatory Documents Required",
            admissions_data["documents_required_mandatory"],
            "🔹"
        )

    elif intent == "DOCUMENTS_REQUIRED_CATEGORY":
        return format_lines(
            "📂 Category-wise Documents",
            admissions_data["documents_required_category"],
            "🔹"
        )

    # ---------- COUNSELING ----------
    elif intent == "COUNSELING_AUTHORITY":
        return format_lines(
            "🏛️ Counseling Authority",
            admissions_data["counseling_authority"],
            "🔹"
        )

    elif intent == "COUNSELING_STEPS":
        return format_lines(
            "🧭 Counseling Steps",
            admissions_data["counseling_steps"],
            "🔹"
        )

    elif intent == "SEAT_ALLOTMENT_RULES":
        return format_lines(
            "📊 Seat Allotment Rules",
            admissions_data["seat_allotment_rules"],
            "🔹"
        )

    # ---------- RESERVATION ----------
    elif intent == "RESERVATION_POLICY_OVERVIEW":
        return format_lines(
            "📜 Reservation Policy",
            admissions_data["reservation_policy_overview"],
            "🔹"
        )

    elif intent == "RESERVATION_SC":
        return format_lines(
            "🧾 SC Reservation",
            admissions_data["reservation_sc"],
            "🔹"
        )

    elif intent == "RESERVATION_ST":
        return format_lines(
            "🧾 ST Reservation",
            admissions_data["reservation_st"],
            "🔹"
        )

    elif intent == "RESERVATION_BC":
        return format_lines(
            "🧾 BC Reservation",
            admissions_data["reservation_bc"],
            "🔹"
        )

    elif intent == "RESERVATION_EWS":
        return format_lines(
            "🧾 EWS Reservation",
            admissions_data["reservation_ews"],
            "🔹"
        )

    elif intent == "RESERVATION_PWD":
        return format_lines(
            "🧾 PwD Reservation",
            admissions_data["reservation_pwd"],
            "🔹"
        )

    elif intent == "MANAGEMENT_QUOTA_RESERVATION":
        return format_lines(
            "🚫 Reservation in Management Quota",
            admissions_data["management_quota_reservation"],
            "🔹"
        )

    # ---------- HELP DESK ----------
    elif intent == "ADMISSION_OFFICER_DETAILS":
        return format_lines(
            "👤 Admission Officer Details",
            admissions_data["admission_officer_details"],
            "🔹"
        )

    elif intent == "ADMISSION_CONTACT_NUMBERS":
        return format_lines(
            "📞 Admission Contact Numbers",
            admissions_data["admission_contact_numbers"],
            "🔹"
        )

    elif intent == "ADMISSION_EMAIL_CONTACTS":
        return format_lines(
            "📧 Admission Email Contacts",
            admissions_data["admission_email_contacts"],
            "🔹"
        )

    # ---------- INTERNATIONAL / NEPAL ----------
    elif intent == "INTERNATIONAL_STUDENTS_OVERVIEW":
        return format_lines(
            "🌍 International Students",
            admissions_data["international_students_overview"],
            "🔹"
        )

    elif intent == "NEPAL_STUDENTS_AVAILABILITY":
        return format_lines(
            "🇳🇵 Nepal Students in BVCEC",
            admissions_data["nepal_students_availability"],
            "🔹"
        )

    elif intent == "NEPAL_REGISTERED_OFFICE_DETAILS":
        return format_lines(
            "🇳🇵 Nepal Registered Office Details",
            admissions_data["nepal_registered_office_details"],
            "🔹"
        )

    elif intent == "INTERNATIONAL_ADMISSIONS_INCHARGE":
        return format_lines(
            "🌍 International Admissions In-charge",
            admissions_data["international_admissions_incharge"],
            "🔹"
        )

    elif intent == "INTERNATIONAL_ADMISSIONS_CONTACT":
        return format_lines(
            "📞 International Admissions Contact",
            admissions_data["international_admissions_contact"],
            "🔹"
        )

    elif intent == "INTERNATIONAL_ADMISSIONS_ADDRESS":
        return format_lines(
            "📍 International Admissions Address",
            admissions_data["international_admissions_address"],
            "🔹"
        )

    # ---------- GENERAL RULES ----------
    elif intent == "GENERAL_ADMISSION_RULES":
        return format_lines(
            "📑 General Admission Rules",
            admissions_data["general_admission_rules"],
            "🔹"
        )

    return "Sorry, I could not find the admission information you requested."
