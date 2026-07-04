# Rising Waters

Rising Waters is a flood prediction web application developed using Flask and Machine Learning. The application predicts the likelihood of flooding based on weather and rainfall parameters entered by the user. It also provides a confidence score for each prediction and stores previous predictions for registered users.

## Features

- User registration and login
- Flood risk prediction using an XGBoost model
- Prediction confidence score
- Prediction history
- User dashboard
- Responsive web interface
- SQLite database integration

## Technologies Used

**Frontend**
- HTML
- CSS
- Bootstrap
- JavaScript

**Backend**
- Python
- Flask

**Machine Learning**
- XGBoost
- Scikit-learn
- Pandas
- NumPy
- Joblib

**Database**
- SQLite

## Project Structure

```
Rising-Waters/
│
├── app.py
├── train_model.py
├── floods.save
├── transform.save
├── requirements.txt
├── static/
├── templates/
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Madhu57827/Rising-Waters.git
```

Move to the project directory:

```bash
cd Rising-Waters
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

## Machine Learning Workflow

1. Load the dataset.
2. Preprocess the data and remove missing values.
3. Split the dataset into training and testing sets.
4. Scale the input features using StandardScaler.
5. Train the XGBoost classifier.
6. Save the trained model and scaler.
7. Use the trained model to predict flood risk from user inputs.

## Future Enhancements

- Integration with live weather data
- Email or SMS notifications
- Interactive flood maps
- Cloud deployment
- Administrative dashboard

## Author

Lanka Madhu Sree

This project was developed as part of the SmartBridge Internship to demonstrate the integration of machine learning with a Flask-based web application for flood risk prediction.
