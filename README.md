# IoT Attack and Security Analysis in Edge Computing Network
The IoT Attack and Security Analysis in Edge Computing Networks is a project focused on detecting and mitigating cyberattacks targeting IoT devices in real-time using machine learning techniques and edge computing. This framework leverages the capabilities of edge nodes, such as a Raspberry Pi, to process and analyze data locally, minimizing latency and enhancing security.

The system integrates IoT devices, including a smart environmental monitoring sensor (DHT11 for temperature and humidity) and a smart bulb, to demonstrate practical IoT device management. The project simulates several common attack scenarios, such as Denial of Service (DoS), Command and Control (C&C) attacks, Horizontal Port Scans, and File Downloads. Machine learning models like Random Forest, XGBoost, and Ensemble are employed for intrusion detection, achieving up to 94.85% accuracy in attack classification. Specifically, the Random Forest model achieved 83.36% accuracy, the Ensemble model reached 94.60% accuracy, and the XGBoost model provided the highest performance with 94.85% accuracy, ensuring robust classification of IoT attacks such as Command and Control (C&C), Denial of Service (DoS), Horizontal Port Scans, and File Downloads.

The framework offers real-time alerts and mitigation capabilities, providing a user-friendly web interface where users can view device statuses, attack logs, and control IoT devices. The system also allows for blocking attackers' IP addresses and downloading detailed logs for further analysis, ensuring rapid response to security threats.

Key tools used in the project include hardware components like the Raspberry Pi 4, DHT11 sensor, and a GPIO-controlled smart bulb, along with software tools such as Python, Flask, TensorFlow, Wireshark, and tcpdump. Machine learning models are trained on the IoT-24 dataset, providing accurate attack classification. Visualization libraries like Matplotlib and Seaborn are used to offer data insights through graphs and charts.

This project demonstrates the effectiveness of combining edge computing with machine learning to enhance the security of IoT networks. It provides a scalable, efficient, and user-friendly solution for detecting and mitigating cyberattacks in real-time.

## 📜 Project Overview

The rapid growth of IoT devices has introduced significant security challenges, especially in edge computing networks. This project aims to address these vulnerabilities by:
- Detecting and mitigating IoT-based cyberattacks in real-time.
- Utilizing edge computing for local data processing and reduced latency.
- Providing a user-friendly web interface for monitoring and control.

### Key Features
- **Edge Computing Node**: Implements a Raspberry Pi 4 as the core processing unit for IoT data and network analysis.
- **IoT Device Integration**: 
  - Smart Environmental Monitoring Sensor for temperature and humidity data.
  - Smart Bulb for actuation and visual feedback.
- **Attack Detection**:
  - Detects attacks like Denial of Service (DoS), Command and Control (C&C), Horizontal Port Scans, and File Downloads.
  - Employs machine learning models with up to 94.85% accuracy.
- **Real-Time Alerts and Mitigation**:
  - Alerts users via a web interface and allows IP blocking of attackers.
  - Logs all events and provides CSV download options.
- **Web Dashboard**: Real-time visualization of device data, attack logs, and system status.

---

## 🚀 Getting Started

### Prerequisites
- **Hardware**:
  - Raspberry Pi 4 (4GB or 8GB RAM)
  - DHT11 Sensor (Temperature & Humidity)
  - Smart Bulb with GPIO interface
- **Software**:
  - Python 3.12
  - TensorFlow 2.18
  - Flask, Scikit-learn, Matplotlib, Seaborn
  - Wireshark, tcpdump
- **Dataset**: IoT-24 Dataset

### Installation
1. Clone the repository:
   ```bash
   git clone https://Chaithanya3116/IoT_Attack_and_Security_Analysis_in_Edge_Computing_Network.git
   cd iot-security-edge

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Set up the Raspberry Pi environment:
- Connect sensors and devices as per the provided schematic.
- Install necessary libraries for GPIO control.

4. Deploy the web interface:
   ```bash
   python app.py

5. Access the dashboard via http://<raspberry-pi-ip>:5000.

## 🧪 Features and Functionality
1. **Edge Computing Node**  
   - Acts as a local processing hub for IoT data.  
   - Hosts pre-trained machine learning models for attack detection.  

2. **Attack Detection**  
   - Detects attacks using machine learning models:  
     - **Random Forest**: 83.36% accuracy  
     - **Ensemble**: 94.60% accuracy  
     - **XGBoost**: 94.85% accuracy  
   - Sends real-time alerts and logs suspicious activity.  

3. **Web Dashboard**  
   - Live monitoring of sensor data (temperature, humidity).  
   - Real-time attack notifications and logs.  
   - IP blocking functionality for threat mitigation.  

4. **Data Visualization**  
   - Graphical representation of attack patterns and environmental data trends.  
   - Downloadable CSV logs for further analysis.  

---

## 🛠️ Tools and Technologies
- **Hardware**: Raspberry Pi 4, DHT11 Sensor, GPIO Smart Bulb  
- **Software**: Python, Flask, TensorFlow, Scikit-learn, Wireshark  
- **Machine Learning**: IoT-24 Dataset, Random Forest, XGBoost, Ensemble Models  
- **Visualization**: Matplotlib, Seaborn  

---

## 📊 Results
| **Model**         | **Accuracy** |
|--------------------|--------------|
| Random Forest      | 83.36%       |
| Ensemble           | 94.60%       |
| XGBoost            | 94.85%       |

The system effectively detects multiple types of attacks in real-time and provides actionable countermeasures, ensuring IoT network security.

---

## 🛤️ Future Scope
- Expand dataset to include more attack types.  
- Improve the user interface for better device management.  
- Explore advanced machine learning techniques like federated learning for enhanced privacy.  

---

## 🤝 Contributors
- **Chaithanya C**  
- **Hemanth Kumar G P**  
- **J Rachana**  
- **Katragadda Sumanth Chowdary**  

---

## 📧 Contact
For queries or contributions, please contact:  
- **Email**: [hakaishin@gmail.com](mailto:hakaishin@gmail.com)  
- **GitHub**: [chaithanya3116](https://github.com/Chaithanya3116)