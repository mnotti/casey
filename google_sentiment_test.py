from google.cloud import language_v1

def sample_analyze_sentiment(content):

    client = language_v1.LanguageServiceClient()

    # content = 'Your text to analyze, e.g. Hello, world!'

    if isinstance(content, bytes):
        content = content.decode("utf-8")

    type_ = language_v1.Document.Type.PLAIN_TEXT
    document = {"type_": type_, "content": content}

    response = client.analyze_sentiment(request={"document": document})
    sentiment = response.document_sentiment
    print(f"Score: {sentiment.score}")
    print(f"Magnitude: {sentiment.magnitude}")

def main():
   sample_analyze_sentiment("woah this is like really good. I like nvdia stock. People say it's not that great, but i think it's got a good chance to grow.") 

if __name__ == "__main__":
    main()
