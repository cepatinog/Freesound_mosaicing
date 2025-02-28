# Audio Mosaicing: A Modular Approach for Creative Sound Reconstruction 

## Carlos Eduardo Patiño Gómez

**Explore the full project code on GitHub:** [Freesound Mosaicing Repository](https://github.com/cepatinog/Freesound_mosaicing) 

https://github.com/cepatinog/Freesound_mosaicing


## Abstract
This project presents a modular, flexible workflow for creative audio mosaicing. By building a personal library of sound "fonts" from Freesound, analyzing audio files to extract timbral and harmonic features, and reconstructing target audio by replacing its frames with carefully selected source frames, we create a system capable of generating novel sonic textures. This approach has both artistic and practical applications, particularly music arrangements. I particularly find the ideas developed in this project very useful because this week I am developing the arrangements for a piece for violins, bass, piano, and electronics, to be presented at Business Immersion Week. Inspired by AI-generated audio from Suno, this piece incorporates live looping techniques where selected fragments based on tonal characteristics enhance harmonic pad sections, while rhythmic parts benefit from well-matched percussion sounds.

Our research compares different feature sets for similarity matching (MFCCs alone vs. MFCCs combined with loudness) and explores advanced techniques such as beat-synchronized segmentation and tonality-based filtering. Our findings demonstrate that parameter choices—including frame size, feature selection, and synchronization methods—greatly influence the quality and coherence of the reconstructed audio.

## 1. Introduction
Recent advances in computational audio analysis and machine learning have enabled novel methods for creative sound processing. Audio mosaicing is one such technique that reconstructs a target audio signal by replacing segments with matching pieces from a pre-collected sound library. This project was designed to explore audio mosaicing through a modular and hierarchical approach, structured into three main phases:

- **Collection of Sounds:** Building a personal sound library by querying the Freesound API.
- **Audio Analysis:** Extracting key audio features (MFCCs, loudness, and tonality) from both source and target files.
- **Audio Mosaicing:** Reconstructing a target audio file by replacing its frames with similar source frames based on different feature sets.

This method is particularly relevant for my current project because I'm working on a piece that incorporates live looping and real-time manipulation of audio fragments. Carefully selecting audio fragments—such as harmonic pads extracted from tonal features and rhythmic elements from percussive sounds—is crucial. The mosaicing method developed here allows for precise matching based on timbral, dynamic, and tonal characteristics, ensuring seamless integration into the musical texture.

## 2. Methodology
### Project Structure and Modular Design
The project is organized into three primary folders:

- **`data/`**: Contains raw audio files (downloaded previews), processed outputs, and metadata CSV files.
- **`notebooks/`**: Jupyter notebooks for each stage of the project (sound collection, analysis, and mosaicing).
- **`src/`**: Python modules implementing core functionality, including:
  - `config.py`: Centralizes API keys, file paths, and metadata field definitions.
  - `sound_collection.py`: Handles querying the Freesound API, downloading audio previews, and generating metadata records.
  - `analysis.py`: Implements `analyze_sound`, which segments audio (fixed or beat-synchronized) and extracts features such as MFCCs, loudness, and tonality.
  - `mosaicing.py`: Provides functions for loading audio segments, finding similar frames via nearest-neighbor searches, and selecting replacement frames based on various feature sets, including advanced tonality-based filtering.

A `.gitignore` file ensures that large audio files (e.g., those in `data/raw/`) are excluded from version control.

### Sound Collection
The first phase involves creating a custom collection of sound “fonts” by querying Freesound for electronic sounds, percussions, violins, basses, and synthesizers. The `query_freesound` function retrieves sounds that meet specified duration filters, and high-quality previews are downloaded to `data/raw/`. Metadata—including sound ID, name, tags, and local file path—is extracted via `make_metadata_record` and saved to `data/metadata/fonts_collection.csv`.

### Audio Analysis
The analysis phase processes both the source collection and a target audio file. The `analyze_sound` function (in `src/analysis.py`) performs the following:

- **Loading Audio:** Uses Essentia’s `MonoLoader` to read files.
- **Segmentation:** Divides the audio into frames using fixed-size segmentation (e.g., 8192 samples for source, 4096 samples for target) or beat-synchronized segmentation (`sync_with_beats=True`).
- **Feature Extraction:**
  - **Loudness:** Calculated with Essentia’s `Loudness` algorithm and normalized by frame length.
  - **MFCCs:** Extracted using a combination of windowing, spectrum calculation, and MFCC extraction.
  - **Tonality:** Extracted using Essentia’s `KeyExtractor`, including key, scale, and key strength.

Extracted features for every frame are stored in `source_analysis.csv` and `target_analysis.csv`, forming the foundation for mosaicing.

### Audio Mosaicing
In the final stage, the target audio is reconstructed by replacing its frames with similar frames from the source collection. The `src/mosaicing.py` module provides key functions:

- **`get_audio_file_segment`**: Retrieves cached audio segments.
- **`find_similar_frames`**: Uses scikit-learn’s `NearestNeighbors` for similarity matching.
- **`choose_frame_from_source_collection`**: Uses MFCC-based selection with a controlled random factor.
- **`choose_frame_by_tonality`**: Filters source frames by matching the target frame’s tonality before nearest-neighbor matching.
- **`reconstruct_target`**: Iterates over target frames, selects a matching source frame, extracts the corresponding audio segment, and reconstructs the full audio.

## 3. Experiments and Findings
### Feature Set Experiments
Three experiments were conducted:

- **Experiment A (MFCC Only):** Captures spectral envelope but lacks dynamic nuance.
- **Experiment B (MFCC + Loudness):** Adds dynamic information, improving transitions and natural feel.
- **Experiment C (Tonality-Based Matching):** Ensures harmonic coherence by matching key, scale, and key strength.

### Parameter Choices and Impact
- **Frame Size:** 8192 samples for source and 4096 samples for target provided a balance between structure and detail.
- **Randomization:** Controlled variability in frame selection, balancing creativity and consistency.
- **Tonality Filtering:** Improved harmonic compatibility, particularly for harmonic pads.

### Personal Relevance
- **Harmonic Pads:** Ensured tonal consistency, crucial for smooth transitions.
- **Rhythmic Sections:** Percussive elements selected via MFCC-based features provided essential rhythmic drive.

## 4. Conclusion
Through a modular design covering sound collection, analysis, and mosaicing, this project has developed a robust system for creative audio reconstruction. Key takeaways include:

- **Feature selection is crucial:** Including loudness and tonality improves smoothness and harmonic coherence.
- **Parameter tuning matters:** Frame size and randomization significantly impact output quality.
- **Practical application:** The system enhances my live looping arrangement by precisely selecting audio fragments for harmonic and rhythmic sections.

Future work could explore additional features (e.g., spectral centroid, flux) and further refine tonality matching. This project not only provides a powerful tool for creative sound reconstruction but also directly supports my ongoing musical work, merging technical innovation with artistic expression.


**Explore the full project code on GitHub:** [Freesound Mosaicing Repository](https://github.com/cepatinog/Freesound_mosaicing)  