import requests
import streamlit as st

# Your Spoonacular API key
spoonacular_api_key = "97df5efa7eaa49b9862a5d7b0326e1f9"

# Spoonacular API URLs
find_by_ingredients_url = "https://api.spoonacular.com/recipes/findByIngredients"
get_recipe_info_url = "https://api.spoonacular.com/recipes/{id}/information"

def fetch_recipes(ingredients):
    params = {
        "ingredients": ",".join(ingredients),
        "number": 5,
        "apiKey": spoonacular_api_key
    }
    response = requests.get(find_by_ingredients_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching recipes: {response.status_code}")
        return []

def get_recipe_info(recipe_id):
    url = get_recipe_info_url.format(id=recipe_id)
    params = {
        "apiKey": spoonacular_api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching recipe details: {response.status_code}")
        return None

def main():
    st.title("Welcome to HealthyMeals AI! by Faradia Caisa")
    ingredients_input = st.text_input("Enter the ingredients you have (comma-separated): ")
    if ingredients_input:
        ingredients = [ingredient.strip() for ingredient in ingredients_input.split(",")]
        recipes = fetch_recipes(ingredients)
        
        if recipes:
            st.write("\nFound the following recipes:")
            for i, recipe in enumerate(recipes):
                st.write(f"{i + 1}. {recipe['title']}")
            
            choice = st.number_input("Enter the number of the recipe you want to see details for:", min_value=1, max_value=len(recipes), step=1)
            if st.button("Get Recipe Details"):
                if 1 <= choice <= len(recipes):
                    recipe_info = get_recipe_info(recipes[choice - 1]['id'])
                    if recipe_info:
                        st.write(f"\n### Detailed Recipe for {recipe_info['title']}:\n")
                        st.write("**Ingredients:**")
                        for ingredient in recipe_info['extendedIngredients']:
                            st.write(f"- {ingredient['original']}")
                        st.write("\n**Instructions:**")
                        for step in recipe_info['analyzedInstructions'][0]['steps']:
                            st.write(f"{step['number']}. {step['step']}")
                else:
                    st.error("Invalid choice!")
        else:
            st.write("No recipes found for the given ingredients.")

if __name__ == "__main__":
    main()
