# 1. 이름을 입력받습니다.
# 2. 나이를 입력받습니다.
# 3. 관심 있는 기술을 입력받습니다.
# 4. 하루 학습 가능 시간을 입력받습니다.
# 5. 입력받은 값을 변수에 저장합니다.
# 6. 나이는 int로 변환합니다.
# 7. 하루 학습 가능 시간은 float으로 변환합니다.
# 8. type()으로 각 변수의 자료형을 출력합니다.
# 9. f-string으로 자기소개 문장을 출력합니다.

print("Start")
name:str = input("이름을 입력하세요: ")
age_str = int(input("나이를 입력하세요: "))
print(f"이름(name) 나이{age-10}")
interest = input("관심 있는 기술을 입력하세요: ")
study_time = input("하루 학습 가능 시간을 입력하세요: ")
age = int(age)
study_time = float(study_time)
print(type(name), type(age), type(interest), type(study_time))
print(f"뿌뿌")
print("End")


