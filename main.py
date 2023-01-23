import spacy
from collections import Counter
import random as rd


def input_file():
    print('Welcome to the random text generator')
    answer = input('Choose an option: \n1. Use test file \n2. Provide a url address for another txt.file \n')
    if answer == '1':
        doc = (open('corpus.txt', 'r', encoding='utf-8')).read()
    elif answer == '2':
        url = input('Please enter the url address of the file you would like to use: ')
        doc = (open(url, 'r', encoding='utf-8')).read()
    else:
        print('Please enter a valid option')
        input_file()
    return doc


def analyze_file(document):
    print('Loading file statistics...')
    nlp = spacy.load("en_core_web_sm")
    nlp.max_length = 1505477
    doc = nlp(document)
    # File statistics
    nouns = [token.text for token in doc if token.is_stop != True and token.is_punct != True and token.pos_ == 'NOUN']
    propers_nouns = [token.text for token in doc if
                     token.is_stop != True and token.is_punct != True and token.pos_ == 'PROPN']
    print('Number of words: ', len([token.text for token in doc if token.is_alpha]))
    print('Number of sentences: ', len(list(doc.sents)))
    print('Number of unique words: ', len(set([token.text for token in doc if token.is_alpha])))
    print('Most common named entities: ', Counter(propers_nouns).most_common(5))
    print('Most common nouns: ', Counter(nouns).most_common(5))
    print('-' * 110)


def tokenize_generate_text(document):
    sent_num = input('How many sentences would you like to generate from the input?')
    print('Generating random sentences...')
    banned_list = ['ca', 'wo', 'nor', 'but', 'both']
    nlp = spacy.load("en_core_web_sm")
    nlp.max_length = 1505477
    doc = nlp(document)
    # make a list of all nouns
    nouns = list(set([token.text.lower() for token in doc if
                      token.is_stop != True and token.is_punct != True and token.pos_ == 'NOUN']))
    propers_nouns = list(set([token.text for token in doc if
                              token.is_stop != True and token.is_punct != True and token.pos_ == 'PROPN']))
    verbs = list(set([token.text.lower() for token in doc if
                      token.is_stop != True and token.is_punct != True and token.pos_ == 'VERB' and token.text[
                          0] != "'" and token.tag_ != 'VBN' and '-' not in token.text]))
    adjectives = list(set([token.text.lower() for token in doc if
                           token.is_stop != True and token.is_punct != True and token.pos_ == 'ADJ']))
    conjunctions = ['and', 'or']
    adverbs = list(set([token.text.lower() for token in doc if
                        token.is_stop != True and token.is_punct != True and token.pos_ == 'ADV']))
    other_verbs = list(set([token.text.lower() for token in doc if
                            token.pos_ == 'AUX' and token.tag_ != 'VBP' and token.text[
                                0] != "'" and "'" not in token.text and token.text.lower() not in banned_list and token.tag_ == 'VBN' or token.tag_ == 'VBD']))
    verbs_lemma = list(set([token.lemma_.lower() for token in doc if
                            token.is_stop != True and token.is_punct != True and token.pos_ == 'VERB' and token.text[
                                0] != "'" and token.tag_ != 'VBN' and '-' not in token.text]))

    phrase = []
    for chunk in doc.noun_chunks:
        if len(chunk) > 2:
            if str(chunk[0]) == 'a' or str(chunk[0]) == 'The' or str(chunk[0]) == 'A':
                phrase.append(chunk)

    print('*' * 60)
    for i in range(int(sent_num)):
        print()
        a = f'{str(rd.choice(propers_nouns)).capitalize()} {rd.choice(other_verbs)} {str(rd.choice(phrase)).split()[0].lower()} {str(rd.choice(phrase)[1:])}'
        b = f'{str(rd.choice(phrase)).split()[0].capitalize()} {str(rd.choice(phrase)[1:])} {str(rd.choice(propers_nouns))} {rd.choice(other_verbs)}'
        c = f'{str(rd.choice(propers_nouns)).capitalize()}, {rd.choice(verbs_lemma)}{rd.choice([".", "!", ","])} {str(rd.choice(phrase)).split()[0].capitalize()} {str(rd.choice(phrase)[1:])} {str(rd.choice(conjunctions))} {str(rd.choice(phrase)).split()[0].lower()} {str(rd.choice(phrase)[1:])}? '
        d = f'{str(rd.choice(adjectives).capitalize())} {str(rd.choice(nouns))} {str(rd.choice(other_verbs))} {str(rd.choice(phrase)).split()[0].lower()} {str(rd.choice(phrase)[1:])}'
        e = f'{str(rd.choice(adverbs)).capitalize()} {str(rd.choice(other_verbs))} {str(rd.choice(phrase)).split()[0].lower()} {str(rd.choice(phrase)[1:])}'
        print(rd.choice([a, b, c, d, e]))


def main():
    file = input_file()
    analyze_file(file)
    tokenize_generate_text(file)


main()
if __name__ == 'main':
    main()
