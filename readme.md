# Sentiment Analysis With NLP

## Overview
This project focuses on performing sentiment analysis on 150 blog posts scraped from various websites. By leveraging Natural Language Processing (NLP) techniques and machine learning models, the project is able to predict the sentiments of these blog posts.

## Table of Contents
- [Introduction](#introduction)
- [Data Collection](#data-collection)
- [Preprocessing](#preprocessing)
- [Modeling](#modeling)
- [Evaluation](#evaluation)
- [Results](#results)
- [Usage](#usage)
- [Contributors](#contributors)
- [License](#license)

## Introduction
Sentiment analysis, also known as opinion mining, involves determining the sentiment expressed in a piece of text. This project aims to categorize the sentiments of blog posts as positive, negative, or neutral. The analysis is carried out using various NLP techniques and machine learning models.

## Data Collection
The dataset consists of 150 blog posts scraped from different websites. The blogs cover a wide range of topics to ensure diversity in the sentiment analysis. Web scraping tools such as BeautifulSoup and Scrapy were used to collect the blog posts.

## Preprocessing
Preprocessing steps include:
- Cleaning the text (removing HTML tags, punctuation, numbers, and special characters)
- Tokenization
- Stop words removal
- Lemmatization

These steps ensure that the text data is in a suitable format for modeling.

## Modeling
Several machine learning models were applied to predict the sentiments:
- **Logistic Regression**
- **Support Vector Machines (SVM)**
- **Random Forest**
- **Naive Bayes**

Additionally, advanced NLP techniques like TF-IDF and word embeddings were utilized to improve model performance.

## Evaluation
The models were evaluated based on metrics such as accuracy, precision, recall, and F1-score. Cross-validation was performed to ensure the robustness of the models.

## Results
The best performing model achieved an accuracy of XX% (update with actual result) on the test set. Detailed results, including confusion matrices and performance metrics for each model, can be found in the `results` directory.

## Usage
To run this project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sentiment-analysis-blog-posts.git


2. Navigate to the project directory:
   ```bash
   cd sentiment-analysis-blog-posts
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the preprocessing script:
   ```bash
   python preprocess.py
   ```

5. Train the models:
   ```bash
   python train.py
   ```

6. Evaluate the models:
   ```bash
   python evaluate.py
   ```

## Contributors
This project was developed by Himanshu Mahajan.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
