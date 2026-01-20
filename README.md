# Motion Capture Data Visualization

Scripts for visualizing marker data from Qualisys motion capture system.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### 3D Animation Viewer

```bash
python3 visualize_markers.py data/Measurement1.tsv
```

**Display:**
- 9 marker points labeled 1 to 9
- 3D animation of movement
- Labels move with markers

**Parameters:**

```bash
# Speed up animation (show every 5th frame)
python3 visualize_markers.py data/Measurement1.tsv --skip-frames 5

# Slow down animation (50 ms interval between frames)
python3 visualize_markers.py data/Measurement1.tsv --interval 50

# Save as GIF
python3 visualize_markers.py data/Measurement1.tsv --save animation.gif

# Save as MP4 (requires ffmpeg)
python3 visualize_markers.py data/Measurement1.tsv --save animation.mp4
```

### Static Plots

```bash
# Display plots
python3 plot_markers_static.py data/Measurement1.tsv

# Save to files
python3 plot_markers_static.py data/Measurement1.tsv \
  --save-trajectories trajectories.png \
  --save-projections projections.png

# Show specific frame
python3 plot_markers_static.py data/Measurement1.tsv --frame 500
```

**Output:**
- 3D trajectories of all markers
- 2D projections (XY, XZ, YZ)

### Data Verification

```bash
python3 test_read_data.py data/Measurement1.tsv
```

Displays marker information, metadata and statistics.

## Data

- **Folder data/** - marker data files
- **Format:** TSV (tab-separated values)
- **Frequency:** 100 Hz
- **Markers:** 9 (automatically filtered from 15)
- **Frames:** 2000 (20 seconds recording)

## Numbering System

Markers are automatically filtered and numbered as **1, 2, 3, 4, 5, 6, 7, 8, 9**.

Excluded markers: l1, l5, l6, r2, r5, r8 (determined automatically by positions).

## Help

For any script:
```bash
python3 visualize_markers.py --help
```
