TEXT_TO_MORSE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".",
    "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---",
    "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---",
    "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
    "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--",
    "Z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--",
    "4": "....-", "5": ".....", "6": "-....", "7": "--...",
    "8": "---..", "9": "----.",
    ".": ".-.-.-", ",": "--..--", "?": "..--..", "!": "-.-.--",
    "'": ".----.", "\"": ".-..-.", ":": "---...", ";": "-.-.-.",
    "/": "-..-.", "-": "-....-", "(": "-.--.", ")": "-.--.-",
    "&": ".-...", "=": "-...-", "+": ".-.-.", "@": ".--.-.",
}

MORSE_TO_TEXT = {value: key for key, value in TEXT_TO_MORSE.items()}


def text_to_morse(text: str) -> str:
    out = []
    for ch in text.upper():
        if ch == " ":
            out.append("/")
        elif ch in TEXT_TO_MORSE:
            out.append(TEXT_TO_MORSE[ch])
    return " ".join(out)


def decode_letter(symbols: str) -> str:
    return MORSE_TO_TEXT.get(symbols, "?")


def decode_message(symbol_list):
    return "".join(decode_letter(symbols) for symbols in symbol_list)
