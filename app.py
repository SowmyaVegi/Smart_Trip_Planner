
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Smart Trip Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "tourist_places.csv"
IMAGE_DIR = BASE_DIR / "images"
PLACES_DIR = IMAGE_DIR / "places"

SUPPORTED_IMAGES = {".jpg", ".jpeg", ".png", ".webp"}


# ============================================================
# 3. CUSTOM DESIGN
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background: #070b14;
        color: #f8fafc;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 1.8rem;
        padding-bottom: 3rem;
    }

    section[data-testid="stSidebar"] {
        background: #0a101c;
        border-right: 1px solid #253047;
    }

    h1, h2, h3, h4 {
        color: #f8fafc !important;
    }

    p, label, .stCaption {
        color: #cbd5e1;
    }

    div[data-testid="stMetric"] {
        background: #101827;
        border: 1px solid #27344a;
        border-radius: 15px;
        padding: 16px;
    }

    div[data-testid="stMetricValue"] {
        color: #a5b4fc !important;
    }

    .stButton > button {
        background: linear-gradient(90deg, #5558f2, #8b5cf6);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        min-height: 42px;
    }

    .stButton > button:hover {
        color: white;
        border: 1px solid #a5b4fc;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #0d1421;
        border-color: #263249;
        border-radius: 16px;
    }

    hr {
        border-color: #263249;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 4. LOAD AND VALIDATE DATA
# ============================================================

@st.cache_data
def load_data(csv_path):
    df = pd.read_csv(csv_path)

    required_columns = [
        "place_name",
        "city",
        "category",
        "entry_fee",
        "visit_hours",
        "popularity",
        "local_cost",
    ]

    missing = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            "Missing CSV columns: " + ", ".join(missing)
        )

    for column in [
        "entry_fee",
        "visit_hours",
        "popularity",
        "local_cost",
    ]:
        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        ).fillna(0)

    df["place_name"] = df["place_name"].astype(str).str.strip()
    df["city"] = df["city"].astype(str).str.strip()
    df["category"] = df["category"].astype(str).str.strip()

    return df


if not DATA_FILE.exists():
    st.error(f"Dataset not found: {DATA_FILE}")
    st.info(
        "Place tourist_places.csv inside the project's data folder."
    )
    st.stop()

try:
    data = load_data(str(DATA_FILE))
except Exception as error:
    st.error(f"Could not load the dataset: {error}")
    st.stop()

if data.empty:
    st.error("Your tourist_places.csv file contains no places.")
    st.stop()


# ============================================================
# 5. IMAGE HELPERS
# ============================================================

def find_images(folder):
    """Return image files in a folder, in a stable order."""

    if not folder.is_dir():
        return []

    return sorted(
        [
            path
            for path in folder.iterdir()
            if path.is_file()
            and path.suffix.lower() in SUPPORTED_IMAGES
        ],
        key=lambda path: path.name.lower(),
    )


def place_folder_name(place_name):
    """Use the place's exact name as its image folder name."""

    return PLACES_DIR / str(place_name).strip()


def get_place_images(place_name):
    """Find all photos belonging to a tourist place."""

    return find_images(place_folder_name(place_name))


def get_cover_image():
    """Choose the cover photo in the preferred order."""

    for filename in [
        "cover.jpg",
        "cover.png",
        "hero.jpg",
        "hero.png",
        "vizag.jpg",
        "araku.jpg",
    ]:
        candidate = IMAGE_DIR / filename

        if candidate.is_file():
            return candidate

    return None


def get_destination_image(destination):
    """Get a destination image or fall back to its first place photo."""

    destination_files = {
        "vizag": ["vizag.jpg", "vizag.png"],
        "araku": ["araku.jpg", "araku.png"],
    }

    for filename in destination_files.get(
        str(destination).lower(), []
    ):
        candidate = IMAGE_DIR / filename

        if candidate.is_file():
            return candidate

    destination_places = data[
        data["city"].str.lower() == str(destination).lower()
    ]

    for place_name in destination_places["place_name"]:
        photos = get_place_images(place_name)

        if photos:
            return photos[0]

    return None


def show_place_gallery(place_name):
    """Display all available photos for one place."""

    photos = get_place_images(place_name)

    if not photos:
        st.info(
            f"No photos found for {place_name}. "
            f"Add images to images/places/{place_name}/"
        )
        return

    st.caption(f"📸 {len(photos)} photo(s)")

    # Display photos in rows of up to three.
    for start in range(0, len(photos), 3):
        photo_row = photos[start:start + 3]
        columns = st.columns(len(photo_row))

        for column, photo in zip(columns, photo_row):
            with column:
                st.image(
                    str(photo),
                    caption=photo.name,
                    use_container_width=True,
                )


# ============================================================
# 6. RECOMMENDATION LOGIC
# ============================================================

def recommend_places(destination, interests):
    """Rank places by matching interests and popularity."""

    result = data[
        data["city"].str.lower() == destination.lower()
    ].copy()

    if result.empty:
        return result

    selected = {interest.lower() for interest in interests}

    result["interest_match"] = result["category"].str.lower().apply(
        lambda category: 1.0 if category in selected else 0.0
    )

    result["recommendation_score"] = (
        0.75 * result["interest_match"]
        + 0.25 * (result["popularity"].clip(0, 5) / 5)
    )

    return result.sort_values(
        ["recommendation_score", "popularity"],
        ascending=False,
    )


# ============================================================
# 7. BUDGET OPTIMIZER
# ============================================================

def optimize_budget(
    recommendations,
    budget,
    people,
    days,
    travel_per_person,
    hotel_per_person,
    food_per_person,
):
    travel = travel_per_person * people
    accommodation = hotel_per_person * people * max(days - 1, 0)
    food = food_per_person * people * days

    fixed_cost = travel + accommodation + food
    remaining = budget - fixed_cost

    selected_places = []
    activity_cost = 0

    if remaining >= 0:
        for _, place in recommendations.iterrows():
            cost = (
                max(0, place["entry_fee"])
                + max(0, place["local_cost"])
            ) * people

            if activity_cost + cost <= remaining:
                selected_places.append(place["place_name"])
                activity_cost += cost

    total = fixed_cost + activity_cost

    return {
        "travel": travel,
        "accommodation": accommodation,
        "food": food,
        "activities": activity_cost,
        "total": total,
        "remaining": budget - total,
        "selected_places": selected_places,
    }


# ============================================================
# 8. DAY-WISE ITINERARY
# ============================================================

def create_itinerary(place_names, days):
    slots = ["Morning", "Afternoon", "Evening"]

    itinerary = {
        f"Day {day}": {
            slot: [] for slot in slots
        }
        for day in range(1, days + 1)
    }

    for index, place_name in enumerate(place_names):
        day_index = index // 3

        if day_index >= days:
            break

        slot = slots[index % 3]
        itinerary[f"Day {day_index + 1}"][slot].append(
            place_name
        )

    return itinerary


# ============================================================
# 9. SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:
    st.markdown("# ✈️ Smart Trip")
    st.caption("Plan smarter. Travel better.")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Home",
            "Plan Your Trip",
            "Explore Places",
            "Budget Analysis",
            "Itinerary",
        ],
    )

    st.divider()
    st.caption("Python • Streamlit • Data Science")


# ============================================================
# 10. HOME PAGE
# ============================================================

if page == "Home":
    cover = get_cover_image()

    if cover:
        st.image(
            str(cover),
            use_container_width=True,
        )
    else:
        st.info(
            "Add a cover image such as images/cover.jpg "
            "to display a large travel photo here."
        )

    st.title("✈️ SMART TRIP PLANNER")
    st.subheader("Plan smarter. Travel better.")

    st.write(
        "Discover destinations, explore tourist attractions, "
        "estimate your expenses, and organize your next journey."
    )

    st.divider()
    st.header("🌍 Popular Destinations")

    destinations = list(data["city"].drop_duplicates())
    columns = st.columns(min(3, len(destinations)))

    for index, destination in enumerate(destinations):
        with columns[index % len(columns)]:
            with st.container(border=True):
                image = get_destination_image(destination)

                if image:
                    st.image(
                        str(image),
                        use_container_width=True,
                    )
                else:
                    st.caption("📷 Add a destination image")

                st.subheader(destination)

                place_count = len(
                    data[data["city"] == destination]
                )

                st.caption(f"{place_count} places to explore")

    st.divider()
    st.header("📊 Your Travel Database")

    col1, col2, col3 = st.columns(3)

    col1.metric("Destinations", data["city"].nunique())
    col2.metric("Tourist Places", len(data))
    col3.metric("Categories", data["category"].nunique())

    st.info(
        "Select 'Plan Your Trip' in the sidebar to create a trip."
    )


# ============================================================
# 11. PLAN YOUR TRIP PAGE
# ============================================================

elif page == "Plan Your Trip":
    st.title("🧭 Plan Your Trip")
    st.caption("Choose your destination, interests, and budget.")

    with st.form("trip_form"):
        left, right = st.columns(2)

        with left:
            start_location = st.text_input(
                "Starting Location",
                placeholder="Example: Hyderabad",
            )

            destination = st.selectbox(
                "Destination",
                sorted(data["city"].unique()),
            )

            days = st.number_input(
                "Number of Days",
                min_value=1,
                max_value=30,
                value=3,
            )

            people = st.number_input(
                "Number of People",
                min_value=1,
                max_value=50,
                value=2,
            )

            budget = st.number_input(
                "Total Budget (₹)",
                min_value=1000,
                max_value=10000000,
                value=20000,
                step=1000,
            )

            interests = st.multiselect(
                "Your Interests",
                sorted(data["category"].unique()),
                default=[data["category"].iloc[0]],
            )

        with right:
            st.subheader("💰 Estimated Expenses")

            travel_cost = st.number_input(
                "Travel cost per person (₹)",
                min_value=0,
                value=1500,
                step=100,
            )

            hotel_cost = st.number_input(
                "Accommodation per person per night (₹)",
                min_value=0,
                value=1200,
                step=100,
            )

            food_cost = st.number_input(
                "Food per person per day (₹)",
                min_value=0,
                value=600,
                step=100,
            )

        submitted = st.form_submit_button(
            "✨ PLAN MY TRIP",
            use_container_width=True,
        )

    if submitted:
        if not start_location.strip():
            st.error("Please enter your starting location.")

        elif not interests:
            st.error("Please select at least one interest.")

        else:
            recommendations = recommend_places(
                destination,
                interests,
            )

            budget_result = optimize_budget(
                recommendations,
                budget,
                people,
                days,
                travel_cost,
                hotel_cost,
                food_cost,
            )

            itinerary = create_itinerary(
                budget_result["selected_places"],
                int(days),
            )

            st.session_state["trip"] = {
                "start_location": start_location,
                "destination": destination,
                "days": int(days),
                "people": int(people),
                "budget": budget,
                "interests": interests,
                "recommendations": recommendations,
                "budget_result": budget_result,
                "itinerary": itinerary,
            }

            st.success(
                "Trip plan created! Open Budget Analysis, "
                "Itinerary, or Explore Places from the sidebar."
            )


# ============================================================
# 12. EXPLORE PLACES PAGE
# ============================================================

elif page == "Explore Places":
    st.title("📸 Explore Places")
    st.caption("Explore destinations and view their photo galleries.")

    destination = st.selectbox(
        "Choose a destination",
        sorted(data["city"].unique()),
    )

    destination_data = data[
        data["city"].str.lower() == destination.lower()
    ]

    for start in range(0, len(destination_data), 3):
        row_data = destination_data.iloc[start:start + 3]
        columns = st.columns(len(row_data))

        for column, (_, place) in zip(
            columns,
            row_data.iterrows(),
        ):
            with column:
                with st.container(border=True):
                    photos = get_place_images(place["place_name"])

                    if photos:
                        st.image(
                            str(photos[0]),
                            use_container_width=True,
                        )
                    else:
                        st.info("📷 Image not found")

                    st.subheader(place["place_name"])
                    st.caption(f"📍 {place['city']}")
                    st.write(f"Category: {place['category']}")
                    st.write(f"Popularity: {place['popularity']}/5")

                    if photos:
                        st.caption(f"{len(photos)} photos available")

                    if st.button(
                        "View Photos",
                        key=f"gallery_{place['place_name']}",
                        use_container_width=True,
                    ):
                        st.session_state["selected_gallery"] = (
                            place["place_name"]
                        )

    selected_gallery = st.session_state.get("selected_gallery")

    if selected_gallery:
        st.divider()
        st.header(f"📷 {selected_gallery} Photo Gallery")
        show_place_gallery(selected_gallery)


# ============================================================
# 13. BUDGET ANALYSIS PAGE
# ============================================================

elif page == "Budget Analysis":
    st.title("💰 Budget Analysis")

    trip = st.session_state.get("trip")

    if not trip:
        st.info("Create a trip first using 'Plan Your Trip'.")
    else:
        result = trip["budget_result"]

        st.caption(
            f"Destination: {trip['destination']} • "
            f"{trip['days']} day(s) • "
            f"{trip['people']} traveller(s)"
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Budget", f"₹{trip['budget']:,.0f}")
        col2.metric("Estimated Cost", f"₹{result['total']:,.0f}")
        col3.metric("Remaining", f"₹{result['remaining']:,.0f}")

        if result["remaining"] < 0:
            st.warning("The estimated trip cost exceeds your budget.")
        else:
            st.success("The estimated trip fits within your budget.")

        budget_df = pd.DataFrame({
            "Category": [
                "Travel",
                "Accommodation",
                "Food",
                "Activities",
            ],
            "Amount": [
                result["travel"],
                result["accommodation"],
                result["food"],
                result["activities"],
            ],
        })

        left, right = st.columns(2)

        with left:
            fig = px.pie(
                budget_df,
                names="Category",
                values="Amount",
                hole=0.5,
                title="Expense Distribution",
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white",
            )

            st.plotly_chart(fig, use_container_width=True)

        with right:
            st.subheader("Expense Breakdown")
            st.dataframe(
                budget_df,
                use_container_width=True,
                hide_index=True,
            )

        st.caption(
            "Costs are estimates based on the values entered "
            "and the sample dataset, not live prices."
        )


# ============================================================
# 14. ITINERARY PAGE
# ============================================================

elif page == "Itinerary":
    st.title("🗓️ Your Trip Itinerary")

    trip = st.session_state.get("trip")

    if not trip:
        st.info("Create a trip first using 'Plan Your Trip'.")
    else:
        st.caption(
            f"{trip['start_location']} → {trip['destination']}"
        )

        itinerary = trip["itinerary"]

        for day, schedule in itinerary.items():
            with st.container(border=True):
                st.subheader(day)

                for slot, places in schedule.items():
                    st.markdown(f"**{slot}**")

                    if places:
                        for place_name in places:
                            st.write(f"📍 {place_name}")
                    else:
                        st.caption("No place scheduled")


# ============================================================
# 15. FOOTER
# ============================================================

st.divider()
st.caption("✈️ Smart Trip Planner | Plan smarter. Travel better.")
