import spacy
from collections import Counter
from random import choice as rc


def input_file():
    print('Welcome to the random text generator')
    print()
    print('Choose an option: \n1. Use test file \n2. Provide a url address for another txt.file \n3. Exit program\n')
    answer = input('Option #: ')
    try:
        if answer == '1':
            return (open('corpus.txt', 'r', encoding='utf-8')).read()
        elif answer == '2':
            url = input('Please enter the url address of the file you would like to use: ')
            return (open(url, 'r', encoding='utf-8')).read()
        elif answer in ['3', 'exit']:
            print('Thank you for using the program')
            exit()
    except TypeError:
        print('Please enter a valid option')
        input_file()


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
    print(
        'Number of unique words: ',
        len({token.text for token in doc if token.is_alpha}),
    )
    print('Most common named entities: ', Counter(propers_nouns).most_common(5))
    print('Most common nouns: ', Counter(nouns).most_common(5))
    print('-' * 100)


def menu_choice(document):
    print(
        'Please choose an option: \n1. Generate random sentences \n2. Ask about your favorite character (if your file '
        'contains a character name)')
    answer = input('Option #: ')
    if answer in ['1', '2']:
        print('Please wait...')
        return answer
    else:
        print('Please enter a valid option')
        menu_choice(document)


def tokenize_generate_text(document, option):
    banned_list = ['ca', 'wo', 'nor', 'but', 'both']
    nlp = spacy.load("en_core_web_sm")
    nlp.max_length = 1505477
    doc = nlp(document)
    nouns = list(
        {
            token.text.lower()
            for token in doc
            if token.is_stop != True
               and token.is_punct != True
               and token.pos_ == 'NOUN'
        }
    )
    propers_nouns = list(
        {
            token.text
            for token in doc
            if token.is_stop != True
               and token.is_punct != True
               and token.pos_ == 'PROPN'
        }
    )
    verbs = list(
        {
            token.text.lower()
            for token in doc
            if token.is_stop != True
               and token.is_punct != True
               and token.pos_ == 'VERB'
               and token.text[0] != "'"
               and token.tag_ != 'VBN'
               and '-' not in token.text
        }
    )
    adjectives = list(
        {
            token.text.lower()
            for token in doc
            if token.is_stop != True
               and token.is_punct != True
               and token.pos_ == 'ADJ'
        }
    )
    adverbs = list(
        {
            token.text.lower()
            for token in doc
            if token.is_stop != True
               and token.is_punct != True
               and token.pos_ == 'ADV'
        }
    )
    other_verbs = list(
        {
            token.text.lower()
            for token in doc
            if token.pos_ == 'AUX'
               and token.tag_ != 'VBP'
               and token.text[0] != "'"
               and "'" not in token.text
               and token.text.lower() not in banned_list
               and token.tag_ == 'VBN'
               or token.tag_ == 'VBD'
        }
    )
    verbs_lemma = list(
        {
            token.lemma_.lower()
            for token in doc
            if token.is_stop != True
               and token.is_punct != True
               and token.pos_ == 'VERB'
               and token.text[0] != "'"
               and token.tag_ != 'VBN'
               and '-' not in token.text
        }
    )

    phrase = [
        chunk
        for chunk in doc.noun_chunks
        if len(chunk) > 2 and str(chunk[0]) in {'a', 'The', 'A', 'the'}
    ]
    if option == '1':
        conjunctions = ['and', 'or']
        try:
            print()
            print('How many sentences would you like to generate from the input?')
            sent_num = input()
            print('Generating random sentences...')
            for _ in range(int(sent_num)):
                char_name = str(rc(propers_nouns))
                verb = str(rc(verbs))
                noun = str(rc(nouns))
                other_verb = str(rc(other_verbs))
                phrase_chunk = str(rc(phrase))
                phrase_1_part = phrase_chunk.split()[0]
                phrase_2_part = str(rc(phrase)[1:])
                phrase_3 = str(rc(phrase))
                conjunct = str(rc(conjunctions))
                punct = rc([".", "!", "?"])
                adject = str(rc(adjectives))
                adverb = str(rc(adverbs))
                sentence_1 = f'{char_name.capitalize()} {other_verb} {phrase_1_part.lower()} {phrase_2_part}'
                sentence_2 = f'{phrase_1_part.capitalize()} {phrase_2_part} {char_name} {rc(other_verbs)}'
                sentence_3 = f'{char_name.capitalize()}, {rc(verbs_lemma)}{rc([".", "!", ","])} {phrase_1_part.capitalize()} {phrase_2_part} {conjunct} {phrase_3} {punct} '
                sentence_4 = f'{adject.capitalize()} {noun} {other_verb} {phrase_1_part.lower()} {phrase_2_part}'
                sentence_5 = f'{adverb.capitalize()} {other_verb} {phrase_1_part.lower()} {phrase_2_part}'
                sentence_6 = f'{char_name.capitalize()} and {phrase_1_part.lower()} {phrase_2_part} {verb} {phrase_3}'
                print()
                print(rc([sentence_1, sentence_2, sentence_3, sentence_4, sentence_5, sentence_6]))
        except TypeError:
            print('Please enter a valid number')
            tokenize_generate_text(document, option)

    elif option == '2':
        try:
            _extracted_from_tokenize_generate_text_(phrase, doc, other_verbs)
        except Exception:
            print('Sorry, I could not find any information about this character')


def _extracted_from_tokenize_generate_text_(phrase, doc, other_verbs):
    print()
    print('Type in the name of a character you would like to ask about')
    name = (input('Enter name:')).capitalize()
    phrase_chunk = str(rc(phrase))
    phrase_1_part = phrase_chunk.split()[0]
    phrase_2_part = str(rc(phrase)[1:])
    phrase_2_question = [
        chunk
        for chunk in doc.noun_chunks
        if len(chunk) > 1 and name in str(chunk)
    ]
    print(f'{str(rc(phrase_2_question))} {rc(other_verbs)} {phrase_1_part.lower()} {phrase_2_part}')


def main():
    file = input_file()
    analyze_file(file)
    answer = menu_choice(file)
    tokenize_generate_text(file, answer)


if __name__ == 'main':
    main()
main()
