import spacy
from spacy.tokens import DocBin
from tqdm import tqdm

import json

from sklearn.model_selection import train_test_split



class data_prep():

    def __init__(self,path) -> None:
        self.path = path
        try:
            self.data = json.load(open(path))
            print("Training data loaded without error.")
            
            self.train, self.test = train_test_split(self.data, test_size=0.1)
        except FileNotFoundError:
            self.data = 0 
            print("There is an error with file path. Please provide an accurate path and try again.")   


    def prep_data(self,dt):
        self.nlp = spacy.blank('en')
        self.db = DocBin()
        self.file = open('error.txt', 'w')

        for text, annot in tqdm(dt):
            doc = self.nlp.make_doc(text)
            annot = annot['entities']

            ents = []
            entity_indices = []

            for start,end, label in annot:
                skip_entity = False
                # check if there is overlap in span of entities
                for idx in range(start,end):
                    if idx in entity_indices:
                        skip_entity = True
                        break
                if skip_entity == True:
                    continue

                entity_indices = entity_indices + list(range(start,end))
                try:
                    span = doc.char_span(start, end, label=label, alignment_mode = 'strict')
                except:
                    continue
                
                if span is None:
                    err_data = str(start)+f"{end}" + " " + str(text) +"\n"
                    #elf.file.write(err_data)
                else:
                    ents.append(span)
            try:
                doc.ents = ents
                self.db.add(doc)
            except:
                pass
        return self.db

    def get_train_test(self):
        train_dt = self.prep_data(self.train)
        test_dt = self.prep_data(self.test)

        train_dt.to_disk('train_data.spacy')
        test_dt.to_disk('test_data.spacy')


if __name__=="__main__":
    path = "train/NER/train_data.json"
    data_preper = data_prep(path)
    if data_preper.data:
        data_preper.get_train_test()