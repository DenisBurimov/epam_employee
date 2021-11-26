class Words:
    def __init__(self, filename):
        self.filename = filename
        with open('sample.txt', 'r') as f:
            content = f.read()
        self.content = content

    def amount_of_symbols(self):
        str_text = [x for x in self.content]
        return len(str_text)

    def words_amount(self):
        stringed_text = ''
        for symbol in self.content:
            stringed_text += symbol
        listed = stringed_text.split()
        return len(listed)

    def sentences(self):
        endpoints = ['.', '!', '?', '...', '!!!', '?!']
        sentences_amount = [x for x in self.content if x in endpoints]
        return len(sentences_amount)