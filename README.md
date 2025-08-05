# 🤖 Industrial Robot Vision System
## Automatic Box Detection and Collision Avoidance System for Multi-Robot Assembly Line

*[Türkçe versiyonu aşağıda bulabilirsiniz / Turkish version available below](#türkçe-versiyon)*

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-green.svg)](https://opencv.org)
[![Webots](https://img.shields.io/badge/Webots-R2023a+-orange.svg)](https://cyberbotics.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Real-time computer vision system for industrial robots detecting falling objects on conveyor belts.**

<img width="755" height="602" alt="image" src="https://github.com/user-attachments/assets/3d38d8fc-05a9-402b-bece-f5eb676f5238" />


## 🎯 Project Overview

This project enhances multi-robot assembly line simulation with intelligent vision-based safety features. Three industrial robot arms (UR3e, UR5e, UR10e) work collaboratively in a conveyor belt system, automatically detecting falling boxes and performing avoidance behaviors to prevent collisions.

### 🔥 Key Features

- **🎥 Multi-Camera Vision System**: Real-time monitoring with 3 industrial cameras
- **🚨 Smart Fall Detection**: Advanced computer vision algorithms detecting falling objects
- **⚡ Automatic Collision Avoidance**: Robots automatically move to safe positions when danger is detected
- **🔄 Intelligent State Management**: Advanced finite state machine for seamless operation
- **⚙️ Performance Optimization**: Frame skipping and ROI processing for real-time performance
- **🛡️ Safety-First**: Built-in cooldown mechanisms and error handling

## 🏭 System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   UR3e Robot    │    │    UR5e Robot    │    │   UR10e Robot   │
│   + Camera3     │    │    + Camera1     │    │   + Camera2     │
└─────────┬───────┘    └─────────┬────────┘    └─────────┬───────┘
          │                      │                       │
          └──────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────▼──────────────┐
                    │   Vision Controller        │
                    │  - Object Detection        │
                    │  - State Management        │
                    │  - Collision Avoidance     │
                    └────────────────────────────┘
```

## 🛠️ Technologies Used

| Technology | Purpose | Version |
|-----------|---------|----------|
| **Python** | Main programming language | 3.7+ |
| **OpenCV** | Computer vision and image processing | 4.0+ |
| **NumPy** | Numerical computations | Latest |
| **Webots** | Robot simulation environment | R2023a+ |

## 🚀 Quick Start

### Prerequisites
```bash
# Install required packages
pip install opencv-python numpy

# Download Webots: https://cyberbotics.com
```

### Installation
```bash
git clone https://github.com/username/industrial-robot-vision.git
cd industrial-robot-vision
```

### Running the Simulation
1. Open Webots
2. Load world file: `worlds/industrial_assembly.wbt`
3. Run controller: `controllers/robot_vision_controller.py`

```bash
# Optional: Set custom robot speed
python robot_vision_controller.py 1.5  # 1.5x speed
```

## 🎮 How It Works

### 1. **Image Processing Pipeline**
- **ROI Extraction**: Focus on conveyor belt areas for efficient processing
- **HSV Color Filtering**: Robust red object detection under variable lighting
- **Morphological Operations**: Noise reduction and shape enhancement
- **Contour Analysis**: Aspect ratio analysis to detect falling objects

### 2. **State Machine**
```python
WAITING → CAPTURING → ROTATING → DROPPING → RETURNING
    ↓
AVOIDING (when falling object detected)
```

### 3. **Collision Avoidance Algorithm**
```python
# Falling object detected
if fallen_detected:
    robot.move_to_safe_position([2.0, -1.0, -1.0, -1.0])
    wait(5_seconds)
    robot.return_to_normal_operation()
```

## 🔧 Configuration

### Robot-Camera Mapping
```python
camera_map = {
    'UR3e': 'camera3',   # Precision tasks
    'UR5e': 'camera1',   # General purpose  
    'UR10e': 'camera2'   # Heavy lifting
}
```

### Adjustable Parameters
- **Detection Sensitivity**: Aspect ratio threshold (default: 1.5)
- **Cooldown Duration**: Preventing repeated alerts (default: 10s)
- **Processing Speed**: Frame skipping interval (default: every 3rd frame)
- **Safety Timeout**: Avoidance behavior duration (default: 5s)

---

## Türkçe Versiyon

*[English version above / İngilizce versiyon yukarıda](#industrial-robot-vision-system)*

# 🤖 Endüstriyel Robot Görü Sistemi
## Çok Robotlu Montaj Hattı için Otomatik Kutu Tespiti ve Çarpışma Kaçınma Sistemi

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-green.svg)](https://opencv.org)
[![Webots](https://img.shields.io/badge/Webots-R2023a+-orange.svg)](https://cyberbotics.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Konveyör bantlarında düşen nesneleri tespit eden endüstriyel robotlar için gerçek zamanlı bilgisayarlı görü sistemi.**

<img width="755" height="602" alt="image" src="https://github.com/user-attachments/assets/44a8c449-dd3d-4549-9eec-516c88e46933" />


## 🎯 Proje Genel Bakış

Bu proje, çok robotlu montaj hattı simülasyonunu akıllı görü tabanlı güvenlik özellikleri ile geliştirmektedir. Üç endüstriyel robot kolu (UR3e, UR5e, UR10e) konveyör bant sisteminde işbirliği içinde çalışarak, düşen kutuları otomatik olarak tespit eder ve çarpışmaları önlemek için kaçınma davranışları sergiler.

### 🔥 Temel Özellikler

- **🎥 Çoklu Kamera Görü Sistemi**: 3 endüstriyel kamera ile gerçek zamanlı izleme
- **🚨 Akıllı Düşme Tespiti**: Düşen nesneleri tespit eden gelişmiş bilgisayarlı görü algoritmaları
- **⚡ Otomatik Çarpışma Kaçınma**: Tehlike tespit edildiğinde robotlar otomatik olarak güvenli pozisyonlara geçer
- **🔄 Akıllı Durum Yönetimi**: Sorunsuz çalışma için gelişmiş sonlu durum makinesi
- **⚙️ Performans Optimizasyonu**: Gerçek zamanlı performans için frame atlama ve ROI işleme
- **🛡️ Güvenlik Öncelikli**: Yerleşik cooldown mekanizmaları ve hata yakalama

## 🏭 Sistem Mimarisi

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   UR3e Robot    │    │    UR5e Robot    │    │   UR10e Robot   │
│   + Kamera3     │    │    + Kamera1     │    │   + Kamera2     │
└─────────┬───────┘    └─────────┬────────┘    └─────────┬───────┘
          │                      │                       │
          └──────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────▼──────────────┐
                    │     Görü Kontrolcüsü       │
                    │  - Nesne Tespiti           │
                    │  - Durum Yönetimi          │
                    │  - Çarpışma Kaçınma        │
                    └────────────────────────────┘
```

## 🛠️ Kullanılan Teknolojiler

| Teknoloji | Amaç | Versiyon |
|-----------|------|----------|
| **Python** | Ana programlama dili | 3.7+ |
| **OpenCV** | Bilgisayarlı görü ve görüntü işleme | 4.0+ |
| **NumPy** | Sayısal hesaplamalar | En son |
| **Webots** | Robot simülasyon ortamı | R2023a+ |

## 🚀 Hızlı Başlangıç

### Ön Gereksinimler
```bash
# Gerekli paketleri yükleyin
pip install opencv-python numpy

# Webots'u indirin: https://cyberbotics.com
```

### Kurulum
```bash
git clone https://github.com/kullaniciadi/endustriyel-robot-goru.git
cd endustriyel-robot-goru
```

### Simülasyonu Çalıştırma
1. Webots'u açın
2. Dünya dosyasını yükleyin: `worlds/industrial_assembly.wbt`
3. Kontrolcüyü çalıştırın: `controllers/robot_vision_controller.py`

```bash
# İsteğe bağlı: Özel robot hızı ayarlayın
python robot_vision_controller.py 1.5  # 1.5x hız
```

## 🎮 Nasıl Çalışır

### 1. **Görüntü İşleme Pipeline**
- **ROI Çıkarımı**: Verimli işleme için konveyör bant alanlarına odaklanır
- **HSV Renk Filtreleme**: Değişken aydınlatma altında güçlü kırmızı nesne tespiti
- **Morfolojik İşlemler**: Gürültü azaltma ve şekil iyileştirme
- **Kontur Analizi**: Düşen nesneleri tespit etmek için en-boy oranı analizi

### 2. **Durum Makinesi**
```python
BEKLEME → YAKALAMA → DÖNDÜRME → BIRAKMA → GERİ_DÖNME
    ↓
KAÇINMA (düşen nesne tespit edildiğinde)
```

### 3. **Çarpışma Kaçınma Algoritması**
```python
# Düşen nesne tespit edildi
if fallen_detected:
    robot.move_to_safe_position([0.5, -1.0, -1.0, -1.0])
    wait(5_saniye)
    robot.return_to_normal_operation()
```

## 🔧 Konfigürasyon

### Robot-Kamera Eşleştirmesi
```python
camera_map = {
    'UR3e': 'camera3',   # Hassas görevler
    'UR5e': 'camera1',   # Genel amaçlı  
    'UR10e': 'camera2'   # Ağır kaldırma
}
```

### Ayarlanabilir Parametreler
- **Tespit Hassasiyeti**: En-boy oranı eşiği (varsayılan: 1.5)
- **Cooldown Süresi**: Tekrarlanan uyarıları önleme (varsayılan: 10s)
- **İşleme Hızı**: Frame atlama aralığı (varsayılan: her 3. frame)
- **Güvenlik Zaman Aşımı**: Kaçınma davranışı süresi (varsayılan: 5s)
