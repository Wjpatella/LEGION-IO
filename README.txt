pip install requests beautifulsoup4

def on_search():
    query = query_entry.get()
    results = search_scholar(query)
    update_results_text(results)
    trend_data = TrendData(query)
    trend_data.fetch_trend_data()

    publication_count = trend_data.get_publication_count()
    update_trend_text(publication_count)

    results = search_scholar(query)
    update_results_text(results)

    8/10/2023
    Pupliaction count is now displayed