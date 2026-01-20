# Motion Capture Data Visualization

Scripts for visualizing marker data from Qualisys motion capture system.

> 🎯 **Vibe-Code Project**: This entire project, including all visualization scripts and documentation, was created using [Cursor](https://cursor.sh/) AI-assisted development.

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
- 9 marker points with anatomical labels (ra, rh, la, lk, etc.)
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

### Angle Calculation

```bash
# Display angle plots
python3 calculate_angles.py data/Measurement1.tsv

# Save plots to file
python3 calculate_angles.py data/Measurement1.tsv --save angles.png
```

**Calculated angles:**

- **q1** (Right/Left): Angle between knee-ankle segment and XY plane
- **q2** (Right/Left): Knee joint angle (ankle-knee-hip)
- **q3** (Right/Left): Hip joint angle (knee-hip-shoulder)

**Output:**
- Three plots comparing right vs left side angles
- Statistical summary (mean, std, range)

## Data

- **Folder data/** - marker data files
- **Format:** TSV (tab-separated values)
- **Frequency:** 100 Hz
- **Frames:** 2000 (20 seconds recording)

### Files:
- **Measurement1.tsv**: 9 markers (filtered from 15)
- **Measurement2.tsv**: 10 markers (filtered from 16)

## Marker Naming System

Markers use anatomical abbreviations:

- **ra** - Right Ankle
- **rk** - Right Knee
- **rh** - Right Hip
- **rs** - Right Shoulder
- **ls** - Left Shoulder
- **lh** - Left Hip
- **lk** - Left Knee
- **la** - Left Ankle
- **spine** - Spine marker
- **mass** - Center of mass marker

### Measurement1.tsv
9 markers (filtered from 15): **ra, rh, spine, la, lk, rs, ls, rk, lh**

Excluded markers: l1, l5, l6, r2, r5, r8 (determined automatically by positions).

### Measurement2.tsv
10 markers (filtered from 16): **spine, lk, mass, rh, ls, rs, ra, la, rk, lh**

Excluded markers at positions: 2, 4, 5, 7, 11, 12 (from original 16 markers).

**Note:** Marker naming is synchronized between datasets by comparing spatial coordinates. All markers have anatomical labels.

## Help

For any script:
```bash
python3 visualize_markers.py --help
```

---

## About

**Vibe-Code Project** 🚀

This project demonstrates the power of AI-assisted development. All visualization scripts, data processing logic, and documentation were created entirely using **Cursor AI** - from the initial concept to the final implementation.

### Technologies Used:
- **Python 3** - Core programming language
- **NumPy** - Numerical computations
- **Matplotlib** - 3D visualization and animation
- **Cursor AI** - AI-assisted development and code generation

### Development Approach:
- Natural language requirements → Working code
- Automated refactoring and optimization
- Real-time code documentation
- Intelligent error fixing

This showcases how modern AI tools can accelerate the development process while maintaining code quality and best practices.
