# UNIguide AI Codebase Instructions

## Architecture Overview

UNIguide is a Flask-based educational chatbot serving college information queries. The system uses a **service-per-domain pattern** with intent detection and data-driven responses.

### Core Components

1. **Flask App** ([backend/app.py](../backend/app.py)): Routes queries through a processing pipeline with keyword-based domain detection
2. **Intent Detection**: Each domain (departments, admissions, events, etc.) has matching `*_intents.py` files using `SentenceTransformer` ("all-MiniLM-L6-v2") for semantic matching
3. **Service Layer**: `*_services.py` files load JSON data and return formatted responses
4. **Response Formatter** ([backend/services/response_formatter.py](../backend/services/response_formatter.py)): Normalizes content into bullet-point lists with emoji headers

## Query Processing Pipeline

The `/chat` route executes this sequence:

```
1. Media Check (get_media_response) → Return if found
2. College Overview Intent → Return if matched
3. Department Detection (CSM, AIML, CAD, CIVIL, CSE, ECE, EEE, IT, MECH)
   → Detect intent (department, faculty, vision_mission, year_1-4, etc.)
   → Return formatted service response
4. Admissions Intent → Return if matched
5. Programs/Courses Intent → Return if matched
6. Events Intent → Return if matched
7. RAG Fallback (get_rag_answer) → Query website embeddings with cosine similarity
```

**Key Pattern**: Keyword matching (`CSM_KEYWORDS = ["csm", "cse aiml"]`) gates domain detection; only matched domains run intent detection.

## Adding New Content or Departments

### For New Department
1. Create `backend/data/departments/<dept>.json` with structure from [backend/data/departments/cse.json](../backend/data/departments/cse.json)
2. Create `backend/services/<dept>_intents.py` with intent definitions using `SentenceTransformer`
3. Create `backend/services/<dept>_services.py` with intent handlers
4. Add imports and keyword detection to [backend/app.py](../backend/app.py) in the DEPARTMENTS section
5. Add routing logic (keyword matching + intent detection) following existing department patterns

### Intent Detection Pattern
Intents are simple dict maps: `"intent_key": ["example query 1", "example query 2", ...]`. The `detect_*_intent()` function uses semantic embeddings to find the best match score.

### Response Pattern
All responses use `format_lines(title, content, emoji)` to normalize output with consistent bullet formatting and emoji headers.

## Data Structure

- **JSON Data**: `backend/data/` stores all college information (departments, admissions, events, programs)
- **Website Scraping**: `backend/data/website_scraped.txt` feeds RAG embeddings; run scraper to update
- **Static Assets**: Images in `backend/static/images/`, served via `get_media_response()`

## Critical Dependencies

- `flask`, `flask-cors`: Web framework
- `sentence-transformers` ("all-MiniLM-L6-v2"): Intent detection and RAG embeddings
- `json`: Data loading (UTF-8 required)

## Common Workflows

**Update department info**: Edit JSON in `backend/data/departments/`, no code changes needed  
**Add new intent**: Add entry to `*_INTENTS` dict and handler in `*_services.py`  
**Debug intent matching**: Check `detect_*_intent()` returns `(intent_key, score)` tuple; low scores require more example queries  
**Test new feature**: Add route in `app.py`, manually test `/chat` endpoint with POST `{"query": "..."}` (no server restart needed with Flask debug mode)
