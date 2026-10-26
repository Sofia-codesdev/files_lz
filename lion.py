import docx
import matplotlib.pyplot as plt
import re

# --- Настройки ---
INPUT_FILE = 'lion.docx'  # Имя твоего файла Word
OUTPUT_FILE = 'statistics.txt' # Файл для сохранения таблицы

def get_text_from_docx(filename):
    """Функция для чтения текста из файла Word (.docx)"""
    try:
        doc = docx.Document(filename)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return ""

def main():
    print(f"--- Анализ текста из файла: {INPUT_FILE} ---")
    
    text = get_text_from_docx(INPUT_FILE)
    
    if not text:
        print("Текст не найден или файл пуст.")
        return

    clean_text = re.sub(r'[^\w\s]', '', text).lower() 
    
    # Статистика по словам
    words = clean_text.split()
    total_words = len(words)
    
    word_counts = {}
    for word in words:
        word_counts[word] = word_counts.get(word, 0) + 1
        
    # Сортируем слова по убыванию частоты
    sorted_words = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)

    #  Запись статистики по словам в файл в виде таблицы
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        header = f"| {'Слово':<20} | {'Частота встречи, раз':<20} | {'Частота встречи в %':<20} |\n"
        separator = "-" * len(header) + "\n"
        f.write(header)
        f.write(separator)
        
        for word, count in sorted_words:
            percent = (count / total_words) * 100
            # Красиво выравниваем столбцы
            line = f"| {word:<20} | {count:<20} | {percent:<20.2f} |\n"
            f.write(line)
            
    print(f" Статистика по словам успешно сохранена в файл: {OUTPUT_FILE}")

    # Статистика по буквам
    # убираем пробелы
    letters_only = clean_text.replace(" ", "") 
    letter_counts = {}
    for char in letters_only:
        letter_counts[char] = letter_counts.get(char, 0) + 1
        
    # Сортируем буквы по алфавиту
    sorted_letters = sorted(letter_counts.items())

    # 4. Построение гистограммы
    letters = [item[0] for item in sorted_letters]
    counts = [item[1] for item in sorted_letters]

    plt.figure(figsize=(14, 6)) # Размер окна
    plt.bar(letters, counts, color='skyblue', edgecolor='black')
    
    plt.title('Гистограмма встречаемости букв в тексте', fontsize=16)
    plt.xlabel('Буквы', fontsize=12)
    plt.ylabel('Количество встреч (раз)', fontsize=12)
    plt.xticks(rotation=0) # Буквы без наклона
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    print("Отображение гистограммы")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()