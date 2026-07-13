# 1. 학생 3명 이상의 정보를 list 안의 dict로 저장합니다.
# 2. 각 학생 dict에는 name, score, tags를 포함합니다.
# 3. tags는 list로 저장합니다.
# 4. 모든 학생의 이름과 점수를 출력합니다.
# 5. 평균 점수를 계산합니다.
# 6. 60점 이상인 학생만 출력합니다.
# 7. 전체 tags를 set으로 변환해 중복을 제거합니다.
# ```

students: list[dict[str, object]] = [
    {"name": "Alice", "score": 85, "tags": ["python", "fastapi"]},
    {"name": "Bob", "score": 72, "tags": ["python", "streamlit"]},
    {"name": "Charlie", "score": 58, "tags": ["python", "supabase"]},
]

print("== 학생 정보 ==")
for student in students:
    print(f"이름: {student['name']}, 점수: {student['score']}")

total_score = 0

for student in students:
    total_score += student["score"]
average_score = total_score / len(students)
print(f"\n평균 점수: {average_score}")

print("\n== 60점 이상인 학생 ==")
for student in students:
    if student["score"] >= 60:
        print(f"이름: {student['name']}, 점수: {student['score']}")

all_tags:set[str] = set()
for student in students:
    all_tags.update(student["tags"])

print(f"\n전체 태그: {all_tags}")