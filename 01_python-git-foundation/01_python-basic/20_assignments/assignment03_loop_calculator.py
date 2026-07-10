while True:
    
    num1 = input("첫 번째 숫자를 입력하세요: ")

    if num1 == "q":
        print("프로그램을 종료합니다.")
        break

    num2 = input("두 번째 숫자를 입력하세요: ")

    operator = input("연산자를 입력하세요(+, -, *, /): ")

    num1 = float(num1)
    num2 = float(num2)

    if operator == "+":
        print(f"결과: {num1 + num2}")

    elif operator == "-":
        print(f"결과: {num1 - num2}")

    elif operator == "*":
        print(f"결과: {num1 * num2}")

    elif operator == "/":
        if num2 == 0:
            print("0으로 나눌 수 없습니다.")
            continue
        print(f"결과: {num1 / num2}")

    else:
        print("잘못된 연산자입니다.")
        continue

    print("-" * 30)