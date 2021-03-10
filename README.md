Purpose of this project is to leverage reviews about major delivery companies that are operating in the UK, and perform NLP tasks to analyze different aspects of the reviews like the sentiment, most common words, probability distributions across word sequences, and more.


```mermaid
graph   LR
    A[Build a tool to connect to web sources APIs] -->|Get reviews from web| B[Clean reviews]
    B --> C(Sentiment Analysis)
    C -->|Deliveroo| D[Sentiment]
    C -->|UberEats| D[Sentiment]
    C -->|JustEat| D[Sentiment]
    B --> E[Knowledge Graphs]
    B --> F[Unsupervised Clustering]
    B --> |Identify topic of review| G[Topic Extraction]
```
Project Roadmap

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggICBMUlxuICAgIEFbQnVpbGQgYSB0b29sIHRvIGNvbm5lY3QgdG8gd2ViIHNvdXJjZXMgQVBJc10gLS0-fEdldCByZXZpZXdzIGZyb20gd2VifCBCW0NsZWFuIHJldmlld3NdXG4gICAgQiAtLT4gQyhTZW50aW1lbnQgQW5hbHlzaXMpXG4gICAgQyAtLT58RGVsaXZlcm9vfCBEW1NlbnRpbWVudF1cbiAgICBDIC0tPnxVYmVyRWF0c3wgRFtTZW50aW1lbnRdXG4gICAgQyAtLT58SnVzdEVhdHwgRFtTZW50aW1lbnRdXG4gICAgQiAtLT4gRVtLbm93bGVkZ2UgR3JhcGhzXVxuICAgIEIgLS0-IEZbVW5zdXBlcnZpc2VkIENsdXN0ZXJpbmddXG4gICAgQiAtLT4gfElkZW50aWZ5IHRvcGljIG9mIHJldmlld3wgR1tUb3BpYyBFeHRyYWN0aW9uXSIsIm1lcm1haWQiOnt9LCJ1cGRhdGVFZGl0b3IiOmZhbHNlfQ)](https://mermaid-js.github.io/mermaid-live-editor/#/edit/eyJjb2RlIjoiZ3JhcGggICBMUlxuICAgIEFbQnVpbGQgYSB0b29sIHRvIGNvbm5lY3QgdG8gd2ViIHNvdXJjZXMgQVBJc10gLS0-fEdldCByZXZpZXdzIGZyb20gd2VifCBCW0NsZWFuIHJldmlld3NdXG4gICAgQiAtLT4gQyhTZW50aW1lbnQgQW5hbHlzaXMpXG4gICAgQyAtLT58RGVsaXZlcm9vfCBEW1NlbnRpbWVudF1cbiAgICBDIC0tPnxVYmVyRWF0c3wgRFtTZW50aW1lbnRdXG4gICAgQyAtLT58SnVzdEVhdHwgRFtTZW50aW1lbnRdXG4gICAgQiAtLT4gRVtLbm93bGVkZ2UgR3JhcGhzXVxuICAgIEIgLS0-IEZbVW5zdXBlcnZpc2VkIENsdXN0ZXJpbmddXG4gICAgQiAtLT4gfElkZW50aWZ5IHRvcGljIG9mIHJldmlld3wgR1tUb3BpYyBFeHRyYWN0aW9uXSIsIm1lcm1haWQiOnt9LCJ1cGRhdGVFZGl0b3IiOmZhbHNlfQ)