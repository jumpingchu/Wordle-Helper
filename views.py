from django.shortcuts import render

def wordle_helper(request):
    import nltk
    import random
    from nltk.corpus import words
    nltk.download('words')

    def get_char_info(char_match: list):
      exclude_char = []
      correct_char = []
      having_char = []
      for c, mark in char_match:
        if mark.lower() == 'x':
          exclude_char.append(c)
        elif mark.lower() == 'o':
          correct_char.append((c, tried.index(c)))
        else:
          having_char.append((c, tried.index(c)))
      return exclude_char, correct_char, having_char

    def get_correct_words(word_list, correct_char):
      if len(correct_char) > 0:
        candidate_words = []
        for w in word_list:
            try:
              if all([w.index(c) == idx for c, idx in correct_char]):
                candidate_words.append(w)
            except:
              continue
        return list(set(candidate_words))
      else:
        return word_list

    def get_excluded_words(word_list: list, exclude_char: list):
      if len(exclude_char) > 0:
        removing = []
        for w in word_list:
            for c in exclude_char:
              if c in w:
                removing.append(w)
        return list(set(removing))
      else:
        return []

    def get_having_words(word_list: list, having_char: list):
      if len(having_char) > 0:
        candidate_words = []
        for w in word_list:
          if all([c in w for c, idx in having_char]) and all([w.index(c) != idx for c, idx in having_char]):
                candidate_words.append(w)
        return list(set(candidate_words))
      else:
        return word_list

    def get_current_correct_word(correct_char):
      word = ['_'] * 5
      for char, idx in correct_char:
        word[idx] = char
      return ''.join(word)

    word = words.words()
    word_list = []
    for i in word:
      if len(i) == 5:
        word_list.append(i.lower())

    word_list = list(set(word_list))

    if request.method == 'POST':
        tried_list = request.POST.get('guess_word').lower()
        result_list = request.POST.get('guess_result').lower()

        if all([result != 'ooooo' for result in result_list.split(',')]):
            for tried, result in zip(tried_list.split(','), result_list.split(',')):
                char_match = list(zip(list(tried), list(result)))
                exclude_char, correct_char, having_char = get_char_info(char_match)

                removing = get_excluded_words(word_list, exclude_char)
                for rm in removing:
                  word_list.remove(rm)
                corrects_list = get_correct_words(word_list, correct_char)
                candidate_words = get_having_words(corrects_list, having_char)
                word_list = candidate_words

            if len(candidate_words) > 100:
                w_list = sorted(list(random.sample(sorted(candidate_words), int(len(candidate_words)/3))))
                return render(
                    request,
                    'wordle-helper.html',
                    {
                        'word': w_list,
                        'guess_word': tried_list,
                        'guess_result': result_list,
                        'correct_word': get_current_correct_word(correct_char)
                    }
                )
            else:
                return render(
                    request,
                    'wordle-helper.html',
                    {
                        'word': sorted(candidate_words),
                        'guess_word': tried_list,
                        'guess_result': result_list,
                        'correct_word': get_current_correct_word(correct_char)
                    }
                )

        else:
            if all([len(result_list) > 1, len(tried_list) > 1]):
                correct_idx = result_list.index('ooooo')
                correct_word = tried_list.split(' ')[correct_idx]
            else:
                correct_word = tried_list

            return render(
                request,
                'wordle-helper.html',
                {'word': [f'恭喜～今天正解是 {correct_word}']}
            )

    else:
        return render(request, 'wordle-helper.html')
