# 📝 Примеры использования скриптов

## 1️⃣ test_read_data.py - Проверка данных

### Базовое использование
```bash
# Файлы по умолчанию (clear_data/Measurement1.tsv и Measurement2.tsv)
python3 test_read_data.py
```

### Указание конкретного файла
```bash
# Относительный путь от текущей директории
python3 test_read_data.py clear_data/Measurement1.tsv

# Полный (абсолютный) путь
python3 test_read_data.py /home/user/biomech/clear_data/Measurement1.tsv

# Файл в другой директории
python3 test_read_data.py /path/to/your/data.tsv
```

### Проверка нескольких файлов
```bash
# Несколько файлов сразу
python3 test_read_data.py clear_data/Measurement1.tsv clear_data/Measurement2.tsv

# Комбинация путей
python3 test_read_data.py clear_data/Measurement1.tsv /home/user/other_data.tsv
```

---

## 2️⃣ visualize_markers.py - Анимация

### Интерактивный режим
```bash
# Выбор из списка
python3 visualize_markers.py
```

### Указание файла
```bash
# Относительный путь (проще всего)
python3 visualize_markers.py clear_data/Measurement1.tsv

# Полный путь
python3 visualize_markers.py /home/user/biomech/clear_data/Measurement1.tsv
```

### С параметрами
```bash
# Ускорить в 5 раз (каждый 5-й кадр)
python3 visualize_markers.py clear_data/Measurement1.tsv --skip-frames 5

# Замедлить (100 мс между кадрами)
python3 visualize_markers.py clear_data/Measurement1.tsv --interval 100

# Комбинация параметров
python3 visualize_markers.py clear_data/Measurement1.tsv --skip-frames 2 --interval 20
```

### Сохранение
```bash
# Сохранить как GIF
python3 visualize_markers.py clear_data/Measurement1.tsv --save output.gif

# Сохранить как MP4 (нужен ffmpeg)
python3 visualize_markers.py clear_data/Measurement1.tsv --save output.mp4

# Сохранить с ускорением
python3 visualize_markers.py clear_data/Measurement1.tsv --skip-frames 5 --save fast.gif
```

---

## 3️⃣ plot_markers_static.py - Статические графики

### Просмотр графиков
```bash
# Относительный путь
python3 plot_markers_static.py clear_data/Measurement1.tsv

# Полный путь
python3 plot_markers_static.py /home/user/biomech/clear_data/Measurement1.tsv
```

### Сохранение графиков
```bash
# Сохранить оба графика
python3 plot_markers_static.py clear_data/Measurement1.tsv \
  --save-trajectories trajectories.png \
  --save-projections projections.png

# Только траектории
python3 plot_markers_static.py clear_data/Measurement1.tsv \
  --save-trajectories trajectories.png

# Только проекции
python3 plot_markers_static.py clear_data/Measurement1.tsv \
  --save-projections projections.png
```

### Анализ конкретного кадра
```bash
# Показать кадр 500
python3 plot_markers_static.py clear_data/Measurement1.tsv --frame 500

# Кадр 1000 и сохранить
python3 plot_markers_static.py clear_data/Measurement1.tsv \
  --frame 1000 \
  --save-projections frame_1000.png
```

---

## 💡 Полезные комбинации

### Быстрая проверка новых данных
```bash
# 1. Проверить что файл читается
python3 test_read_data.py /path/to/new/data.tsv

# 2. Посмотреть статические графики
python3 plot_markers_static.py /path/to/new/data.tsv

# 3. Посмотреть анимацию
python3 visualize_markers.py /path/to/new/data.tsv
```

### Создание презентационных материалов
```bash
# Статические графики для слайдов
python3 plot_markers_static.py clear_data/Measurement1.tsv \
  --save-trajectories traj_measurement1.png \
  --save-projections proj_measurement1.png

# Короткая быстрая анимация для видео
python3 visualize_markers.py clear_data/Measurement1.tsv \
  --skip-frames 5 \
  --save presentation.gif
```

### Анализ разных кадров
```bash
# Начало движения (кадр 0)
python3 plot_markers_static.py clear_data/Measurement1.tsv --frame 0 \
  --save-projections start.png

# Середина движения (кадр 1000)
python3 plot_markers_static.py clear_data/Measurement1.tsv --frame 1000 \
  --save-projections middle.png

# Конец движения (кадр 1999)
python3 plot_markers_static.py clear_data/Measurement1.tsv --frame 1999 \
  --save-projections end.png
```

---

## 🔍 Проверка доступных опций

Для любого скрипта можно посмотреть полный список опций:

```bash
python3 test_read_data.py --help
python3 visualize_markers.py --help
python3 plot_markers_static.py --help
```
