# config/feature_flags.py
import os

FEATURE_FLAGS = {
    "NEW_THEME": os.getenv("FEATURE_NEW_THEME", "false").lower() == "true",
    "RESUME_UPLOAD": os.getenv("FEATURE_RESUME_UPLOAD", "false").lower() == "true",
    "MCS_RECOMMENDER": os.getenv("FEATURE_MCS", "false").lower() == "true",
    "ASK_ALUM": os.getenv("FEATURE_ASK_ALUM", "false").lower() == "true",
}
