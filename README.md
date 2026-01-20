# Motion Capture Data Visualization

Scripts for visualizing marker data from Qualisys motion capture system.

> 🎯 **Vibe-Code Project**: This entire project, including all visualization scripts and documentation, was created using [Cursor](https://cursor.sh/) AI-assisted development.

## Demo

![Combined Visualization](combined.gif)

*Real-time 3D marker animation synchronized with joint angle plots. The graphs build progressively as the animation plays.*

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
# Fast animation (all frames, 1ms between frames)
python3 visualize_markers.py data/Measurement1.tsv --interval 1

# Slow animation (all frames, 50ms between frames)
python3 visualize_markers.py data/Measurement1.tsv --interval 50

# Skip frames (faster but less smooth)
python3 visualize_markers.py data/Measurement1.tsv --skip-frames 5

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

### Save Angles to JSON

```bash
# Process both measurements
python3 save_angles.py

# Process specific measurement
python3 save_angles.py --measurement 1
python3 save_angles.py --measurement 2

# Specify custom output directory
python3 save_angles.py --output-dir /path/to/output
```

**Output:**
- JSON files saved to `data/calculated_angles/`
- Files: `Measurement1_calculated_angles.json`, `Measurement2_calculated_angles.json`

**JSON structure:**
- `metadata`: Frequency, number of frames, source metadata
- `angles`: Arrays of angle values for each frame (qr1, qr2, qr3, ql1, ql2, ql3)
- `statistics`: Mean, standard deviation, min, max for each angle

### Combined Visualization (3D + Angles)

```bash
# Display combined view (default speed)
python3 visualize_with_angles.py data/Measurement1.tsv

# Speed up animation (all frames, fast playback)
python3 visualize_with_angles.py data/Measurement1.tsv --interval 1

# Speed up animation (skip frames, faster but less smooth)
python3 visualize_with_angles.py data/Measurement1.tsv --skip-frames 5

# Save animation
python3 visualize_with_angles.py data/Measurement1.tsv --save combined.gif
```

**Speed control:**
- `--interval 1` - Very fast (all frames, 1ms between frames) ⚡
- `--interval 5` - Fast (all frames, 5ms between frames)
- `--interval 10` - Normal speed (default)
- `--interval 30` - Slow (all frames, 30ms between frames)
- `--skip-frames N` - Skip every N frames (less smooth)

**Display:**
- Left side: 3D marker animation
- Right side: Three angle plots that build progressively
- Real-time synchronization: graphs "follow" the 3D animation
- Angles are plotted point-by-point as animation progresses

## Data

- **Folder data/** - marker data files
- **Format:** TSV (tab-separated values)
- **Frequency:** 100 Hz
- **Frames:** 2000 (20 seconds recording)

### Files:
- **Measurement1.tsv**: 9 markers (filtered from 15)
- **Measurement2.tsv**: 10 markers (filtered from 16)

### Data Structure:

```
data/
├── Measurement1.tsv          # Raw marker data
├── Measurement2.tsv          # Raw marker data
├── calculated_angles/        # Calculated angles (JSON)
│   ├── Measurement1_calculated_angles.json
│   └── Measurement2_calculated_angles.json
└── angle_data/              # Reference angle data (TSV)
    ├── mes1/                # Measurement 1 reference angles
    └── mes2/                # Measurement 2 reference angles
```

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
