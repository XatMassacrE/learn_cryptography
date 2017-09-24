import string

lowercase = string.ascii_lowercase

letter_frequency = {
        'e': 0.1268,
        't': 0.0978,
        'a': 0.0788,
        'o': 0.0776,
        'i': 0.0707,
        'n': 0.0706,
        's': 0.0634,
        'r': 0.0594,
        'h': 0.0573,
        'l': 0.0394,
        'd': 0.0389,
        'u': 0.0280,
        'c': 0.0268,
        'f': 0.0256,
        'm': 0.0244,
        'w': 0.0214,
        'y': 0.0202,
        'g': 0.0187,
        'p': 0.0186,
        'b': 0.0156,
        'v': 0.0102,
        'k': 0.0060,
        'x': 0.0016,
        'j': 0.0010,
        'q': 0.0009,
        'z': 0.0006
        }

def get_letter_frequency():
    result = ''
    for key in letter_frequency:
        result += key
    return result

def get_key_size_space(num):
    i = 0
    while True:
        minv = 2**i
        maxv = 2**(i+1)
        if minv < num < maxv:
            if num - minv > maxv - num:
                i += 1
            return i
        i += 1

def substitution(text, key_table):
    text = text.lower()
    result = ''
    for l in text:
        i = lowercase.find(l)
        if i < 0:
            result += l
        else:
            result += key_table[i]
    return result

def caesar_cypher_encrypt(text, shift):
    key_table = lowercase[shift:] + lowercase[:shift]
    return substitution(text, key_table)

def caesar_cypher_decrypt(text, shift):
    return caesar_cypher_encrypt(text, -shift)

def crack_caesar_cypher(text):
    for i in range(26):
        key_table = lowercase[-i:] + lowercase[:-i]
        print(substitution(text, key_table)[:75], '| shift is ', i, )

def insert_letter(text, i, l):
    return text[:i] + l + text[i:]

def get_blank_record(text):
    text = text.lower()
    blank_record = []
    for i in range(len(text)):
        l = text[i]
        item = []
        if lowercase.find(l) < 0:
            item.append(i)
            item.append(l)
            blank_record.append(item)
    return blank_record

def restore_blank_record(text, blank_record):
    for i in blank_record:
        text = insert_letter(text, i[0], i[1])
    return text

def get_trim_text(text):
    text = text.lower()
    trim_text = ''
    for l in text:
        if lowercase.find(l) >= 0:
            trim_text += l
    return trim_text

def get_vigener_key_table(text, key):
    trim_text = get_trim_text(text)
    total_length = len(trim_text)
    key_length = len(key)
    quotient = total_length // key_length
    reminder = total_length % key_length
    key_table = quotient * key + key[:reminder]

    return trim_text, key_table

def get_var(data, mean=0.067):
    if not data:
        return 0
    var_sum = 0
    for d in data:
        var_sum += (d - mean) ** 2

    return var_sum / len(data)

def get_coincidence_index(text):
    trim_text = get_trim_text(text)
    length = len(trim_text)
    letter_stats = []
    for l in lowercase:
        lt = {}
        count = trim_text.count(l)
        lt[l] = count
        letter_stats.append(lt)
    
    index = 0
    for d in letter_stats:
        v = list(d.values())[0]
        index += (v/length) ** 2

    return index

def get_key_length(text):
    trim_text = get_trim_text(text)
    # assume text length less than 26
    group = []
    for n in range(1, 26):
        group_str = ['' for i in range(n)]
        for i in range(len(trim_text)):
            l = trim_text[i] 
            for j in range(n):
                if i % n == j:
                    group_str[j] += l
        group.append(group_str)
        
    var_list = []
    length = 1
    for text in group:
        data = []
        for t in text:
            index = get_coincidence_index(t)
            data.append(index)
        var_list.append([length, get_var(data)])
        length += 1
    var_list = sorted(var_list, key=lambda x: x[1])
    return [v[0] for v in var_list[:12]]

def crack_vigener_cypher(text, key_length):
    blank_record = get_blank_record(text)
    trim_text = get_trim_text(text)
    group = ['' for i in range(key_length)]
    for i in range(len(trim_text)):
        l = trim_text[i] 
        for j in range(key_length):
            if i % key_length == j:
                group[j] += l

    key = ''
    letter_stats_group = []
    for j in range(key_length):
        letter_stats = []
        for l in lowercase:
            lt = {}
            count = group[j].count(l)
            lt[l] = count
            letter_stats.append(lt)
        
        letter_stats = sorted(letter_stats, key=lambda x: list(x.values())[0], reverse=True)
        letter_stats_group.append(letter_stats)
        # print('group', j, ':', letter_stats[:8])

        # gvctxs
        score_list = []
        for i in range(3):
            current_letter = list(letter_stats[i].keys())[0]
            index = lowercase.find(current_letter)
            key_letter = lowercase[index - lowercase.find('e')]
            item = []
            item.append(key_letter)
            score = 0
            for k in range(3):
                vl = list(letter_stats[k].keys())[0]
                for fl in ['t', 'a']:
                    #if i == 1 and (k == 1 or k == 2) and j == 1:
                    if (lowercase.find(key_letter) + lowercase.find(fl)) % 26 == lowercase.find(vl):
                        score += 1
            item.append(score)
            score_list.append(item)
        score_list = sorted(score_list, key=lambda x: x[1], reverse=True)
        key += score_list[0][0]

    plain_text = vigener_cypher_decrypt(trim_text, key)
    return key, restore_blank_record(plain_text, blank_record)
    

def vigener_cypher_encrypt(text, key, is_encrypt=True):
    blank_record = get_blank_record(text)
    trim_text, key_table = get_vigener_key_table(text, key)

    result = ''
    for i in range(len(trim_text)):
        l = trim_text[i]
        index_lowercase = lowercase.find(l)
        index_key_table = lowercase.find(key_table[i])
        if not is_encrypt:
            index_key_table = -index_key_table
        result += lowercase[(index_lowercase + index_key_table) % 26]

    return restore_blank_record(result, blank_record) 

def vigener_cypher_decrypt(text, key):
    return vigener_cypher_encrypt(text, key, False)

def get_index(text):
    result = ''
    for l in text:
        i = lowercase.find(l)
        if not i < 0: 
            result += str(i)
    print(result)

if __name__ == '__main__':
    shift = 3
    plain_text = 'We intend to begin on the first of February unrestricted submarine warfare. We shall endeavor in spite of this to keep the United States of America neutral. In the event of this not succeeding, we make Mexico a proposal of alliance on the following basis: make war together, make peace together, generous financial support and an understanding on our part that Mexico is to reconquer the lost territory in Texas, New Mexico, and Arizona. The settlement in detail is left to you. You will inform the President of the above most secretly as soon as the outbreak of war with the United States of America is certain and add the suggestion that he should, on his own initiative, invite Japan to immediate adherence and at the same time mediate between Japan and ourselves. Please call the Presidents attention to the fact that the ruthless employment of our submarines now offers the prospect of compelling England in a few months to make peace.'
    #cypher_text = caesar_cypher_encrypt(plain_text, shift)
    #caesar_cypher_decrypt(cypher_text, shift)
    #crack_caesar_cypher(cypher_text)
    cypher_text = vigener_cypher_encrypt(plain_text, 'crypto')
    #print(vigener_cypher_decrypt(cypher_text, 'crypto'))
    data = get_key_length(cypher_text)
    for d in data:
        key, plain_text = crack_vigener_cypher(cypher_text, d)
        print(plain_text[:75], '| key length is', d, '| key is', key)
    

