class Unifictaion:
    def __init__(self, file_name):
        self.file_name = file_name
        import numpy as np

    def read_file(self):
        clause = []
        file = open('cnf_pairs/' + self.file_name, 'r')
        lines = file.readlines()
        list_terms=[]
        for line in lines:
            terms=[]
            line = line.replace(' ', '')
            splited_txts = line.split("|")
            appended_list_predicates = []
            for splited_txt in splited_txts:
                idx_p_open = splited_txt.rfind('(')
                predicate = splited_txt[:idx_p_open]
                idx_p_close = splited_txt.rfind(')')
                arg = splited_txt[idx_p_open + 1:idx_p_close]
                term = Term(predicate,arg)
                terms.append(term)

            list_terms.append(terms)
        return list_terms

    def identical_predicate(self, p1, p2):
        if p1 != "" and p2 != "" and (p1 == p2 or p1 == "-" + p2 or "-" + p1 == p2):
            return 1
        else:
            return 0

    def variable(self, var):
        if type(var) is  not list and var.islower():
            return 1
        else:
            return 0

    def constant(self, var):
        if not var[0].islower():
            return 1
        else:
            return 0

    def read_clause(self,list_terms):
        count=0
        import copy
        self.print_output(list_terms,1)
        for obj1 in range(len(list_terms[0])):
            for obj2 in range(len(list_terms[1])):

                r=11
                list_terms_copy = copy.deepcopy(list_terms)
                if self.identical_predicate(list_terms_copy[0][obj1].predicate, list_terms_copy[1][obj2].predicate):
                    count+=1
                    args_str_list1 = list_terms_copy[0][obj1].arg
                    args_str_list2 = list_terms_copy[1][obj2].arg
                    args_list1 = args_str_list1.split(",")
                    args_list2 = args_str_list2.split(",")
                    for arg_idx in range(len(args_list1)):
                        result_unify=self.unify(args_list1[arg_idx], args_list2[arg_idx])
                        if self.variable(result_unify):
                            result_unify=result_unify+str(r)
                            r+=1
                        args_str_list1 = list_terms_copy[0][obj1].arg
                        args_str_list2 = list_terms_copy[1][obj2].arg
                        args_list1 = args_str_list1.split(",")
                        args_list2 = args_str_list2.split(",")
                        if result_unify!=0:
                            list_terms_copy=self.subsitute(args_list1[arg_idx], args_list2[arg_idx],result_unify,args_str_list1, args_str_list2,list_terms_copy)

                    self.print_output(list_terms_copy)
        return count



    def unify(self, a1, a2):

        if self.constant(a1):
            if self.constant(a2):
                if a1 == a2:
                    return a1
                else:
                    return 0
            if self.variable(a2):
                return a1
        else:
            if self.constant(a2):
                return a2
            elif self.variable(a2):
                return "v"

    def subsitute(self,var1,var2,result_unify,arg_str1,arg_str2,list_terms):

        for idx_terms in range(len(list_terms)):
            arg_list = []
            for idx_term in range(len(list_terms[idx_terms])):
                str=list_terms[idx_terms][idx_term].arg
                replace_txt=str.replace(var1, result_unify).replace(var2, result_unify)
                list_terms[idx_terms][idx_term].arg=replace_txt

        return list_terms

    def print_output(self,list_terms,original=0):
        if original == 1:
            final_output1 = "1. "
            final_output2 = "2. "

        else:
            final_output1 = ""
            final_output2 = ""

        for term in list_terms[0]:
            if type(term.arg)==list :

                text_result = ",".join(term.arg)

            else:
                text_result=term.arg
            final_output1+=term.predicate+"("+text_result+")"+" | "


        print("\t")
        print(final_output1[:-2])
        for term in list_terms[1]:
            if type(term.arg)==list :
                text_result = ",".join(term.arg)
            else:
                text_result=term.arg
            final_output2+= term.predicate+"("+text_result+")"+" | "

        f = final_output2.rstrip(final_output2[-1])
        print(final_output2[:-2])
        return 1


class Term:
    def __init__(self, predicate,arg):
        self.predicate = predicate
        self.arg= arg


a = Unifictaion("p3.cnf")
list_terms = a.read_file()
count=a.read_clause(list_terms)
print("\nAttempted ", count , "unification")


