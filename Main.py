import requests #import requests: Imports the requests library, which is used for making HTTP requests. In this script, it is used to send a request to Google Scholar.
from bs4 import BeautifulSoup #from bs4 import BeautifulSoup: Imports the BeautifulSoup class from the bs4 (Beautiful Soup 4) library, which is used for parsing HTML and XML documents. It helps to extract data from the HTML response.
import tkinter as tk #import tkinter as tk: Imports the tkinter library, which is used for creating graphical user interfaces (GUIs) in Python. It is aliased as tk for convenience.
from tkinter import scrolledtext #from tkinter import scrolledtext: Imports the scrolledtext module from tkinter, which provides a text widget with a vertical scrollbar for displaying large amounts of text.
import webbrowser
from trend_data import TrendData


def search_scholar(query):
    # Define the URL with the search query
    url = f"https://scholar.google.com/scholar?q={query}"
    # Send a GET request to the URL
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return
    
    # This Parse will break down the given HTML with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all the result elements
    results = soup.find_all('div', class_='gs_r gs_or gs_scl')
    
    # Extract and format the relevant information from Google Scholar HTML
    formatted_results = []
    for result in results:
        title = result.find('h3').text
        link = result.find('a')['href']
        snippet = result.find('div', class_='gs_rs').text
        formatted_results.append(f"Title: {title}\nLink: {link}\nSnippet: {snippet}\n\n")
    
    return "\n".join(formatted_results)

    #return "\n".join(formatted_results)

        
def on_search():
    query = query_entry.get()
    
    # Fetch and display trend data
    trend_data = TrendData(query)
    trend_data.fetch_trend_data()
    publication_count = trend_data.get_publication_count()
    update_trend_text(publication_count)
    
    # Fetch and display search results
    results = search_scholar(query)
    update_results_text(results)
    
def update_trend_text(publication_count):
    trend_text.delete(1.0, tk.END)
    trend_text.insert(tk.END, f"Publication Count: {publication_count}")

def update_results_text(results):
     # Ensure that results is not None
    if results:
        results_text.delete(1.0, tk.END)
        insert_linked_text(results_text, results)
    else:
        results_text.delete(1.0, tk.END)
        results_text.insert(tk.END, "No results found or there was an error retrieving data.")

def move_selection(text_widget):
    try:
        selected_text = text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
        saved_text.insert(tk.END, selected_text + '\n')
        
        #text_widget.delete(tk.SEL_FIRST, tk.SEL_LAST) was deleting text
    except tk.TclError:
        pass

def insert_linked_text(text_widget, text):
    # Ensure that text is not None
    if text:
        # Insert text into the Text widget and bind clicks to open links
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, text)

        # Remove previous tags
        text_widget.tag_configure("link", foreground="blue", underline=True)
    
        # Find and tag links
        lines = text.split('\n')
        for index, line in enumerate(lines):
            if 'Link:' in line:
                link_start = line.index('Link:') + len('Link: ')
                link_end = len(line)
                url = line[link_start:].strip()  # Extract the URL
                # Tag the link
                text_widget.tag_add("link", f"{index+1}.{link_start}", f"{index+1}.{link_end}")
                text_widget.tag_bind("link", "<Button-1>", lambda e, url=url: open_link(url))
                #text_widget.tag_config("link", foreground="blue", underline=True)
            
            elif 'Title:' in line:
                title_start = line.index('Title:') + len('Title: ')
                title_end = len(line)
                text_widget.tag_add("title", f"{index+1}.{title_start}", f"{index+1}.{title_end}")
    else:
        text_widget.delete(1.0, tk.END)

def open_link(url):
    webbrowser.open(url)

'''
def move_selection():
    try:
        selected_text = results_text.get(tk.SEL_FIRST, tk.SEL_LAST)
        saved_text.insert(tk.END, selected_text + '\n')
        results_text.delete(tk.SEL_FIRST, tk.SEL_LAST)
    except tk.TclError:
        pass
'''
def toggle_popout():
    global popout_window, popout_results_text
    if popout_window:
        popout_window.destroy()
        popout_window = None
    else:
        popout_window = tk.Toplevel(root)
        popout_window.title("Results")

        # Create and place the text widget in the popout window
        popout_results_text = scrolledtext.ScrolledText(popout_window, wrap=tk.WORD, width=100, height=30, bg="#ffffff", fg="#000000")
        popout_results_text.pack(pady=5)

        # Insert current results into the popout text widget
        insert_linked_text(popout_results_text, results_text.get(1.0, tk.END))
        #popout_results_text.insert(tk.END, results_text.get(1.0, tk.END))

        # Add a button to the popout window for moving selected text
        move_button = tk.Button(popout_window, text="Move Selection", command=lambda: move_selection(popout_results_text))
        move_button.pack(pady=5)


# Create the main window
root = tk.Tk()
root.title("L.E.G.I.O.N. I.O.")
popout_window = None

# Set the window icon
root.iconbitmap('LEGION.ico')  # Use .ico format for Windows

# Create a menu bar
menu_bar = tk.Menu(root)

# Add a "File" menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Search", command=on_search)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Add a "View" menu
view_menu = tk.Menu(menu_bar, tearoff=0)
view_menu.add_command(label="Toggle Popout", command=toggle_popout)
menu_bar.add_cascade(label="View", menu=view_menu)

# Configure the menu
root.config(menu=menu_bar)

#Title lable
header_label = tk.Label(root, text="L.E.G.I.O.N. I.O.")
header_label.pack(pady=5)


# Create and place the query entry widget
query_label = tk.Label(root, text="Enter search query:")
query_label.pack(pady=5)
query_entry = tk.Entry(root, width=50)
query_entry.pack(pady=5)

# Create and place the search button
search_button = tk.Button(root, text="Search", command=on_search)
search_button.pack(pady=5)

# Create a frame to hold the text widgets side by side
text_frame = tk.Frame(root)
text_frame.pack(pady=5, padx=5)

# Create and place the text widget for trend data
trend_text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, width=30, height=30, bg="#ffffff", fg="#000000")
trend_text.pack(side=tk.LEFT, padx=5)


# Create and place the text widget for displaying results
results_text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, width=100, height=30, bg="#ffffff", fg="#000000")
results_text.pack(side=tk.LEFT, padx=5)

# Create and place the text widget for saving results
saved_text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, width=50, height=30, bg="#ffffff", fg="#000000")
saved_text.pack(side=tk.LEFT, padx=5)

# Create and place the move button
move_button = tk.Button(root, text="Move Selection", command=lambda: move_selection(results_text))
move_button.pack(pady=5)

# Create and place the toggle button
toggle_button = tk.Button(root, text="Toggle Popout", command=toggle_popout)
toggle_button.pack(pady=5)

# Start the main event loop
root.mainloop()
# Example search
#search_scholar("machine learning")
#run sript python scholar_search.py