import cv2


def preview_camera() -> None:
    """Display a simple camera preview using OpenCV."""
    # 카메라 열기 (0번 장치는 일반적으로 기본 웹캠입니다)
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        return

    if not cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1):
        print("자동 노출을 설정할 수 없습니다.")

    if not cap.set(cv2.CAP_PROP_GAIN, 100):
        print("게인을 설정할 수 없습니다.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임을 읽을 수 없습니다.")
            break

        # 화면에 프레임 출력
        cv2.imshow("Camera Preview", frame)

        # q를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 리소스 정리
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    preview_camera()

