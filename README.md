# Academic Resource Gatherer

An AI-powered tool that gathers comprehensive academic resources for any given topic.

## Features

- Gathers resources from multiple categories:
  - Blogs & Articles
  - Tutorials
  - YouTube Videos
  - Online Courses
  - Research Papers
  - Books & PDFs
  - Communities & Forums
  - Practice & Projects

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API keys:
   ```
   GROQ_API_KEY=your_groq_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

## Usage

Run the script with a topic:
```bash
python academic_agent.py "Your Topic"
```

## Requirements

- Python 3.8+
- Groq API key
- Tavily API key 