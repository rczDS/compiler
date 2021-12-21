import sys
# from translate import Translator


def main():
    cmdStr = input("please input input-filename (and output-filename): ")
    filename = cmdStr.split(' ')
    if len(filename) < 1 or len(filename) > 2:
        print("wrong")
        return
    else:
        # translator = Translator()
        if len(filename) == 1:
            inputFilename = filename[0]
            outputFilename = '.'.join(inputFilename.split('.')[:-1]) + '.py'
            print(inputFilename+' '+outputFilename)
            # translator.translate(inputFilename, outputFilename)
        else:
            inputFilename = filename[0]
            outputFilename = filename[1]
            if '.' in outputFilename and outputFilename.split('.')[-1] != 'py':
                print('please rename the outputfile')
            else:
                print(inputFilename+' '+outputFilename)
                # translator.translate(inputFilename, outputFilename)


if __name__ == '__main__':
    main()
