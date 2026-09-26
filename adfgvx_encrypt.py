#!/usr/bin/env python3
"""Encrypt text with the ADFGVX cipher."""

import sys
import unicodedata


COORDINATES = "ADFGVX"
CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# Enter your personal keyword here. Use the same one in both programs.
KEYWORD = "MEINSCHLUESSEL"

# Display the ciphertext in groups of four on a single line.
GROUP_SIZE = 4

# Colors are only used when the program is running in a real terminal.
COLOR_ENABLED = sys.stdout.isatty()
BLUE = "\033[96m" if COLOR_ENABLED else ""
GREEN = "\033[92m" if COLOR_ENABLED else ""
RED = "\033[91m" if COLOR_ENABLED else ""
BOLD = "\033[1m" if COLOR_ENABLED else ""
RESET = "\033[0m" if COLOR_ENABLED else ""
WIDTH = 58


def display_title(title: str, subtitle: str) -> None:
    line = "═" * WIDTH
    print(f"\n{BLUE}╔{line}╗")
    print(f"║{title:^{WIDTH}}║")
    print(f"╚{line}╝{RESET}")
    print(f"{subtitle}\n")


def divider() -> None:
    print(f"{BLUE}{'─' * (WIDTH + 2)}{RESET}")


def normalize_key(text: str) -> str:
    """Prepare the keyword for columnar transposition."""
    text = (
        text.upper()
        .replace("Ä", "AE")
        .replace("Ö", "OE")
        .replace("Ü", "UE")
        .replace("ß", "SS")
        .replace("ẞ", "SS")
    )
    text = unicodedata.normalize("NFKD", text)
    return "".join(character for character in text if character in CHARACTERS)


def encode_plaintext(text: str) -> str:
    """Encode any text losslessly using only A-F and 0-9."""
    return text.encode("utf-8").hex().upper()


def substitution_step(plaintext: str) -> str:
    result = []
    for character in plaintext:
        position = CHARACTERS.index(character)
        row, column = divmod(position, 6)
        result.append(COORDINATES[row] + COORDINATES[column])
    return "".join(result)


def columnar_transposition(text: str, key: str) -> str:
    columns = [text[index::len(key)] for index in range(len(key))]
    order = sorted(range(len(key)), key=lambda i: (key[i], i))
    return "".join(columns[index] for index in order)


def format_ciphertext(text: str) -> str:
    groups = [
        text[position : position + GROUP_SIZE]
        for position in range(0, len(text), GROUP_SIZE)
    ]
    return " ".join(groups)


def encrypt(plaintext: str, key: str) -> tuple[str, str, str]:
    if not plaintext:
        raise ValueError("The text must not be empty.")
    key = normalize_key(key)
    if not key:
        raise ValueError("The keyword does not contain any supported characters.")

    encoded_plaintext = encode_plaintext(plaintext)
    substituted = substitution_step(encoded_plaintext)
    ciphertext = columnar_transposition(substituted, key)
    return plaintext, key, ciphertext


def main() -> None:
    display_title(
        "ADFGVX · ENCRYPTION",
        "Enter the text you want to encrypt.",
    )
    text = input(f"{BOLD}Your text{RESET}\n› ")

    try:
        _, key, ciphertext = encrypt(text, KEYWORD)
    except ValueError as error:
        print(f"\n{RED}✗ Error: {error}{RESET}")
        return

    print(f"\n{GREEN}✓ Text encrypted successfully{RESET}")
    print(f"Keyword: {key}\n")
    divider()
    print(f"{BOLD}ENCRYPTED TEXT · READY TO COPY{RESET}")
    divider()
    print(format_ciphertext(ciphertext))
    divider()
    print()


if __name__ == "__main__":
    main()
