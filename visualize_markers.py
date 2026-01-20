#!/usr/bin/env python3
"""
Скрипт для чтения и визуализации данных маркеров захвата движения.
Читает TSV файлы из папок clear_data/ и milana/ и создает 3D анимацию.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pathlib import Path
from typing import Dict, Tuple, List


class MarkerDataReader:
  """Класс для чтения данных маркеров из TSV файлов."""
  
  def __init__(self, file_path: str):
    """
    Инициализация ридера.
    
    Args:
      file_path: Путь к TSV файлу с данными маркеров
    """
    self.file_path = Path(file_path)
    self.metadata = {}
    self.marker_names = []
    self.simple_names = []  # Простые имена типа r1, l1
    self.frames_data = None
    
  def read_file(self) -> Dict:
    """
    Читает TSV файл и извлекает метаданные и данные маркеров.
    
    Returns:
      Словарь с метаданными и данными маркеров
    """
    with open(self.file_path, 'r') as f:
      lines = f.readlines()
    
    # Парсим метаданные (первые строки до строки с заголовками)
    data_start_line = 0
    for i, line in enumerate(lines):
      if line.startswith('Frame\t'):
        # Нашли строку с заголовками столбцов
        data_start_line = i + 1
        # Извлекаем имена маркеров из заголовка
        self._parse_marker_names(lines[i])
        break
      else:
        # Парсим метаданные
        self._parse_metadata_line(line)
    
    # Читаем данные маркеров начиная со строки data_start_line
    self._parse_marker_data(lines[data_start_line:])
    
    # Создаем простые имена маркеров (l1, l2, r1, r2 и т.д.)
    self._create_simple_names()
    
    return {
      'metadata': self.metadata,
      'marker_names': self.marker_names,
      'simple_names': self.simple_names,
      'frames': self.frames_data
    }
  
  def _parse_metadata_line(self, line: str):
    """
    Парсит строку метаданных.
    
    Args:
      line: Строка с метаданными в формате "KEY\tVALUE"
    """
    parts = line.strip().split('\t')
    if len(parts) >= 2:
      key = parts[0]
      value = parts[1]
      self.metadata[key] = value
  
  def _parse_marker_names(self, header_line: str):
    """
    Извлекает имена маркеров из строки заголовков.
    
    Args:
      header_line: Строка с заголовками столбцов
    """
    # Разбиваем строку по табуляции
    columns = header_line.strip().split('\t')
    
    # Пропускаем "Frame" и "Time", остальное - координаты маркеров
    # Формат: "MarkerName X", "MarkerName Y", "MarkerName Z"
    marker_set = []
    for col in columns[2:]:  # Пропускаем Frame и Time
      # Убираем суффиксы X, Y, Z
      marker_name = col.rsplit(' ', 1)[0]
      if marker_name not in marker_set:
        marker_set.append(marker_name)
    
    self.marker_names = marker_set
  
  def _parse_marker_data(self, data_lines: List[str]):
    """
    Парсит данные маркеров из строк файла.
    
    Args:
      data_lines: Список строк с данными кадров
    """
    num_markers = len(self.marker_names)
    num_frames = len(data_lines)
    
    # Создаем массив для хранения данных: (кадры, маркеры, координаты XYZ)
    self.frames_data = np.zeros((num_frames, num_markers, 3))
    
    for frame_idx, line in enumerate(data_lines):
      # Разбиваем строку по табуляции
      values = line.strip().split('\t')
      
      # Пропускаем Frame и Time (первые два столбца)
      coords = values[2:]
      
      # Заполняем координаты для каждого маркера
      for marker_idx in range(num_markers):
        x_idx = marker_idx * 3
        y_idx = marker_idx * 3 + 1
        z_idx = marker_idx * 3 + 2
        
        # Конвертируем строки в числа
        if x_idx < len(coords) and y_idx < len(coords) and z_idx < len(coords):
          self.frames_data[frame_idx, marker_idx, 0] = float(coords[x_idx])
          self.frames_data[frame_idx, marker_idx, 1] = float(coords[y_idx])
          self.frames_data[frame_idx, marker_idx, 2] = float(coords[z_idx])
  
  def _create_simple_names(self):
    """
    Создает простые имена для маркеров и фильтрует ненужные.
    Определяет лево/право на основе средней координаты Y, затем фильтрует
    и переименовывает оставшиеся маркеры как 1, 2, 3...
    """
    # Вычисляем среднюю позицию каждого маркера по всем кадрам
    mean_positions = np.mean(self.frames_data, axis=0)  # (маркеры, XYZ)
    
    # Определяем центр по Y-координате
    center_y = np.mean(mean_positions[:, 1])
    
    # Разделяем маркеры на левые (Y < center_y) и правые (Y >= center_y)
    left_markers = []
    right_markers = []
    
    for idx in range(len(self.marker_names)):
      marker_y = mean_positions[idx, 1]
      if marker_y < center_y:
        left_markers.append((idx, marker_y))
      else:
        right_markers.append((idx, marker_y))
    
    # Сортируем по Y-координате (от меньшего к большему)
    left_markers.sort(key=lambda x: x[1])
    right_markers.sort(key=lambda x: x[1])
    
    # Создаем временный словарь для маппинга индекса маркера -> временное имя (l1, r1...)
    temp_name_map = {}
    
    for i, (marker_idx, _) in enumerate(left_markers):
      temp_name_map[marker_idx] = f'l{i+1}'
    
    for i, (marker_idx, _) in enumerate(right_markers):
      temp_name_map[marker_idx] = f'r{i+1}'
    
    # Список маркеров для исключения
    markers_to_exclude = ['l1', 'l6', 'l5', 'r5', 'r8', 'r2']
    
    # Определяем индексы маркеров, которые нужно оставить
    indices_to_keep = []
    for idx in range(len(self.marker_names)):
      if temp_name_map[idx] not in markers_to_exclude:
        indices_to_keep.append(idx)
    
    # Фильтруем данные маркеров
    self.frames_data = self.frames_data[:, indices_to_keep, :]
    
    # Фильтруем оригинальные имена
    self.marker_names = [self.marker_names[i] for i in indices_to_keep]
    
    # Создаем новые простые имена (просто 1, 2, 3...)
    self.simple_names = [str(i+1) for i in range(len(self.marker_names))]


class MarkerAnimator:
  """Класс для создания 3D анимации маркеров."""
  
  def __init__(self, frames_data: np.ndarray, marker_names: List[str], 
               simple_names: List[str] = None, title: str = "Marker Animation"):
    """
    Инициализация аниматора.
    
    Args:
      frames_data: Массив данных маркеров (кадры, маркеры, XYZ)
      marker_names: Список имен маркеров
      simple_names: Список простых имен маркеров (l1, r1 и т.д.)
      title: Заголовок анимации
    """
    self.frames_data = frames_data
    self.marker_names = marker_names
    self.simple_names = simple_names if simple_names else marker_names
    self.title = title
    self.fig = None
    self.ax = None
    self.scatter = None
    self.labels = []  # Текстовые подписи для маркеров
    
  def setup_plot(self):
    """Настраивает 3D график для анимации."""
    # Создаем фигуру и 3D оси
    self.fig = plt.figure(figsize=(12, 9))
    self.ax = self.fig.add_subplot(111, projection='3d')
    
    # Вычисляем границы для осей (используем все кадры)
    all_x = self.frames_data[:, :, 0].flatten()
    all_y = self.frames_data[:, :, 1].flatten()
    all_z = self.frames_data[:, :, 2].flatten()
    
    # Устанавливаем одинаковый масштаб для всех осей
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
    
    # Подписи осей
    self.ax.set_xlabel('X (mm)')
    self.ax.set_ylabel('Y (mm)')
    self.ax.set_zlabel('Z (mm)')
    self.ax.set_title(self.title)
    
    # Создаем начальный scatter plot (первый кадр)
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
    
    # Добавляем подписи для каждого маркера
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
    Обновляет позиции маркеров для текущего кадра.
    
    Args:
      frame_num: Номер кадра для отображения
    """
    # Получаем данные для текущего кадра
    current_frame = self.frames_data[frame_num]
    
    # Обновляем позиции точек
    self.scatter._offsets3d = (
      current_frame[:, 0],
      current_frame[:, 1],
      current_frame[:, 2]
    )
    
    # Обновляем позиции подписей
    for i, (x, y, z) in enumerate(current_frame):
      self.labels[i].set_position((x, y))
      self.labels[i].set_3d_properties(z, 'z')
    
    # Обновляем заголовок с номером кадра
    self.ax.set_title(f'{self.title} - Frame {frame_num + 1}/{len(self.frames_data)}')
    
    return [self.scatter] + self.labels
  
  def animate(self, interval: int = 10, skip_frames: int = 1):
    """
    Запускает анимацию.
    
    Args:
      interval: Интервал между кадрами в миллисекундах
      skip_frames: Количество кадров для пропуска (для ускорения)
    
    Returns:
      Объект анимации
    """
    # Настраиваем график
    self.setup_plot()
    
    # Создаем анимацию
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
  """Главная функция для запуска визуализации."""
  import argparse
  
  # Парсинг аргументов командной строки
  parser = argparse.ArgumentParser(
    description='Визуализация данных маркеров захвата движения'
  )
  parser.add_argument(
    'file',
    nargs='?',
    type=str,
    help='Путь к TSV файлу (если не указан, будет интерактивный выбор)'
  )
  parser.add_argument(
    '--save',
    type=str,
    help='Сохранить анимацию в файл (например: output.gif или output.mp4)'
  )
  parser.add_argument(
    '--skip-frames',
    type=int,
    default=1,
    help='Пропускать каждые N кадров для ускорения (по умолчанию: 1)'
  )
  parser.add_argument(
    '--interval',
    type=int,
    default=10,
    help='Интервал между кадрами в мс (по умолчанию: 10)'
  )
  
  args = parser.parse_args()
  
  # Путь к корневой директории проекта
  project_root = Path(__file__).parent
  
  # Если файл указан через аргумент
  if args.file:
    selected_file = Path(args.file)
    # Если путь относительный, проверяем относительно текущей директории
    if not selected_file.is_absolute():
      # Сначала проверим относительно текущей директории
      if (Path.cwd() / selected_file).exists():
        selected_file = Path.cwd() / selected_file
      else:
        # Если не нашли, пробуем относительно директории проекта
        selected_file = project_root / selected_file
  else:
    # Список файлов для визуализации
    files_to_visualize = [
      project_root / 'milana' / 'Measurement1.tsv',
      project_root / 'data' / 'Measurement1.tsv',
    ]
    
    # Выбираем файл для визуализации
    print("Доступные файлы для визуализации:")
    for idx, file_path in enumerate(files_to_visualize):
      print(f"{idx + 1}. {file_path.relative_to(project_root)}")
    
    # Запрашиваем выбор пользователя
    choice = input("\nВыберите номер файла (или нажмите Enter для первого): ").strip()
    
    if choice == "":
      selected_idx = 0
    else:
      try:
        selected_idx = int(choice) - 1
        if selected_idx < 0 or selected_idx >= len(files_to_visualize):
          print("Неверный выбор. Используем первый файл.")
          selected_idx = 0
      except ValueError:
        print("Неверный ввод. Используем первый файл.")
        selected_idx = 0
    
    selected_file = files_to_visualize[selected_idx]
  
  # Проверяем существование файла
  if not selected_file.exists():
    print(f"Ошибка: Файл {selected_file} не найден!")
    return
  
  print(f"\nЧтение файла: {selected_file}")
  
  # Читаем данные маркеров
  reader = MarkerDataReader(selected_file)
  data = reader.read_file()
  
  # Выводим информацию о данных
  print(f"\n{'='*60}")
  print(f"📊 Метаданные:")
  print(f"  Количество кадров: {data['metadata'].get('NO_OF_FRAMES', 'N/A')}")
  print(f"  Количество маркеров: {data['metadata'].get('NO_OF_MARKERS', 'N/A')}")
  print(f"  Частота: {data['metadata'].get('FREQUENCY', 'N/A')} Hz")
  print(f"  Количество камер: {data['metadata'].get('NO_OF_CAMERAS', 'N/A')}")
  
  print(f"\n🎯 Маркеры:")
  print(f"  Первые 5: {', '.join(data['marker_names'][:5])}")
  print(f"  Всего маркеров: {len(data['marker_names'])}")
  print(f"  Форма данных: {data['frames'].shape} (кадры, маркеры, XYZ)")
  print(f"{'='*60}")
  
  # Создаем и запускаем анимацию
  print("\n🎬 Создание анимации...")
  
  animator = MarkerAnimator(
    data['frames'],
    data['marker_names'],
    data['simple_names'],
    title=f"Markers - {selected_file.stem}"
  )
  
  # Параметры анимации
  # interval: задержка между кадрами в мс
  # skip_frames: пропуск кадров для ускорения
  anim = animator.animate(interval=args.interval, skip_frames=args.skip_frames)
  
  # Сохраняем или показываем анимацию
  if args.save:
    print(f"\n💾 Сохранение анимации в файл: {args.save}")
    print("   (это может занять несколько минут...)")
    
    # Определяем writer в зависимости от расширения файла
    if args.save.endswith('.gif'):
      writer = 'pillow'
    elif args.save.endswith('.mp4'):
      writer = 'ffmpeg'
    else:
      writer = None
    
    try:
      anim.save(args.save, writer=writer, fps=int(1000/args.interval))
      print(f"✅ Анимация сохранена: {args.save}")
    except Exception as e:
      print(f"❌ Ошибка при сохранении: {e}")
      print("   Попробуйте установить: sudo apt-get install ffmpeg")
  else:
    print("\n▶️  Анимация запущена. Закройте окно для завершения.")
    plt.show()


if __name__ == "__main__":
  main()
