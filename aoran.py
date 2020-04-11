import sys
import traceback
from os import path
import urllib.request
import urllib.error


class UnableToCompleteDownload(Exception):
  pass


class WordNotFound(Exception):
  pass


class UnauthorizedToFetchDatabase(Exception):
  pass


# https://en.wikipedia.org/wiki/ARPABET (CMUdict uses the 2-letter table)
ARPABET_VOWEL_PHONEMES = [
  b'AA', b'AE', b'AH', b'AO', b'AW', b'AX', b'AY', b'EH', b'ER',
  b'EY', b'IH', b'IX', b'IY', b'OW', b'OY', b'UH', b'UW', b'UX'
]


CMUDICT_FILE_NAME = 'cmudict-0.7b'
CMUDICT_LATEST_RELEASE = f'http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/{CMUDICT_FILE_NAME}'


def resolve_article_for(word, silently=True, database_file=CMUDICT_FILE_NAME):

  # Check if we have the CMUdict release available, downloading it if necessary
  if not path.exists(database_file):

    if silently:
      answer = 'y'
    else:
      answer = input('Hey, I need to download a copy of CMUdict (~3.5mb), can I? (y/n) ')

    if answer.strip().lower() == 'y':
      if not silently:
        print('Downloading...')
      try:
        response = urllib.request.urlopen(CMUDICT_LATEST_RELEASE)
        data = response.read()
        with open(database_file, 'wb') as file:
          file.write(data)
        if not silently:
          print('Downloaded! Thanks for waiting.')
      except urllib.error.URLError:
        print(traceback.format_exc(limit=3, chain=0), file=sys.stderr)
        raise UnableToCompleteDownload()
    else:
      raise UnauthorizedToFetchDatabase()
  else:
    with open(database_file, 'rb') as file:
      data = file.read()

  try:
    line_start = data.index(b'\n' + bytes(word.upper(), encoding='utf-8'))
  except ValueError:
    raise WordNotFound()

  # Find the word inside the database, and check if the first phoneme is a vowel sound
  next_line_break = data.index(b'\n', line_start + 1)
  full_line = data[line_start:next_line_break]
  first_phoneme = full_line.split()[1][:2] # the :2 part is there to discard auxiliary symbols
  if first_phoneme in ARPABET_VOWEL_PHONEMES:
    return 'an'
  else:
    return 'a'


if __name__ == '__main__':

  # Extract the word to be checked from the command line arguments
  if len(sys.argv) != 2:
    print('Usage: ./aoran <word>\nExample: ./aoran university')
    exit(0)
  word = sys.argv[1]

  try:
    article = resolve_article_for(word, silently=False)
    print(f'{article} {word}')
  except UnableToCompleteDownload:
    print('Sorry! Unable to complete the download :(')
  except WordNotFound:
    print('Sorry, I couldn\'t find this word :(')
  except UnauthorizedToFetchDatabase:
    print('Ok, maybe next time :)')
