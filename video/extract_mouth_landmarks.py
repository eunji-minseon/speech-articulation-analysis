def extract_mouth_landmarks(video_path, output_path="mouth_coords.txt"):
    import cv2
    import mediapipe as mp

    mp_face_mesh = mp.solutions.face_mesh
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"❌ 영상 파일 열기 실패: {video_path}")
        return

    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)
    frame_count = 0
    success_count = 0

    with open(output_path, "w") as f:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame_count += 1

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb)

            if results.multi_face_landmarks:
                landmarks = results.multi_face_landmarks[0]
                mouth_indices = list(range(61, 88))
                coords = [(lm.x, lm.y) for i, lm in enumerate(landmarks.landmark) if i in mouth_indices]
                f.write(str(coords) + "\n")
                success_count += 1

    cap.release()
    print(f"📽️ {video_path}: 총 {frame_count}프레임 중 {success_count}개에서 얼굴 인식 성공")
