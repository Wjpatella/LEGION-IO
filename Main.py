import requests #import requests: Imports the requests library, which is used for making HTTP requests. In this script, it is used to send a request to Google Scholar.
from bs4 import BeautifulSoup #from bs4 import BeautifulSoup: Imports the BeautifulSoup class from the bs4 (Beautiful Soup 4) library, which is used for parsing HTML and XML documents. It helps to extract data from the HTML response.
import tkinter as tk #import tkinter as tk: Imports the tkinter library, which is used for creating graphical user interfaces (GUIs) in Python. It is aliased as tk for convenience.
from tkinter import scrolledtext #from tkinter import scrolledtext: Imports the scrolledtext module from tkinter, which provides a text widget with a vertical scrollbar for displaying large amounts of text.

def search_scholar(query):
    # Define the URL with the search query
    url = f"https://scholar.google.com/scholar?q={query}"
    
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return
    
    # Parse the response content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all the result elements
    results = soup.find_all('div', class_='gs_r gs_or gs_scl')
    
    # Extract and print the relevant information
    formatted_results = []
    for result in results:
        title = result.find('h3').text
        link = result.find('a')['href']
        snippet = result.find('div', class_='gs_rs').text
        formatted_results.append(f"Title: {title}\nLink: {link}\nSnippet: {snippet}\n")
    
    return "\n\n".join(formatted_results)
        #print(f"Title: {title}\nLink: {link}\nSnippet: {snippet}\n")


def on_search():
    query = query_entry.get()
    results = search_scholar(query)
    results_text.delete(1.0, tk.END)
    results_text.insert(tk.END, results)

# Create the main window
root = tk.Tk()
root.title("LEGION IO")

# Set the window icon
root.iconbitmap('LEGION.ico')  # Use .ico format for Windows

# Create and place the query entry widget
query_label = tk.Label(root, text="Enter search query:")
query_label.pack(pady=5)
query_entry = tk.Entry(root, width=50)
query_entry.pack(pady=5)

# Create and place the search button
search_button = tk.Button(root, text="Search", command=on_search)
search_button.pack(pady=5)

# Create and place the text widget for displaying results
results_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
results_text.pack(pady=5)

# Start the main event loop
root.mainloop()
# Example search
#search_scholar("machine learning")
#run sript python scholar_search.py


