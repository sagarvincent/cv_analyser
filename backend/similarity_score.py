import spacy
import re


class similarity_score():

    def __init__(self,cv,jd) -> None:
        self.score = 0
        self.expalnation = "Explanation feature yet to be added "
        self.cv = cv
        self.jd = jd
    
    def remove_symbols(self,text):
        cleaned_text = re.sub('[^A-Z a-z0-9]+', ' ', text)
        return cleaned_text

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
        lemma_jd = {}
        lemma_cv = {}
    
        # Lemmatize each token in the text
        for token in jd_doc:
            lemma_jd[token.lemma_] = 1
        for token in cv_doc:
            lemma_cv[token.lemma_] = 1
        # Lemmatize each token in the text
        for x in lemma_cv.keys():    
            if x in lemma_jd.keys():
                self.score= self.score +1
        self.score = round((self.score/len(lemma_jd)),3)
        print(self.score)

        return self.score, self.expalnation

if __name__ =="__main__":
    cv_path = r"D:\Projects\Job\alindor\cv_analyser\test\data\SagarResume-2.pdf"
    s = similarity_score(cv_path, "As an AI Engineer, you will be responsible for developing and implementing AI models and algorithms, building machine learning pipelines, and integrating AI solutions into existing systems. You will collaborate with cross-functional teams to identify business problems and develop AI solutions that meet business requirements. You will also be responsible for researching and evaluating new AI technologies and trends. Responsibilities: • Develop and implement AI models and algorithms. • Integrate AI solutions into existing systems. • Collaborate with cross-functional teams to identify business problems and develop AI solutions that meet business requirements. • Research, evaluate and propose new AI technologies and trends. • Continuously learn and keep up with the latest AI trends and technologies. • Communicate technical concepts to non-technical stakeholders. Requirements: • Bachelor's or Master's degree in computer science, artificial intelligence, machine learning, or a related field. • 3+ years of experience in developing AI solutions in a professional setting. • Proven experience in developing and implementing AI models and algorithms. • Strong programming skills in languages like Python, and SQL. • Experience with popular AI frameworks like TensorFlow, PyTorch. • Experience with building and deploying AI solutions in a production environment • Familiarity with data preprocessing and data augmentation techniques for AI models • Strong understanding of deep learning architectures like CNNs, RNNs, and LSTMs • Experience with data visualization and reporting tools like Matplotib • Excellent problem-solving and analytical skills. • Strong collaboration and communication skills. • Experience with natural language processing, computer vision, and/or speech recognition. • Familiarity with DevOps and CI/CD pipelines for AI solutions.")
    r = s.sim_score()













