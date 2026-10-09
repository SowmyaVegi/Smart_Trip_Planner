
def optimize_budget(
    recommended_places,
    total_budget,
    people,
    days,
    travel_cost,
    accommodation_per_person,
    food_per_person
):

    # Calculate transportation
    travel = travel_cost * people

    # Calculate accommodation
    accommodation = (
        accommodation_per_person
        * people
        * max(days - 1, 0)
    )

    # Calculate food
    food = food_per_person * people * days

    # Calculate fixed expenses
    fixed_expenses = travel + accommodation + food

    # Remaining budget
    remaining_budget = total_budget - fixed_expenses

    selected_places = []

    activity_cost = 0

    # Select places based on recommendation score
    for _, place in recommended_places.iterrows():

        place_cost = (
            place["entry_fee"] * people
            + place["local_cost"] * people
        )

        if activity_cost + place_cost <= remaining_budget:

            selected_places.append(place["place_name"])

            activity_cost += place_cost

    # Calculate final expense
    total_expense = fixed_expenses + activity_cost

    return {
        "travel": travel,
        "accommodation": accommodation,
        "food": food,
        "activities": activity_cost,
        "total": total_expense,
        "remaining": total_budget - total_expense,
        "selected_places": selected_places
    }
