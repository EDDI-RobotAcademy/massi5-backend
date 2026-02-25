-- PostgreSQL 18 기준 LunchRecord 최소 ERD 보강
-- 대상: lunch_records
-- 목적: 기존 테이블을 파괴하지 않고 필요한 컬럼만 안전하게 추가

BEGIN;

ALTER TABLE lunch_records
    ADD COLUMN IF NOT EXISTS photo_url VARCHAR(512),
    ADD COLUMN IF NOT EXISTS menu_name VARCHAR(100),
    ADD COLUMN IF NOT EXISTS category VARCHAR(50),
    ADD COLUMN IF NOT EXISTS meal_type VARCHAR(50),
    ADD COLUMN IF NOT EXISTS rating INTEGER;

-- 과거 데이터가 있을 때 NOT NULL 제약을 위해 기본값 백필
UPDATE lunch_records SET menu_name = COALESCE(menu_name, '미기록');
UPDATE lunch_records SET category = COALESCE(category, '미분류');
UPDATE lunch_records SET meal_type = COALESCE(meal_type, '기타');
UPDATE lunch_records SET rating = COALESCE(rating, 3);

ALTER TABLE lunch_records
    ALTER COLUMN menu_name SET NOT NULL,
    ALTER COLUMN category SET NOT NULL,
    ALTER COLUMN meal_type SET NOT NULL,
    ALTER COLUMN rating SET NOT NULL;

ALTER TABLE lunch_records
    ALTER COLUMN recorded_at SET DEFAULT CURRENT_DATE;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'ck_lunch_records_rating_range'
    ) THEN
        ALTER TABLE lunch_records
            ADD CONSTRAINT ck_lunch_records_rating_range
            CHECK (rating BETWEEN 1 AND 5);
    END IF;
END $$;

-- reports 도메인 호환을 위해 recorded_at 인덱스 보강
CREATE INDEX IF NOT EXISTS ix_lunch_records_recorded_at
    ON lunch_records (recorded_at);

-- 홈/달력 조회 최적화 (사용자 + 날짜)
CREATE INDEX IF NOT EXISTS ix_lunch_records_user_id_recorded_at
    ON lunch_records (user_id, recorded_at DESC);

COMMIT;
