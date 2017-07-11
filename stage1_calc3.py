import re, sys, traceback, nltk
class Calculator:
    def __init__(self, query):
        self.query = query
        #self.digit mapping
        self.digit = {"one":1, "two":2, "three":3, "four":4 , "five":5, "six":6,\
                 "seven":7, "eight":8, "nine":9, "ten":10,"twenty":20, "thirty":30,\
                 "forty":40, "fifty":50, "sixty":60,\
                 "seventy":70, "eighty":80, "ninety":90, "hundred":100\
                    ,"thousand":1000, "million":1000000, "billion": 1000000000}
        self.tens_dict = {"twenty":20, "thirty":30, "forty":40, "fifty":50, "sixty":60,\
                 "seventy":70, "eighty":80, "ninety":90}
        #operator mapping
        self.operator_sym = {"plus":"+", "minus":"-", "times":"*", "by":"/", "mod":"%"}
        #regexp for tagging
        self.operator = r'(plus|minus|times|by|mod)'
        self.number = r'one|two|three|four|five|six|seven|eight|nine'
        self.tens = r'ten|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety'
        #map for tagging
        self.patterns = [(self.number, "number"),(self.tens, "tens"),("hundred", "hundred"),\
                    ("thousand", "thousand"), ("million", "million"), \
                    ("billion", "billion"),(self.operator, "operator"), ("and", "sep"),\
                    (",", "sep"), ("\.", "sep"), ("\?","sep"), ("!","sep"),\
                    ("([0-9]+[+\-/%])+[0-9]+", "numeric")]
        self.priority = {"number":0, "tens":1, "hundred":2\
                    ,"thousand":3, "million":4, "billion": 5,"operator":-1, "sep":-2}
        self.expressions = []
        self.result = []
        self.prev_prio = -1
        self.num_operands = 0
        self.operation = []
        self.cur_num = []
        self.bad_expr = False
        self.expr = []
        self.loop_count = 0
        self.end_of_ip = False
        self.multiple = []
        self.highest_mul = 6
        self.sep_detected = False
        
    def convertToDigit(self):
         cur_operand = 0
         for j in range (len(self.multiple)):
             print(self.multiple[j])
             cur_operand += self.multiple[j]
         self.operation.append(str(cur_operand))
         print(self.operation)
         if self.loop_count != len(self.expr) -1:
             self.multiple = []
             self.cur_num = []
    def appendOperand(self):
         tens_detected = False
         print(self.loop_count)
         print(self.multiple)
         for j in range(len(self.cur_num)):
                cur_multiple = 1
                print(self.cur_num[j])
                if self.cur_num[j] in self.tens_dict: tens_detected = True
                if not tens_detected:
                    print(self.digit[self.cur_num[j]])
                    cur_multiple *= self.digit[self.cur_num[j]]
                else: cur_multiple += self.digit[self.cur_num[j]]
                print(cur_multiple)
                self.multiple.append(cur_multiple)
                print("appending " + str(cur_multiple))
         
        
    def calc(self):
        query = self.query.lower()
        print(query)
                #tagging
        tagger = nltk.RegexpTagger(self.patterns)
        self.expr = tagger.tag(nltk.tokenize.word_tokenize(query))

        print("self.expression = " + str(self.expr))

    #############################init vars for evaluation###########################
        
        print("self.expr length = " + str(len(self.expr)))
    ########################### Evaluation of self.expression(s) ########################
        while self.loop_count < len(self.expr):
            if self.expr[self.loop_count][1] == "numeric":
                if self.loop_count == len(self.expr) -1: self.sep_detected == True
                try:
                    cur_res = eval(self.expr[self.loop_count][0])
                    self.result.append(self.expr[self.loop_count][0] + "=" + str(cur_res))
                    self.loop_count += 1
                    continue
                except:
                    traceback.print_exc()
                    self.loop_count += 1
                    continue
            self.sep_detected = False
            if(self.expr[self.loop_count][1]) == None:
                self.loop_count += 1
                continue
            print("evaluating " + str(self.expr[self.loop_count]))
            if self.bad_expr == True:
                print("bad_expr self.expression")
                while self.priority[self.expr[self.loop_count][1]] > self.priority["sep"]:
                    print("skipping " + self.expr[self.loop_count][1])
                    if self.loop_count < len(self.expr)-1:
                        self.loop_count += 1
                    else:
                        self.end_of_ip = True
                        break
            if self.end_of_ip: break
            if self.priority[self.expr[self.loop_count][1]] == self.priority["sep"] and self.bad_expr == True:
                print("end of bad_expr self.expression")
                self.loop_count += 1
                self.bad_expr = False
                self.loop_count += 1
                continue
            if self.priority[self.expr[self.loop_count][1]] == self.priority["sep"]:
                if self.expr[self.loop_count-1][1] == "numeric" or self.expr[self.loop_count-1][1] == "sep":
                    self.sep_detected = True
                    self.loop_count += 1
                    continue
                self.num_operands = 0
                print("separator/eof detected, calculating self.result")
                self.sep_detected = True
                cur_multiple = 1
                self.highest_mul = 5
                self.appendOperand()
                self.convertToDigit()
                final_exp = "".join(self.operation)
                try:
                    cur_result = eval(final_exp)
                    res_str = final_exp + "=" + str(cur_result)
                    self.result.append(res_str)
                    self.operation = []
                    self.prev_prio = -1
                    self.loop_count += 1
                    continue
                except:
                    self.result.append("error")
                    traceback.print_exc()
                    self.operation = []
                    self.loop_count += 1
                    self.prev_prio = -1
                    continue
                
            if self.expr[self.loop_count][1] == "operator":
                if self.num_operands > 0:
                    self.bad_expr = True
                    self.num_operands = 0
                    self.loop_count += 1
                    continue
                cur_multiple = 1
                self.highest_mul = 6
                print(self.cur_num)
                self.appendOperand()
                self.convertToDigit()
                self.operation.append(self.operator_sym[self.expr[self.loop_count][0]])
                self.num_operands += 1
            elif self.priority[self.expr[self.loop_count][1]] > self.prev_prio:
                print("first self.digit/higher multiplier")
                if self.priority[self.expr[self.loop_count][1]] >= self.highest_mul:
                    print("bad_expr multiplier")
                    self.bad_expr = True
                    self.loop_count += 1
                    continue
                self.cur_num.append(self.expr[self.loop_count][0])
            elif self.priority[self.expr[self.loop_count][1]] < self.prev_prio:
                print("next multiplier")
                cur_multiple = 1
                self.highest_mul = self.priority[self.expr[self.loop_count-1][1]]
                self.appendOperand()
                self.cur_num = []
                """for j in range(len(self.cur_num)):
                    tens_detected = False
                    if self.cur_num[j] in self.tens_dict: tens_detected = True
                    if not tens_detected:
                        cur_multiple *= self.digit[self.cur_num[j]]
                    else: cur_multiple += self.digit[self.cur_num[j]]
                    self.multiple.append(cur_multiple)"""
                
            self.prev_prio = self.priority[self.expr[self.loop_count][1]]                
            self.loop_count += 1
            

        if self.loop_count == len(self.expr) and not self.sep_detected:
            print("last loop")
            print(self.multiple)
            cur_multiple = 1
            self.highest_mul = 5
            
            print(self.cur_num)
            if(len(self.cur_num)==0):
                print("Error")
                pass
            for j in range(len(self.cur_num)):
                tens_detected = False
                if self.cur_num[j] in self.tens_dict: tens_detected = True
                if not tens_detected:
                    cur_multiple *= self.digit[self.cur_num[j]]
                else: cur_multiple += self.digit[self.cur_num[j]]
            self.multiple.append(cur_multiple)
            self.cur_num = []
            cur_operand = 0
            for j in range (len(self.multiple)):
                cur_operand += self.multiple[j]
            self.operation.append(str(cur_operand))
            self.multiple = []
            final_exp = "".join(self.operation)
            try:
                cur_result = eval(final_exp)
                res_str = final_exp + "=" + str(cur_result)
                self.result.append(res_str)
                self.loop_count += 1
            except:
                self.result.append("error")
                traceback.print_exc()
                self.loop_count += 1
        l1 = self.result
        return l1 
################################################################################
