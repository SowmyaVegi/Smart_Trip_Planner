
def generate_itinerary(selected_places, days):

    itinerary = {}

    # Create empty days
    for day in range(1, days + 1):

        itinerary[f"Day {day}"] = {
            "Morning": [],
            "Afternoon": [],
            "Evening": []
        }

    # Distribute places across days
    time_slots = ["Morning", "Afternoon", "Evening"]

    for index, place in enumerate(selected_places):

        day_number = (index // 3) + 1

        slot = time_slots[index % 3]

        if day_number <= days:

            itinerary[f"Day {day_number}"][slot].append(place)

    return itinerary
