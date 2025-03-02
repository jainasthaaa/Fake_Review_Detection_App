# **Fake Review Detection System**

## **Overview**
The Fake Review Detection System is designed to identify and prevent fake reviews in e-commerce platforms using a combination of **Machine Learning (ML), Blockchain, and Authentication techniques**. This system helps maintain the credibility of online reviews by verifying purchases and securely storing review data.

## **Technologies Used**
- **Machine Learning**: Naïve Bayes classifier with **TF-IDF vectorization** for fake review detection.
- **Blockchain**: SHA-256 hashing to ensure the integrity and tamper-proof storage of reviews.
- **Authentication**: Purchase verification to prevent fake reviews from unverified users.
- **Flask**: Web framework for building APIs and handling user interactions.
- **Pandas & Scikit-Learn**: Data processing and machine learning model training.

## **Features**
- **Detects fake reviews** using ML.
- **Verifies purchases** before accepting a review.
- **Stores reviews securely** with blockchain-based integrity.
- **Provides an API** for submitting and retrieving reviews.

## Screenshots

### **1. Fake Review Detection Result I**
![Detection Result](screenshots/Screenshot (108).png)

### **2. Fake Review Detection Result II**
![Detection Result](screenshots/Screenshot (109).png)

### **3. Fake Review Detection Result III**
![Detection Result](screenshots/Screenshot (110).png)


## **Installation**
### **1. Clone the Repository**
```bash
 git clone https://github.com/jainasthaaa/Fake_Review_Detection_App.git
 cd Fake_Review_Detection_App
```

### **2. Create and Activate Virtual Environment**
```bash
 python -m venv venv
 source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3. Install Dependencies**
```bash
 pip install -r requirements.txt
```

## **Usage**
### **Run the Flask App**
```bash
 python app.py
```
The app will run on **http://localhost:8080**

### **API Endpoints**
1. **Predict Fake Review:**
   - `POST /predict`
   - **Input:** `user_id, product_id, review_text, proof (optional)`
   - **Output:** JSON response with review authenticity and blockchain hash.

2. **Get Review Chain:**
   - `GET /review-chain`
   - **Output:** List of all stored reviews with blockchain security.

## **Example API Call**
```bash
curl -X POST http://localhost:8080/predict -d "user_id=user123&product_id=productA&review=Great quality product!"
```

## **Project Structure**
```
📂 fake-review-detection
├── 📂 uploads/          # Stores proof of purchase files
├── app.py              # Main Flask application
├── requirements.txt    # Dependencies
├── templates/
│   ├── c.html         # Frontend interface
└── README.md           # Project documentation
```

## **License**
This project is licensed under the **MIT License**.

## **Contributors**
- **Your Name** - [GitHub Profile](https://github.com/jainasthaaa)

---
Feel free to contribute by submitting issues or pull requests!

