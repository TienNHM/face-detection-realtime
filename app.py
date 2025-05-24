import cv2
import tempfile
import streamlit as st
import mediapipe as mp

# Khởi tạo MediaPipe
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

st.set_page_config(page_title="Face Detection Realtime", layout="centered")
st.title("🎥 Real-time Face Detection")

# Sidebar cấu hình
st.sidebar.header("⚙️ Cấu hình")

def detect_faces(image, detector):
    """Nhận diện khuôn mặt và vẽ annotation lên ảnh."""
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = detector.process(rgb_image)
    if results.detections:
        for detection in results.detections:
            mp_drawing.draw_detection(image, detection)
    return image

def run_webcam(confidence, camera_index=0):
    """Chạy webcam realtime nhận diện khuôn mặt."""
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        st.toast("❌ Không thể truy cập webcam.", icon="🚫")
        return

    st.toast("📷 Đang chạy webcam...", icon="✅")
    frame_placeholder = st.empty()

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

def process_uploaded_image(file_path, confidence):
    """Xử lý file ảnh upload."""
    image = cv2.imread(file_path)
    if image is None:
        st.error("❌ Không thể đọc ảnh.")
        return
    with mp_face_detection.FaceDetection(
        model_selection=0,
        min_detection_confidence=confidence
    ) as face_detector:
        annotated_image = detect_faces(image, face_detector)
        st.image(cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB), use_container_width=True)

def process_uploaded_video(file_path, confidence):
    """Xử lý file video upload."""
    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        st.error("❌ Không thể đọc video.")
        return

    stframe = st.empty()
    with mp_face_detection.FaceDetection(
        model_selection=0,
        min_detection_confidence=confidence
    ) as face_detector:

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (640, 480))
            annotated_image = detect_faces(frame, face_detector)
            stframe.image(cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB), use_container_width=True)

    cap.release()

def handle_upload(confidence):
    """Xử lý file upload từ người dùng."""
    uploaded_file = st.sidebar.file_uploader(
        "Tải lên ảnh hoặc video (mp4, mov, jpg, png, ...)",
        type=["mp4", "mov", "avi", "jpg", "jpeg", "png"],
        help="Chọn file ảnh hoặc video để thực hiện nhận diện khuôn mặt."
    )
    if uploaded_file is None:
        st.info("📁 Vui lòng tải lên file ảnh hoặc video để nhận diện.")
        return

    # Lưu file tạm để OpenCV đọc
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    temp_file_path = tfile.name

    if uploaded_file.type.startswith("image"):
        process_uploaded_image(temp_file_path, confidence)
    elif uploaded_file.type.startswith("video"):
        process_uploaded_video(temp_file_path, confidence)
    else:
        st.error("❌ Định dạng file không được hỗ trợ.")

# Main app logic

mode = st.sidebar.radio(
    "Chọn chế độ hoạt động:",
    options=["Webcam", "Upload File"],
    help="Chọn chế độ dùng webcam realtime hoặc tải lên ảnh/video để nhận diện."
)

confidence = st.sidebar.slider(
    "🔍 Ngưỡng Confidence",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.05,
    help="Đặt ngưỡng confidence để lọc các khuôn mặt yếu. Giá trị càng cao, kết quả càng chính xác nhưng có thể bỏ sót khuôn mặt."
)

if mode == "Webcam":
    camera_index = st.sidebar.selectbox(
        "📷 Camera Index",
        options=[0],
        index=0,
        help="Chọn webcam để sử dụng."
    )
    run = st.sidebar.toggle(
        "▶️ Bắt đầu webcam",
        help="Bật/tắt webcam để nhận diện khuôn mặt realtime."
    )

    if run:
        run_webcam(confidence, camera_index)
    else:
        st.info("👈 Bật webcam ở sidebar để bắt đầu nhận diện khuôn mặt.", icon="ℹ️")
else:
    handle_upload(confidence)
