"""문서를 Ollama로 Embedding하여 pgvector에 저장하고 검색합니다."""

from _pgvector_store import delete_collection, similarity_search, upsert_text


COLLECTION = "rag_test"
DOCUMENTS = [
    # ("호텔 환불", "체크인 3일 전까지 취소하면 전액 환불합니다.", "hotel-refund.md"),
    # ("호텔 환불", "당일 취소는 환불되지 않습니다.", "hotel-refund.md"),
    # ("수하물", "교육용 국내선의 위탁 수하물은 15kg까지 허용합니다.", "baggage.md"),
    # ("관광지", "바다 박물관은 매주 화요일에 휴관합니다.", "attraction-hours.md"),
    # ("regal", "임차인은 최대한의 권한을 보호 받는다.", "regal.md"),
    # ("regal", "임차인은 2년간의 기간은 보호 받으며 이후 임대인과 협의 후 연장 가능합니다.", "regal.md"),
    ("12개월 미만 아기 구강관리 - 치과 검진","첫 이가 나고 6개월 이내 혹은 첫 돌이 되기 전에 치과에서 검진을 받도록 합니다.","baby-oral-care.md"),
    ("12개월 미만 아기 구강관리 - 수유 후 잇몸 관리","수유 후에는 매번 멸균된 거즈로 아이의 잇몸을 닦아줍니다.","baby-oral-care.md"),
    ("12개월 미만 아기 구강관리 - 첫 이가 난 후 양치","첫 이가 나온 후에는 즉시 부드러운 어린이용 칫솔에 물만 묻혀서 이를 닦아줍니다.","baby-oral-care.md"),
    ("12개월 미만 아기 구강관리 - 수면 중 수유 주의","아이가 잘 때 분유, 유아기 보충식, 설탕물 혹은 주스가 담긴 분유병을 물려서 재우면 안 됩니다. 모유수유 하는 아이도 젖을 물고 자는 것은 바람직하지 않습니다.","baby-oral-care.md"),
    ("12개월 미만 아기 구강관리 - 분유 온도 확인 주의","분유 온도를 체크하기 위해 어른이 분유병의 젖꼭지를 빨아 보면 안 됩니다.","baby-oral-care.md"),
]


def index_documents() -> None:
    delete_collection(COLLECTION)
    for index, (title, content, source) in enumerate(DOCUMENTS):
        upsert_text(
            collection=COLLECTION,
            title=title,
            content=content,
            source=source,
            chunk_index=index,
            metadata={"lesson": "04_rag"},
        )
        print(f"저장: {source} | {content}")


if __name__ == "__main__":
    index_documents()

    question = "아기 첫 이가 나왔는데 치과는 언제 가야 해?"
    print("\n질문:", question)
    for item in similarity_search(question, collection=COLLECTION, top_k=3):
        print(f"{item['score']:.3f} | {item['source']} | {item['content']}")
