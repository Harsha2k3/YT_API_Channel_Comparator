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
   - The Engagement Rate is a key metric used to measure the level of interaction and involvement a YouTube channel's audience has with its content. It is calculated by      considering various factors such as likes, comments, and views. A higher engagement rate indicates that the audience finds the content interesting and engaging. 
     This metric helps in understanding how effectively a channel is connecting with its viewers and fostering active participation.
   - The engagement rate can be calculated using the following formula:
     ![image](https://github.com/user-attachments/assets/71830087-fe6e-4b07-99c4-8b493bbd20af)


7. **Sentiment Analysis on Comments using ML**:
   - Uses machine learning to analyze the sentiment of comments on videos from both channels.

## Installation

To get started with this project, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/youtube-channel-comparison.git
    cd youtube-channel-comparison
    ```

2. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up YouTube API**:
   - Obtain your API key from the [Google Developer Console](https://console.developers.google.com/).
   - Add your API key to the project configuration file.

## Usage

1. **Run the main script** to fetch data from YouTube API and perform analysis:
    ```bash
    python main.py
    ```

2. **Generate visualizations and reports**:
    - The script will generate tables and charts for comparison.
    - The results will be saved in the `output` directory.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
