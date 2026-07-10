menu = input("메뉴 번호를 입력하세요(1~3): ")

match menu:
    case "1":
        score = int(input("점수를 입력하세요: "))

        if score >= 90:
            print("A")
        elif score >= 80:
            print("B")
        elif score >= 70:
            print("C")
        else:
            print("D")

    case "2":
        number = int(input("숫자를 입력하세요: "))

        if number > 0:
            print("양수입니다.")
        elif number == 0:
            print("0입니다.")
        else:
            print("음수입니다.")

    case "3":
        role = input("역할을 입력하세요(admin, member, guest): ")

        match role:
            case "admin":
                print("관리자입니다.")
            case "member":
                print("회원입니다.")
            case "guest":
                print("손님입니다.")
            case _:
                print("알 수 없는 역할입니다.")
    
    case _:
        print("알 수 없는 메뉴입니다.")

            
            

        
    


