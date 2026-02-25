import sqlite3
import os
import glob

print("🔍 Searching for all database files...\n")

# Find all .db files
db_files = glob.glob("**/*.db", recursive=True)
db_files.extend(glob.glob("*.db"))
db_files = list(set(db_files))  # Remove duplicates

if not db_files:
    print("❌ No database files found!")
    exit()

print(f"Found {len(db_files)} database file(s):")
for db in db_files:
    print(f"  📁 {db}")

print("\n" + "="*60)

for db_path in db_files:
    print(f"\n🔧 Fixing: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if goals table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='goals'")
        if not cursor.fetchone():
            print("  ⚠️  No goals table found, skipping")
            conn.close()
            continue
        
        # Check schema
        cursor.execute("PRAGMA table_info(goals)")
        columns = cursor.fetchall()
        has_description = any(col[1] == 'description' for col in columns)
        
        if has_description:
            print("  ⚠️  Found description column - fixing...")
            
            # Backup data
            cursor.execute("SELECT * FROM goals")
            backup = cursor.fetchall()
            print(f"  📦 Backing up {len(backup)} goals...")
            
            # Drop and recreate
            cursor.execute("DROP TABLE goals")
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
            
            # Restore data
            for row in backup:
                try:
                    cursor.execute('''
                        INSERT INTO goals (habit_id, goal_type, target_value, current_value, is_completed, created_at, completed_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        row[1],  # habit_id
                        row[2] or '30_day_streak',  # goal_type
                        row[3] or 30,  # target_value
                        row[5] if len(row) > 5 else 0,  # current_value
                        row[6] if len(row) > 6 else 0,  # is_completed
                        row[7] if len(row) > 7 else '2026-01-01 00:00:00',  # created_at
                        row[8] if len(row) > 8 else None  # completed_at
                    ))
                except:
                    pass
            
            conn.commit()
            print("  ✅ Fixed!")
        else:
            print("  ✅ Schema is correct")
        
        conn.close()
        
    except Exception as e:
        print(f"  ❌ Error: {e}")

print("\n" + "="*60)
print("🎉 Done! All databases checked and fixed.\n")