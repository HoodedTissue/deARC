import extract, repack, patch, sys

def main():
    help = "deARC\n\nUSAGE:\n  py main.py verb <inputs ...>\nVERBS:\n  extract\textract .arc. Inputs: <infile>\n  repack\trepack .arc file. Inputs: <originalarc> <infolder> <outfile>\n  patch\t\tpatch 00_info.bin (must do before repacking script.arc). Inputs: <infile>\nEXAMPLE:\n  py main.py repack script.arc script_files script_new.arc"
    inFile = ""
    inFolder = ""
    outFile = ""

    try:
        if len(sys.argv) == 1:
            print(help)
        else:
            option = sys.argv[1]
            if option.lower() == 'repack':
                inFile = sys.argv[2]
                inFolder = sys.argv[3]
                outFile = sys.argv[4]
                repack.Repack(inFile, inFolder, outFile).repackArc()
            elif option.lower() == 'extract':
                inFile = sys.argv[2]
                extract.Extract(inFile).extractArc()
            elif option.lower() == 'patch':
                inFile = sys.argv[2]
                patch.Patch(inFile).patch_info()
            else:
                print(help)
    except:
        raise

if __name__ == "__main__":
    main()