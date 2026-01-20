#!/usr/bin/env python3
"""
Script for creating static plots of marker trajectories.
Useful for quick data analysis without running full animation.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from visualize_markers import MarkerDataReader
import argparse


def plot_marker_trajectories(frames_data, marker_names, simple_names=None, title="Marker Trajectories"):
  """
  Creates 3D plot of all marker trajectories.
  
  Args:
    frames_data: Data array (frames, markers, XYZ)
    marker_names: List of marker names
    simple_names: List of simple names (l1, r1, etc.)
    title: Plot title
  """
  if simple_names is None:
    simple_names = marker_names
  # Create figure with 3D plot
  fig = plt.figure(figsize=(14, 10))
  ax = fig.add_subplot(111, projection='3d')
  
  # Generate colors for each marker
  colors = plt.cm.rainbow(np.linspace(0, 1, len(marker_names)))
  
  # Draw trajectory for each marker
  for marker_idx, (simple_name, color) in enumerate(zip(simple_names, colors)):
    # Extract marker trajectory (all frames)
    trajectory = frames_data[:, marker_idx, :]
    
    # Draw trajectory line
    ax.plot(
      trajectory[:, 0],
      trajectory[:, 1],
      trajectory[:, 2],
      color=color,
      alpha=0.6,
      linewidth=2,
      label=simple_name
    )
    
    # Mark initial position with label
    ax.scatter(
      trajectory[0, 0],
      trajectory[0, 1],
      trajectory[0, 2],
      color=color,
      s=150,
      marker='o',
      edgecolors='black',
      linewidths=2
    )
    
    # Add label near initial position
    ax.text(
      trajectory[0, 0],
      trajectory[0, 1],
      trajectory[0, 2],
      simple_name,
      fontsize=10,
      fontweight='bold',
      color='black',
      ha='center',
      va='bottom'
    )
  
  # Configure axes
  ax.set_xlabel('X (mm)')
  ax.set_ylabel('Y (mm)')
  ax.set_zlabel('Z (mm)')
  ax.set_title(title)
  
  # Add legend (only first 8 markers to avoid clutter)
  if len(marker_names) <= 8:
    ax.legend(loc='upper right', fontsize=8)
  
  # Set equal scale for all axes
  max_range = np.array([
    frames_data[:, :, 0].max() - frames_data[:, :, 0].min(),
    frames_data[:, :, 1].max() - frames_data[:, :, 1].min(),
    frames_data[:, :, 2].max() - frames_data[:, :, 2].min()
  ]).max() / 2.0
  
  mid_x = (frames_data[:, :, 0].max() + frames_data[:, :, 0].min()) * 0.5
  mid_y = (frames_data[:, :, 1].max() + frames_data[:, :, 1].min()) * 0.5
  mid_z = (frames_data[:, :, 2].max() + frames_data[:, :, 2].min()) * 0.5
  
  ax.set_xlim(mid_x - max_range, mid_x + max_range)
  ax.set_ylim(mid_y - max_range, mid_y + max_range)
  ax.set_zlim(mid_z - max_range, mid_z + max_range)
  
  return fig


def plot_marker_positions_2d(frames_data, marker_names, simple_names=None, frame_idx=0):
  """
  Creates 2D projections of marker positions for specific frame.
  
  Args:
    frames_data: Data array (frames, markers, XYZ)
    marker_names: List of marker names
    simple_names: List of simple names (l1, r1, etc.)
    frame_idx: Frame index to display
  """
  if simple_names is None:
    simple_names = marker_names
    
  # Create figure with three subplots (XY, XZ, YZ projections)
  fig, axes = plt.subplots(1, 3, figsize=(18, 6))
  
  # Extract data for specified frame
  frame_data = frames_data[frame_idx]
  
  # XY projection
  axes[0].scatter(frame_data[:, 0], frame_data[:, 1], s=150, c='red', alpha=0.7, edgecolors='black', linewidths=1.5)
  for i, name in enumerate(simple_names):
    axes[0].annotate(name, (frame_data[i, 0], frame_data[i, 1]), 
                    fontsize=12, fontweight='bold', alpha=0.9,
                    ha='center', va='bottom')
  axes[0].set_xlabel('X (mm)')
  axes[0].set_ylabel('Y (mm)')
  axes[0].set_title('XY Projection (top view)')
  axes[0].grid(True, alpha=0.3)
  axes[0].set_aspect('equal', adjustable='box')
  
  # XZ projection
  axes[1].scatter(frame_data[:, 0], frame_data[:, 2], s=150, c='green', alpha=0.7, edgecolors='black', linewidths=1.5)
  for i, name in enumerate(simple_names):
    axes[1].annotate(name, (frame_data[i, 0], frame_data[i, 2]), 
                    fontsize=12, fontweight='bold', alpha=0.9,
                    ha='center', va='bottom')
  axes[1].set_xlabel('X (mm)')
  axes[1].set_ylabel('Z (mm)')
  axes[1].set_title('XZ Projection (side view)')
  axes[1].grid(True, alpha=0.3)
  axes[1].set_aspect('equal', adjustable='box')
  
  # YZ projection
  axes[2].scatter(frame_data[:, 1], frame_data[:, 2], s=150, c='blue', alpha=0.7, edgecolors='black', linewidths=1.5)
  for i, name in enumerate(simple_names):
    axes[2].annotate(name, (frame_data[i, 1], frame_data[i, 2]), 
                    fontsize=12, fontweight='bold', alpha=0.9,
                    ha='center', va='bottom')
  axes[2].set_xlabel('Y (mm)')
  axes[2].set_ylabel('Z (mm)')
  axes[2].set_title('YZ Projection (front view)')
  axes[2].grid(True, alpha=0.3)
  axes[2].set_aspect('equal', adjustable='box')
  
  fig.suptitle(f'Marker Positions - Frame {frame_idx + 1}', fontsize=14)
  fig.tight_layout()
  
  return fig


def main():
  """Main function."""
  # Parse arguments
  parser = argparse.ArgumentParser(
    description='Create static plots of marker trajectories'
  )
  parser.add_argument(
    'file',
    type=str,
    help='Path to TSV file with marker data'
  )
  parser.add_argument(
    '--frame',
    type=int,
    default=0,
    help='Frame number for 2D projections (default: 0)'
  )
  parser.add_argument(
    '--save-trajectories',
    type=str,
    help='Save trajectory plot to file'
  )
  parser.add_argument(
    '--save-projections',
    type=str,
    help='Save 2D projections to file'
  )
  
  args = parser.parse_args()
  
  # File path
  file_path = Path(args.file)
  if not file_path.exists():
    print(f"❌ Error: File {file_path} not found!")
    return
  
  print(f"📂 Reading file: {file_path}")
  
  # Read data
  reader = MarkerDataReader(file_path)
  data = reader.read_file()
  
  print(f"✅ Read {len(data['frames'])} frames, {len(data['marker_names'])} markers")
  
  # Create trajectory plot
  print("\n🎨 Creating trajectory plot...")
  fig_traj = plot_marker_trajectories(
    data['frames'],
    data['marker_names'],
    data.get('simple_names'),
    title=f"Marker Trajectories - {file_path.stem}"
  )
  
  if args.save_trajectories:
    print(f"💾 Saving trajectory plot: {args.save_trajectories}")
    fig_traj.savefig(args.save_trajectories, dpi=150, bbox_inches='tight')
    print(f"✅ Saved: {args.save_trajectories}")
  
  # Create 2D projections
  print(f"\n🎨 Creating 2D projections for frame {args.frame + 1}...")
  fig_proj = plot_marker_positions_2d(
    data['frames'],
    data['marker_names'],
    data.get('simple_names'),
    frame_idx=args.frame
  )
  
  if args.save_projections:
    print(f"💾 Saving 2D projections: {args.save_projections}")
    fig_proj.savefig(args.save_projections, dpi=150, bbox_inches='tight')
    print(f"✅ Saved: {args.save_projections}")
  
  # Display plots if not saving
  if not args.save_trajectories and not args.save_projections:
    print("\n📊 Displaying plots...")
    plt.show()
  elif not args.save_trajectories or not args.save_projections:
    print("\n📊 Displaying plots...")
    plt.show()
  
  print("\n✅ Done!")


if __name__ == "__main__":
  main()
