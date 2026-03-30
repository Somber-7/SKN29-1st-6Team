-- 현대자동차 FAQ 테이블
-- 출처: https://www.hyundai.com/kr/ko/faq.html

CREATE TABLE IF NOT EXISTS tbl_hyundai_faq (
    id      INT            NOT NULL AUTO_INCREMENT   COMMENT '고유 식별자',
    cat1    VARCHAR(100)   NOT NULL                  COMMENT '대분류 카테고리',
    cat2    VARCHAR(100)   NOT NULL                  COMMENT '소분류 카테고리',
    subject VARCHAR(500)   NOT NULL                  COMMENT 'FAQ 제목',
    content TEXT           NOT NULL                  COMMENT 'FAQ 내용',
    PRIMARY KEY (id)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='현대자동차 FAQ';

-- 기아자동차 FAQ 테이블
-- 출처: https://www.kia.com/kr/customer-service/center/faq

CREATE TABLE IF NOT EXISTS tbl_kia_faq (
    id      INT            NOT NULL AUTO_INCREMENT   COMMENT '고유 식별자',
    cat     VARCHAR(100)   NOT NULL                  COMMENT '카테고리',
    subject VARCHAR(500)   NOT NULL                  COMMENT 'FAQ 제목',
    content TEXT           NOT NULL                  COMMENT 'FAQ 내용',
    PRIMARY KEY (id)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='기아자동차 FAQ';

-- 제네시스 FAQ 테이블
-- 출처: https://www.genesis.com/kr/ko/support/faq/vehicle-purchase/faq_tab.html

CREATE TABLE IF NOT EXISTS tbl_genesis_faq (
    id      INT            NOT NULL AUTO_INCREMENT   COMMENT '고유 식별자',
    cat1    VARCHAR(100)   NOT NULL                  COMMENT '대분류 카테고리',
    cat2    VARCHAR(100)   NOT NULL                  COMMENT '소분류 카테고리',
    subject VARCHAR(500)   NOT NULL                  COMMENT 'FAQ 제목',
    content TEXT           NOT NULL                  COMMENT 'FAQ 내용',
    PRIMARY KEY (id)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='제네시스 FAQ';

-- KGM FAQ 테이블
-- 출처: https://www.kg-mobility.com/sr/online-center/faq

CREATE TABLE IF NOT EXISTS tbl_kgm_faq (
    id      INT            NOT NULL AUTO_INCREMENT   COMMENT '고유 식별자',
    cat     VARCHAR(100)   NOT NULL                  COMMENT '카테고리',
    subject VARCHAR(500)   NOT NULL                  COMMENT 'FAQ 제목',
    content TEXT           NOT NULL                  COMMENT 'FAQ 내용',
    PRIMARY KEY (id)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='KGM FAQ';
