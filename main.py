import hashlib
import os

def calculate_hash_md5(number: int) -> str:
    return hashlib.md5(str(number).encode()).hexdigest()

def get_phones(file_path:str) -> list:
    with open(file_path, mode='r') as f:
        known_phones = f.read().splitlines()
        return known_phones

def get_dehashed(file_path) -> tuple[dict, set]:
    with open(file_path, mode='r') as f:
        dehashed_lines = f.read().splitlines()
        hash_values = set()
        phones_dehashed = {}

        for line in dehashed_lines:
            hash_value, number = line.split(':')
            hash_values.add(hash_value)
            phones_dehashed[number] = hash_value

    return phones_dehashed, hash_values

def find_salt_md5_digits(
    known_phones: list,
    phones_dehashed:dict,
    hash_values:set,
):
    used_phone_int = int(known_phones[0])
    for phone_dehashed, original_hash in phones_dehashed.items():
        phone_dehashed_int = int(phone_dehashed)
        current_salt = phone_dehashed_int - used_phone_int
        
        for known_phone in known_phones:
            known_phone_int = int(known_phone)
            hashed_with_current_salt = calculate_hash_md5(known_phone_int + current_salt)
            if hashed_with_current_salt not in hash_values:
                break
        else:
            return current_salt

def dehashe(
    file_path_input: str='hashed_data.txt',
    file_path_output:str='dehashed_with_salt.txt',
    optimized:bool=True,
): 
    if optimized:
        optimization = '-O --opencl-device-types 1'
    else:
        optimization =  ''

    os.system(f"hashcat -a 3 -m 0 {optimization} {file_path_input} --outfile {file_path_output} --show '89?d?d?d?d?d?d?d?d?d'")

def main():
    dehashe()
    phones = get_phones('phones.txt')
    phones_dehashed, hash_values = get_dehashed('dehashed_with_salt.txt')
    print(find_salt_md5_digits(phones, phones_dehashed, hash_values))

if __name__ == "__main__":
    main()
