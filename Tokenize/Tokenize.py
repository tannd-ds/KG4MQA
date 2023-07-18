from langdetect import detect
from Data.Vocabulary import *
import re
import joblib
from underthesea import word_tokenize, pos_tag
from pyvi import ViTokenizer, ViPosTagger
import py_vncorenlp



class pyvi_tokenize:
  def __init__(self, vocab = False):
    self.token = ViTokenizer
    self.postag = ViPosTagger
    if vocab:
      self.vocab = get_vocabulary()
    else:
      self.vocab = []

  def __extract_match(self, m):
    for k, v in m.groupdict().items():
        if v is not None:
            return v, k

  def tokenizer(self, text, fixed_words = []):
    if len(fixed_words) > 0:
      insert_vocab(fixed_words, self.vocab)

    if self.vocab != []:
      compiled_fixed_words = [re.sub(' ', '\ ', fixed_word) for fixed_word in self.vocab]
      fixed_words_pattern = "(?P<fixed_words>" + "|".join(self.vocab) + ")"
      merged_regex_patterns = [fixed_words_pattern]
      regex_patterns_combine = r"(" + "|".join(merged_regex_patterns) + ")"
      patterns = re.compile(regex_patterns_combine, re.VERBOSE | re.UNICODE)

      matches = [m for m in re.finditer(patterns, text)]
      tokens = [self.__extract_match(m) for m in matches]
      tokens = [token[0] for token in tokens]
      _tokens = [i.replace(' ', '_') for i in tokens]
      try:
        for i in range(len(tokens)):
          text = text.replace(tokens[i], _tokens[i])
      except:
        pass

    return self.token.tokenize(text).split(' ')

  def annotate(self,text, fixed_words = []):
    output = []
    doc = self.postag.postagging(' '.join(self.tokenizer(text, fixed_words = fixed_words)))
    for i in range(len(doc[0])):
      if doc[1][i] == 'F':
        doc[1][i] = 'CH'
      output.append([doc[0][i],doc[1][i]])

    return output

  def info(self):
    return('PyVi')


class Underthesea_tokenize:

  def __init__(self, vocab = False):
    if vocab:
      self.vocab = get_vocabulary()
    else:
      self.vocab = []


  def tokenizer(self,text, fixed_words = []):
    if len(fixed_words) > 0:
      insert_vocab(fixed_words, self.vocab)

    sentence = word_tokenize(text, fixed_words = self.vocab)
    sentence = [i.replace(' ', '_') for i in sentence]

    return sentence
  def annotate(self,text, fixed_words = []):

    sentence = ' '.join(self.tokenizer(text, fixed_words = fixed_words))
    tagging = pos_tag(sentence)
    tagging = [list(i) for i in tagging]


    return tagging

  def info(self):
    return('Underthesea')


class Underthesea_pyvi:

  def __init__(self, vocab = False):
    if vocab:
      self.vocab = get_vocabulary()
    else:
      self.vocab = []

  def tokenizer(self,text, fixed_words = []):
    if len(fixed_words) > 0:
      insert_vocab(fixed_words, self.vocab)

    sentence = word_tokenize(text, fixed_words = self.vocab)
    sentence = [i.replace(' ', '_') for i in sentence]

    return sentence

  def annotate(self,text, fixed_words = []):
    output = []
    doc = ViPosTagger.postagging(' '.join(self.tokenizer(text, fixed_words = fixed_words)))
    for i in range(len(doc[0])):
      if doc[1][i] == 'F':
        doc[1][i] = 'CH'
      output.append([doc[0][i],doc[1][i]])

    return output


  def info(self):
    return('Underthesea_pyvi')

  
class VncoreNLP_tokenize:

  def __init__(self, vocab = False, path_vn = None):
    if path_vn == None:
      path_vn = '/content/drive/MyDrive/[1]Colab_Notebooks/[3] NLP/VnCoreNLP'
    self.model = py_vncorenlp.VnCoreNLP(save_dir= path_vn)
    if vocab:
      self.vocab = get_vocabulary()
    else:
      self.vocab = []

    pass



  def __extract_match(self, m):
    for k, v in m.groupdict().items():
        if v is not None:
            return v, k
  def tokenizer(self,text, fixed_words = []):
    if len(fixed_words) > 0:
      insert_vocab(fixed_words, self.vocab)

    if self.vocab != []:
      compiled_fixed_words = [re.sub(' ', '\ ', fixed_word) for fixed_word in self.vocab]
      fixed_words_pattern = "(?P<fixed_words>" + "|".join(self.vocab) + ")"
      merged_regex_patterns = [fixed_words_pattern]
      regex_patterns_combine = r"(" + "|".join(merged_regex_patterns) + ")"
      patterns = re.compile(regex_patterns_combine, re.VERBOSE | re.UNICODE)

      matches = [m for m in re.finditer(patterns, text)]
      tokens = [self.__extract_match(m) for m in matches]
      tokens = [token[0] for token in tokens]
      _tokens = [i.replace(' ', '_') for i in tokens]
      try:
        for i in range(len(tokens)):
          text = text.replace(tokens[i], _tokens[i])
      except:
        pass

    self.text = self.model.annotate_text(text)[0]

    return [tok['wordForm'] for tok in self.text]

  def annotate(self,text, fixed_words = []):
    self.tokenizer(text, fixed_words = fixed_words)

    return [[tok['wordForm'], tok['posTag']] for tok in self.text]

  def close(self):

    pass
  def info(self):
    return('VnCoreNLP')


class longest_matching:
  def __init__(self, vocab = True, max_tok = 12):
    if vocab:
      self.vocab = get_vocabulary()
    else:
      self.vocab = []

    self.max_tok = max_tok
    pass
  


  def __isvocab(self, word: list, num_word, vocab):
    _word = ' '.join(word)
    print(_word)

    if num_word == 1:
      return [1, _word]


    if is_vocab(_word, vocab):
      return [num_word, _word.replace(' ', '_')]

    else:
      return self.__isvocab(word[:-1], num_word=num_word-1, vocab = vocab)


  def tokenizer(self,text, fixed_words = []):

    sentence = text.split(' ')
    if self.vocab == []:
      return sentence
    toks_len = len(sentence)
    curr_id = 0
    result = []
    while curr_id < toks_len:
      curr = sentence[curr_id]
      if curr_id  >= toks_len - self.max_tok:
        num_words = toks_len - curr_id
      else:
        num_words = self.max_tok
      _new = self.__isvocab(sentence[curr_id: curr_id + num_words], num_words, self.vocab)

      result.append(_new[1])
      curr_id += _new[0]

    return (result)

  def annotate(self,text, fixed_words = []):
    output = []
    doc = ViPosTagger.postagging(' '.join(self.tokenizer(text, fixed_words = fixed_words)))
    for i in range(len(doc[0])):
      if doc[1][i] == 'F':
        doc[1][i] = 'CH'
      output.append([doc[0][i],doc[1][i]])

    return output


  def info(self):
    return('longest_matching')


class Tokenize:
  def __init__(self, vocab = True, max_tok = 12):
    if vocab:
      self.vocab = get_vocabulary()
    else:
      self.vocab = []

    self.max_tok = max_tok
    self.Under_py = Underthesea_pyvi(vocab = False)
    pass

  def __is_vocab(self, word):
    try:
      _word = self.Under_py.tokenizer(word)
      _vocab = [i.replace('_', ' ') for i in _word if '_' in i]
      self.vocab = insert_vocab(_vocab, self.vocab)
      if len(_word) == 1:
        return True
      else:
        return False
    except:
      return False
  def __isvocab(self, word: list, num_word, vocab):
    
    self.vocab = list(sorted(self.vocab, reverse=True, key = len))
    _word = ' '.join(word)

    if num_word == 1:
      return [1, _word]

    if is_vocab(_word, vocab):
      return [num_word, _word.replace(' ', '_')]
    elif self.__is_vocab(_word) == True:
      print("XXX")
      return [num_word, _word.replace(' ', '_')]
    else:
      return self.__isvocab(word[:-1], num_word=num_word-1, vocab = vocab)


  def tokenizer(self,text, fixed_words = []):
    sentence = text.split(' ')
    if len(fixed_words) > 0:
      insert_vocab(fixed_words, self.vocab)

    if self.vocab == []:
      return sentence
    toks_len = len(sentence)
    curr_id = 0
    result = []
    while curr_id < toks_len:
      curr = sentence[curr_id]
      if curr_id  >= toks_len - self.max_tok:
        num_words = toks_len - curr_id
      else:
        num_words = self.max_tok
      _new = self.__isvocab(sentence[curr_id: curr_id + num_words], num_words, self.vocab)

      result.append(_new[1])
      curr_id += _new[0]

    return (result)

  def annotate(self,text, fixed_words = []):
    output = []
    doc = ViPosTagger.postagging(' '.join(self.tokenizer(text, fixed_words = fixed_words)))
    for i in range(len(doc[0])):
      if doc[1][i] == 'F':
        doc[1][i] = 'CH'
      output.append([doc[0][i],doc[1][i]])

    return output


  def info(self):
    return('Tokenize')
