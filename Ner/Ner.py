from Data.Vocabulary import *
from Data.Text_normalize import *
from Tokenize.Tokenize import *
import phonlp


LOC = set(Get_File('LOC'))
ORG = set(Get_File('ORG'))
PER = set(Get_File('PER'))
THING = set(Get_File('THING'))
TIME = set(Get_File('TIME'))

def isNp(tok):
  # vd_tok = 'Ho Chi Minh'

  words = tok.split(' ')
  return sum([w[0].isupper() for w in words]) == len(words)

def isnlower(tok):
  try:
    float(tok)
    return [False]
  except:
    return not tok.islower()

def isPER(tok):
  """
  return is person in dict
  """
  _tok = tok.lower()
  return (_tok in PER)

def isLOC(tok):
  """
  return  (isnlower(tok)) and (_tok in LOC)
  """
  _tok = tok.lower()
  return (isnlower(tok)) and (_tok in LOC)

patternloc = """[Qq][Uu][Ââ][Nn][  ][Kk][Hh][Uu][  ]
[Kk][Hh][Uu][  ][Pp][Hh][Ốố][  ]
[Hh][Uu][Yy][Ệệ][Nn][  ]
[Tt][Hh][Àà][Nn][Hh][  ][Pp][Hh][Ốố][  ][Tt][Rr][Ựự][Cc][  ][Tt][Hh][Uu][Ộộ][Cc][  ][Tt][Rr][Uu][Nn][Gg][  ][Ưư][Ơơ][Nn][Gg][  ]
[Pp][Hh][Ưư][Ờờ][Nn][Gg][  ]
[Tt][Hh][Ịị][  ][Xx][Ãã][  ]
[Tt][Hh][Àà][Nn][Hh][  ][Pp][Hh][Ốố][  ]
[Kk][Hh][Uu][  ][Vv][Ựự][Cc][  ]
[Tt][Ỉỉ][Nn][Hh][  ]
[Đđ][Ảả][Oo][  ]
[Nn][Hh][Àà][  ][Ss][Ốố][  ]
[Ấấ][Pp][  ]
[Kk][Hh][Uu][  ][Tt][Ựự][  ][Tt][Rr][Ịị][  ]
[Xx][Ãã][  ]
[Đđ][Ưư][Ờờ][Nn][Gg][  ]
[Tt][Hh][Ủủ][  ][Đđ][Ôô][  ]
[Xx][Óó][Mm][  ]
[Bb][Ảả][Nn][  ]
[Nn][Gg][Áá][Cc][Hh][  ]
[Ss][Ốố][  ][Nn][Hh][Àà][  ]
[Ll][Àà][Nn][Gg][  ]
[Ll][Àà][Nn][Gg][  ][Xx][Ãã][  ]
[Tt][Hh][Ôô][Nn][  ]
[Cc][Hh][Ââ][Uu][  ]
[Bb][Uu][Ôô][Nn][  ]
[Đđ][Ưư][Ờờ][Nn][Gg][  ][Ss][Ốố][  ]
[Tt][Hh][Ịị][  ][Tt][Rr][Ấấ][Nn][  ]
[Vv][Ùù][Nn][Gg][  ]
[Qq][Uu][Ậậ][Nn][  ]""".split('\n')
patternloc


def isLOC1(tok: list, num_tok):
  if num_tok > 2:
    return [False]

  pattern = '|'.join(patternloc)
  _tok = re.sub(pattern, '', tok[0])
  if num_tok == 2:
    _tok += ' ' + tok[1]
  if _tok == '':
    return [False]
  _tok = re.sub('\s+', ' ', _tok)
  if _tok == ' ':
    return [False]
  try:
    if tok[0] == ' ':
      tok = tok[1:]
    if tok[-1] == ' ':
      tok = tok[:-1]
    float(_tok)
    return [True, 3]
  except:
    pass
  if (isLOC(tok)) or (isNp(tok)):
    return [True, 3]
  return [False, 3]

def isORG(tok):
  """
  return ORG in dict
  """
  _tok = tok.lower()
  return (_tok in ORG)

def isTHING(tok):
  """
  return THING in dict
  """
  _tok = tok.lower()
  return (_tok in THING)


def isPHARSE(tok:list, num_tok, MIN_PHARSE = 3):
  if num_tok > 3:
    return [False]

  if num_tok > 1:
    for t in tok:
      if isLabel(t, start = start, special = [1])[0]:
        return [False]
  tok = ' '.join(tok)
  pharse = len(tok.split(' ')) >= MIN_PHARSE and isnlower(tok)
  if not pharse:
    return [False] 

  _tok = tok.lower()
  _org_start = ['ban ', 'bộ ', 'nhà nước ', 'tổ chức ', 'cơ quan ', 'nhà ', 'đế quốc ', 'cộng hòa ', 'đế chế',
              'ủy ban', 'đội ', 'đảng ', 'đoàn ', 'viện ', 'tổng bộ ', 'tổng cục ', 'trung tâm ', 'tập đoàn ',
              'quân đội ', 'liên ', 'cục ', 'chính phủ ']
  _org_start = ['^' + i for i in _org_start]
  _pattern = '|'.join(_org_start)
  _org_end = [' đảng$', ' hội$']
  _pattern += '|' + '|'.join(_org_end)
  _tok = re.findall(_pattern, _tok)
  if _tok == []:
    return [True, 4]
  else:
    return [True, 2]

def isTIME(tok):
  """
  return TIME in dict
  """
  _tok = tok.lower()
  return (_tok in TIME)


def isN(tok, label, MIN_PHARSE = 3):
  """
  num_tok = 1
  """
  lower = not isnlower(tok)
  noun = bool('N' in label)
  notNpThing1 = not isPHARSE([tok], num_tok = 1, MIN_PHARSE = 3)[0]
  return lower and noun and notNpThing1

def isV(tok, label, MIN_PHARSE = 3):
  """
  num_tok = 1
  """
  verb = bool(label == 'V')
  notNpThing1 = not isPHARSE([tok], num_tok = 1, MIN_PHARSE = 3)[0]
  return verb and notNpThing1

def isA(tok, label, MIN_PHARSE = 3):
  """
  num_tok = 1
  """
  adj = bool(label in ['A', 'S'])
  notNpThing1 = not isPHARSE([tok], num_tok = 1, MIN_PHARSE = 3)[0]
  return adj and notNpThing1

import datetime
def isday(word):
  # 15-17/07/2003
  # 15 17/07/2003
  # 17/07/2003
  # 17/07
  # 17-07
  # 17-20/07
  # 07/2003
  # 05 07/2003
  # 2022 2023
  # 2022-2023
  # 1945
  word = word.replace(' ', '-')
  days = word.split('/')
  days = sum([w.split('-') for w in days], [])
  try:
    days = [int(x) for x in days]
  except:
    return False
  if '-' not in word:
    if len(days) == 3:
      try:
        return bool(datetime.date(days[2], days[1], days[0]))
      except:
        return False

    if len(days) == 2:
      try:
        return bool(datetime.date(days[1], days[0], 1))
      except:
        try:
          return bool(datetime.date(1990, days[1], days[0]))
        except:
          return False

    if len(days) == 1:
      return bool(days[0] in range(1700, 2050))

    return False

  else:
    days = word.split('-')
    for i in range(len(days)-1):
      try:
        days[i] = days[i] + days[-1][days[-1].index("/"):]
      except:
        pass

    return sum([isday(x) for x in days])


def isPre(text, label):
  day = isday(text)
  _label = bool(label in ['M', 'L', 'S'])
  return _label and not day

def isLabel(tok, start = False, special = []):
  """
  num_tok == 1
  1: PER
  2: ORG
  3: LOC
  4: THING
  5: TIME
  """
  if isPER(tok) and (1 not in special):
    return [True,1]
  if isORG(tok) and (2 not in special):
    return [True, 2]
  if isLOC(tok) and (3 not in special):
    return [True, 3]

  if start == True:
    tok = tok[0].lower() + tok[1:]

  if isTHING(tok) and (4 not in special):
    return [True, 4]

  if isTIME(tok) and (5 not in special):
    return [True, 5]

  try:
    if isday(tok):
      return [True, 5]
  except:
    pass

  if (special == []):
    try:
      return [True, isLOC1([tok], num_tok = 1)[1]]
    except:
      return isPHARSE([tok], num_tok = 1)
  return [False]

# L_M_N
# M_N_N
# L_M_A
# N_A_A
def isPharse(tok: list, label:list, num_tok, start = False):
  """
  1: PER
  2: ORG
  3: LOC
  4: THING
  5: TIME
  6: N
  7: V
  8: A
  """
  num_tok = len(tok)
  if num_tok == 1:
    return isLabel(tok[0], start)
  else:
    for t in tok:
      if isLabel(t, start = start, special = [1])[0]:
        return [False]


  _m0 = isPre(tok[0], label[0])
  _m1 = isPre(tok[0], label[0])
  _n0 = isN(tok[0], label[0])
  _n1 = isN(tok[1], label[1])
  _a0 = isA(tok[0], label[0])
  _a1 = isA(tok[1], label[1])
  _v0 = isV(tok[0], label[0])
  _v1 = isV(tok[1], label[1])
  _p0 = isPER(tok[0])
  _p1 = isPER(tok[1])

  
  if num_tok == 2:

    # Per: LM_Nper or Nper_A
    if _m0 and _p1:
      return [True, 1]
    if _p0 and _a1:
      return [True, 1]

    # N: LM_N, N_N, N_A
    if (_m0 or _n0) and _n1:
      return [True, 6]
    if _n0 and _a1:
      return [True, 6]

    # A: AA
    if _a0 and _a1:
      return [True, 8]

    # N: Nc_V
    if label[0] == 'Nc' and _v1:
      return [True, 6]

    if _v0 and (_v1 or _a1):
      return [True, 7]

    return [False]

  if num_tok > 2:
    p1 = isPharse(tok[1:], label[1:], num_tok = num_tok-1)
    try:
      p1[1]
      pass
    except:
      return [False]

    if _m0 :
      if p1[1] in [1,6]:
        return p1
      return [True, 7]

    if _n0 and (p1[1] in [8, 6]):
      return [True, 6]

    if _a0 and p1[1] == 8:
      return [True, 8]

    if _v0 and p1[1] in [7, 8]:
      return [True,7]

    return [False]

def check_label(tok, label, start = False, num_tok = 1):
  if tok == '' or tok == ' ':
    return -1

  toks =tok.split(' ')
  toks = [t.replace('_', ' ') for t in toks]

  p = isPharse(toks, label, num_tok, start)
  if p[0]:
    if p[1] not in [1, 2, 3, 4, 5] and ('nhà' in tok or 'đoàn' in tok):
      return 1
    else:
      return p[1]

  if num_tok > 1:
    return -1

  
  if start == True:
    toks[0] = toks[0][0].lower() + toks[0][1:]

  if isN(toks[0], label[0]):
    return 6
  if isA(toks[0], label[0]):
    return 8
  if isV(toks[0], label[0]):
    return 7

  return 0

labels = {1:'PER',
          2:'ORG',
          3:'LOC',
          4:'THING',
          5:'TIME',
          6:'N',
          7:'V',
          8:'A',
          0:'O',
          -1: 'X'}

def new_label(sent_id, word, label_name, start = False, num_word = 1):
  """
  sent_id: int
  word: str vd: Ho_CHi_Minh di tim
  label: list
  start: bool(is_start)
  num_word in range(1,4)
  """
  _word = word.replace('_', ' ')
  _words = word.split(' ')
  label_id = check_label(word, label_name, start, num_word)

  if label_id != -1 or num_word == 1:
    return[[sent_id, _word, label_name, labels[label_id]]]
  return False


def Matching(toks, max_tok = 5):
  """
  toks: list[[]]
  toks[i] : [id_sent, token, label]

  """
  toks1 = []
  toks_len = len(toks)
  curr_id = 0
  START = False
  id_start = -1



  while curr_id < toks_len:
    #print(toks[curr_id])
    curr_sent = toks[curr_id][0]
    curr_word = toks[curr_id][1]
    curr_label = toks[curr_id][2]

    # check is_start
    if int(curr_sent) > id_start:
      START = True
      id_start += 1
    elif int(curr_sent) == id_start:
      START = False
    else:
      print('ERROR sent_id or id_start')
      break


    def _label(tok, num_words, start = START):
      num_words = len(tok)
      if num_words == 1:
        if (tok[0][2] == 'CH') or (isPre(tok[0][1], tok[0][2])):
          return [True, [[tok[0][0], tok[0][1], tok[0][2], 'O']], 1]
        return [True, new_label(tok[0][0], tok[0][1], tok[0][2], start = START, num_word = num_words), 1]

      if num_words > 1:
        word = " ".join([i[1] for i in tok])
        try:
          t = np.diff([int(i[0]) for i in tok])
          num_words = np.where(t == 1)[0][0] +1
          return _label(tok = tok[:num_words], num_words = num_words, start = START)
        except:
          pass
        try:
          num_words = [i[2] for i in tok].index('CH')
          if num_words == 0:
            return [True, [[tok[0][0], tok[0][1], tok[0][2], 'O']], 1]
          return _label(tok = tok[:num_words], num_words = num_words, start = START)
        except:
          pass
        if new_word := new_label(tok[0][0], word, [i[2] for i in tok], start = START, num_word = num_words):
          return [True, new_word, num_words]
        else:
          return _label(tok = tok[:-1], num_words = num_words - 1, start = START)

    #print(START)
    if curr_id >= toks_len - max_tok:
      num_words = toks_len - curr_id
      new = _label(toks[curr_id: curr_id + num_words], num_words, start = START)
      toks1 += new[1]
      curr_id += new[2]
    else:
      new = _label(toks[curr_id:curr_id + max_tok], max_tok, start = START)
      if new[0]:
        toks1 += new[1]
        curr_id += new[2]


  return toks1

class NER_MATCHING:
  def __init__(self, special = False):
    self.special = special
    pass

  def __format_tok(self, tok):
    if type(tok[2]) != list:
      tok[2] = [tok[2]]

    if ('L' in tok[2]) and (len(tok[1].split(' ')) < 4):
      tok[3] = 'O'

    if self.special == False:
      return [tok[1], tok[3], tok[2]]
    return [tok[1], tok[3]]

  def __connect(self, toks):
    flag = False
    num = -1
    result = []
    queue = []
    for tok in toks:
      if flag == tok[1] and tok[1] not in  ['O', 'M']:
        result[-1][0] += ' ' + tok[0]

      if tok[2] == ['CH']:
        tok[1] = 'CH'


      if tok[2] == ['M']:
        num = 3
        queue.append(tok)

      elif tok[2][0] == 'M' and num > 0:
        t = ''
        for q in queue:
          t += q[0] + ' '
        t += tok[0]
        result.append([t, tok[1], tok[2]])
        queue = []

      elif num > 0:
        queue.append(tok)

      elif num == 0 and queue != []:
        result += queue
        queue = []

      elif num < 0:
        result.append(tok)

      num -=1
      flag = tok[1]

    return [[i[0], i[1]] for i in result]


  def matching(self, sentence_after_annotate, id_sent = 0, max_tok = 5):
    """
    sentence_after_annotate[0] = ['Hồ Chí Minh', 'Np']
    """

    toks = [[str(id_sent), tok[0], tok[1]] for tok in sentence_after_annotate]
    toks = Matching(toks = toks, max_tok = max_tok)

    toks = [self.__format_tok(t) for t in toks]
    toks = self.__connect(toks)

    return toks

class NER_MATCHING:
  def __init__(self, special = False):
    self.special = special
    pass

  def __format_tok(self, tok):
    if type(tok[2]) != list:
      tok[2] = [tok[2]]

    if ('L' in tok[2]) and (len(tok[1].split(' ')) < 4):
      tok[3] = 'O'

    if self.special == False:
      return [tok[1], tok[3], tok[2]]
    return [tok[1], tok[3]]

  def __connect(self, toks):
    flag = False
    num = -1
    result = []
    queue = []
    for tok in toks:
      if flag == tok[1] and tok[1] not in  ['O', 'M']:
        result[-1][0] += ' ' + tok[0]

      if tok[2] == ['CH']:
        tok[1] = 'CH'


      if tok[2] == ['M']:
        num = 3
        queue.append(tok)

      elif tok[2][0] == 'M' and num > 0:
        t = ''
        for q in queue:
          t += q[0] + ' '
        t += tok[0]
        result.append([t, tok[1], tok[2]])
        queue = []

      elif num > 0:
        queue.append(tok)

      elif num == 0 and queue != []:
        result += queue
        queue = []

      elif num < 0:
        result.append(tok)

      num -=1
      flag = tok[1]

    return [[i[0], i[1]] for i in result]


  def matching(self, sentence_after_annotate, id_sent = 0, max_tok = 5):
    """
    sentence_after_annotate[0] = ['Hồ Chí Minh', 'Np']
    """

    toks = [[str(id_sent), tok[0], tok[1]] for tok in sentence_after_annotate]
    toks = Matching(toks = toks, max_tok = max_tok)

    toks = [self.__format_tok(t) for t in toks]
    toks = self.__connect(toks)

    return toks


class NER:
  def __init__(self, token = None, path_phonlp = None, _match = True, normalize = True):
    if token == None:
      self.Token = Tokenize()
    else:
      self.Token = token

    if path_phonlp == None:
      path_phonlp = 'Ner/PhoNLP/phonlp/models/phonlp83/'

    if _match:
      self.matching = NER_MATCHING()
    else:
      self.matching = False

    self.phonlp = phonlp.load(save_dir=path_phonlp)
    self.normalize = normalize


  def NER_matching(self, sentence, id_sent = 0, max_tok = 5):
    if self.normalize == True:
      sentence = text_normalize(sentence)

    toks = self.Token.annotate(sentence)
    toks = self.matching.matching(toks,id_sent = id_sent, max_tok = max_tok)
    toks1  = [toks[0]]
    for i in range(1, len(toks)):
      if toks[i][0] in toks1[-1][0]:
        continue

      toks1.append(toks[i])


    sentence = ' '.join(i[0].replace(' ', '_') for i in toks1)

    return [sentence, toks1]



  def NER_phoNLP(self, sentence, tok = False):

    if tok == False:
      sentence = self.NER_matching(sentence)[0]
    else:
      if self.normalize == True:
        sentence = text_normalize(sentence)
      toks = self.Token.tokenizer(sentence)
      sentence = ' '.join(toks)
    

    toks = self.phonlp.annotate(text=sentence)
    toks = [[toks[0][0][i], toks[2][0][i]] for i in range(len(toks[0][0]))]
    result = []
    for i in range(len(toks)):
      toks[i][0] = toks[i][0].replace('_', ' ')
      toks[i][1] = toks[i][1].replace('B-', '')

      if 'I-' in toks[i][1]:
        result[-1][1] += ' ' + toks[i][0]
        continue
      result.append(toks[i])

    return result


  def NER_sentence(self, sentence, id_sent = 0, max_tok = 5):


    sentence, toks = self.NER_matching(sentence, id_sent = id_sent, max_tok = max_tok)
    toks1 = self.NER_phoNLP(sentence, tok = True)

    for i in range(len(toks)):
      if (toks[i][1] != toks1[i][1]):
        if toks[i][1] == 'CH':
          continue
        #toks[i][1] == 'O'
        i0 = list(labels.keys())[list(labels.values()).index(toks[i][1])]
        i1 = list(labels.keys())[list(labels.values()).index(toks1[i][1])]

        if i1 > 0 and i1 < i0:
          toks[i][1] = toks1[i][1]

    return toks

