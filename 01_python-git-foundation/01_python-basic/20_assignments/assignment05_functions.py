students = [
    {"name": "Jean", "score": 95},
    {"name": "Mina", "score": 82},
    {"name": "Jun", "score": 58},
    {"name": "Tim", "score": 95},
    {"name": "Tam", "score": 72},
    {"name": "Jain", "score": 68},
]

#  1. 학생들의 평균점수를 출력한다.
#  calculate_average(students:list)->float:

def calculate_average(students:list)->float:
    total: int = 0

    for student in students:
        total += student["score"]

    return total / len(students)

#  2. 학생의 학점(90,80,70,60)과 패스여부(60)을 출력한다.
#  print_students_status(student:dict)->tuple(str,bool):

def get_grade(score: int)-> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    return "D"

def is_passed(score:int)->bool:
    return score >= 60

def print_students_status(student: dict[str, object]) -> tuple[str, bool]:
    grade = get_grade(student["score"])
    passed = is_passed(student["score"])

    print(
        f"이름: {student['name']}, "
        f"점수: {student['score']}, "
        f"학점: {grade}, "
        f"합격: {passed}"
    )

    return grade, passed

#  3. 모든 학생의 평균 점수보다 낮은 학생들을 출력한다.
#  filter_passed_students(students:list)->tuple:

def filter_passed_students(students:list)->tuple:
    average = calculate_average(students)

    result = []

    for student in  students:
        if student["score"] <= average:
            result.append(student)

    return result

average: float = calculate_average(students)
print(f"평균 점수 : {average}")

print("\n===== 학생 상태 =====")
for student in students:
    print_students_status(student)

print("\n===== 평균보다 낮은 학생 =====")
low_students = filter_passed_students(students)

for student in low_students:
    print(f"{student['name']} : {student['score']}")