# Student Services Feature Implementation

## Overview
Comprehensive student support services chatbot feature added to UNIguide. Provides guidance on mental health, academics, hostel, scholarships, internships, exams, clubs, and learning resources.

## Implementation Summary

### 1. Data Files Created (JSONs)
Location: `backend/data/student_services/`

- **mental_health_support.json** - Mental health resources & crisis support
- **academic_support.json** - Tutoring, coaching, backlog clearance
- **hostel_guide.json** - Hostel facilities, fees, application process
- **scholarships_financial_aid.json** - Merit/need-based scholarships, loans
- **internship_opportunities.json** - Career timeline, companies, prep tips
- **exam_countdown.json** - Exam schedules, time management per department
- **clubs_societies.json** - Technical, cultural, sports clubs & professional bodies
- **extra_curricular_resources.json** - Learning platforms, books, skill development
- **student_wellness.json** - Mental health, fitness, career guidance
- **learning_resources.json** - Coding, DS, web design, certification prep

### 2. Intent Detection System
File: `backend/services/student_services_intents.py`

**Supported Intents (9 categories):**
1. `mental_health` - Psychological support, stress management
2. `academic_help` - Tutoring, remedial classes, backlog clearance
3. `hostel_information` - Accommodation, mess, facilities
4. `scholarships_financial_aid` - Financial assistance & loans
5. `internship_preparation` - Career guidance & placement prep
6. `exam_preparation` - Exam schedules & study tips
7. `clubs_and_societies` - Extracurricular activities
8. `extra_curricular_resources` - Learning materials & skill development
9. `general_student_services` - Overview of all available services

**Technology:**
- Uses `SentenceTransformer` (all-MiniLM-L6-v2) for semantic similarity matching
- Threshold: 0.4 (configurable in intent detection)
- Returns: (intent_key, confidence_score)

### 3. Response Handler
File: `backend/services/student_services_service.py`

**Features:**
- Loads student service JSON data on demand
- Maps intents to handler functions
- Returns formatted responses using `format_lines()` utility
- Includes emoji headers & bullet-point formatting
- Graceful error handling with fallback messages

**Handler Functions:**
- `get_mental_health_support()` - Counselling, wellness programs
- `get_academic_help()` - Tutoring, study materials
- `get_hostel_information()` - Accommodation & amenities
- `get_scholarships_financial_aid()` - Financial aid options
- `get_internship_opportunities()` - Career guidance
- `get_exam_countdown()` - Exam preparation
- `get_clubs_societies()` - Club information
- `get_learning_resources()` - Skill development resources

### 4. Chat Pipeline Integration
File: `backend/app.py` (Lines 773-787)

**Pipeline Position:** Step 1.7 (before department detection)

**Process:**
1. User query processed
2. Intent detection via `detect_student_service_intent()`
3. Score threshold check (minimum 0.5 for activation)
4. Response generation via `get_student_service_response()`
5. Formatting via `format_student_service_response()`
6. Chat history saved to database

**Priority:** Runs before department queries, after college overview & admissions

## Example Queries

### Mental Health
- "How do I manage stress about exams?"
- "I feel overwhelmed with studies"
- "Where can I talk to a counselor?"

### Scholarships
- "How do I get a scholarship?"
- "SC ST OBC scholarship eligibility"
- "Education loan options"

### Internships
- "How to prepare for internship?"
- "Expected CTC for CSE?"
- "Resume building tips"

### Exams
- "How many days until exams?"
- "How to manage time during exams?"
- "Exam schedule for CSE?"

### Clubs
- "What clubs are available?"
- "How to join coding club?"
- "Sports club information"

## Architecture

```
User Query
    ↓
Intent Detection (SentenceTransformer)
    ↓
Route to Handler Function
    ↓
Load JSON Data (if needed)
    ↓
Format Response (emoji headers + bullets)
    ↓
Return to Frontend
    ↓
Save Chat to Database
```

## File Structure

```
backend/
├── data/student_services/
│   ├── mental_health_support.json
│   ├── academic_support.json
│   ├── hostel_guide.json
│   ├── scholarships_financial_aid.json
│   ├── internship_opportunities.json
│   ├── exam_countdown.json
│   ├── clubs_societies.json
│   ├── extra_curricular_resources.json
│   └── ... (6 total JSON files)
├── services/
│   ├── student_services_intents.py (Intent detection)
│   ├── student_services_service.py (Response handlers)
│   └── response_formatter.py (Formatting utility)
└── app.py (Pipeline integration)
```

## Configuration

### To Adjust Intent Threshold
Edit `backend/app.py` line 775:
```python
if student_service_intent and service_score >= 0.5:  # Change 0.5 to desired value (0.3-0.7)
```

### To Add New Student Service
1. Create new intent in `STUDENT_SERVICES_INTENTS` dict (student_services_intents.py)
2. Add example queries for training semantic matching
3. Create corresponding handler function in student_services_service.py
4. Add JSON data file (optional, for future enhancement)
5. Map intent to handler in `get_student_service_response()`

### To Update Content
Edit corresponding JSON file in `backend/data/student_services/`
- No code changes required
- Changes reflect immediately in production

## Dependencies

- **sentence-transformers**: For semantic intent matching
- **torch**: For tensor operations (required by sentence-transformers)
- **response_formatter.py**: For consistent message formatting

## Testing

Test the feature with sample queries:
- "I'm stressed about exams"
- "How do I apply for hostel?"
- "Tell me about scholarships"
- "What clubs can I join?"
- "How to prepare for internship?"

All queries should return relevant student service information with proper formatting.

## Future Enhancements

1. **Personalization:** Get student's branch and customize responses
2. **Database Integration:** Store student service preferences
3. **Rich Media:** Add images & links to external resources
4. **Real-time Updates:** Auto-update exam dates, event schedules
5. **Multi-language Support:** Translate responses to other languages
6. **Mobile Optimization:** Responsive formatting for mobile devices

## Status: ✅ COMPLETE

All components implemented, tested, and integrated into the chat pipeline.
