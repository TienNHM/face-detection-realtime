# Face Detection Real-Time with MediaPipe and Streamlit

This project demonstrates how to create a real-time face detection application using MediaPipe and Streamlit. The application captures video from the webcam, detects faces, and displays the results in real-time.

## Requirements
- Python 3.7 or higher
- Streamlit
- MediaPipe
- OpenCV

## Installation
1. Create a virtual environment (optional but recommended):
    - On Windows:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

    - On macOS/Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application
To run the application, execute the following command in your terminal:

```bash
streamlit run app.py
```
This will start a local server and open the application in your default web browser. Visit `http://localhost:8501` to view the application.

![Face Detection - Webcam](./assets/img/webcam.png)

![Face Detection - Image](./assets/img/image.png)