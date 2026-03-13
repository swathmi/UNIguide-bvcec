from app import db, app
from sqlalchemy import text

with app.app_context():
    conn = db.engine.connect()
    try:
        conn.execute(text("ALTER TABLE user ADD COLUMN reset_token VARCHAR(255)"))
        print('Added column: reset_token')
    except Exception as e:
        print('reset_token:', e)
    try:
        conn.execute(text("ALTER TABLE user ADD COLUMN reset_token_expiry DATETIME"))
        print('Added column: reset_token_expiry')
    except Exception as e:
        print('reset_token_expiry:', e)
    conn.close()
