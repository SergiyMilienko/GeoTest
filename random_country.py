from countries_lists import popular_countries, less_popular_countries, least_popular_countries, all_countries, africa, asia, europe, north_america, oceania, south_america
from flask import session
import random

def get_random_country():
    difficulty = session.get("difficulty")
    guessed_countries = session.get("guessed_countries", [])
    
    if difficulty == "easy":
        available_countries = popular_countries
        session["max_score"] = len(popular_countries)
    elif difficulty == "medium":
        available_countries = less_popular_countries
        session["max_score"] = len(less_popular_countries)
    elif difficulty == "hard":
        available_countries = least_popular_countries
        session["max_score"] = len(least_popular_countries)
    elif difficulty == "all":
        available_countries = all_countries
        session["max_score"] = len(all_countries)
    elif difficulty == "europe":
        available_countries = europe
        session["max_score"] = len(europe)
    elif difficulty == "asia":
        available_countries = asia
        session["max_score"] = len(asia)
    elif difficulty == "oceania":
        available_countries = oceania
        session["max_score"] = len(oceania)
    elif difficulty == "north_america":
        available_countries = north_america
        session["max_score"] = len(north_america) 
    elif difficulty == "south_america":
        available_countries = south_america
        session["max_score"] = len(south_america)
    elif difficulty == "africa":
        available_countries = africa
        session["max_score"] = len(africa)


    available_countries = [country for country in available_countries if country not in guessed_countries]

    if available_countries:
        return random.choice(available_countries)
    else: 
        session["guessed_countries"] = []
        return get_random_country()