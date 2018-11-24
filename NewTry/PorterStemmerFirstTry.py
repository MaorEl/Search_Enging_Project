class PorterStemmer:
    def isCons(self, letter):
        if letter == 'a' or letter == 'e' or letter == 'i' or letter == 'o' or letter == 'u':
            return False
        elif letter == 'A' or letter == 'E' or letter == 'I' or letter == 'O' or letter == 'U':
            return False
            return True

    def isConsonant(self, word, i):
        letter = word[i]
        if self.isCons(letter):
            if letter == 'y' and (-1*(i-1))>len(word) and self.isCons(word[i - 1]):
                return False
            elif letter == 'Y' and (-1*(i-1))>len(word) and self.isCons(word[i - 1]):
                return False
            else:
                return True
        else:
            return False

    def isVowel(self, word, i):
        return not(self.isConsonant(word, i))

    # *S
    def endsWith(self, stem, letter):
        if stem.endswith(letter):
            return True
        else:
            return False

    # *v*
    def containsVowel(self, stem):
        for i in stem:
            if not self.isCons(i):
                return True
        return False

    # *d
    def doubleCons(self, stem):
        if len(stem) >= 2:
            if self.isConsonant(stem, -1) and self.isConsonant(stem, -2):
                return True
            else:
                return False
        else:
            return False

    def getForm(self, word):
        form = []
        formStr = ''
        for i in range(len(word)):
            if self.isConsonant(word, i):
                if i != 0:
                    prev = form[-1]
                    if prev != 'C':
                        form.append('C')
                else:
                    form.append('C')
            else:
                if i != 0:
                    prev = form[-1]
                    if prev != 'V':
                        form.append('V')
                else:
                    form.append('V')
        for j in form:
            formStr += j
        return formStr

    def getM(self, word):
        form = self.getForm(word)
        m = form.count('VC')
        return m

    # *o
    def cvc(self, word):
        if len(word) >= 3:
            f = -3
            s = -2
            t = -1
            third = word[t]
            if self.isConsonant(word, f) and self.isVowel(word, s) and self.isConsonant(word, t):
                if third != 'w' and third != 'x' and third != 'y':
                    return True
                elif third != 'W' and third != 'X' and third != 'Y':
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def replace(self, orig, rem, rep):
        result = orig.rfind(rem)
        base = orig[:result]
        replaced = base + rep
        return replaced

    def replaceM0(self, orig, rem, rep):
        result = orig.rfind(rem)
        base = orig[:result]
        if self.getM(base) > 0:
            replaced = base + rep
            return replaced
        else:
            return orig

    def replaceM1(self, orig, rem, rep):
        result = orig.rfind(rem)
        base = orig[:result]
        if self.getM(base) > 1:
            replaced = base + rep
            return replaced
        else:
            return orig

    def step1a(self, word):
        if word.endswith('sses'):
            word = self.replace(word, 'sses', 'ss')
        elif word.endswith('ies'):
            word = self.replace(word, 'ies', 'i')
        elif word.endswith('ss'):
            word = self.replace(word, 'ss', 'ss')
        elif word.endswith('s'):
            word = self.replace(word, 's', '')
        elif word.endswith('SSES'):
            word = self.replace(word, 'SSES', 'ss')
        elif word.endswith('IES'):
            word = self.replace(word, 'IES', 'I')
        elif word.endswith('SS'):
            word = self.replace(word, 'SS', 'SS')
        elif word.endswith('S'):
            word = self.replace(word, 'S', '')
        else:
            pass
        return word

    def step1b(self, word):
        flag = False
        if word.endswith('eed'):
            result = word.rfind('eed')
            base = word[:result]
            if self.getM(base) > 0:
                word = base
                word += 'ee'
        elif word.endswith('ed'):
            result = word.rfind('ed')
            base = word[:result]
            if self.containsVowel(base):
                word = base
                flag = True
        elif word.endswith('ing'):
            result = word.rfind('ing')
            base = word[:result]
            if self.containsVowel(base):
                word = base
                flag = True
        elif word.endswith('EED'):
            result = word.rfind('EED')
            base = word[:result]
            if self.getM(base) > 0:
                word = base
                word += 'EE'
        elif word.endswith('ED'):
            result = word.rfind('ED')
            base = word[:result]
            if self.containsVowel(base):
                word = base
                flag = True
        elif word.endswith('ING'):
            result = word.rfind('ING')
            base = word[:result]
            if self.containsVowel(base):
                word = base
                flag = True
        if flag:
            if word.endswith('at') or word.endswith('bl') or word.endswith('iz'):
                word += 'e'
            elif self.doubleCons(word) and not self.endsWith(word, 'l') and not self.endsWith(word, 's') and not self.endsWith(word, 'z'):
                word = word[:-1]
            elif not word.isupper() and self.getM(word) == 1 and self.cvc(word):
                word += 'e'
            elif word.endswith('AT') or word.endswith('BL') or word.endswith('IZ'):
                word += 'e'
            elif self.doubleCons(word) and not self.endsWith(word, 'L') and not self.endsWith(word, 'S') and not self.endsWith(word, 'Z'):
                word = word[:-1]
            elif word.isupper() and self.getM(word) == 1 and self.cvc(word):
                word += 'E'
            else:
                pass
        else:
            pass
        return word

    def step1c(self, word):
        if word.endswith('y'):
            result = word.rfind('y')
            base = word[:result]
            if self.containsVowel(base):
                word = base
                word += 'i'
        elif word.endswith('Y'):
            result = word.rfind('Y')
            base = word[:result]
            if self.containsVowel(base):
                word = base
                word += 'i'
        return word

    def step2(self, word):
        if word.endswith('ational'):
            word = self.replaceM0(word, 'ational', 'ate')
        elif word.endswith('tional'):
            word = self.replaceM0(word, 'tional', 'tion')
        elif word.endswith('enci'):
            word = self.replaceM0(word, 'enci', 'ence')
        elif word.endswith('anci'):
            word = self.replaceM0(word, 'anci', 'ance')
        elif word.endswith('izer'):
            word = self.replaceM0(word, 'izer', 'ize')
        elif word.endswith('abli'):
            word = self.replaceM0(word, 'abli', 'able')
        elif word.endswith('alli'):
            word = self.replaceM0(word, 'alli', 'al')
        elif word.endswith('entli'):
            word = self.replaceM0(word, 'entli', 'ent')
        elif word.endswith('eli'):
            word = self.replaceM0(word, 'eli', 'e')
        elif word.endswith('ousli'):
            word = self.replaceM0(word, 'ousli', 'ous')
        elif word.endswith('ization'):
            word = self.replaceM0(word, 'ization', 'ize')
        elif word.endswith('ation'):
            word = self.replaceM0(word, 'ation', 'ate')
        elif word.endswith('ator'):
            word = self.replaceM0(word, 'ator', 'ate')
        elif word.endswith('alism'):
            word = self.replaceM0(word, 'alism', 'al')
        elif word.endswith('iveness'):
            word = self.replaceM0(word, 'iveness', 'ive')
        elif word.endswith('fulness'):
            word = self.replaceM0(word, 'fulness', 'ful')
        elif word.endswith('ousness'):
            word = self.replaceM0(word, 'ousness', 'ous')
        elif word.endswith('aliti'):
            word = self.replaceM0(word, 'aliti', 'al')
        elif word.endswith('iviti'):
            word = self.replaceM0(word, 'iviti', 'ive')
        elif word.endswith('biliti'):
            word = self.replaceM0(word, 'biliti', 'ble')
        if word.endswith('ATIONAL'):
            word = self.replaceM0(word, 'ATIONAL', 'ATE')
        elif word.endswith('TIONAL'):
            word = self.replaceM0(word, 'TIONAL', 'TION')
        elif word.endswith('ENCI'):
            word = self.replaceM0(word, 'ENCI', 'ENCE')
        elif word.endswith('ANCI'):
            word = self.replaceM0(word, 'ANCI', 'ANCE')
        elif word.endswith('IZER'):
            word = self.replaceM0(word, 'IZER', 'IZE')
        elif word.endswith('ABLI'):
            word = self.replaceM0(word, 'ABLI', 'ABLE')
        elif word.endswith('ALLI'):
            word = self.replaceM0(word, 'ALLI', 'AL')
        elif word.endswith('ENTLI'):
            word = self.replaceM0(word, 'ENTLI', 'ENT')
        elif word.endswith('ELI'):
            word = self.replaceM0(word, 'ELI', 'E')
        elif word.endswith('OUSLI'):
            word = self.replaceM0(word, 'OUSLI', 'OUS')
        elif word.endswith('IZATION'):
            word = self.replaceM0(word, 'IZATION', 'IZE')
        elif word.endswith('ATION'):
            word = self.replaceM0(word, 'ATION', 'ATE')
        elif word.endswith('ATOR'):
            word = self.replaceM0(word, 'ATOR', 'ATE')
        elif word.endswith('ALISM'):
            word = self.replaceM0(word, 'ALISM', 'AL')
        elif word.endswith('IVENESS'):
            word = self.replaceM0(word, 'IVENESS', 'IVE')
        elif word.endswith('FULNESS'):
            word = self.replaceM0(word, 'FULNESS', 'FUL')
        elif word.endswith('OUSNESS'):
            word = self.replaceM0(word, 'OUSNESS', 'OUS')
        elif word.endswith('ALITI'):
            word = self.replaceM0(word, 'ALITI', 'AL')
        elif word.endswith('IVITI'):
            word = self.replaceM0(word, 'IVITI', 'IVE')
        elif word.endswith('BILITI'):
            word = self.replaceM0(word, 'BILITI', 'BLE')
        return word

    def step3(self, word):
        if word.endswith('icate'):
            word = self.replaceM0(word, 'icate', 'ic')
        elif word.endswith('ative'):
            word = self.replaceM0(word, 'ative', '')
        elif word.endswith('alize'):
            word = self.replaceM0(word, 'alize', 'al')
        elif word.endswith('iciti'):
            word = self.replaceM0(word, 'iciti', 'ic')
        elif word.endswith('ful'):
            word = self.replaceM0(word, 'ful', '')
        elif word.endswith('ness'):
            word = self.replaceM0(word, 'ness', '')
        elif word.endswith('ICATE'):
            word = self.replaceM0(word, 'ICATE', 'IC')
        elif word.endswith('ATIVE'):
            word = self.replaceM0(word, 'ATIVE', '')
        elif word.endswith('ALIZE'):
            word = self.replaceM0(word, 'ALIZE', 'AL')
        elif word.endswith('ICITI'):
            word = self.replaceM0(word, 'ICITI', 'IC')
        elif word.endswith('FUL'):
            word = self.replaceM0(word, 'FUL', '')
        elif word.endswith('NESS'):
            word = self.replaceM0(word, 'NESS', '')
        return word

    def step4(self, word):
        if word.endswith('al'):
            word = self.replaceM1(word, 'al', '')
        elif word.endswith('ance'):
            word = self.replaceM1(word, 'ance', '')
        elif word.endswith('ence'):
            word = self.replaceM1(word, 'ence', '')
        elif word.endswith('er'):
            word = self.replaceM1(word, 'er', '')
        elif word.endswith('ic'):
            word = self.replaceM1(word, 'ic', '')
        elif word.endswith('able'):
            word = self.replaceM1(word, 'able', '')
        elif word.endswith('ible'):
            word = self.replaceM1(word, 'ible', '')
        elif word.endswith('ant'):
            word = self.replaceM1(word, 'ant', '')
        elif word.endswith('ement'):
            word = self.replaceM1(word, 'ement', '')
        elif word.endswith('ment'):
            word = self.replaceM1(word, 'ment', '')
        elif word.endswith('ent'):
            word = self.replaceM1(word, 'ent', '')
        elif word.endswith('ou'):
            word = self.replaceM1(word, 'ou', '')
        elif word.endswith('ism'):
            word = self.replaceM1(word, 'ism', '')
        elif word.endswith('ate'):
            word = self.replaceM1(word, 'ate', '')
        elif word.endswith('iti'):
            word = self.replaceM1(word, 'iti', '')
        elif word.endswith('ous'):
            word = self.replaceM1(word, 'ous', '')
        elif word.endswith('ive'):
            word = self.replaceM1(word, 'ive', '')
        elif word.endswith('ize'):
            word = self.replaceM1(word, 'ize', '')
        elif word.endswith('ion'):
            result = word.rfind('ion')
            base = word[:result]
            if self.getM(base) > 1 and (self.endsWith(base, 's') or self.endsWith(base, 't')):
                word = base
            word = self.replaceM1(word, '', '')
        elif word.endswith('AL'):
            word = self.replaceM1(word, 'AL', '')
        elif word.endswith('ANCE'):
            word = self.replaceM1(word, 'ANCE', '')
        elif word.endswith('ENCE'):
            word = self.replaceM1(word, 'ENCE', '')
        elif word.endswith('ER'):
            word = self.replaceM1(word, 'ER', '')
        elif word.endswith('IC'):
            word = self.replaceM1(word, 'IC', '')
        elif word.endswith('ABLE'):
            word = self.replaceM1(word, 'ABLE', '')
        elif word.endswith('IBLE'):
            word = self.replaceM1(word, 'IBLE', '')
        elif word.endswith('ANT'):
            word = self.replaceM1(word, 'ANT', '')
        elif word.endswith('EMENT'):
            word = self.replaceM1(word, 'EMENT', '')
        elif word.endswith('MENT'):
            word = self.replaceM1(word, 'MENT', '')
        elif word.endswith('ENT'):
            word = self.replaceM1(word, 'ENT', '')
        elif word.endswith('OU'):
            word = self.replaceM1(word, 'OU', '')
        elif word.endswith('ISM'):
            word = self.replaceM1(word, 'ISM', '')
        elif word.endswith('ATE'):
            word = self.replaceM1(word, 'ATE', '')
        elif word.endswith('ITI'):
            word = self.replaceM1(word, 'ITI', '')
        elif word.endswith('OUS'):
            word = self.replaceM1(word, 'OUS', '')
        elif word.endswith('IVE'):
            word = self.replaceM1(word, 'IVE', '')
        elif word.endswith('IZE'):
            word = self.replaceM1(word, 'IZE', '')
        elif word.endswith('ION'):
            result = word.rfind('ION')
            base = word[:result]
            if self.getM(base) > 1 and (self.endsWith(base, 'S') or self.endsWith(base, 'T')):
                word = base
            word = self.replaceM1(word, '', '')
        return word

    def step5a(self, word):
        if word.endswith('e') or word.endswith('E'):
            base = word[:-1]
            if self.getM(base) > 1:
                word = base
            elif self.getM(base) == 1 and not self.cvc(base):
                word = base
        return word

    def step5b(self, word):
        if self.getM(word) > 1 and self.doubleCons(word) and (self.endsWith(word, 'l') or (self.endsWith(word, 'L'))):
            word = word[:-1]
        return word

    def stem(self, word):
        word = self.step1a(word)
        word = self.step1b(word)
        word = self.step1c(word)
        word = self.step2(word)
        word = self.step3(word)
        word = self.step4(word)
        word = self.step5a(word)
        word = self.step5b(word)
        return word

