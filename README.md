# YouTube Channel Comparison

This project uses the YouTube API to compare two YouTube channels based on various metrics. The project aims to provide a comprehensive analysis of the channels' performance, growth, and audience engagement.

## Features

1. **Table for Subscriber Counts, Video Counts, and View Counts**:
   - Displays a table comparing the key metrics of the two channels.

2. **Bar Chart of Subscriber Counts**:
   - Visual representation of the subscriber counts for each channel.

3. **Bar Chart of Video Counts**:
   - Visual representation of the video counts for each channel.

4. **Bar Chart of View Counts**:
   - Visual representation of the view counts for each channel.

5. **Growth Rate Analysis**:
   - Analyzes and compares the growth rate of each channel over a specified period.

6. **Engagement Rate**:
   - Calculates and compares the engagement rates of the channels, providing insights into audience interaction.
   - The Engagement Rate is a key metric used to measure the **level of interaction and involvement a YouTube channel's audience has with its content**. It is
     calculated by considering various factors such as likes, comments, and views. **A higher engagement rate indicates that the audience finds the content interesting
     and engaging**.This metric helps in understanding how effectively a channel is connecting with its viewers and fostering active participation.
   - The engagement rate can be calculated using the following formula:
     ![image](https://github.com/user-attachments/assets/71830087-fe6e-4b07-99c4-8b493bbd20af)


7. **Sentiment Analysis on Comments using ML**:
   - Uses machine learning to analyze the sentiment of comments on videos from the channels.

## Installation

To get started with this project, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Harsha2k3/YT_API_Channel_Comparator.git
    YT_API_Channel_Comparator
    ```

2. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up YouTube API**:
   - Go to https://developers.google.com/youtube/v3
   - Click on "Add YouTube functionality to your site"
     ![image](https://github.com/user-attachments/assets/1b8edadf-c76b-4a68-95c1-3aade0e28ccb)
   - Click on "Google Developers Console"
     ![image](https://github.com/user-attachments/assets/1baa6af1-ef51-4596-8232-76867978807e)
   - Click on "Youtube Statistics"
     ![image](https://github.com/user-attachments/assets/4c20823a-e9d6-4dff-a91a-c64375682532)
   - Create New Project
     ![image](https://github.com/user-attachments/assets/4bbf45a6-0ba9-4922-a33c-4dbeb2ad554e)
   - Select project in notifications
     ![image](https://github.com/user-attachments/assets/cbcf1f4a-305c-4dd9-bc5d-9aa483ac0ea5)
   - Click on ENABLE APIS AND SERVICES
     ![image](https://github.com/user-attachments/assets/e08dad00-a869-48d7-b0bb-3a7a06860ff8)
   - Click on "Credentials"
     ![image](https://github.com/user-attachments/assets/656ce39d-12fa-4e38-8c11-115249787ce3)
   - Create Credentials and select API key
     ![image](https://github.com/user-attachments/assets/7a424556-0354-4515-be19-5061f3a62833)
   - Copy the created API key
   - Now, we have to enable the API key
   - Click on ENABLE APIS AND SERVICES
     ![image](https://github.com/user-attachments/assets/281a0394-77e7-4c5a-b3e9-fb54b6296e32)
   - Search for "youtube data api v3"
     ![image](https://github.com/user-attachments/assets/56f81888-1386-43f2-86c6-b17269289a97)
   - Select it
     ![image](https://github.com/user-attachments/assets/aaed2ec7-1ab9-4273-a661-64b5a6e3ec94)
   - Click "ENABLE"
     ![image](https://github.com/user-attachments/assets/5eb484d1-9e1a-4c06-b65a-76d52a4c6559)



## Usage

1. **Run the main script** to fetch data from YouTube API and perform analysis:
    ```bash
    python main.py
    ```

2. **Generate visualizations and reports**:
    - The script will generate tables and charts for comparison.
    - The results will be saved in the `output` directory.

## Contact :
- For any inquiries or questions regarding the T-20 Score Predictor, please reach out to harshamamidipaka2003@gmail.com
