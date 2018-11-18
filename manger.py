# Imports
import dataHandler as datah
import stoplist as stopli
import os,inspect
import moce_dir as diry
from collections import Counter

import itertools

# Global Vars
corpus_dir = "source" ##defination  for source directory

num = 1 ##global var
class check_id:
    num = 1


## Class doc object for doclist
class doc_id:
    def __init__(self, Doc_Id, Title, Autor, Language, Brief, Location):
        self.d = Doc_Id
        self.title = Title
        self.autor = Autor
        self.language = Language
        self.brief = Brief
        self.location = Location

# Class word object for postinglist
class word_details:
    def __init__(self,word,docid,hits):
        self.w = word
        self.n = docid
        self.h = hits

# Get files from folder
def get_file_from_folder():
    # go to to dir and get path for every file
    text_files = [os.path.join(corpus_dir, f) for f in os.listdir(corpus_dir)]
    # getting number of docs
    Number_of_docs = len(text_files) ##get len of txt in directory
    index = 0
    file_list = [] #arr for file
    while index < Number_of_docs:
        file_list.append(text_files[index])
        index += 1
    return file_list #return list with all the files names and path

# Find information about the project
def find_between(file, doc_num,filename): ##get deatiles from txt title,autor etc..

    first1 = 'Title: '
    first2 = 'Author: '
    first3 = 'Language: '
    file.replace("\n","")
    first4 = ''.join(file[58:151]) #get lines from txt
    first4 = first4.translate({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"+"\n"}) #regex for pharse and ignore special char
    path= filename.name.split(os.sep)
    first5 = "storage\\"+path[1]
    # print(first5)
    last = '\n'  ##pharse part from text from first char to last char
    try:
        start1 = file.index(first1) + len(first1)
        end1 = file.index(last, start1)
        answer1 = file[start1:end1]
    except ValueError:
        return ""
    try:
        start2 = file.index(first2) + len(first2)
        end2 = file.index(last, start2)
        answer2 = file[start2:end2]
    except ValueError:
        return ""
    try:
        start3 = file.index(first3) + len(first3)
        end3 = file.index(last, start3)
        answer3 = file[start3:end3]
    except ValueError:
        return ""
    doc_det = doc_id(doc_num, answer1, answer2, answer3, first4, first5)
    return doc_det

# Take care of parse file
def file_handler(file, index_doc):
    ##create array for word and freq pharse the text,count words
    ##regex,stoplist create obj to create every word to list and return list
    frequency = {}
    document_text = open(file, 'r') #open file
    text_string = document_text.read().lower() #lower case for word
    text_string = text_string.translate({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
    ##regex for speical char very usefull
    list_for_index = []
    words = text_string.split()
    shows = Counter(words)
    words = list(set(words))
    words.sort()
    for word in words:
        count = frequency.get(word)
        frequency[word] = shows[word]

    frequency_list = frequency.keys()
    ##check stoplist
    frequency_list = stopli.removeStopwords(frequency_list, stopli.stopwords)

    for words in frequency_list:
        # print(words, frequency[words])
        var_1 = word_details(words, index_doc, frequency[words])
        list_for_index.append(var_1)
    return list_for_index

# Insert to DB
def insert_lists(list1):
    k = 0
    for eachvar in list1:
        eachvar = (list1[k])
        datah.insert_to_post_list(eachvar)
        k += 1

##the main loop for main program
def loop_file(index_file_in_folder):
    All_doc = get_file_from_folder()
    for doc in All_doc:
        f = open(doc, 'r')
        con = f.read()
        result_doc_file = find_between(con, index_file_in_folder,f) #find deatiels
        datah.insert_to_doc_list(result_doc_file)   ##insert to db
        var_word_deatils = file_handler(doc, index_file_in_folder)#pharse and handle files postlist
        docy = insert_lists(var_word_deatils) #insert to mysql
        index_file_in_folder += 1 #inc
        f.close() ##close every file that opened before very important
        datah.sort_ab() ##sort db by alphabatic
    return index_file_in_folder

def main():
    diry.copytree(corpus_dir, diry.dst, symlinks=False) #copy dir to another dir
    index_file_in_folder = 1+datah.genrate_docId() #gertate id doc
    loop_file(index_file_in_folder) ##call to loopfile
    diry.delete_dir() #delete source dir
    print('finish index files')

##for debug
if __name__ == "__main__":
    diry.copytree(corpus_dir, diry.dst, symlinks=False)
    datah.create_db()
    index_file_in_folder =0
    index_doc=loop_file(index_file_in_folder)
    diry.delete_dir()
