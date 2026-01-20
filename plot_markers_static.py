#!/usr/bin/env python3
"""
Скрипт для создания статических графиков траекторий маркеров.
Полезно для быстрого анализа данных без запуска полной анимации.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from visualize_markers import MarkerDataReader
import argparse


def plot_marker_trajectories(frames_data, marker_names, title="Marker Trajectories"):
  """
  Создает график траекторий всех маркеров в 3D.
  
  Args:
    frames_data: Массив данных (кадры, маркеры, XYZ)
    marker_names: Список имен маркеров
    title: Заголовок графика
  """
  # Создаем фигуру с 3D графиком
  fig = plt.figure(figsize=(14, 10))
  ax = fig.add_subplot(111, projection='3d')
  
  # Генерируем цвета для каждого маркера
  colors = plt.cm.rainbow(np.linspace(0, 1, len(marker_names)))
  
  # Рисуем траекторию для каждого маркера
  for marker_idx, (marker_name, color) in enumerate(zip(marker_names, colors)):
    # Извлекаем траекторию маркера (все кадры)
    trajectory = frames_data[:, marker_idx, :]
    
    # Рисуем линию траектории
    ax.plot(
      trajectory[:, 0],
      trajectory[:, 1],
      trajectory[:, 2],
      color=color,
      alpha=0.6,
      linewidth=1,
      label=marker_name
    )
    
    # Отмечаем начальную позицию
    ax.scatter(
      trajectory[0, 0],
      trajectory[0, 1],
      trajectory[0, 2],
      color=color,
      s=100,
      marker='o',
      edgecolors='black',
      linewidths=2
    )
  
  # Настройка осей
  ax.set_xlabel('X (mm)')
  ax.set_ylabel('Y (mm)')
  ax.set_zlabel('Z (mm)')
  ax.set_title(title)
  
  # Добавляем легенду (только первые 8 маркеров, чтобы не загромождать)
  if len(marker_names) <= 8:
    ax.legend(loc='upper right', fontsize=8)
  
  # Устанавливаем одинаковый масштаб для всех осей
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


def plot_marker_positions_2d(frames_data, marker_names, frame_idx=0):
  """
  Создает 2D проекции позиций маркеров для конкретного кадра.
  
  Args:
    frames_data: Массив данных (кадры, маркеры, XYZ)
    marker_names: Список имен маркеров
    frame_idx: Индекс кадра для отображения
  """
  # Создаем фигуру с тремя подграфиками (проекции XY, XZ, YZ)
  fig, axes = plt.subplots(1, 3, figsize=(18, 6))
  
  # Извлекаем данные для указанного кадра
  frame_data = frames_data[frame_idx]
  
  # Проекция XY
  axes[0].scatter(frame_data[:, 0], frame_data[:, 1], s=100, c='red', alpha=0.7)
  for i, name in enumerate(marker_names):
    axes[0].annotate(name, (frame_data[i, 0], frame_data[i, 1]), 
                    fontsize=8, alpha=0.7)
  axes[0].set_xlabel('X (mm)')
  axes[0].set_ylabel('Y (mm)')
  axes[0].set_title('Проекция XY (вид сверху)')
  axes[0].grid(True, alpha=0.3)
  axes[0].set_aspect('equal', adjustable='box')
  
  # Проекция XZ
  axes[1].scatter(frame_data[:, 0], frame_data[:, 2], s=100, c='green', alpha=0.7)
  for i, name in enumerate(marker_names):
    axes[1].annotate(name, (frame_data[i, 0], frame_data[i, 2]), 
                    fontsize=8, alpha=0.7)
  axes[1].set_xlabel('X (mm)')
  axes[1].set_ylabel('Z (mm)')
  axes[1].set_title('Проекция XZ (вид сбоку)')
  axes[1].grid(True, alpha=0.3)
  axes[1].set_aspect('equal', adjustable='box')
  
  # Проекция YZ
  axes[2].scatter(frame_data[:, 1], frame_data[:, 2], s=100, c='blue', alpha=0.7)
  for i, name in enumerate(marker_names):
    axes[2].annotate(name, (frame_data[i, 1], frame_data[i, 2]), 
                    fontsize=8, alpha=0.7)
  axes[2].set_xlabel('Y (mm)')
  axes[2].set_ylabel('Z (mm)')
  axes[2].set_title('Проекция YZ (вид спереди)')
  axes[2].grid(True, alpha=0.3)
  axes[2].set_aspect('equal', adjustable='box')
  
  fig.suptitle(f'Позиции маркеров - Кадр {frame_idx + 1}', fontsize=14)
  fig.tight_layout()
  
  return fig


def main():
  """Главная функция."""
  # Парсинг аргументов
  parser = argparse.ArgumentParser(
    description='Создание статических графиков траекторий маркеров'
  )
  parser.add_argument(
    'file',
    type=str,
    help='Путь к TSV файлу с данными маркеров'
  )
  parser.add_argument(
    '--frame',
    type=int,
    default=0,
    help='Номер кадра для 2D проекций (по умолчанию: 0)'
  )
  parser.add_argument(
    '--save-trajectories',
    type=str,
    help='Сохранить график траекторий в файл'
  )
  parser.add_argument(
    '--save-projections',
    type=str,
    help='Сохранить 2D проекции в файл'
  )
  
  args = parser.parse_args()
  
  # Путь к файлу
  file_path = Path(args.file)
  if not file_path.exists():
    print(f"❌ Ошибка: Файл {file_path} не найден!")
    return
  
  print(f"📂 Чтение файла: {file_path}")
  
  # Читаем данные
  reader = MarkerDataReader(file_path)
  data = reader.read_file()
  
  print(f"✅ Прочитано {len(data['frames'])} кадров, {len(data['marker_names'])} маркеров")
  
  # Создаем график траекторий
  print("\n🎨 Создание графика траекторий...")
  fig_traj = plot_marker_trajectories(
    data['frames'],
    data['marker_names'],
    title=f"Траектории маркеров - {file_path.stem}"
  )
  
  if args.save_trajectories:
    print(f"💾 Сохранение графика траекторий: {args.save_trajectories}")
    fig_traj.savefig(args.save_trajectories, dpi=150, bbox_inches='tight')
    print(f"✅ Сохранено: {args.save_trajectories}")
  
  # Создаем 2D проекции
  print(f"\n🎨 Создание 2D проекций для кадра {args.frame + 1}...")
  fig_proj = plot_marker_positions_2d(
    data['frames'],
    data['marker_names'],
    frame_idx=args.frame
  )
  
  if args.save_projections:
    print(f"💾 Сохранение 2D проекций: {args.save_projections}")
    fig_proj.savefig(args.save_projections, dpi=150, bbox_inches='tight')
    print(f"✅ Сохранено: {args.save_projections}")
  
  # Показываем графики, если не сохраняем
  if not args.save_trajectories and not args.save_projections:
    print("\n📊 Отображение графиков...")
    plt.show()
  elif not args.save_trajectories or not args.save_projections:
    print("\n📊 Отображение графиков...")
    plt.show()
  
  print("\n✅ Готово!")


if __name__ == "__main__":
  main()
