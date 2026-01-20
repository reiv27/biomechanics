#!/usr/bin/env python3
"""
Script for calculating and saving joint angles to JSON files.
Reads marker data and saves calculated angles.
"""

import json
import numpy as np
from pathlib import Path
from calculate_angles import calculate_angles
from visualize_markers import MarkerDataReader


def save_angles_to_json(angles, metadata, output_path, frequency=100):
  """
  Save calculated angles to JSON file.
  
  Args:
    angles: Dictionary with angle arrays (qr1, qr2, qr3, ql1, ql2, ql3)
    metadata: Dictionary with metadata from marker data
    output_path: Path to output JSON file
    frequency: Sampling frequency in Hz
  """
  # Prepare data for JSON (convert numpy arrays to lists)
  json_data = {
    'metadata': {
      'frequency': frequency,
      'num_frames': len(angles['qr1']),
      'source_metadata': metadata
    },
    'angles': {
      'right': {
        'qr1': angles['qr1'].tolist(),
        'qr2': angles['qr2'].tolist(),
        'qr3': angles['qr3'].tolist()
      },
      'left': {
        'ql1': angles['ql1'].tolist(),
        'ql2': angles['ql2'].tolist(),
        'ql3': angles['ql3'].tolist()
      }
    },
    'statistics': {
      'right': {
        'qr1': {
          'mean': float(np.mean(angles['qr1'])),
          'std': float(np.std(angles['qr1'])),
          'min': float(np.min(angles['qr1'])),
          'max': float(np.max(angles['qr1']))
        },
        'qr2': {
          'mean': float(np.mean(angles['qr2'])),
          'std': float(np.std(angles['qr2'])),
          'min': float(np.min(angles['qr2'])),
          'max': float(np.max(angles['qr2']))
        },
        'qr3': {
          'mean': float(np.mean(angles['qr3'])),
          'std': float(np.std(angles['qr3'])),
          'min': float(np.min(angles['qr3'])),
          'max': float(np.max(angles['qr3']))
        }
      },
      'left': {
        'ql1': {
          'mean': float(np.mean(angles['ql1'])),
          'std': float(np.std(angles['ql1'])),
          'min': float(np.min(angles['ql1'])),
          'max': float(np.max(angles['ql1']))
        },
        'ql2': {
          'mean': float(np.mean(angles['ql2'])),
          'std': float(np.std(angles['ql2'])),
          'min': float(np.min(angles['ql2'])),
          'max': float(np.max(angles['ql2']))
        },
        'ql3': {
          'mean': float(np.mean(angles['ql3'])),
          'std': float(np.std(angles['ql3'])),
          'min': float(np.min(angles['ql3'])),
          'max': float(np.max(angles['ql3']))
        }
      }
    }
  }
  
  # Save to JSON file
  output_path = Path(output_path)
  output_path.parent.mkdir(parents=True, exist_ok=True)
  
  with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(json_data, f, indent=2, ensure_ascii=False)
  
  print(f"✅ Углы сохранены в: {output_path}")


def process_measurement(measurement_num, output_dir=None):
  """
  Process a single measurement: calculate and save angles.
  
  Args:
    measurement_num: Measurement number (1 or 2)
    output_dir: Output directory for JSON files (default: data/angle_data/mes{N}/)
  """
  print(f"\n{'='*80}")
  print(f"📊 Обработка Measurement{measurement_num}")
  print(f"{'='*80}")
  
  # Paths
  base_dir = Path(__file__).parent
  marker_file = base_dir / 'data' / f'Measurement{measurement_num}.tsv'
  
  if output_dir is None:
    # Save calculated angles to separate directory
    output_dir = base_dir / 'data' / 'calculated_angles'
  else:
    output_dir = Path(output_dir)
  
  if not marker_file.exists():
    print(f"❌ Файл маркеров не найден: {marker_file}")
    return
  
  # Read marker data and calculate angles
  print(f"\n📂 Чтение данных маркеров: {marker_file}")
  reader = MarkerDataReader(marker_file)
  marker_data = reader.read_file()
  
  print(f"✅ Загружено {len(marker_data['frames'])} кадров")
  print(f"   Маркеры: {', '.join(marker_data['simple_names'])}")
  
  # Calculate angles
  print(f"\n📐 Вычисление углов...")
  calculated_angles = calculate_angles(marker_data['frames'], marker_data['simple_names'])
  
  # Get frequency
  frequency = float(marker_data['metadata'].get('FREQUENCY', 100))
  
  # Print statistics
  print(f"\n📊 Статистика углов:")
  print(f"\n  Правая сторона:")
  print(f"    qr1: {calculated_angles['qr1'].mean():.1f}° ± {calculated_angles['qr1'].std():.1f}° "
        f"(диапазон: {calculated_angles['qr1'].min():.1f}° - {calculated_angles['qr1'].max():.1f}°)")
  print(f"    qr2: {calculated_angles['qr2'].mean():.1f}° ± {calculated_angles['qr2'].std():.1f}° "
        f"(диапазон: {calculated_angles['qr2'].min():.1f}° - {calculated_angles['qr2'].max():.1f}°)")
  print(f"    qr3: {calculated_angles['qr3'].mean():.1f}° ± {calculated_angles['qr3'].std():.1f}° "
        f"(диапазон: {calculated_angles['qr3'].min():.1f}° - {calculated_angles['qr3'].max():.1f}°)")
  
  print(f"\n  Левая сторона:")
  print(f"    ql1: {calculated_angles['ql1'].mean():.1f}° ± {calculated_angles['ql1'].std():.1f}° "
        f"(диапазон: {calculated_angles['ql1'].min():.1f}° - {calculated_angles['ql1'].max():.1f}°)")
  print(f"    ql2: {calculated_angles['ql2'].mean():.1f}° ± {calculated_angles['ql2'].std():.1f}° "
        f"(диапазон: {calculated_angles['ql2'].min():.1f}° - {calculated_angles['ql2'].max():.1f}°)")
  print(f"    ql3: {calculated_angles['ql3'].mean():.1f}° ± {calculated_angles['ql3'].std():.1f}° "
        f"(диапазон: {calculated_angles['ql3'].min():.1f}° - {calculated_angles['ql3'].max():.1f}°)")
  
  # Save to JSON
  output_path = output_dir / f'Measurement{measurement_num}_calculated_angles.json'
  print(f"\n💾 Сохранение углов в JSON...")
  save_angles_to_json(
    calculated_angles,
    marker_data['metadata'],
    output_path,
    frequency=frequency
  )
  
  return output_path


def main():
  """Main function."""
  import argparse
  
  parser = argparse.ArgumentParser(
    description='Calculate and save joint angles to JSON files'
  )
  parser.add_argument(
    '--measurement',
    type=int,
    choices=[1, 2],
    help='Measurement number to process (1 or 2). If not specified, process both.'
  )
  parser.add_argument(
    '--output-dir',
    type=str,
    help='Output directory for JSON files (default: data/angle_data/mes{N}/)'
  )
  
  args = parser.parse_args()
  
  if args.measurement:
    process_measurement(args.measurement, args.output_dir)
  else:
    # Process both measurements
    process_measurement(1, args.output_dir)
    process_measurement(2, args.output_dir)
  
  print(f"\n{'='*80}")
  print("✅ Обработка завершена!")
  print(f"{'='*80}\n")


if __name__ == "__main__":
  main()
