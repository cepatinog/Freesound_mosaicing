"""
Module for analyzing audio files.
This module uses Essentia to load audio files and extract features such as loudness and MFCC coefficients
from audio frames.
"""

import essentia
import essentia.standard as estd

def analyze_sound(audio_path, frame_size=None, audio_id=None, sync_with_beats=False):
    """
    Analyze an audio file and return a list of dictionaries, each corresponding to a frame
    of the audio with extracted features.
    
    Parameters:
      - audio_path: Path to the audio file.
      - frame_size: The number of samples per frame. If None, the entire audio is analyzed as one frame.
      - audio_id: A custom identifier for the audio; useful for linking analysis results back to a source.
      - sync_with_beats: If True, the audio is segmented according to beat positions instead of equal intervals.
      
    Returns:
      - analysis_output: A list of dictionaries containing metadata and extracted features for each frame.
    """
    analysis_output = []
    
    # Load the audio file using Essentia's MonoLoader
    loader = estd.MonoLoader(filename=audio_path)
    audio = loader()
    
    # If no frame_size is provided, analyze the entire audio as one frame
    if frame_size is None:
        frame_size = len(audio)
    
    # Ensure the frame size is even to avoid potential issues
    if frame_size % 2 != 0:
        frame_size += 1
    
    # Determine segmentation method: fixed-size segmentation or beat-synchronized segmentation
    if sync_with_beats:
        # Use Essentia's BeatTrackerDegara to detect beat positions
        beat_tracker_algo = estd.BeatTrackerDegara()
        beat_positions = beat_tracker_algo(audio)
        # Convert beat positions from seconds to sample indices (assuming 44100 Hz sample rate)
        beat_positions = [int(round(position * 44100)) for position in beat_positions]
        # Create frame intervals from consecutive beat positions
        frame_start_end_samples = zip(beat_positions[:-1], beat_positions[1:])
    else:
        # Fixed segmentation: split audio into frames of 'frame_size'
        frame_start_samples = range(0, len(audio), frame_size)
        frame_start_end_samples = zip(frame_start_samples[:-1], frame_start_samples[1:])
    
    # Process each frame to extract features
    for count, (fstart, fend) in enumerate(frame_start_end_samples):
        frame = audio[fstart:fend]
        # Create a dictionary to store analysis results for this frame
        frame_output = {
            'freesound_id': audio_id,
            'id': f'{audio_id}_f{count}',
            'path': audio_path,
            'start_sample': fstart,
            'end_sample': fend,
        }
        
        # Compute loudness using Essentia's Loudness algorithm and normalize by frame length
        loudness_algo = estd.Loudness()
        loudness = loudness_algo(frame)
        frame_output['loudness'] = loudness / len(frame)
        
        # Extract MFCC coefficients:
        w_algo = estd.Windowing(type='hann')
        spectrum_algo = estd.Spectrum()
        mfcc_algo = estd.MFCC()
        spec = spectrum_algo(w_algo(frame))
        _, mfcc_coeffs = mfcc_algo(spec)
        for j, coeff in enumerate(mfcc_coeffs):
            frame_output[f'mfcc_{j}'] = coeff
        

    # Extract other features here and add to 'frame_output' dictionary

        # Extract tonality information using Essentia's KeyExtractor
        key_extractor = estd.KeyExtractor()
        key, scale, key_strength = key_extractor(frame)
        frame_output['key'] = key          # e.g., 0=C, 1=C#/Db, etc.
        frame_output['scale'] = scale      # 'major' or 'minor'
        frame_output['key_strength'] = key_strength


        analysis_output.append(frame_output)

    return analysis_output
