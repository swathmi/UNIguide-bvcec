import json
import os
from services.response_formatter import format_lines

# -------- LOAD JSON DATA --------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PLACEMENT_PATH = os.path.join(BASE_DIR, "data", "placement_materials.json")

with open(PLACEMENT_PATH, "r", encoding="utf-8") as f:
    placement_data = json.load(f)

# ================= MAIN SERVICE FUNCTION =================

def get_placement_response(intent):
    """Returns response based on placement-related intents"""
    
    if intent == "placement_materials":
        return format_lines(
            "📚 Placement Materials Available",
            [
                "🖥️ Programming Languages: C, Java, Python, SQL",
                "📊 Aptitude: Quantitative, Logical Reasoning",
                "🗣️ Verbal: English, Communication",
                "📋 Previous Exam Papers by Subject",
                "💼 Company Placement Information",
                "✅ Ask for specific material: 'java materials', 'aptitude resources', etc."
            ],
            "📖"
        )

    elif intent == "programming_languages":
        langs = placement_data["placement_materials"]["programming_languages"]
        content = []
        for lang in langs:
            content.append(f"{lang['language']}: {lang['description']}")
            for resource in lang['resources']:
                content.append(f"  • {resource['type'].title()}: {resource['title']}")
        
        return format_lines(
            "💻 Programming Languages & Resources",
            content,
            "🔧"
        )

    elif intent == "aptitude_materials":
        apt = placement_data["placement_materials"]["aptitude"]
        content = []
        for category in apt:
            content.append(f"📌 {category['category']}: {category['description']}")
            for resource in category['resources']:
                content.append(f"  • {resource['type'].replace('_', ' ').title()}: {resource['title']}")
        
        return format_lines(
            "🧮 Aptitude Materials & Resources",
            content,
            "📐"
        )

    elif intent == "verbal_materials":
        verbal = placement_data["placement_materials"]["verbal"]
        content = []
        for category in verbal:
            content.append(f"📌 {category['category']}")
            for resource in category['resources']:
                content.append(f"  • {resource['type'].replace('_', ' ').title()}: {resource['title']}")
        
        return format_lines(
            "🗣️ English & Communication Materials",
            content,
            "💬"
        )

    elif intent == "company_placements":
        placements_2025 = placement_data["company_placements"]["2025"]
        content = ["🏢 Top Companies Recruiting from BVCEC (2025):"]
        
        for company in placements_2025["top_companies"]:
            content.append(
                f"{company['company_name']}: {company['students_placed']} students | "
                f"Package: {company['package']} | Branches: {', '.join(company['branches'])}"
            )
        
        content.append("📊 Overall Statistics:")
        stats = placements_2025["placement_statistics"]
        content.append(f"Total Placed: {stats['total_placed']}")
        content.append(f"Average Package: {stats['average_package']}")
        content.append(f"Highest Package: {stats['highest_package']}")
        
        return format_lines(
            "🏆 Company Placements",
            content,
            "💼"
        )

    elif intent == "attendance_policy":
        policy = placement_data["policies"]["attendance_policy"]
        content = [
            f"📌 Minimum Attendance: {policy['minimum_attendance']}",
            f"📌 Subject-wise: {policy['subject_wise']}",
            "",
            "✅ Exemptions:",
        ]
        content.extend([f"  • {ex}" for ex in policy['exemptions']])
        
        content.append("⚠️ Consequences of Low Attendance:")
        content.extend([f"  • {con}" for con in policy['consequences']])
        
        content.append(f"📞 Contact: {policy['contact']}")
        
        return format_lines(
            "📋 Attendance Policy",
            content,
            "✅"
        )

    elif intent == "faculty_development":
        programs = placement_data["policies"]["faculty_development_programs"]
        content = []
        
        for program in programs:
            content.append(f"📌 {program['program']} (Duration: {program['duration']})")
            for benefit in program['benefits']:
                content.append(f"  ✓ {benefit}")
            content.append("")
        
        return format_lines(
            "👨‍🏫 Faculty Development Programs",
            content,
            "📚"
        )

    elif intent == "circulars":
        circulars = placement_data["policies"]["circulars"]
        content = []
        
        for circular in sorted(circulars, key=lambda x: x['date'], reverse=True):
            content.append(
                f"📌 [{circular['date']}] {circular['title']} ({circular['category']})"
            )
            content.append(f"   {circular['content']}")
            content.append("")
        
        return format_lines(
            "📢 Latest Circulars & Announcements",
            content,
            "📣"
        )

    return "ℹ️ Please specify what placement information you need."
