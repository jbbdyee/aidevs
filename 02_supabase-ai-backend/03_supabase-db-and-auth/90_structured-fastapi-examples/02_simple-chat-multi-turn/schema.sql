-- conversation_id별 멀티턴 대화 기록을 저장합니다.
create table if not exists ex90_multi_turn_chat_logs (
  id uuid primary key default gen_random_uuid(),
  conversation_id uuid not null,
  user_message text not null,
  assistant_message text not null,
  model text not null,
  created_at timestamptz not null default now()
);

-- create index if not exists ex90_multi_turn_chat_logs_conversation_created_idx
-- on ex90_multi_turn_chat_logs (conversation_id, created_at);

-- conversation_id 는 사용자의 채팅창 값? 이게 있어야 넌 지니야 -> 웅 난 지니야 할수있음
-- 아이디로 하면 전체내용을 다 보내야하니까