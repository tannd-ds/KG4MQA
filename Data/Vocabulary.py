from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import pandas as pd
import string
import re
from urllib.parse import unquote
from collections import defaultdict
import unicodedata as ud
import numpy as np
import math
import ast
from langdetect import detect
import joblib

def format_search_uri (search):
  return quote_plus((search.replace(' ', '_').encode('utf-8')))
  #return searchs
def uri2str(uri):
  return unquote(uri)

def get_all_links_in_page (searchs, soups_xml, parent):
  pattern  = r"/wiki/(\S+)"
  for paragraph in soups_xml.find_all('p'):
    for link in paragraph.find_all('a'):
      search = re.findall(pattern, link.get('href',''))
      if search == []:
        continue
      if search[0] not in [row[0] for row in searchs]:
        search.append(parent)
        searchs.append(search)
        with open('Data/resources/searchs.txt', 'a', encoding='utf-8') as f:
          f.writelines(','.join(search))
          f.write('\n')
        f.close()


  return searchs

def update_search(raw_sources : list, soups_xml : list, searchs : list, start = 0, end = 20):
  while start < len(searchs):
    url = f'https://vi.wikipedia.org/wiki/{format_search_uri(searchs[start][0])}'
    try:
      raw_source = urlopen(url).read()
      raw_sources.append(raw_source)
    except:
      searchs.pop(start)
      continue
    soup_xml = BeautifulSoup(raw_source, 'lxml')
    soups_xml.append(soup_xml)
    searchs = get_all_links_in_page(searchs, soup_xml, url)
    print(len(searchs))
    start += 1
    if start == end:
      print('sucess')
      break


def word2regex(word):
  regex = "\\b"
  for i in word:
    regex += f"[{i.upper()}{i.lower()}]"

  return regex+'\\b'

def regex2word(regex):
  """
  regex: \\b[Nn][Gg][Uu][Yy][Ễễ][Nn][  ][Tt][Hh][Ịị]\\b
  """
  if len(re.findall(r'\\b', regex)) != 2:
    return False
  word = ''
  _regex = regex[2:-2]
  for i in range(2, len(_regex), 4):
    word += _regex[i]

  punct = set(string.punctuation)
  pattern = '|'.join(['\\' + i for i in punct])
  if re.findall(pattern, word) != [] or not word.islower():
    #print(_regex)
    return False

  return word

def get_vocabulary(path_vocabulary = None):
  if path_vocabulary == None:
    path_vocabulary = '/content/drive/MyDrive/[1]Colab_Notebooks/[0]Project/[1]viMuQA/Auto/Data/resources/data.txt'

  with open(path_vocabulary, 'r', encoding = 'utf-8') as f:
    data = set(f.read().split('\n')) - {'', ' '}
    data = list(sorted(data, reverse=True, key = len))

  return data

def isregex(x):
  if bool(regex2word(x)):
    return True
  return False

def isword(x):
  return bool(regex2word(word2regex(x)))


def insert_vocab(vocab, data = None, path = None):
  
  if path == None:
    path = '/content/drive/MyDrive/[1]Colab_Notebooks/[0]Project/[1]viMuQA/Auto/Data/resources/data.txt'
  if data == None:
    data = get_vocabulary(path)

  for x in vocab:
    if is_vocab(x, data):
      continue

    if isregex(x):
      data.append(x)
    elif isword(x):
      data.append(word2regex(x))

  with open(path, 'w', encoding = 'utf-8') as f:
    f.write('\n'.join(data))

  
  
  return data

def is_vocab(x, data = None):
  if data == None:
    data = get_vocabulary()
  if isregex(x):
    return (x in data)
  elif isword(x):
    return (word2regex(x) in data)

  return False

def remove_data(vocab, data = None, path = None):
 
  if path == None:
    path = '/content/drive/MyDrive/[1]Colab_Notebooks/[0]Project/[1]viMuQA/Auto/Data/resources/data.txt'

  if data == None:
    data = set(get_vocabulary())
  for x in vocab:
    if isregex(x):
      data = data - {x}
    elif isword(x):
      data = data - {regex2word(x)}
    else:
      print(x, ' not in vocabulary')

    
  with open(path, 'w', encoding = 'utf-8') as f:
    f.write('\n'.join(data))

  return data

def Get_File(filename, path_core = None):
  """
  LOC, ORG, PER, THING, TIME
  """
  if path_core == None:
    path_core = "/content/drive/MyDrive/[1]Colab_Notebooks/[0]Project/[1]viMuQA/Auto/Data/NER/"
  with open(path_core + filename + '.txt', 'r', encoding = 'utf-8') as f:
    locals()[filename] =  list(set(f.read().split('\n')) - {''})
  locals()[filename] = sum([s.split(',') for s in locals()[filename]], [])
  for i in range(len(locals()[filename])):
    #locals()[filename][i] = re.sub(r'\(.+\)', '', locals()[filename][i])
    locals()[filename][i] = re.sub(r'\s+', ' ', locals()[filename][i])
    if locals()[filename][i][0] == ' ':
      locals()[filename][i] = locals()[filename][i][1:]
    if locals()[filename][i][-1] == ' ':
      locals()[filename][i] = locals()[filename][i][:-1]
  locals()[filename] = sorted(set([x.lower() for x in locals()[filename]]))
  
  return locals()[filename]

def Save_File(data, filename, path_core = None):
  """
  LOC, ORG, PER, THING, TIME
  """
  if path_core == None:
    path_core = "/content/drive/MyDrive/[1]Colab_Notebooks/[0]Project/[1]viMuQA/Auto/Data/NER/"
  with open(path_core + filename + '.txt', 'w', encoding = 'utf-8') as f:
    f.write('\n'.join(data))
  

def Insert_File(word : list, data = None, filename = None, path_core = None):
  if data == None and filename == None:
    raise Exception('No file to insert')
  
  if data == None:
    _data = Get_File(filename, path_core)

  _data = set(data)
  _data.update(word)

  if data == None:
    Save_File(_data, filename, path_core)
  
  return _data
