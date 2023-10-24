from googlesearch import search
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def get_search_results(query, num_results):
    search_results = []
    
    # Perform the Google search
    search_result = search(query, num_results=num_results)
    for result in search_result:
        search_results.append(result)
    
    return search_results

def get_title_and_description(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the title and description from the HTML
    title = soup.title.string if soup.title else 'No title found'
    description = soup.find('meta', attrs={'name': 'description'})
    description = description['content'] if description else 'No description found'
    
    return title, description

def count_headings_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    headings = {}
    
    # Iterate over each heading tag and count its occurrences
    for heading_level in range(1, 7):
        tag = f'h{heading_level}'
        count = len(soup.find_all(tag))
        headings[tag] = count
    
    # Count the number of <a> tags (links)
    link_count = len(soup.find_all('a'))
    
    return headings, link_count

def count_occurrences(url, word):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all text occurrences of the word
    occurrences = soup.body.text.lower().count(word.lower())
    
    return occurrences

def count_paragraphs(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Count the number of <p> tags
    paragraph_count = len(soup.find_all('p'))
    
    return paragraph_count

def count_images(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Count the number of <img> tags
    image_count = len(soup.find_all('img'))
    
    return image_count

def get_page_size(url):
    response = requests.get(url)
    return len(response.content)

def convert_bytes_to_kilobytes(bytes):
    kilobytes = bytes / 1024
    return kilobytes

def main():
    # Take input from the user
    word = input("Enter a word to search on Google: ")
    file_name = input("Enter the name of the Excel file to save the results: ")
    
    # Specify the number of search results
    num_results = 10
    
    # Perform the search
    search_results = get_search_results(word, num_results=num_results)
    
    # Check if there are enough search results
    if len(search_results) >= num_results:
        # Create lists to store the results
        titles = []
        descriptions = []
        urls = []
        heading_counts = {f'h{i}': [] for i in range(1, 7)}
        link_counts = []
        occurrences_counts = []
        paragraph_counts = []
        image_counts = []  # New list to store image counts
        page_sizes_kb = []
        
        # Extract the title, description, URL, heading counts, link counts, occurrences counts, paragraph counts, image counts, and page sizes of each search result
        for url in search_results:
            title, description = get_title_and_description(url)
            headings, link_count = count_headings_links(url)
            occurrences_count = count_occurrences(url, word)
            paragraph_count = count_paragraphs(url)
            image_count = count_images(url)  # Count images
            page_size_bytes = get_page_size(url)
            page_size_kb = convert_bytes_to_kilobytes(page_size_bytes)
            
            titles.append(title)
            descriptions.append(description)
            urls.append(url)
            
            for heading_level in range(1, 7):
                tag = f'h{heading_level}'
                count = headings.get(tag, 0)
                heading_counts[tag].append(count)
            
            link_counts.append(link_count)
            occurrences_counts.append(occurrences_count)
            paragraph_counts.append(paragraph_count)
            image_counts.append(image_count)  # Append image count
            page_sizes_kb.append(page_size_kb)
        
        # Create a DataFrame to store the results
        data = {'URL': urls, 'Title': titles, 'Description': descriptions, 'Link Count': link_counts, word : occurrences_counts, 'Paragraph Count': paragraph_counts, 'Image Count': image_counts, 'Page Size (KB)': page_sizes_kb}
        data.update(heading_counts)
        df = pd.DataFrame(data)
        
        # Save the DataFrame to an Excel file
        df.to_excel(file_name, index=False)
        
        print("Results saved to", file_name)
    else:
        print("Not enough search results.")

if __name__ == '__main__':
    main()