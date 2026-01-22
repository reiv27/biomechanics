#!/usr/bin/env python3
"""
Script for calculating and visualizing joint angles from motion capture data.
Calculates angles for right and left body sides.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from visualize_markers import MarkerDataReader
import argparse


def angle_with_xy_plane(vector):
  """
  Calculate angle between a vector and XY plane.
  
  Args:
    vector: 3D vector (numpy array)
  
  Returns:
    Angle in degrees
  """
  xy_projection = np.array([vector[0], vector[1], 0])
  
  if np.linalg.norm(vector) == 0 or np.linalg.norm(xy_projection) == 0:
    return 0.0
  
  cos_angle = np.dot(vector, xy_projection) / (np.linalg.norm(vector) * np.linalg.norm(xy_projection))
  cos_angle = np.clip(cos_angle, -1.0, 1.0)
  angle = np.arccos(cos_angle)
  
  return np.degrees(angle)


def angle_between_vectors(v1, v2):
  """
  Calculate angle between two vectors.
  
  Args:
    v1: First 3D vector
    v2: Second 3D vector
  
  Returns:
    Angle in degrees
  """
  if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0:
    return 0.0
  
  cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
  cos_angle = np.clip(cos_angle, -1.0, 1.0)
  angle = np.arccos(cos_angle)
  
  return np.degrees(angle)


def calculate_angles(frames_data, marker_names):
  """
  Calculate joint angles for all frames.
  
  Args:
    frames_data: Array of marker positions (frames, markers, XYZ)
    marker_names: List of marker names
  
  Returns:
    Dictionary with calculated angles for each frame
  """
  num_frames = len(frames_data)
  
  # Create index mapping for marker names
  marker_indices = {name: i for i, name in enumerate(marker_names)}
  
  # Initialize angle arrays
  angles = {
    'qr1': np.zeros(num_frames),
    'qr2': np.zeros(num_frames),
    'qr3': np.zeros(num_frames),
    'ql1': np.zeros(num_frames),
    'ql2': np.zeros(num_frames),
    'ql3': np.zeros(num_frames),
  }
  
  # Check if all required markers are present
  required_right = ['ra', 'rk', 'rh', 'rs']
  required_left = ['la', 'lk', 'lh', 'ls']
  
  has_right = all(m in marker_indices for m in required_right)
  has_left = all(m in marker_indices for m in required_left)
  
  if not has_right:
    print(f"Warning: Missing right side markers. Available: {marker_names}")
  if not has_left:
    print(f"Warning: Missing left side markers. Available: {marker_names}")
  
  # Calculate angles for each frame
  for frame_idx in range(num_frames):
    frame = frames_data[frame_idx]
    
    # Right side angles
    if has_right:
      ra = frame[marker_indices['ra']]
      rk = frame[marker_indices['rk']]
      rh = frame[marker_indices['rh']]
      rs = frame[marker_indices['rs']]
      
      # qr1: angle between rk->ra and XY plane
      vec_rk_ra = ra - rk
      angles['qr1'][frame_idx] = angle_with_xy_plane(vec_rk_ra)
      
      # qr2: angle between ra->rk and rh->rk
      vec_ra_rk = rk - ra
      vec_rh_rk = rk - rh
      angles['qr2'][frame_idx] = 180.0 - angle_between_vectors(vec_ra_rk, vec_rh_rk)
      
      # qr3: angle between rk->rh and rs->rh
      vec_rk_rh = rh - rk
      vec_rs_rh = rh - rs
      angles['qr3'][frame_idx] = 180.0 - angle_between_vectors(vec_rk_rh, vec_rs_rh)
    
    # Left side angles
    if has_left:
      la = frame[marker_indices['la']]
      lk = frame[marker_indices['lk']]
      lh = frame[marker_indices['lh']]
      ls = frame[marker_indices['ls']]
      
      # ql1: angle between lk->la and XY plane
      vec_lk_la = la - lk
      angles['ql1'][frame_idx] = angle_with_xy_plane(vec_lk_la)
      
      # ql2: angle between la->lk and lh->lk
      vec_la_lk = lk - la
      vec_lh_lk = lk - lh
      angles['ql2'][frame_idx] = 180.0 - angle_between_vectors(vec_la_lk, vec_lh_lk)
      
      # ql3: angle between lk->lh and ls->lh
      vec_lk_lh = lh - lk
      vec_ls_lh = lh - ls
      angles['ql3'][frame_idx] = 180.0 - angle_between_vectors(vec_lk_lh, vec_ls_lh)
  
  return angles


def plot_angles(angles, frequency=100, save_path=None, start_frame=None, end_frame=None):
  """
  Plot calculated angles.
  
  Args:
    angles: Dictionary with angle arrays
    frequency: Sampling frequency in Hz
    save_path: Optional path to save the plot
    start_frame: Start frame index (0-based, inclusive). If None, start from beginning.
    end_frame: End frame index (0-based, exclusive). If None, end at last frame.
  """
  num_frames = len(angles['qr1'])
  
  # Determine frame range for plotting
  if start_frame is not None or end_frame is not None:
    start = start_frame if start_frame is not None else 0
    end = end_frame if end_frame is not None else num_frames
    start = max(0, min(start, num_frames))
    end = max(start, min(end, num_frames))
    
    # Filter angles for plotting
    plot_angles = {
      'qr1': angles['qr1'][start:end],
      'qr2': angles['qr2'][start:end],
      'qr3': angles['qr3'][start:end],
      'ql1': angles['ql1'][start:end],
      'ql2': angles['ql2'][start:end],
      'ql3': angles['ql3'][start:end],
    }
    plot_frames = end - start
    time = np.arange(plot_frames) / frequency
    range_info = f' (frames {start}-{end})'
  else:
    plot_angles = angles
    time = np.arange(num_frames) / frequency
    range_info = ''
  
  # Create figure with 3 subplots
  fig, axes = plt.subplots(3, 1, figsize=(14, 10))
  fig.suptitle(f'Joint Angles Comparison (Right vs Left){range_info}', fontsize=16, fontweight='bold')
  
  # Plot qr1 and ql1
  axes[0].plot(time, plot_angles['qr1'], 'b-', linewidth=2, label='qr1 (Right)', alpha=0.8)
  axes[0].plot(time, plot_angles['ql1'], 'r-', linewidth=2, label='ql1 (Left)', alpha=0.8)
  axes[0].set_ylabel('Angle (degrees)', fontsize=12)
  axes[0].set_title('Q1: Angle between knee-ankle and XY plane', fontsize=13, fontweight='bold')
  axes[0].legend(loc='upper right', fontsize=11)
  axes[0].grid(True, alpha=0.3)
  
  # Plot qr2 and ql2
  axes[1].plot(time, plot_angles['qr2'], 'b-', linewidth=2, label='qr2 (Right)', alpha=0.8)
  axes[1].plot(time, plot_angles['ql2'], 'r-', linewidth=2, label='ql2 (Left)', alpha=0.8)
  axes[1].set_ylabel('Angle (degrees)', fontsize=12)
  axes[1].set_title('Q2: Angle at knee joint (ankle-knee-hip)', fontsize=13, fontweight='bold')
  axes[1].legend(loc='upper right', fontsize=11)
  axes[1].grid(True, alpha=0.3)
  
  # Plot qr3 and ql3
  axes[2].plot(time, plot_angles['qr3'], 'b-', linewidth=2, label='qr3 (Right)', alpha=0.8)
  axes[2].plot(time, plot_angles['ql3'], 'r-', linewidth=2, label='ql3 (Left)', alpha=0.8)
  axes[2].set_xlabel('Time (seconds)', fontsize=12)
  axes[2].set_ylabel('Angle (degrees)', fontsize=12)
  axes[2].set_title('Q3: Angle at hip joint (knee-hip-shoulder)', fontsize=13, fontweight='bold')
  axes[2].legend(loc='upper right', fontsize=11)
  axes[2].grid(True, alpha=0.3)
  
  plt.tight_layout()
  
  if save_path:
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"✅ Plot saved to: {save_path}")
  else:
    plt.show()


def main():
  """Main function."""
  parser = argparse.ArgumentParser(
    description='Calculate and visualize joint angles from motion capture data'
  )
  parser.add_argument(
    'file',
    type=str,
    help='Path to TSV file with marker data'
  )
  parser.add_argument(
    '--save',
    type=str,
    help='Save plot to file (e.g., angles.png)'
  )
  parser.add_argument(
    '--from',
    type=int,
    dest='start_frame',
    metavar='FRAME',
    help='Start frame index (0-based, inclusive). If not specified, start from beginning.'
  )
  parser.add_argument(
    '--to',
    type=int,
    dest='end_frame',
    metavar='FRAME',
    help='End frame index (0-based, exclusive). If not specified, end at last frame.'
  )
  
  args = parser.parse_args()
  
  # Read marker data
  file_path = Path(args.file)
  if not file_path.exists():
    print(f"❌ Error: File {file_path} not found!")
    return
  
  print(f"📂 Reading file: {file_path}")
  
  reader = MarkerDataReader(file_path)
  data = reader.read_file()
  
  print(f"✅ Loaded {len(data['frames'])} frames with {len(data['marker_names'])} markers")
  print(f"   Markers: {', '.join(data['simple_names'])}")
  
  # Calculate angles
  print("\n📐 Calculating joint angles...")
  angles = calculate_angles(data['frames'], data['simple_names'])
  
  # Print statistics
  print("\n📊 Angle Statistics:")
  print(f"\n  Right side:")
  print(f"    qr1: {angles['qr1'].mean():.1f}° ± {angles['qr1'].std():.1f}° (range: {angles['qr1'].min():.1f}° - {angles['qr1'].max():.1f}°)")
  print(f"    qr2: {angles['qr2'].mean():.1f}° ± {angles['qr2'].std():.1f}° (range: {angles['qr2'].min():.1f}° - {angles['qr2'].max():.1f}°)")
  print(f"    qr3: {angles['qr3'].mean():.1f}° ± {angles['qr3'].std():.1f}° (range: {angles['qr3'].min():.1f}° - {angles['qr3'].max():.1f}°)")
  
  print(f"\n  Left side:")
  print(f"    ql1: {angles['ql1'].mean():.1f}° ± {angles['ql1'].std():.1f}° (range: {angles['ql1'].min():.1f}° - {angles['ql1'].max():.1f}°)")
  print(f"    ql2: {angles['ql2'].mean():.1f}° ± {angles['ql2'].std():.1f}° (range: {angles['ql2'].min():.1f}° - {angles['ql2'].max():.1f}°)")
  print(f"    ql3: {angles['ql3'].mean():.1f}° ± {angles['ql3'].std():.1f}° (range: {angles['ql3'].min():.1f}° - {angles['ql3'].max():.1f}°)")
  
  # Get frequency from metadata
  frequency = float(data['metadata'].get('FREQUENCY', 100))
  
  # Plot angles
  print("\n📈 Creating plots...")
  if args.start_frame is not None or args.end_frame is not None:
    num_frames = len(angles['qr1'])
    start = args.start_frame if args.start_frame is not None else 0
    end = args.end_frame if args.end_frame is not None else num_frames
    print(f"   Showing frames {start} to {end} (total: {num_frames})")
  
  plot_angles(
    angles, 
    frequency=frequency, 
    save_path=args.save,
    start_frame=args.start_frame,
    end_frame=args.end_frame
  )
  
  print("\n✅ Done!")


if __name__ == "__main__":
  main()
