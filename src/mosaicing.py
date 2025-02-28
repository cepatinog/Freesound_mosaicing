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

def choose_frame_by_tonality(target_frame, df_source_frames, tolerance=0.1, n_neighbors=10):
    """
    Choose a source frame that matches the tonality of the target frame.
    
    The function first filters source frames to only include those with the same key and scale.
    Optionally, it further filters by key_strength if the difference is within the given tolerance.
    Then, among the filtered frames, it uses nearest neighbors on MFCC features to select a similar frame.
    
    Parameters:
      - target_frame: A Series from the target analysis DataFrame that must include 'key', 'scale', and 'key_strength'.
      - df_source_frames: The source analysis DataFrame.
      - tolerance: Acceptable difference in key_strength between target and source frames.
      - n_neighbors: Number of neighbors to consider for the nearest-neighbors search.
    
    Returns:
      - A Series representing the chosen source frame.
    """
    # Filter the source frames to those matching the key and scale of the target frame
    filtered = df_source_frames[(df_source_frames['key'] == target_frame['key']) &
                                  (df_source_frames['scale'] == target_frame['scale'])]
    
    # Optionally, filter based on key_strength difference
    if 'key_strength' in target_frame and 'key_strength' in df_source_frames.columns:
        ks_target = target_frame['key_strength']
        filtered = filtered[abs(filtered['key_strength'] - ks_target) < tolerance]
    
    # If filtering yields too few frames, fallback to using the full source set
    if len(filtered) < n_neighbors:
        filtered = df_source_frames
    
    # Use MFCC features for similarity matching
    similarity_features = [f'mfcc_{i}' for i in range(13)]
    query_vector = target_frame[similarity_features].values.reshape(1, -1)
    
    from sklearn.neighbors import NearestNeighbors
    nbrs = NearestNeighbors(n_neighbors=n_neighbors, algorithm='ball_tree').fit(filtered[similarity_features].values)
    distances, indices = nbrs.kneighbors(query_vector)
    similar_frames = [filtered.iloc[k] for k in indices[0]]
    
    # Randomly select one among the similar frames for creative variation
    chosen_frame = random.choice(similar_frames)
    return chosen_frame


def reconstruct_target(target_df, df_source, similarity_features, use_tonality=False, tolerance=0.1):
    """
    Reconstruct the target audio by replacing each frame with a similar frame
    from the source analysis DataFrame, based on the given similarity features.
    If use_tonality is True, the function filters source frames to only consider those 
    matching the target frame's tonality (i.e., key, scale, and key_strength within tolerance)
    before performing a nearest-neighbor search.
    
    Parameters:
      - target_df: Pandas DataFrame containing target audio frame analyses.
      - df_source: Pandas DataFrame containing source audio frame analyses.
      - similarity_features: List of feature names to use for similarity matching.
      - use_tonality: Boolean flag. If True, filter by tonality.
      - tolerance: Tolerance for key_strength differences when filtering by tonality.
      
    Returns:
      - generated_audio: A numpy array containing the reconstructed audio.
      - used_ids: A list of source Freesound IDs used in the reconstruction.
    """
    # Load the target audio from the first frame's path (assumes all frames come from the same file)
    target_sound_path = target_df.iloc[0]['path']
    target_audio = estd.MonoLoader(filename=target_sound_path)()
    total_length = len(target_audio)
    
    generated_audio = np.zeros(total_length)
    used_ids = []
    
    for idx, target_frame in target_df.iterrows():
        # Choose a source frame using tonality matching if enabled
        if use_tonality:
            chosen_frame = choose_frame_by_tonality(target_frame, df_source, tolerance=tolerance, n_neighbors=10)
        else:
            chosen_frame = choose_frame_from_source_collection(target_frame, df_source, random_factor=0.2)
        
        used_ids.append(chosen_frame['freesound_id'])
        
        # Determine the number of samples in this target frame
        n_samples = target_frame['end_sample'] - target_frame['start_sample']
        # Extract the corresponding audio segment from the chosen source frame
        source_audio_segment = get_audio_file_segment(chosen_frame['path'], chosen_frame['start_sample'], n_samples)
        start_idx = target_frame['start_sample']
        generated_audio[start_idx:start_idx + len(source_audio_segment)] = source_audio_segment
        
    return generated_audio, used_ids
