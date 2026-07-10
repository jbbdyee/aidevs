import sys

print("start")

while True:
    print("Menu Start")
    cmd = input("nput cmd..")
    print(f"입력하신 정보는 {cmd}")
    if (cmd == "q"):
        print("bye")
        sys.exit()
print("end")