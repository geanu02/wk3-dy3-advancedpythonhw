string_1 = "igPay atinlay siay oolcay"
string_2 = "elloHay orldway !"

def pigLatin(str_param):
    word_list = str_param.split()
    new_word = ''
    for word in word_list:
        if word.isalpha():
            new_word += word[1:] + word[0] + 'ay '
        else:
            new_word += word
    return new_word.rstrip()
