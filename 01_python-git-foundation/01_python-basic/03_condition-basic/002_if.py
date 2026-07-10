import sys
print("start")
input_data = "카드"

if(input_data != "카드1" & input_data != "카드2" ):
    sys.exit()
    
if(input_data != "카드1"):
    print("카드1 업무 진행")
else:
    print("카드2 업무 진행")


print("카드 업무 진행")

print("end")