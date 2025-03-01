import os
from typing import List, Dict, Any, Optional

# Removed opea dependency
from langchain.schema import Document
from scholarly import scholarly
from langchain.tools import tool
from bs4 import BeautifulSoup
import requests

class PaperRetriever:
    """Class for retrieving academic papers."""
    
    def __init__(self, model_name: str = "gemma:2b"):
        """Initialize the PaperRetriever with the specified LLM model."""
        self.model_name = model_name
        
    def set_model(self, model_name: str) -> str:
        """Change the model used."""
        self.model_name = model_name
        return f"Model changed to {model_name}"

    @tool
    def search_google_scholar(self, query: str = None) -> List[Dict[str, Any]]:
        """
        Search for academic papers on Google Scholar.
        
        Args:
            query: The search query string
            
        Returns:
            A list of paper metadata including title, authors, year, and URL
        """
        if not query:
            return [{"error": "Search query is required"}]
            
        try:
            search_query = scholarly.search_pubs(query)
            results = []
            
            # Get the first 5 results
            for i in range(5):
                try:
                    publication = next(search_query)
                    
                    # Extract relevant information
                    paper_info = {
                        "title": publication.get("bib", {}).get("title", "No title"),
                        "authors": publication.get("bib", {}).get("author", "Unknown"),
                        "year": publication.get("bib", {}).get("pub_year", "Unknown"),
                        "url": publication.get("pub_url", "No URL available"),
                        "abstract": publication.get("bib", {}).get("abstract", "No abstract available"),
                        "citations": publication.get("num_citations", 0)
                    }
                    
                    results.append(paper_info)
                except StopIteration:
                    break
                except Exception as e:
                    print(f"Error processing a publication: {e}")
                    continue
                    
            return results
        except Exception as e:
            return [{"error": f"Failed to search Google Scholar: {str(e)}"}]

    @tool
    def fetch_paper_abstract(self, url: str = None) -> str:
        """
        Fetch and extract the abstract from a paper URL.
        
        Args:
            url: URL of the academic paper
            
        Returns:
            The abstract text of the paper
        """
        if not url:
            return "URL is required to fetch paper abstract"
            
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                return f"Failed to fetch the paper: HTTP {response.status_code}"
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try different strategies to find abstract
            # Strategy 1: Look for elements with 'abstract' in id or class
            abstract_elements = soup.find_all(['div', 'p', 'section'], 
                                            id=lambda x: x and 'abstract' in x.lower())
            
            if not abstract_elements:
                abstract_elements = soup.find_all(['div', 'p', 'section'], 
                                                class_=lambda x: x and 'abstract' in x.lower())
            
            if abstract_elements:
                return abstract_elements[0].get_text().strip()
            
            # If no abstract was found with above methods
            return "Could not extract abstract from the provided URL."
            
        except Exception as e:
            return f"Error fetching paper abstract: {str(e)}"

    @tool
    def search_arxiv(self, query: str = None, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search for papers on arXiv using their API.
        
        Args:
            query: The search query string
            max_results: Maximum number of results to return
            
        Returns:
            A list of paper metadata including title, authors, abstract, and URL
        """
        if not query:
            return [{"error": "Search query is required"}]
            
        try:
            base_url = "http://export.arxiv.org/api/query"
            params = {
                "search_query": f"all:{query}",
                "start": 0,
                "max_results": max_results
            }
            
            response = requests.get(base_url, params=params)
            
            if response.status_code != 200:
                return [{"error": f"arXiv API returned status code {response.status_code}"}]
                
            soup = BeautifulSoup(response.content, "xml")
            entries = soup.find_all("entry")
            
            results = []
            for entry in entries:
                try:
                    # Extract authors
                    authors = [author.find("name").text for author in entry.find_all("author")]
                    
                    # Create paper info dictionary
                    paper_info = {
                        "title": entry.find("title").text.strip(),
                        "authors": ", ".join(authors),
                        "abstract": entry.find("summary").text.strip(),
                        "published": entry.find("published").text.strip(),
                        "url": entry.find("id").text.strip(),
                        "pdf_url": next((link["href"] for link in entry.find_all("link") 
                                        if link.get("title") == "pdf"), "No PDF link")
                    }
                    
                    results.append(paper_info)
                except Exception as e:
                    print(f"Error processing an arXiv entry: {e}")
                    continue
                    
            return results
        except Exception as e:
            return [{"error": f"Failed to search arXiv: {str(e)}"}]
    
    def retrieve_papers(self, query: str, search_source: str = "all") -> Dict[str, Any]:
        """
        Retrieve academic papers based on the query and specified source.
        
        Args:
            query: The search query for papers
            search_source: Where to search ("google_scholar", "arxiv", or "all")
            
        Returns:
            Dictionary with search results and any additional information
        """
        if not query:
            return {
                "success": False,
                "error": "Search query is required",
                "papers": []
            }
            
        try:
            papers = []
            
            # Search different sources based on the search_source parameter
            if search_source in ["google_scholar", "all"]:
                scholar_results = self.search_google_scholar(query)
                papers.extend(scholar_results)
                
            if search_source in ["arxiv", "all"]:
                arxiv_results = self.search_arxiv(query)
                papers.extend(arxiv_results)
            
            # Fetch abstracts for papers where needed
            for paper in papers:
                if "abstract" not in paper or not paper["abstract"] or paper["abstract"] == "No abstract available":
                    if "url" in paper and paper["url"] and paper["url"] != "No URL available":
                        abstract = self.fetch_paper_abstract(paper["url"])
                        if abstract and "Error" not in abstract and "Failed" not in abstract:
                            paper["abstract"] = abstract
            
            return {
                "success": True,
                "query": query,
                "source": search_source,
                "result": f"Found {len(papers)} papers related to '{query}'",
                "papers": papers
            }
            
        except Exception as e:
            return {
                "success": False,
                "query": query,
                "error": str(e),
                "papers": []
            }