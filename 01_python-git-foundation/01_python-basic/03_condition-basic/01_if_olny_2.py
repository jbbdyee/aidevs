# 숫자를 입력 받는다 (1~10)
# 숫자가 아니면 프로그램 종료
# 숫자이면 출력

print("start")
input_str = input("1~10사이의 숫자를 입력하세요: ")
input_number = int(input_str)
if(input_number < 1 | input_number > 10):
    sys.exit()
# if(input_number < 10):
#     sys.exit()

print(f"입력 숫자는 {input_number}")
print("end")

