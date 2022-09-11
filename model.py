import random

N = 3  # показатель длинны


class Model:
    def __init__(self):
        self.ngram = dict()  # для строки из n-1 первых слов вернет список возможных вариантов слов и кол-во ngram, где оно встречается
        self.swords = set()

    def prepare(self, s: str):  # превращает строку в массив "токенов"
        alp = [chr(i) for i in range(ord('a'), ord('z') + 1)] + \
              [chr(i) for i in range(ord('A'), ord('Z') + 1)] + \
              [chr(i) for i in range(ord('А'), ord('Я') + 1)] + \
              [chr(i) for i in range(ord('а'), ord('я') + 1)] + \
              [chr(i) for i in range(ord('0'), ord('9') + 1)]  # здесь указаны символы, которые я буду считать частью слова

        words = ["!s"] * (N - 1)  # введем !s за обозначение начала текста.
        word = ""
        for c in s:  # вычленяем слова
            if (c in alp):
                word += c
            else:
                if (word != ""):
                    words.append(word.lower())
                    word = ""
        return words

    def upd(self, prev, word):
        if (prev not in self.ngram):
            self.ngram[prev] = dict()
            self.ngram[prev]["!sum"] = 0  # здесь будет количество упоминаний в сумме (понадобится дальше для рандома)
        dic = self.ngram[prev]  # здесь лежат пары [word : cnt]
        if (word not in dic):
            dic[word] = 0
        dic[word] += 1
        dic["!sum"] += 1

    def teach(self, s: str):  # займемся обучением модели
        words = self.prepare(s)
        for i in range(N - 1, len(words)):
            if (words[i] == '!s'): continue
            word = words[i]
            self.swords.add(word)
            st = set()
            for size in range(1, N + 1):
                prev = " ".join(['!s'] * (N - size) + words[i - size + 1: i])
                st.add(prev)
            for x in st:
                self.upd(x, word)

    def get_random(self):
        arr = list(self.swords)
        return arr[random.randint(0, len(arr) - 1)]

    def generate(self, prefix, length):  # принимает список слов и длину генерируемой последовательности
        length -= len(prefix)
        if (len(prefix) == 0):
            prefix.append(self.get_random())
        output = prefix
        current = ["!s"] * N + prefix
        current = current[len(current) - N + 1:]  # берем последние N-1 слов
        for i in range(length):
            prev = " ".join(current)  # подобрали последние слова
            if (prev not in self.ngram.keys()):
                prev = []
                if (N >= 2):
                    prev += ['!s'] * (N - 2)
                prev += [self.get_random()]
                prev = " ".join(prev)
            dic = self.ngram[prev]
            num = random.randint(1, dic['!sum'])
            new_word = ""
            for word, count in dic.items():
                if (word == "!sum"): continue
                if (num <= count):
                    new_word = word
                    break
                num -= count
            # выше реализован способ выбрать слово, однако не брать каждый раз слово с макс вероятностью, а выбрать случайное слово пропорционально тому,
            # сколько раз оно встречается в тексте
            output.append(new_word)
            current = current[1:] + [new_word]
        return output
