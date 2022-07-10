import re

html_simbls = {
    '&rsquo;':   '',
    '&#167;':   '§',  # параграф
    '&#169;':   '©',  #	знак охраны авторского права (copyright)
    '&#174;':	'®',  #	символ зарегистрированного товарного знака
    '&#153;':	'™',  #	символ товарного знака
    '&#176;':	'°',  #	знак градуса
    '&laquo;':	'«',  #	левая кавычка (левая елочка)
    '&raquo;':	'»',  #	правая кавычка (правая елочка)
    '&#146;':	'’',  #	апостроф
    '&#132;':	'„',  #	открывающая лапка
    '&#147;':	'“',  #	закрывающая лапка
    '&#147;':	'“',  #	открывающая английская лапка
    '&#148;':	'”',  #	закрывающая английская лапка
    '&#149;':	'•',  #	жирная точка
    '&#150;':	'–',  #	короткое тире (см. одноименный § 158)
    '&minus;':	'−',  #	минус
    '&#177;':	'±',  #	плюс-минус
    '&#151;':	'—',  #	тире
    '&#8470;':	'№',  #	знак номера
    '&quot;':   '"',
    '&nbsp;':   ' ',
    '&mdash;':  '—',
    '&reg;':    '®',
    '&bdquo;':  '"',
    '&ldquo;':  '"',
}

# text_in = '...Когда В. И. Пупкин увидел в газете ("Сермяжная правда" № 45) рубрику Weather Forecast®, он не поверил своим глазам — температуру…'
text_out = '...Когда В.&nbsp;И. Пупкин увидел в&nbsp;газете (&laquo;Сермяжная правда&raquo; &#8470;&nbsp;45) рубрику Weather Forecast<sup class="reg">&reg;</sup>, он&nbsp;не&nbsp;поверил своим глазам&nbsp;&mdash; температуру...<br />'
# text_in = '...Когда В. И. Пупкин правда" № 45) он не поверил своим глазам…'
# text_out = '&rsquo;...Когда В.&nbsp;И. Пупкин правда&quot; &#8470;&nbsp;45) он&nbsp;не&nbsp;поверил своим глазам...&rsquo;'


def struct_text_list(text_out: str, line_max: int = 40) -> list:
    """Очищаем текст от HTML и пакуем слова в предложения длиной line_max
        return list of str
    """

    def striphtml(text: str) -> str:
        """Убираем html tag <..> из текста"""
        p = re.compile(r'<.*?>')
        return p.sub('', text)

    def pack_words(text_list: list, text_len: list) -> list:
        """Пакуем слова в строку и заполняем ее пробелами до нужной длины"""
        idx_start = 0
        idx_stop = 0
        line_cur = 0
        result = []
        while True:
            line_cur += text_len[idx_stop]

            # если равно
            if line_cur == line_max:
                text = ' '.join(text_list[idx_start:idx_stop + 1])
                result.append(text)
                idx_start = idx_stop + 1
                idx_stop = idx_stop
                line_cur = -1

            # если равно + пробел
            if line_cur + 1 == line_max:
                text = ' '.join(text_list[idx_start:idx_stop + 1]) + ' '
                result.append(text)
                idx_start = idx_stop + 1
                idx_stop = idx_stop
                line_cur = -1

            # если больше
            if line_cur > line_max:
                text = ' '.join(text_list[idx_start:idx_stop])
                num_spaces = line_max - (line_cur - 1 - text_len[idx_stop])
                spaces = ''.join([' '] * num_spaces)
                result.append(text + spaces)
                idx_start = idx_stop
                idx_stop = idx_stop - 1
                line_cur = -1

            # если меньше
            idx_stop += 1
            line_cur += 1  # учитываем +1 пробел

            if idx_stop == len(text_len):
                text = ' '.join(text_list[idx_start:])
                spaces = ''.join([' '] * (line_max - line_cur + 1))
                result.append(text + spaces)
                break

        return result

    def words_len(words: list) -> list:
        '''Считаем длину каждого слова'''
        words_len = []
        for word in words:
            words_len.append(len(word))
        return words_len

    text_out = striphtml(text_out)  # убираем html tag <..>
    text_list = text_out.split()  # бьем на слова

    # заменяем ненужные символы на нужные
    for idx, text in enumerate(text_list):
        for key in html_simbls:
            text = text.replace(key, html_simbls[key])
        text_list[idx] = text

    text_len = words_len(text_list)  # Вычисляем длину каждого слова

    if max(text_len) > line_max:  # Проверка на превышение длины слова
        text_html_norm = []
        for item in text_list:
            if len(item) <= line_max:
                text_html_norm.append(item)
            else:
                # Если превышает line_max то бьем на равные части с пробелами
                new_items = [item[i:i + line_max] for i in range(0, len(item), line_max)]
                text_html_norm += new_items
        text_list = text_html_norm
        text_len = words_len(text_list)  # Пересчитываем длину

    return pack_words(text_list, text_len)  # Пакуем в строки


def struct_text_str(text_out: str, line_max: int = 40) -> str:
    """Очищаем текст от HTML и пакуем слова в предложения длиной line_max
        return str
    """
    result = struct_text_list(text_out, line_max)
    return "\n".join(result)


if __name__ == '__main__':
    result = struct_text_str(text_out, 40)
    print(result)
