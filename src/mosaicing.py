"""
Module for audio mosaicing.
This module provides functions to:
  - Load audio file segments (with caching)
  - Find similar audio frames using a nearest neighbors approach
  - Choose a source frame to replace a target frame
"""

import os
import numpy as np
import random
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import essentia
import essentia.standard as estd

# Global cache to avoid re-loading audio files
loaded_audio_files = {}

def get_audio_file_segment(file_path, start_sample, n_samples):
    """
    Load an audio file (using caching) and return a segment starting at start_sample with n_samples.
    
    Parameters:
      - file_path: Path to the audio file.
      - start_sample: Starting sample index.
      - n_samples: Number of samples to extract.
      
    Returns:
      - A numpy array containing the requested audio segment.
    """
    if file_path not in loaded_audio_files:
        loader = estd.MonoLoader(filename=file_path)
        audio = loader()
        loaded_audio_files[file_path] = audio
    else:
        audio = loaded_audio_files[file_path]
    
    return audio[start_sample:start_sample+n_samples]

def find_similar_frames(query_frame, df_source_frames, n, features):
    """
    Find the n most similar frames from a DataFrame of source frames based on given features.
    
    Parameters:
      - query_frame: A numpy array of features for the target frame.
      - df_source_frames: A Pandas DataFrame where each row is a source frame with its features.
      - n: Number of similar frames to retrieve.
      - features: List of feature names to use for similarity calculation.
    
    Returns:
      - A list of Pandas Series corresponding to the n most similar source frames.
    """
    query_frame = query_frame.reshape(1, -1)
    nbrs = NearestNeighbors(n_neighbors=n, algorithm='ball_tree').fit(df_source_frames[features].values)
    distances, indices = nbrs.kneighbors(query_frame)
    return [df_source_frames.iloc[k] for k in indices[0]]

# def choose_frame_from_source_collection(target_frame, df_source_frames):
#     """
#     Choose one frame from the source collection to replace a target frame.
#     Uses MFCC features for similarity and introduces a bit of randomization.
    
#     Parameters:
#       - target_frame: A dictionary or Pandas Series containing features of the target frame.
#       - df_source_frames: A Pandas DataFrame with source frame features.
    
#     Returns:
#       - A Pandas Series representing the chosen source frame.
#     """
#     n_neighbors = 10
#     # Use MFCC coefficients as similarity features; adjust as needed
#     similarity_features = [f'mfcc_{i}' for i in range(13)]
    
#     query_features = target_frame[similarity_features].values
#     similar_frames = find_similar_frames(query_features, df_source_frames, n_neighbors, similarity_features)
    
#     # Randomly choose one frame among the top similar frames for variety
#     chosen_frame = random.choice(similar_frames)
#     return chosen_frame


def choose_frame_from_source_collection(target_frame, df_source_frames, random_factor=0.2):
    """
    Choose one frame from the source collection to replace a target frame.
    Uses MFCC features for similarity and adds additional randomization.
    
    Parameters:
      - target_frame: A dictionary or Pandas Series containing features of the target frame.
      - df_source_frames: A Pandas DataFrame with source frame features.
      - random_factor: A float between 0 and 1 to control randomization strength.
    
    Returns:
      - A Pandas Series representing the chosen source frame.
    """
    n_neighbors = 10
    similarity_features = [f'mfcc_{i}' for i in range(13)]
    query_features = target_frame[similarity_features].values
    similar_frames = find_similar_frames(query_features, df_source_frames, n_neighbors, similarity_features)
    
    # Calculate distances for additional randomization (if desired)
    # Here, we assign a probability inversely proportional to the rank and add some randomness.
    # For simplicity, we randomly choose one among the top n_neighbors weighted by random_factor.
    if random_factor > 0:
        weights = np.linspace(1, 1 - random_factor, num=n_neighbors)
        weights = weights / np.sum(weights)
        chosen_frame = random.choices(similar_frames, weights=weights, k=1)[0]
    else:
        chosen_frame = similar_frames[0]
    return chosen_frame
