import cv2
from ultralytics import YOLO
import flag_set

# YOLOv8モデルの初期化
def load_model(model_path='yolov8n.pt'):
    return YOLO(model_path)

# オレンジのカウントを行う関数
def count_oranges(results, target_class='orange'):
    orange_count = 0
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])  # クラスIDを取得
            class_name = result.names[class_id]  # クラス名を取得
            if class_name == target_class:
                orange_count += 1
    return orange_count

# 物体検出を行い、オレンジの数を数える関数
def detect_objects(frame, model, target_class='orange'):
    results = model(frame)
    orange_count = count_oranges(results, target_class)
    detection_frame = results[0].plot()  # 検出結果が描画されたフレームを取得
    return detection_frame, orange_count

# メイン処理
def main():
    model = load_model()  # モデルのロード
    cap = cv2.VideoCapture(0)  # カメラ映像の取得
    if not cap.isOpened():
        print("カメラが開けませんでした。")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("フレームの取得に失敗しました。")
                break

            cv2.imshow('Real-time Camera Feed', frame)  # リアルタイムの映像を表示

            # スペースキーまたはチェックフラグで物体検出を実行
            key = cv2.waitKey(1) & 0xFF
            check_flag = flag_set.check_buttom_flag()
            if check_flag == 1:
                detection_frame, orange_count = detect_objects(frame, model)
                cv2.imshow('YOLOv8 Detection Result', detection_frame)

                if orange_count == 5:
                    flag_set.result_out(1)
                else:
                    flag_set.result_out(2)

            # 'q'キーで終了
            if key == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
