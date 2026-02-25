# test_goals_table.py
from app.db.database import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()

# Check if table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='goals'")
table_exists = cursor.fetchone()

if table_exists:
    print("✅ Goals table EXISTS")
    
    # Check table schema
    cursor.execute("PRAGMA table_info(goals)")
    columns = cursor.fetchall()
    print("\nTable schema:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
    
    # Count goals
    cursor.execute("SELECT COUNT(*) FROM goals")
    count = cursor.fetchone()[0]
    print(f"\n📊 Total goals in database: {count}")
    
else:
    print("❌ Goals table DOES NOT EXIST")
    print("\nCreating goals table...")
    
    cursor.execute('''
        CREATE TABLE goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            goal_type TEXT NOT NULL,
            target_value INTEGER NOT NULL,
            current_value INTEGER DEFAULT 0,
            is_completed INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            completed_at TEXT,
            FOREIGN KEY (habit_id) REFERENCES habits (id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    print("✅ Goals table created")

conn.close()