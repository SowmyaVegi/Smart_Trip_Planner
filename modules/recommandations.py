
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def recommend_places(data, destination, interests):

    # Filter places based on destination
    city_data = data[
        data["city"].str.lower() == destination.lower()
    ].copy()

    if city_data.empty:
        return city_data

    # Convert categories into lowercase
    city_data["category"] = (
        city_data["category"].str.lower()
    )

    # Convert user interests into lowercase
    user_preferences = " ".join(interests).lower()

    # Prepare text documents
    documents = city_data["category"].tolist()

    documents.append(user_preferences)

    # Convert text into numerical vectors
    vectorizer = CountVectorizer()

    vectors = vectorizer.fit_transform(documents)

    # Calculate cosine similarity
    similarity = cosine_similarity(
        vectors[-1],
        vectors[:-1]
    )[0]

    # Store similarity scores
    city_data["similarity_score"] = similarity

    # Calculate final recommendation score
    city_data["recommendation_score"] = (
        0.8 * similarity
        + 0.2 * (city_data["popularity"] / 5)
    )

    # Sort by recommendation score
    city_data = city_data.sort_values(
        by="recommendation_score",
        ascending=False
    )

    return city_data
