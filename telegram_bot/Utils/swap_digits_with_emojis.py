def swap_digits_with_emojis(input_string):
    # Словарь для соответствия цифр и смайликов
    digit_to_emoji = {
        '0': '0️⃣',
        '1': '1️⃣',
        '2': '2️⃣',
        '3': '3️⃣',
        '4': '4️⃣',
        '5': '5️⃣',
        '6': '6️⃣',
        '7': '7️⃣',
        '8': '8️⃣',
        '9': '9️⃣'
    }

    # Заменяем каждую цифру на соответствующий смайлик
    result = ''.join(digit_to_emoji.get(char, char) for char in input_string)
    return result

