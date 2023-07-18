import unicodedata
import re
import joblib
from langdetect import detect
from unidecode import unidecode
from os.path import join, dirname



class TextNormalizer:
    def __init__(self, binary_file):
        data = joblib.load(binary_file)
        self.character_map = data["character"]
        self.token_map = data["token"]


text_normalizer = TextNormalizer("/content/drive/MyDrive/[1]Colab_Notebooks/[0]Project/[1]viMuQA/Auto/Data/tn_rules_2022_08_11.bin")
character_map = text_normalizer.character_map
token_map = text_normalizer.token_map

def character_normalize(text):
    for character_non_standard in character_map:
        character_standard = character_map[character_non_standard]
        text = text.replace(character_non_standard, character_standard)
    return text


def utf8_normalize(text):
    if not is_unicode(text):
        text = text.unicodedata.normalize('NFKD', text).encode('utf-8' , 'ignore').decode('utf-8')
    text = unicodedata.normalize("NFC", text)
    return text


def normalize_characters_in_text(text):
    text = utf8_normalize(text)
    text = character_normalize(text)
    return text


def is_unicode(text):
    return type(text) == str


def token_normalize(token, use_character_normalize=True):
    """
    normalize each token
    """
    if len(token) > 6:
        return token
    # character normalize
    if use_character_normalize:
        token = normalize_characters_in_text(token)
    if token in token_map:
        return token_map[token]
    return token

def unicode_normalize(token):
  try:
    if detect(token) != 'vi':
      return unidecode(token)

    return token
  except:
    return token


def unidecode_chinese(string):
    _list = re.findall(u'[^\u4E00-\u9FA5]', string)
    for c in string:
        if c not in _list:
          new_c = unidecode(c)[:-1]
          string = string.replace(c, new_c)
    return string




def format_day(text, slipt = ' '):
  day = ''
  for word in text.split(slipt):
    try:
      int(word)
      day = day + word + '/'
    except:
      pass

  return day[:-1]

def format_days(sentence):

  sentence1 = sentence.lower()
  date = [
      r"ngày\s\d+\stháng\s\d+\snăm\s\d{4}",
      r"\d{1,2}\stháng\s\d+\snăm\s\d{4}",
      r"ngày\s\d+\stháng\s\d{1,2}",
      r"\d{1,2}\stháng\s\d{1,2}",
      r"tháng\s\d+\snăm\s\{4}",
      r"\d{1,2}\snăm\s\d{4}",
      r"năm\s\d{4}",
      r"tháng\s\d{1,2}",
      r"ngày\s\d{1,2}"
  ]

  datetime = [
    r"\d{1,2}\s\/\s\d{1,2}\s\/\s\d+", 
    r"\d{1,2}\s\/\s\d{1,4}",
    r"\d{4}\s\/\s\d{1,2}\s\/\s\d{1,2}",
  ]

  pattern = '|'.join(date) + '|' + '|'.join(datetime)
  days = re.findall(pattern, sentence1)

  for day in days:
    start, end = re.search(day, sentence1).span()
    sentence = list(sentence)
    sentence[start:end] = format_day(day, slipt = ' ')
    sentence1 = re.sub(day, format_day(day, slipt = ' '), sentence1, count = 1)
  return(''.join(sentence))

def text_normalize(text):
    """
    Args:
        tokenizer (str)
    """

    text = re.sub(r"\[.*?\]+", '', text)

    word = '\w+'
    non_word = '[^\w\s]'
    digits = '\d+([\.,_]\d+)+'
    
    patterns = []
    patterns.extend([word, non_word, digits])
    patterns = f"({'|'.join(patterns)})"
    tokens = re.findall(patterns, text, re.UNICODE)
    tokens = [token[0] for token in tokens]

    normalized_tokens = [token_normalize(token) for token in tokens]
    normalized_tokens = unicode_normalize(normalized_tokens)
    normalized_text = " ".join(normalized_tokens)
    normalized_text = format_days(normalized_text)
    normalized_text = unidecode_chinese(string = normalized_text)
    return normalized_text
