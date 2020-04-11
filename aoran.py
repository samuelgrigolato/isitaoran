import sys
import traceback
from os import path
import urllib.request
import urllib.error


# https://en.wikipedia.org/wiki/ARPABET (CMUdict uses the 2-letter table)
ARPABET_VOWEL_PHONEMES = [
  b'AA', b'AE', b'AH', b'AO', b'AW', b'AX', b'AY', b'EH', b'ER',
  b'EY', b'IH', b'IX', b'IY', b'OW', b'OY', b'UH', b'UW', b'UX'
]


CMUDICT_FILE_NAME = 'cmudict-0.7b'
CMUDICT_LATEST_RELEASE = f'http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/{CMUDICT_FILE_NAME}'


# Extract the word to be checked from the command line arguments
if len(sys.argv) != 2:
  print('Usage: ./aoran <word>\nExample: ./aoran university')
  exit(0)
word = sys.argv[1]


# Check if we have the CMUdict release available, downloading it if necessary
if not path.exists(CMUDICT_FILE_NAME):
  answer = input('Hey, I need to download a copy of CMUdict (~3.5mb), can I? (y/n) ')
  if answer.strip().lower() == 'y':
    print('Downloading...')
    try:
      response = urllib.request.urlopen(CMUDICT_LATEST_RELEASE)
      data = response.read()
      with open(CMUDICT_FILE_NAME, 'wb') as file:
        file.write(data)
      print('Downloaded!')
    except urllib.error.URLError:
      print('Sorry, couldn\'t complete the download :(')
      print(traceback.format_exc(limit=3, chain=0), file=sys.stderr)
      exit(1)
  else:
    print('Ok, maybe next time :)')
    exit(0)
else:
  with open(CMUDICT_FILE_NAME, 'rb') as file:
    data = file.read()


# Find the word inside the database, and check if the first phoneme is a vowel sound
try:

  line_start = data.index(b'\n' + bytes(word.upper(), encoding='utf-8'))
  next_line_break = data.index(b'\n', line_start + 1)
  full_line = data[line_start:next_line_break]
  first_phoneme = full_line.split()[1][:2] # the :2 part is to discard auxiliary symbols
  if first_phoneme in ARPABET_VOWEL_PHONEMES:
    print(f'an {word}')
  else:
    print(f'a {word}')

except ValueError:
  print('Sorry, I couldn\'t find this word :(')
