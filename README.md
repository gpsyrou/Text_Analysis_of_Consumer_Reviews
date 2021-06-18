# Description

Purpose of this project is to leverage reviews about major delivery companies that are operating in the UK, and perform NLP tasks to analyze different aspects of the reviews like the sentiment, most common words, probability distributions across word sequences, and more.


```mermaid
graph   LR
    A[Build a tool to connect to web sources APIs] -->|Get reviews from web| B[Clean reviews]
    B --> D[Knowledge Graphs]
    B --> F[Unsupervised Clustering]
    B --> C(Sentiment Analysis)
    B --> |Identify topic of review| E[Topic Extraction]
    E -->  |Train Model| I[Assign Topic to new instances]
    C --> |Train Model| J[Sentiment Classifier]
    I --> K[Build UI]
    J --> K[Build UI]
```
Project Roadmap

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggICBMUlxuICAgIEFbQnVpbGQgYSB0b29sIHRvIGNvbm5lY3QgdG8gd2ViIHNvdXJjZXMgQVBJc10gLS0-fEdldCByZXZpZXdzIGZyb20gd2VifCBCW0NsZWFuIHJldmlld3NdXG4gICAgQiAtLT4gRFtLbm93bGVkZ2UgR3JhcGhzXVxuICAgIEIgLS0-IEZbVW5zdXBlcnZpc2VkIENsdXN0ZXJpbmddXG4gICAgQiAtLT4gQyhTZW50aW1lbnQgQW5hbHlzaXMpXG4gICAgQiAtLT4gfElkZW50aWZ5IHRvcGljIG9mIHJldmlld3wgRVtUb3BpYyBFeHRyYWN0aW9uXVxuICAgIEUgLS0-ICB8VHJhaW4gTW9kZWx8IElbQXNzaWduIFRvcGljIHRvIG5ldyBpbnN0YW5jZXNdXG4gICAgQyAtLT4gfFRyYWluIE1vZGVsfCBKW1NlbnRpbWVudCBDbGFzc2lmaWVyXVxuICAgIEkgLS0-IEtbQnVpbGQgVUldXG4gICAgSiAtLT4gS1tCdWlsZCBVSV0iLCJtZXJtYWlkIjp7InRoZW1lIjoiZGVmYXVsdCJ9LCJ1cGRhdGVFZGl0b3IiOmZhbHNlfQ)](https://mermaid-js.github.io/mermaid-live-editor/#/edit/eyJjb2RlIjoiZ3JhcGggICBMUlxuICAgIEFbQnVpbGQgYSB0b29sIHRvIGNvbm5lY3QgdG8gd2ViIHNvdXJjZXMgQVBJc10gLS0-fEdldCByZXZpZXdzIGZyb20gd2VifCBCW0NsZWFuIHJldmlld3NdXG4gICAgQiAtLT4gRFtLbm93bGVkZ2UgR3JhcGhzXVxuICAgIEIgLS0-IEZbVW5zdXBlcnZpc2VkIENsdXN0ZXJpbmddXG4gICAgQiAtLT4gQyhTZW50aW1lbnQgQW5hbHlzaXMpXG4gICAgQiAtLT4gfElkZW50aWZ5IHRvcGljIG9mIHJldmlld3wgRVtUb3BpYyBFeHRyYWN0aW9uXVxuICAgIEUgLS0-ICB8VHJhaW4gTW9kZWx8IElbQXNzaWduIFRvcGljIHRvIG5ldyBpbnN0YW5jZXNdXG4gICAgQyAtLT4gfFRyYWluIE1vZGVsfCBKW1NlbnRpbWVudCBDbGFzc2lmaWVyXVxuICAgIEkgLS0-IEtbQnVpbGQgVUldXG4gICAgSiAtLT4gS1tCdWlsZCBVSV0iLCJtZXJtYWlkIjp7InRoZW1lIjoiZGVmYXVsdCJ9LCJ1cGRhdGVFZGl0b3IiOmZhbHNlfQ)

# Data Retrieval API

To get reviews from the TrustPilot website, we are leveraging a custom made web scraping tool. This tool is iterating across different pages of the website and collects the reviews and any other relevant information, with the output being stored in CSV files.

### Running Guide

1. Set-up the appropriate configurations in config.json. The config needs to get populated with the following metadata:<br>
        - <em>source_url</em>: Main domain URL<br>
        - <em>starting_page</em>: Domain subpath to a specific reviews page<br>
        - <em>steps</em>: Defines number of pages to iterate over<br>
        - <em>company</em>: Company/Service of interest<br>

2. Execute the python retriever script<br>
        `python data_retriever.py`
