#!/usr/bin/env python3
"""
Тестовый скрипт для проверки чтения данных маркеров без GUI.
Просто выводит информацию о данных в консоль.
"""

from visualize_markers import MarkerDataReader
from pathlib import Path
import argparse
import sys


def main():
  """Главная функция для тестирования чтения данных."""
  
  # Парсинг аргументов командной строки
  parser = argparse.ArgumentParser(
    description='Проверка чтения данных маркеров из TSV файлов'
  )
  parser.add_argument(
    'files',
    nargs='*',
    help='Пути к TSV файлам для проверки (если не указаны, используются файлы по умолчанию)'
  )
  
  args = parser.parse_args()
  
  project_root = Path(__file__).parent
  
  # Если файлы указаны в аргументах, используем их
  if args.files:
    test_files = []
    for file_path in args.files:
      path = Path(file_path)
      # Если путь относительный, делаем его относительно текущей директории
      if not path.is_absolute():
        path = Path.cwd() / path
      test_files.append(path)
  else:
    # Список файлов по умолчанию для тестирования
    test_files = [
      project_root / 'data' / 'Measurement1.tsv',
      project_root / 'data' / 'Measurement2.tsv',
    ]
  
  for file_path in test_files:
    if not file_path.exists():
      print(f"⚠️  Файл не найден: {file_path}")
      continue
    
    print(f"\n{'='*60}")
    print(f"Чтение файла: {file_path.relative_to(project_root)}")
    print(f"{'='*60}")
    
    # Читаем данные
    reader = MarkerDataReader(file_path)
    data = reader.read_file()
    
    # Выводим метаданные
    print("\n📊 Метаданные:")
    for key, value in data['metadata'].items():
      print(f"  {key}: {value}")
    
    # Выводим информацию о маркерах
    print(f"\n🎯 Маркеры ({len(data['marker_names'])} шт.):")
    print("  Простые имена и оригинальные:")
    for i in range(min(5, len(data['marker_names']))):
      simple_name = data['simple_names'][i] if 'simple_names' in data else f"m{i+1}"
      orig_name = data['marker_names'][i]
      print(f"  {simple_name} ({orig_name})")
    if len(data['marker_names']) > 5:
      print(f"  ... и еще {len(data['marker_names']) - 5}")
    
    # Выводим информацию о данных
    print(f"\n📈 Данные:")
    print(f"  Форма массива: {data['frames'].shape}")
    print(f"  (кадры, маркеры, координаты XYZ)")
    
    # Выводим пример первого кадра
    print(f"\n🔍 Первый кадр (первые 3 маркера):")
    for i in range(min(3, len(data['marker_names']))):
      simple_name = data['simple_names'][i] if 'simple_names' in data else data['marker_names'][i]
      x, y, z = data['frames'][0, i, :]
      print(f"  {simple_name}:")
      print(f"    X: {x:8.3f} mm")
      print(f"    Y: {y:8.3f} mm")
      print(f"    Z: {z:8.3f} mm")
    
    # Статистика по движению
    print(f"\n📉 Статистика движения (все кадры):")
    for axis_idx, axis_name in enumerate(['X', 'Y', 'Z']):
      axis_data = data['frames'][:, :, axis_idx]
      print(f"  {axis_name}: min={axis_data.min():8.2f}, max={axis_data.max():8.2f}, "
            f"mean={axis_data.mean():8.2f} mm")
  
  print(f"\n{'='*60}")
  print("✅ Тестирование завершено!")
  print(f"{'='*60}\n")


if __name__ == "__main__":
  main()
