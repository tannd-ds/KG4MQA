
# KNOWLEDGE GRAPH FOR MULTI-HOP QUESTION ANSWERING

Question Answering (QA) is an important problem in Natural Language Processing (NLP); however, several limitations persist, particularly in the realm of Vietnamese language processing. A major challenge lies in the ability to infer complex reasoning. Additionally, historical language data remains underutilized, presenting an opportunity for further exploration. As a response to these challenges, We do a research and develop the Multi-hop QA problem for Vietnamese history, employing the power of Knowledge Graphs.

However, the model has not achieved the expected accuracy and complexity, our team will continue on developing the model and historical vocabulary to expand the Knowledge Graph and improve the Multi-hop QA tool based on the knowledge graph in the future.

![image](https://github.com/tannd-ds/vi-potqa/assets/64354200/29bfef36-d7e9-474f-a260-968e5a37281f)

Details of the models and experimental results can be found in the following report.

Our model is available at [https://github.com/ndp1707/KG4MQA](https://github.com/tannd-ds/KG4MQA)
## Result


| Models                        | Accuracy    |
|-------------------------------|-------------|
| Token+NER\_MATCHING           | 53.5046     |
| Token+NER\_phoNLP             | 43.1433     |
| **Token+NER\_sentence**       | **56.7348** |
| Token+NER\_original\_sentence | 53.7337     |
| Longest+NER\_MATCHING         | 52.9981     |
| Longest+NER\_phoNLP           | 43.143      |
| **Longest+NER\_sentence**     | **56.3394** |
| Underpy+NER\_MATCHING         | 52.8087     |
| Underpy+NER\_phoNLP           | 41.1765     |
| Underpy+NER\_sentence         | 56.0173     |


## Data

- Wikipedia
- [A collection of Vietnamese data files in text format for language processing](https://github.com/winstonleedev/tudien/tree/master)
- [Multi-hop QA Dataset (vi-potpa)](https://github.com/tannd-ds/vi-potqa)





## Usage/Examples

### Vocabulary

```python
from Data.Vocabulary import

# Get word_regex from Vocabulary
get_vocabulary(path_vocabulary = '/absolute/path/to/vocabulary')
# \\b[Hh][Ồồ][  ][Cc][Hh][Íí][  ][Mm][Ii][Nn][Hh]\\b


# Insert word_list into vocabulary
insert_vocab(word_list, data = vocabulary , path= '/absolute/path/to/vocabulary')


# Remove word_list from vocabulary
remove_data(word_list, data = vocabulary , path= '/absolute/path/to/vocabulary')

```


### TOKENIZE, POSTAG
- Tokenize based on Longest_matching, [underthesea](https://github.com/undertheseanlp/underthesea) and [Pyvi](https://github.com/trungtv/pyvi)
```python
from Tokenize.Tokenize import Tokenize, longest_matching, Underthesea_pyvi

model = Tokenize(vocab = True)

model.tokenizer(text = 'Hồ Chí Minh là nhà cách mạng cộng sản Việt Nam .')
# Hồ_Chí_Minh là nhà_cách_mạng_cộng_sản Việt_Nam

model.annotate(text = 'Tôi là nhà cách mạng cộng sản Việt Nam .')
# [['Hồ_Chí_Minh', 'P'], ['là', 'V'], ['nhà_cách_mạng_cộng_sản', 'N'], ['Việt_Nam', 'Np'], ['.', 'CH']]

```

### NER

- Our NER() approach based on [PhoNLP](https://github.com/VinAIResearch/PhoNLP) with [PhoBERT](https://github.com/VinAIResearch/PhoBERT)-base pretrain and our Historical Dictionary.
- The pre-trained phonlp for History of VietNam can be manually downloaded from [here](https://drive.google.com/file/d/13Y0alDyz_Q7cHli5ytYuiwxu1yo7ijwE/view?usp=drive_link)
```python
from ner.ner import NER

model = NER(token = Tokenize(), path_phonlp = '/absolute/path/to/phonlp_dict', normalize = True)


model.NER_sentence(sentence = 'Tôi là nhà cách mạng cộng sản Việt Nam .')
# [['Hồ_Chí_Minh', 'PER'], ['là', 'V'], ['nhà_cách_mạng_cộng_sản', 'PER'], ['Việt_Nam', 'LOC'], ['.', 'CH']]

```

### EXTRACT RELATION

```python
from ner.ner import NER
from RE.RE import extract_triples(tok, triples= result)

model = NER(token = Tokenize(), path_phonlp = '/absolute/path/to/phonlp_dict', normalize = True)


toks = model.NER_sentence(sentence = 'Tôi là nhà cách mạng cộng sản Việt Nam .')
# [['Hồ_Chí_Minh', 'PER'], ['là', 'V'], ['nhà_cách_mạng_cộng_sản', 'PER'], ['Việt_Nam', 'LOC'], ['.', 'CH']]

extract_triples(toks = toks, triples= triples)
# [['Hồ Chí Minh', 'nhà cách mạng cộng sạn', 'là'], ['nhà cách mạng cộng sản', 'Việt Nam', 'ở'], ['Hồ Chí Minh', 'Việt Nam', 'ở']

```
## Authors

- [@Tan Nhat Do - 21522575@gm.uit.edu.vn](https://github.com/tannd-ds)
- [@Phuong Dieu Nguyen - 21520091@gm.uit.edu.vn](https://github.com/Ndphuong-17)
