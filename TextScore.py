import inspect

from Scores import DistanceScore
from Tokenizers import tokenize_words
from Tokenizers import tokenize_sentence


def edit_distance(word_a, word_b):
    length_a = len(word_a)
    length_b = len(word_b)

    # this approach assumes the length of a <= length of b

    list_a = list(word_a)
    list_b = list(word_b)

    if length_b < length_a:
        list_a = list(word_b)
        list_b = list(word_a)

    position_a = 0
    edit_count = 0

    while position_a < len(list_a):
        if list_a[position_a] != list_b[position_a]:
            if len(list_b) > length_a and list_a[position_a] == list_b[position_a + 1]:
                edit_count = edit_count + 1
                position_a = position_a + 1
                list_b = list_b[:position_a] + list_b[position_a + 1:]
            else:
                edit_count = edit_count + 1
                list_b[position_a] = list_a[position_a]

                if position_a != len(list_a) - 1:
                    # minimize edits delete elements from b until a matches b at some point. If there are no matches then
                    # that means the rest of the edits will be substitutions. Only delete up to the first match, going
                    # further may create an excessive amount of edits
                    match_index = find_first_match(list_a[position_a+1], position_a+1, list_b)
                    if match_index is not None:
                        first_matching_pair_index = find_first_match2(position_a+1, list_a, list_b)
                        if first_matching_pair_index is None or first_matching_pair_index >= match_index:
                            list_b = list_b[:position_a + 1]+list_b[match_index:]
                            edit_count = edit_count + (match_index - (position_a + 1))

                position_a = position_a + 1
        else:
            position_a = position_a + 1

    if len(list_a) < len(list_b):
        edit_count = edit_count + len(list_b) - len(list_a)

    return edit_count


def edit_score(word_a, word_b):
    distance = edit_distance(word_a, word_b)
    max_length = max(len(word_b), len(word_a))

    return DistanceScore(distance, max_length)

    # if distance == 0:
    #     return 1
    # else:
    #     return 1 - (distance / max_length)


def find_first_match(search_char, starting_position, char_list):
    # find the first matching character, else return None if no match is found
    try:
        return char_list.index(search_char, starting_position)
    except ValueError:
        return None


def find_first_match2(starting_position, list_a, list_b):
    for i in range(starting_position, len(list_a)):
        for j in range(i, len(list_b)):
            if list_a[i] == list_b[j]:
                return i

    return None


def sentence_score(sentence_a, sentence_b):
    words_a = tokenize_words(sentence_a)
    words_b = tokenize_words(sentence_b)

    if len(words_b) < len(words_a):
        words_a = tokenize_words(sentence_b)
        words_b = tokenize_words(sentence_a)

    word_to_scores_dict = {}

    for i, word_a in enumerate(words_a):
        scores = []
        for j, word_b in enumerate(words_b):
            if j >= i:
                scores.append((i, j, edit_score(word_a, word_b)))
        best_score = sorted(scores, key=lambda x: x[2].edit_distance).pop(0)
        word_to_scores_dict.update({i: best_score})

    total_max_score = 0
    total_score = 0
    for k, v in word_to_scores_dict.items():
        total_score = total_score + v[2].edit_distance
        total_max_score = total_max_score + v[2].max_score
        word_b_index = v[1]
        word_a_index = v[0]
        if v[2].edit_distance != v[2].max_score:
            # if the match is less then max (meaning no match), swap in the word this will
            # get around small changes with words or punctuation
            words_b[word_b_index] = words_a[word_a_index]

    sentence_edit_score = edit_score(words_a, words_b)

    total_score = total_score + sentence_edit_score.edit_distance
    total_max_score = total_max_score + sentence_edit_score.max_score

    return DistanceScore(total_score, total_max_score)


def text_score(text_a, text_b):

    sentences_a = [inspect.cleandoc(y) for y in tokenize_sentence(text_a) if len(y) > 0]
    sentences_b = [inspect.cleandoc(x) for x in tokenize_sentence(text_b) if len(x) > 0]

    if len(sentences_b) < len(sentences_a):
        sentences_a = [inspect.cleandoc(x) for x in tokenize_sentence(text_b) if len(x) > 0]
        sentences_b = [inspect.cleandoc(y) for y in tokenize_sentence(text_a) if len(y) > 0]

    word_to_scores_dict = {}

    for i, word_a in enumerate(sentences_a):
        scores = []
        for j, word_b in enumerate(sentences_b):
            if j >= i:
                scores.append((i, j, sentence_score(word_a, word_b)))
        best_score = sorted(scores, key=lambda x: x[2].edit_distance).pop(0)
        word_to_scores_dict.update({i: best_score})

    total_max_score = 0
    total_score = 0
    for k, v in word_to_scores_dict.items():
        total_score = total_score + v[2].edit_distance
        total_max_score = total_max_score + v[2].max_score
        word_b_index = v[1]
        word_a_index = v[0]
        if v[2].edit_distance != v[2].max_score:
            # if the match is less then max (meaning no match), swap in the word this will
            # get around small changes with words or punctuation
            sentences_a[word_b_index] = sentences_b[word_a_index]

    sentence_edit_score = edit_score(sentences_a, sentences_b)

    total_score = total_score + sentence_edit_score.edit_distance
    total_max_score = total_max_score + sentence_edit_score.max_score

    return DistanceScore(total_score, total_max_score)