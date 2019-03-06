from SDT import SDTAnalysis
from Mips import Assembler
from Production import getCPro

if __name__ == '__main__':


    inputPro = getCPro()               #获取产生式
    sdt = SDTAnalysis(inputPro)  #构造语法分析器
    sdt.buildProList()              #构造产生式表
    sdt.setStart('Program')         #设置起始符号
    sdt.delLeftRecur()              #消除左递归
    sdt.getFirst()                  #求FIRST集合
    sdt.getFollow()                 #求FOLLOW集合
    #sdt.isLL1()                    #判断是否LL1
    sdt.buildLL1Table()             #构造LL1分析表
    #sdt.showLL1Table()             #展示LL1分析表
    sdt.readFile('test.txt')        #读取待分析文件
    ERRORresult, codeList, symbolList = sdt.analyze()   #语法分析,返回要错误信息和栈信息
    if ERRORresult == '':
        mips = Assembler(symbolList, codeList)
        print (mips.generate())
    else:
        print (ERRORresult)
    








