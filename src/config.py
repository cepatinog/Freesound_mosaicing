# Configuration settings (e.g., API keys, file paths)
# src/config.py
"""
Configuration file for the audio mosaicing project.
This file contains constants and settings that are used throughout the project.
"""

# Replace with your own Freesound API key
FREESOUND_API_KEY = 'zr5kUObkkKtoSIiWGRPG6DPNUMOxdU1ercdOGcaJ'

# Directory to store downloaded sound files (previews)
RAW_DIR = '../data/raw'
PROCESSED_DIR = '../data/processed'
METADATA_DIR = '../data/metadata'

# CSV file to store metadata of the sound collection
DATAFRAME_FILENAME = '../data/metadata/fonts_collection.csv'

# Freesound metadata properties that we want to store
FREESOUND_STORE_METADATA_FIELDS = ['id', 'name', 'username', 'previews', 'license', 'tags']
