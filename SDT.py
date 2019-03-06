from Production import Production, ProductionList
from Stack import MyStack
from lexicalAnalyze import LexAn
from Tree import node

'''LL1分析表类'''
class LL1Table():
    def __init__(self, Virables):
        self.table = {}
        for v in Virables:
            self.table[v] = {}

    def getPro(self, Virable, Terminal):
        return self.table[Virable][Terminal]

    def add(self, Virable, Terminal, Pro):
        self.table[Virable][Terminal] = Pro

'''语法制导翻译器类'''
class SDTAnalysis:

    def __init__(self, InputPro):
        self.InputPro = InputPro
        self.Terminals = []
        self.TerAndEnd = []
        self.Virables = []
        self.start = ''
        self.pList = ProductionList()
        self.First = {}
        self.Follow = {}
        self.string = ''
        self.ERROR = False
        self.symbolList = []
        self.offset = 0
        self.domain = 'global'
        self.funCode = {}
        self.funCode['global'] = []
        self.regCount = 7
        self.errorReason = ''
        self.tmpAddNodeList = MyStack()
        self.tmpMulNodeList = MyStack()
        self.tmpParam = MyStack()
        self.tmpSymbolIndex = MyStack()
        self.tmpCallNode = MyStack()
        self.haveReturn = {}

    '''设置起始符号'''
    def setStart(self, s):
        self.start = s

    '''构造产生式表'''
    def buildProList(self):

        for p in self.InputPro:
            self.pList.add(Production(p[0], p[1]))
            if p[0] not in self.Virables:
                self.Virables.append(p[0])

        for p in self.InputPro:
            for t in p[1]:
                if t not in self.Virables and t not in self.Terminals and t != 'NULL':
                    self.Terminals.append(t)

        self.TerAndEnd = self.Terminals.copy()
        self.TerAndEnd.append('#')

    '''消除非终结符p的直接左递归'''
    def delDirectRecur(self, p):
        v = p
        vPList = self.pList.getVirablePro(v)
        isLeftRecur = False
        for p in vPList:
            if p.left == p.right[0]:
                isLeftRecur = True
        if isLeftRecur == True:
            new_v = v + '1'
            assert new_v not in self.Virables
            self.Virables.append(new_v)
            for p in vPList:
                if p.left == p.right[0]:
                    self.pList.delete(p)
                    p.right.remove(p.left)
                    p.right.append(new_v)
                    self.pList.add(Production(new_v, p.right))
                else:
                    if p.right == ['NULL']:
                        p.right = [new_v]
                    else:
                        p.right.append(new_v)
                    self.pList.add(Production(v, p.right))
            self.pList.add(Production(new_v, ['NULL']))

    '''消除左递归'''
    def delLeftRecur(self):
        for v in self.Virables:
            self.delDirectRecur(v)



    '''求FIRST集合'''
    def getFirst(self):
        first = {}
        for v in self.Virables:
            first[v] = []
        while (True):
            Modify = False
            for p in self.pList:
                if p.right[0] in self.Terminals:
                    if p.right[0] not in first[p.left]:
                        first[p.left].append(p.right[0])
                        Modify = True
                elif p.right == ['NULL']:
                    if 'NULL' not in first[p.left]:
                        first[p.left].append('NULL')
                        Modify = True
                else:
                    for i in range(len(p.right)):
                        if p.right[i] in self.Virables and i == 0:
                            for t in first[p.right[i]]:
                                if t not in first[p.left]:
                                    first[p.left].append(t)
                                    Modify = True
                        if p.right[i] in self.Virables and i >= 1 \
                            and p.right[i-1] in self.Virables \
                            and 'NULL' in first[p.right[i-1]]:
                            for t in first[p.right[i]]:
                                if t not in first[p.left]:
                                    first[p.left].append(t)
                                    Modify = True
                            if i == len(p.right) - 1 and \
                                'NULL' in first[p.right[i]]:
                                if 'NULL' not in first[p.left]:
                                    first[p.left].append('NULL')
                                    Modify = True

                        if p.right[i] in self.Terminals and i >= 1 \
                            and p.right[i - 1] in self.Virables \
                            and 'NULL' in first[p.right[i - 1]]:
                            if p.right[i] not in first[p.left]:
                                first[p.left].append(p.right[i])
                                Modify = True
                                break
            if not Modify:
                self.First = first
                break

    '''求FOLLOW集合'''
    def getFollow(self):

        follow = {}
        for v in self.Virables:
            follow[v] = []
            if v == self.start:
                follow[v].append('#')
        while (True):
            Modify = False
            for p in self.pList:
                i = len(p.right) - 1
                rightNull = True
                while (i >= 0):
                    if p.right[i] in self.Terminals:
                        rightNull = False
                    if p.right[i] in self.Virables:
                        if rightNull == True:
                            for t in follow[p.left]:
                                if t not in follow[p.right[i]]:
                                    follow[p.right[i]].append(t)
                                    Modify = True
                        if 'NULL' not in self.First[p.right[i]]:
                            rightNull = False
                        if i < len(p.right) - 1 and p.right[i+1] in self.Terminals:
                            if p.right[i+1] not in follow[p.right[i]]:
                                follow[p.right[i]].append(p.right[i+1])
                                Modify = True
                        if i < len(p.right) - 1 and p.right[i + 1] in self.Virables:
                            for t in self.First[p.right[i+1]]:
                                if t not in follow[p.right[i]] and t != 'NULL':
                                    follow[p.right[i]].append(t)
                                    Modify = True
                    i -= 1
            if not Modify:
                self.Follow = follow
                break

    '''求产生式的FIRST集合,之前须调用getFirst()'''
    def getProFirst(self, pro):
        first = []
        i = 0
        AllNull = True
        while (i < len(pro.right)):
            if pro.right[i] in self.Terminals:
                if pro.right[i] not in first:
                    first.append(pro.right[i])
                AllNull = False
                break
            elif pro.right[i] == 'NULL':
                break
            else:
                for t in self.First[pro.right[i]]:
                    if t not in first:
                        first.append(t)
                if 'NULL' not in self.First[pro.right[i]]:
                    AllNull = False
                    break
                else:
                    i += 1
        if AllNull:
            first.append('NULL')
        return first

    '''判断是否为LL1文法'''
    def isLL1(self):
        for v in self.Virables:
            pro = self.pList.getVirablePro(v)
            for p in pro:
                for q in pro:
                    if p != q:
                        first_p = self.getProFirst(p)
                        first_q = self.getProFirst(q)
                        for t in first_p:
                            if t in first_q:
                                print (p.right,q.right)
                                return False
            if 'NULL' in self.First[v]:
                for t in self.First[v]:
                    if t in self.Follow[v]:
                        print (self.First[v])
                        print (self.Follow[v])
                        print (v)
                        return False
        return True

    '''构造LL1分析表'''
    def buildLL1Table(self):
        self.Table = LL1Table(self.Virables)
        for p in self.pList:
            first_p = self.getProFirst(p)
            for t in first_p:
                self.Table.add(p.left, t, p)
            if 'NULL' in first_p:
                for k in self.Follow[p.left]:
                    self.Table.add(p.left, k, p)

        for v in self.Virables:
            for t in self.TerAndEnd:
                if t not in self.Table.table[v]:
                    if t in self.Follow[v]:
                        self.Table.table[v][t] = 'synch'
                    else:
                        self.Table.table[v][t] = ' '

    def showLL1Table(self):
        for v in self.Virables:
            for t in self.TerAndEnd:
                if self.Table.table[v][t] == ' ' or self.Table.table[v][t] == 'synch':
                    print (v, t, self.Table.table[v][t])
                else:
                    print (v, t, self.Table.table[v][t].left, self.Table.table[v][t].right)

    '''读取待分析文件'''
    def readFile(self, fileName):
        f = open(fileName, 'r')
        self.string = f.read()
        f.close()

    '''读取待分析字符串'''
    def getString(self, s):
        self.string = s

    '''读取下一个词'''
    def advance(self):
        while (self.pointer < len(self.string)):
            if self.string[self.pointer] in ['\n', '\t', ' ']:
                if self.string[self.pointer] == '\n':
                    self.lineCounter += 1
                self.pointer += 1
            else:
                end, label = self.lex.lex_analyze(self.pointer)
                word = self.string[self.pointer:end+1]
                self.pointer = end + 1
                if label == '标识符':
                    now = '标识符'
                elif label == '数值':
                    now = 'num'
                else:
                    now = word
                return word, label, now
        return -1, -1, -1  #越界

    def genCode(self, op=None, arg1=None, arg2=None, result=None):
        code = {}
        code['addr'] = 0
        code['op'] = op
        if arg1 != None:
            code['arg1'] = arg1
        if arg2 != None:
            code['arg2'] = arg2
        code['result'] = result
        return code

    def lookUpSymbol(self, name, domain):

        for i in range(len(self.symbolList)):
            if self.symbolList[i]["idName"] == name and self.symbolList[i]["domain"] == domain:
                return i, self.symbolList[i]["domain"]
        for i in range(len(self.symbolList)):
            if self.symbolList[i]["idName"] == name:
                return i, self.symbolList[i]["domain"]
        return -1, "NULL"

    def newReg(self):
        if self.regCount == 24:
            self.regCount = 7
        self.regCount += 1
        return self.regCount

    def arrangeAddr(self):
        codeList = []
        unknownList = []
        funAddr = {}
        counter = 0
        funAddr['main'] = 100
        self.funCode['main'][-1]['result'] = 'end'
        for c in self.funCode['main']:
            c['addr'] = 100 + counter
            if c['op'][0] == 'j':
                try:
                    if c['result'][:3] == 'to_':
                        c['result'] = c['result'][3:]
                        unknownList.append(counter)
                except:
                    c['result'] = 100 + counter + c['result']
            codeList.append(c)
            counter += 1
        for key in self.funCode:
            if key != "main":
                funAddr[key] = 100 + counter
                for c in self.funCode[key]:
                    c['addr'] = 100 + counter
                    if c['op'][0] == 'j':
                        try:
                            if c['result'][:3] == 'to_':
                                c['result'] = c['result'][3:]
                                unknownList.append(counter)
                        except:
                            c['result'] = 100 + counter + c['result']
                    codeList.append(c)
                    counter += 1
        for u in unknownList:
            if codeList[u]['result'] == "end":
                codeList[u]['result'] = len(codeList)+ 100
            else:
                codeList[u]['result'] = funAddr[codeList[u]['result']]

        self.codeList = codeList

    '''语法制导翻译'''
    def analyze(self):
        self.ERROR = False
        self.head = node()
        self.head.setData('head')

        stack = MyStack()
        self.lex = LexAn(self.string)

        endNode = node()
        endNode.setData('#')
        stack.push(endNode)

        startNode = node()
        startNode.setData(self.start)
        startNode.setParent(self.head)
        self.head.addChildren(startNode)
        stack.push(startNode)

        self.pointer = 0
        self.lineCounter = 1
        word, label, now = self.advance()
        outResult = ''
        while (True):
            '''遇注释号跳过'''
            if label == '注释号':
                word, label, now = self.advance()
                continue

            '''文件读完,未完成语法分析'''
            if word == -1:
                self.errorReason += ('语法错误,line %d:' % self.lineCounter + ' 语法分析错误结束\n')
                outResult += '\n'
                break

            '''遇非法字符'''
            if label == 'ERROR':
                self.errorReason += ('语法错误,line %d:' % self.lineCounter + ' 跳过非法词%s\n'%word)
                outResult += '\n'
                #word, label, now = self.advance()
                break

            out = ('line %d: '%self.lineCounter
                        + word +','+ label)
            outResult = outResult + out.ljust(20, ' ')

            proResult = False
            topNode = stack.pop()
            X = topNode.data
            if X in self.Terminals:

                if X == now:
                    if X == "标识符":
                        topNode.parent.addAttributes('place', word)
                        if topNode.parent.parent.data == '参数':
                            symbol = {}
                            symbol['type'] = topNode.parent.parent.children[0].data
                            symbol['idName'] = word
                            symbol['label'] = 'formal'
                            symbol["domain"] = self.domain
                            code = self.genCode(op='pop', result={'reg': self.newReg()})
                            symbol['reg'] = code['result']['reg']
                            self.symbolList.append(symbol)
                            self.funCode[self.domain].append(code)
                        if topNode.parent.parent.data == '内部变量声明':
                            symbol = {}
                            symbol['type'] = topNode.parent.parent.children[0].data
                            symbol['idName'] = word
                            symbol['offset'] = self.offset
                            self.offset += 4
                            symbol['label'] = 'data'
                            symbol['domain'] = self.domain
                            self.symbolList.append(symbol)
                    if X == "num":
                        topNode.parent.addAttributes('place', {'Imme': word})
                    if X == ';':
                        if topNode.parent.data == '赋值语句':
                            symbolIndex, tag = self.lookUpSymbol(topNode.parent.children[0].attributes['place'], self.domain)
                            if symbolIndex < 0 or (tag != self.domain and tag != "global"):
                                self.errorReason += ("Line%d: 未声明的标识符 %s\n"%(self.lineCounter, topNode.parent.children[0].attributes['place']))
                                break
                            if self.symbolList[symbolIndex]['label'] == 'formal':
                                code = self.genCode(op=':=', arg1=topNode.parent.children[2].attributes['place'],
                                                    result={'reg':self.symbolList[symbolIndex]['reg']})
                            elif self.symbolList[symbolIndex]['label'] == 'data':
                                code = self.genCode(op=':=', arg1=topNode.parent.children[2].attributes['place'],
                                                    result={'symbolIndex': symbolIndex})
                            self.funCode[self.domain].append(code)

                        elif topNode.parent.data == '返回值':
                            self.haveReturn[self.domain] = True
                            if topNode.parent.children[0].data == '表达式':
                                symbolIndex, _ = self.lookUpSymbol(self.domain, self.domain)
                                if self.symbolList[symbolIndex]['type'] == 'void':
                                    self.errorReason += 'Line%d: void %s函数不能有返回值'%(self.lineCounter,
                                                                                   self.domain)
                                self.funCode[self.domain].append(self.genCode(
                                    op='push', result= topNode.parent.children[0].attributes['place']
                                ))
                            else:
                                symbolIndex, _ = self.lookUpSymbol(self.domain, self.domain)
                                if self.symbolList[symbolIndex]['type'] == 'int':
                                    self.errorReason += 'Line%d: int %s函数必须返回一个值' % (self.lineCounter,
                                                                                     self.domain)
                            self.funCode[self.domain].append(self.genCode(
                                op='jr', result='$ra'
                            ))
                            self.domain = 'global'
                    if X == ')':
                        if topNode.parent.data == 'if语句':
                            self.funCode[self.domain].append(self.genCode(
                                op='j'+topNode.parent.children[2].children[1].children[0].children[0].data,
                                arg1=topNode.parent.children[2].children[0].attributes['place'],
                                arg2=topNode.parent.children[2].children[1].children[1].attributes['place'],
                                result=2
                            ))
                            self.funCode[self.domain].append(self.genCode(
                                op='j',
                                result=0
                            ))
                            topNode.parent.attributes['false'] = len(self.funCode[self.domain])-1
                        elif topNode.parent.data == 'while语句':
                            self.funCode[self.domain].append(self.genCode(
                                op='j' + topNode.parent.children[2].children[1].children[0].children[0].data,
                                arg1=topNode.parent.children[2].children[0].attributes['place'],
                                arg2=topNode.parent.children[2].children[1].children[1].attributes['place'],
                                result=2
                            ))
                            self.funCode[self.domain].append(self.genCode(
                                op='j',
                                result=0
                            ))
                            topNode.parent.attributes['end'] = len(self.funCode[self.domain]) - 1
                        elif topNode.parent.data == '因子':
                            topNode.parent.attributes['place'] = topNode.parent.children[1].attributes['place']
                    if X == '}':
                        if topNode.parent.data == '语句块':
                            if topNode.parent.parent.data == 'if语句':
                                self.funCode[self.domain].append(self.genCode(
                                    op='j', result=0
                                ))
                                false = topNode.parent.parent.attributes['false']
                                self.funCode[self.domain][false]['result'] = len(self.funCode[self.domain]) - false
                                topNode.parent.parent.attributes['end'] = len(self.funCode[self.domain]) - 1
                            elif topNode.parent.parent.data == 'else语句':
                                end = topNode.parent.parent.parent.attributes['end']
                                self.funCode[self.domain][end]['result'] = len(self.funCode[self.domain]) - end
                            elif topNode.parent.parent.data == 'while语句':
                                end = topNode.parent.parent.attributes['end']
                                self.funCode[self.domain].append(self.genCode(
                                    op='j', result= end - len(self.funCode[self.domain]) - 1
                                ))
                                self.funCode[self.domain][end]['result'] = len(self.funCode[self.domain]) - end
                    topNode.addAttributes('lineNum', self.lineCounter)
                    word, label, now = self.advance()
                else:
                    self.errorReason += ('语法错误,line %d:'%self.lineCounter + ' 期待%s\n'%(X))
                    outResult += '\n'
                    break
            elif X == '#':
                if X == now:
                    break
                else:
                    self.errorReason += ('语法错误,line %d:'%self.lineCounter + ' 检查%s附近\n'%(word))
                    outResult += '\n'
                    break
            elif X in self.Virables and self.Table.table[X][now] not in [' ', 'synch']:
                if self.Table.table[X][now].right == ['NULL']:
                    newNode = node()
                    newNode.setParent(topNode)
                    newNode.setData('NULL')
                    topNode.addChildren(newNode)
                else:
                    k = len(self.Table.table[X][now].right) - 1
                    while (k >= 0):
                        newNode = node()
                        newNode.setParent(topNode)
                        newNode.setData(self.Table.table[X][now].right[k])
                        topNode.addChildren(newNode)
                        stack.push(newNode)
                        k -= 1
                    topNode.reverseChildren()
                if X == '变量声明':
                    symbol = {}
                    symbol['type'] = topNode.parent.parent.children[0].data
                    symbol['idName'] = topNode.parent.parent.children[1].attributes['place']
                    symbol['offset'] = self.offset
                    self.offset += 4
                    symbol['label'] = 'data'
                    symbol['domain'] = self.domain
                    self.symbolList.append(symbol)
                elif X == '函数声明' and topNode.parent.data == '声明类型':
                    symbol = {}
                    symbol['type'] = topNode.parent.parent.children[0].data
                    symbol['idName'] = topNode.parent.parent.children[1].attributes['place']
                    self.domain = symbol['idName']
                    self.funCode[self.domain] = []
                    symbol['label'] = 'func'
                    symbol['domain'] = self.domain
                    symbol['offset'] = self.offset
                    self.offset += 4
                    self.haveReturn[self.domain] = False
                    self.symbolList.append(symbol)
                elif X == '函数声明' and topNode.parent.data == '声明':
                    symbol = {}
                    symbol['type'] = topNode.parent.children[0].data
                    symbol['idName'] = topNode.parent.children[1].attributes['place']
                    self.domain = symbol['idName']
                    self.funCode[self.domain] = []
                    symbol['label'] = 'func'
                    symbol['domain'] = self.domain
                    self.haveReturn[self.domain] = True
                    self.symbolList.append(symbol)

                if X == '加法表达式':
                    self.tmpAddNodeList.push([])
                elif X == '加法表达式1':
                    top = self.tmpAddNodeList.top()
                    top.append(topNode)
                elif X == '项':
                    self.tmpMulNodeList.push([])
                elif X == '项1':
                    top = self.tmpMulNodeList.top()
                    top.append(topNode)

                if X == '加法表达式1' and topNode.children[0].data == 'NULL':
                    topAddNode = self.tmpAddNodeList.top()
                    self.tmpAddNodeList.pop()
                    if topNode.parent.data == '加法表达式':
                        topNode.parent.attributes['place'] = topNode.parent.children[0].attributes['place']
                    del topAddNode[-1]
                    for k in range(len(topAddNode)):
                        addNode = topAddNode[len(topAddNode)-k-1]
                        if  addNode.children[0].data == '-':
                            addNode.children[0].data = '减'
                            newReg = self.newReg()
                            self.funCode[self.domain].append(
                                self.genCode(op='+',arg1={'reg':0},arg2= addNode.children[1].attributes['place'],
                                             result={'reg':newReg}))
                            self.funCode[self.domain].append(
                                self.genCode(op='uminus',result={'reg':newReg})
                            )
                            addNode.children[1].attributes['place'] = {'reg': newReg}
                        if  addNode.parent.children[0].data == '-':
                            addNode.parent.children[0].data = '减'
                            newReg = self.newReg()
                            self.funCode[self.domain].append(
                                self.genCode(op='+',arg1={'reg':0},arg2= addNode.parent.children[1].attributes['place'],
                                             result={'reg':newReg}))
                            self.funCode[self.domain].append(
                                self.genCode(op='uminus',result={'reg':newReg})
                            )
                            addNode.parent.children[1].attributes['place'] = {'reg': newReg}
                        newReg = self.newReg()
                        if  addNode.parent.data == '加法表达式':
                            code = self.genCode('+',
                                                addNode.parent.children[0].attributes['place'],
                                                addNode.children[1].attributes['place'],
                                                {'reg': newReg})
                            addNode.parent.addAttributes('place', {'reg': newReg})
                        else:
                            code = self.genCode('+',
                                                addNode.parent.children[1].attributes['place'],
                                                addNode.children[1].attributes['place'],
                                                {'reg': newReg})
                            addNode.parent.children[1].addAttributes('place', {'reg': newReg})
                        self.funCode[self.domain].append(code)

                elif X == '项1' and topNode.children[0].data == 'NULL':
                    topMulNode = self.tmpMulNodeList.top()
                    self.tmpMulNodeList.pop()
                    if topNode.parent.data == '项':
                        topNode.parent.attributes['place'] = topNode.parent.children[0].attributes['place']
                    del topMulNode[-1]
                    for k in range(len(topMulNode)):
                        mulNode = topMulNode[len(topMulNode) - k - 1]
                        newReg = self.newReg()
                        if mulNode.parent.data == '项':
                            code = self.genCode(mulNode.children[0].data,
                                                mulNode.parent.children[0].attributes['place'],
                                                mulNode.children[1].attributes['place'],
                                                {'reg': newReg})
                            mulNode.parent.addAttributes('place', {'reg': newReg})
                        else:
                            code = self.genCode(mulNode.children[0].data,
                                                mulNode.parent.children[1].attributes['place'],
                                                mulNode.children[1].attributes['place'],
                                                {'reg': newReg})
                            mulNode.parent.children[1].addAttributes('place', {'reg': newReg})
                        self.funCode[self.domain].append(code)
                elif X == '表达式1' and topNode.children[0].data == 'NULL':
                    if topNode.parent.data != '表达式1':

                        topNode.parent.addAttributes('place', topNode.parent.children[0].attributes['place'])
                        if topNode.parent.parent.data == '因子':
                            topNode.parent.parent.addAttributes('place', topNode.parent.children[0].attributes['place'])
                        if topNode.parent.parent.data in ['实参列表','实参列表1']:
                            top = self.tmpParam.top()
                            top.append(topNode.parent.attributes['place'])

                elif X == 'FTYPE' and topNode.children[0].data == 'NULL':
                        symbolIndex, tag = self.lookUpSymbol(
                            topNode.parent.children[0].attributes['place'],
                            self.domain)
                        if symbolIndex < 0 or (tag != self.domain and tag != "global"):
                            self.errorReason += ("Line%d: 未声明的标识符 %s\n" % (self.lineCounter,  topNode.parent.children[0].attributes['place']))
                            break
                        if self.symbolList[symbolIndex]['label'] == 'formal':
                            topNode.parent.addAttributes('place',
                                                                {'reg': self.symbolList[symbolIndex]['reg']})
                        elif self.symbolList[symbolIndex]['label'] == 'data':
                            topNode.parent.addAttributes('place',
                                                                {'symbolIndex': symbolIndex})
                elif X == 'call':
                    symbolIndex, tag = self.lookUpSymbol(
                        topNode.parent.parent.children[0].attributes['place'],
                        self.domain)
                    if symbolIndex < 0:
                        self.errorReason += ("Line%d: 未声明的函数 %s\n" % (self.lineCounter, topNode.parent.parent.children[0].attributes['place']))
                        break
                    self.tmpSymbolIndex.push(symbolIndex)
                    self.tmpParam.push([])
                    self.tmpCallNode.push(topNode.parent.parent)

                elif X in ['实参列表','实参列表1'] and topNode.children[0].data == 'NULL':
                    paramCount = 0
                    for s in self.symbolList:
                        if s['domain'] == self.symbolList[self.tmpSymbolIndex.top()]['idName'] \
                                and s['label'] == 'formal':
                            paramCount += 1
                    topParam = self.tmpParam.top()
                    topSymbolIndex = self.tmpSymbolIndex.top()
                    self.tmpParam.pop()
                    self.tmpSymbolIndex.pop()
                    if paramCount != len(topParam):
                        self.errorReason += ("Line%d: %s函数不接受%d个参数" % (
                            self.lineCounter,
                            self.symbolList[topSymbolIndex]['idName'],
                            len(topParam)
                        ))
                        break
                    for i in range(len(topParam)):
                        self.funCode[self.domain].append(self.genCode(
                            op='push',
                            result=topParam[len(topParam)-i-1],
                        ))
                    self.funCode[self.domain].append(self.genCode(
                        op='jal',
                        result='to_%s'%(self.symbolList[topSymbolIndex]['idName']),
                    ))
                    topCallNode = self.tmpCallNode.top()
                    self.tmpCallNode.pop()
                    newReg = self.newReg()
                    self.funCode[self.domain].append(self.genCode(op='pop', result={'reg': newReg}))
                    topCallNode.addAttributes("place", {'reg': newReg})


                out = ('产生式: ' + self.Table.table[X][now].left
                              +'-->'+' '.join(self.Table.table[X][now].right))
                outResult += out.ljust(40, ' ')

                proResult = True
            else:
                if len(stack.s) == 1 or self.Table.table[X][now] == ' ':
                    newNode = node()
                    newNode.setData(X)
                    stack.push(newNode)
                    self.errorReason += ('语法错误,line %d:'%self.lineCounter + ' 跳过%s, 检查%s附近\n'%(word, word))

                    word, label, now = self.advance()
                    if word == -1:
                        self.errorReason += ('ERROR,line %d:' % self.lineCounter + ' 语法分析错误结束\n')
                        outResult += '\n'
                        break
                    break
                elif self.Table.table[X][now] == 'synch':
                    self.errorReason += ('语法错误,line %d:'%self.lineCounter + ' %s出栈, 检查%s附近\n'%(X, word))
                    break
                outResult += '\n'
                continue
            if not proResult:
                outResult += ' '.ljust(40)

            outResult += (('栈: ' + stack.show()).ljust(40)+'\n')
        if 'main' not in self.funCode.keys():
            self.errorReason += '未定义主函数'
        for key in self.funCode.keys():
            if key == 'global': continue
            self.funCode[key][0]['entry'] = key
            if self.haveReturn[key] == False:
                self.errorReason += 'int %s函数必须返回一个值'%(key)
        if self.errorReason == '':
            self.arrangeAddr()
            for c in self.codeList:
                print (c)
            return self.errorReason, self.codeList, self.symbolList
        else:
            return self.errorReason, None, None

