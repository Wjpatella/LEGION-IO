import requests
from bs4 import BeautifulSoup

class TrendData:
    def __init__(self, query):
        self.query = query
        self.publication_count = None

    def fetch_trend_data(self):
        url = f"https://scholar.google.com/scholar?q={self.query}"
        response = requests.get(url)
        if response.status_code == 200:
            self.process_trend_data(response.content)
        else:
            print(f"Failed to retrieve trend data: {response.status_code}")

    def process_trend_data(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        #The publication count is in the secound div with class name 'gs_ab_mdw'
        result_summaries = soup.find_all('div', {'class': 'gs_ab_mdw'})
        if len(result_summaries) > 1:
            #The second div is the one containg the search count
            result_summary = result_summaries[1]
            self.publication_count = self.extract_publication_count(result_summary.text)

    def extract_publication_count(self, text):
        print(f"Extracting from text: {text}") # Debugging line
        # Example: "About 12,345 results (0.34 sec)"
        if "About" in text and "results" in text:
            words = text.split()
            for i, word in enumerate(words):
                if word.lower() == "about" and i + 1 < len(words):
                    # The next word should be the number of results
                    count_str = words[i + 1].replace(",", "")
                if count_str.isdigit():
                    return int(count_str)
        return None
    def get_publication_count(self):
        return self.publication_count
'''
# Example usage:
query = "machine learning"
trend_data = TrendData(query)
trend_data.fetch_trend_data()
print(f"Publication count for '{query}': {trend_data.get_publication_count()}")
'''