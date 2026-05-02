import sys
import math
from pydub import AudioSegment

def compute_peak_dbfs(audio_segment):
    """
    Возвращает максимальную громкость в dBFS и пиковую абсолютную амплитуду.
    """
    # Получаем сырые сэмплы как массив целых чисел
    samples = audio_segment.get_array_of_samples()
    
    # Определяем максимально возможное значение для данного sample_width
    # sample_width — количество байт на сэмпл: 2 для 16‑бит, 3 для 24‑бит, 4 для 32‑бит
    max_abs_sample = 2 ** (8 * audio_segment.sample_width - 1) - 1
    
    # Находим максимальную абсолютную амплитуду среди всех каналов
    peak_amplitude = max(abs(sample) for sample in samples)
    
    # Вычисляем dBFS (избегаем log(0) — тишина даёт -inf)
    if peak_amplitude == 0:
        dbfs = -float('inf')
    else:
        dbfs = 20 * math.log10(peak_amplitude / max_abs_sample)
    
    return dbfs, peak_amplitude

def main():
    if len(sys.argv) != 2:
        print("Использование: python mp3_peak_volume.py <путь_к_mp3>")
        sys.exit(1)
    
    mp3_path = sys.argv[1]
    
    try:
        # Загружаем MP3 (может занять время для больших файлов)
        audio = AudioSegment.from_mp3(mp3_path)
    except Exception as e:
        print(f"Ошибка загрузки файла: {e}")
        print("Убедитесь, что установлен ffmpeg или libav и файл существует.")
        sys.exit(1)
    
    # Если нужно, можно свести стерео в моно для наглядности,
    # но peak по всем каналам уже даст максимум громкости.
    dbfs, peak_amp = compute_peak_dbfs(audio)
    
    print(f"Файл: {mp3_path}")
    print(f"Разрядность: {audio.sample_width * 8} бит, каналов: {audio.channels}")
    print(f"Пиковая амплитуда (абсолютное значение): {peak_amp}")
    if dbfs == -float('inf'):
        print("Максимальная громкость: -∞ dBFS (тишина)")
    else:
        print(f"Максимальная громкость: {dbfs:.2f} dBFS")

if __name__ == "__main__":
    main()