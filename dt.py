import pandas
import math
from functools import reduce

ROUND_NUM = 3
NODE_NAME = 'A'


class Field:
    saveField = []
    dataInit = None
    entropyInit = 0

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.attr = {}
        self.value = []
        self.jsonData = {}
        self.nodeEntropy = {}
        self.infGain = float()
        Field.saveField += [self]

    def getLengthTable(self):
        return len(self.value)

    def fillData(self, data):
        for idx, attr in enumerate(data):
            self.value += [{idx: attr}]
            if not (attr in self.attr):
                self.attr[attr] = 1
            else:
                self.attr[attr] += 1

    def setDataInit(self):
        Field.dataInit = self
        self.calEntropyInit()
        print("\n\n\n\n\nGoi '"+NODE_NAME+"' la tap du lieu huan luyen ban dau voi '" +
              str(self.getLengthTable()) + "' phan tu")
        print("Bao gom:", [(name + ": " + str(Field.dataInit.attr[name]))
              for name in Field.dataInit.attr])
        print("tinh tung gia tri cua phan tu (value) trong H('"+NODE_NAME+"') theo cong thuc sau roi cong lai")
        print("value = - gtpt/tongpt * log2(gtpt/tongpt)")
        print("\nH(EntropyInit) = H('"+NODE_NAME+"') = ", Field.entropyInit)
        print("\n\n\n\n")

    def calEntropyInit(self):
        data = Field.dataInit
        res = 0
        total = reduce(lambda x, y: x+data.attr[y], data.attr, 0) * 1.0
        for name in data.attr:
            res += (-data.attr[name]/total)*math.log2(data.attr[name]/total)
        Field.entropyInit = round(res, ROUND_NUM)

    def calculateEntropy(self):
        datamap = list(
            map(lambda x, y: (x, y), self.value, Field.dataInit.value))
        data_json = {}
        for x in self.attr:
            data_json[x] = {}
            for y in Field.dataInit.attr:
                data_json[x][y] = 0
            data_json[x]['_tong_'] = 0
        for idx, val in enumerate(datamap):
            attr = val[0][idx]
            typ = val[1][idx]
            if typ in data_json[attr]:
                data_json[attr][typ] += 1
            else:
                data_json[attr][typ] = 1
            data_json[attr]['_tong_'] += 1
        # print(data_json)
        for subAttr in data_json:
            # print(data_json[subAttr])
            res = 0
            for subInitAttr in data_json[subAttr]:
                if subInitAttr != '_tong_':
                    ps = data_json[subAttr][subInitAttr] / \
                        data_json[subAttr]['_tong_'] * 1.0
                    res += 0 if ps == 0 else (-ps)*math.log2(ps)
            self.nodeEntropy[subAttr] = round(res, ROUND_NUM)
        self.jsonData = data_json

    def calInformationGain(self):
        value = 0.0
        value = reduce(
            lambda y, x: y+-self.nodeEntropy[x]*self.attr[x]/self.getLengthTable(), self.attr, 0.0)
        # value += ((-self.nodeEntropy[x]*self.attr[x]/self.getLengthTable()) for x in self.attr)
        res = Field.entropyInit + value
        self.infGain = round(res, ROUND_NUM)
        # print("H(", self.name, ") = ", self.infGain)

    @classmethod
    def printAll(cls):
        for x in cls.saveField:
            print(
                "\n====================================================================")
            print('x.id\t=', x.id)
            print('x.name\t=', x.name)
            print('x.attr\t=', x.attr)
            print('x.value\t=', x.value)
            print("\n-----\n")
            print(x.jsonData)
            print(
                "\nXet thuoc tinh: '"+str(x.name)+"'\nNeu chia node '"+NODE_NAME+"' dua tren '"+str(x.name)+"' theo cong thuc tren thi ta co:\n")
            print([("H(" + str(x.name) + "=" + str(value) + ") = " + str(x.nodeEntropy[value]))
                  for value in x.nodeEntropy])
            print("H(", x.name, ") = ", x.infGain)


def main():
    dataCSV = pandas.read_csv('data.csv')
    field_list = []
    headName = list(dataCSV.columns)
    for id, name in enumerate(headName):
        element = Field(id, name)
        element.fillData(dataCSV[name])
        field_list.append(element)
    field_list[len(field_list)-1].setDataInit()
    for field in field_list:
        field.calculateEntropy()
        field.calInformationGain()
    Field.printAll()


if __name__ == '__main__':
    main()
