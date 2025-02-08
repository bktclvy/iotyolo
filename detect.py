import cv2
from ultralytics import YOLO

# YOLOv8モデルの初期化
def load_model(model_path='model_- 2 february 2025 9_14 (1).pt'):
    return YOLO(model_path)

# オレンジのカウントを行う関数
def count_balls(results, target_class='ball'):
    ball_count = 0
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])  # クラスIDを取得
            class_name = result.names[class_id]  # クラス名を取得
            if class_name == target_class:
                ball_count += 1
    return ball_count

# 物体検出を行い、オレンジの数を数える関数
def detect_objects(frame, model):
    results = model(frame, conf=0.5)
    # ball_count = count_balls(results, target_class)
    detection_frame = results[0].plot()  # 検出結果が描画されたフレームを取得
    return detection_frame

# メイン処理
def main():
    model = load_model()  # モデルのロード
    cap = cv2.VideoCapture(0)  # カメラ映像の取得
    print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    if not cap.isOpened():
        print("カメラが開けませんでした。")
        return

    try:
        while True:
            ret, frame = cap.read()
            frame = frame[40:680,320:960]
        
            # frame = frame[640:1280,220:860]
            if not ret:
                print("フレームの取得に失敗しました。")
                break

            cv2.imshow('Real-time Camera Feed', frame)  # リアルタイムの映像を表示

            # スペースキーまたはチェックフラグで物体検出を実行
            key = cv2.waitKey(1) & 0xFF
            if key == ord(' '):
                detection_frame = detect_objects(frame, model)
                cv2.imshow('YOLOv8 Detection Result', detection_frame)

            # 'q'キーで終了
            if key == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
