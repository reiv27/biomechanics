# 📖 Как использовать скрипты - Полное руководство

## 🎯 Основное использование

### Способ 1: Самый простой (указываем только путь к файлу)

```bash
# Проверить данные
python3 test_read_data.py data/Measurement1.tsv

# Посмотреть анимацию
python3 visualize_markers.py data/Measurement1.tsv

# Создать графики
python3 plot_markers_static.py data/Measurement1.tsv
```

### Способ 2: С полным путем

```bash
# Если ваш файл где-то в другом месте
python3 test_read_data.py /home/user/my_data/experiment1.tsv
python3 visualize_markers.py /home/user/my_data/experiment1.tsv
python3 plot_markers_static.py /home/user/my_data/experiment1.tsv
```

### Способ 3: Интерактивный (для visualize_markers.py)

```bash
# Просто запустите без аргументов
python3 visualize_markers.py

# Скрипт покажет список доступных файлов
# Выберите нужный номер или нажмите Enter
```

---

## 🔥 Частые сценарии использования

### Сценарий 1: Быстро проверить новый файл

```bash
# 1. Проверить что файл читается правильно
python3 test_read_data.py /path/to/new_file.tsv

# 2. Посмотреть анимацию
python3 visualize_markers.py /path/to/new_file.tsv
```

### Сценарий 2: Создать материалы для презентации

```bash
# 1. Создать статические картинки
python3 plot_markers_static.py data/Measurement1.tsv \
  --save-trajectories trajectories.png \
  --save-projections projections.png

# 2. Создать короткую GIF-анимацию
python3 visualize_markers.py data/Measurement1.tsv \
  --skip-frames 5 \
  --save animation.gif
```

### Сценарий 3: Анализ нескольких файлов

```bash
# Проверить несколько файлов одной командой
python3 test_read_data.py data/Measurement1.tsv data/Measurement2.tsv
```

### Сценарий 4: Ускоренная/замедленная анимация

```bash
# Ускорить в 10 раз (для длинных записей)
python3 visualize_markers.py data/Measurement1.tsv --skip-frames 10

# Замедлить (для детального анализа)
python3 visualize_markers.py data/Measurement1.tsv --interval 50
```

---

## 📂 Работа с путями

### Относительные пути (рекомендуется)

```bash
# Если вы в папке проекта /home/user/biomech
python3 test_read_data.py data/Measurement1.tsv

# Если вы в другой папке
cd /home/user
python3 biomech/test_read_data.py biomech/data/Measurement1.tsv
```

### Абсолютные пути

```bash
# Всегда работает, независимо от текущей директории
python3 test_read_data.py /home/user/biomech/data/Measurement1.tsv
```

### Файлы в других местах

```bash
# Ваши данные могут быть где угодно
python3 test_read_data.py /mnt/data/experiments/subject1.tsv
python3 visualize_markers.py ~/Desktop/my_data.tsv
```

---

## 🎨 Все параметры

### test_read_data.py

```bash
# Без аргументов - файлы по умолчанию
python3 test_read_data.py

# Один файл
python3 test_read_data.py path/to/file.tsv

# Несколько файлов
python3 test_read_data.py file1.tsv file2.tsv file3.tsv

# Справка
python3 test_read_data.py --help
```

### visualize_markers.py

```bash
# Интерактивный режим
python3 visualize_markers.py

# Указать файл
python3 visualize_markers.py path/to/file.tsv

# С параметрами
python3 visualize_markers.py path/to/file.tsv \
  --skip-frames 5 \
  --interval 50 \
  --save output.gif

# Справка
python3 visualize_markers.py --help
```

**Параметры:**
- `--skip-frames N` - показывать каждый N-й кадр (ускорение)
- `--interval N` - задержка между кадрами в миллисекундах
- `--save FILE` - сохранить в файл (.gif или .mp4)

### plot_markers_static.py

```bash
# Просмотр
python3 plot_markers_static.py path/to/file.tsv

# Сохранение
python3 plot_markers_static.py path/to/file.tsv \
  --save-trajectories traj.png \
  --save-projections proj.png

# Конкретный кадр
python3 plot_markers_static.py path/to/file.tsv --frame 500

# Справка
python3 plot_markers_static.py --help
```

**Параметры:**
- `--frame N` - номер кадра для 2D проекций
- `--save-trajectories FILE` - сохранить график траекторий
- `--save-projections FILE` - сохранить 2D проекции

---

## 💡 Полезные советы

### Для медленных компьютеров
```bash
# Показывать каждый 10-й кадр
python3 visualize_markers.py data/Measurement1.tsv --skip-frames 10
```

### Для детального анализа
```bash
# Замедленная анимация
python3 visualize_markers.py data/Measurement1.tsv --interval 100

# Посмотреть конкретный кадр
python3 plot_markers_static.py data/Measurement1.tsv --frame 1000
```

### Для создания видео (требуется ffmpeg)
```bash
# Установить ffmpeg
sudo apt-get install ffmpeg

# Создать MP4
python3 visualize_markers.py data/Measurement1.tsv --save video.mp4
```

---

## 📚 Где найти больше информации

- **CHEATSHEET.md** - быстрая шпаргалка (самое частое)
- **EXAMPLES.md** - подробные примеры всех возможностей
- **QUICKSTART.md** - быстрый старт для новичков
- **USAGE.md** - детальное руководство по всем функциям
- **README.md** - полная документация проекта
- **CHANGELOG.md** - что изменилось в новой версии

---

## ❓ Частые вопросы

**Q: Как указать путь к моему файлу?**
```bash
# Просто укажите путь после названия скрипта
python3 test_read_data.py /path/to/your/file.tsv
```

**Q: Можно ли проверить несколько файлов сразу?**
```bash
# Да, для test_read_data.py
python3 test_read_data.py file1.tsv file2.tsv file3.tsv
```

**Q: Как сохранить анимацию в файл?**
```bash
# Добавьте --save
python3 visualize_markers.py data/Measurement1.tsv --save output.gif
```

**Q: Анимация слишком быстрая, как замедлить?**
```bash
# Увеличьте интервал (в миллисекундах)
python3 visualize_markers.py data/Measurement1.tsv --interval 50
```

**Q: Анимация слишком медленная, как ускорить?**
```bash
# Пропускайте кадры (каждый 5-й кадр)
python3 visualize_markers.py data/Measurement1.tsv --skip-frames 5
```

**Q: Где посмотреть все опции?**
```bash
# Добавьте --help к любому скрипту
python3 visualize_markers.py --help
```
