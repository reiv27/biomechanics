#!/usr/bin/env python3
"""
Test script for verifying marker data reading without GUI.
Simply outputs data information to console.
"""

from visualize_markers import MarkerDataReader
from pathlib import Path
import argparse
import sys


def main():
  """Main function for testing data reading."""
  
  # Parse command line arguments
  parser = argparse.ArgumentParser(
    description='Verify marker data reading from TSV files'
  )
  parser.add_argument(
    'files',
    nargs='*',
    help='Paths to TSV files for verification (if not specified, use default files)'
  )
  
  args = parser.parse_args()
  
  project_root = Path(__file__).parent
  
  # If files specified in arguments, use them
  if args.files:
    test_files = []
    for file_path in args.files:
      path = Path(file_path)
      # If relative path, make it relative to current directory
      if not path.is_absolute():
        path = Path.cwd() / path
      test_files.append(path)
  else:
    # Default file list for testing
    test_files = [
      project_root / 'data' / 'Measurement1.tsv',
      project_root / 'data' / 'Measurement2.tsv',
    ]
  
  for file_path in test_files:
    if not file_path.exists():
      print(f"⚠️  File not found: {file_path}")
      continue
    
    print(f"\n{'='*60}")
    print(f"Reading file: {file_path.relative_to(project_root)}")
    print(f"{'='*60}")
    
    # Read data
    reader = MarkerDataReader(file_path)
    data = reader.read_file()
    
    # Display metadata
    print("\n📊 Metadata:")
    for key, value in data['metadata'].items():
      print(f"  {key}: {value}")
    
    # Display marker information
    print(f"\n🎯 Markers ({len(data['marker_names'])} pcs):")
    print("  Simple names and original:")
    for i in range(min(5, len(data['marker_names']))):
      simple_name = data['simple_names'][i] if 'simple_names' in data else f"m{i+1}"
      orig_name = data['marker_names'][i]
      print(f"  {simple_name} ({orig_name})")
    if len(data['marker_names']) > 5:
      print(f"  ... and {len(data['marker_names']) - 5} more")
    
    # Display data information
    print(f"\n📈 Data:")
    print(f"  Array shape: {data['frames'].shape}")
    print(f"  (frames, markers, XYZ coordinates)")
    
    # Display first frame example
    print(f"\n🔍 First frame (first 3 markers):")
    for i in range(min(3, len(data['marker_names']))):
      simple_name = data['simple_names'][i] if 'simple_names' in data else data['marker_names'][i]
      x, y, z = data['frames'][0, i, :]
      print(f"  {simple_name}:")
      print(f"    X: {x:8.3f} mm")
      print(f"    Y: {y:8.3f} mm")
      print(f"    Z: {z:8.3f} mm")
    
    # Movement statistics
    print(f"\n📉 Movement statistics (all frames):")
    for axis_idx, axis_name in enumerate(['X', 'Y', 'Z']):
      axis_data = data['frames'][:, :, axis_idx]
      print(f"  {axis_name}: min={axis_data.min():8.2f}, max={axis_data.max():8.2f}, "
            f"mean={axis_data.mean():8.2f} mm")
  
  print(f"\n{'='*60}")
  print("✅ Testing completed!")
  print(f"{'='*60}\n")


if __name__ == "__main__":
  main()
