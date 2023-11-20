import hashlib

# константы
NUMBERS_FILE = "hash_numbers_with_salt.txt"
OUTPUT_DIR = "hashed_output"
NUMBERS_TO_MATCH = [89176820333, 89656565569, 89866200060, 89699250890, 89859647020]
TEST_SALTS = [1, 10000, 100000, 291673, 30000000, 123456789, 500000000, 999999999, 100000000,
               123456789, 212121, 9999999, 381, 1, 226677881]

# функция для хеширования данных с использованием MD5
def hash_md5(data):
    h = hashlib.md5(str(data).encode('utf-8'))
    return h.hexdigest()

# для хеширования данных с использованием SHA-1
def hash_sha1(data):
    h = hashlib.sha1(str(data).encode('utf-8'))
    return h.hexdigest()

# для хеширования данных с использованием SHA-256
def hash_sha256(data):
    h = hashlib.sha256(str(data).encode('utf-8'))
    return h.hexdigest()

# для записи данных в файл
def write_to_file(file_path, data):
    with open(file_path, "w") as f:
        for item in data:
            f.write(str(item) + '\n')

# чтение номеров из файла
with open(NUMBERS_FILE, "r") as f:
    NUMBERS = [int(line[-12:-1]) for line in f.readlines()]

# вычисление разницы относительно эталонных номеров
DIFFERENCES = [[num - ref_num for num in NUMBERS] for ref_num in NUMBERS_TO_MATCH]

# подсчет встречаемости разницы для определения общей соли
SALT_COUNTER = {}
for diff_list in DIFFERENCES:
    for diff in diff_list:
        SALT_COUNTER[diff] = SALT_COUNTER.get(diff, 0) + 1

# поиск общей соли
COMMON_SALT = max(SALT_COUNTER, key=SALT_COUNTER.get)
print("Общая соль:", COMMON_SALT)

# вычисление оригинальных номеров без соли (в отдельный файл для дальнейшего анализа)
NO_SALT_NUMBERS = [num - COMMON_SALT for num in NUMBERS]
write_to_file("no_salt_numbers.txt", NO_SALT_NUMBERS)

# хеширование номеров с разными солями и запись в файлы
for i, salt in enumerate(TEST_SALTS):
    salted_numbers = [num + salt for num in NO_SALT_NUMBERS]
    
    MD5_HASHES = [hash_md5(num) for num in salted_numbers]
    SHA1_HASHES = [hash_sha1(num) for num in salted_numbers]
    SHA256_HASHES = [hash_sha256(num) for num in salted_numbers]

    write_to_file(f"{OUTPUT_DIR}/md5_{i}.txt", MD5_HASHES)
    write_to_file(f"{OUTPUT_DIR}/sha1_{i}.txt", SHA1_HASHES)
    write_to_file(f"{OUTPUT_DIR}/sha256_{i}.txt", SHA256_HASHES)
