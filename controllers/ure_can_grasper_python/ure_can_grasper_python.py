import sys
import cv2
import time
import numpy as np
from controller import Robot

# Sabitler
TIME_STEP = 32
GRIPPER_MIN_POSITION = 0.0495
WAITING, GRASPING, ROTATING, RELEASING, ROTATING_BACK, AVOIDING = range(6)

class CanDetection:
    def __init__(self, robot):
        self.robot = robot
        self.cameras = {}
        self.fallen_detected = False
        self.detection_time = 0
        
        # Frame skipping için (performans)
        self.frame_counter = 0
        self.process_every_n_frames = 3  # Her 3 frame'den birini işle
        
        robot_name = robot.getName()
        print(f"🤖 Robot: {robot_name}")
        
        # Robot-kamera eşleştirmesi
        camera_map = {
            'UR3e': 'camera3',
            'UR5e': 'camera1', 
            'UR10e': 'camera2'
        }
        
        # Sabit ROI - basit ve etkili
        self.roi_config = {
            'camera1': {'x': 0.2, 'y': 0.4, 'w': 0.6, 'h': 0.6},
            'camera2': {'x': 0.2, 'y': 0.4, 'w': 0.6, 'h': 0.6},
            'camera3': {'x': 0.3, 'y': 0.3, 'w': 0.4, 'h': 0.7}
        }
        
        camera_name = camera_map.get(robot_name)
        if camera_name:
            camera = robot.getDevice(camera_name)
            if camera:
                camera.enable(TIME_STEP)
                self.cameras[camera_name] = camera
                print(f"✅ {camera_name} aktif")
        
        print(f"📷 {len(self.cameras)} kamera hazır")
    
    def get_roi(self, frame, camera_name):
        """ROI çıkarma - değişmez"""
        if camera_name not in self.roi_config:
            return frame, (0, 0)
            
        h, w = frame.shape[:2]
        roi = self.roi_config[camera_name]
        
        x1 = int(w * roi['x'])
        y1 = int(h * roi['y'])
        x2 = int(w * (roi['x'] + roi['w']))
        y2 = int(h * (roi['y'] + roi['h']))
        
        roi_frame = frame[y1:y2, x1:x2]
        return roi_frame, (x1, y1)
    
    def detect_red_objects(self, frame):
        """İyileştirilmiş kırmızı tespit"""
        # Daha küçük frame - daha hızlı işlem
        small_frame = cv2.resize(frame, (240, 180))  # 320x240 → 240x180
        hsv = cv2.cvtColor(small_frame, cv2.COLOR_BGR2HSV)
        
        # Optimize edilmiş kırmızı aralıklar
        mask1 = cv2.inRange(hsv, np.array([0, 120, 80]), np.array([10, 255, 255]))
        mask2 = cv2.inRange(hsv, np.array([170, 120, 80]), np.array([180, 255, 255]))
        mask = cv2.bitwise_or(mask1, mask2)
        
        # Tek morfoloji operasyonu
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Orijinal boyuta geri çevir
        mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]))
        return mask
        
    def analyze_contours(self, frame, camera_name):
        """Basit ve etkili contour analizi"""
        roi_frame, offset = self.get_roi(frame, camera_name)
        mask = self.detect_red_objects(roi_frame)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 400:  # Küçük gürültü filtresi
                continue
                
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h if h > 0 else 0
            
            # Ana tespit kriteri - basit ve güvenilir
            if aspect_ratio > 1.5:  # 2.0 → 1.8 (biraz daha hassas)
                return True
                
        return False
        
    def check_cameras(self):
        """Frame skipping ile optimize edilmiş kamera kontrolü"""
        # Frame skipping - performans için
        self.frame_counter += 1
        if self.frame_counter % self.process_every_n_frames != 0:
            return False
            
        current_time = time.time()
        
        # Cooldown kontrolü
        if self.fallen_detected and (current_time - self.detection_time) < 10.0:
            return False
            
        for camera_name, camera in self.cameras.items():
            try:
                image_data = camera.getImageArray()
                if image_data is None:
                    continue
                    
                height = camera.getHeight()
                width = camera.getWidth()
                
                # Hızlı numpy dönüşüm
                if isinstance(image_data, list):
                    image_array = np.array(image_data, dtype=np.uint8)
                else:
                    image_array = image_data.astype(np.uint8)
                
                if image_array.size == height * width * 3:
                    frame = image_array.reshape((height, width, 3))
                    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    
                    # Düşme tespiti
                    has_fallen = self.analyze_contours(frame_bgr, camera_name)
                    
                    if has_fallen and not self.fallen_detected:
                        self.alert_fallen_can(camera_name)
                        self.fallen_detected = True
                        self.detection_time = current_time
                        return True
                        
            except Exception as e:
                print(f"⚠️ Kamera hatası: {e}")
                continue
                
        return False
    
    def reset_detection(self):
        """Tespit flag'ini sıfırla"""
        self.fallen_detected = False
        
    def alert_fallen_can(self, camera_name):
        timestamp = time.strftime("%H:%M:%S")
        print("🚨" * 15)
        print(f"🚨 KUTU DÜŞTÜ! [{timestamp}] - Kamera: {camera_name}")
        print("🚨 Robot kaçınma moduna geçiyor...")
        print("🚨" * 15)

def main():
    robot = Robot()
    
    # Hız ayarı
    speed = 1.2
    if len(sys.argv) > 1:
        try:
            speed = float(sys.argv[1])
        except ValueError:
            speed = 1.2
    
    print(f"🚀 Robot başlatılıyor, hız: {speed}")
    
    # Tespit sistemi
    detector = CanDetection(robot)
    
    # Değişkenler
    counter = 0
    state = WAITING
    target_positions = [-1.88, -2.14, -2.38, -1.51]
    avoid_positions = [2.0, -1.0, -1.0, -1.0]
    last_camera_check = 0
    avoid_start_time = 0
    
    # El motorları
    hand_motors = []
    for motor_name in ["finger_1_joint_1", "finger_2_joint_1", "finger_middle_joint_1"]:
        motor = robot.getDevice(motor_name)
        if motor:
            hand_motors.append(motor)
            motor.setPosition(GRIPPER_MIN_POSITION)
    
    # Kol motorları
    ur_motors = []
    for motor_name in ["shoulder_lift_joint", "elbow_joint", "wrist_1_joint", "wrist_2_joint"]:
        motor = robot.getDevice(motor_name)
        if motor:
            motor.setVelocity(speed)
            ur_motors.append(motor)
    
    # Sensörler
    distance_sensor = robot.getDevice("distance sensor")
    if distance_sensor:
        distance_sensor.enable(TIME_STEP)
        print("✅ Distance sensor aktif")
    
    position_sensor = robot.getDevice("wrist_1_joint_sensor")
    if position_sensor:
        position_sensor.enable(TIME_STEP)
        print("✅ Position sensor aktif")
    
    print("🤖 Robot hazır. Kutu bekleniyor...")
    
    # Ana döngü
    while robot.step(TIME_STEP) != -1:
        current_time = time.time()
        
        # Kamera kontrolü - daha sık kontrol (3 saniye)
        if state == WAITING and current_time - last_camera_check > 2.0:
            fallen_detected = detector.check_cameras()
            if fallen_detected:
                state = AVOIDING
                avoid_start_time = current_time
                print("🏃 Kaçınma modu: Banttan uzaklaşıyorum!")
                for i, motor in enumerate(ur_motors):
                    if i < len(avoid_positions):
                        motor.setPosition(avoid_positions[i])
            last_camera_check = current_time
        
        if counter <= 0:
            if state == WAITING:
                if distance_sensor and distance_sensor.getValue() < 500:
                    print("🎯 Kutu yaklaştı! Yakalıyorum...")
                    state = GRASPING
                    counter = 8
                    for motor in hand_motors:
                        motor.setPosition(0.85)
                        
            elif state == GRASPING:
                if len(ur_motors) >= 4:
                    for i in range(4):
                        ur_motors[i].setPosition(target_positions[i])
                    print("🔄 Kol dönüyor")
                    state = ROTATING
                
            elif state == ROTATING:
                if position_sensor and position_sensor.getValue() < -2.3:
                    counter = 8
                    print("📦 Kutu bırakılıyor")
                    state = RELEASING
                    for motor in hand_motors:
                        motor.setPosition(GRIPPER_MIN_POSITION)
                        
            elif state == RELEASING:
                for motor in ur_motors:
                    motor.setPosition(0.0)
                print("🔄 Kol geri dönüyor")
                state = ROTATING_BACK
                
            elif state == ROTATING_BACK:
                if position_sensor and position_sensor.getValue() > -0.1:
                    state = WAITING
                    print("⏳ Yeni kutu bekleniyor...")
                    
            elif state == AVOIDING:
                # Kaçınma süresi 
                if current_time - avoid_start_time > 7.0:
                    print("✅ Kaçınma tamamlandı, normale dönüyorum")
                    for motor in ur_motors:
                        motor.setPosition(0.0)
                    state = WAITING
                    detector.reset_detection()
        
        counter -= 1

if __name__ == "__main__":
    main()