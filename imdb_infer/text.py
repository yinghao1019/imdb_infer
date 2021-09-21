
from tokenizers import Tokenizer
import string
import logging
import json
import spacy
import re

# build spacy model for procees text
spacy.prefer_gpu()
en_nlp = spacy.load("en_core_web_md")
ENTITY_MAPPINGS = {"O": 0, "CARDINAL_B": 1, "CARDINAL_I": 2, "DATE_B": 3, "DATE_I": 4, "EVENT_B": 5, "EVENT_I": 6, "FAC_B": 7,
                   "FAC_I": 8, "GPE_B": 9, "GPE_I": 10, "LANGUAGE_B": 11, "LANGUAGE_I": 12, "LAW_B": 13, "LAW_I": 14, "LOC_B": 15,
                   "LOC_I": 16, "MONEY_B": 17, "MONEY_I": 18, "NORP_B": 19, "NORP_I": 20, "ORDINAL_B": 21, "ORDINAL_I": 22, "ORG_B": 23,
                   "ORG_I": 24, "PERCENT_B": 25, "PERCENT_I": 26, "PERSON_B": 27, "PERSON_I": 28, "PRODUCT_B": 29, "PRODUCT_I": 30,
                   "QUANTITY_B": 31, "QUANTITY_I": 32, "TIME_B": 33, "TIME_I": 34, "WORK_OF_ART_B": 35, "WORK_OF_ART_I": 36}

# replace html element in context
NonHtml = re.compile(
    r"<[^<]+?>|<!--.*?-->|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
# remove continous punctations
rmpct = re.compile(r"[^\w\.,;\?\!<=>\/$'\s]|[\.,;\?\!<=>\/$']{2,}")

def load_tokenizer(token_path):

    with open(token_path,"r",encoding="utf-8") as f_r:
        params=f_r.read().strip()

    tokenizer=Tokenizer.from_str(params)

    return tokenizer



def strip_html(text):
    text = NonHtml.sub("", text)
    return text


def rm_punct(text):
    text = rmpct.sub("", text)
    return text


def nlp_preprocess(text, tokenizer):
    tokens = []
    ents = []
    for t in en_nlp(text):
        if t.text not in string.punctuation:
            words = [t.text.lower()]
            # split word to subword
            words = tokenizer.encode(words, is_pretokenized=True).tokens
            tokens.extend(words)

            # extract subword name entity type with BIO scheme
            if t.ent_type_:
                ents.extend([t.ent_type_+"_"+t.ent_iob_]*len(words))
            else:
                ents.extend(["O"]*len(words))

    # confirm subword hae correct entity
    assert len(tokens) == len(ents), \
        f"The sent len not equal to entites num\n Token len:{len(tokens)},entites num:{len(ents)}"

    return tokens, ents


def nlp_potsprocess(tokens, ents, tokenizer):
    texts = []

    for t, e in zip(tokens, ents):
        texts.append((tokenizer.token_to_id(t), ENTITY_MAPPINGS[e]))
    return zip(*texts)

# set logger logging message
def init_logger():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                        datefmt=r'%m/%d/%Y %H:%M:%S',
                        level=logging.INFO)
