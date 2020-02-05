#using lists to contain lines\headlines( both index and contents)
def extract_key_value(inputFiles,outPutFile):
    f = open(outPutFile,"a") #"vector_with*.txt"
    f.write("Sequence number, image name 1, image name 2, Chip number X, Chip number Y , On chip coordinate X, On chip coordinate Y, Stage X coordinate, Stage Y coordinate, Measurement Method,  Characteristic value\n")
    for inputFile in inputFiles: 
        mylines=[]      #all the lines

        with open(inputFile, "rt") as myfile: #"20190717_100846_CU_PAI1_TGAP_FINAL_DTGAP.msr"
        # read the file
                for myline in myfile: # everyline in the file
                        mylines.append(myline.rstrip('\n')) # contain everyline (as an element) in the list mylines

        i=0 # to contain the number of the picture
        

        for j in range (len(mylines) ): # for each line
                if ('$' in mylines[j]): # if the line contains $, then it indicates the start of a new picture
                        elements = []
                        items = mylines[j].split()
                        elements.append(i)
                        elements.append("null")
                        elements.append("null")
                        k = j + 1
                        templine=[]    #context in file
                        templine.append(mylines[j].rstrip('\n'))
                        while(k < len(mylines) and '$' not in mylines[k]):
                                templine.append(mylines[k].rstrip('\n'))
                                k += 1
                        for l in range (len(templine)):
                                if("&no_of_mp_image" in templine[l]):
                                        namesLine = templine[l].split()
                                        num = int(namesLine[1])
                                        if(num == 0):
                                                break
                                        for nameNum in range(num):
                                                elements[nameNum + 1] = templine[l + nameNum + 1].split()[2]
                                        
                        i = i+1                 
                        for l in range(3):
                                elements.append(items[4 + l])
                        elements.append(items[8])
                        for element in elements:
                                f.write(str(element) + ',')
                        if(items[len(items) - 1] != '*'):
                                f.write(items[len(items) - 1] + '\n')
                        else:
                                f.write('0' + '\n')









