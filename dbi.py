import pymysql
import os
from dic import Dictionary
import collections

##handle query that part is from another code in web
def shunting_yard(infix_tokens):
    # define precedences
    precedence = {}
    precedence['NOT'] = 3
    precedence['AND'] = 2
    precedence['OR'] = 1
    precedence['('] = 0
    precedence[')'] = 0

    # declare data strucures
    output = []
    operator_stack = []

    # while there are tokens to be read
    for token in infix_tokens:

        # if left bracket
        if (token == '('):
            operator_stack.append(token)

        # if right bracket, pop all operators from operator stack onto output until we hit left bracket
        elif (token == ')'):
            operator = operator_stack.pop()
            while operator != '(':
                output.append(operator)
                operator = operator_stack.pop()

        # if operator, pop operators from operator stack to queue if they are of higher precedence
        elif (token in precedence):
            # if operator stack is not empty
            if (operator_stack):
                current_operator = operator_stack[-1]
                while (operator_stack and precedence[current_operator] > precedence[token]):
                    output.append(operator_stack.pop())
                    if (operator_stack):
                        current_operator = operator_stack[-1]

            operator_stack.append(token)  # add token to stack

        # else if operands, add to output list
        else:
            output.append(token.lower())

    # while there are still operators on the stack, pop them into the queue
    while (operator_stack):
        output.append(operator_stack.pop())
    # print('postfix:', output)  # check
    return output





##declare obj db hanlder from sql to dic
class DBHandler(object):
    def __init__(self):
        self._db = None
        self._cur = None
        self._dbc= None
        self.dictionary = Dictionary()
        self.tokens=[]

    def connect(self):
        try:
            self._db = pymysql.connect("localhost","root","","projectRet",charset='utf8')
            self._cur = self._db.cursor()
            #self.__init_db__()
        except pymysql.DataError as e:
            print(e)

    def build_dictionary(self):
        self.connect()
        self._cur.execute("""SELECT * FROM Postinglist""")
        posting_file_table = self._cur.fetchall()
        self.dictionary.build_dictionary_from_table(posting_file_table)


    def __get_docs_by_id__(self, doc_list):
        self.connect()
        docs = []
        for doc in doc_list:
            self._cur.execute('SELECT * FROM docFile WHERE docId=(%s)',(doc))
            current_doc = self._cur.fetchall()[0]
            doc_id = current_doc[0]
            doc_title = current_doc[1]
            doc_author = current_doc[2]
            doc_language = current_doc[3]
            doc_brief = current_doc[4]
            doc_location = current_doc[5]
            docs.append((doc_id, doc_title, doc_author, doc_language, doc_brief, doc_location))
        # print(docs)
        return docs

    def get_all_doc(self):
        self.connect()
        r=[]
        print('get_all_doc')
        self._cur.execute('SELECT * FROM docFile')
        docs=self._cur.fetchall()
        for d in docs:
            if d not in self.dictionary.hidden_docs:
                r.append(d)

        return r

    def get_hidden_file(self,doc_list):
        self.connect()
        docs = []
        for doc in doc_list:
            self._cur.execute('SELECT * FROM docFile WHERE docId=(%s)', (doc))
            current_doc = self._cur.fetchall()[0]
            doc_id = current_doc[0]
            doc_title = current_doc[1]
            doc_author = current_doc[2]
            doc_language = current_doc[3]
            doc_brief = current_doc[4]
            doc_location = current_doc[5]
            docs.append((doc_id, doc_title, doc_author, doc_language, doc_brief, doc_location))
        # print(docs)
        return docs

    def get_one_doc_by_id(self, docID):
        self.connect()
        print('first:', docID)
        if docID is None:
            print('not found any doc')

        else:
            self._cur.execute('SELECT * FROM docFile WHERE docId=(%s)',(docID))
            current_doc = self._cur.fetchone()
            doc_id = current_doc[0]
            doc_title = current_doc[1]
            doc_author = current_doc[2]
            doc_language = current_doc[3]
            doc_brief = current_doc[4]
            doc_location = current_doc[5]
            # print('current_doc: ',current_doc)
            return current_doc

        return 1


    ##doesnt use that part but it can help to handle query too
    #
    # def __split_query_to_array(self, query):
    #     query = query.replace("%29", ")")
    #     query = query.replace("%7C", "|")
    #     query = query.replace("%26", "&")
    #     query = query.replace("%28", "(")
    #     query = query.replace("%21", "!")
    #     query = query.replace("%22", '"')
    #     query = filter(lambda char: char != '' and char != ' ', query)
    #     query_list =[]
    #     global wordy
    #     for wordy in query:
    #         #check
    #         # print(wordy)
    #         query_list.append(wordy.replace(" ", ""))
    #     words = filter(lambda a_word: a_word not in self.dictionary.operators, query)
    #     return query_list, words


    ##main part to process query
    def process_query(self, query):
        self.tokens.clear()
        # prepare query list
        query = query.replace('(', '( ')
        query = query.replace(')', ' )')
        query = query.split(' ')
        results_stack = []
        postfix_queue = collections.deque(shunting_yard(query))  # get query in postfix notation as a queue
        # print('query: ', query)
        while postfix_queue:
            result = []
            token = postfix_queue.popleft()
            if (token != 'AND' and token != 'OR' and token != 'NOT'):
                # token = stemmer.stem(token)  # stem the token
                # default empty list if not in dictionary
                #print('before:', token)
                #print(self.dictionary.get_dictionary())
                if (token in self.dictionary.get_dictionary()):
                    # print('token in dictionary: ', token)
                    result=self.dictionary.find_in_dictionary(token)
                    self.tokens.append(token)
                    # print('find in dictonary: ',result)
                    # print(dictionary.find_in_dictionary(dictionary,token))
                    # result = load_posting_list(post_file, dictionary[token][0], dictionary[token][1])

            # else if AND operator
            elif (token == 'AND'):
                right_operand = results_stack.pop()
                left_operand = results_stack.pop()
                # print(left_operand, 'AND',right_operand)  # check
                result = self.dictionary.execute_and(right_operand,left_operand)  # evaluate AND

            # else if OR operator
            elif (token == 'OR'):
                right_operand = results_stack.pop()
                left_operand = results_stack.pop()
                # print(left_operand, 'OR', left_operand)  # check
                result = self.dictionary.execute_or(right_operand,left_operand)  # evaluate OR

            # else if NOT operator
            elif (token == 'NOT'):
                right_operand = results_stack.pop()
                left_operand = results_stack.pop()
                # print('NOT !!!! ', right_operand,left_operand)  # check
                result = self.dictionary.execute_not(right_operand,left_operand)  # evaluate NOT

            # push evaluated result back to stack
            results_stack.append(result)
            # print('result:::', results_stack)  # check

        # NOTE: at this point results_stack should only have one item and it is the final result
        if len(results_stack) != 1:print("ERROR: results_stack. Please check valid query")  # check for errors

        return results_stack.pop()

    ##search
    def search(self,query):
        a=[]
        result= self.process_query(query)
        for r in result:
            if r not in self.dictionary.hidden_docs:
                a.append(r)
        docresult=self.__get_docs_by_id__(a)
        # print('docresult: ',docresult)
        return docresult

    def delete(self, doc):
        self.dictionary.hide_doc(doc)

    def restore(self, doc):
        self.dictionary.un_hide_doc(doc)

    def close_connection(self):
         self._db.close()

#FOR DEBUG ONLY
#if __name__ == '__main__':
    # mydb = DBHandler()
    # mydb.connect()
    # mydb.build_dictionary()
    # # a=mydb.dictionary.get_dictionary()
    # # pprint(a)
    # #mydb.__parse_query__("( asleep|     thy ) & !cat")
    # #pprint(mydb.dictionary.get_dictionary())
    # #mydb.__parse_query__("(thy&o)")
    # # mydb.process_query("(thy AND o)")
    # query="title AND thy"
    # #mydb.process_query(query)
    # mydb.search(query)