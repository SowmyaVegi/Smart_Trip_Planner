# ✈️ Smart Trip Planner

### Plan Smarter. Travel Better.

Smart Trip Planner is a Python-based travel planning application that helps users explore tourist destinations, discover recommended places, estimate trip expenses, and organize their travel itinerary based on their preferences and budget.

## 🌟 Features

- **Destination Explorer:** Explore tourist destinations such as Visakhapatnam (Vizag) and Araku Valley.
- **Personalized Recommendations:** Recommend tourist attractions based on user-selected interests.
- **Budget Optimization:** Estimate travel, accommodation, food, and activity expenses.
- **Itinerary Generation:** Organize recommended places into a day-wise travel plan.
- **Place Photo Galleries:** View multiple photos of tourist attractions.
- **Interactive Dashboard:** Explore trip information through charts and visual summaries.

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Plotly

## 📂 Project Structure

```text
Smart_Trip_Planner/
├── app.py
├── requirements.txt
├── data/
│   └── tourist_places.csv
├── modules/
│   ├── recommendation.py
│   ├── itinerary.py
│   └── budget_optimizer.py
├── images/
│   ├── hero.jpg
│   ├── vizag.jpg
│   ├── araku.jpg
│   └── places/
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/Smart-Trip-Planner.git
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Open the project folder

```bash
cd Smart-Trip-Planner
```

### 3. Create a virtual environment (optional)

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install the required libraries

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

The application should open in your browser.

## 🧠 How It Works

1. Enter the starting location and choose a destination.
2. Select the number of travel days and people.
3. Enter your estimated budget and interests.
4. Generate personalized place recommendations.
5. Review the estimated expenses and suggested itinerary.
6. Explore photos of tourist attractions.

## 📊 Data Science Concepts

- Content-based recommendation using text features and cosine similarity.
- Ranking tourist attractions using recommendation scores.
- Budget-based selection of tourist activities.
- Data visualization for estimated trip expenses.

## 🚀 Future Enhancements

- Live weather information.
- Interactive maps and route planning.
- Real-time hotel and transportation prices.
- More destinations and tourist attractions.
- Downloadable PDF trip itineraries.
- Machine learning-based travel recommendations.

## 👩‍💻 Author

**Vegi Likitha Sai Sowmya**

B.Tech — Computer Science / AI & ML

## 📄 Disclaimer

Trip costs and destination information are estimates for planning purposes. Actual prices, travel times, and availability may vary. Ensure that images used in the project are appropriately licensed and credited.

---

*Smart Trip Planner — Plan Smarter. Travel Better.*