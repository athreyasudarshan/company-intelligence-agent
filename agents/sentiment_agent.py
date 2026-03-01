from transformers import pipeline
from schemas.company_schema import SentimentData, NewsItem
from typing import List

# Load the sentiment analysis model once
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert"
)

def analyze_sentiment(news_items: List[NewsItem]) -> SentimentData:
    try:
        if not news_items:
            return SentimentData(
                overall="Neutral",
                score=0.5,
                positive_count=0,
                neutral_count=0,
                negative_count=0
            )

        positive_count = 0
        neutral_count = 0
        negative_count = 0
        total_score = 0.0

        for item in news_items:
            text = item.title
            if item.summary:
                text += " " + item.summary[:200]  # limit text length

            # truncate to 512 tokens max
            text = text[:512]

            result = sentiment_pipeline(text)[0]
            label = result["label"]
            score = result["score"]

            if label == "positive":
                positive_count += 1
                total_score += score
            elif label == "negative":
                negative_count += 1
                total_score += (1 - score)
            else:
                neutral_count += 1
                total_score += 0.5

        total = len(news_items)
        avg_score = total_score / total

        if avg_score >= 0.65:
            overall = "Positive"
        elif avg_score <= 0.4:
            overall = "Negative"
        else:
            overall = "Neutral"
            neutral_count = total - positive_count - negative_count

        return SentimentData(
            overall=overall,
            score=round(avg_score, 2),
            positive_count=positive_count,
            neutral_count=neutral_count,
            negative_count=negative_count
        )

    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return SentimentData(
            overall="Neutral",
            score=0.5,
            positive_count=0,
            neutral_count=0,
            negative_count=0
        )