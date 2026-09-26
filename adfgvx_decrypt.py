#!/usr/bin/env python3
"""Decrypt text produced by adfgvx_encrypt.py."""

import sys
import unicodedata


COORDINATES = "ADFGVX"
CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# Enter the same keyword used in the encryption program.
KEYWORD = "MEINSCHLUESSEL"

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


def normalize_ciphertext(text: str) -> str:
    return "".join(character for character in text.upper() if character in COORDINATES)


def reverse_transposition(text: str, key: str) -> str:
    width = len(key)
    full_rows, remainder = divmod(len(text), width)
    lengths = [full_rows + (1 if i < remainder else 0) for i in range(width)]
    order = sorted(range(width), key=lambda i: (key[i], i))

    columns = [""] * width
    position = 0
    for index in order:
        length = lengths[index]
        columns[index] = text[position : position + length]
        position += length

    return "".join(
        columns[column][row]
        for row in range(full_rows + (1 if remainder else 0))
        for column in range(width)
        if row < len(columns[column])
    )


def reverse_substitution(text: str) -> str:
    if len(text) % 2:
        raise ValueError("The ciphertext must contain an even number of characters.")

    result = []
    for position in range(0, len(text), 2):
        row = COORDINATES.index(text[position])
        column = COORDINATES.index(text[position + 1])
        result.append(CHARACTERS[row * 6 + column])
    return "".join(result)


def decode_plaintext(text: str) -> str:
    """Restore spaces, punctuation, capitalization, and Unicode characters."""
    try:
        return bytes.fromhex(text).decode("utf-8")
    except (ValueError, UnicodeDecodeError) as error:
        raise ValueError("The ciphertext or keyword is invalid.") from error


def decrypt(ciphertext: str, key: str) -> tuple[str, str]:
    ciphertext = normalize_ciphertext(ciphertext)
    key = normalize_key(key)
    if not ciphertext:
        raise ValueError("No valid ADFGVX ciphertext was entered.")
    if not key:
        raise ValueError("The keyword does not contain any supported characters.")

    substituted = reverse_transposition(ciphertext, key)
    encoded_plaintext = reverse_substitution(substituted)
    return key, decode_plaintext(encoded_plaintext)


def main() -> None:
    display_title(
        "ADFGVX · DECRYPTION",
        "Paste the encrypted text and press Enter.",
    )
    ciphertext = input(f"{BOLD}Encrypted text{RESET}\n› ")

    try:
        _, plaintext = decrypt(ciphertext, KEYWORD)
    except ValueError as error:
        print(f"\n{RED}✗ Error: {error}{RESET}")
        return

    print(f"\n{GREEN}✓ Text decrypted successfully{RESET}\n")
    divider()
    print(f"{BOLD}DECRYPTED TEXT{RESET}")
    divider()
    print(plaintext)
    divider()
    print()


if __name__ == "__main__":
    main()
