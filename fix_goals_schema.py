"""
Fix Goals Table Schema
"""
from app.db.database import get_db_connection

print("Checking goals table schema...")

conn = get_db_connection()
cursor = conn.cursor()

# Check current schema
cursor.execute("PRAGMA table_info(goals)")
current_schema = cursor.fetchall()

print("\nCurrent schema:")
for col in current_schema:
    print(f"  {col[1]:20s} {col[2]:15s} {'NOT NULL' if col[3] else 'NULL'} {f'DEFAULT {col[4]}' if col[4] else ''}")

# Check if description column exists
has_description = any(col[1] == 'description' for col in current_schema)

if has_description:
    print("\n⚠️  Found 'description' column - this needs to be removed or made nullable")
    
    # Option 1: Drop and recreate table (RECOMMENDED)
    print("\nRecreating table with correct schema...")
    
    # Backup existing goals
    cursor.execute("SELECT * FROM goals")
    existing_goals = cursor.fetchall()
    print(f"Backing up {len(existing_goals)} existing goals...")
    
    # Drop table
    cursor.execute("DROP TABLE IF EXISTS goals")
    
    # Create correct table
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
    
    print("✅ Table recreated with correct schema")
    
    # Restore goals (if any)
    if existing_goals:
        print(f"Restoring {len(existing_goals)} goals...")
        for goal in existing_goals:
            try:
                cursor.execute('''
                    INSERT INTO goals (id, habit_id, goal_type, target_value, current_value, is_completed, created_at, completed_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    goal[0],  # id
                    goal[1],  # habit_id
                    goal[2] if goal[2] else '30_day_streak',  # goal_type
                    goal[3] if goal[3] else 30,  # target_value
                    goal[4] if len(goal) > 4 else 0,  # current_value
                    goal[5] if len(goal) > 5 else 0,  # is_completed
                    goal[6] if len(goal) > 6 else '2026-01-01 00:00:00',  # created_at
                    goal[7] if len(goal) > 7 else None  # completed_at
                ))
            except Exception as e:
                print(f"  Warning: Could not restore goal {goal[0]}: {e}")
        
        print("✅ Goals restored")
else:
    print("\n✅ Schema is correct (no description column)")

conn.commit()
conn.close()

print("\nDone! Schema is now correct.")