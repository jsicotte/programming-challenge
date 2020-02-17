import inspect

from Scores import DistanceScore
from Tokenizers import tokenize_words
from Tokenizers import tokenize_sentence


def edit_distance(word_a, word_b):
    """ Calculate the edit distance between two lists. As long as the elements in the list can be compared this
    function will produce an edit distance
    """
    list_a, list_b = _shortest_first(list(word_a), list(word_b))
    length_a = len(list_a)

    position_a = 0
    edit_count = 0

    while position_a < length_a:
        if list_a[position_a] != list_b[position_a]:
            if len(list_b) > length_a and list_a[position_a] == list_b[position_a + 1]:
                position_a = position_a + 1
                list_b = list_b[:position_a] + list_b[position_a + 1:]
            else:
                list_b[position_a] = list_a[position_a]

                if position_a != len(list_a) - 1:
                    # minimize edits by using a delete from b until a matches b at some point. If there are no matches
                    # then that means the rest of the edits will be substitutions. Only delete up to the first match,
                    # going further may create an excessive amount of edits
                    match_index = find_first_match(list_a[position_a+1], position_a+1, list_b)
                    if match_index is not None:
                        first_matching_pair_index = find_first_matching_pair(position_a+1, list_a, list_b)
                        if first_matching_pair_index is None or first_matching_pair_index >= match_index:
                            list_b = list_b[:position_a + 1]+list_b[match_index:]
                            edit_count = edit_count + (match_index - (position_a + 1))

                position_a = position_a + 1
            edit_count = edit_count + 1
        else:
            position_a = position_a + 1

    if len(list_a) < len(list_b):
        edit_count = edit_count + len(list_b) - len(list_a)

    return edit_count


def edit_distance_score(word_a, word_b):
    distance = edit_distance(word_a, word_b)
    max_length = max(len(word_b), len(word_a))

    return DistanceScore(distance, max_length)


def find_first_match(search_char, starting_position, char_list):
    # find the first matching character, else return None if no match is found
    try:
        return char_list.index(search_char, starting_position)
    except ValueError:
        return None


def find_first_matching_pair(starting_position, list_a, list_b):
    for i in range(starting_position, len(list_a)):
        for j in range(i, len(list_b)):
            if list_a[i] == list_b[j]:
                return i

    return None


def generic_score(tokenized_a, tokenized_b, edit_distance_function):
    """ Given two tokenized set of elements, try to match up the tokens by the best edit distance (in order). The total
    of those distances are then used in conjunction with edit distance of the two lists to calculate a total score. The
    use of both scores is an attempt to minimize smaller differences such a punctuation etc.
    """
    tokens_a, tokens_b = _shortest_first(tokenized_a, tokenized_b)

    token_to_scores_dict = _find_best_score(edit_distance_function, tokens_a, tokens_b)

    total_score, total_max_score = _calculate_total_scores(token_to_scores_dict)

    for k, v in token_to_scores_dict.items():
        token_b_index = v[1]
        token_a_index = v[0]
        if v[2].edit_distance != v[2].max_score:
            # if the match is less then max (meaning no match): swap in the token, this will
            # get around small changes with words or punctuation
            tokens_b[token_b_index] = tokens_a[token_a_index]

    sentence_edit_score = edit_distance_score(tokens_a, tokens_b)
    total_score = total_score + sentence_edit_score.edit_distance
    total_max_score = total_max_score + sentence_edit_score.max_score

    return DistanceScore(total_score, total_max_score)


def sentence_score(sentence_a, sentence_b):
    return generic_score(
        tokenize_words(sentence_a),
        tokenize_words(sentence_b),
        lambda a, b: edit_distance_score(a, b)
    )


def text_score(text_a, text_b):
    return generic_score(
        [inspect.cleandoc(y) for y in tokenize_sentence(text_a) if len(y) > 0],
        [inspect.cleandoc(x) for x in tokenize_sentence(text_b) if len(x) > 0],
        lambda a, b: sentence_score(a, b)
    )


def _find_best_score(edit_distance_function, list_a, list_b):
    word_to_scores_dict = {}

    for i, word_a in enumerate(list_a):
        scores = []
        for j, word_b in enumerate(list_b):
            if j >= i:
                scores.append((i, j, edit_distance_function(word_a, word_b)))
        best_score = sorted(scores, key=lambda x: x[2].edit_distance).pop(0)
        word_to_scores_dict.update({i: best_score})

    return word_to_scores_dict


def _shortest_first(list_a, list_b):
    length_a = len(list_a)
    length_b = len(list_b)

    if length_b < length_a:
        return list_b, list_a
    else:
        return list_a, list_b


def _calculate_total_scores(element_to_scores_dict):
    total_max_score = 0
    total_score = 0
    for k, v in element_to_scores_dict.items():
        total_score = total_score + v[2].edit_distance
        total_max_score = total_max_score + v[2].max_score

    return total_score, total_max_score