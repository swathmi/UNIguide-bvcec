import json
import os
from services.response_formatter import format_lines

# ---------------- LOAD JSON DATA ----------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "events_scraped.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# ================= MAIN SERVICE FUNCTION =================

def get_institution_response(intent, extra=None):

    # ================= PLACEMENTS =================
    if intent == "PLACEMENT_OVERVIEW":
        return data["placements"]["overview"]

    elif intent == "PLACEMENT_HEAD":
        head = data["placements"]["placement_head"]
        return format_lines(
            "🏢 Placement Cell Head",
            [
                f"Name: {head['name']}",
                f"Designation: {head['designation']}",
                f"Email: {head['email']}"
            ],
            "📌"
        )

    elif intent == "FIRST_PLACEMENT_2026":
        fp = data["placements"]["batch_wise_placements"]["2026"]["first_placement"]
        return format_lines(
            "🎉 First Placement – 2026",
            [
                f"Student: {fp['student_name']}",
                f"Branch: {fp['branch']}",
                f"Company: {fp['company']}",
                f"Package: {fp['package']}",
                f"Date: {fp['date']}"
            ],
            "🏆"
        )

    elif intent == "PLACEMENT_DRIVES":
        drives = data["placements"]["drives_summary"]["drive_list"]
        lines = [
            f"{d['company']} | {d['drive_date']} | {d['average_package']}"
            for d in drives
        ]
        return format_lines("🚗 Placement Drives", lines, "📍")

    elif intent == "ONGOING_PLACEMENT_DRIVES":
        return data["placements"]["ongoing_drives"]["status"]

    elif intent == "UPCOMING_PLACEMENT_DRIVES":
        return data["placements"]["upcoming_drives"]["status"]

    elif intent == "TOP_RECRUITERS":
        return format_lines(
            "🏢 Top Recruiters",
            data["placements"]["top_leading_recruiters"],
            "🏭"
        )

    elif intent == "PLACEMENT_TRAINING":
        return format_lines(
            "🎯 Placement Training Programs",
            data["placements"]["training_and_preparation"]["placement_training_programs"],
            "📘"
        )

    elif intent == "COMPANY_WISE_PLACEMENTS" and extra:
        company = data["placements"]["company_lookup"].get(extra)
        if not company:
            return "Company details not found."
        return format_lines(
            f"🏢 {extra} – Placement Details",
            [
                f"Drive Date: {company['drive_date']}",
                f"Package: {company['package']}",
                f"Eligible Branches: {', '.join(company['branches'])}"
            ],
            "📌"
        )

    # ================= EVENTS =================
    elif intent == "EVENT_TYPES":
        return format_lines(
            "🎉 Types of Events Conducted",
            data["events"]["event_types_conducted"],
            "🎈"
        )

    elif intent == "TECHNICAL_EVENTS":
        return format_lines(
            "💻 Technical Events",
            data["events"]["technical_events"],
            "⚙️"
        )

    elif intent == "WORKSHOPS_SEMINARS":
        return format_lines(
            "🧠 Workshops & Seminars",
            data["events"]["workshops_and_seminars"],
            "📚"
        )

    elif intent == "CULTURAL_EVENTS":
        return format_lines(
            "🎭 Cultural Events",
            data["events"]["cultural_events"],
            "🎶"
        )

    elif intent == "NSS_EVENTS":
        return format_lines(
            "🌱 NSS & Social Activities",
            data["events"]["nss_and_social_activities"],
            "🤝"
        )

    elif intent == "RECENT_EVENTS":
        return format_lines(
            "🕒 Recent Events",
            data["events"]["recent_events"],
            "📍"
        )

    # ================= LATEST UPDATES =================
    elif intent == "LATEST_UPDATES":
        updates = [
            f"{u['date']} – {u['title']}"
            for u in data["latest_updates"]
        ]
        return format_lines("📰 Latest Updates", updates, "🆕")

    # ================= FDP =================
    elif intent == "FACULTY_DEVELOPMENT_PROGRAMS":
        fdps = data["faculty_development_programs"]["programs"]
        lines = [
            f"{f['faculty_name']} – {f['title']} ({f['duration']})"
            for f in fdps
        ]
        return format_lines("👨‍🏫 Faculty Development Programs", lines, "📘")

    # ================= RESEARCH =================
    elif intent == "RESEARCH_PUBLICATIONS":
        pubs = data["research_publications"]["publications"]
        lines = [
            f"{p['faculty_name']} – {p['paper_title']} ({p['indexing']})"
            for p in pubs
        ]
        return format_lines("📄 Research Publications", lines, "🔬")

    elif intent == "FACULTY_WISE_PUBLICATIONS" and extra:
        pubs = [
            p for p in data["research_publications"]["publications"]
            if extra.lower() in p["faculty_name"].lower()
        ]
        if not pubs:
            return "No publications found for this faculty."
        return format_lines(
            f"📚 Publications by {extra}",
            [p["paper_title"] for p in pubs],
            "📄"
        )

    return "Sorry, I could not find the information you requested."
