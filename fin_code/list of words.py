# macedonian_dict.tsv
#12
import re

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
def F_standart_grammar(grammar_inf):
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
    a1 = a1.replace('Модален збор', 'modal_word')

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

# количество слогов: на выходе количество слогов вообще по гласным и с учётом "слоговых"
# (+печатает слова "без-гласных"). (+печатает слова с двумя шва).
def F_number_syllables_by_vowels_plus_schwa(word, syllabic_head):
    n_syllables = 0

    for element in word:
        for i in range(0, 10):
            if element == syllabic_head[i]:
                n_syllables += 1
#['a', 'e', 'i', 'o', 'u', 'è', 'ì', 'L', 'N', 'R']
    n_syllables_s = n_syllables
    for letter in word:
        if letter == syllabic_head[7] or syllabic_head[8] or syllabic_head[9]:
            n_syllables_s = n_syllables_s + 1
        else:
            n_syllables_s = n_syllables_s

    total_n = str(n_syllables) + '\t' + str(n_syllables_s)
    #print(total_n)

# такое слово вероятней всего сокращение
    #if n_syllables == 0:
        #print(word)

# проверка разности слогов: две швы в одном слове было бы подозрительно, (если это не Р)
    alt_j = n_syllables_s - n_syllables_s
    if alt_j != 0 and 1:
        print ('слова с двумя слоговыми: ', total_n)

    return total_n

# инициали БЕЗ УЧЁТА СЛОГОВОСТИ Р
def F_words_initials_wo_sR(word):
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
    else:
        initial = 'VOW'

    #print(initial)
    return initial

# финали БЕЗ УЧЁТА СЛОГОВЫХ СОНОРНЫХ
def F_words_finals_wo_sS(word):
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
    #if res!= ['']:
    if res != []:
        #print(res)
        #final = str(res)#[1]
        final = res[0][0]
        res1 = re.findall('^(-).', final)
        if res1:
            #print(res1[0])
            final = final.replace('-', '', 1)

    #print(final)
    return final

# сортировка
def F_sort(list_to_sort):
    sorted_c = str(sorted(list_to_sort))
    sorted_c = sorted_c.replace("'", "")
    sorted_c = sorted_c.replace("[", "")
    sorted_c = sorted_c.replace("]", "")
    sorted_c = sorted_c.split(',')

    #print(sorted_c)
    return sorted_c

# таблица с:
#   грамматической информацией
#   словами
#   разбиение по буквам
#   разбиение по буквам в МФА
#   количествами слогов
#   инициалями
#   финалями
def M_create_table_1():
    f_name = 'macedonian_dict1.tsv'

    syllabic_heads = ['a', 'e', 'i', 'o', 'u', 'è', 'ì', 'L', 'N', 'R'] #'ə']

    possible_initials_wo_s = []
    possible_initials = [] # 'INITIALS'
    possible_finals_wo_s = []
    possible_finals = [] # 'FINALS'
    all_words = ''
    st = '\t'
    sn = '\n'

    my_lines = F_get_lines(f_name)
    #asd = my_lines[1:54498]        # все слова: без первой строчки с названиями
    asd = my_lines[1:]
    #asd = my_lines[4000:5000]     # тестовая выборка

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

        grammar_inf = line_split[2] # для данного слова есть его грамматическая инфорация
        grammar_inf = F_standart_grammar(grammar_inf)
        #print(grammar_inf)
# получена грамматическая информация
        full_data = grammar_inf + st + entry # грам информация и слово через \t
        #print(full_data)


        if not ('_' in full_data or 'abbr' in full_data or 'affixoid_pref' in full_data or 'affixoid_suf' in full_data or 'compound' in full_data):

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

# следующие строчки кода печатают слова со слоговыми л и н
            #res_l = re.findall('-L$', ipa_word)
            #if res_l:
            #    print(ipa_word)
            #res_n = re.findall('-N$', ipa_word)
            #if res_n:
            #    print(ipa_word)


            number_syllables = F_number_syllables_by_vowels_plus_schwa(ipa_word, syllabic_heads)
# получено количество слогов по гласным + '\t' слоговым
            full_data = full_data + st + str(number_syllables)
            #print(full_data)

            words_initials_wo_sR = F_words_initials_wo_sR(ipa_word)
# получены инициали слов МФА !!! без расчёта слоговых
            full_data = full_data + st + words_initials_wo_sR

            words_initials = F_words_initials(ipa_word)
# получены инициали слов МФА
            full_data = full_data + st + words_initials
            #print(full_data)

            words_finals_wo_sR = F_words_finals_wo_sS(ipa_word)
# получены финали слов МФА !!! без расчёта слоговых
            full_data = full_data + st + words_finals_wo_sR

            words_finals = F_words_finals(ipa_word)
# получены финали слов МФА
            full_data = full_data + st + words_finals

            #if words_initials_wo_sR not in possible_initials_wo_s:
            #    possible_initials_wo_s.append(words_initials_wo_sR)     # инициали без слоговых: possible_initials_wo_s
            if words_initials not in possible_initials:
                possible_initials.append(words_initials)                # инициали со слоговыми: possible_initials
                #possible_initials = possible_initials + sn + words_initials

            #if words_finals_wo_sR not in possible_finals_wo_s:
            #    possible_finals_wo_s.append(words_finals_wo_sR)         # финали без слоговых: possible_finals_wo_s
            if words_finals not in possible_finals:
                possible_finals.append(words_finals)                    # инициали без слоговых: possible_finals
                #possible_finals = possible_finals + sn + words_finals

            #print(full_data)

            all_words = all_words + sn + full_data

    #print(all_words)
# печать всех инициалей

    possible_initials_W = 'INITIALS'
    possible_initials = F_sort(possible_initials)
    for initial in possible_initials:
        possible_initials_W = possible_initials_W + sn + initial
    #print(possible_initials_W)
    F_write_in_file(possible_initials_W, 'initials.txt')


# печать всех финалей
    possible_finals_W = 'FINALS'
    possible_finals = F_sort(possible_finals)
    for final in possible_finals:
        possible_finals_W = possible_finals_W + sn + final
    #print(possible_finals_W)
    F_write_in_file(possible_finals_W, 'finals.txt')

    first_line = 'grammar' + st + 'lemma' + st + 'lettering' + st + 'ipa_lettering' + st + 'n_syllables_wo' \
                 + st + 'n_syllables' + st + 'initial_wo' + st + 'initial' + st + 'final_wo' + st + 'final'

    data = first_line + all_words
    F_write_in_file(data, 'phon_table.tsv')

M_create_table_1()
