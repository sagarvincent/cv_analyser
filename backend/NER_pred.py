import spacy

class NER_pred():
    def __init__(self):        
        self.nlp_model =  spacy.load(r'model\model\roberta-base\model-best')

    def get_pred(self):
        doc = self.nlp_model('My name is Sagar Vincent. I currently work as a Machine Learning Engineer at University of Birmingham, United Kingdom. My skills inclusde : machine learning, Deep learning, computer vision, robotics, linux etc. I am a honest, passionate, hardworking individual, capable of delivering the highest quality works on a tight deadline.')
        for ent in doc.ents:
            print(ent.text, "  ->>>>>>", ent.label_)


if __name__=="__main__":

    nlp_predictor = NER_pred()
    nlp_predictor.get_pred()





















