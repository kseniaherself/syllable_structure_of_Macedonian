# macedonian_dict.tsv
#12
# то что WOS то без учёта слоговости
# иниц без сл: 6, со: 4; фин без сл: 5, с: 3
# Plosive, Fricative, Affricate, [Lateral, Nasal, Trill, Glide] > Sonorants 
# [Bilabial, Labio-Dental], [Dental, Alveolar, Alveo-Palatal], [Palatal, Velar]
# syllabic: SYS
import re
import operator
import time
start_time = time.time()

# чтение строк из файла, возвращает строки
def F_get_lines(f_name):
    f = open(f_name, 'r')
    my_lines = f.readlines()
    #print(my_lines)
    f.close()
    return my_lines

# запись в файл
def F_write_in_file(data , f_name):
    f = open(f_name, 'w')
    f.write(data)
    #print(data)
    f.close()

# стандартизация грамматического комментария: получает на М, возвращает станд.вариант
def F_standardization_grammar(grammar_inf):
    st_grammar_inf = grammar_inf

    a1 = st_grammar_inf.replace('Вид збор: ', '')

    a1 = a1.replace('Заменка', 'pronoun')
    a1 = a1.replace('Именка,', 'noun')
    a1 = a1.replace('женски род', 'fem')
    a1 = a1.replace('машки род', 'masc')
    a1 = a1.replace('среден род', 'neut')
    a1 = a1.replace('множина', 'pluralia_tantum')
    a1 = a1.replace('Име', 'proper_noun')

    a1 = a1.replace('Префикс', 'affixoid_pref')     #часть сложного слова
    a1 = a1.replace('Суфикс', 'affixoid_suf')       #часть сложного слова
    a1 = a1.replace('Скратеница', 'abbr')           #abbreviation & reduction
    a1 = a1.replace('Сложенка', 'compound')          #compound, complex noun

    a1 = a1.replace('Глагол,', 'verb')
    a1 = a1.replace('свршен и несвршен', 'bi-aspectual')
    a1 = a1.replace('несвршен', 'impfv')
    a1 = a1.replace('свршен', 'pfv')

    a1 = a1.replace('Број', 'num')
    a1 = a1.replace('Придавка', 'adj')
    a1 = a1.replace('Прилог', 'adv')
    a1 = a1.replace('Модален збор', 'modal word')

    a1 = a1.replace('Извик', 'interjection')
    a1 = a1.replace('Предлог', 'prep')
    a1 = a1.replace('Сврзник', 'conjunction')   #cnj
    a1 = a1.replace('Честичка', 'particle')

    return a1

# разбиение на символы: на входе слово, на выходе оно в разделённом виде
def F_lettering(word):
    lettering = ''

    for element in word:
        lettering = lettering + '-' + element
    lettering = lettering.replace('-', '', 1)

    return lettering

# транскриптор: на выходе слово в МФА +слоговые сонорные
def F_ipa_transcriber(word):

    cyrillic_s = ['а', 'б', 'в', 'г', 'д', 'ѓ', 'е', 'ж', 'з', 'ѕ', 'и', 'ј', 'к', 'л', 'љ', 'м', 'н', 'њ',
                  'о', 'п', 'р', 'с', 'т', 'ќ', 'у', 'ф', 'х', 'ц', 'ч', 'џ', 'ш', 'ѐ', 'ѝ']

    ipa_s = ['a', 'b', 'v', 'ɡ', 'd', 'ɟ', 'e', 'ʒ', 'z', 'dz', 'i', 'j', 'k', 'l', 'lj', 'm', 'n', 'nj',
             'o', 'p', 'r', 's', 't', 'c', 'u', 'f', 'x', 'ts', 'tʃ', 'dʒ','ʃ', 'è', 'ì']

    for element in word:
        for i in range(0, 33):
            if cyrillic_s[i] == element:
                word = word.replace(cyrillic_s[i], ipa_s[i])

# добавление слоговых сонорных: r, l, m, n
    ipa_consonants = ['b', 'v', 'ɡ', 'd', 'ɟ', 'ʒ', 'z', 'dz', 'k', 'l', 'lj', 'm', 'n', 'nj',
                      'p', 'r', 's', 't', 'c', 'f', 'x', 'ts', 'tʃ', 'dʒ', 'ʃ'] # add ['R'], минус ['j',]

    for j in range(0, 25):
        environment_in_left = '^r-' + str(ipa_consonants[j])
        environment_out_left = 'R-' + str(ipa_consonants[j])
        word = re.sub(environment_in_left, environment_out_left, word)

        environment_in_right_r = str(ipa_consonants[j]) + '-r$'
        environment_out_right_r = str(ipa_consonants[j]) + '-R'
        word = re.sub(environment_in_right_r, environment_out_right_r, word)

        for k in range (0, 25):
            environment_in = str(ipa_consonants[j]) + '-r-' + str(ipa_consonants[k])
            environment_out = str(ipa_consonants[j]) + '-R-' + str(ipa_consonants[k])
            word = word.replace(environment_in, environment_out)

    for l in range(0, 25):
        environment_in_right_l = str(ipa_consonants[l]) + '-l$'
        environment_out_right_l = str(ipa_consonants[l]) + '-L'
        word = re.sub(environment_in_right_l, environment_out_right_l, word)

        environment_in_right_n = str(ipa_consonants[l]) + '-n$'
        environment_out_right_n = str(ipa_consonants[l]) + '-N'
        word = re.sub(environment_in_right_n, environment_out_right_n, word)

    return word

# транспонировани: способ образования
def F_articulation_manner(word):

    ipa_consonants = ['R', 'r', 'dz', 'ts', 'tʃ', 'dʒ', 'lj', 'l', 'm', 'nj', 'n',
                      'b', 'p', 'd', 't', 'ɟ', 'c', 'ɡ', 'k',
                      'v', 'f', 'z', 's', 'ʒ', 'ʃ', 'x', 'j']  # add ['R'], минус ['j',]

    #ipa_manner = ['stop', 'fricative', 'stop', 'stop', 'stop', 'fricative', 'fricative', 'affricate', 'stop',
    #              'lateral', 'lateral', 'nasal', 'nasal', 'nasal', 'stop', 'trill', 'fricative', 'stop', 'stop',
    #              'fricative', 'fricative', 'affricate', 'affricate', 'affricate', 'fricative']  # add ['R'], минус ['j',]

    ipa_manner = ['T', 'T', 'A', 'A', 'A', 'A', 'L', 'L', 'N', 'N', 'N',
                  'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P',
                  'F', 'F', 'F', 'F', 'F', 'F', 'F', 'G'] #ДОБАВЛЕНО 'R'

    for i in range(0, 27):
        if ipa_consonants[i] in word:
            word = word.replace(ipa_consonants[i], ipa_manner[i])

    return word

# транспонирование: место образования
def F_articulation_place(word):

    ipa_consonants = ['N', 'L', 'R', 'r', 'dz', 'ts', 'dʒ', 'tʃ', 'lj', 'nj', 'b', 'p', 'm', 'v', 'f',
                      'd', 't', 'z', 's', 'l', 'n', 'ʒ', 'ʃ', 'ɟ', 'c', 'j', 'ɡ', 'k', 'x']

    ipa_place = ['D', 'D', 'A', 'A', 'D', 'D', 'AP', 'AP', 'A', 'P', 'BL', 'BL', 'BL', 'LD', 'LD',
                 'D', 'D', 'D', 'D', 'D', 'D', 'AP', 'AP', 'P', 'P', 'P', 'V', 'V', 'V']

    for i in range(0, 29):
        if ipa_consonants[i] in word:
            word = word.replace(ipa_consonants[i], ipa_place[i])

    return word

# транспонировани: способ образования (соединённые категории)
def F_articulation_manner_MERGED(word):

    ipa_consonants = ['N', 'L', 'R', 'r', 'dz', 'ts', 'tʃ', 'dʒ', 'lj', 'l', 'm', 'nj', 'n',
                      'b', 'p', 'd', 't', 'ɟ', 'c', 'ɡ', 'k',
                      'v', 'f', 'z', 's', 'ʒ', 'ʃ', 'x', 'j']  # add ['R'], минус ['j',]

    #ipa_manner = ['stop', 'fricative', 'stop', 'stop', 'stop', 'fricative', 'fricative', 'affricate', 'stop',
    #              'lateral', 'lateral', 'nasal', 'nasal', 'nasal', 'stop', 'trill', 'fricative', 'stop', 'stop',
    #              'fricative', 'fricative', 'affricate', 'affricate', 'affricate', 'fricative']  # add ['R'], минус ['j',]

    ipa_manner = ['S', 'S', 'S', 'S', 'A', 'A', 'A', 'A', 'S', 'S', 'S', 'S', 'S',
                  'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P',
                  'F', 'F', 'F', 'F', 'F', 'F', 'F', 'S'] #ДОБАВЛЕНО 'R'

    for i in range(0, 29):
        if ipa_consonants[i] in word:
            word = word.replace(ipa_consonants[i], ipa_manner[i])

    return word

# транспонирование: место образования (соединённые категории)
def F_articulation_place_MERGED(word):

    ipa_consonants = ['N', 'L', 'R', 'r', 'dz', 'ts', 'dʒ', 'tʃ', 'lj', 'nj', 'b', 'p', 'm', 'v', 'f',
                      'd', 't', 'z', 's', 'l', 'n', 'ʒ', 'ʃ', 'ɟ', 'c', 'j', 'ɡ', 'k', 'x'] # L это A

    ipa_place = ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'D', 'L', 'L', 'L', 'L', 'L',
                 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'D', 'D', 'D', 'D', 'D', 'D'] # Dorsal Anterior Labial

    for i in range(0, 29):
        if ipa_consonants[i] in word:
            word = word.replace(ipa_consonants[i], ipa_place[i])

    return word

# транспонирование: качество звука
def F_articulation_quality(word):

    ipa_consonants = ['N', 'L', 'R', 'r', 'ts', 'dz', 'tʃ', 'dʒ', 'lj', 'nj', 'v',
                      'p', 'b', 't', 'd', 'c', 'ɟ', 'k', 'ɡ', 's', 'z', 'ʃ', 'ʒ', 'f', 'x',
                      'l', 'm', 'n', 'j']

    ipa_quality = ['S', 'S', 'S', 'S', 'O', 'O', 'O', 'O', 'S', 'S', 'O',
                   'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O',
                   'S', 'S', 'S', 'S']

    for i in range(0, 29):
        if ipa_consonants[i] in word:
            word = word.replace(ipa_consonants[i], ipa_quality[i])

    ipa_vow = ['a', 'e', 'i', 'o', 'u', 'è', 'ì']
    for j in range(0, 7):
        if ipa_vow[j] in word:
            word = word.replace(ipa_vow[j], 'V')

    return word

# транспонирование: качество звука ДЛЯ СЛОГОВЫХ
def F_articulation_quality_word(word):

    ipa_consonants = ['r', 'ts', 'dz', 'tʃ', 'dʒ', 'lj', 'nj', 'v',
                      'p', 'b', 't', 'd', 'c', 'ɟ', 'k', 'ɡ', 's', 'z', 'ʃ', 'ʒ', 'f', 'x',
                      'l', 'm', 'n', 'j']

    ipa_quality = ['S', 'O', 'O', 'O', 'O', 'S', 'S', 'O',
                   'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O',
                   'S', 'S', 'S', 'S']

    for i in range(0, 26):
        if ipa_consonants[i] in word:
            word = word.replace(ipa_consonants[i], ipa_quality[i])

    ipa_vow = ['a', 'e', 'i', 'o', 'u', 'è', 'ì', 'N', 'L', 'R']
    for j in range(0, 10):
        if ipa_vow[j] in word:
            word = word.replace(ipa_vow[j], 'V')

    return word

# количество слогов: на выходе количество слогов вообще по гласным и с учётом "слоговых"
# (+печатает слова "без-гласных"). (+печатает слова с двумя шва). (+печатает слова с апострофом). (+печатает слова с Л,Н).
def F_number_syllables_by_vowels_plus_schwa(word, syllabic_head):
    WOS_n_syllables = 0

    for element in word:
        for i in range(0, 6):
            if element == syllabic_head[i]:
                WOS_n_syllables += 1
#['a', 'e', 'i', 'o', 'u', 'è', 'ì', 'L', 'N', 'R']
    n_syllables = WOS_n_syllables
    #print(WOS_n_syllables)
    for letter in word:
        #print(letter, n_syllables)
        if letter == syllabic_head[7]:
            n_syllables = n_syllables + 1

        elif letter == syllabic_head[8]:
            n_syllables = n_syllables + 1

        elif letter == syllabic_head[9]:
            n_syllables = n_syllables + 1

        else:
            n_syllables = n_syllables

    #print(n_syllables)
    total_n = str(WOS_n_syllables) + '\t' + str(n_syllables)
    #print(total_n)

# такое слово вероятней всего сокращение, но необязательно
    #if n_syllables == 0:
        #print(word)

# проверка разности слогов: две швы в одном слове было бы подозрительно, (если это не Р)
    alt_j = n_syllables - WOS_n_syllables
    #print(alt_j)
    if alt_j != 0 and alt_j != 1:
        print ('слова с двумя слоговыми: ', word, total_n)
# может напечатать слова в МФА со слоговыми
    #if alt_j == 1:
    #    print(word, total_n)

# может напечатать слова с apostrophe
    if '’' in word:
        print('слово с этой ’ штукой: ', word)

# может напечатать слова со слоговым Л или Н
    #if '-L' in word:
    #    print('слово со слоговым Л', word)
    #if '-N' in word:
    #    print('слово со слоговым Н', word)

    return total_n

# инициали БЕЗ УЧЁТА СЛОГОВОСТИ Р
def F_words_initials_wos(word):
    initial = 'V'
    res = re.match('([^aeiouèì]+?)(((-)*?[aeiouèì])|$)', word)
    if res:
        initial = res.group(1)
        #print(initial)

    #print(initial)
    return initial

# инициали С УЧЁТОМ СЛОГОВОГО Р
def F_words_initials(word):
    initial = 'V'
    res = re.match('([^aeiouèìLNR]+?)(-)*?[aeiouèìLNR]', word) #('([^aeiouèìə]+?(R)*?)(-)*?[aeiouèìə]', word)
    if res:
        initial = res.group(1)

    res_syl = re.match('^[RLM]', word)
    if res_syl:
        initial = 'SYL'

    #print(initial)
    return initial

# финали БЕЗ УЧЁТА СЛОГОВЫХ СОНОРНЫХ
def F_words_finals_wos(word):
    final = 'V'
    res = re.findall('[aeiouèì]*?([^aeiouèì]+?$)', word) #'^|[aeiouèì]*?(-)*?([^aeiouèì]+?$)'
    #print(res)
    if res != []:         #[('', '')]: #['']:
        #print(res[0])
        final = str(res[0])    #[1]#[1] #.group(2)
        #final = final.replace('-', '', 1)
        res1 = re.findall('^(-).', final)
        if res1:
            # print(res1[0])
            final = final.replace('-', '', 1)

    #print(final)
    return final

# финали С УЧЁТОМ СЛОГОВЫХ СОНОРНЫХ
def F_words_finals(word):
    final = 'V'

    res = re.findall('-*?([^aeiouèìLNR]+?|([^aeiouèì([LNR])]+?)$', word) #('-*?([^aeiouèì(.ə)]+?|([Rln]ə[^aeiouèì(.ə)]+?)|[Rln]ə)$', word)    #('^|[aeiouèì]|[Rlmnə]-*?([^aeiouèì]+?$)', word)
    #print(res)

    if res != []:
        #print(res)
        #final = str(res)#[1]
        final = res[0][0]
        res1 = re.findall('^(-).', final)
        if res1:
            #print(res1[0])
            final = final.replace('-', '', 1)

    res_syl1 = re.findall('[LNR]$', word)
    # print(word)

    if res_syl1 != []:
        final = 'SYL'
        #print(final)

    #print(final)
    return final

# сегменты кластеров
def F_items_segments(words_items, sta, sto, ste):
    items_segments = ''

    words_segments = words_items.split('-')

    delta = sto + len(words_segments)*ste
    if ste == 1:
        words_segments = words_segments + delta*['']
    else:
        words_segments = delta*[''] + words_segments

    for i in range(sta, sto):

        if words_segments[i] != '':
            #print(words_segments[i])
            items_segments = items_segments + words_segments[i] + '\t'

        else:
            items_segments = items_segments + '\t'

    #print(items_segments)
    return items_segments

# monosyllabic
def F_get_monosyllabic(word, number_syllables):

    n_s_split = number_syllables.split('\t')

    WOS_no_syllables = ''
    no_syllables = ''
    WOS_monosyllabic_word = ''
    monosyllabic_word = ''

    if n_s_split[0] == '0':
        WOS_no_syllables = word

    if n_s_split[1] == '0':
        no_syllables = word

    if n_s_split[0] == '1':
        WOS_monosyllabic_word = word

    if n_s_split[1] == '1':
        monosyllabic_word = word

    n_syl = [WOS_no_syllables, no_syllables, WOS_monosyllabic_word, monosyllabic_word] #.append(WOS_no_syllables, no_syllables, WOS_monosyllabic_word, monosyllabic_word)

    return n_syl

# сортировка
def F_sort_dictionary(list_to_sort):
    sorted_c = str(sorted(list_to_sort))
    sorted_c = sorted_c.replace("'", "")
    sorted_c = sorted_c.replace("[", "")
    sorted_c = sorted_c.replace("]", "")
    sorted_c = sorted_c.split(',')

    #print(sorted_c)
    return sorted_c

# запись в словарь
def F_w_d(my_dict, my_key):
    if my_key not in my_dict:
        my_dict[my_key] = 1
    else:
        my_dict[my_key] += 1

    return my_dict

# записывает файлы про инициали и финали
def F_w_f_b(items_name, possible_items, f_name):

    possible_W = items_name
    possible_items = F_sort_dictionary(possible_items)
    for element in possible_items:
        possible_W = possible_W + '\n' + element
    F_write_in_file(possible_W, f_name)

# записывает файл с отсортированными по частотностями штуками
def F_sort_wd_items(my_items, items_name):
    sorted_items = sorted(my_items.items(), key=operator.itemgetter(1), reverse=True)
    items_freq = items_name + '\t' + 'frequency'
    for k in sorted_items:
        items_freq = items_freq + '\n' + k[0] + '\t' + str(k[1])
    f_name = items_name + '_frequency' + '.txt'
    F_write_in_file(items_freq, f_name)

# таблица с:
#   грамматической информацией
#   словами
#   разбиение по буквам
#   разбиение по буквам в МФА
#   количествами слогов
#   инициалями
#   финалями
def M_create_table_1():

    st = '\t'
    sn = '\n'

    all_cyr_words = 'word'
    f_name_full_list = 'words_full_list.tsv'

    items_i = 'INITIALS'
    items_f = 'FINALS'
    ext = '.txt' # разрешение файлов
    f_name = 'macedonian_dict1.tsv'

    syllabic_heads = ['a', 'e', 'i', 'o', 'u', 'è', 'ì', 'L', 'N', 'R'] #'ə']

    WOS_nosyllabic_words = 'WOS_nonsyllabic'
    nosyllabic_words = 'nonsyllabic'
    WOS_monosyllabic_words = 'WOS_monosyllabic'
    monosyllabic_words = 'monosyllabic'

    WOS_t_monosyllabic_words = 'WOS_monosyllabic' + st + 'sounds_quality'
    t_monosyllabic_words = 'monosyllabic' + st + 'sounds_quality'

    WOS_t_monosyllabic_words_m = 'WOS_monosyllabic' + st + 'sounds_manner'
    t_monosyllabic_words_m = 'monosyllabic' + st + 'sounds_manner'

    WOS_t_monosyllabic_words_p = 'WOS_monosyllabic' + st + 'sounds_place'
    t_monosyllabic_words_p = 'monosyllabic' + st + 'sounds_place'

    WOS_initials = {}
    initials = {}
    WOS_initials_m = {}
    initials_m = {}
    WOS_initials_p = {}
    initials_p = {}
    WOS_initials_q = {}
    initials_q = {}

    WOS_monosyllabic_initials_q = {}
    monosyllabic_initials_q = {}
    WOS_monosyllabic_initials_m = {}
    monosyllabic_initials_m = {}
    WOS_monosyllabic_initials_p = {}
    monosyllabic_initials_p = {}

    WOS_possible_initials = []
    possible_initials = []          # 'INITIALS'
    WOS_possible_initials_M = []
    possible_initials_M = []
    WOS_possible_initials_P = []
    possible_initials_P = []
    WOS_possible_initials_Q = []
    possible_initials_Q = []

    WOS_finals = {}
    finals = {}
    WOS_finals_m = {}
    finals_m = {}
    WOS_finals_p = {}
    finals_p = {}
    WOS_finals_q = {}
    finals_q = {}

    WOS_monosyllabic_finals_q = {}
    monosyllabic_finals_q = {}
    WOS_monosyllabic_finals_m = {}
    monosyllabic_finals_m = {}
    WOS_monosyllabic_finals_p = {}
    monosyllabic_finals_p = {}

    WOS_possible_finals = []
    possible_finals = []            # 'FINALS'
    WOS_possible_finals_M = []
    possible_finals_M = []
    WOS_possible_finals_P = []
    possible_finals_P = []
    WOS_possible_finals_Q = []
    possible_finals_Q = []

    all_words = ''

    my_lines = F_get_lines(f_name)
    #asd = my_lines[1:54498]        # все слова: без первой строчки с названиями
    asd = my_lines[1:]             # РАБОЧАЯ ВЕРСИЯ ДЛЯ ВСЕХ СЛОВ
    #asd = my_lines[1:1330]       # тестовая выборка

    for line in asd:
        #print(line)
        line_split = line.split(st)
        dict_entry = line_split[11] # для данного слова есть его словарное вхождение
        entry = dict_entry.strip()
        #print(dict_entry, end="")

# замена тире на нижнее подчёркивание
        for element in entry:
            if element == '-':
                entry = entry.replace('-', '_')
                #print(entry)

        grammar_info = line_split[2] # для данного слова есть его грамматическая инфорация
        grammar_info = F_standardization_grammar(grammar_info)
        #print(grammar_inf)
# получена грамматическая информация
        full_data = grammar_info + st + entry # грам информация и слово через \t
        #print('full_dat: ', full_data)


        if '’' not in full_data and '_' not in full_data and 'abbr'not in full_data \
                and 'compound' not in full_data and 'interjection' not in full_data:

            entry = entry.replace('!', '')              # зачем это?...

            #print(entry)
            all_cyr_words = all_cyr_words + sn + entry
            #print(all_cyr_words)

            lettering = F_lettering(entry)
            #print(lettering)
# получена запись слова буква за буквой
            full_data = full_data + st + lettering
            #print(full_data)

            lower_lettering = str.lower(lettering)   # на случай имён
            ipa_word = F_ipa_transcriber(lower_lettering)
            #print(ipa_word)
# получено разделённое слово в МФА
            full_data = full_data + st + ipa_word
            #print(full_data)

            quality_word = F_articulation_quality_word(ipa_word)
            full_data = full_data + st + quality_word

            number_syllables = F_number_syllables_by_vowels_plus_schwa(ipa_word, syllabic_heads)
# получено количество слогов по гласным + '\t' слоговым
            full_data = full_data + st + str(number_syllables)
            #print(full_data)

            WOS_words_initial = F_words_initials_wos(ipa_word)
# получены инициали слов МФА !!! без расчёта слоговых
            WOS_initials_m = F_w_d(WOS_initials_m, F_articulation_manner_MERGED(WOS_words_initial))
            WOS_initials_p = F_w_d(WOS_initials_p, F_articulation_place_MERGED(WOS_words_initial))
            WOS_initials_q = F_w_d(WOS_initials_q, F_articulation_quality(WOS_words_initial))
            WOS_initials = F_w_d(WOS_initials, WOS_words_initial)

            words_initial = F_words_initials(ipa_word)
# получены инициали слов МФА
            initials_m = F_w_d(initials_m, F_articulation_manner_MERGED(words_initial))
            initials_p = F_w_d(initials_p, F_articulation_place_MERGED(words_initial))
            initials_q = F_w_d(initials_q, F_articulation_quality(words_initial))
            initials = F_w_d(initials, words_initial)

            WOS_words_final = F_words_finals_wos(ipa_word)
# получены финали слов МФА !!! без расчёта слоговых
            WOS_finals_m = F_w_d(WOS_finals_m, F_articulation_manner_MERGED(WOS_words_final))
            WOS_finals_p = F_w_d(WOS_finals_p, F_articulation_place_MERGED(WOS_words_final))
            WOS_finals_q = F_w_d(WOS_finals_q, F_articulation_quality(WOS_words_final))
            WOS_finals = F_w_d(WOS_finals, WOS_words_final)

            words_final = F_words_finals(ipa_word)
# получены финали слов МФА
            finals_m = F_w_d(finals_m, F_articulation_manner_MERGED(words_final))
            finals_p = F_w_d(finals_p, F_articulation_place_MERGED(words_final))
            finals_q = F_w_d(finals_q, F_articulation_quality(words_final))
            finals = F_w_d(finals, words_final)

            words_items = WOS_words_initial + st + words_initial + st + WOS_words_final + st + words_final
            full_data = full_data + st + words_items

# тут нужно разбить на сегменты
            WOS_initials_segments = F_items_segments(WOS_words_initial, 0, 6, -1)
            initials_segments = F_items_segments(words_initial, 0, 4, -1)

            WOS_finals_segments = F_items_segments(WOS_words_final, 0, 5, 1)
            finals_segments = F_items_segments(words_final, 0, 3, 1)
# финали и инициали разбиты на сегменты

            segments = WOS_initials_segments + initials_segments + WOS_finals_segments + finals_segments
            full_data = full_data + st + segments

            words_items_manner = F_articulation_manner_MERGED(words_items)
            words_items_place = F_articulation_place_MERGED(words_items)
            words_items_quality = F_articulation_quality(words_items)
# кластеры инициалей и финалей переведены по способу образования
            #full_data = full_data + words_items_manner #+ words_items_place

            segments_manner = F_articulation_manner_MERGED(segments)
            segments_place = F_articulation_place_MERGED(segments)
            segments_quality = F_articulation_quality(segments)
# сегменты инициалей и финалей переведены по способу образования
            full_data = full_data + words_items_manner + st + segments_manner

            full_data = full_data + words_items_place + st + segments_place
            full_data = full_data + words_items_quality + st + segments_quality

# слова без слогов, с одним слогом
            n_syllabic_words = F_get_monosyllabic(entry, number_syllables)

            if n_syllabic_words[0] == entry:
                WOS_nosyllabic_words = WOS_nosyllabic_words + sn + n_syllabic_words[0]

            if n_syllabic_words[1] == entry:
                nosyllabic_words = nosyllabic_words + sn + n_syllabic_words[1]

# односложные без слоговых
            if n_syllabic_words[2] == entry:
                WOS_monosyllabic_words = WOS_monosyllabic_words + sn + n_syllabic_words[2]

# quality
                WOS_segments_q = F_articulation_quality(WOS_initials_segments) + '<NUCL>' + st + F_articulation_quality(WOS_finals_segments)
                WOS_segments_q = re.sub('\\tV', '\t', WOS_segments_q)
                WOS_segments_q = re.sub('\\t$', '', WOS_segments_q)

                #WOS_segments_q = F_articulation_quality(WOS_segments_q)
                WOS_t_monosyllabic_words = WOS_t_monosyllabic_words + sn + n_syllabic_words[2] + st + WOS_segments_q

                WOS_monosyllabic_initials_q = F_w_d(WOS_monosyllabic_initials_q, F_articulation_quality(WOS_words_initial))
                WOS_monosyllabic_finals_q = F_w_d(WOS_monosyllabic_finals_q, F_articulation_quality(WOS_words_final))

# manner
                WOS_segments_m = F_articulation_manner_MERGED(WOS_initials_segments) + '<NUCL>' + st + F_articulation_manner_MERGED(WOS_finals_segments)
                WOS_segments_m = re.sub('\\tV', '\t', WOS_segments_m)
                WOS_segments_m = re.sub('\\t$', '', WOS_segments_m)

                WOS_t_monosyllabic_words_m = WOS_t_monosyllabic_words_m + sn + n_syllabic_words[2] + st + WOS_segments_m

                WOS_monosyllabic_initials_m = F_w_d(WOS_monosyllabic_initials_m, F_articulation_manner_MERGED(WOS_words_initial))
                WOS_monosyllabic_finals_m = F_w_d(WOS_monosyllabic_finals_m, F_articulation_manner_MERGED(WOS_words_final))

# place
                WOS_segments_p = F_articulation_place_MERGED(WOS_initials_segments) + '<NUCL>' + st + F_articulation_place_MERGED(WOS_finals_segments)
                WOS_segments_p = re.sub('\\tV', '\t', WOS_segments_p)
                WOS_segments_p = re.sub('\\t$', '', WOS_segments_p)

                WOS_t_monosyllabic_words_p = WOS_t_monosyllabic_words_p + sn + n_syllabic_words[2] + st + WOS_segments_p

                WOS_monosyllabic_initials_p = F_w_d(WOS_monosyllabic_initials_p, F_articulation_place_MERGED(WOS_words_initial))
                WOS_monosyllabic_finals_p = F_w_d(WOS_monosyllabic_finals_p, F_articulation_place_MERGED(WOS_words_final))

# односложные со слоговыми
            if n_syllabic_words[3] == entry:
                monosyllabic_words = monosyllabic_words + sn + n_syllabic_words[3]

# quality
                segments_q = F_articulation_quality(initials_segments) + '<NUCL>' + st + F_articulation_quality(finals_segments)
                segments_q = re.sub('V\\t', '\t', segments_q)
                segments_q = re.sub('\\t$', '', segments_q)

                #segments_q = F_articulation_quality(segments_q)
                t_monosyllabic_words = t_monosyllabic_words + sn + n_syllabic_words[3] + st + segments_q

                monosyllabic_initials_q = F_w_d(monosyllabic_initials_q, F_articulation_quality(words_initial))
                monosyllabic_finals_q = F_w_d(monosyllabic_finals_q, F_articulation_quality(words_final))

# manner
                segments_m = F_articulation_manner_MERGED(initials_segments) + '<NUCL>' + st + F_articulation_manner_MERGED(finals_segments)
                segments_m = re.sub('V\\t', '\t', segments_m)
                segments_m = re.sub('\\t$', '', segments_m)

                t_monosyllabic_words_m = t_monosyllabic_words_m + sn + n_syllabic_words[3] + st + segments_m

                monosyllabic_initials_m = F_w_d(monosyllabic_initials_m, F_articulation_manner_MERGED(words_initial))
                monosyllabic_finals_m = F_w_d(monosyllabic_finals_m, F_articulation_manner_MERGED(words_final))

# place
                segments_p = F_articulation_place_MERGED(initials_segments) + '<NUCL>' + st + F_articulation_place_MERGED(finals_segments)
                segments_p = re.sub('V\\t', '\t', segments_p)
                segments_p = re.sub('\\t$', '', segments_p)

                t_monosyllabic_words_p = t_monosyllabic_words_p + sn + n_syllabic_words[3] + st + segments_p

                monosyllabic_initials_p = F_w_d(monosyllabic_initials_p, F_articulation_place_MERGED(words_initial))
                monosyllabic_finals_p = F_w_d(monosyllabic_finals_p, F_articulation_place_MERGED(words_final))


# собираются массивы с инициалями и финалями разных сортов
            if WOS_words_initial not in WOS_possible_initials:
                WOS_possible_initials.append(WOS_words_initial)     # инициали без учёта слоговых: WOS_possible_initials
            if words_initial not in possible_initials:
                possible_initials.append(words_initial)                # инициали со слоговыми: possible_initials
                #possible_initials = possible_initials + sn + words_initial

            if WOS_words_final not in WOS_possible_finals:
                WOS_possible_finals.append(WOS_words_final)         # финали без учёта слоговых: WOS_possible_finals
            if words_final not in possible_finals:
                possible_finals.append(words_final)                    # финали со слоговыми: possible_finals
                #possible_finals = possible_finals + sn + words_final

# способ образования
# создаёт массив инициалей способа образования без учёта слоговости
            WOS_words_initial_M = F_articulation_manner_MERGED(WOS_words_initial)
            if WOS_words_initial_M not in WOS_possible_initials_M:
                WOS_possible_initials_M.append(WOS_words_initial_M)

# создаёт массив инициалей способа образования
            words_initial_M = F_articulation_manner_MERGED(words_initial)
            if words_initial_M not in possible_initials_M:
                possible_initials_M.append(words_initial_M)

# создаёт массив финалей способа образования без учёта слоговости
            WOS_words_final_M = F_articulation_manner_MERGED(WOS_words_final)
            if WOS_words_final_M not in WOS_possible_finals_M:
                WOS_possible_finals_M.append(WOS_words_final_M)

# создаёт массив финалей способа образования
            words_final_M = F_articulation_manner_MERGED(words_final)
            if words_final_M not in possible_finals_M:
                possible_finals_M.append(words_final_M)

# место образования
# создаёт массив инициалей места образования без учёта слоговости
            WOS_words_initial_P = F_articulation_place_MERGED(WOS_words_initial)
            if WOS_words_initial_P not in WOS_possible_initials_P:
                WOS_possible_initials_P.append(WOS_words_initial_P)

# создаёт массив инициалей места образования
            words_initial_P = F_articulation_place_MERGED(words_initial)
            if words_initial_P not in possible_initials_P:
                possible_initials_P.append(words_initial_P)

# создаёт массив финалей места образования без учёта слоговости
            WOS_words_final_P = F_articulation_place_MERGED(WOS_words_final)
            if WOS_words_final_P not in WOS_possible_finals_P:
                WOS_possible_finals_P.append(WOS_words_final_P)

# создаёт массив финалей места образования
            words_final_P = F_articulation_place_MERGED(words_final)
            if words_final_P not in possible_finals_P:
                possible_finals_P.append(words_final_P)

# качество звуков
# создаёт массив инициалей качества без учёта слоговости
            WOS_words_initial_Q = F_articulation_quality(WOS_words_initial)
            if WOS_words_initial_Q not in WOS_possible_initials_Q:
                WOS_possible_initials_Q.append(WOS_words_initial_Q)

# создаёт массив инициалей качества
            words_initial_Q = F_articulation_quality(words_initial)
            if words_initial_Q not in possible_initials_Q:
                possible_initials_Q.append(words_initial_Q)

# создаёт массив финалей качества без учёта слоговости
            WOS_words_final_Q = F_articulation_quality(WOS_words_final)
            if WOS_words_final_Q not in WOS_possible_finals_Q:
                #print(WOS_words_final_Q)
                WOS_possible_finals_Q.append(WOS_words_final_Q)

# создаёт массив финалей качества
            words_final_Q = F_articulation_quality(words_final)
            if words_final_Q not in possible_finals_Q:
                possible_finals_Q.append(words_final_Q)

            #print(full_data)

            all_words = all_words + sn + full_data

    #print(all_words)

# запись односложных и бессложных слов
    #F_write_in_file(WOS_nosyllabic_words, 'WOS_nosyllabic_words.tsv')
    #F_write_in_file(nosyllabic_words, 'nosyllabic_words.tsv')
    #F_write_in_file(WOS_monosyllabic_words, 'WOS_monosyllabic_words.tsv')
    #F_write_in_file(monosyllabic_words, 'monosyllabic_words.tsv')

# запись односложных таблиц
    #F_write_in_file(WOS_t_monosyllabic_words, 'WOS_table_monosyllabic_words.tsv')
    #F_write_in_file(t_monosyllabic_words, 'table_monosyllabic_words.tsv')

# запись в файл инициалей и финалей и всего такого
    #F_w_f_b(items_i, WOS_possible_initials, ('WOS_' + items_i + ext))
    #F_w_f_b(items_i, possible_initials, (items_i + ext))
    #F_w_f_b(items_i, WOS_possible_initials_M, 'WOS_' + 'manner_' + items_i + ext)
    #F_w_f_b(items_i, possible_initials_M, ('manner_' + items_i + ext))
    #F_w_f_b(items_i, WOS_possible_initials_P, ('WOS_' + 'place_' + items_i + ext))
    #F_w_f_b(items_i, possible_initials_P, ('place_' + items_i + ext))
    #F_w_f_b(items_i, WOS_possible_initials_Q, ('WOS_' + 'quality_' + items_i + ext))
    #F_w_f_b(items_i, possible_initials_Q, ('quality_' + items_i + ext))

    #F_w_f_b(items_f, WOS_possible_finals, ('WOS_' + items_f + ext))
    #F_w_f_b(items_f, possible_finals, (items_f + ext))
    #F_w_f_b(items_f, WOS_possible_finals_M, ('WOS_' + 'manner_' + items_f + ext))
    #F_w_f_b(items_f, possible_finals_M, ('manner_' + items_f + ext))
    #F_w_f_b(items_f, WOS_possible_finals_P, ('WOS_' + 'place_' + items_f + ext))
    #F_w_f_b(items_f, possible_finals_P, ('place_' + items_f + ext))
    #F_w_f_b(items_f, WOS_possible_finals_Q, ('WOS_' + 'quality_' + items_f + ext))
    #F_w_f_b(items_f, possible_finals_Q, ('quality_' + items_f + ext))

# названия столбцов таблицы
    first_line = 'grammar' + st + 'lemma' + st + 'lettering' + st + 'ipa_lettering' + st + 'quality_lettering' + st + 'n_syllables_wos' \
                 + st + 'n_syllables' + st + 'initials_wos' + st + 'initials' + st + 'finals_wos' + st + 'finals' \
                 + st + 'initial_wos_6' + st + 'initial_wos_5' + st + 'initial_wos_4' + st + 'initial_wos_3' \
                 + st + 'initial_wos_2' + st + 'initial_wos_1' \
                 + st + 'initial_4' + st + 'initial_3' + st + 'initial_2' + st + 'initial_1' \
                 + st + 'final_wos_1' + st + 'final_wos_2' + st + 'final_wos_3' + st + 'final_wos_4'+ st + 'final_wos_5' \
                 + st + 'final_1' + st + 'final_2' + st + 'final_3' \
                 + st + 'initials_wos_manner' + st + 'initials_manner' + st + 'finals_wos_manner' + st + 'finals_manner' \
                 + st + 'initial_wos_6_manner' + st + 'initial_wos_5_manner' + st + 'initial_wos_4_manner' \
                 + st + 'initial_wos_3_manner' + st + 'initial_wos_2_manner' + st + 'initial_wos_1_manner' \
                 + st + 'initial_4_manner' + st + 'initial_3_manner' + st + 'initial_2_manner' + st + 'initial_1_manner' \
                 + st + 'final_wos_1_manner' + st + 'final_wos_2_manner' + st + 'final_wos_3_manner' \
                 + st + 'final_wos_4_manner'+ st + 'final_wos_5_manner' \
                 + st + 'final_1_manner' + st + 'final_2_manner' + st + 'final_3_manner' \
                 + st + 'initials_wos_place' + st + 'initials_place' + st + 'finals_wos_place' + st + 'finals_place' \
                 + st + 'initial_wos_6_place' + st + 'initial_wos_5_place' + st + 'initial_wos_4_place' \
                 + st + 'initial_wos_3_place' + st + 'initial_wos_2_place' + st + 'initial_wos_1_place' \
                 + st + 'initial_4_place' + st + 'initial_3_place' + st + 'initial_2_place' + st + 'initial_1_place' \
                 + st + 'final_wos_1_place' + st + 'final_wos_2_place' + st + 'final_wos_3_place' \
                 + st + 'final_wos_4_place' + st + 'final_wos_5_place' \
                 + st + 'final_1_place' + st + 'final_2_place' + st + 'final_3_place' \
                 + st + 'initials_wos_quality' + st + 'initials_quality' + st + 'finals_wos_quality' + st + 'finals_quality' \
                 + st + 'initial_wos_6_quality' + st + 'initial_wos_5_quality' + st + 'initial_wos_4_quality' \
                 + st + 'initial_wos_3_quality' + st + 'initial_wos_2_quality' + st + 'initial_wos_1_quality' \
                 + st + 'initial_4_quality' + st + 'initial_3_quality' + st + 'initial_2_quality' + st + 'initial_1_quality' \
                 + st + 'final_wos_1_quality' + st + 'final_wos_2_quality' + st + 'final_wos_3_quality' \
                 + st + 'final_wos_4_quality' + st + 'final_wos_5_quality' \
                 + st + 'final_1_quality' + st + 'final_2_quality' + st + 'final_3_quality' \
                 #+ st + '1' + st + '2' + st + '3' + st + '4' + st + '5' + st + '6' + st + '7' + st + '8' + st + '9' + st + '10' + st + '11' + st + '12'


    data = first_line + all_words
    #print(data)
# таблица создана и записана

    #F_sort_wd_items(WOS_initials, ('WOS_' + items_i))
    #F_sort_wd_items(initials, (items_i))
    #F_sort_wd_items(WOS_initials_m, ('WOS_' + 'manner_' + items_i))
    #F_sort_wd_items(initials_m, ('manner_' + items_i))
    #F_sort_wd_items(WOS_initials_p, ('WOS_' + 'place_' + items_i))
    #F_sort_wd_items(initials_p, ('place_' + items_i))
    #F_sort_wd_items(WOS_initials_q, ('WOS_' + 'quality_' + items_i))
    #F_sort_wd_items(initials_q, ('quality_' + items_i))

    #F_sort_wd_items(WOS_monosyllabic_initials_q, ('WOS_' + 'quality' + 'monosyllabic_' + items_i))
    #F_sort_wd_items(monosyllabic_initials_q, ('quality_' + 'monosyllabic_' + items_i))
    #F_sort_wd_items(WOS_monosyllabic_initials_m, ('WOS_' + 'manner_' + 'monosyllabic_' + items_i))
    #F_sort_wd_items(monosyllabic_initials_m, ('manner_' + 'monosyllabic_' + items_i))
    #F_sort_wd_items(WOS_monosyllabic_initials_p, ('WOS_' + 'place_' + 'monosyllabic_' + items_i))
    #F_sort_wd_items(monosyllabic_initials_p, ('place_' + 'monosyllabic_' + items_i))

    #F_sort_wd_items(WOS_finals, ('WOS_' + items_f))
    #F_sort_wd_items(finals, (items_f))
    #F_sort_wd_items(WOS_finals_m, ('WOS_' + 'manner_' + items_f))
    #F_sort_wd_items(finals_m, ('manner_' + items_f))
    #F_sort_wd_items(WOS_finals_p, ('WOS_' + 'place_' + items_f))
    #F_sort_wd_items(finals_p, ('place_' + items_f))
    #F_sort_wd_items(WOS_finals_q, ('WOS_' + 'quality_' + items_f))
    #F_sort_wd_items(finals_q, ('quality_' + items_f))

    #F_sort_wd_items(WOS_monosyllabic_finals_q, ('WOS_' + 'quality' + 'monosyllabic_' + items_f))
    #F_sort_wd_items(monosyllabic_finals_q, ('quality' + 'monosyllabic_' + items_f))
    #F_sort_wd_items(WOS_monosyllabic_finals_m, ('WOS_' + 'manner_' + 'monosyllabic_' + items_f))
    #F_sort_wd_items(monosyllabic_finals_m, ('manner_' + 'monosyllabic_' + items_f))
    #F_sort_wd_items(WOS_monosyllabic_finals_p, ('WOS_' + 'place_' + 'monosyllabic_' + items_f))
    #F_sort_wd_items(monosyllabic_finals_p, ('place_' + 'monosyllabic_' + items_f))

    #F_write_in_file(all_cyr_words, f_name_full_list)

    #print(data)
    F_write_in_file(data, 'phon_table.tsv')

# попытка в интервокальные кластеры
def M_create_table_2():

    intervocal = ''

    my_lines = F_get_lines('words_full_list.tsv')
    #sdf = my_lines[1:]             # РАБОЧАЯ ВЕРСИЯ ДЛЯ ВСЕХ СЛОВ
    sdf = my_lines[145:167]             # ТЕСТОВАЯ ВЫБОРКА

    for line in sdf:
        line = line.strip()
        line = re.sub('\n', '', line)
        line = F_ipa_transcriber(line)

        for i in range(0, 10):
            res1 = re.search('(.)*[^aeiouèìLNR]*(\w)*[^aeiouèìLNR]*(\w)*[^aeiouèìLNR]*(\w)*[^aeiouèìLNR]*(\w)*[^aeiouèìLNR]*(\w)*[^aeiouèìLNR]*(\w)*[^aeiouèìLNR]*(\w)*[^aeiouèìLNR]*(\w)*[^aeiouèìLNR]*(\w)*[^aeiouèìLNR]*(\w)*', line)
            if res1.group(i):
                intervocal = intervocal + '\n' + line + '\t' + (res1.group(i))

    print(intervocal)

# должна считать частотность звуков в инициалях и финалях соответственно
def M_3(column_n, f_out_name):
    f_name = 'phon_table.tsv'
    abs_freq = {}

    my_lines = F_get_lines(f_name)
    #print(my_lines[0])

    dfg = my_lines[1:]  # РАБОЧАЯ ВЕРСИЯ ДЛЯ ВСЕХ СЛОВ
    #dfg = my_lines[0:1330]

    for line in dfg:
        line_split = line.split('\t')
        #print(line_split)
        my_line = line_split[column_n] # берётся сущность из соответствующей колонки для подсчёта
        my_line = my_line.strip()
        my_line = my_line.split('-')
        #print(my_line)

        for elem in my_line:
            abs_freq = F_w_d(abs_freq, elem)

    #f_out_name = f_out_name + '.tsv'
    F_sort_wd_items(abs_freq, f_out_name)

# должна считать вероятность и сравнивать
def M_4(f_name):
    my_lines = F_get_lines(f_name)
    fgh = my_lines[1:]
    #fgh = my_lines[1:654]

    my_segments = []
    my_dict = {}

    #symbols = ['S', 'O']
    symbols = []

    for line in fgh:
        #line =
        line_split = line.split('\t')
        # print(line_split)
        my_line = line_split[0]  # берётся сущность из соответствующей колонки для подсчёта
        my_line = my_line.strip()
        # print(my_line)
        if my_line not in symbols:
            symbols = symbols + list(my_line)
            my_segments = my_segments + [line_split[0], (line_split[1]).strip()]

    print(my_segments)
    len_symbols = len(symbols) * 2
    #for i in range(0, 4):            # для инициалей с учётом слоговых
    for j in range(0, len_symbols, 2):

        probability_1 = my_segments[j+1]#[1]
        k_name_1 = my_segments[j]#[0]]
        my_dict[k_name_1] = probability_1

        for k in range(0, len_symbols, 2):
            #print((my_segments[j+1]) * int(my_segments[k+1]))

            probability_2 = int(my_segments[j+1]) * int(my_segments[k+1])
            # P(A⋅B)=P(A)⋅P(B)
            k_name_2 = my_segments[j] + my_segments[k]
            my_dict[k_name_2] = probability_2

            #for l in range(0, len_symbols):
            #    for m in range(0, len_symbols):
            #        print('f')

    #print(symbols)
    print(my_dict)


#M_create_table_1()

#M_3(7, 'initial_segments')
#M_3(9, 'final_segments')
#M_3(29, 'manner_initial_segments')
#M_3(31, 'manner_fintial_segments')
#M_3(51, 'place_initial_segments')
#M_3(53, 'place_fintial_segments')
#M_3(73, 'quality_initial_segments')
#M_3(75, 'quality_fintial_segments')

M_4('quality_initial_segments_frequency.txt')

syllabic_heads = ['a', 'e', 'i', 'o', 'u', 'è', 'ì', 'L', 'N', 'R']  # 'ə']

#M_create_table_2()

print("--- %s seconds ---" % (time.time() - start_time))
