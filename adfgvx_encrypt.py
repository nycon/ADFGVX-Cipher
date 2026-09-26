#!/usr/bin/env python3
"""Encrypt text with the ADFGVX cipher."""

import hashlib
import os
import secrets
import sys
import unicodedata
from pathlib import Path


COORDINATES = "ADFGVX"
CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# Both programs load the same secret file from their own folder.
KEY_FILE = Path(__file__).with_name("adfgvx_secret.key")
SECRET_SIZE = 64

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


def derive_key(secret: bytes) -> str:
    """Derive a repeatable ADFGVX key from the shared secret bytes."""
    return hashlib.sha512(secret).hexdigest().upper()


def load_or_create_key() -> tuple[str, bool]:
    """Load the shared secret, or securely create it when it is missing."""
    try:
        secret = KEY_FILE.read_bytes()
        created = False
    except FileNotFoundError:
        secret = secrets.token_bytes(SECRET_SIZE)
        try:
            descriptor = os.open(
                KEY_FILE,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                0o600,
            )
            with os.fdopen(descriptor, "wb") as key_file:
                key_file.write(secret)
            created = True
        except FileExistsError:
            # Another program instance may have created the file first.
            try:
                secret = KEY_FILE.read_bytes()
                created = False
            except OSError as error:
                raise ValueError(f"The key file could not be read: {error}") from error
        except OSError as error:
            raise ValueError(f"The key file could not be created: {error}") from error
    except OSError as error:
        raise ValueError(f"The key file could not be read: {error}") from error

    if len(secret) < SECRET_SIZE:
        raise ValueError(
            f"The key file is too short. It must contain at least {SECRET_SIZE} bytes."
        )
    return derive_key(secret), created


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

    try:
        key, key_created = load_or_create_key()
    except ValueError as error:
        print(f"{RED}✗ Error: {error}{RESET}")
        return

    if key_created:
        print(
            f"{GREEN}✓ A new {SECRET_SIZE * 8}-bit key file was generated: "
            f"{KEY_FILE.name}{RESET}\n"
        )
    else:
        print(f"Key file loaded: {KEY_FILE.name}\n")

    text = input(f"{BOLD}Your text{RESET}\n› ")

    try:
        _, _, ciphertext = encrypt(text, key)
    except ValueError as error:
        print(f"\n{RED}✗ Error: {error}{RESET}")
        return

    print(f"\n{GREEN}✓ Text encrypted successfully{RESET}")
    print(f"Key file: {KEY_FILE.name}\n")
    divider()
    print(f"{BOLD}ENCRYPTED TEXT · READY TO COPY{RESET}")
    divider()
    print(format_ciphertext(ciphertext))
    divider()
    print()


if __name__ == "__main__":
    main()
