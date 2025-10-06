import json
from fuzzywuzzy import fuzz
import os


IDEA_STORE_PATH = "data/idea_store.json"


def load_ideas():
    # Create file if missing
    if not os.path.exists(IDEA_STORE_PATH):
        os.makedirs(os.path.dirname(IDEA_STORE_PATH), exist_ok=True)
        with open(IDEA_STORE_PATH, 'w') as f:
            f.write("[]")
        return []

    # Read file safely
    with open(IDEA_STORE_PATH, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # If file is empty or corrupted, reset to empty list
            return []

def save_idea(idea_data):
    data = load_ideas()
    data.append(idea_data)
    with open(IDEA_STORE_PATH, 'w') as f:
        json.dump(data, f, indent=4)



def check_similarity(new_idea, threshold=50):
    existing_ideas = load_ideas()
    for idea in existing_ideas:
        # Skip if the idea is identical to the new one (self-match)
        if idea['name'] == new_idea['name'] and idea['description'] == new_idea['description']:
            continue
        score = fuzz.token_sort_ratio(new_idea['description'], idea['description'])
        if score >= threshold:
            return True, idea, score
    return False, None, 0