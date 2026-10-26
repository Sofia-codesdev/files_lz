import pandas as pd
import matplotlib.pyplot as plt

INPUT_FILE = 'titanic.parquet'   # Исходный файл
OUTPUT_FILE = 'titanic.csv'      # Файл, куда сохраним результат

def main():
    print(f"--- Обработка файла: {INPUT_FILE} ---")
    
    try:
        # Читаем исходный parquet-файл
        df = pd.read_parquet(INPUT_FILE)
        print("Файл parquet успешно прочитан.")
        
        # Переводим данные в формат CSV и сохраняем в исходную папку
        df.to_csv(OUTPUT_FILE, index=False)
        print(f" Данные успешно сохранены в файл: {OUTPUT_FILE}")
        
        # Проверка корректности: заново открываем созданный CSV-файл
        df_check = pd.read_csv(OUTPUT_FILE)
        print(" Созданный CSV-файл успешно открыт для проверки.")
        
    except FileNotFoundError:
        print(f" Ошибка: Файл '{INPUT_FILE}' не найден в текущей папке.")
        return
    except Exception as e:
        print(f" Произошла ошибка: {e}")
        return
    
    # считаем количество пассажиров по классам и выживаемости
    # groupby группирует по классу и статусу, а size() считает количество строк
    pivot_data = df_check.groupby(['Pclass', 'Survived']).size().unstack(fill_value=0)

    pivot_data = pivot_data.rename(columns={0: 'Не выжил', 1: 'Выжил'})
    
    # Переводим абсолютные числа в проценты
    pivot_percent = pivot_data.div(pivot_data.sum(axis=1), axis=0) * 100

    # Построение гистограммы
    class_labels = {1: 'первый класс', 2: 'второй класс', 3: 'третий класс'}
    pivot_percent.index = [class_labels[i] for i in pivot_percent.index]

    ax = pivot_percent.plot(kind='bar', stacked=True, figsize=(10, 6), color=['#4c72b0', '#dd8452'])

    plt.title('Выживаемость пассажиров Титаника', fontsize=16)
    plt.xlabel('Класс билета', fontsize=12)
    plt.ylabel('Процент выживших', fontsize=12)
    
    # Настраиваем ось Y, чтобы она показывала от 0 до 100%
    plt.ylim(0, 100)
    plt.yticks([0, 50, 100], ['0%', '50%', '100%'])
    
    # Поворачиваем подписи классов горизонтально, чтобы было красиво
    plt.xticks(rotation=0)
    
    # Добавляем легенду 
    plt.legend(title='Статус', loc='upper center', bbox_to_anchor=(0.5, 1.0), ncol=2)
    
    # Убираем лишние линии по бокам
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    print("📊 Отображение гистограммы...")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()