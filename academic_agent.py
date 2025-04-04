import os
import json
from typing import Dict, List
from dotenv import load_dotenv
import groq
from tavily import TavilyClient
import requests
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

class AcademicResourceGatherer:
    def __init__(self):
        # Initialize Groq client with the latest API version
        self.groq_client = groq.Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )
        self.tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        
    def search_tavily(self, query: str) -> List[Dict]:
        """Search for resources using Tavily API"""
        search_query = f"{query} academic resources tutorials courses papers"
        response = self.tavily_client.search(
            query=search_query,
            search_depth="advanced",
            include_answer=True,
            include_domains=["github.com", "arxiv.org", "youtube.com", "coursera.org", 
                           "reddit.com", "stackoverflow.com", "medium.com", "towardsdatascience.com"]
        )
        return response.get("results", [])

    def analyze_with_groq(self, search_results: List[Dict], topic: str) -> Dict:
        """Analyze search results using Groq LLM"""
        # Prepare context for Groq
        context = f"Topic: {topic}\n\nSearch Results:\n"
        for result in search_results[:10]:  # Limit to top 10 results
            context += f"- {result.get('title', '')}: {result.get('url', '')}\n"
        
        # Create prompt for Groq
        prompt = f"""Analyze these search results for the topic '{topic}' and categorize them into the following categories:
        1. Blogs & Articles
        2. Tutorials
        3. YouTube Videos
        4. Online Courses
        5. Research Papers
        6. Books & PDFs
        7. Communities & Forums
        8. Practice & Projects

        For each category, provide a list of relevant resources with their titles and URLs.
        Format the response as a JSON object with these categories as keys.

        Search Results:
        {context}"""

        # Get response from Groq
        completion = self.groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that categorizes academic resources."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        try:
            # Parse the response as JSON
            response_text = completion.choices[0].message.content
            # Extract JSON from the response (in case there's additional text)
            json_str = response_text[response_text.find("{"):response_text.rfind("}")+1]
            return json.loads(json_str)
        except Exception as e:
            print(f"Error parsing Groq response: {e}")
            return {}

    def answer_question(self, topic: str, question: str) -> str:
        """Answer questions about the topic using Groq"""
        # Search for relevant information
        search_query = f"{topic} {question}"
        response = self.tavily_client.search(
            query=search_query,
            search_depth="advanced",
            include_answer=True,
            include_domains=["github.com", "arxiv.org", "youtube.com", "coursera.org", 
                           "reddit.com", "stackoverflow.com", "medium.com", "towardsdatascience.com"]
        )
        
        # Prepare context from search results
        context = f"Topic: {topic}\nQuestion: {question}\n\nRelevant Information:\n"
        for result in response.get("results", [])[:5]:
            context += f"- {result.get('title', '')}: {result.get('url', '')}\n"
        
        # Create prompt for Groq
        prompt = f"""Based on the following information about {topic}, please answer this question: {question}

        Provide a clear, concise, and informative answer. Include relevant details and examples when possible.
        If you're not sure about something, please say so.

        Context:
        {context}"""

        # Get response from Groq
        completion = self.groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful educational assistant that provides clear and accurate answers."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        return completion.choices[0].message.content

    def gather_resources(self, topic: str) -> Dict:
        """Main method to gather and analyze resources"""
        print(f"Searching for resources about: {topic}")
        
        # Search for resources
        search_results = self.search_tavily(topic)
        
        # Analyze results with Groq
        categorized_resources = self.analyze_with_groq(search_results, topic)
        
        return categorized_resources

def main():
    # Get topic from command line argument
    import sys
    if len(sys.argv) < 2:
        print("Please provide a topic as a command line argument")
        print("Usage: python academic_agent.py 'Your Topic'")
        sys.exit(1)
    
    topic = sys.argv[1]
    
    # Initialize and run the gatherer
    gatherer = AcademicResourceGatherer()
    resources = gatherer.gather_resources(topic)
    
    # Print results in a formatted way
    print("\n📚 Academic Resources for:", topic)
    print("=" * 50)
    
    for category, items in resources.items():
        print(f"\n📌 {category}:")
        if isinstance(items, list):
            for item in items:
                print(f"  • {item}")
        else:
            print(f"  • {items}")

if __name__ == "__main__":
    main() 