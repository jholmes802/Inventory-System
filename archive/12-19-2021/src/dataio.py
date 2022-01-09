import sys
import os


class FileError(Exception):
    def __init__(self, message: object) -> None:
        self.message = message
        super().__init__(self.message)
class ItemError(Exception):
    def __init__(self, message: object) -> None:
        self.message = message
        super().__init__(self.message)


class item():
    def __init__(self,part_number, name, qty):
        self.name:str = name
        self.part_num:str = part_number
        self.qty:int = qty
    def __str__(self) -> str:
        return "Part Name: " + self.name + " Part Num: " + str( self.part_num) + " Qty: " + str(self.qty)

items = list[item]

class DataIO():
    def getFields(fpath:str)-> list[str]:
        fhand = open(fpath, "r")
        fread = fhand.readlines().rstrip("\n").split(",")
        for f in fread:
            print(f)
        fhand.close()
    def extractall(fpath:str)-> items:
        if not fpath.endswith('.csv'):
            print("Invalid File Path")
            raise FileError("Provided file: '"+fpath+"' is not a '.csv' file type")
        if not os.path.exists(fpath):
            print("File not found")
            raise FileError("Listed file could not be found at:", fpath)
        fhand = open(fpath, 'r')
        fread = fhand.readlines()
        if len(fread) <= 1:
            fhand.close()
            raise FileError("Provided file is too small. Has No headerline.")
        else:
            results = []
            for line in fread[1:]:
                line = line.rstrip("\n").split(',')
                if len(line) != 3:
                    continue
                i = item(line[0], line[1], line[2])
                results.append(i)
            fhand.close()
            return results

    def part_num_check(its:items)->bool:
        if len(its) <= 1:
            print("Passes rule 1")
            return True
        keys:list[str] = []
        for i in its:
            if i.part_num in keys:
                print("failed rule 2")
                return False
            else:
                keys.append(i.part_num)
        print("Passes rule 3")
        return True
            
    def new_item(fpath:str, new_item:item, check:bool = True)-> None:
        if check:
            its:items = DataIO.extractall(fpath)
            its.append(new_item)
            if not DataIO.part_num_check(its):
                raise ItemError("Item Already Exsits")
            else:
                nline = new_item.part_num + "," + new_item.name + "," + new_item.qty+ "\n"
                fhand = open(fpath,'a')
                fhand.write(nline)
                fhand.close()
        else:
            nline = new_item.part_num + "," + new_item.name + "," + new_item.qty+ "\n"
            fhand = open(fpath,'a')
            fhand.write(nline)
            fhand.close()