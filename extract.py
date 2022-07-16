import os

class Extract:

    index_length = None
    file_count = None
    file_names = []
    file_sizes = []
    file_offsets = []
    save_path = './out'

    def __init__(self, inFile):
        self.inFile = inFile

    def extractArc(self):
        Extract.createOutFolder()
        Extract.getData(self)
        with open(self.inFile, "rb") as arc:
            print("Extracting...")
            for name, offset, size in zip(Extract.file_names, Extract.file_offsets, Extract.file_sizes):
                print(f"File: {name}, offset: {offset}, size: {size}")
                arc.seek(offset)
                with open(os.path.join(Extract.save_path,name), "wb") as output_arc:
                    output_arc.write(arc.read(size))
        arc.close()
        output_arc.close()
        print("Finished")
            
    def getData(self):
        with open(self.inFile, "rb") as arc:
            Extract.index_length = int.from_bytes(arc.read(4), "little")
            Extract.file_count = int.from_bytes(arc.read(4), "little")

            for i in range(Extract.file_count):
                name = arc.read(64).decode('932')
                name = name[:name.find("\x00")]
                Extract.file_names.append(name)
                size = int.from_bytes(arc.read(4), "little")
                Extract.file_sizes.append(size)
                offset = int.from_bytes(arc.read(4), "little")
                Extract.file_offsets.append(offset)
        arc.close()
    def createOutFolder():
        dir = os.path.join("out")
        if not os.path.exists(dir):
            os.mkdir(dir)