# Slovenian BIP39 Wordlist

This repository contains a carefully selected and sorted list of 2048 Slovenian words that can be used as a non-standard BIP39 mnemonic phrase. Each word in the list is unique, and no two words share the same first four letters. There might be similarities between words in meaning though.

## Selection and Sortation Process

Creating this wordlist was an incredibly time-consuming task. I utilized [fran.si SSKJ²](https://www.fran.si/iskanje?FilteredDictionaryIds=133&View=1&Query=%2A) and meticulously reviewed every page for each letter, extracting words that seemed suitable and memorable for mnemonic use. After compiling an initial list to exclude words, I ran the words through a tool to check for mistakes and to identify any words that shared the same first four letters.

During the first compilation, it became apparent that the list was short of the required 2048 words by over 450. To address this, I conducted a second, more exhaustive review of the dictionary. In this round, I included words that, while still relatively memorable, were less commonly used in everyday Slovenian language. This allowed me to fill the gaps and reach the target of 2048 words.

## Challenges with the Slovenian Language
The Slovenian language, unlike English, offers a more limited range of options, particularly when considering mnemonic usability and diversity. This inherent limitation made the selection process especially challenging, requiring careful balancing between word uniqueness, memorability, and appropriateness.

## Statistic

*Words starting with:*

- A = 2.49% = 51 words
- B = 2.59% = 53 words
- C = 1.66% = 34 words
- Č = 1.61% = 33 words
- D = 3.27% = 67 words
- E = 2.00% = 41 words
- F = 1.61% = 33 words
- G = 2.93% = 60 words
- H = 2.49% = 51 words
- I = 3.71% = 76 words
- J = 2.10% = 43 words
- K = 8.64% = 177 words
- L = 4.83% = 99 words
- M = 7.18% = 147 words
- N = 5.03% = 103 words
- O = 6.74% = 138 words
- P = 8.64% = 177 words
- R = 4.00% = 82 words
- S = 6.88% = 141 words
- Š = 2.15% = 44 words
- T = 4.05% = 83 words
- U = 1.66% = 34 words
- V = 6.59% = 135 words
- Z = 4.54% = 93 words
- Ž = 2.59% = 53 words

*Word length distribution:*

- 3-letter words = 6.93% = 142 words
- 4-letter words = 14.11% = 289 words
- 5-letter words = 22.90% = 469 words
- 6-letter words = 21.34% = 437 words
- 7-letter words = 16.16% = 331 words
- 8-letter words = 9.08% = 186 words
- 9-letter words = 5.18% = 106 words
- 10-letter words = 2.78% = 57 words
- 11-letter words = 0.78% = 16 words
- 12-letter words = 0.54% = 11 words
- 13-letter words = 0.10% = 2 words
- 14-letter words = 0.10% = 2 words

## Words Dictionary
I have included a JSON file that provides meaning in slovene language for each word in this wordlist, along with the tools used to create this file. You will find all the tools in the tools folder, each with self-explanatory filenames. However, please use the parser tools responsibly!

## Disclaimer

Please note that this Slovenian wordlist is not "yet", and probably never will be, officially supported by the BIP39 standard. As a result, importing 12 Slovenian words into any of the well-known wallets like Electrum, Blue Wallet, etc., will simply not work. For more information on the official BIP39 standard, visit the [BIP39 GitHub repository](https://github.com/bitcoin/bips/tree/
master/bip-0039).

## Why This Wordlist?

I created this wordlist in my native language out of curiosity while developing my own mnemonic generation and recovery tool in Python, called [BIP39_exotica](https://github.com/StellarStoic/BIP39_Exotica). This tool allows you to generate Bitcoin wallets and Nostr keys using any wordlist you can imagine, including this Slovenian wordlist and even colors. Yup you read that right. Colors.

## Using this wordlist

With the tools provided in the [BIP39_exotica](https://github.com/StellarStoic/BIP39_Exotica) repository, you can:

- Generate Bitcoin wallets using this Slovenian wordlist.
- Creating Nostr keys
- Recover those wallets using the same wordlist, ensuring compatibility and accessibility in your native language.

I highly recommend not to modify this wordlist any further to avoid any confusion in the future if the world decide to switch to the Bitcoin standard and they start massively incorporating all the languages in the BIP39 ⋆⭒˚.⋆🪐 ⋆⭒˚.⋆ Pleb can dream right!

## Authenticety

The hash of this original slovenian.txt wordlist is 

*dee8744a4faec765fd483695e3de9005fca29f0cdcf328ba0c9cce3a29e86056* 

While you can verify this hash using any standard hashing tool, to make your life easier, I've created a Python script called `wordlist_HASH_checker.py`. This script is included in the repository and allows you to easily check the authenticity of the original slovenian wordlist file.

## License

This wordlist is provided freely and openly. There are no restrictions on its use, modification, or distribution.

Feel free to explore, use, and modify this wordlist for your projects. feedback is always welcome!