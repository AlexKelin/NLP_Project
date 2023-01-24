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


def menu_choice(document):
    print('Please choose an option: \n1. Generate random sentences \n2. Ask about you favorite character')
    answer = input('Option #: ')
    if answer == '1' or answer == '2':
        print('Please wait...')
        tokenize_generate_text(document, answer)
    else:
        print('Please enter a valid option')
        menu_choice(document)


def tokenize_generate_text(document, option):
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
    option_1 = f'{str(rd.choice(propers_nouns)).capitalize()} {rd.choice(other_verbs)} {str(rd.choice(phrase)).split()[0].lower()} {str(rd.choice(phrase)[1:])}'
    option_2 = f'{str(rd.choice(phrase)).split()[0].capitalize()} {str(rd.choice(phrase)[1:])} {str(rd.choice(propers_nouns))} {rd.choice(other_verbs)}'
    option_3 = f'{str(rd.choice(propers_nouns)).capitalize()}, {rd.choice(verbs_lemma)}{rd.choice([".", "!", ","])} {str(rd.choice(phrase)).split()[0].capitalize()} {str(rd.choice(phrase)[1:])} {str(rd.choice(conjunctions))} {str(rd.choice(phrase)).split()[0].lower()} {str(rd.choice(phrase)[1:])}{rd.choice([".", "!", "?"])} '
    option_4 = f'{str(rd.choice(adjectives).capitalize())} {str(rd.choice(nouns))} {str(rd.choice(other_verbs))} {str(rd.choice(phrase)).split()[0].lower()} {str(rd.choice(phrase)[1:])}'
    option_5 = f'{str(rd.choice(adverbs)).capitalize()} {str(rd.choice(other_verbs))} {str(rd.choice(phrase)).split()[0].lower()} {str(rd.choice(phrase)[1:])}'


    if option == '1':
        try:
            print()
            print('How many sentences would you like to generate from the input?')
            sent_num = input()
            print('Generating random sentences...')
            for i in range(int(sent_num)):
                print()
                print(rd.choice([option_1, option_2, option_3, option_4, option_5]))
        except:
            print('Please enter a valid number')
            tokenize_generate_text(document, option)

    elif option == '2':
        try:
            print()
            print('Type in the name of a character you would like to ask about')
            name = (input('Enter name:')).capitalize()
            phrase_2_question = []
            for chunk in doc.noun_chunks:
                if len(chunk) > 1:
                    if name in str(chunk):
                        phrase_2_question.append(chunk)
            print(f'{str(rd.choice(phrase_2_question)).capitalize()} {rd.choice(other_verbs)} {str(rd.choice(phrase)).split()[0].lower()} {str(rd.choice(phrase)[1:])}')
        except:
            print('Sorry, I could not find any information about this character')



def main():
    file = input_file()
    analyze_file(file)
    menu_choice(file)


main()
if __name__ == 'main':
    main()
