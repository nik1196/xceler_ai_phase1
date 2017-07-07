import re, sys, traceback, nltk

def calc(query):
    query = query.lower()
    print(query)
    #digit mapping
    digit = {"one":1, "two":2, "three":3, "four":4 , "five":5, "six":6,\
             "seven":7, "eight":8, "nine":9, "ten":10,"twenty":20, "thirty":30,\
             "forty":40, "fifty":50, "sixty":60,\
             "seventy":70, "eighty":80, "ninety":90, "hundred":100\
                ,"thousand":1000, "million":1000000, "billion": 1000000000}
    tens_dict = {"twenty":20, "thirty":30, "forty":40, "fifty":50, "sixty":60,\
             "seventy":70, "eighty":80, "ninety":90}
    #operator mapping
    operator_sym = {"plus":"+", "minus":"-", "times":"*", "by":"/", "mod":"%"}
    #regexp for tagging
    operator = r'(plus|minus|times|by|mod)'
    number = r'one|two|three|four|five|six|seven|eight|nine'
    tens = r'ten|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety'
    #map for tagging
    patterns = [(number, "number"),(tens, "tens"),("hundred", "hundred"),\
                ("thousand", "thousand"), ("million", "million"), \
                ("billion", "billion"),(operator, "operator"), ("and", "sep"),\
                (",", "sep"), ("\.", "sep"), ("\?","sep"), ("!","sep"),\
                ("([0-9]+[+\-/%])+[0-9]+", "numeric")]
    #tagging
    tagger = nltk.RegexpTagger(patterns)
    expr = tagger.tag(nltk.tokenize.word_tokenize(query))
    priority = {"number":0, "tens":1, "hundred":2\
                ,"thousand":3, "million":4, "billion": 5,"operator":-1, "sep":-2}
    print("expression = " + str(expr))

#############################init vars for evaluation###########################
    expressions = []
    result = []
    prev_prio = -1
    num_operands = 0
    operation = []
    cur_num = []
    bad_expr = False
    i = 0
    end_of_ip = False
    multiple = []
    highest_mul = 6
    sep_detected = False
    print("expr length = " + str(len(expr)))
########################### Evaluation of expression(s) ########################
    while i < len(expr):
        if expr[i][1] == "numeric":
            if i == len(expr) -1: sep_detected == True
            try:
                cur_res = eval(expr[i][0])
                result.append(expr[i][0] + "=" + str(cur_res))
                i += 1
                continue
            except:
                traceback.print_exc()
                i += 1
                continue
        sep_detected = False
        if(expr[i][1]) == None:
            i += 1
            continue
        print("evaluating " + str(expr[i]))
        if bad_expr == True:
            print("bad expression")
            while priority[expr[i][1]] > priority["sep"]:
                print("skipping " + expr[i][1])
                if i < len(expr)-1:
                    i += 1
                else:
                    end_of_ip = True
                    break
        if end_of_ip: break
        if priority[expr[i][1]] == priority["sep"] and bad_expr == True:
            print("end of bad expression")
            i += 1
            bad_expr = False
            i += 1
            continue
        if priority[expr[i][1]] == priority["sep"]:
            if expr[i-1][1] == "numeric" or expr[i-1][1] == "sep":
                sep_detected = True
                i += 1
                continue
            num_operands = 0
            print("separator/eof detected, calculating result")
            sep_detected = True
            cur_multiple = 1
            highest_mul = 5
            tens_detected = False
            for j in range(len(cur_num)):
                if cur_num[j] in tens_dict: tens_detected = True
                if not tens_detected:
                    cur_multiple *= digit[cur_num[j]]
                else: cur_multiple += digit[cur_num[j]]
            multiple.append(cur_multiple)
            cur_num = []
            cur_operand = 0
            for j in range (len(multiple)):
                cur_operand += multiple[j]
            operation.append(str(cur_operand))
            multiple = []
            final_exp = "".join(operation)
            try:
                cur_result = eval(final_exp)
                res_str = final_exp + "=" + str(cur_result)
                result.append(res_str)
                operation = []
                i += 1
                continue
            except:
                result.append("error")
                traceback.print_exc()
                operation = []
                i += 1
                continue
            
        if expr[i][1] == "operator":
            if num_operands > 0:
                bad_expr = True
                num_operands = 0
                i += 1
                continue
            cur_multiple = 1
            highest_mul = 6
            tens_detected = False
            for j in range(len(cur_num)):
                if cur_num[j] in tens_dict: tens_detected = True
                if not tens_detected:
                    cur_multiple *= digit[cur_num[j]]
                else: cur_multiple += digit[cur_num[j]]
            multiple.append(cur_multiple)
            cur_num = []
            cur_operand = 0
            for j in range (len(multiple)):
                cur_operand += multiple[j]
            operation.append(str(cur_operand))
            operation.append(operator_sym[expr[i][0]])
            multiple = []
            num_operands += 1
        elif priority[expr[i][1]] > prev_prio:
            print("first digit/higher multiplier")
            if priority[expr[i][1]] >= highest_mul:
                print("bad multiplier")
                bad_expr = True
                i += 1
                continue
            cur_num.append(expr[i][0])
        elif priority[expr[i][1]] < prev_prio:
            print("next multiplier")
            cur_multiple = 1
            highest_mul = priority[expr[i-1][1]]
            tens_detected = False
            for j in range(len(cur_num)):
                if cur_num[j] in tens_dict: tens_detected = True
                if not tens_detected:
                    cur_multiple *= digit[cur_num[j]]
                else: cur_multiple += digit[cur_num[j]]
            multiple.append(cur_multiple)
            cur_num = []
        prev_prio = priority[expr[i][1]]
        i += 1
    if i == len(expr) and not sep_detected:
        print("separator/eof detected, calculating result")
        cur_multiple = 1
        highest_mul = 5
        tens_detected = False
        for j in range(len(cur_num)):
            if cur_num[j] in tens_dict: tens_detected = True
            if not tens_detected:
                cur_multiple *= digit[cur_num[j]]
            else: cur_multiple += digit[cur_num[j]]
        multiple.append(cur_multiple)
        cur_num = []
        cur_operand = 0
        for j in range (len(multiple)):
            cur_operand += multiple[j]
        operation.append(str(cur_operand))
        multiple = []
        final_exp = "".join(operation)
        try:
            cur_result = eval(final_exp)
            res_str = final_exp + "=" + str(cur_result)
            result.append(res_str)
            i += 1
        except:
            result.append("error")
            traceback.print_exc()
            i += 1
    l1 = result
    return l1 
################################################################################
