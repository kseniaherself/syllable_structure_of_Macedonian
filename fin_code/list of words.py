# macedonian_dict.tsv
#12
# то что WOS то без учёта слоговости
# иниц без сл: 6, со: 4; фин без сл: 5, с: 3
# Plosive, Fricative, Affricate, Lateral, Nasal, Trill, Glide
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

    ipa_consonants = ['dz', 'ts', 'tʃ', 'dʒ', 'lj', 'l', 'm', 'nj', 'n', 'R', 'r',
                      'b', 'p', 'd', 't', 'ɟ', 'c', 'ɡ', 'k',
                      'v', 'f', 'z', 's', 'ʒ', 'ʃ', 'x', 'j']  # add ['R'], минус ['j',]

    #ipa_manner = ['stop', 'fricative', 'stop', 'stop', 'stop', 'fricative', 'fricative', 'affricate', 'stop',
    #              'lateral', 'lateral', 'nasal', 'nasal', 'nasal', 'stop', 'trill', 'fricative', 'stop', 'stop',
    #              'fricative', 'fricative', 'affricate', 'affricate', 'affricate', 'fricative']  # add ['R'], минус ['j',]

    ipa_manner = ['A', 'A', 'A', 'A', 'L', 'L', 'N', 'N', 'N', 'T', 'T',
                  'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P',
                  'F', 'F', 'F', 'F', 'F', 'F', 'F', 'G'] #ДОБАВЛЕНО 'R'

    for i in range(0, 27):
        if ipa_consonants[i] in word:
            word = word.replace(ipa_consonants[i], ipa_manner[i])

    return word

# транспонирование: место образования
def F_articulation_place():
    print('hallo')

# количество слогов: на выходе количество слогов вообще по гласным и с учётом "слоговых"
# (+печатает слова "без-гласных"). (+печатает слова с двумя шва). (+печатает слова с апострофом). (+печатает слова с Л,Н).
def F_number_syllables_by_vowels_plus_schwa(word, syllabic_head):
    n_syllables_wos = 0

    for element in word:
        for i in range(0, 6):
            if element == syllabic_head[i]:
                n_syllables_wos += 1
#['a', 'e', 'i', 'o', 'u', 'è', 'ì', 'L', 'N', 'R']
    n_syllables = n_syllables_wos
    #print(n_syllables_wos)
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
    total_n = str(n_syllables_wos) + '\t' + str(n_syllables)
    #print(total_n)

# такое слово вероятней всего сокращение, но необязательно
    #if n_syllables == 0:
        #print(word)

# проверка разности слогов: две швы в одном слове было бы подозрительно, (если это не Р)
    alt_j = n_syllables - n_syllables_wos
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
    initial = 'VOW'
    res = re.match('([^aeiouèì]+?)(((-)*?[aeiouèì])|$)', word)
    if res:
        initial = res.group(1)
        #print(initial)

    #print(initial)
    return initial

# инициали С УЧЁТОМ СЛОГОВОГО Р
def F_words_initials(word):
    initial = 'VOW'
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
    final = 'VOW'
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
    final = 'VOW'

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

# записывает файл с отсортированными по частотностями штуками
def F_sord_wd_items(my_items, items_name):
    sorted_items = sorted(my_items.items(), key=operator.itemgetter(1), reverse=True)
    items_freq = items_name + '\t' + 'frequency'
    for k in sorted_items:
        items_freq = items_freq + '\n' + k[0] + '\t' + str(k[1])
    f_name = items_name + '_frequency.txt'
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
    items_i = 'INITIALS'
    items_f = 'FINALS'
    f_name = 'macedonian_dict1.tsv'

    syllabic_heads = ['a', 'e', 'i', 'o', 'u', 'è', 'ì', 'L', 'N', 'R'] #'ə']

    initials_wos = {}
    initials = {}
    initials_wos_m = {}
    initials_m = {}

    possible_initials = [] # 'INITIALS'
    possible_initials_M = []

    finals_wos = {}
    finals = {}
    finals_wos_m = {}
    finals_m = {}

    possible_finals = [] # 'FINALS'
    possible_finals_M = []

    all_words = ''

    st = '\t'
    sn = '\n'

    my_lines = F_get_lines(f_name)
    #asd = my_lines[1:54498]        # все слова: без первой строчки с названиями
    asd = my_lines[1:]             # РАБОЧАЯ ВЕРСИЯ ДЛЯ ВСЕХ СЛОВ
    #asd = my_lines[15170:52272]       # тестовая выборка

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

            entry = entry.replace('!', '')
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

            number_syllables = F_number_syllables_by_vowels_plus_schwa(ipa_word, syllabic_heads)
# получено количество слогов по гласным + '\t' слоговым
            full_data = full_data + st + str(number_syllables)
            #print(full_data)

            words_initial_wos = F_words_initials_wos(ipa_word)
# получены инициали слов МФА !!! без расчёта слоговых
            initials_wos_m = F_w_d(initials_wos_m, F_articulation_manner(words_initial_wos))
            initials_wos = F_w_d(initials_wos, words_initial_wos)

            words_initial = F_words_initials(ipa_word)
# получены инициали слов МФА
            initials_m = F_w_d(initials_m, F_articulation_manner(words_initial))
            initials = F_w_d(initials, words_initial)

            words_final_wos = F_words_finals_wos(ipa_word)
# получены финали слов МФА !!! без расчёта слоговых
            finals_wos_m = F_w_d(finals_wos_m, F_articulation_manner(words_final_wos))
            finals_wos = F_w_d(finals_wos, words_final_wos)

            words_final = F_words_finals(ipa_word)
# получены финали слов МФА
            finals_m = F_w_d(finals_m, F_articulation_manner(words_final))
            finals = F_w_d(finals, words_final)

            words_items = words_initial_wos + st + words_initial + st + words_final_wos + st + words_final
            full_data = full_data + st + words_items

# тут нужно разбить на сегменты
            initials_segments_wos = F_items_segments(words_initial_wos, 0, 6, -1)
            initials_segments = F_items_segments(words_initial, 0, 4, -1)

            finals_segments_wos = F_items_segments(words_final_wos, 0, 5, 1)
            finals_segments = F_items_segments(words_final, 0, 3, 1)
# финали и инициали разбиты на сегменты

            segments = initials_segments_wos + initials_segments + finals_segments_wos + finals_segments
            full_data = full_data + st + segments

            words_items_manner = F_articulation_manner(words_items)
# кластеры инициалей и финалей переведены по способу образования
            full_data = full_data + words_items_manner

            segments_manner = F_articulation_manner(segments)
# сегменты инициалей и финалей переведены по способу образования
            full_data = full_data + st + segments_manner

            #if words_initial_wos not in possible_initials_wos:
            #    possible_initials_wos.append(words_initial_wos)     # инициали без учёта слоговых: possible_initials_wos
            if words_initial not in possible_initials:
                possible_initials.append(words_initial)                # инициали со слоговыми: possible_initials
                #possible_initials = possible_initials + sn + words_initial

            #if words_final_wos not in possible_finals_wos:
            #    possible_finals_wos.append(words_final_wos)         # финали без учёта слоговых: possible_finals_wos
            if words_final not in possible_finals:
                possible_finals.append(words_final)                    # финали со слоговыми: possible_finals
                #possible_finals = possible_finals + sn + words_final

            words_initial_M = F_articulation_manner(words_initial)
            if words_initial_M not in possible_initials_M:
                possible_initials_M.append(words_initial_M)

            words_final_M = F_articulation_manner(words_final)
            if words_final_M not in possible_finals_M:
                possible_finals_M.append(words_final_M)

            #print(full_data)

            all_words = all_words + sn + full_data

    #print(all_words)

# печать всех инициалей
    possible_initials_W = items_i
    possible_initials = F_sort_dictionary(possible_initials)
    for initial in possible_initials:
        possible_initials_W = possible_initials_W + sn + initial
    #print(possible_initials_W)
    F_write_in_file(possible_initials_W, 'initials.txt')

# печать всех финалей
    possible_finals_W = items_f
    possible_finals = F_sort_dictionary(possible_finals)
    for final in possible_finals:
        possible_finals_W = possible_finals_W + sn + final
    #print(possible_finals_W)
    F_write_in_file(possible_finals_W, 'finals.txt')

# печать всех инициалей _способ образования
    possible_initials_W_M = items_i
    possible_initials_M = F_sort_dictionary(possible_initials_M)
    for initial in possible_initials_M:
        possible_initials_W_M = possible_initials_W_M + sn + initial
    # print(possible_initials_W)
    F_write_in_file(possible_initials_W_M, 'initials_manner.txt')

# печать всех финалей _способ образования
    possible_finals_W_M = items_f
    possible_finals_M = F_sort_dictionary(possible_finals_M)
    for final in possible_finals_M:
        possible_finals_W_M = possible_finals_W_M + sn + final
        # print(possible_finals_W)
    F_write_in_file(possible_finals_W_M, 'finals_manner.txt')


    first_line = 'grammar' + st + 'lemma' + st + 'lettering' + st + 'ipa_lettering' + st + 'n_syllables_wos' \
                 + st + 'n_syllables' + st + 'initial_wos' + st + 'initial' + st + 'final_wos' + st + 'final' \
                 + st + 'i_wos_6' + st + 'i_wos_5' + st + 'i_wos_4' + st + 'i_wos_3' + st + 'i_wos_2' + st + 'i_wos_1' \
                 + st + 'i_4' + st + 'i_3' + st + 'i_2' + st + 'i_1' \
                 + st + 'f_wos_1' + st + 'f_wos_2' + st + 'f_wos_3' + st + 'f_wos_4'+ st + 'f_wos_5' \
                 + st + 'f_1' + st + 'f_2' + st + 'f_3' \
                 + st + 'i_wos_manner' + st + 'i_manner' + st + 'f_wos_manner' + st + 'f_manner' + st + 'i_wos_6_m' \
                 + st + 'i_wos_5_m' + st + 'i_wos_4_m' + st + 'i_wos_3_m' + st + 'i_wos_2_m' + st + 'i_wos_1_m' \
                 + st + 'i_4_m' + st + 'i_3_m' + st + 'i_2_m' + st + 'i_1_m' \
                 + st + 'f_wos_1_m' + st + 'f_wos_2_m' + st + 'f_wos_3_m' + st + 'f_wos_4_m'+ st + 'f_wos_5_m' \
                 + st + 'f_1_m' + st + 'f_2_m' + st + 'f_3_m' +st + '10' + st + '11' + st + '12' + st + '13' \
                 + st + '14' + st + '15' + st + '16' + st + '17' + st + '18' + st + '19' + st + '20'


    data = first_line + all_words
    #print(data)
#  таблица создана и записана

    F_sord_wd_items(initials_wos, (items_i + '_wos'))
    F_sord_wd_items(initials, items_i)
    F_sord_wd_items(initials_wos_m, (items_i + '_wos_manner'))
    F_sord_wd_items(initials_m, (items_i + '_manner'))

    F_sord_wd_items(finals_wos, (items_f + '_wos'))
    F_sord_wd_items(finals, items_f)
    F_sord_wd_items(finals_wos_m, (items_f + '_wos_manner'))
    F_sord_wd_items(finals_m, (items_f + '_manner'))

    #print(data)
    F_write_in_file(data, 'phon_table.tsv')

M_create_table_1()
print("--- %s seconds ---" % (time.time() - start_time))
