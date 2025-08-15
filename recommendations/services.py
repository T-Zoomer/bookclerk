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
            f"i=stripbooks&"
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
            
            print("CLEANED CONTENT FOR JSON PARSING:")
            print(repr(content))
            print("=" * 50)
            
            recommendations = json.loads(content)
            
            print("PARSED RECOMMENDATIONS:")
            print(recommendations)
            print("=" * 50)
            
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
            
            print("FINAL RECOMMENDATIONS LIST:")
            print(recommendations)
            print("=" * 50)
            
            return recommendations
            
        except json.JSONDecodeError as e:
            print(f"JSON DECODE ERROR: {e}")
            print(f"FAILED TO PARSE: {repr(content)}")
            print("=" * 50)
            # Fallback recommendations if JSON parsing fails
            return self._get_fallback_recommendations()
        except Exception as e:
            print(f"GENERAL ERROR: {e}")
            print("=" * 50)
            return self._get_fallback_recommendations()
    
    def _get_fallback_recommendations(self) -> List[Dict[str, str]]:
        """Fallback recommendations in case of API errors."""
        return [
            {
                "title": "The Midnight Library",
                "author": "Matt Haig",
                "description": "A philosophical novel about a magical library between life and death where the protagonist explores different versions of her life.",
                "reason": "A thought-provoking book that appeals to readers who enjoy contemplating life's possibilities and philosophical themes."
            },
            {
                "title": "Educated",
                "author": "Tara Westover",
                "description": "A memoir about a woman who grows up in a survivalist family in rural Idaho and eventually earns a PhD from Cambridge University.",
                "reason": "An inspiring true story that showcases the power of education and personal transformation."
            }
        ]