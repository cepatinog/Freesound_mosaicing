# Audio Mosaicing for Creative Sound Reconstruction 

## Overview
This project presents a modular workflow for creative audio mosaicing, enabling the reconstruction of audio files by replacing segments with matching frames from a curated sound collection. The system facilitates:

- **Sound Collection:** Querying Freesound to build a diverse library of sound "fonts."
- **Audio Analysis:** Extracting timbral and harmonic features from source and target audio.
- **Audio Mosaicing:** Reconstructing target audio using similarity-based selection of source fragments.

This approach is particularly useful for live looping and creative arrangements, such as my current project—an arrangement for violins, bass, piano, and electronics for Business Immersion Week, inspired by AI-generated audio from Suno.

## Features
### Sound Collection
- Query the **Freesound API** to gather a collection of electronic sounds, percussions, violins, basses, and synthesizers.
- Download high-quality previews and store metadata in **CSV format** for easy access.

### Audio Analysis
- Segment audio files into frames (fixed-length or beat-synchronized).
- Extract key features:
  - **MFCC coefficients** (for spectral envelope characterization)
  - **Loudness** (for dynamic consistency)
  - **Tonality** (key, scale, key strength for harmonic matching)

### Audio Mosaicing
- Replace target audio frames with similar source frames using different feature sets:
  - **MFCC only** (basic spectral matching)
  - **MFCC + Loudness** (improves transition smoothness)
  - **Tonality-based matching** (ensures harmonic consistency)
- Fine-tune frame selection strategies, including randomization factors for creative variation.

### Modularity
- Organized into **dedicated modules**, making the system flexible and extensible for future improvements.

## Project Structure
```
FREESOUND/
│
├── data/
│   ├── metadata/
│   │   ├── fonts_collection.csv        # Metadata for the sound collection
│   │   ├── source_analysis.csv         # Analysis results for source files
│   │   └── target_analysis.csv         # Analysis results for the target file
│   ├── processed/                      # Processed audio outputs (e.g., reconstructed audio)
│   └── raw/                            # Downloaded audio previews
│
├── notebooks/
│   ├── 1_source_collection.ipynb       # Build your collection of sound fonts
│   ├── 2_analysis.ipynb                # Analyze source and target audio files
│   ├── 3_mosaicing.ipynb               # Reconstruct target audio using mosaicing
│
├── src/
│   ├── __init__.py                     # Package initializer
│   ├── config.py                       # Configuration settings (API keys, paths, etc.)
│   ├── sound_collection.py             # Functions for querying Freesound and building the sound collection
│   ├── analysis.py                      # Audio analysis functions (feature extraction)
│   ├── mosaicing.py                     # Audio mosaicing functions (frame selection & reconstruction)
│
├── .gitignore                          # Excludes large audio files from version control
├── environment.yml                     # Conda environment specification
├── requirements.txt                    # Python dependencies
├── README.md                           # Project documentation
└── test_modules.py                      # Test scripts for modules
```

## Installation
### Clone the Repository
```bash
git clone https://github.com/cepatinog/Freesound_mosaicing
cd freesound
```
### Create and Activate a Virtual Environment
#### Using Conda
```bash
conda env create -f environment.yml
conda activate freesound
```
#### Using venv and requirements.txt
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
### Set Up Your Freesound API Key
Edit `src/config.py` and replace the placeholder API key:
```python
FREESOUND_API_KEY = 'YOUR_ACTUAL_API_KEY'
```
### Ensure Folder Structure
Confirm that directories specified in `src/config.py` (e.g., `data/raw`, `data/metadata`) exist. The notebooks include code to create them if necessary.

## Usage
### 1. Building the Sound Collection
- Open `notebooks/1_source_collection.ipynb`
- Run all cells to query Freesound, download audio previews, and generate the metadata CSV file.

### 2. Analyzing Audio Files
- Open `notebooks/2_analysis.ipynb`
- Extract MFCCs, loudness, and tonality for both source and target files.
- Save results in `data/metadata`.

### 3. Performing Audio Mosaicing
- Open `notebooks/3_mosaicing.ipynb`
- Experiment with different feature sets:
  - **MFCC only**
  - **MFCC + Loudness**
  - **Tonality-based matching**
- Save the reconstructed audio in `data/processed`.

### 4. Listening to Results
- The notebooks generate mixes (original + mosaiced audio) for evaluation.
- Saved as MP3 files for lightweight playback.

## Experiments and Findings
This project is particularly valuable for my arrangement for violins, bass, piano, and electronics at Business Immersion Week. Inspired by Suno’s AI-generated audio, this piece explores **live looping techniques**, benefiting from targeted audio fragment selection:

### Harmonic Pads
- **Tonality-based matching** ensures a consistent key and scale across replacement frames.

### Rhythmic Sections
- **Percussive elements** selected based on **MFCC-based matching** provide a strong rhythmic foundation.

### Key Findings
- **Including loudness** in feature sets improves transition smoothness.
- **Tonality filtering** enhances harmonic coherence but reduces the pool of available source frames.
- **Frame size selection matters:**
  - **8192 samples** for source ensures structural integrity.
  - **4096 samples** for target captures finer details.
