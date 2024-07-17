import streamlit as st
import pandas as pd
import numpy as np
from googleapiclient.discovery import build
from dateutil import parser
import isodate
import seaborn as sns
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from dateutil import parser

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('vader_lexicon')

st.title("You Tube Channels Comparision")
st.subheader("Enter YouTube Channel IDs")

st.write("To find the channel IDs, use this link : [Streamweasels Website](https://www.streamweasels.com/tools/youtube-channel-id-and-user-id-convertor/)")


num_fields = st.number_input("How many input fields do you want to add?", min_value=1, max_value=100, value=1)

input_values = []

def get_channel_stats(youtube, channel_ids):
    df = []
    request = youtube.channels().list(part='snippet,contentDetails,statistics', id=','.join(channel_ids))
    request = request.execute()
    for i in range(len(request['items'])):
        x = dict(
            title=request['items'][i]['snippet']['title'],
            video_count=request['items'][i]['statistics']['videoCount'],
            subscriber_count=request['items'][i]['statistics']['subscriberCount'],
            view_counts=request['items'][i]['statistics']['viewCount'],
            channel_id=request['items'][i]['contentDetails']['relatedPlaylists']['uploads']
        )
        df.append(x)
    return pd.DataFrame(df)

for i in range(num_fields):
    input_values.append(st.text_input(f"Input field {i+1}"))

if st.button("Submit"):
    input_values = [value for value in input_values if value]

    api_key = "AIzaSyBzEpUDo6MV-QbhVEpx2lycr_bE2KXwwQs"

    channel_ids = input_values

    youtube = build("youtube", "v3", developerKey=api_key)

    x = get_channel_stats(youtube, channel_ids)

    numeric_cols = ["video_count", "subscriber_count", "view_counts"]
    x[numeric_cols] = x[numeric_cols].apply(pd.to_numeric, errors="coerce")

    st.write("Basic Information")
    st.write(x)

    st.header("Visualizations")

    # Bar chart of video counts
    st.subheader("Bar Chart of Video Counts")
    plt.figure(figsize=(10, 6))
    sns.barplot(x="title", y="video_count", data=x)
    st.pyplot(plt)

    # Bar chart of subscriber counts
    st.subheader("Bar Chart of Subscriber Counts")
    plt.figure(figsize=(10, 6))
    sns.barplot(x="title", y="subscriber_count", data=x)
    st.pyplot(plt)

    # Bar chart of view counts
    st.subheader("Bar Chart of View Counts")
    plt.figure(figsize=(10, 6))
    sns.barplot(x="title", y="view_counts", data=x)
    st.pyplot(plt)

    # Fetch video details for each channel
    def get_playlists(youtube, playlist_id):
        video_ids = []
        request = youtube.playlistItems().list(part='contentDetails', playlistId=playlist_id, maxResults=50)
        response = request.execute()
        for i in response['items']:
            video_ids.append(i['contentDetails']['videoId'])
        next_page_token = response.get('nextPageToken')
        while next_page_token:
            request = youtube.playlistItems().list(part='contentDetails', playlistId=playlist_id, maxResults=50, pageToken=next_page_token)
            response = request.execute()
            for i in response['items']:
                video_ids.append(i['contentDetails']['videoId'])
            next_page_token = response.get('nextPageToken')
        return video_ids

    def get_video_details(youtube, video_ids):
        all_video_info = []
        for i in range(0, len(video_ids), 50):
            request = youtube.videos().list(part="snippet,contentDetails,statistics", id=','.join(video_ids[i:i+50]))
            response = request.execute()
            for video in response['items']:
                stats_to_keep = {
                    'snippet': ['channelTitle', 'title', 'description', 'tags', 'publishedAt'],
                    'statistics': ['viewCount', 'likeCount', 'favoriteCount', 'commentCount'],
                    'contentDetails': ['duration', 'definition', 'caption']
                }
                video_info = {'video_id': video['id']}
                for k in stats_to_keep.keys():
                    for v in stats_to_keep[k]:
                        try:
                            video_info[v] = video[k][v]
                        except:
                            video_info[v] = None
                all_video_info.append(video_info)
        return pd.DataFrame(all_video_info)

    def get_comments_in_videos(youtube, video_ids):

        all_comments = []

        for video_id in video_ids:
            try:
                request = youtube.commentThreads().list(
                    part="snippet,replies",
                    videoId=video_id
                )
                response = request.execute()

                comments_in_video = [comment['snippet']['topLevelComment']['snippet']['textOriginal'] for comment in response['items'][0:10]]
                comments_in_video_info = {'video_id': video_id, 'comments': comments_in_video}

                all_comments.append(comments_in_video_info)

            except:
                # When error occurs - most likely because comments are disabled on a video
                print('Could not get comments for video ' + video_id)

        return pd.DataFrame(all_comments)

    # Function to calculate the overall sentiment
    def get_overall_sentiment(comments):
        pos_count = 0
        neg_count = 0
        neu_count = 0

        for comment in comments:
            score = analyzer.polarity_scores(comment)['compound']
            if score >= 0.05:
                pos_count += 1
            elif score <= -0.05:
                neg_count += 1
            else:
                neu_count += 1

        if pos_count > neg_count and pos_count > neu_count:
            return 'Positive'
        elif neg_count > pos_count and neg_count > neu_count:
            return 'Negative'
        else:
            return 'Neutral'

    st.subheader("Growth Rate Analysis")
    for _, row in x.iterrows():
        st.markdown(f"**Analysis for {row['title']}**")

        playlist_id = row['channel_id']
        video_ids = get_playlists(youtube, playlist_id)

        video_df = get_video_details(youtube, video_ids)

        comments_df = get_comments_in_videos(youtube , video_ids)

        numeric_cols_ = ['viewCount', 'likeCount', 'commentCount']
        video_df[numeric_cols_] = video_df[numeric_cols_].apply(pd.to_numeric, errors='coerce', axis=1)

        video_df['publishedAt'] = video_df['publishedAt'].apply(lambda x: parser.parse(x))
        video_df['pushblishDayName'] = video_df['publishedAt'].apply(lambda x: x.strftime("%A"))

        video_df['durationSecs'] = video_df['duration'].apply(lambda x: isodate.parse_duration(x))
        video_df['durationSecs'] = video_df['durationSecs'].astype('timedelta64[s]')

        # Growth Rate Analysis and Predicting Channel Growth
        video_df['year'] = video_df['publishedAt'].dt.year
        video_df['month'] = video_df['publishedAt'].dt.month

        monthly_data = video_df.groupby(['channelTitle', 'year', 'month']).agg({
            'viewCount': 'sum',
            'likeCount': 'sum',
            'commentCount': 'sum',
            'video_id': 'count'
        }).reset_index()
        monthly_data.rename(columns={'video_id': 'videoCount'}, inplace=True)
        monthly_data['viewGrowth'] = monthly_data.groupby('channelTitle')['viewCount'].pct_change() * 100
        monthly_data['likeGrowth'] = monthly_data.groupby('channelTitle')['likeCount'].pct_change() * 100
        monthly_data['commentGrowth'] = monthly_data.groupby('channelTitle')['commentCount'].pct_change() * 100
        monthly_data['videoGrowth'] = monthly_data.groupby('channelTitle')['videoCount'].pct_change() * 100
        monthly_data.fillna(0, inplace=True)
        monthly_data['date'] = pd.to_datetime(monthly_data[['year', 'month']].assign(day=1))

        plt.figure(figsize=(12, 8))
        plt.subplot(2, 2, 1)
        plt.plot(monthly_data['date'], monthly_data['viewGrowth'], marker='o')
        plt.title(f'{row["title"]} - View Growth Rate')
        plt.xlabel('Time')
        plt.ylabel('Growth Rate (%)')
        plt.xticks(rotation=45)
        plt.subplot(2, 2, 2)
        plt.plot(monthly_data['date'], monthly_data['likeGrowth'], marker='o')
        plt.title(f'{row["title"]} - Like Growth Rate')
        plt.xlabel('Time')
        plt.ylabel('Growth Rate (%)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(plt)


    all_channel_data = pd.DataFrame()

    st.subheader("Engagement rate")

    for _, row in x.iterrows():
        st.markdown(f"**Analysis for {row['title']}**")

        playlist_id = row['channel_id']
        video_ids = get_playlists(youtube, playlist_id)

        video_df = get_video_details(youtube, video_ids)

        numeric_cols_ = ['viewCount', 'likeCount', 'commentCount']
        video_df[numeric_cols_] = video_df[numeric_cols_].apply(pd.to_numeric, errors='coerce', axis=1)

        video_df['publishedAt'] = video_df['publishedAt'].apply(lambda x: parser.parse(x))
        video_df['pushblishDayName'] = video_df['publishedAt'].apply(lambda x: x.strftime("%A"))

        video_df['durationSecs'] = video_df['duration'].apply(lambda x: isodate.parse_duration(x))
        video_df['durationSecs'] = video_df['durationSecs'].astype('timedelta64[s]')

        # Growth Rate Analysis and Predicting Channel Growth
        video_df['year'] = video_df['publishedAt'].dt.year
        video_df['month'] = video_df['publishedAt'].dt.month

        # Group by channel to get total likes, comments, views, and subscribers
        channel_data = video_df.groupby('channelTitle').agg({
            'likeCount': 'sum',
            'commentCount': 'sum',
            'viewCount': 'sum',
            'video_id': 'count'
        }).reset_index()

        # Rename columns for clarity
        channel_data.rename(columns={'video_id': 'videoCount'}, inplace=True)

        # Calculate Channel Engagement Rate (CER)
        channel_data['CER'] = ((channel_data['likeCount'] + channel_data['commentCount']) / channel_data['viewCount']) * 100

        st.write(f"On an average, about {round(channel_data['CER'][0], 2)}% of viewers of the videos on the channel engage with the content in the form of likes or comments.")

        # Accumulate the engagement rate data
        all_channel_data = pd.concat([all_channel_data, channel_data])

    # Plot Engagement Rates

    plt.figure(figsize=(12, 8))
    sns.barplot(x='channelTitle', y='CER', data=all_channel_data)
    plt.title('Engagement Rate of Channels')
    plt.xlabel('Channel Title')
    plt.ylabel('Engagement Rate (%)')
    st.pyplot(plt.gcf())


    st.subheader("Sentiment Analysis on Comments")
    for _, row in x.iterrows():
        st.markdown(f"**Analysis for {row['title']}**")

        playlist_id = row['channel_id']
        video_ids = get_playlists(youtube, playlist_id)

        video_df = get_video_details(youtube, video_ids)

        comments_df = get_comments_in_videos(youtube , video_ids)

        numeric_cols_ = ['viewCount', 'likeCount', 'commentCount']
        video_df[numeric_cols_] = video_df[numeric_cols_].apply(pd.to_numeric, errors='coerce', axis=1)

        video_df['publishedAt'] = video_df['publishedAt'].apply(lambda x: parser.parse(x))
        video_df['pushblishDayName'] = video_df['publishedAt'].apply(lambda x: x.strftime("%A"))

        video_df['durationSecs'] = video_df['duration'].apply(lambda x: isodate.parse_duration(x))
        video_df['durationSecs'] = video_df['durationSecs'].astype('timedelta64[s]')

        # Growth Rate Analysis and Predicting Channel Growth
        video_df['year'] = video_df['publishedAt'].dt.year
        video_df['month'] = video_df['publishedAt'].dt.month

        # Sentiment Analysis on Comments
        # Initialize VADER sentiment analyzer
        analyzer = SentimentIntensityAnalyzer()

        # Flatten the list of comments
        all_comments = [comment for sublist in comments_df['comments'] for comment in sublist]

        # Calculate the overall sentiment for all comments
        overall_sentiment = get_overall_sentiment(all_comments)

        # Display the overall sentiment
        st.write(f'Overall Sentiment on comments: {overall_sentiment}')