# ADFGVX Cipher Learning Project

This is a small educational project for experimenting with the historical
ADFGVX cipher and learning how encryption and decryption work.

It contains:

- `adfgvx_encrypt.py` — encrypts a message.
- `adfgvx_decrypt.py` — decrypts a message.
- `adfgvx_secret.key` — the shared secret key file.
- `previous-key-backup/` — contains the key used by the previous version.

The encrypted output is displayed in groups of four characters on one line.
The original spaces, punctuation, capitalization, umlauts, and other Unicode
characters are restored after decryption.

## Requirements

- Python 3.9 or newer
- No additional packages

## How the key file works

The keyword is not stored in the Python code. Both programs derive their
internal ADFGVX key from `adfgvx_secret.key`.

If that file does not exist, the encryption program automatically creates a new
64-byte (512-bit) random key file when it starts. It uses Python's secure random
generator, and SHA-512 is used to derive the internal key.

The decryption program never creates a replacement key. It must receive an
identical copy of the key file that was used for encryption. Two independently
generated key files cannot decrypt each other's messages.

## Encrypt a message

Open a terminal in this folder and run:

```bash
python3 adfgvx_encrypt.py
```

On the first start, the program creates `adfgvx_secret.key` if it is missing.
Enter your message and press Enter. Copy the encrypted text from the result
section.

## Decrypt a message

Make sure the correct `adfgvx_secret.key` is in the same folder as the
decryption program, then run:

```bash
python3 adfgvx_decrypt.py
```

Paste the complete encrypted text and press Enter. Spaces between the
four-character groups are accepted and removed automatically.

## Giving the encryption program to someone else

To let another person generate an independent key, give them
`adfgvx_encrypt.py` without your `adfgvx_secret.key`. Their program creates a
new key file on first launch. They must keep that file and provide an identical
copy to the person who needs to decrypt their messages.

## Key safety

- Keep a protected backup of every key file you use.
- Never modify the contents of the key file.
- Never publish the key file or send it together with the encrypted message.
- Share it only with the intended recipient, preferably through a separate,
  trusted channel.
- Deleting the key makes the encryption program generate a different one the
  next time it starts.
- A newly generated key cannot decrypt messages made with an older key.
- Losing the only copy of a key means its messages cannot be recovered.

## Previous key backup

The earlier 32-byte key is stored in:

```text
previous-key-backup/adfgvx_secret.key
```

The decryption program supports both the previous 32-byte format and the current
64-byte format. To decrypt an older message:

1. Preserve the current `adfgvx_secret.key` in a safe location.
2. Copy the previous key next to the scripts and name it
   `adfgvx_secret.key`.
3. Decrypt the older message.
4. Restore the current key afterward.

Never overwrite your only copy of either key.

## Educational use and disclaimer

This project is a learning experiment created for fun. It demonstrates basic
ideas behind substitution and transposition ciphers. ADFGVX is a historical
cipher and is not safe for passwords, private documents, financial data, or any
other sensitive information. A longer key file does not turn ADFGVX into modern
secure encryption.

The project is provided as-is and without any guarantee. The author accepts no
responsibility or liability for how it is used, for incorrect results, for data
loss, or for any direct or indirect damage resulting from its use. You use this
project entirely at your own risk.
