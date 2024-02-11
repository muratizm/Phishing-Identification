
#***HACETTEPE UNIVERSITY***

#***COMPUTER ENGINEERING***



**Özgür Demirhat - 2200356070** 

**Murat Beder - 21945891**











**TABLE OF CONTENTS**

[**1 Problem Description and Introduction**	2](#_toc155284925)

[**2 Implementation**	3](#_toc155284926)

[**3 System Flow Chart**	7](#_toc155284927)

[**4 Reasons of our some decisions**	8](#_toc155284928)

[**5 Results**	9](#_toc155284929)

[**6 Conclusions and Insights**	11](#_toc155284930)










# <a name="_b1m7kk2isdyj"></a>
# <a name="_toc155284925"></a>**1 Problem Description and Introduction**

Phishing, as one of the most popular forms of cyber threats, involves deceptive attempts to obtain sensitive information by posing as trusted entities through emails, messages, or websites. It exploits human vulnerabilities, relying on social engineering techniques to trick individuals into divulging confidential datas. The importance of countering phishing lies in its potential to cause financial losses, compromise personal information, and lead to unauthorized access. Successful phishing attacks can result in severe conseqences, including identity theft and reputational damage.




In the realm of cybersecurity, defending against phishing is crucial. This mission aims to create a comprehensive threat intelligence system by leveraging Machine Learning (ML) and Natural Language Processing (NLP) techniques. The aim is to distinguish phishing web pages from legitimate ones by understanding subtle semantic differences. 





The dataset used PhishIntention covers 50,000 different samples containing various information sources such as URL, screenshots and HTML files. Through careful and detailed preprocessing, the underlying data content is isolated, paving the way for subsequent stages that include parsing, embedding generation , and development of ML. This research-oriented assignment encourages in-depth exploration of concepts and implementation techniques critical to strong cybersecurity mechanisms.

# <a name="_toc155284926"></a>**2 Implementation**
In this section, we provided comprehensive overview of the implementation details for each component of the assignmen. The assignment involves three main Python scripts: **data\_prepare.py**, **model\_build.py**, **prepare\_embedding.py**, and Flask server script **server.py**. These scripts collectively address data preparation, feature extraction, machine learning, and deployment phases.

**1. Data Preparation (data\_prepare.py):**

This script focuses on organizing the dataset, specifically the PhishIntention dataset, which comprises phishing, legitimate, and misleading samples. The data is structured into "Phishing" and "Legitimate" folders. 

![çizgi, ekran görüntüsü, diyagram, yazı tipi içeren bir resim

Açıklama otomatik olarak oluşturuldu](./readmeimages/Aspose.Words.54d7a36f-0fcb-4cb3-946b-cbb1fdbcb469.004.png)



The key functions involve copying HTML files to destination folders based on specific conditions. 



This process is very important because of ensuring the dataset is properly formatted for subsequent machine learning tasks.

**2. Feature Extraction (prepare\_embedding.py):**

This script utilizes Trafilatura, a powerful HTML parser, to extract meaningful textual content from HTML files. Then, the content is then translated to English using Google Translate, overcoming language diversity in the dataset. 

"xlm-roberta" and "sbert," are employed for embedding generation. The embeddings are saved in the "embeddings" folder.

Step by step how it Works:

- **HTML File Parsing:**
  - We implemented the **parse\_html\_file** function to read HTML content.
  - Utilizing the Trafilatura library, we extracted relevant information from the HTML content and stored in a NumPy array.

- **Translation to English:**
  - We created the **translate\_to\_english** function to translate HTML content to English using the Google Translate API.
  - To **overcome API limitations**, we performed the translation in chunks, handling shorter and longer parts separately.
  - The translated text chunks were stored in NumPy array named **translated\_parts**.

- **Selection of Embedding Model:**
  - We incorporated a command-line argument (algorithm) to determine which Sentence Transformer model to use.
  - If the chosen algorithm is '**sbert**' or '**electra**', we translated the HTML content to English using the previously defined function.
  - Depending on the selected algorithm, we loaded appropriate Sentence Transformer model using the SentenceTransformer library.

- **Embedding Generation:**
  - We generated embedding vectors for both legitimate and phishing samples with Sentence Transformer model and stored the resultings at **legitimate\_data** and **phishing\_data**.
  - Labels were assigned to the legitimate samples (with 0s) phishing samples (with1s)
  - We put the data and labels into the **embedding\_data**.
  - Then, this dictionary serialized and saved as a pickle file in the "embeddings".

**3. Machine Learning (model\_build.py):**

This script loads precomputed embeddings, splits the data, selects and trains a machine learning model (XGBoost or CatBoost) based on user input, saves the trained model, and evaluates it’s performance on the test set, reporting key metrics.

- **Model Evaluation Function (evaluate\_model):**
  - Takes a machine learning model (**model**), test data (**x\_test**), and corresponding labels (**y\_test**).
  - The function predicts labels using the model on the test data and calculates accuracy, precision, and recall scores using scikit-learn metrics.

- **Data Preparation:**
  - The features (**x**) and labels (**y**) are extracted from the loaded embeddings.
  - The data is split into training and testing sets.

- **Model Selection and Initialization:**
  - Based on the command-line argument, either an XGBoost or CatBoost model is selected and initialized.
  - The code creates either an XGBoost model with GPU acceleration or a CatBoost model configured for GPU, based on the command-line argument (‘xgb’ or ‘cat’)

- **Model Training:** 
  - The selected model is trained using the training data.
  - The trained model is saved as a pickle file in the "model" directory. 

- **Model Evaluation:**
  - The **evaluate\_model** function is called to assess the model's performance on the test data.
  - Scores are calculated and printed.


**4. Deployment (server.py):**

The script sets up a web service where users can upload HTML files, and the application predicts whether the content is legitimate or potentially phishing based on a pre-trained XGBoost model.

- **Flask App Setup:**
  - An instance is created (**app = Flask(\_\_name\_\_)**).
- **Loading the Model:**
  - The XGBoost model is loaded using **joblib.load('model/best\_model.pkl')**.
- **Routes:**
  - The main route ("/") renders an HTML template called 'index.html'.
  - The '/predict' route is configured to accept HTTP POST requests.
- **Prediction Logic:**
  - When a file is uploaded, the HTML content of the file is extracted using **trafilatura**.
  - We translate it to English using Google Translate if necessary.
  - The translated HTML is encoded using a Sentence Transformer model.
  - The encoded HTML is fed into the pre-trained XGBoost model for prediction.
  - The result is returned as a ("Legitimate" or "Phishing".)
- **Running the Flask App:**
  - The Flask app runs on port 5050.


# ![System Flow Chart


[System Flow Chart](./readmeimages/Aspose.Words.54d7a36f-0fcb-4cb3-946b-cbb1fdbcb469.006.png)<a name="_toc155284927"></a>**3 System Flow Chart**



# <a name="_qz3tr64t1du4"></a><a name="_toc155284928"></a>**4 Reasons of our some decisions**

**1- Explanation for using Google Small Discriminator:**

`   `We used Google Small Discriminator model for electra in the assignment because instantiating a configuration with the defaults will yield a similar configuration to that of the electra google/electra-small-discriminator architecture and we have small data compared to tens of thosands of data.



**2- Reason for using np.unique:**

`   `After parcing the html files, we encountered lots of same data which will be a problem while training because in ML models if you test an already trained data this outcome is untrustfull and could lead to overtraining. Thats why we removed the recurring ones and used only unique data.


**3- Explanation for the Use of Sleeps and Resetting Translator Object:**

`    `While using googletrans lib, we encountered so many website errors mainly 429 too much request. So inorder to use the lib, we first splitted our data into two parts that one is bigger than 4900 chars and one is smaller, than later if its smaller it will get translated and the program will go to sleep for 1/10 secs inorder to not spam and after 200 data that has been translated we reset the translator to not get ip ban for a day, if its bigger than 4900 chars we split into parts that has 4900 chars and translate seperately and concatenate it.


# <a name="_toc155284929"></a>**5 Results**
As you can see below, our model results highlight a commendable effort in addressing phishing threats. Across various embedding models and ML algorithms, our system consistently demonstrates high accuracy, precision, and recall. The Sbert model, when integrated with both XGBoost and CatBoost, particularly stands out for its robust performance. Additionally, our detailed approach in data preparation, feature extraction, and model evaluation showcases a methodical understanding of the problem.

Addressing challenges, such as evolving phishing techniques, will be a focal point for future enhancements. Overall, we've done solid work in deploying ML for cybersecurity.

Sbert:

![Sbert

[Sbert Results](./readmeimages/Aspose.Words.54d7a36f-0fcb-4cb3-946b-cbb1fdbcb469.009.jpeg)

Electra:

![Electra

[Electra Results](./readmeimages/Aspose.Words.54d7a36f-0fcb-4cb3-946b-cbb1fdbcb469.010.jpeg)

Xlm-roberta

![Xlm-roberta


[Xlm-roberta Results](./readmeimages/Aspose.Words.54d7a36f-0fcb-4cb3-946b-cbb1fdbcb469.011.jpeg)

# <a name="_toc155284930"></a>**6 Conclusions and Insights**

`     `In summary, this assignment thoroughly delves into phishing detection using advanced ML and NLP techniques. Our system for detecting phishing, which incorporates a variety of embedding models and machine learning algorithms, consistently exhibits strong performance, boasting high accuracy, precision, and recall scores. The resulting threat intelligence system, combining semantics and HTML content analysis, highlights its potential for practical applications in cybersecurity.
1
