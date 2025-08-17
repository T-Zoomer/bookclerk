import json
import urllib.parse
from django.conf import settings
from openai import OpenAI
from typing import List, Dict


class BookRecommendationService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def generate_amazon_affiliate_link(self, title: str, author: str) -> str:
        """
        Generate an Amazon affiliate link for a book.
        Uses search URL with affiliate tag.
        """
        # Clean and format the search query for better results
        # Remove special characters that might interfere with search
        clean_title = title.replace(" & ", " and ").replace("&", "and")
        clean_author = author.strip()
        
        # Use both title and author for more precise search
        search_query = f'"{clean_title}" "{clean_author}"'
        
        # Properly encode the entire query
        encoded_query = urllib.parse.quote_plus(search_query)
        
        print(f"AMAZON SEARCH QUERY: {search_query}")
        print(f"ENCODED QUERY: {encoded_query}")
        
        # Amazon search URL with affiliate tag
        amazon_link = (
            f"{settings.AMAZON_BASE_URL}/s?"
            f"k={encoded_query}&"
            f"tag={settings.AMAZON_AFFILIATE_TAG}"
        )
        
        print(f"AMAZON LINK: {amazon_link}")
        print("=" * 50)
        
        return amazon_link
    
    def get_book_recommendations(self, user_preferences: str) -> List[Dict[str, str]]:
        """
        Get book recommendations from OpenAI based on user preferences.
        Returns a list of dictionaries with title, author, description, and reason.
        """
        prompt = f"""
        Based on these user preferences: "{user_preferences}"
        
        Please recommend 5 books that would be a great fit. For each book, provide:
        - Title
        - Author
        - Brief description (2-3 sentences)
        - Reason why this book matches the user's preferences (1-2 sentences)
        
        Return the response as a JSON array with objects containing "title", "author", "description", and "reason" fields.
        Make sure the JSON is valid and parseable.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a knowledgeable book recommendation expert. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content.strip()
            
            # Print the raw LLM output to console for debugging
            print("=" * 50)
            print("LLM RAW OUTPUT:")
            print(content)
            print("=" * 50)
            
            # Try to extract JSON from the response
            if content.startswith('```json'):
                content = content.replace('```json', '').replace('```', '').strip()
            elif content.startswith('```'):
                content = content.replace('```', '').strip()
            
            recommendations = json.loads(content)
            
            # Handle different JSON structures
            if isinstance(recommendations, dict):
                if 'books' in recommendations:
                    # Handle {"books": [...]} structure
                    recommendations = recommendations['books']
                elif 'recommendations' in recommendations:
                    # Handle {"recommendations": [...]} structure
                    recommendations = recommendations['recommendations']
                else:
                    # Single recommendation object
                    recommendations = [recommendations]
            elif not isinstance(recommendations, list):
                # Convert single item to list
                recommendations = [recommendations]
            
            return recommendations
            
        except json.JSONDecodeError as e:
            print(f"JSON DECODE ERROR: {e}")
            print(f"FAILED TO PARSE: {repr(content)}")
            print("=" * 50)
            # Raise the error to be handled by the view
            raise Exception("Failed to parse AI response. Please try again.")
        except Exception as e:
            print(f"GENERAL ERROR: {e}")
            print("=" * 50)
            # Re-raise with a user-friendly message
            raise Exception("Unable to get recommendations at this time. Please try again later.")
    
