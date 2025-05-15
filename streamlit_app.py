import os
import sys
import ast 

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ✅ ffmpeg 설치 변수 및 함수 정의
FFMPEG_URL = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"
FFMPEG_DIR = "/tmp/ffmpeg"

def setup_ffmpeg():
    if not os.path.exists(f"{FFMPEG_DIR}/ffmpeg"):
        import tarfile, urllib.request
        print("🔽 ffmpeg 바이너리 다운로드 중...")
        os.makedirs(FFMPEG_DIR, exist_ok=True)
        tmp_path = "/tmp/ffmpeg.tar.xz"
        urllib.request.urlretrieve(FFMPEG_URL, tmp_path)

        with tarfile.open(tmp_path) as tar:
            tar.extractall(path="/tmp")

        extracted = [f for f in os.listdir("/tmp") if f.startswith("ffmpeg") and os.path.isdir(f"/tmp/{f}")][0]
        os.rename(f"/tmp/{extracted}", FFMPEG_DIR)

        print("✅ ffmpeg 다운로드 완료!")

    os.environ["PATH"] = f"{FFMPEG_DIR}:" + os.environ["PATH"]

# ✅ ffmpeg 실행
setup_ffmpeg()

# ✅ 패키지 import 수정 완료!
from video.extract_mouth_landmarks import extract_mouth_landmarks
from analysis.compare_shapes import calculate_similarity

def load_coords_from_txt(path):
    coords = []
    with open(path, 'r') as f:
        for line in f:
            try:
                coords.append(ast.literal_eval(line.strip()))
            except (SyntaxError, ValueError):
                st.warning(f"⚠️ 잘못된 좌표 형식 무시됨: {line.strip()}")
    return coords

# ✅ 파일 경로
normal_video = "data/raw/normal.mp4"
error_video = "data/raw/error.mp4"

normal_coords_path = "data/processed/normal_coords.txt"
error_coords_path = "data/processed/error_coords.txt"

# ✅ 디렉토리 생성
os.makedirs("data/processed", exist_ok=True)

# ✅ 좌표 추출 실행
extract_mouth_landmarks(normal_video, normal_coords_path)
extract_mouth_landmarks(error_video, error_coords_path)

# ✅ 좌표 불러오기
normal_coords = load_coords_from_txt(normal_coords_path)
error_coords = load_coords_from_txt(error_coords_path)

# ✅ 좌표 확인 및 예외처리
if not normal_coords or not error_coords:
    print("🚨 좌표 파일이 비어 있습니다. 영상을 다시 확인해주세요.")
    sys.exit()

# ✅ 프레임 하나 선택해서 비교
normal_frame = normal_coords[0]
error_frame = error_coords[0]

similarity = calculate_similarity(normal_frame, error_frame)
print(f"정상 발음 유사도: {similarity}%")

# ✅ 결과 피드백
if similarity >= 85:
    print("✅ 거의 정상에 가깝습니다. 좋은 발음이에요!")
elif similarity >= 60:
    print("⚠️ 약간 차이가 있습니다. 조금 더 연습해보세요.")
else:
    print("❌ 정상 발음에 비해 많이 다릅니다. 입모양을 다시 확인해보세요.")