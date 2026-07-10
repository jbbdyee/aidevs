import sys

print("start")

while True:
    print("Menu Start")
    cmd = input("nput cmd..")
    print(f"입력하신 정보는 {cmd}")
    if (cmd == "1"):
        print("1번 메뉴를 선택하셨습니다.")
        
    if (cmd == "q"):
        print("bye")
        break

print("end")