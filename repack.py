import os
import binascii

class Repack:

    index_length = ""
    file_count = 0
    file_offsets = []
    data_offsets = []
    file_names = []
    file_sizes = []

    def __init__(self, originalArc, inFolder, outFile):
        self.inFolder = inFolder
        self.outFile = outFile
        self.originalArc = originalArc

    def repackArc(self):
        print("Repacking...")
        count = 0
        Repack.getIndexLenAndNumOfFiles(self)
        Repack.getFileNames(self)
        Repack.getFileSizes(self)
        with open(self.outFile, "wb") as output_file:
            output_file.write(Repack.index_length + Repack.file_count)
            for i in range(int.from_bytes(Repack.file_count, "little")): 
                output_file.write(Repack.file_names[count])
                output_file.write(Repack.file_sizes[count])
                currentPos = output_file.tell()
                Repack.file_offsets.append(currentPos)
                output_file.write(b"\x00\x00\x00\x00") #place holder for offsets
                count += 1
            for file in os.listdir(self.inFolder):
                currentPos= output_file.tell()
                Repack.data_offsets.append(currentPos)
                output_file.write(Repack.writeFileData(self, file))
            Repack.setOffsets(self)
        output_file.close()
        print("Finished")

    def getIndexLenAndNumOfFiles(self): #probably a better way to do this through calculation but these two values should stay the same and I'm too lazy to write it all
        with open(self.originalArc, "rb") as arc:
            Repack.index_length = arc.read(4)
            Repack.file_count = arc.read(4)
        self.originalArc = None
            
    def setOffsets(self):
        counter = 0
        with open(self.outFile, "r+b") as file:
            for i in Repack.file_offsets:
                file.seek(i)
                n = Repack.convert2Hex(Repack.data_offsets[counter])
                n = Repack.big2SmallEndian(n)
                file.write(n)
                counter += 1
        self.outFile = None

    def writeFileData(self, file):
        with open(os.path.join(self.inFolder, file), 'rb') as open_file:
            data = open_file.read()
            open_file.close()
            return data
            

    def getFileCount(self):
        Repack.file_count = 0
        for file in os.listdir(self.inFolder):
            Repack.file_count += 1
        print(Repack.file_count)
        Repack.file_count = Repack.convert2Hex(Repack.file_count)
        file_count_bytes = bytes.fromhex(Repack.file_count)
        file_count_bytes = Repack.getPadding(4, b"\x00", file_count_bytes)
        return file_count_bytes
    
    def getFileNames(self):
        for file in os.listdir(self.inFolder):
            filename = bytes(file, 'cp932') + b"\x00"
            filename = Repack.addPadding(64, b"\xfe", filename)
            Repack.file_names.append(filename)
        return Repack.file_names


    def getFileSizes(self):
        for file in os.listdir(self.inFolder):
            size = os.path.getsize(self.inFolder + "\\" + file)
            size = Repack.convert2Hex(size)
            size = Repack.big2SmallEndian(size)
            size = Repack.addPadding(4, b"\x00", size)
            Repack.file_sizes.append(size)

    def convert2Hex(n):
        x = '%x' % (n,)
        return ('0' * (len(x) % 2)) + x

    def big2SmallEndian(n):
        b = bytearray.fromhex(n)
        b.reverse()
        s = ''.join(format(x, "02x") for x in b)
        b = binascii.unhexlify(s)
        return b

    def addPadding(max, byte, string):
        padding = max - len(string)
        for i in range(padding):
            string = string + byte
        return string
    