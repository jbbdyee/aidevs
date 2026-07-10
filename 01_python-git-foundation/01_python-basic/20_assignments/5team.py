while True:
    print("\n===== 게임 캐릭터 생성 =====")

    name = input("이름을 입력하세요(q: 종료): ")

    if name == "q":
        print("프로그램을 종료합니다.")
        break

    print("\n직업을 선택하세요.")
    print("1. 전사")
    print("2. 마법사")
    print("3. 궁수")

    job_number = input("직업번호를 입력하세요: ")

    match job_number:
        case "1":
            job = "전사"
        case "2":
            job = "마법사"
        case "3":
            job = "궁수"
        case _:
            print("잘못된 직업 번호입니다.")
            continue

    level = int(input("레벨을 입력하세요: "))

    if level < 1:
        print("레벨은 1 이상이어야 합니다.")
        continue
    elif level <= 10:
        level_message = "초보 모험가"
    elif level <= 30:
        level_message = "숙련된 모험가"
    else:
        level_message = "전설의 모험가"

    print("\n===== 캐릭터 정보 =====")
    print(f"이름: {name}")
    print(f"직업: {job}")
    print(f"레벨: {level}")
    print(f"등급: {level_message}")

    restart = input("\n새 캐릭터를 만들까요? (y/n): ")

    if restart == "n":
        print("프로그램을 종료합니다.")
        break
    elif restart != "y":
        print("잘못 입력했지만 처음으로 돌아갑니다.")
        continue