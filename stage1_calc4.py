import re, sys, traceback, nltk, __future__
class Calculator:
    """convert all numbers written as words into numerics, separate the individual queries, and pass them to the os"""
#############################init vars for evaluation###########################
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
        self.operator_sym = {"plus":"+", "minus":"-", "times":"*", "by":"/", "mod":"%",}
        #regexp for tagging
        self.operator = r'(plus|minus|times|by|mod)'
        self.alt_operator = r'(sum of|product of|quotient of|modulo of)'
        self.number = r'one|two|three|four|five|six|seven|eight|nine'
        self.tens = r'ten|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety'
        self.separator_sym = "[?,!]|and"
        #map for tagging
        self.patterns = [(self.number, "number"),(self.tens, "tens"),("hundred", "hundred"),\
                    ("thousand", "thousand"), ("million", "million"), \
                    ("billion", "billion"),("plus|\+","plus"), ("minus|\-","minus"),("negative","minus"),\
                         ("positive","plus"),("point","point"),('divided by',"by"),("by|upon|/", "by"), ("times|\*","times")\
                         ,("mod|modulo|%","mod"),("\d+", "numeric"), (".+?","others")]
        self.pattern_tags = ["number", "tens", "hundred", "thousand", "million", "billion", "plus",\
                             "minus", "by","times","mod"]
        self.priority = {"number":0, "tens":1, "hundred":2\
                    ,"thousand":3, "million":4, "billion": 5,"operator":-1, "sep":-2, "converted":-1}
        self.recognised_words = ["add", "subtract", "multiply", "divide", "mod", "sum", "product", "difference",\
                                 "quotient", "modulo", "remainder", "of", "and",".","(",")",","]
        
        self.expressions = []
        self.sentential_queries = []
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
        self.num_index_range = [-1,-1]
        
    def convertToDigit(self):
         print("ConvertToDigit")
         cur_operand = 0
         #print("multiples:")
         #print(self.multiple)
         for j in range (len(self.multiple)):
             #print(self.multiple[j])
             cur_operand += self.multiple[j]
         for j in range(self.num_index_range[0], self.num_index_range[1]+1):
             #print("number starting from " + str(self.num_index_range[0]))
             #print(self.expr)
             print("popping expr " + str(self.num_index_range[0]))
             self.expr.pop(self.num_index_range[0])
         self.expr.insert(self.num_index_range[0], (cur_operand, "converted"))
         #print(self.expr)
         self.cur_num = []
         self.multiple = []
         print("cur_num")
         print(self.cur_num)
             
    def appendOperand(self):
         print("appendOperand")
         tens_detected = False
         print("cur_num: ")
         print(self.cur_num)
         cur_multiple = 1
         for j in range(len(self.cur_num)):
                if self.cur_num[j] in self.tens_dict: tens_detected = True
                if not tens_detected:
                    #print(str(self.cur_num[j]))
                    cur_multiple *= self.digit[self.cur_num[j]]
                    #print("cur_ multiple=" + str(self.digit[self.cur_num[j]]))
                else:
                    if len(self.cur_num) == 1:
                        cur_multiple = self.digit[self.cur_num[j]]
                    else:
                        cur_multiple += self.digit[self.cur_num[j]]
                    #print("cur_ multiple=" + str(self.digit[self.cur_num[j]]))
         self.multiple.append(cur_multiple)
         print("appending " + str(cur_multiple))

    def convertAndResetNumber(self, loop_count):
        self.num_index_range[1] = loop_count-1
        self.appendOperand()
        self.convertToDigit()
        self.prev_prio = -1
        self.highest_mul = 6
        
        
    def convertNonDigits(self):
        loop_count = 0
        while loop_count < len(self.expr):
            print("loop count: " + str(loop_count))
            print(self.expr)
            if self.bad_expr == True:
                print("bad expr true")
                if self.expr[loop_count][1] in self.pattern_tags:
                    return
                else:
                    self.bad_expr = False
            if self.expr[loop_count][1] == "point":
                print("decimal")
                replacement_tuple=(".","others")
                self.expr.pop(loop_count)
                self.expr.insert(loop_count, replacement_tuple)
                self.convertAndResetNumber(loop_count)
                loop_count = self.num_index_range[0]+1
                self.num_index_range = [-1,-1]
                inner_loop = loop_count+1
                while(inner_loop < len(self.expr)):
                    if self.expr[inner_loop][1] == "number":
                        self.num_index_range = [inner_loop,inner_loop]
                        self.cur_num.append(self.expr[inner_loop][0])
                        self.convertAndResetNumber(inner_loop+1)
                        self.num_index_range = [-1,-1]
                        inner_loop += 1
                        loop_count += 1
                    else: break
                loop_count +=1
                print(self.expr)
                print(len(self.expr),loop_count)
                if loop_count < len(self.expr):
                    while self.expr[loop_count][1] == "number":
                        print(self.expr[loop_count])
                        self.expr.pop(loop_count)
                loop_count -=1
                print("multiple priority:" + str(self.prev_prio))
                    
                
                
                    
            elif self.expr[loop_count][1] in ["plus", "minus", "times", "by", "mod"]:
                if self.expr[loop_count][0] in ["positive", "negative"]:
                    if self.expr[loop_count][0] == "positive":
                        self.expr.pop(loop_count)
                        continue
                    elif self.expr[loop_count][0] == "negative":
                        replacement_tuple=("-","others")
                        self.expr.pop(loop_count)
                        self.expr.insert(loop_count, replacement_tuple)
                        
                else:        
                    print("operator " + self.expr[loop_count][0] + " at " + str(loop_count))
                    replacement_tuple = (self.operator_sym[self.expr[loop_count][1]], self.expr[loop_count][1])
                    self.expr.pop(loop_count)
                    self.expr.insert(loop_count, replacement_tuple)
                    if self.expr[loop_count-1][1] not in ["numeric","converted"]:
                        print(self.num_index_range)
                        self.convertAndResetNumber(loop_count)
                        print(self.num_index_range)
                        loop_count = self.num_index_range[0] + 1
                        self.num_index_range = [-1,-1]
            elif self.expr[loop_count][1] == "others":
                if self.expr[loop_count-1][1] in ["number", "tens", "hundred", "thousand", "million", "billion"] and loop_count-1 >= 0:
                    print("other at " + str(loop_count) + ", number at " + str(loop_count -1))
                    self.convertAndResetNumber(loop_count)
                    loop_count = self.num_index_range[0]+1
                    self.num_index_range = [-1,-1]
                    cur_multiple = 1
            elif self.expr[loop_count][1] != "numeric":
                if self.priority[self.expr[loop_count][1]] > self.prev_prio:
                    if self.priority[self.expr[loop_count][1]] >= self.highest_mul:
                        print("bad multiplier")
                        self.bad_expr = True
                        return
                    if self.prev_prio == -1:
                        print("first multiplier " + str(self.expr[loop_count][0]))
                        self.num_index_range[0] = loop_count
                    else:
                        print(self.prev_prio)
                        print("higher multiplier")
                        self.num_index_range[1] = loop_count
                    self.cur_num.append(self.expr[loop_count][0])
                    print("cur_num append "+ str(self.expr[loop_count][0]))
                elif self.priority[self.expr[loop_count][1]] < self.prev_prio:
                    print("next multiplier")
                    if self.expr[loop_count-1][1] in self.priority:
                        self.highest_mul = self.priority[self.expr[loop_count-1][1]]
                    self.appendOperand()
                    self.cur_num = [self.expr[loop_count][0]]
            try:
                self.prev_prio = self.priority[self.expr[loop_count][1]]
            except:
                pass
            loop_count += 1
        if len(self.cur_num) > 0:
            self.convertAndResetNumber(len(self.expr))
        for i in range(len(self.expr)):
            if self.expr[i][0] == "-" and self.expr[i][1] == "others":
                self.expr.pop(i)
                self.expr.insert(i, ("-", "minus"))
        print("After converting: ")
        print(self.expr)


    def separateForms(self):
        words = []
        #words = [word for (word,etc) in self.expr]
        for i in range(len(self.expr)):
            print(self.expr[i])
            val1 = self.expr[i][0]
            val2 = self.expr[i][1]
            if val2 == "others":
                if val1 in self.recognised_words:
                    words.append(str(val1))
                if (val1 == "(" and self.expr[i-1][1] in ["numeric", "converted"]):
                    if i>0:
                        words.append("*")
            elif val2 == "numeric": 
                if i>0 and self.expr[i-1][0] == ")":
                    words.append("*")
                words.append(str(val1))
            else: words.append(str(val1))
        joinedQuery = "".join(words)
        print(joinedQuery)
        splitQueries = re.split(self.separator_sym, joinedQuery)
        print(splitQueries)
        index = 0
        cur_index = 0
        for query in splitQueries:
            print("index:"+str(index))
            print(splitQueries)
            if query == "":
                index += 1
                continue
            if query[0].isdigit() or query.startswith("(") or query.startswith("-"):          
                try:
                    res =  eval(compile(query, '<string>', 'eval', __future__.division.compiler_flag))
                    print(query + "=" + str(res))
                    self.result.append(query + "=" + str(res))
                except TypeError:
                    self.result.append("Please include the multiplication operator (*) before or after parentheses, wherever applicable.")
                    traceback.print_exc()
                except:
                    self.result.append("Error")
                    traceback.print_exc()
            else:
                cur_index = index+1
                print("cur_index:" + str(cur_index))
                query1 = query + "s"
                op_list = []
                op_list.insert(0,query1)
                while(cur_index < len(splitQueries)):
                    if splitQueries[cur_index].isdigit():
                        splitQueries[cur_index] = splitQueries[cur_index]+"s"
                        op_list.append(splitQueries[cur_index])
                    else: break
                    cur_index += 1
                for i in range(index, cur_index):
                    splitQueries.pop(index)
                splitQueries.insert(index, "".join(op_list))
                print("after joining sentential forms")
                print(splitQueries)
                if splitQueries[index][0].isalpha():
                    nums = re.split("(\D+)",splitQueries[index])
                    for num in nums:
                        if num in ["", "s"]:
                            nums.remove(num)
                    nums.pop()
                    print("nums:")
                    print(nums)
                    if nums[0].startswith("p"):
                        op_string = "*".join(nums[1:])
                        try:
                            res  = eval(compile(op_string, '<string>', 'eval', __future__.division.compiler_flag))
                            print(op_string + "=" + str(res))
                            self.result.append(op_string + "=" + str(res))
                        except:
                            self.result.append("error")
                            traceback.print_exc()
                    if nums[0].startswith("s"):
                        op_string = "+".join(nums[1:])
                        try:
                            res  = eval(compile(op_string, '<string>', 'eval', __future__.division.compiler_flag))
                            print(op_string + "=" + str(res))
                            self.result.append(op_string  + "=" + str(res))
                        except:
                            self.result.append("error")
                            traceback.print_exc()
                    if nums[0].startswith("d"):
                        op_string = "-".join(nums[1:])
                        try:
                            res  = eval(compile(op_string, '<string>', 'eval', __future__.division.compiler_flag))
                            print(op_string + "=" + str(res))
                            self.result.append(op_string  + "=" + str(res))
                        except:
                            self.result.append("error")
                            traceback.print_exc()
                    if nums[0].startswith("q"):
                        op_string = "/".join(nums[1:])
                        try:
                            res = eval(op_strig)
                            print(op_string + "=" + str(res))
                            self.result.append(op_string  + "=" + str(res))
                        except:
                            self.result.append("error")
                            traceback.print_exc()
                    if nums[0].startswith("m") or nums[0].startswith("r"):
                        op_string = "%".join(nums[1:])
                        try:
                            res  = eval(compile(op_string, '<string>', 'eval', __future__.division.compiler_flag))
                            print(op_string + "=" + str(res))
                            self.result.append(op_string  + "=" + str(res))
                        except:
                            self.result.append("error")
                            traceback.print_exc()
                        
            index += 1     
                
    def tagExpr(self):
        query1 = self.query.lower()
        query2 = re.escape(query1)
        query3 = re.split("([()+\-/%\s*])", query1)
        print(query3)
        for ele in query3:
            if ele == " ":
                query3.remove(ele)
        query = " ".join(query3)
        print(query)
################################tagging################################################
        tagger = nltk.RegexpTagger(self.patterns)
        self.expr = tagger.tag(nltk.tokenize.word_tokenize(query))
        for tag in self.expr:
            if tag[1] == None:
                self.expr.remove(tag)
        print("self.expression = " + str(self.expr))
        
        
        print("self.expr length = " + str(len(self.expr)))

                
    def findQueries(self):
        query = self.query.lower()
        self.sentential_queries = re.split("(product of .*?and .*?[,!?.])|"\
                                           "(sum of .*?and .*?[,!?.])"\
                                           "(difference of .*?and .*?[,!?.])"\
                                           "(quotient of .*?and .*?[,!?.])"\
                                           "(modulo of .*?and .*?[,!?.])",query)
            
            
        
    def calc(self):
        
        self.tagExpr()
        self.convertNonDigits()
        self.separateForms()
########################### Evaluation of self.expression(s) ##########################
        l1 = self.result
        return l1 
################################################################################
