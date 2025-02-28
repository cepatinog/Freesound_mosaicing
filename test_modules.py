# test_modules.py
import os
import sys
# Add absolute path to the root
sys.path.append(os.path.abspath(".."))

from src import config, sound_collection


# Test querying Freesound (use a simple query, e.g., "piano")
results = sound_collection.query_freesound("piano", None, num_results=5)
print(f"Retrieved {len(results)} sounds for query 'piano'.")

# Optionally, test downloading a preview for the first sound (ensure the FILES_DIR exists)
import os
if not os.path.exists(config.FILES_DIR):
    os.makedirs(config.FILES_DIR)

if results:
    sound = results[0]
    print(f"Downloading preview for sound id: {sound.id}")
    sound_collection.download_sound_preview(sound, config.FILES_DIR)
    
    # Create a metadata record
    record = sound_collection.make_metadata_record(sound, config.FILES_DIR)
    print("Metadata record for the sound:")
    print(record)
