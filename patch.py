import os, re, repack

class Patch:
    
    flag_count = 0
    info_offsets = {} #flag name, flag offset in info.bin, flag offset in script, new flag offset in script
    
    def __init__(self, path):
        self.infobin = open(path, "r+b")

    def patch_info(self):
        print("Patching 00_info.bin...")
        Patch.get_flag_info(self)
        for key in Patch.info_offsets.keys():
            for i in Patch.info_offsets[key]:
                offset = repack.Repack.convert2Hex(i[3])
                offset = repack.Repack.big2SmallEndian(offset)
                self.infobin.seek(i[1])
                self.infobin.write(offset)
        print("Finished")

    def get_flag_info(self):
        flag_name = ""
        flag_file = ""
        flag_position = 0
        flag_offset = 0

        Patch.flag_count = int.from_bytes(self.infobin.read(8), "little")

        for i in range(Patch.flag_count):
            flag_name = self.infobin.read(64).decode('932')
            flag_name = flag_name[:flag_name.find("\x00")]
            flag_file = self.infobin.read(64).decode('932')
            flag_file = flag_file[:flag_file.find("\x00")]
            flag_position = self.infobin.tell()
            flag_offset = int.from_bytes(self.infobin.read(8), "little")

            if flag_file in Patch.info_offsets.keys():
                Patch.info_offsets[flag_file].append([flag_name, flag_position, flag_offset])
            else:
                Patch.info_offsets[flag_file] = [[flag_name, flag_position, flag_offset]]
        Patch.open_script(self)

    def open_script(self):
        for key in Patch.info_offsets.keys():
            for i in Patch.info_offsets[key]:
                with open(os.path.join("out", key), "rb") as script_file:
                    label = bytes("<label "+ i[0] + ">", '932')
                    find = re.search(label, script_file.read())
                    offset = find.start()
                    if find:
                        i.append(offset)
                    else:
                        print("ERROR: label not found")
                script_file.close()