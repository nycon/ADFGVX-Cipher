# ADFGVX Cipher

This small Python project contains two terminal programs:

- `adfgvx_encrypt.py` encrypts a message.
- `adfgvx_decrypt.py` decrypts the message again.

The encrypted text is displayed in groups of four characters on a single line.
Spaces, punctuation, capitalization, umlauts, and other Unicode characters are
restored during decryption.

## Requirements

- Python 3.9 or newer
- No additional packages are required

## Set your keyword

Open both Python files and find this line near the top:

```python
KEYWORD = "MEINSCHLUESSEL"
```

Replace the value with your own keyword. The keyword must be exactly the same
in both files. If the keywords are different, decryption will fail.

## Encrypt a message

Open a terminal in this folder and run:

```bash
python3 adfgvx_encrypt.py
```

Enter your message and press Enter. Copy only the encrypted text shown in the
result section.

## Decrypt a message

Run:

```bash
python3 adfgvx_decrypt.py
```

Paste the complete encrypted text and press Enter. Spaces between the groups
are accepted and removed automatically.

## Important notes

- Changing the keyword means older messages can only be decrypted with the old
  keyword.
- Both scripts must use the same version because this project adds a reversible
  UTF-8 encoding step to preserve the original text exactly.
- ADFGVX is a historical cipher. It is useful for learning, but it is not safe
  for protecting passwords or confidential information.

## Educational use and disclaimer

This project is a small learning experiment created for fun. It can help you
understand the basic ideas behind encryption and decryption, but it is not a
modern security tool and must not be used to protect sensitive information.

The project is provided as-is and without any guarantee. The author accepts no
responsibility or liability for how it is used, for incorrect results, for data
loss, or for any direct or indirect damage resulting from its use. You use this
project entirely at your own risk.
