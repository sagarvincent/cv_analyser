import spacy
import re


class similarity_score:
    def __init__(self, cv, jd) -> None:
        self.score = 0
        self.expalnation = "Explanation feature yet to be added "
        self.cv = cv
        self.jd = jd

    def remove_symbols(self, text):
        return re.sub("[^A-Z a-z0-9]+", " ", text)

    def sim_score(self):
        nlp = spacy.load("en_core_web_sm")

        self.cv = self.remove_symbols(self.cv)
        cv_doc = nlp(self.cv)
        cv_doc = " ".join([token.text for token in cv_doc if not token.is_stop])
        cv_doc = nlp(cv_doc)

        self.jd = self.remove_symbols(self.jd)
        jd_doc = nlp(self.jd)
        jd_doc = " ".join([token.text for token in jd_doc if not token.is_stop])
        jd_doc = nlp(jd_doc)

        lemma_jd = {token.lemma_: 1 for token in jd_doc}
        lemma_cv = {token.lemma_: 1 for token in cv_doc}

        for x in lemma_cv:
            if x in lemma_jd:
                self.score += 1
        self.score = round((self.score / len(lemma_jd)), 3)

        return self.score, self.expalnation
