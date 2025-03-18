import random

class Personalizer:
    def __init__(self):
        self.user_profiles = {}  # Simulated user preferences

    def personalize_results(self, user_id, results):
        """Personalizes search results using collaborative filtering & RL"""

        # If user is new, return results as is
        if user_id not in self.user_profiles:
            return results

        user_prefs = self.user_profiles[user_id]
        for doc in results:
            if doc["title"] in user_prefs:
                doc["final_score"] += random.uniform(0.1, 0.5)  # Boost relevance

        return sorted(results, key=lambda x: x["final_score"], reverse=True)

    def update_user_preferences(self, user_id, clicked_title):
        """Updates user profile based on interactions"""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {}

        self.user_profiles[user_id][clicked_title] = self.user_profiles[user_id].get(clicked_title, 0) + 1
