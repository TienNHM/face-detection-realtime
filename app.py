import cv2
import streamlit as st
import mediapipe as mp

# Khởi tạo MediaPipe
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

st.set_page_config(page_title="Face Detection Realtime", layout="centered")
st.title("🎥 Real-time Face Detection")

# Sidebar cấu hình
st.sidebar.header("⚙️ Cấu hình")

confidence = st.sidebar.slider(
    "🔍 Ngưỡng Confidence",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.05,
    help="Đặt ngưỡng confidence để lọc các khuôn mặt yếu. Giá trị càng cao, kết quả càng chính xác nhưng có thể bỏ sót khuôn mặt."
)

camera_index = st.sidebar.selectbox(
    "📷 Camera Index",
    options=[0],
    index=0,
    help="Chọn nguồn webcam. Thường là 0 nếu bạn chỉ có một camera tích hợp."
)

run = st.sidebar.toggle(
    "▶️ Bắt đầu webcam",
    help="Bật hoặc tắt camera để bắt đầu nhận diện khuôn mặt theo thời gian thực."
)

frame_placeholder = st.empty()

def detect_faces(image, detector):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = detector.process(rgb_image)

    if results.detections:
        for detection in results.detections:
            mp_drawing.draw_detection(image, detection)
    return image

if run:
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        st.toast("❌ Không thể truy cập webcam.", icon="🚫")
    else:
        st.toast("📷 Đang chạy webcam...", icon="✅")

        with mp_face_detection.FaceDetection(
            model_selection=0,
            min_detection_confidence=confidence
        ) as face_detector:

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    st.toast("⚠️ Không thể đọc frame từ webcam.", icon="⚠️")
                    break

                frame = cv2.resize(frame, (640, 480))
                annotated_image = detect_faces(frame, face_detector)

                frame_placeholder.image(
                    cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB),
                    channels="RGB",
                    use_container_width=True
                )

    cap.release()
else:
    st.toast("👈 Bật webcam ở sidebar để bắt đầu nhận diện khuôn mặt.", icon="ℹ️")
