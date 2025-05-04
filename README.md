# Feel the CUPRA Tavascan - HackUPC 2025

<p align="center">
  <img src="https://github.com/user-attachments/assets/dbad1f2a-cf4a-410f-aaa3-de891e77bc9a" alt="logo2" width="500"/>
  <img src="https://github.com/user-attachments/assets/aa60a680-b543-4750-8989-a7e042b8f9c6" alt="logo3" width="268"/>
</p>


## Authors
- Arnau Claramunt
- Josep Díaz
- Genís López
- Pay Mayench

[![GitHub followers](https://img.shields.io/github/followers/ArnauCS03?label=ArnauCS03)](https://github.com/ArnauCS03) &nbsp;&nbsp; 
[![GitHub followers](https://img.shields.io/github/followers/Nascarin?label=Nascarin)](https://github.com/Nascarin) &nbsp;&nbsp; 
[![GitHub followers](https://img.shields.io/github/followers/GenisLopez5?label=GenisLopez5)](https://github.com/GenisLopez5) &nbsp;&nbsp; 
[![GitHub followers](https://img.shields.io/github/followers/PauMayench?label=PauMayench)](https://github.com/PauMayench) <br><br>

---


>[!IMPORTANT]  
> ### Project Demo and Screenshots can be found at the end of the README.


---

## Project Overview | CUPRA Feel

This project is our implementation of the **Know your CUPRA** challenge, presented at the HackUPC 2025 Hackathon, by the **CUPRA | Seat** company.

The project consists on a groundbreaking digital twin representation of the **Cupra Tavascan 2024** car so that the customers of the model are able to learn all its cutting-edge functionalities without reading the manual. This allows them to enjoy a full exploitation of the car features before they even get the car. 

<br>

This digital twin includes many state of the art functionalities, such as a **3D model** representation of the car integrated with a user-friendly tutorial. In addition to the tutorial, voice interactive **Generative AI** agent is able to answer any user question based on the oficial car user manual using a **RAG strategy**. Moreover, we have implemented a electroencephalograpic (controlled with the mind) driving simulator for the Tavascan.

<br>

---

## 🛠️ Technologies & Tools  

| **Component**        | **Technology**    | **Purpose**                                   |
|----------------------|-------------------|-----------------------------------------------|
| **Visualization**    | Unity             | Creates a 3D visualization of the car and scene.   |
| **Hardware**         | Muse Headband     | Device to understand the brain signals. |
| **AI**               | Gemini 2.0 Flash  | Voice interactive generative AI assistant.  |
| **API Layer**        | FastAPI           | Communication between Muse Headband and Unity. |
| **Integration**      | Docker            | Compatibility of the AI assistant from Linux to Windows. |

---


## Key Features

- **Interactive user-friendly digital twin** to showcase all car features.

When we first open the application, we are presented with a realtime 3D animation of the Cupra Tavascan welcoming the software. This 3D model is the main focus in the application,
since it is the digital-twin that will approach the car to the user before even having it, noticing no differences once you see the physical car. 
A "Know more" button makes the user eager to feel what is like having a Cupra Tavascan after that cinematic introduction, wich when pressed, leads us to a new scene where we can
discover every single one of the features that the car offers to us. A "Learn about..." menu pops up, revealing the possibility to go through 6 different visually and voice assisted tours that guide the user through all the amazing features, without needing to read any manual. Some of this tours have the possibility of you to try out a feature, for example, the car acceleration and braking system, in a physically accurate simulation. 
In every moment, you have the possibility to ask the virtual assistant any question you might have about the car by pressing a button and start talking.
The technologies used for this are Unity3D and C#, using every single feature about Unity: Animations, Lighting, Physics, Interactive UI and integration with all the other project parts.
  
- **Voice interactive AI assistant**: it knows all about the user manual and answer the questions the customer has about the car using:
  - Gemini 2.0 Flash
  - Embeddings (RAG strategy)
  - Voice processing
  - Pipeline: Record user audio -> precess audio and answer based on the manual -> output the response audio and transcript to text

- **Mind controlled physically accurate driving simulation** to showcase the acceleration and brakes of the car.
    
The EEG component is implemented using a Muse EEG headband. Although this device is primarily marketed to help users meditate by monitoring their brainwaves, it also provides real-time measurements of alpha and beta wave activity. Since higher beta wave levels generally correspond to increased mental activity, we can infer whether a person is focused or relaxed.

The headband uses four electrodes positioned near the frontal cortex to capture raw EEG signals. We acquired these signals in Python, then filtered out noise via a Fast Fourier Transform (FFT) to isolate the relevant frequency bands.

Next, we assembled a dataset from the cleaned EEG readings and manually labeled each sampling period as “focused” or “relaxed.” Using this labeled data, we trained a Random Forest classifier to predict mental state from EEG features.

Finally, we integrated the classifier into a simple visualization tool: an orange cube whose behavior—accelerating or braking a simulated car—is controlled by the model’s predictions. We exposed the classifier via a Flask API, allowing the Unity-based simulation to update the car’s speed in real time based on the user’s mental state.


Kinematic equations with the real values of power, torque, acceleration curves, mass etc. are used to build an unprecedented simulator of the acceleraion and braking phases of the car in the most realistic way in Unity3D using the C# programming language. The best of all: it is controlled with the mind through the brain signals explained before. We know equally that, on the one hand, when you buy a Cupra you simply do not look for a regular car, you want the best confort and performance, as well as, on the other hand, the Tavascan represents the most sophisticated and cutting-edge mark of the Brand. This simulation aims to make even the most strict enthusiast fall in love with the car in a way he/she Will not resist it: by being the car and feeling it and its Sporting capabilities.

---

<br>

## Screenshots

### All created from scratch in 36 hours.

![F0](https://github.com/user-attachments/assets/15d5f9a0-cf7c-4b45-a1ce-69290d30af5a)

![F1_1](https://github.com/user-attachments/assets/97f50a95-ec9e-4aab-8528-ac3e16d96f9f)

![F2](https://github.com/user-attachments/assets/443c51f4-efef-4f75-ad2d-f4e8467e8ea1)

![F3_1](https://github.com/user-attachments/assets/26f232ef-38b5-425c-a129-6bf0d05ffc03)

![F4Edited](https://github.com/user-attachments/assets/8d318341-df41-4160-9769-ba4aaf130352)

![F5](https://github.com/user-attachments/assets/6cb98668-a849-4a47-9938-7fd9eeb08a25)

<br>

### Muse headband:

![IMG20250504063325](https://github.com/user-attachments/assets/f581d4aa-62c0-4a85-8eb1-d5f6ecdb0327)


#### During testing, the EEG signal was classified by the ML model as indicating focus, which triggered the car’s brakes.

https://github.com/user-attachments/assets/90e45f24-c5e2-4a2a-a717-d76f5a168fc2

#### Other test when staying focus, the signals of the brain where captured and triggered the acceleration of the car.


https://github.com/user-attachments/assets/6b369952-38ae-4e35-bd08-04d979f0611e



<br>
<br>
