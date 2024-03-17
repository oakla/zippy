in_words_file = r"src\zippy\10-million-password-list-top-100000.txt"
out_words_file = r"src\zippy\top-100000-common-passwords.txt"


with open(in_words_file, 'r') as fp:
    words_to_keep = [x for x in fp.readlines() if len(x) >= 8]


with open(out_words_file, 'w') as fp:
    fp.writelines(words_to_keep)