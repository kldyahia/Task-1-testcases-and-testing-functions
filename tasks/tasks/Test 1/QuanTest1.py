def QuantizationTest1(file_name,Your_EncodedValues,Your_QuantizedValues):
    expectedEncodedValues=[]
    expectedQuantizedValues=[]
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L=line.strip()
            if len(L.split(' '))==2:
                L=line.split(' ')
                V2=str(L[0])
                V3=float(L[1])
                expectedEncodedValues.append(V2)
                expectedQuantizedValues.append(V3)
                line = f.readline()
            else:
                break
    if( (len(Your_EncodedValues)!=len(expectedEncodedValues)) or (len(Your_QuantizedValues)!=len(expectedQuantizedValues))):
        print("QuantizationTest1 Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_EncodedValues)):
        if(Your_EncodedValues[i]!=expectedEncodedValues[i]):
            print(f"QuantizationTest1 Test case failed on sample: {i}, your EncodedValues: {Your_EncodedValues[i]} have different EncodedValues from the expected one: {expectedEncodedValues[i]}") 
            return
    for i in range(len(expectedQuantizedValues)):
        if abs(Your_QuantizedValues[i] - expectedQuantizedValues[i]) < 0.01:
            continue
        else:
            print("QuantizationTest1 Test case failed, your QuantizedValues have different values from the expected one") 
            return
    print("QuantizationTest1 Test case passed successfully")



import sys
sys.path.append("../../../") 

from functions import QuantizeSignal, ReadSignalFile

i1,s1= ReadSignalFile("Quan1_input.txt")
indices, quantized_samples, quantization_errors, encoded_signals, interval_indices, bits_count, levels= QuantizeSignal((i1,s1),3)
QuantizationTest1("Quan1_out.txt",encoded_signals,quantized_samples)