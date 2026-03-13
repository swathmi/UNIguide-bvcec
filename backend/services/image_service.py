import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
IMAGES_PATH = os.path.join(BASE_DIR, "data", "website_images.json")

# Load all images
with open(IMAGES_PATH, "r", encoding="utf-8") as f:
    all_images = json.load(f)


def get_images_for_query(query, limit=3):
    """
    Get relevant images from scraped data based on query keywords.
    Returns list of image dicts with url, alt, description.
    """
    query_lower = query.lower()
    
    # Keywords to search in alt, description
    keywords = query_lower.split()
    
    scored_images = []
    
    for img in all_images:
        alt_text = img.get("alt", "").lower()
        description = img.get("description", "").lower()
        
        # Calculate relevance score
        score = 0
        for keyword in keywords:
            if keyword in alt_text:
                score += 2
            if keyword in description:
                score += 1
        
        if score > 0:
            scored_images.append({
                "score": score,
                "url": img.get("url"),
                "alt": img.get("alt", "Image"),
                "description": img.get("description", "")
            })
    
    # Sort by score and return top N
    scored_images.sort(key=lambda x: x["score"], reverse=True)
    return scored_images[:limit]
