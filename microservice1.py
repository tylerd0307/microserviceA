from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Dummy storage for user workouts
workout_data = {}

def get_workout_data_in_range(user_id, start_date, end_date):
    """Fetch workout data for a user within a date range."""
    if user_id not in workout_data:
        return []
    
    return [
        entry for entry in workout_data[user_id] 
        if start_date <= datetime.fromisoformat(entry["date"]) <= end_date
    ]

@app.route('/log_workout', methods=['POST'])
def log_workout():
    """Logs new workout data for a user."""
    data = request.json
    if "user_id" not in data or "steps" not in data or "calories" not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    user_id = str(data["user_id"])  # Ensure user_id is always a string
    entry = {
        "date": datetime.now().isoformat(), 
        "steps": data["steps"],
        "calories": data["calories"],
        "workout_duration": data.get("workout_duration", 0) # Optional
    }
    
    if user_id not in workout_data:
        workout_data[user_id] = []
    
    workout_data[user_id].append(entry)
    return jsonify({"message": "Workout logged successfully!"}), 200

@app.route('/fitness_insights', methods=['GET'])
def fitness_insights():
    """Provides fitness analysis based on past workouts within a date range."""
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    
    user_id = str(user_id)  # Ensure user_id is a string
    if user_id not in workout_data:
        return jsonify({"error": "User not found"}), 400

    # Get date range from query parameters
    start_date_str = request.args.get("start_date")  # Optional
    end_date_str = request.args.get("end_date")  # Optional
    today = datetime.now()

    # Default to last 7 days if no range is provided
    if not start_date_str or not end_date_str:
        start_date = today - timedelta(days=7)
        end_date = today
    else:
        try:
            start_date = datetime.fromisoformat(start_date_str)
            end_date = datetime.fromisoformat(end_date_str)
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    # Fetch workout data within the specified range
    user_workouts = get_workout_data_in_range(user_id, start_date, end_date)

    if not user_workouts:
        return jsonify({"message": "No workout data in the selected date range."}), 200

    total_steps = sum(entry["steps"] for entry in user_workouts)
    total_calories = sum(entry["calories"] for entry in user_workouts)
    avg_steps = total_steps // len(user_workouts)

    insights = {
        "summary": f"You walked {total_steps} steps and burned {total_calories} calories in this period.",
        "suggestion": "Increase cardio by 10 minutes per day." if avg_steps < 5000 else "Maintain your current pace!"
    }

    return jsonify(insights), 200

if __name__ == '__main__':
    app.run(debug=True)
