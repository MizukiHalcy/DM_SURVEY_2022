import random
import spacy
import pandas

from config import CREATURES_NAME_XLSX_PATH

tribe = "アーマード・ドラゴン"
nlp = spacy.load("ja_ginza")

def generate_model_from_df(df):
    model = {"root" : [], "conpound": []}
    for index, data in df.iterrows():
        name = data[0]
        generated = generate_model(name)
        model["root"].extend(generated["root"])
        model["conpound"].extend(generated["conpound"])
    return model

def generate_model(name):
    model = {"root" : [], "conpound": []}
    doc = nlp(name)
    for sent in doc.sents:
        for token in sent:
            if token.dep_ == "ROOT":
                model["root"].append(token)
            else:
                model["conpound"].append(token)
    return model

def generate_creature_name(model):
    sentence_number = random.randint(1, 3)
    root_name = random.choice(model["root"])
    conpounds = get_conpounds(model["conpound"], root_name)
    secounds_name = random.choice(conpounds)
    others = random.sample([i for i in model["conpound"]], sentence_number)
    others.append(secounds_name)
    others.append(root_name)
    return others

def normalize(tokens, l):
    raw = []
    tokens_itr = iter(tokens)
    x = next(tokens_itr)
    for y in tokens_itr:
        if x.tag_ == "SYM" and y.tag_ == "SYM":
            raw.append(get_name_expect_sym(l))
        else:
            raw.append(y)
    return raw


def get_conpounds(l, root_name):
    conpounds = [i for i in l if i.head.text == root_name.text]
    if len(conpounds) == 0:
        return get_conpounds(l)
    return conpounds

def get_name_expect_sym(l):
    name = random.choice(l)
    if name.tag_ == "SYM":
        return get_name_expect_sym(l)
    return name


df = pandas.read_excel(CREATURES_NAME_XLSX_PATH, sheet_name=tribe)
model = generate_model_from_df(df)
name = generate_creature_name(model)
print(name)
