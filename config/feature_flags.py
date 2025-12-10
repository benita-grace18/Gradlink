# config/feature_flags.py
import os

FEATURE_FLAGS = {
    "NEW_THEME": os.getenv("FEATURE_NEW_THEME", "true").lower() == "true",
    "RESUME_UPLOAD": os.getenv("FEATURE_RESUME_UPLOAD", "true").lower() == "true",
    "MCS_RECOMMENDER": os.getenv("FEATURE_MCS", "true").lower() == "true",
    "ASK_ALUM": os.getenv("FEATURE_ASK_ALUM", "true").lower() == "true",
}
