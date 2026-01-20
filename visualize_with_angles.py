#!/usr/bin/env python3
"""
Script for simultaneous visualization of 3D markers and joint angles.
Shows 3D animation alongside real-time angle plots.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.gridspec import GridSpec
from pathlib import Path
from visualize_markers import MarkerDataReader
from calculate_angles import calculate_angles
import argparse


class CombinedVisualizer:
  """Class for combined 3D marker and angle visualization."""
  
  def __init__(self, frames_data, marker_names, simple_names, angles, title="Motion Capture Visualization"):
    """
    Initialize visualizer.
    
    Args:
      frames_data: Marker data array (frames, markers, XYZ)
      marker_names: List of original marker names
      simple_names: List of simple marker names
      angles: Dictionary with calculated angles
      title: Visualization title
    """
    self.frames_data = frames_data
    self.marker_names = marker_names
    self.simple_names = simple_names
    self.angles = angles
    self.title = title
    
    self.fig = None
    self.ax_3d = None
    self.ax_q1 = None
    self.ax_q2 = None
    self.ax_q3 = None
    
    self.scatter = None
    self.labels = []
    
    # Lines for angle plots
    self.line_qr1 = None
    self.line_ql1 = None
    self.line_qr2 = None
    self.line_ql2 = None
    self.line_qr3 = None
    self.line_ql3 = None
    
    # Data for progressive plotting
    self.time_data = []
    self.qr1_data = []
    self.ql1_data = []
    self.qr2_data = []
    self.ql2_data = []
    self.qr3_data = []
    self.ql3_data = []
    
  def setup_plot(self, frequency=100):
    """Set up the combined visualization layout."""
    # Create figure with custom layout
    self.fig = plt.figure(figsize=(18, 10))
    gs = GridSpec(3, 2, figure=self.fig, width_ratios=[1.2, 1], hspace=0.3, wspace=0.25)
    
    # 3D subplot (left side, spans all rows)
    self.ax_3d = self.fig.add_subplot(gs[:, 0], projection='3d')
    
    # Angle subplots (right side)
    self.ax_q1 = self.fig.add_subplot(gs[0, 1])
    self.ax_q2 = self.fig.add_subplot(gs[1, 1])
    self.ax_q3 = self.fig.add_subplot(gs[2, 1])
    
    self.fig.suptitle(self.title, fontsize=14, fontweight='bold')
    
    # Setup 3D plot
    self._setup_3d_plot()
    
    # Setup angle plots
    self._setup_angle_plots(frequency)
    
  def _setup_3d_plot(self):
    """Set up 3D marker visualization."""
    # Calculate axis boundaries
    all_x = self.frames_data[:, :, 0].flatten()
    all_y = self.frames_data[:, :, 1].flatten()
    all_z = self.frames_data[:, :, 2].flatten()
    
    max_range = np.array([
      all_x.max() - all_x.min(),
      all_y.max() - all_y.min(),
      all_z.max() - all_z.min()
    ]).max() / 2.0
    
    mid_x = (all_x.max() + all_x.min()) * 0.5
    mid_y = (all_y.max() + all_y.min()) * 0.5
    mid_z = (all_z.max() + all_z.min()) * 0.5
    
    self.ax_3d.set_xlim(mid_x - max_range, mid_x + max_range)
    self.ax_3d.set_ylim(mid_y - max_range, mid_y + max_range)
    self.ax_3d.set_zlim(mid_z - max_range, mid_z + max_range)
    
    self.ax_3d.set_xlabel('X (mm)', fontsize=10)
    self.ax_3d.set_ylabel('Y (mm)', fontsize=10)
    self.ax_3d.set_zlabel('Z (mm)', fontsize=10)
    self.ax_3d.set_title('3D Marker Positions', fontsize=12, fontweight='bold')
    
    # Create initial scatter plot
    first_frame = self.frames_data[0]
    self.scatter = self.ax_3d.scatter(
      first_frame[:, 0],
      first_frame[:, 1],
      first_frame[:, 2],
      c='red',
      s=80,
      marker='o',
      alpha=0.8,
      edgecolors='black',
      linewidths=1.5
    )
    
    # Add labels
    self.labels = []
    for i, (x, y, z) in enumerate(first_frame):
      label = self.ax_3d.text(
        x, y, z,
        self.simple_names[i],
        fontsize=8,
        fontweight='bold',
        color='blue',
        ha='center',
        va='bottom'
      )
      self.labels.append(label)
  
  def _setup_angle_plots(self, frequency):
    """Set up angle plot axes."""
    num_frames = len(self.frames_data)
    total_time = num_frames / frequency
    
    # Calculate Y-axis limits from all angle data
    all_q1 = np.concatenate([self.angles['qr1'], self.angles['ql1']])
    all_q2 = np.concatenate([self.angles['qr2'], self.angles['ql2']])
    all_q3 = np.concatenate([self.angles['qr3'], self.angles['ql3']])
    
    q1_min, q1_max = np.nanmin(all_q1), np.nanmax(all_q1)
    q2_min, q2_max = np.nanmin(all_q2), np.nanmax(all_q2)
    q3_min, q3_max = np.nanmin(all_q3), np.nanmax(all_q3)
    
    # Add 10% padding
    q1_padding = (q1_max - q1_min) * 0.1
    q2_padding = (q2_max - q2_min) * 0.1
    q3_padding = (q3_max - q3_min) * 0.1
    
    # Q1 plot - create empty lines
    self.line_qr1, = self.ax_q1.plot([], [], 'b-', linewidth=1.5, label='Right', alpha=0.7)
    self.line_ql1, = self.ax_q1.plot([], [], 'r-', linewidth=1.5, label='Left', alpha=0.7)
    self.ax_q1.set_ylabel('Angle (°)', fontsize=9)
    self.ax_q1.set_title('Q1: Knee-Ankle vs XY plane', fontsize=10, fontweight='bold')
    self.ax_q1.legend(loc='upper right', fontsize=8)
    self.ax_q1.grid(True, alpha=0.3)
    self.ax_q1.set_xlim(0, total_time)
    self.ax_q1.set_ylim(q1_min - q1_padding, q1_max + q1_padding)
    
    # Q2 plot - create empty lines
    self.line_qr2, = self.ax_q2.plot([], [], 'b-', linewidth=1.5, label='Right', alpha=0.7)
    self.line_ql2, = self.ax_q2.plot([], [], 'r-', linewidth=1.5, label='Left', alpha=0.7)
    self.ax_q2.set_ylabel('Angle (°)', fontsize=9)
    self.ax_q2.set_title('Q2: Knee Angle', fontsize=10, fontweight='bold')
    self.ax_q2.legend(loc='upper right', fontsize=8)
    self.ax_q2.grid(True, alpha=0.3)
    self.ax_q2.set_xlim(0, total_time)
    self.ax_q2.set_ylim(q2_min - q2_padding, q2_max + q2_padding)
    
    # Q3 plot - create empty lines
    self.line_qr3, = self.ax_q3.plot([], [], 'b-', linewidth=1.5, label='Right', alpha=0.7)
    self.line_ql3, = self.ax_q3.plot([], [], 'r-', linewidth=1.5, label='Left', alpha=0.7)
    self.ax_q3.set_xlabel('Time (s)', fontsize=9)
    self.ax_q3.set_ylabel('Angle (°)', fontsize=9)
    self.ax_q3.set_title('Q3: Hip Angle', fontsize=10, fontweight='bold')
    self.ax_q3.legend(loc='upper right', fontsize=8)
    self.ax_q3.grid(True, alpha=0.3)
    self.ax_q3.set_xlim(0, total_time)
    self.ax_q3.set_ylim(q3_min - q3_padding, q3_max + q3_padding)
  
  def update_frame(self, frame_num, frequency=100):
    """Update both 3D markers and angle plots."""
    # Update 3D markers
    current_frame = self.frames_data[frame_num]
    
    self.scatter._offsets3d = (
      current_frame[:, 0],
      current_frame[:, 1],
      current_frame[:, 2]
    )
    
    for i, (x, y, z) in enumerate(current_frame):
      self.labels[i].set_position((x, y))
      self.labels[i].set_3d_properties(z, 'z')
    
    # Update 3D title
    self.ax_3d.set_title(f'3D Marker Positions - Frame {frame_num + 1}/{len(self.frames_data)}', 
                         fontsize=12, fontweight='bold')
    
    # Add new data point to angle plots
    current_time = frame_num / frequency
    self.time_data.append(current_time)
    self.qr1_data.append(self.angles['qr1'][frame_num])
    self.ql1_data.append(self.angles['ql1'][frame_num])
    self.qr2_data.append(self.angles['qr2'][frame_num])
    self.ql2_data.append(self.angles['ql2'][frame_num])
    self.qr3_data.append(self.angles['qr3'][frame_num])
    self.ql3_data.append(self.angles['ql3'][frame_num])
    
    # Update line data
    self.line_qr1.set_data(self.time_data, self.qr1_data)
    self.line_ql1.set_data(self.time_data, self.ql1_data)
    self.line_qr2.set_data(self.time_data, self.qr2_data)
    self.line_ql2.set_data(self.time_data, self.ql2_data)
    self.line_qr3.set_data(self.time_data, self.qr3_data)
    self.line_ql3.set_data(self.time_data, self.ql3_data)
    
    return ([self.scatter] + self.labels + 
            [self.line_qr1, self.line_ql1, self.line_qr2, 
             self.line_ql2, self.line_qr3, self.line_ql3])
  
  def _reset_data(self):
    """Reset accumulated plot data for new animation cycle."""
    self.time_data = []
    self.qr1_data = []
    self.ql1_data = []
    self.qr2_data = []
    self.ql2_data = []
    self.qr3_data = []
    self.ql3_data = []
  
  def animate(self, interval=10, skip_frames=1, frequency=100):
    """Run the animation."""
    self.setup_plot(frequency)
    
    num_frames = len(self.frames_data)
    frames_to_show = range(0, num_frames, skip_frames)
    
    # Function to update frame and reset on loop
    def update_with_reset(frame_idx):
      # If this is the first frame, reset data
      if frame_idx == 0:
        self._reset_data()
      return self.update_frame(frame_idx, frequency)
    
    anim = FuncAnimation(
      self.fig,
      update_with_reset,
      frames=frames_to_show,
      interval=interval,
      blit=False,
      repeat=True
    )
    
    return anim


def main():
  """Main function."""
  parser = argparse.ArgumentParser(
    description='Combined visualization of 3D markers and joint angles'
  )
  parser.add_argument(
    'file',
    type=str,
    help='Path to TSV file with marker data'
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
  parser.add_argument(
    '--save',
    type=str,
    help='Save animation to file (e.g.: output.gif or output.mp4)'
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
  
  # Get frequency
  frequency = float(data['metadata'].get('FREQUENCY', 100))
  
  # Create visualizer
  print("\n🎬 Creating combined visualization...")
  
  visualizer = CombinedVisualizer(
    data['frames'],
    data['marker_names'],
    data['simple_names'],
    angles,
    title=f"Motion Capture Visualization - {file_path.stem}"
  )
  
  anim = visualizer.animate(
    interval=args.interval,
    skip_frames=args.skip_frames,
    frequency=frequency
  )
  
  # Save or display
  if args.save:
    print(f"\n💾 Saving animation to: {args.save}")
    print("   (this may take several minutes...)")
    
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
  
  print("\n✅ Done!")


if __name__ == "__main__":
  main()
