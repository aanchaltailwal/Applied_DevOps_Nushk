from flask import Flask, render_template, request, redirect, url_for
import requests
from textblob import TextBlob
import statistics
import random

app = Flask(__name__)

# Empty list to store comments
filtered_comments = []

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/process_comments', methods=['POST'])
def process_comments():
    global filtered_comments

    commentNumber = int(request.form['commentNumber'])
    videoId = request.form['videoId']

    url = f"https://www.googleapis.com/youtube/v3/commentThreads?key=AIzaSyAdiwelV4X32OUoQHAk4s8uFGQ8i3K2iGk&textFormat=plainText&part=snippet&videoId={videoId}&maxResults={commentNumber}"
    response = requests.get(url)
    data = response.json()

    # Get all the comments from the API response
    for item in data['items']:
        filtered_comments.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])

    # Process and analyze the comments using TextBlob
    analysis_results = analysis(filtered_comments)

    # Redirect to the result page with the analysis_results parameter
    return redirect(url_for('result', analysis_results=analysis_results))

@app.route('/result')
def result():
    # Get the analysis results from the URL parameter
    analysis_results = request.args.get('analysis_results')

    if analysis_results is None:
        # Handle the case where analysis_results is not defined
        return "Error: Analysis results not available."

    # Return the sentiment analysis results here
    return render_template('result.html', analysis_results=analysis_results)

def analysis(filtered_comments):
    # Your TextBlob analysis code here
    positive = 0
    wpositive = 0
    spositive = 0
    negative = 0
    wnegative = 0
    snegative = 0
    neutral = 0
    track = []

    for comment in filtered_comments:
        analysis = TextBlob(comment)
        i = analysis.sentiment.polarity
        if (i == 0):
            neutral += 1
        elif (i > 0 and i <= 0.3):
            wpositive += 1
        elif (i > 0.3 and i <= 0.6):
            positive += 1
        elif (i > 0.6 and i <= 1):
            spositive += 1
        elif (i > -0.3 and i <= 0):
            wnegative += 1
        elif (i > -0.6 and i <= -0.3):
            negative += 1
        elif (i > -1 and i <= -0.6):
            snegative += 1
        track.append(i)

    NoOfTerms = len(filtered_comments)

    positive_percentage = format(100 * float(positive) / float(NoOfTerms), '0.2f')
    wpositive_percentage = format(100 * float(wpositive) / float(NoOfTerms), '0.2f')
    spositive_percentage = format(100 * float(spositive) / float(NoOfTerms), '0.2f')
    negative_percentage = format(100 * float(negative) / float(NoOfTerms), '0.2f')
    wnegative_percentage = format(100 * float(wnegative) / float(NoOfTerms), '0.2f')
    snegative_percentage = format(100 * float(snegative) / float(NoOfTerms), '0.2f')
    neutral_percentage = format(100 * float(neutral) / float(NoOfTerms), '0.2f')

    Final_score = statistics.mean(track)

    if Final_score > 0:
        sentiment_result = f"Using TextBlob Sentiment Analyzer: Overall Reviews are Positive with Score {format(100 * Final_score, '0.2f')}%"
    elif Final_score < 0:
        sentiment_result = f"Using TextBlob Sentiment Analyzer: Overall Reviews are Negative with Score {format(100 * Final_score, '0.2f')}%"
    else:
        sentiment_result = f"Using TextBlob Sentiment Analyzer: Overall Reviews are Moderate with Score {format(100 * Final_score, '0.2f')}%"

    detailed_report = (
        f"Detailed Report: {positive_percentage}% people thought it was positive, "
        f"{wpositive_percentage}% people thought it was weakly positive, "
        f"{spositive_percentage}% people thought it was strongly positive, "
        f"{negative_percentage}% people thought it was negative, "
        f"{wnegative_percentage}% people thought it was weakly negative, "
        f"{snegative_percentage}% people thought it was strongly negative, "
        f"{neutral_percentage}% people thought it was neutral"
    )

    # Add line breaks for better readability
    return f"{sentiment_result}\n\n{detailed_report}"
if __name__ == '__main__':
    app.run(debug=True)
