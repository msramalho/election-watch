import pandas as pd
from .misc import abs_path, find_whole_word


class HatespeechTerms:
    def __init__(self, filename):
        self.terms = pd.read_csv(abs_path(filename), sep=',')
        self.terms.insult = self.terms.insult == "yes"
        self.terms.minority[self.terms.minority == "no"] = False
        self.terms["regex_finder"] = [find_whole_word(w) for w in self.terms["word"].values]

    def get_minority(self, word):
        try: return self.terms[self.terms["word"] == word]["minority"].values[0]
        except: return

    def is_insult(self, word):
        try: return self.terms[self.terms["word"] == word]["insult"].values[0]
        except: return

    def find_all_words(self, text):
        result = []  # {'word': 'WORD', 'minority': 'WORD' | False, 'insult': Boolean}
        for i, row in self.terms.iterrows():
            if row["regex_finder"](text): result.append({"word": row["word"], "minority": row["minority"], "insult": row["insult"]})
        return result
