# 🚀 Шпаргалка по использованию скриптов

## Самые частые команды

### 1. Проверить данные
```bash
# Файлы по умолчанию
python3 test_read_data.py

# Конкретный файл
python3 test_read_data.py data/Measurement1.tsv

# Ваш файл
python3 test_read_data.py /path/to/your/file.tsv
```

### 2. Посмотреть анимацию
```bash
# Интерактивный выбор
python3 visualize_markers.py

# Конкретный файл
python3 visualize_markers.py data/Measurement1.tsv

# Ваш файл
python3 visualize_markers.py /path/to/your/file.tsv
```

### 3. Создать картинки
```bash
# Просмотр
python3 plot_markers_static.py data/Measurement1.tsv

# Сохранить
python3 plot_markers_static.py data/Measurement1.tsv \
  --save-trajectories trajectories.png \
  --save-projections projections.png
```

---

## Полезные опции

### Ускорить анимацию (каждый 5-й кадр)
```bash
python3 visualize_markers.py data/Measurement1.tsv --skip-frames 5
```

### Замедлить анимацию (100 мс между кадрами)
```bash
python3 visualize_markers.py data/Measurement1.tsv --interval 100
```

### Сохранить анимацию в GIF
```bash
python3 visualize_markers.py data/Measurement1.tsv --save animation.gif
```

### Посмотреть конкретный кадр
```bash
python3 plot_markers_static.py data/Measurement1.tsv --frame 500
```

---

## Типы путей

### Относительный путь (от текущей папки)
```bash
python3 test_read_data.py data/Measurement1.tsv
```

### Полный путь
```bash
python3 test_read_data.py /home/user/biomech/data/Measurement1.tsv
```

### Несколько файлов
```bash
python3 test_read_data.py data/Measurement1.tsv data/Measurement2.tsv
```

---

## Справка

```bash
python3 test_read_data.py --help
python3 visualize_markers.py --help
python3 plot_markers_static.py --help
```

---

## Подробности

- **EXAMPLES.md** - полный список примеров
- **USAGE.md** - детальное руководство
- **QUICKSTART.md** - быстрый старт
- **README.md** - полная документация
