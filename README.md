# Biomech - Визуализация данных захвата движения

Проект для чтения и визуализации данных маркеров из системы захвата движения Qualisys.

## Установка зависимостей

```bash
pip install -r requirements.txt
```

## Запуск

### Интерактивный режим
```bash
python3 visualize_markers.py
```
Скрипт предложит выбрать файл для визуализации из доступных вариантов.

### Указание конкретного файла
```bash
python3 visualize_markers.py --file milana/Measurement1.tsv
```

### Сохранение анимации в файл
```bash
# Сохранить как GIF
python3 visualize_markers.py --file milana/Measurement1.tsv --save output.gif

# Сохранить как MP4 (требуется ffmpeg)
python3 visualize_markers.py --file clear_data/Measurement1.tsv --save output.mp4
```

### Управление скоростью анимации
```bash
# Показывать каждый 2-й кадр (ускорение в 2 раза)
python3 visualize_markers.py --skip-frames 2

# Изменить интервал между кадрами (мс)
python3 visualize_markers.py --interval 20
```

### Тестирование чтения данных
```bash
python3 test_read_data.py
```
Выводит информацию о данных без запуска GUI.

### Создание статических графиков
```bash
# Показать траектории и 2D проекции
python3 plot_markers_static.py milana/Measurement1.tsv

# Сохранить графики в файлы
python3 plot_markers_static.py milana/Measurement1.tsv \
  --save-trajectories trajectories.png \
  --save-projections projections.png

# Показать 2D проекции для конкретного кадра
python3 plot_markers_static.py clear_data/Measurement1.tsv --frame 100
```

## Структура данных

- `milana/` - данные захвата движения субъекта Milana (3D координаты маркеров)
- `clear_data/` - данные захвата движения субъекта Roman Eidelman (3D координаты маркеров)
- `Milana/` - обработанные угловые данные для обоих субъектов

## Формат файлов

TSV файлы содержат:
- Метаданные (количество кадров, частота, количество маркеров)
- 3D координаты (X, Y, Z) для каждого маркера в каждом кадре
- Частота захвата: 100 Hz
- Количество маркеров: 15
