# 🚀 Быстрый старт

## Установка (один раз)

```bash
pip install -r requirements.txt
```

## Что создано?

### 📜 Скрипты:

1. **`test_read_data.py`** - Проверка данных (без GUI)
2. **`plot_markers_static.py`** - Статические графики траекторий
3. **`visualize_markers.py`** - 3D анимация маркеров

### 📖 Документация:

- **`README.md`** - Полное описание проекта
- **`USAGE.md`** - Детальное руководство по всем функциям
- **`QUICKSTART.md`** - Этот файл

## Первый запуск

### Шаг 1: Проверить данные
```bash
python3 test_read_data.py
```

### Шаг 2: Посмотреть анимацию
```bash
python3 visualize_markers.py
```
Выберите файл из списка (или нажмите Enter для первого).

## Полезные команды

### Создать статические графики
```bash
python3 plot_markers_static.py clear_data/Measurement1.tsv \
  --save-trajectories trajectories.png \
  --save-projections projections.png
```

### Ускоренная анимация
```bash
python3 visualize_markers.py clear_data/Measurement1.tsv --skip-frames 5
```

### Сохранить анимацию в GIF
```bash
python3 visualize_markers.py clear_data/Measurement1.tsv --save animation.gif
```

## Доступные данные
- `clear_data/Measurement1.tsv`
- `clear_data/Measurement2.tsv`

## Помощь

Для любого скрипта:
```bash
python3 <script_name>.py --help
```

Подробности в **`USAGE.md`**
