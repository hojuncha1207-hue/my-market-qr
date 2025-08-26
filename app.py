from flask import Flask, request, jsonify
from flask_cors import CORS # CORS 라이브러리 추가
import sqlite3
import json

app = Flask(__name__)
CORS(app) # CORS 설정: 모든 외부 요청을 허용 (테스트용)

DB_NAME = "orders.db"

# --- 데이터베이스 테이블 초기화 함수 ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # 사용자 ID를 기본 키로 하는 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            user_id TEXT PRIMARY KEY,
            order_data TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# --- API 엔드포인트: 주문 정보 생성/업데이트 ---
@app.route('/api/create-order', methods=['POST'])
def create_order():
    # 1. 프론트엔드에서 보낸 JSON 데이터 받기
    data = request.get_json()

    # 2. 데이터 유효성 검사
    if not data or 'userId' not in data or 'items' not in data:
        return jsonify({'success': False, 'message': '잘못된 데이터 형식입니다.'}), 400

    user_id = data['userId']
    # 주문 내역(items)을 JSON 문자열로 변환하여 저장
    order_data_str = json.dumps(data)

    # 3. 데이터베이스에 저장
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        # 동일한 user_id가 있으면 덮어쓰기(UPDATE), 없으면 새로 추가(INSERT)
        cursor.execute('''
            INSERT INTO orders (user_id, order_data) VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET order_data=excluded.order_data, timestamp=CURRENT_TIMESTAMP
        ''', (user_id, order_data_str))
        conn.commit()
        conn.close()
        # 4. 성공 응답 보내기
        return jsonify({'success': True, 'message': f'{user_id}의 주문이 저장되었습니다.'}), 201
    except Exception as e:
        return jsonify({'success': False, 'message': '서버 오류 발생', 'error': str(e)}), 500

if __name__ == '__main__':
    init_db() # 서버 시작 시 DB 테이블이 있는지 확인/생성
    app.run(host='0.0.0.0', port=5000, debug=True)