#!/usr/bin/env python3
"""
Script for reading and visualizing motion capture marker data.
Reads TSV files from data folders and creates 3D animation.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pathlib import Path
from typing import Dict, Tuple, List


class MarkerDataReader:
  """Class for reading marker data from TSV files."""
  
  def __init__(self, file_path: str):
    """
    Initialize the reader.
    
    Args:
      file_path: Path to TSV file with marker data
    """
    self.file_path = Path(file_path)
    self.metadata = {}
    self.marker_names = []
    self.simple_names = []  # Simple names like r1, l1
    self.frames_data = None
    
  def read_file(self) -> Dict:
    """
    Reads TSV file and extracts metadata and marker data.
    
    Returns:
      Dictionary with metadata and marker data
    """
    with open(self.file_path, 'r') as f:
      lines = f.readlines()
    
    # Parse metadata (first lines before header line)
    data_start_line = 0
    for i, line in enumerate(lines):
      if line.startswith('Frame\t'):
        # Found the column headers line
        data_start_line = i + 1
        # Extract marker names from header
        self._parse_marker_names(lines[i])
        break
      else:
        # Parse metadata
        self._parse_metadata_line(line)
    
    # Read marker data starting from data_start_line
    self._parse_marker_data(lines[data_start_line:])
    
    # Create simple marker names (l1, l2, r1, r2, etc.)
    self._create_simple_names()
    
    return {
      'metadata': self.metadata,
      'marker_names': self.marker_names,
      'simple_names': self.simple_names,
      'frames': self.frames_data
    }
  
  def _parse_metadata_line(self, line: str):
    """
    Parses a metadata line.
    
    Args:
      line: Metadata line in format "KEY\tVALUE"
    """
    parts = line.strip().split('\t')
    if len(parts) >= 2:
      key = parts[0]
      value = parts[1]
      self.metadata[key] = value
  
  def _parse_marker_names(self, header_line: str):
    """
    Extracts marker names from header line.
    
    Args:
      header_line: Line with column headers
    """
    # Split by tab
    columns = header_line.strip().split('\t')
    
    # Skip "Frame" and "Time", rest are marker coordinates
    # Format: "MarkerName X", "MarkerName Y", "MarkerName Z"
    marker_set = []
    for col in columns[2:]:  # Skip Frame and Time
      # Remove X, Y, Z suffixes
      marker_name = col.rsplit(' ', 1)[0]
      if marker_name not in marker_set:
        marker_set.append(marker_name)
    
    self.marker_names = marker_set
  
  def _parse_marker_data(self, data_lines: List[str]):
    """
    Parses marker data from file lines.
    
    Args:
      data_lines: List of lines with frame data
    """
    num_markers = len(self.marker_names)
    num_frames = len(data_lines)
    
    # Create array to store data: (frames, markers, XYZ coordinates)
    self.frames_data = np.zeros((num_frames, num_markers, 3))
    
    for frame_idx, line in enumerate(data_lines):
      # Split by tab
      values = line.strip().split('\t')
      
      # Skip Frame and Time (first two columns)
      coords = values[2:]
      
      # Fill coordinates for each marker
      for marker_idx in range(num_markers):
        x_idx = marker_idx * 3
        y_idx = marker_idx * 3 + 1
        z_idx = marker_idx * 3 + 2
        
        # Convert strings to numbers
        if x_idx < len(coords) and y_idx < len(coords) and z_idx < len(coords):
          self.frames_data[frame_idx, marker_idx, 0] = float(coords[x_idx])
          self.frames_data[frame_idx, marker_idx, 1] = float(coords[y_idx])
          self.frames_data[frame_idx, marker_idx, 2] = float(coords[z_idx])
  
  def _create_simple_names(self):
    """
    Creates simple names for markers and filters unnecessary ones.
    Determines left/right based on average Y coordinate, then filters
    and renames remaining markers as 1, 2, 3...
    """
    # Calculate average position of each marker across all frames
    mean_positions = np.mean(self.frames_data, axis=0)  # (markers, XYZ)
    
    # Determine center by Y-coordinate
    center_y = np.mean(mean_positions[:, 1])
    
    # Split markers into left (Y < center_y) and right (Y >= center_y)
    left_markers = []
    right_markers = []
    
    for idx in range(len(self.marker_names)):
      marker_y = mean_positions[idx, 1]
      if marker_y < center_y:
        left_markers.append((idx, marker_y))
      else:
        right_markers.append((idx, marker_y))
    
    # Sort by Y-coordinate (from smaller to larger)
    left_markers.sort(key=lambda x: x[1])
    right_markers.sort(key=lambda x: x[1])
    
    # Create temporary dictionary for mapping marker index -> temporary name (l1, r1...)
    temp_name_map = {}
    
    for i, (marker_idx, _) in enumerate(left_markers):
      temp_name_map[marker_idx] = f'l{i+1}'
    
    for i, (marker_idx, _) in enumerate(right_markers):
      temp_name_map[marker_idx] = f'r{i+1}'
    
    # List of markers to exclude
    markers_to_exclude = ['l1', 'l6', 'l5', 'r5', 'r8', 'r2']
    
    # Determine indices of markers to keep
    indices_to_keep = []
    for idx in range(len(self.marker_names)):
      if temp_name_map[idx] not in markers_to_exclude:
        indices_to_keep.append(idx)
    
    # Filter marker data
    self.frames_data = self.frames_data[:, indices_to_keep, :]
    
    # Filter original names
    self.marker_names = [self.marker_names[i] for i in indices_to_keep]
    
    # Create new simple names (just 1, 2, 3...)
    self.simple_names = [str(i+1) for i in range(len(self.marker_names))]


class MarkerAnimator:
  """Class for creating 3D marker animation."""
  
  def __init__(self, frames_data: np.ndarray, marker_names: List[str], 
               simple_names: List[str] = None, title: str = "Marker Animation"):
    """
    Initialize animator.
    
    Args:
      frames_data: Marker data array (frames, markers, XYZ)
      marker_names: List of marker names
      simple_names: List of simple marker names (l1, r1, etc.)
      title: Animation title
    """
    self.frames_data = frames_data
    self.marker_names = marker_names
    self.simple_names = simple_names if simple_names else marker_names
    self.title = title
    self.fig = None
    self.ax = None
    self.scatter = None
    self.labels = []  # Text labels for markers
    
  def setup_plot(self):
    """Sets up 3D plot for animation."""
    # Create figure and 3D axes
    self.fig = plt.figure(figsize=(12, 9))
    self.ax = self.fig.add_subplot(111, projection='3d')
    
    # Calculate axis boundaries (using all frames)
    all_x = self.frames_data[:, :, 0].flatten()
    all_y = self.frames_data[:, :, 1].flatten()
    all_z = self.frames_data[:, :, 2].flatten()
    
    # Set equal scale for all axes
    max_range = np.array([
      all_x.max() - all_x.min(),
      all_y.max() - all_y.min(),
      all_z.max() - all_z.min()
    ]).max() / 2.0
    
    mid_x = (all_x.max() + all_x.min()) * 0.5
    mid_y = (all_y.max() + all_y.min()) * 0.5
    mid_z = (all_z.max() + all_z.min()) * 0.5
    
    self.ax.set_xlim(mid_x - max_range, mid_x + max_range)
    self.ax.set_ylim(mid_y - max_range, mid_y + max_range)
    self.ax.set_zlim(mid_z - max_range, mid_z + max_range)
    
    # Axis labels
    self.ax.set_xlabel('X (mm)')
    self.ax.set_ylabel('Y (mm)')
    self.ax.set_zlabel('Z (mm)')
    self.ax.set_title(self.title)
    
    # Create initial scatter plot (first frame)
    first_frame = self.frames_data[0]
    self.scatter = self.ax.scatter(
      first_frame[:, 0],
      first_frame[:, 1],
      first_frame[:, 2],
      c='red',
      s=100,
      marker='o',
      alpha=0.8,
      edgecolors='black',
      linewidths=1.5
    )
    
    # Add labels for each marker
    self.labels = []
    for i, (x, y, z) in enumerate(first_frame):
      label = self.ax.text(
        x, y, z,
        self.simple_names[i],
        fontsize=10,
        fontweight='bold',
        color='blue',
        ha='center',
        va='bottom'
      )
      self.labels.append(label)
    
    return self.fig, self.ax
  
  def update_frame(self, frame_num: int):
    """
    Updates marker positions for current frame.
    
    Args:
      frame_num: Frame number to display
    """
    # Get data for current frame
    current_frame = self.frames_data[frame_num]
    
    # Update point positions
    self.scatter._offsets3d = (
      current_frame[:, 0],
      current_frame[:, 1],
      current_frame[:, 2]
    )
    
    # Update label positions
    for i, (x, y, z) in enumerate(current_frame):
      self.labels[i].set_position((x, y))
      self.labels[i].set_3d_properties(z, 'z')
    
    # Update title with frame number
    self.ax.set_title(f'{self.title} - Frame {frame_num + 1}/{len(self.frames_data)}')
    
    return [self.scatter] + self.labels
  
  def animate(self, interval: int = 10, skip_frames: int = 1):
    """
    Runs the animation.
    
    Args:
      interval: Interval between frames in milliseconds
      skip_frames: Number of frames to skip (for speed up)
    
    Returns:
      Animation object
    """
    # Set up the plot
    self.setup_plot()
    
    # Create animation
    num_frames = len(self.frames_data)
    frames_to_show = range(0, num_frames, skip_frames)
    
    anim = FuncAnimation(
      self.fig,
      self.update_frame,
      frames=frames_to_show,
      interval=interval,
      blit=False,
      repeat=True
    )
    
    return anim


def main():
  """Main function to run visualization."""
  import argparse
  
  # Parse command line arguments
  parser = argparse.ArgumentParser(
    description='Motion capture marker data visualization'
  )
  parser.add_argument(
    'file',
    nargs='?',
    type=str,
    help='Path to TSV file (if not specified, interactive selection)'
  )
  parser.add_argument(
    '--save',
    type=str,
    help='Save animation to file (e.g.: output.gif or output.mp4)'
  )
  parser.add_argument(
    '--skip-frames',
    type=int,
    default=1,
    help='Skip every N frames for speed up (default: 1)'
  )
  parser.add_argument(
    '--interval',
    type=int,
    default=10,
    help='Interval between frames in ms (default: 10)'
  )
  
  args = parser.parse_args()
  
  # Path to project root directory
  project_root = Path(__file__).parent
  
  # If file specified via argument
  if args.file:
    selected_file = Path(args.file)
    # If relative path, check relative to current directory
    if not selected_file.is_absolute():
      # First check relative to current directory
      if (Path.cwd() / selected_file).exists():
        selected_file = Path.cwd() / selected_file
      else:
        # If not found, try relative to project directory
        selected_file = project_root / selected_file
  else:
    # List of files for visualization
    files_to_visualize = [
      project_root / 'milana' / 'Measurement1.tsv',
      project_root / 'data' / 'Measurement1.tsv',
    ]
    
    # Select file for visualization
    print("Available files for visualization:")
    for idx, file_path in enumerate(files_to_visualize):
      print(f"{idx + 1}. {file_path.relative_to(project_root)}")
    
    # Request user choice
    choice = input("\nSelect file number (or press Enter for first): ").strip()
    
    if choice == "":
      selected_idx = 0
    else:
      try:
        selected_idx = int(choice) - 1
        if selected_idx < 0 or selected_idx >= len(files_to_visualize):
          print("Invalid choice. Using first file.")
          selected_idx = 0
      except ValueError:
        print("Invalid input. Using first file.")
        selected_idx = 0
    
    selected_file = files_to_visualize[selected_idx]
  
  # Check file existence
  if not selected_file.exists():
    print(f"Error: File {selected_file} not found!")
    return
  
  print(f"\nReading file: {selected_file}")
  
  # Read marker data
  reader = MarkerDataReader(selected_file)
  data = reader.read_file()
  
  # Display data information
  print(f"\n{'='*60}")
  print(f"📊 Metadata:")
  print(f"  Number of frames: {data['metadata'].get('NO_OF_FRAMES', 'N/A')}")
  print(f"  Number of markers: {data['metadata'].get('NO_OF_MARKERS', 'N/A')}")
  print(f"  Frequency: {data['metadata'].get('FREQUENCY', 'N/A')} Hz")
  print(f"  Number of cameras: {data['metadata'].get('NO_OF_CAMERAS', 'N/A')}")
  
  print(f"\n🎯 Markers:")
  print(f"  First 5: {', '.join(data['marker_names'][:5])}")
  print(f"  Total markers: {len(data['marker_names'])}")
  print(f"  Data shape: {data['frames'].shape} (frames, markers, XYZ)")
  print(f"{'='*60}")
  
  # Create and run animation
  print("\n🎬 Creating animation...")
  
  animator = MarkerAnimator(
    data['frames'],
    data['marker_names'],
    data['simple_names'],
    title=f"Markers - {selected_file.stem}"
  )
  
  # Animation parameters
  # interval: delay between frames in ms
  # skip_frames: skip frames for speed up
  anim = animator.animate(interval=args.interval, skip_frames=args.skip_frames)
  
  # Save or display animation
  if args.save:
    print(f"\n💾 Saving animation to file: {args.save}")
    print("   (this may take several minutes...)")
    
    # Determine writer based on file extension
    if args.save.endswith('.gif'):
      writer = 'pillow'
    elif args.save.endswith('.mp4'):
      writer = 'ffmpeg'
    else:
      writer = None
    
    try:
      anim.save(args.save, writer=writer, fps=int(1000/args.interval))
      print(f"✅ Animation saved: {args.save}")
    except Exception as e:
      print(f"❌ Error saving: {e}")
      print("   Try installing: sudo apt-get install ffmpeg")
  else:
    print("\n▶️  Animation started. Close window to exit.")
    plt.show()


if __name__ == "__main__":
  main()
