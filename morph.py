import random
import spacy
import pandas

from config import CREATURES_NAME_XLSX_PATH

tribe = "エンジェル・コマンド"
nlp = spacy.load("ja_ginza")

def generate_model_from_df(df):
    model = {"root" : [], "conpound": [], "start": []}
    for index, data in df.iterrows():
        name = data[0]
        generated = generate_model(name)
        model["root"].extend(generated["root"])
        model["conpound"].extend(generated["conpound"])
        model["start"].extend(generated["start"])
    return model

def generate_model(name):
    model = {"root" : [], "conpound": [], "start": []}
    doc = nlp(name)
    for sent in doc.sents:
        for index, token in enumerate(sent):
            if index == 0:
                model["start"].append(token)
            elif index + 1 == len(sent):
                model["root"].append(token)
            else:
                model["conpound"].append(token)
    return model

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

def model_fitting_both(model):
    counter = {}
    counter["root"] = model_fitting(model["root"])
    counter["conpound"] = model_fitting(model["conpound"])
    counter["start"] = model_fitting(model["start"])
    return counter

def model_fitting(model):
    counter = {}
    for token in model:
        if token.text in counter.keys():
            counter[token.text] += 1
        else:
            counter[token.text] = 1
    return counter

def counter_generate(counter):
    gause_numbers = []
    for key, value in counter.items():
        for i in range(value):
            gause_numbers.append(key)
    index = random.randrange(len(gause_numbers))
    return gause_numbers[index]

def generate_creature_name(counter, input_name):
    name = []
    conpounds = []
    name.append(counter_generate(counter["start"]))
    count = random.randrange(0, 3)
    for i in range(count):
        conpound = counter_generate(counter["conpound"])
        conpounds.append(conpound)
    conpounds.insert(random.randint(0, len(conpounds)), input_name)
    name.extend(conpounds)
    name.append(counter_generate(counter["root"]))
    return name

def main():
    input_name = "ハルプブ"
    df = pandas.read_excel(CREATURES_NAME_XLSX_PATH, sheet_name=tribe)
    model = generate_model_from_df(df)
    counter = model_fitting_both(model)
    name = generate_creature_name(counter, input_name)
    print(name)

if __name__ == "__main__":
    main()
