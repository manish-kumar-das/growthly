# test_create_goal.py
from app.services.goal_service import get_goal_service
from app.services.habit_service import get_habit_service

print("\n" + "="*60)
print("TESTING GOAL CREATION")
print("="*60)

# Get services
goal_service = get_goal_service()
habit_service = get_habit_service()

# Get first habit
habits = habit_service.get_all_habits()
print(f"\nAvailable habits: {len(habits)}")

if not habits:
    print("❌ No habits found! Create a habit first.")
    exit()

habit = habits[0]
print(f"Using habit: {habit.name} (ID: {habit.id})")

# Try to create goal
print("\nAttempting to create goal...")
goal_id = goal_service.create_goal(
    habit_id=habit.id,
    goal_type='30_day_streak',
    target_value=30
)

if goal_id:
    print(f"\n✅ SUCCESS! Goal created with ID: {goal_id}")
    
    # Verify
    goals = goal_service.get_all_goals(include_completed=True)
    print(f"Total goals in database: {len(goals)}")
    
    for g in goals:
        print(f"\n  Goal #{g.id}:")
        print(f"    Habit ID: {g.habit_id}")
        print(f"    Type: {g.goal_type}")
        print(f"    Target: {g.target_value}")
        print(f"    Created: {g.created_at}")
else:
    print("\n❌ FAILED! Goal was not created")

print("\n" + "="*60 + "\n")