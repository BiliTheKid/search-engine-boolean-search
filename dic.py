# Imports
from collections import Counter,OrderedDict
from math import log

# Class dictionary
class Dictionary(object):
    def __init__(self):
        self._dictionary = {}
        self.stop_list = ["i", "and", "a", "an", "the", "to", "am"]
        self.operators = {
            '&': '%26',
            '|': '%7c',
            '!': '%21',
            '"': '%22',
            '(': '%28',
            ')': '%28'
        }
        self._doc_list = set()
        self.hidden_docs = []

    ##build dic
    def build_dictionary_from_table(self, table):
        self._dictionary = {}
        for row in table:
            term = row[0]
            doc = (row[1], row[2])
            self.add_to_dictionary(term, doc)
            self._doc_list.add(doc)


    #all deatiles for dic
    def get_dictionary(self):
        return self._dictionary
    ##add to dic
    def add_to_dictionary(self, key, value):
        if key in self._dictionary:
            self._dictionary[key].append(value)
        else:
            self._dictionary[key] = [value]
    #
    # def get_wildcard_words(self, word):
    #     word = word.replace("*", "")
    #     return [key for key in self._dictionary if key.find(word) != -1]

    def find_in_dictionary(self, word):
        try:
            global words
            result = []
            if word.find('*') != -1:
                words = self.get_wildcard_words(word) ##doesnt implemnt it this cond
            else:
                words = [word]
            for a_word in words:
                for doc in self._dictionary[a_word]:
                    if word not in self.stop_list:
                        result.append(doc[0])
            return result
        except KeyError:
            return []

    #and for boolean search work on dic not on the db directly
    def execute_and(self, right_operand, left_operand):
        print("exe and",right_operand,left_operand)
        result = list(set(right_operand) & set(left_operand))
        return result
    #or for boolean search work on dic not on the db directly
    def execute_or(self, right_operand, left_operand):
        print("exe or",right_operand, left_operand)
        result = list(set(right_operand) | set(left_operand))
        return list(result)
    ##not for boolean search work on dic not on the db directly
    def execute_not(self, right_operand,left_operand):
        # print("exe not",right_operand , left_operand)
        result=[]
        for doc in left_operand:
            if doc in right_operand:
                # print('not: ',doc)
                continue
            else:
                result.append(doc)
        #check
        if len(result) < 1:
            return [[]]
        return list(result)
    ##doesnt delete the deatiels hide and unhide
    ##remove** hide doc for hide doc
    def hide_doc(self, doc_id):
        self.hidden_docs.append(doc_id)
        print (self.hidden_docs)
    ##for restore** docs unhide
    def un_hide_doc(self, doc_id):
        self.hidden_docs.remove(doc_id)
    ##doesnt implemnt it
    def __tf_tag__(self, tf):
        return 1 + log(tf, 10)

    ##doesnt implemnt it
    def __idf__(self, docs_number, shows):
        return log(docs_number / shows, 10)

    ##doesnt implemnt it
    def tf_idf(self, tf, idf):
        return tf * idf

    ##doesnt implemnt it
    def __sort_by_number_of_words(self, docs_list, query):
        temp_list = []
        for word in query:
            if word in self._dictionary:
                for doc in self._dictionary[word]:
                    temp_list.append(doc[0])
        sorted_dict = Counter(temp_list)
        sorted_dict = sorted(sorted_dict.items(), key=lambda x: x[1])
        sorted_dict.reverse()
        sorted_list = []
        for key in sorted_dict:
            if key[0] in docs_list:
                sorted_list.append(key[0])
        return sorted_list

