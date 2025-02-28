# src/sound_collection.py
"""
Module for querying Freesound, downloading sound previews,
and creating metadata records for a collection of sound fonts.
"""

import os
import freesound
from src import config

# Initialize Freesound client with the API key from config
freesound_client = freesound.FreesoundClient()
freesound_client.set_token(config.FREESOUND_API_KEY)


def query_freesound(query, filter, num_results=10):
    """
    Query Freesound with the given search term and filter.
    Returns a list of Freesound sound objects.
    
    If no filter is provided, a default filter (duration less than 30 seconds) is used.
    """
    # Use default filter if none provided
    if filter is None:
        filter = 'duration:[0 TO 30]'
    pager = freesound_client.text_search(
        query=query,
        filter=filter,
        fields=','.join(config.FREESOUND_STORE_METADATA_FIELDS),
        group_by_pack=1,
        page_size=num_results
    )
    # Return the results as a list
    return [sound for sound in pager]

def download_sound_preview(sound, directory):
    """
    Download the high-quality OGG preview of a given Freesound sound object
    and save it in the specified directory.
    """
    # Extract the preview URL and determine the local file name
    preview_url = sound.previews.preview_hq_ogg
    file_name = preview_url.split('/')[-1]
    file_path = os.path.join(directory, file_name)
    
    # Download the file using Freesound's FSRequest
    return freesound.FSRequest.retrieve(preview_url, freesound_client, file_path)

def make_metadata_record(sound, directory):
    """
    Create a dictionary containing metadata for a given Freesound sound object.
    This record is used later to build a Pandas DataFrame.
    """
    # Get the metadata as a dictionary
    record = {key: sound.as_dict()[key] for key in config.FREESOUND_STORE_METADATA_FIELDS}
    
    # Remove the 'previews' dictionary, as we'll store only the file path
    del record['previews']
    
    # Rename 'id' to 'freesound_id' for clarity and remove the original 'id'
    record['freesound_id'] = record['id']
    del record['id']
    
    # Store the local file path for the downloaded preview
    file_name = sound.previews.preview_hq_ogg.split('/')[-1]
    record['path'] = os.path.join(directory, file_name)
    
    return record
