# 청냠리 MVP

## 구조
- web/ → 프론트엔드 (index.html)
- server/ → 백엔드 (Express + Neon DB)
- GitHub → Render → Neon

## 실행 방법 (로컬)
```bash
cd server
npm install
npm start
```

## 배포
1. GitHub에 전체 업로드
2. Render 연결 → server/ 배포
3. Render 환경변수에 DATABASE_URL 추가 (Neon DB 연결)
