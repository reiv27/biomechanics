#!/usr/bin/env python3
"""
Script for plotting angle dependencies and approximating with 3rd degree polynomials.
Reads calculated angles from JSON files and finds phi_1(q2) and phi_3(q2) approximations.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import argparse


def load_angles_from_json(json_path):
  """
  Load angles from JSON file.
  
  Args:
    json_path: Path to JSON file
    
  Returns:
    Dictionary with angles and metadata (including frame_range if present)
  """
  with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
  
  result = {
    'metadata': data['metadata'],
    'angles': {
      'right': {
        'q1': np.array(data['angles']['right']['qr1']),
        'q2': np.array(data['angles']['right']['qr2']),
        'q3': np.array(data['angles']['right']['qr3'])
      },
      'left': {
        'q1': np.array(data['angles']['left']['ql1']),
        'q2': np.array(data['angles']['left']['ql2']),
        'q3': np.array(data['angles']['left']['ql3'])
      }
    }
  }
  
  if 'frame_range' in data['metadata']:
    result['frame_range'] = data['metadata']['frame_range']
  
  return result


def filter_angles_by_range(angles_data, start_frame=None, end_frame=None):
  """
  Filter angles data by frame range.
  
  Args:
    angles_data: Dictionary with angles (from load_angles_from_json)
    start_frame: Start frame index (0-based, inclusive). If None, start from beginning.
    end_frame: End frame index (0-based, exclusive). If None, end at last frame.
    
  Returns:
    Filtered angles data
  """
  filtered = {
    'metadata': angles_data['metadata'].copy(),
    'angles': {
      'right': {},
      'left': {}
    }
  }
  
  qr1 = angles_data['angles']['right']['q1']
  qr2 = angles_data['angles']['right']['q2']
  qr3 = angles_data['angles']['right']['q3']
  ql1 = angles_data['angles']['left']['q1']
  ql2 = angles_data['angles']['left']['q2']
  ql3 = angles_data['angles']['left']['q3']
  
  num_frames = len(qr1)
  start = start_frame if start_frame is not None else 0
  end = end_frame if end_frame is not None else num_frames
  
  start = max(0, min(start, num_frames))
  end = max(start, min(end, num_frames))
  
  filtered['angles']['right']['q1'] = qr1[start:end]
  filtered['angles']['right']['q2'] = qr2[start:end]
  filtered['angles']['right']['q3'] = qr3[start:end]
  filtered['angles']['left']['q1'] = ql1[start:end]
  filtered['angles']['left']['q2'] = ql2[start:end]
  filtered['angles']['left']['q3'] = ql3[start:end]
  
  return filtered, start, end


def approximate_polynomial_3rd_degree(x, y):
  """
  Approximate y = f(x) with single 3rd degree polynomial: y = a*x^3 + b*x^2 + c*x + d
  
  Args:
    x: Independent variable array
    y: Dependent variable array
    
  Returns:
    Tuple (coefficients, polynomial_function)
    coefficients: [a, b, c, d] for polynomial a*x^3 + b*x^2 + c*x + d
    polynomial_function: Function that computes polynomial value
  """
  coefficients = np.polyfit(x, y, deg=3)
  poly_func = np.poly1d(coefficients)
  
  return coefficients, poly_func


def approximate_polynomial_5th_degree(x, y):
  """
  Approximate y = f(x) with single 5th degree polynomial: y = a*x^5 + b*x^4 + c*x^3 + d*x^2 + e*x + f
  
  Args:
    x: Independent variable array
    y: Dependent variable array
    
  Returns:
    Tuple (coefficients, polynomial_function)
    coefficients: [a, b, c, d, e, f] for polynomial a*x^5 + b*x^4 + c*x^3 + d*x^2 + e*x + f
    polynomial_function: Function that computes polynomial value
  """
  coefficients = np.polyfit(x, y, deg=5)
  poly_func = np.poly1d(coefficients)
  
  return coefficients, poly_func


def calculate_derivative(q2, frequency=100):
  """
  Calculate derivative of q2 with respect to time using numpy.gradient.
  
  Args:
    q2: Array of q2 values (in radians)
    frequency: Sampling frequency in Hz
    
  Returns:
    Array of dq2/dt values (radians per second)
  """
  dt = 1.0 / frequency
  dq2_dt = np.gradient(q2, dt)
  
  return dq2_dt


def save_approximation_data(result_data, angles_data, measurement_name, output_path):
  """
  Save approximation coefficients and derivative data to JSON file.
  
  Args:
    result_data: Dictionary with coefficients and derivatives from plot_angle_dependencies
    angles_data: Original angles data
    measurement_name: Name of measurement
    output_path: Path to output JSON file
  """
  frequency = angles_data['metadata'].get('frequency', 100)
  num_frames = len(result_data['time'])
  
  json_data = {
    'metadata': {
      'measurement': measurement_name,
      'frequency': frequency,
      'num_frames': num_frames,
      'source_metadata': angles_data['metadata'].get('source_metadata', {})
    },
    'approximation_coefficients': result_data['coefficients'],
    'derivatives': result_data['derivatives'],
    'q2': result_data['q2'],
    'time': result_data['time']
  }
  
  if 'frame_range' in angles_data:
    json_data['metadata']['frame_range'] = angles_data['frame_range']
  
  output_path = Path(output_path)
  output_path.parent.mkdir(parents=True, exist_ok=True)
  
  with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(json_data, f, indent=2, ensure_ascii=False)
  
  print(f"✅ Approximation data saved to: {output_path}")


def plot_angle_dependencies(angles_data, measurement_name, save_path=None, start_frame=None, end_frame=None):
  """
  Plot dependencies: q1 vs q2, q3 vs q2, and dq2/dt vs time.
  
  Args:
    angles_data: Dictionary with angles (from load_angles_from_json)
    measurement_name: Name of measurement (for title)
    save_path: Optional path to save the plot
    start_frame: Start frame index for filtering (overrides JSON frame_range if present)
    end_frame: End frame index for filtering (overrides JSON frame_range if present)
    
  Returns:
    Dictionary with approximation coefficients and derivative data
  """
  if 'frame_range' in angles_data and (start_frame is None and end_frame is None):
    frame_range = angles_data['frame_range']
    range_info = f' (frames {frame_range["start_frame"]}-{frame_range["end_frame"]} from total {frame_range["total_frames"]})'
  elif start_frame is not None or end_frame is not None:
    angles_data, start, end = filter_angles_by_range(angles_data, start_frame, end_frame)
    range_info = f' (frames {start}-{end})'
  else:
    range_info = ''
  
  frequency = angles_data['metadata'].get('frequency', 100)
  num_frames = len(angles_data['angles']['right']['q1'])
  time = np.arange(num_frames) / frequency
  
  fig, axes = plt.subplots(4, 2, figsize=(14, 14))
  fig.suptitle(f'Angle Dependencies and Derivatives - {measurement_name}{range_info}', fontsize=16, fontweight='bold')
  
  qr1 = angles_data['angles']['right']['q1']
  qr2 = angles_data['angles']['right']['q2']
  qr3 = angles_data['angles']['right']['q3']
  
  ql1 = angles_data['angles']['left']['q1']
  ql2 = angles_data['angles']['left']['q2']
  ql3 = angles_data['angles']['left']['q3']
  
  phi1_r_coeffs, phi1_r_func = approximate_polynomial_3rd_degree(qr2, qr1)
  phi3_r_coeffs, phi3_r_func = approximate_polynomial_3rd_degree(qr2, qr3)
  
  phi1_l_coeffs, phi1_l_func = approximate_polynomial_3rd_degree(ql2, ql1)
  phi3_l_coeffs, phi3_l_func = approximate_polynomial_3rd_degree(ql2, ql3)
  
  q2_r_coeffs, q2_r_func = approximate_polynomial_5th_degree(time, qr2)
  q2_l_coeffs, q2_l_func = approximate_polynomial_5th_degree(time, ql2)
  
  dq2_r_dt = calculate_derivative(qr2, frequency)
  dq2_l_dt = calculate_derivative(ql2, frequency)
  
  q2_r_approx = q2_r_func(time)
  q2_l_approx = q2_l_func(time)
  dq2_r_dt_approx = calculate_derivative(q2_r_approx, frequency)
  dq2_l_dt_approx = calculate_derivative(q2_l_approx, frequency)
  
  print(f"\n📊 Polynomial coefficients for {measurement_name}:")
  print(f"\n  Right side:")
  print(f"    phi_1(q2) = q1: a={phi1_r_coeffs[0]:.6e}, b={phi1_r_coeffs[1]:.6e}, c={phi1_r_coeffs[2]:.6e}, d={phi1_r_coeffs[3]:.6e}")
  print(f"    phi_3(q2) = q3: a={phi3_r_coeffs[0]:.6e}, b={phi3_r_coeffs[1]:.6e}, c={phi3_r_coeffs[2]:.6e}, d={phi3_r_coeffs[3]:.6e}")
  print(f"    q2(t): a={q2_r_coeffs[0]:.6e}, b={q2_r_coeffs[1]:.6e}, c={q2_r_coeffs[2]:.6e}, d={q2_r_coeffs[3]:.6e}, e={q2_r_coeffs[4]:.6e}, f={q2_r_coeffs[5]:.6e}")
  print(f"\n  Left side:")
  print(f"    phi_1(q2) = q1: a={phi1_l_coeffs[0]:.6e}, b={phi1_l_coeffs[1]:.6e}, c={phi1_l_coeffs[2]:.6e}, d={phi1_l_coeffs[3]:.6e}")
  print(f"    phi_3(q2) = q3: a={phi3_l_coeffs[0]:.6e}, b={phi3_l_coeffs[1]:.6e}, c={phi3_l_coeffs[2]:.6e}, d={phi3_l_coeffs[3]:.6e}")
  print(f"    q2(t): a={q2_l_coeffs[0]:.6e}, b={q2_l_coeffs[1]:.6e}, c={q2_l_coeffs[2]:.6e}, d={q2_l_coeffs[3]:.6e}, e={q2_l_coeffs[4]:.6e}, f={q2_l_coeffs[5]:.6e}")
  
  qr2_smooth = np.linspace(qr2.min(), qr2.max(), 200)
  ql2_smooth = np.linspace(ql2.min(), ql2.max(), 200)
  
  axes[0, 0].scatter(qr2, qr1, alpha=0.5, s=10, c='black', label='Data')
  axes[0, 0].plot(qr2_smooth, phi1_r_func(qr2_smooth), 'brown', linewidth=2, label='phi_1(q2) polynomial', alpha=0.8)
  axes[0, 0].set_xlabel('q2 (radians)', fontsize=12)
  axes[0, 0].set_ylabel('q1 (radians)', fontsize=12)
  axes[0, 0].set_title('Right: q1 vs q2', fontsize=13, fontweight='bold')
  axes[0, 0].grid(True, alpha=0.3)
  axes[0, 0].legend()
  
  axes[0, 1].scatter(qr2, qr3, alpha=0.5, s=10, c='black', label='Data')
  axes[0, 1].plot(qr2_smooth, phi3_r_func(qr2_smooth), 'brown', linewidth=2, label='phi_3(q2) polynomial', alpha=0.8)
  axes[0, 1].set_xlabel('q2 (radians)', fontsize=12)
  axes[0, 1].set_ylabel('q3 (radians)', fontsize=12)
  axes[0, 1].set_title('Right: q3 vs q2', fontsize=13, fontweight='bold')
  axes[0, 1].grid(True, alpha=0.3)
  axes[0, 1].legend()
  
  axes[1, 0].scatter(ql2, ql1, alpha=0.5, s=10, c='red', label='Data')
  axes[1, 0].plot(ql2_smooth, phi1_l_func(ql2_smooth), 'b-', linewidth=2, label='phi_1(q2) polynomial', alpha=0.8)
  axes[1, 0].set_xlabel('q2 (radians)', fontsize=12)
  axes[1, 0].set_ylabel('q1 (radians)', fontsize=12)
  axes[1, 0].set_title('Left: q1 vs q2', fontsize=13, fontweight='bold')
  axes[1, 0].grid(True, alpha=0.3)
  axes[1, 0].legend()
  
  axes[1, 1].scatter(ql2, ql3, alpha=0.5, s=10, c='red', label='Data')
  axes[1, 1].plot(ql2_smooth, phi3_l_func(ql2_smooth), 'b-', linewidth=2, label='phi_3(q2) polynomial', alpha=0.8)
  axes[1, 1].set_xlabel('q2 (radians)', fontsize=12)
  axes[1, 1].set_ylabel('q3 (radians)', fontsize=12)
  axes[1, 1].set_title('Left: q3 vs q2', fontsize=13, fontweight='bold')
  axes[1, 1].grid(True, alpha=0.3)
  axes[1, 1].legend()
  
  axes[2, 0].plot(time, qr2, 'k-', linewidth=1.5, label='Right q2 (raw)', alpha=0.7)
  axes[2, 0].plot(time, q2_r_approx, 'brown', linestyle='--', linewidth=2, label='Right q2 (polynomial)', alpha=0.8)
  axes[2, 0].set_xlabel('Time (seconds)', fontsize=12)
  axes[2, 0].set_ylabel('q2 (radians)', fontsize=12)
  axes[2, 0].set_title('Right: q2 vs time', fontsize=13, fontweight='bold')
  axes[2, 0].grid(True, alpha=0.3)
  axes[2, 0].legend()
  
  axes[2, 1].plot(time, ql2, 'r-', linewidth=1.5, label='Left q2 (raw)', alpha=0.7)
  axes[2, 1].plot(time, q2_l_approx, 'b--', linewidth=2, label='Left q2 (polynomial)', alpha=0.8)
  axes[2, 1].set_xlabel('Time (seconds)', fontsize=12)
  axes[2, 1].set_ylabel('q2 (radians)', fontsize=12)
  axes[2, 1].set_title('Left: q2 vs time', fontsize=13, fontweight='bold')
  axes[2, 1].grid(True, alpha=0.3)
  axes[2, 1].legend()
  
  axes[3, 0].plot(time, dq2_r_dt, 'k-', linewidth=1.5, label='Right dq2/dt (raw)', alpha=0.7)
  axes[3, 0].plot(time, dq2_r_dt_approx, 'brown', linestyle='--', linewidth=2, label='Right dq2/dt (from polynomial)', alpha=0.8)
  axes[3, 0].set_xlabel('Time (seconds)', fontsize=12)
  axes[3, 0].set_ylabel('dq2/dt (radians/s)', fontsize=12)
  axes[3, 0].set_title('Right: dq2/dt vs time', fontsize=13, fontweight='bold')
  axes[3, 0].grid(True, alpha=0.3)
  axes[3, 0].legend()
  
  axes[3, 1].plot(time, dq2_l_dt, 'r-', linewidth=1.5, label='Left dq2/dt (raw)', alpha=0.7)
  axes[3, 1].plot(time, dq2_l_dt_approx, 'b--', linewidth=2, label='Left dq2/dt (from polynomial)', alpha=0.8)
  axes[3, 1].set_xlabel('Time (seconds)', fontsize=12)
  axes[3, 1].set_ylabel('dq2/dt (radians/s)', fontsize=12)
  axes[3, 1].set_title('Left: dq2/dt vs time', fontsize=13, fontweight='bold')
  axes[3, 1].grid(True, alpha=0.3)
  axes[3, 1].legend()
  
  plt.tight_layout()
  
  if save_path:
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"✅ Plot saved to: {save_path}")
  else:
    plt.show()
  
  return {
    'coefficients': {
      'right': {
        'phi_1': {
          'a': float(phi1_r_coeffs[0]),
          'b': float(phi1_r_coeffs[1]),
          'c': float(phi1_r_coeffs[2]),
          'd': float(phi1_r_coeffs[3])
        },
        'phi_3': {
          'a': float(phi3_r_coeffs[0]),
          'b': float(phi3_r_coeffs[1]),
          'c': float(phi3_r_coeffs[2]),
          'd': float(phi3_r_coeffs[3])
        },
        'q2_t': {
          'a': float(q2_r_coeffs[0]),
          'b': float(q2_r_coeffs[1]),
          'c': float(q2_r_coeffs[2]),
          'd': float(q2_r_coeffs[3]),
          'e': float(q2_r_coeffs[4]),
          'f': float(q2_r_coeffs[5])
        }
      },
      'left': {
        'phi_1': {
          'a': float(phi1_l_coeffs[0]),
          'b': float(phi1_l_coeffs[1]),
          'c': float(phi1_l_coeffs[2]),
          'd': float(phi1_l_coeffs[3])
        },
        'phi_3': {
          'a': float(phi3_l_coeffs[0]),
          'b': float(phi3_l_coeffs[1]),
          'c': float(phi3_l_coeffs[2]),
          'd': float(phi3_l_coeffs[3])
        },
        'q2_t': {
          'a': float(q2_l_coeffs[0]),
          'b': float(q2_l_coeffs[1]),
          'c': float(q2_l_coeffs[2]),
          'd': float(q2_l_coeffs[3]),
          'e': float(q2_l_coeffs[4]),
          'f': float(q2_l_coeffs[5])
        }
      }
    },
    'derivatives': {
      'right': {
        'dq2_dt': dq2_r_dt.tolist(),
        'dq2_dt_from_polynomial': dq2_r_dt_approx.tolist()
      },
      'left': {
        'dq2_dt': dq2_l_dt.tolist(),
        'dq2_dt_from_polynomial': dq2_l_dt_approx.tolist()
      }
    },
    'q2': {
      'right': qr2.tolist(),
      'left': ql2.tolist()
    },
    'time': time.tolist()
  }


def main():
  """Main function."""
  parser = argparse.ArgumentParser(
    description='Plot angle dependencies and approximate with 3rd degree polynomials: q1 = phi_1(q2), q3 = phi_3(q2)'
  )
  parser.add_argument(
    '--measurement',
    type=int,
    choices=[1, 2],
    help='Measurement number (1 or 2). If not specified, plot both.'
  )
  parser.add_argument(
    '--save',
    type=str,
    help='Save plot to file (e.g., dependencies.png)'
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
  parser.add_argument(
    '--save-json',
    type=str,
    help='Save approximation coefficients and derivatives to JSON file'
  )
  
  args = parser.parse_args()
  
  base_dir = Path(__file__).parent
  json_dir = base_dir / 'data' / 'calculated_angles'
  
  if args.measurement:
    json_path = json_dir / f'Measurement{args.measurement}_calculated_angles.json'
    if not json_path.exists():
      print(f"❌ Error: File {json_path} not found!")
      return
    
    print(f"📂 Reading: {json_path}")
    angles_data = load_angles_from_json(json_path)
    
    if args.start_frame is not None or args.end_frame is not None:
      num_frames = len(angles_data['angles']['right']['q1'])
      start = args.start_frame if args.start_frame is not None else 0
      end = args.end_frame if args.end_frame is not None else num_frames
      print(f"📊 Filtering data: frames {start} to {end} (total: {num_frames})")
    
    result_data = plot_angle_dependencies(
      angles_data, 
      f'Measurement{args.measurement}', 
      args.save,
      args.start_frame,
      args.end_frame
    )
    
    if args.save_json:
      save_approximation_data(result_data, angles_data, f'Measurement{args.measurement}', args.save_json)
  else:
    # Plot both measurements
    for meas_num in [1, 2]:
      json_path = json_dir / f'Measurement{meas_num}_calculated_angles.json'
      if not json_path.exists():
        print(f"⚠️  Warning: File {json_path} not found, skipping...")
        continue
      
      print(f"\n📂 Reading: {json_path}")
      angles_data = load_angles_from_json(json_path)
      
      if args.start_frame is not None or args.end_frame is not None:
        num_frames = len(angles_data['angles']['right']['q1'])
        start = args.start_frame if args.start_frame is not None else 0
        end = args.end_frame if args.end_frame is not None else num_frames
        print(f"📊 Filtering data: frames {start} to {end} (total: {num_frames})")
      
      result_data = plot_angle_dependencies(
        angles_data, 
        f'Measurement{meas_num}', 
        args.save,
        args.start_frame,
        args.end_frame
      )
      
      if args.save_json:
        json_path_save = args.save_json.replace('.json', f'_m{meas_num}.json') if args.save_json.endswith('.json') else f'{args.save_json}_m{meas_num}.json'
        save_approximation_data(result_data, angles_data, f'Measurement{meas_num}', json_path_save)
  
  print("\n✅ Done!")


if __name__ == "__main__":
  main()
