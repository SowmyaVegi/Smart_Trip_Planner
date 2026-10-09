import streamlit as st
import os
import pandas as pd
import plotly.express as px
from pathlib import Path

from modules.recommandations import recommend_places
from modules.itenerary import generate_itinerary
from modules.budget_optimizer import optimize_budget


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Smart Trip Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).parent

DATA_PATH = BASE_DIR / "data" / "tourist_places.csv"

IMAGE_DIR = BASE_DIR / "images"

PLACES_DIR = IMAGE_DIR / "places"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* MAIN APP */

    .stApp {
        background:
            radial-gradient(
                circle at top right,
                rgba(70, 80, 180, 0.12),
                transparent 30%
            ),
            #070b14;
        color: #ffffff;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* SIDEBAR */

    section[data-testid="stSidebar"] {
        background: #080c15;
        border-right: 1px solid #20283a;
    }


    /* HEADINGS */

    h1, h2, h3, h4 {
        color: #ffffff !important;
    }


    /* BUTTON */

    .stButton > button {
        background: linear-gradient(
            90deg,
            #5b5ff5,
            #8b5cf6
        );

        color: white;
        border: none;
        border-radius: 12px;

        font-weight: 700;
        padding: 0.7rem 1rem;

        transition: 0.2s;
    }

    .stButton > button:hover {
        transform: translateY(-2px);

        box-shadow:
            0 8px 25px
            rgba(99, 102, 241, 0.35);
    }


    /* INPUTS */

    .stTextInput input,
    .stNumberInput input {

        background: #111827 !important;
        color: white !important;

        border: 1px solid #29344a !important;

        border-radius: 10px !important;
    }


    /* SELECT BOX */

    div[data-baseweb="select"] {

        background: #111827 !important;

        border-radius: 10px !important;
    }


    /* METRICS */

    div[data-testid="stMetric"] {

        background: #0d1422;

        border: 1px solid #202b40;

        border-radius: 16px;

        padding: 18px;
    }

    div[data-testid="stMetricValue"] {

        color: #8b8df7 !important;

        font-weight: 800;
    }


    /* CONTAINERS */

    div[data-testid="stVerticalBlockBorderWrapper"] {

        background: #0c121e;

        border-color: #222d42 !important;

        border-radius: 18px;
    }


    /* IMAGE */

    img {

        border-radius: 14px;
    }


    /* DIVIDER */

    hr {

        border-color: #202a3d;
    }


    /* SMALL TEXT */

    .muted {

        color: #8c96a8;

        font-size: 14px;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    return pd.read_csv(DATA_PATH)


data = load_data()


# ============================================================
# IMAGE FUNCTIONS
# ============================================================

def get_images_for_place(place_name):

    """
    Finds all images inside:

    images/places/PLACE_NAME/
    """

    folder = PLACES_DIR / place_name

    if not folder.exists():

        return []

    images = []

    for extension in [
        "*.jpg",
        "*.jpeg",
        "*.png",
        "*.webp"
    ]:

        images.extend(
            folder.glob(extension)
        )

    return sorted(images)


def get_first_place_image(place_name):

    """
    Gets first image of a place.
    """

    images = get_images_for_place(
        place_name
    )

    if images:

        return str(images[0])


    # Fallback images

    fallback = {

        "RK Beach":
            IMAGE_DIR / "vizag.jpg",

        "Rushikonda Beach":
            IMAGE_DIR / "vizag.jpg",

        "Yarada Beach":
            IMAGE_DIR / "vizag.jpg",

        "Kailasagiri":
            IMAGE_DIR / "vizag.jpg",

        "Simhachalam Temple":
            IMAGE_DIR / "simhachalam.jpg",

        "Submarine Museum":
            IMAGE_DIR / "vizag.jpg",

        "Indira Gandhi Zoological Park":
            IMAGE_DIR / "vizag.jpg",

        "Borra Caves":
            IMAGE_DIR / "araku.jpg",

        "Araku Valley":
            IMAGE_DIR / "araku.jpg",

        "Tribal Museum":
            IMAGE_DIR / "araku.jpg",

        "Padmapuram Gardens":
            IMAGE_DIR / "araku.jpg",

        "Katiki Waterfalls":
            IMAGE_DIR / "araku.jpg"
    }


    image = fallback.get(place_name)


    if image and image.exists():

        return str(image)


    return None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ✈️ Smart Trip")

    st.caption(
        "Plan smarter • Travel better"
    )

    st.divider()

    page = st.radio(
        "MENU",
        [
            "🏠 Home",
            "🧭 Plan Trip",
            "📸 Explore Places",
            "💰 Budget",
            "🗓️ Itinerary"
        ]
    )

    st.divider()

    st.caption(
        "Data Science Project"
    )

    st.caption(
        "Smart Trip Planner"
    )


# ============================================================
# HOME
# ============================================================

if page == "🏠 Home":

    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    hero_path = IMAGE_DIR / "hero.png"

    if not hero_path.exists():

        hero_path = IMAGE_DIR / "vizag.jpg"


    if hero_path.exists():

        st.image(
            str(hero_path),
            use_container_width=True
        )

    else:

        st.info(
            "Add hero.jpg inside the images folder."
        )


    st.title(
        "✈️ SMART TRIP PLANNER"
    )

    st.markdown(
        "### Plan smarter. Travel better."
    )

    st.caption(
        "Discover destinations, get personalized recommendations, "
        "optimize your budget and create a day-wise itinerary."
    )


    st.divider()


    # --------------------------------------------------------
    # POPULAR DESTINATIONS
    # --------------------------------------------------------

    st.header(
        "🌍 Popular Destinations"
    )

    st.caption(
        "Explore some of the most popular destinations."
    )


    col1, col2, col3 = st.columns(
        3,
        gap="large"
    )


    # VIZAG

    with col1:

        with st.container(
            border=True
        ):

            image = IMAGE_DIR / "vizag.jpg"

            if image.exists():

                st.image(
                    str(image),
                    use_container_width=True
                )

            st.subheader(
                "Vizag"
            )

            st.caption(
                "🏖️ Coastal Paradise"
            )

            st.write(
                "Beaches • Nature • Adventure"
            )

            st.write(
                "⭐ 4.5"
            )


    # ARAKU

    with col2:

        with st.container(
            border=True
        ):

            image = IMAGE_DIR / "araku.jpg"

            if image.exists():

                st.image(
                    str(image),
                    use_container_width=True
                )

            st.subheader(
                "Araku Valley"
            )

            st.caption(
                "⛰️ Hill Station"
            )

            st.write(
                "Hills • Coffee • Scenic Views"
            )

            st.write(
                "⭐ 4.6"
            )


    # SIMHACHALAM

    with col3:

        with st.container(
            border=True
        ):

            image = IMAGE_DIR / "simhachalam.jpg"

            if image.exists():

                st.image(
                    str(image),
                    use_container_width=True
                )

            st.subheader(
                "Simhachalam"
            )

            st.caption(
                "🛕 Heritage & Culture"
            )

            st.write(
                "Temple • Culture • Heritage"
            )

            st.write(
                "⭐ 4.7"
            )


    st.divider()


    # --------------------------------------------------------
    # PROJECT STATISTICS
    # --------------------------------------------------------

    st.header(
        "📊 Travel Database"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Destinations",
        data["city"].nunique()
    )

    c2.metric(
        "Tourist Places",
        len(data)
    )

    c3.metric(
        "Categories",
        data["category"].nunique()
    )

    c4.metric(
        "Planner",
        "AI Powered"
    )


# ============================================================
# PLAN TRIP
# ============================================================

elif page == "🧭 Plan Trip":

    st.header(
        "🧭 Plan Your Trip"
    )

    st.caption(
        "Enter your preferences and create a personalized trip."
    )


    left, right = st.columns(
        [1.4, 1],
        gap="large"
    )


    # --------------------------------------------------------
    # TRIP DETAILS
    # --------------------------------------------------------

    with left:

        with st.container(
            border=True
        ):

            st.subheader(
                "Trip Details"
            )

            start_location = st.text_input(
                "Starting Location",
                placeholder="Example: Hyderabad"
            )


            destination = st.selectbox(
                "Destination",
                sorted(
                    data["city"].unique()
                )
            )


            col1, col2 = st.columns(2)


            with col1:

                days = st.number_input(
                    "Number of Days",
                    min_value=1,
                    max_value=15,
                    value=3
                )


            with col2:

                people = st.number_input(
                    "Number of People",
                    min_value=1,
                    max_value=20,
                    value=2
                )


            budget = st.number_input(
                "Total Budget (₹)",
                min_value=1000,
                value=20000,
                step=1000
            )


            interests = st.multiselect(
                "Interests",
                sorted(
                    data["category"].unique()
                ),
                default=["Nature"]
            )


    # --------------------------------------------------------
    # BUDGET SETTINGS
    # --------------------------------------------------------

    with right:

        with st.container(
            border=True
        ):

            st.subheader(
                "💰 Budget Settings"
            )


            travel_cost = st.number_input(
                "Travel Cost / Person",
                min_value=0,
                value=1500,
                step=100
            )


            accommodation = st.number_input(
                "Accommodation / Person / Night",
                min_value=0,
                value=1200,
                step=100
            )


            food = st.number_input(
                "Food / Person / Day",
                min_value=0,
                value=600,
                step=100
            )


            st.write("")


            plan = st.button(
                "✨ PLAN MY TRIP",
                use_container_width=True
            )


    # --------------------------------------------------------
    # GENERATE PLAN
    # --------------------------------------------------------

    if plan:

        if not start_location.strip():

            st.warning(
                "Please enter your starting location."
            )

        elif not interests:

            st.warning(
                "Please select at least one interest."
            )

        else:

            recommended = recommend_places(
                data,
                destination,
                interests
            )


            budget_result = optimize_budget(
                recommended,
                budget,
                people,
                days,
                travel_cost,
                accommodation,
                food
            )


            itinerary = generate_itinerary(
                budget_result["selected_places"],
                days
            )


            st.session_state["trip"] = {

                "start": start_location,

                "destination": destination,

                "days": days,

                "people": people,

                "budget": budget,

                "interests": interests,

                "recommended": recommended,

                "budget_result": budget_result,

                "itinerary": itinerary
            }


            st.success(
                "🎉 Your trip has been planned!"
            )


# ============================================================
# TRIP RESULTS
# ============================================================

if "trip" in st.session_state:

    trip = st.session_state["trip"]

    recommended = trip["recommended"]

    budget_result = trip["budget_result"]

    itinerary = trip["itinerary"]


    st.divider()


    st.header(
        "✨ Your Trip Overview"
    )


    m1, m2, m3, m4 = st.columns(4)


    m1.metric(
        "Budget",
        f"₹{trip['budget']:,.0f}"
    )


    m2.metric(
        "Estimated Cost",
        f"₹{budget_result['total']:,.0f}"
    )


    m3.metric(
        "Remaining",
        f"₹{budget_result['remaining']:,.0f}"
    )


    m4.metric(
        "Places",
        len(
            budget_result[
                "selected_places"
            ]
        )
    )


    # --------------------------------------------------------
    # RECOMMENDED PLACES
    # --------------------------------------------------------

    st.header(
        "📍 Recommended Places"
    )


    top_places = recommended.head(6)


    columns = st.columns(
        3,
        gap="large"
    )


    for index, (_, place) in enumerate(
        top_places.iterrows()
    ):

        with columns[
            index % 3
        ]:

            with st.container(
                border=True
            ):

                image = get_first_place_image(
                    place["place_name"]
                )


                if image:

                    st.image(
                        image,
                        use_container_width=True
                    )

                else:

                    st.info(
                        "📷 Add image"
                    )


                st.subheader(
                    place["place_name"]
                )


                st.caption(
                    f"📍 {place['city']} • "
                    f"{place['category']}"
                )


                st.write(
                    f"⭐ Popularity: "
                    f"{place['popularity']}/5"
                )


    # --------------------------------------------------------
    # PHOTO GALLERY
    # --------------------------------------------------------
# ---------- PLACE PHOTO GALLERY ----------
  
for place in places:
    place_folder = os.path.join(
        IMAGE_DIR,
        "places",
        place["folder"]
    )

if os.path.isdir(place_folder):

    photo_files = []

    for filename in os.listdir(place_folder):

        if filename.lower().endswith(
            (".jpg", ".jpeg", ".png", ".webp")
        ):
            photo_files.append(
                os.path.join(place_folder, filename)
            )

    photo_files.sort()

    if photo_files:

        st.write(f"📸 {len(photo_files)} photos")

        photo_columns = st.columns(
            min(len(photo_files), 3)
        )

        for index, photo in enumerate(photo_files):

            with photo_columns[index % len(photo_columns)]:

                st.image(
                    photo,
                    use_container_width=True
                )
    
    # BUDGET
    # --------------------------------------------------------

    st.divider()

    st.header(
        "💰 Budget Analysis"
    )


    budget_df = pd.DataFrame({

        "Category": [
            "Travel",
            "Accommodation",
            "Food",
            "Activities"
        ],

        "Amount": [
            budget_result["travel"],
            budget_result["accommodation"],
            budget_result["food"],
            budget_result["activities"]
        ]
    })


    col1, col2 = st.columns(
        2
    )


    with col1:

        fig = px.pie(
            budget_df,
            names="Category",
            values="Amount",
            hole=0.55
        )


        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        st.dataframe(
            budget_df,
            use_container_width=True,
            hide_index=True
        )


    # --------------------------------------------------------
    # ITINERARY
    # --------------------------------------------------------

    st.divider()

    st.header(
        "🗓️ Your Itinerary"
    )


    for day, schedule in itinerary.items():

        with st.container(
            border=True
        ):

            st.subheader(
                day
            )


            for slot, places in schedule.items():

                if places:

                    st.write(
                        f"**{slot}**"
                    )

                    st.write(
                        " • ".join(places)
                    )


# ============================================================
# EXPLORE PLACES
# ============================================================

elif page == "📸 Explore Places":

    st.header(
        "📸 Explore Places"
    )

    selected_city = st.selectbox(
        "Choose Destination",
        sorted(
            data["city"].unique()
        )
    )


    city_data = data[
        data["city"] == selected_city
    ]


    for start in range(
        0,
        len(city_data),
        3
    ):

        row = city_data.iloc[
            start:start + 3
        ]


        columns = st.columns(
            3,
            gap="large"
        )


        for column, (_, place) in zip(
            columns,
            row.iterrows()
        ):

            with column:

                with st.container(
                    border=True
                ):

                    image = get_first_place_image(
                        place["place_name"]
                    )


                    if image:

                        st.image(
                            image,
                            use_container_width=True
                        )

                    else:

                        st.info(
                            "📷 Image not found"
                        )


                    st.subheader(
                        place["place_name"]
                    )


                    st.caption(
                        place["category"]
                    )


                    st.write(
                        f"⭐ {place['popularity']}/5"
                    )


                    images = get_images_for_place(
                        place["place_name"]
                    )


                    if images:

                        st.caption(
                            f"📸 {len(images)} photos available"
                        )


# ============================================================
# BUDGET PAGE
# ============================================================

elif page == "💰 Budget":

    st.header(
        "💰 Budget Optimizer"
    )


    if "trip" not in st.session_state:

        st.info(
            "Create a trip first."
        )

    else:

        result = st.session_state[
            "trip"
        ]["budget_result"]


        df = pd.DataFrame({

            "Category": [
                "Travel",
                "Accommodation",
                "Food",
                "Activities"
            ],

            "Amount": [
                result["travel"],
                result["accommodation"],
                result["food"],
                result["activities"]
            ]
        })


        fig = px.bar(
            df,
            x="Category",
            y="Amount",
            text="Amount"
        )


        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# ITINERARY PAGE
# ============================================================

elif page == "🗓️ Itinerary":

    st.header(
        "🗓️ Trip Itinerary"
    )


    if "trip" not in st.session_state:

        st.info(
            "Create a trip first."
        )

    else:

        itinerary = st.session_state[
            "trip"
        ]["itinerary"]


        for day, schedule in itinerary.items():

            with st.container(
                border=True
            ):

                st.subheader(
                    day
                )


                for slot, places in schedule.items():

                    if places:

                        st.write(
                            f"**{slot}**"
                        )

                        st.write(
                            " • ".join(places)
                        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "✈️ Smart Trip Planner • "
    "Data Science Project • "
    "Plan smarter. Travel better."
)