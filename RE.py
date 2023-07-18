from Data.Vocabulary import *
from Data.Text_normalize import *
from Tokenize.Tokenize import *
from Ner.Ner import *

def compact_sentence(toks: list):
  """
  just 1 sentence
  toks[0]: ['Hồ Chí Minh', 'PER']
  """
  root = False
  entity = []
  flag = False
  flag1 = False
  queue = []
  for tok in toks:
    if root == False and tok[1] in ['PER', 'ORG', 'THING']:
      root = tok[0]
      entity.append(tok)
      continue

    if root == False:
      continue

    if tok[0] in entity[-1][0]:
      continue

    if tok[1] == flag1 and queue != []:
      entity.append(queue)
      flag1 =False
      queue = []

    if len(tok[1]) > 1:
      entity.append(tok)
      flag = False
      flag1 = tok[1]
      continue

    if tok[1] == 'V':
      flag = True
      flag1 = tok[1]
      entity.append(tok)
      continue

    if flag == True and tok[1] == 'N':
      flag = True
      entity.append(tok)
      flag1 = tok[1]
      continue

    if tok[1] == 'O':
      queue = tok


  return entity

def Entity(tok):
  x = int(len(tok.split(' ')) >= 3)
  x += int(isnlower(tok))

  return bool(x) and (x not in ['tên'])

def is_Entity(tok):
  if (tok[1] in ['PER', 'ORG', 'THING', 'TIME', 'LOC']):
    return True
  if Entity(tok[0]) and tok[1]== 'N':
    return True


def get_root(tok):
  #tok = compact_sentence(tok)
  try:
    root = [compact_sentence(tok)[0]]
  except:
    root = []
    return root
    pass
  flag = False
  for i in range(1,len(tok)):
    if tok[i] in root:
      continue
    if tok[i][0] in ['của', 'ở', 'là']:
      return root
    elif tok[i][1] in ['O', 'CH']:
      pass
    elif tok[i][1] == root[0][1]:
      root.append(tok[i])
    elif tok[i][1] in ['PER', 'ORG']:
      root.append(tok[i])
    else:
      return root


import string
punct = list(string.punctuation)  + ['–']


def insert_sentence(toks, root):
  t = []
  for r in root:
    for tok in toks:
      x = [r] + tok[1:]
      t.append(x)

  return t


def new_sentence(toks):
  _root = get_root(toks)
  if _root == []:
    return [[], []]
  root = [_root[0]]

  result= []
  for i in range(len(toks)):
    if is_Entity(toks[i]):
      result.append(toks[i])
    if toks[i][1] == 'CH' and toks[i][0] != '.' and toks[i+1][1] in ['V', 'O']:
      result += root
    if toks[i][1] in ['V', 'O']:
      result.append(toks[i])
      flag = True
    else:
      flag = False

  result += [['.', 'CH']]

  _new = 0
  new = []
  for i in range(1, len(result)):
    if (result[i] in root) or (result[i] == ['.', 'CH']):
      new.append(result[_new: i])
      _new = i
  if len(_root) > 1:
    new = insert_sentence(new, _root)

  return [new, _root]

def is_equal(toks, between):
  T = [i[0] for i in between]
  R = [i[1] for i in between]
  flag = False
  if 'của' in toks[2]:
    return False
  if len(between) < 3 and  ('V' not in R):
    flag = True
  if 'như' in T and len(between) < 7:
    flag = True
  if toks[0][1] == toks[1][1] and flag:
    return True

  return False

def remove_duplicate(triples):
  result = []

  for i in triples:
    if i == [] or i in result:
      continue
    result.append(i)

  return result

def is_triple(toks, between, root):
  """
  toks: [[E1, N1], [E2, N2], [R, NR]]
  between: [[E, N],...]

  return if:
  E1: PER, THING, ORG, LOC
  E2: PER, THING,
  """

  E1 = toks[0]
  E2 = toks[1]
  R = toks[2]
  V = bool('V' in [i[1] for i in between])

  if is_equal(toks, between):
    return [False, [E1[0], E2[0]]]

  if E2 in root:
    return [False]

  if E1[0] == E2[0]:
    return [False]


  # R: la
  if R == 'là':
    if E1[1] == 'PER' and E2[1] == 'PER':
      return [True, toks]
    if E1[1] == 'THING' and E2[1] == 'THING':
      return [True, toks]

    return [False]

  # E2: LOC
  if E1[1] == 'LOC':
    return [False]
  if E2[1] == 'LOC':
    if 'ở' not in R:
      R += ' ở'
      return [True, [E1, E2, R]]
    return [True, toks]



  return [True, toks]


def extract_relation(e1, e2, toks, special = False):
  flag = False
  flag1 = False
  flag2 = False
  relation = []
  for tok in toks:
    if tok == e1:
      flag = True
    if tok == e2:
      flag = False
    if flag and (tok[1] == 'V') :
      relation.append(tok)
      flag1 = True
    if flag and tok[0] in ['của', 'ở', 'là']:
      relation = [tok]
      flag1 = False
    if flag and tok[1] == 'O' and tok[0] not in punct:
      flag2 = True

  if relation != []:
    return [e1, e2, ' '.join([i[0] for i in relation])]
  if flag2 and not special:
    return [False]

  if e1[1] == 'PER':
    if e2[1] == 'PER':
      return [e1, e2, 'là']

    #if e2[1] == 'TIME' and isNp(e1[0]) and next_to:
      #return [e1, e2, 'DAY_OF_BIRTH']

    if e2[1] == 'TIME' and not isNp(e1[0]):
      return [e1, e2, 'từ']

    if e2[1] == 'ORG':
      return [e1, e2, 'của']

  if e1[1] == 'THING':
    if e2[1] == 'ORG':
      return [e1, e2, 'của']
    if e2[1] == 'PER':
      return [e1, e2, 'của']
    if e2[1] == 'LOC':
      return [e1, e2, 'ở']
    if e2[1] == 'TIME':
      return [e1, e2, 'từ']

  if e2[1] == 'LOC':
    if e1[1] in ['ORG']:
      return [e1, e2, 'ở']

  return [False]



def extract_triple(tok, root, step = 17, special = False):

  E2 = []
  E1 = []
  triple = []
  entity = [i for i in enumerate(tok) if is_Entity(i[1])]
  flag = True
  non = [i for i in tok if is_Entity(i)]
  equals = []

  if len(entity) < 6:
      special= True
  while flag and (len(non) > 0) and step>0:
    for i in range(len(entity) - 1):
      if step <= 5:
        special= True
      x = extract_relation(entity[i][1], entity[i+1][1], tok, special = special)
      if x[0] != False:
        x = is_triple(toks = x, between= tok[entity[i][0]+1: entity[i+1][0]], root= root)
        if x[0] != False:
          E1.append(x[1][0])
          E2.append(x[1][1])
          try:
            if x == triple[-1]:
              flag = False
          except:
            pass
          if x[1] in triple:
            pass
          else:
            triple.append(x[1])
        else:
          try:
            equal = x[1]
            if equal not in equals:
              equals.append(equal)
          except:
            pass
    entity = [i for i in entity if i[1] not in E2 or i[1] in E1]
    non = [i[1] for i in entity if i[1] not in E2 and i[1] not in E1]
    step -=1

  triple = [[t[0][0], t[1][0], t[2]] for t in triple]


  flag = False
  for i in range(len(triple)):
    if flag == False and triple[i][2] == 'từ':
      flag = triple[i][0]

    elif triple[i][0] == flag and triple[i][2] == 'từ':
      triple[i][2] = 'đến'

  _len = len(triple)
  for i in equals:
    for j in range(_len):
      if triple[j][0] in i:
        triple[j][0] = i[0]
        triple.append([i[1], triple[j][1], triple[j][2]])
      if triple[j][1] in i:
        triple[j][1] = i[0]
        triple.append([triple[j][1], i[1], triple[j][2]])

  return triple

def extract_triples(toks, triples = []):
  toks, root = new_sentence(toks)
  for tok in toks:
    triples += extract_triple(tok, root)

  triples = remove_duplicate(triples)

  return triples
