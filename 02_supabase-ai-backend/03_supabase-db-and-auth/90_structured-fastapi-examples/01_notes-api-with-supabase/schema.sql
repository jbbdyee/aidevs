-- 01_notes-api-with-supabase 예제에서 사용하는 테이블입니다.
--
-- 이 예제의 목표:
-- 1. FastAPI 구조를 router/schema/service로 나눕니다.
-- 2. service 계층에서 Supabase 테이블을 CRUD합니다.
-- 3. 인증/RLS 없이 가장 단순한 DB 연결 흐름부터 확인합니다.

create table if not exists ex90_notes (
  -- id는 각 노트를 구분하는 고유값입니다.
  -- gen_random_uuid()는 Supabase/PostgreSQL이 자동으로 uuid를 만들어 줍니다.
  id uuid primary key default gen_random_uuid(),

  -- title/content는 사용자가 입력하는 필수 텍스트입니다.
  title text not null,
  content text not null,

  -- created_at은 row가 만들어진 시간을 자동 기록합니다.
  created_at timestamp not null default now()
);

-- Sample notes (id and created_at use their default values).
insert into ex90_notes (title, content)
values
  ('FastAPI 시작하기', 'FastAPI 프로젝트의 기본 구조와 실행 방법을 정리합니다.'),
  ('Supabase 연결 설정', '환경 변수로 Supabase URL과 API 키를 안전하게 관리합니다.'),
  ('노트 생성 API', 'POST 요청을 사용해 새로운 노트를 생성하는 방법을 기록합니다.'),
  ('노트 목록 조회', '저장된 노트 목록을 최신순으로 조회하는 기능을 구현합니다.'),
  ('노트 상세 조회', 'UUID를 이용해 특정 노트 한 건을 조회합니다.'),
  ('노트 수정 API', 'PATCH 요청으로 제목과 내용을 선택적으로 수정합니다.'),
  ('노트 삭제 API', 'DELETE 요청으로 더 이상 필요하지 않은 노트를 삭제합니다.'),
  ('예외 처리', '존재하지 않는 노트를 요청했을 때 404 응답을 반환합니다.'),
  ('입력값 검증', '빈 제목이나 잘못된 요청 데이터가 저장되지 않도록 검증합니다.'),
  ('API 테스트', 'Swagger UI와 자동화 테스트를 이용해 CRUD 동작을 확인합니다.');
