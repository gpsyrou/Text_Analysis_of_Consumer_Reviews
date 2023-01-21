# Topic Modelling with NLP & Latent Dirichlet Allocation on Customer Reviews
![Python](https://img.shields.io/badge/-Python-000?&logo=Python) ![Jupyter Notebook](https://img.shields.io/badge/Jupyter-Notebook-orange?&logo=Jupyter)

Purpose of this project is to leverage reviews about major delivery companies that are operating in the UK, and perform NLP tasks to analyze different aspects of the reviews like the sentiment, most common words, probability distributions across word sequences, and more.

## Project Roadmap

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


## Data Retrieval API

To get reviews from the TrustPilot website, we are leveraging a custom made web scraping tool. This tool is iterating across different pages of the website and collects the reviews and any other relevant information, with the output being stored in CSV files.

### Running Guide

1. Set-up the appropriate configurations in config.json. The config needs to get populated with the following metadata:<br>
        - <em>source_url</em>: Main domain URL<br>
        - <em>starting_page</em>: Domain subpath to a specific reviews page<br>
        - <em>steps</em>: Defines number of pages to iterate over<br>
        - <em>company</em>: Company/Service of interest<br>

2. Execute the python retriever script<br>
        `python data_retriever.py`
