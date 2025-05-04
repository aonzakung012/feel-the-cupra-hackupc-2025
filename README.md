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
  
- **Voice interactive AI assistant**: it knows all about the user manual and answer the questions the customer has about the car using:
  - Gemini 2.0 Flash
  - Embeddings (RAG strategy)
  - Voice processing
  - Pipeline: Record user audio -> precess audio and answer based on the manual -> output the response audio and transcript to text

- **Mind controlled physically accurate driving simulation** to showcase the acceleration and brakes of the car.
    
Muse hardware provided by hackupc, ML trained model to understand the brain signals.
Cinematic equations with the real values of power, torque, acceleration curves, mass etc. are used to build an unprecedented simulator of the acceleraion and braking phases of the car in the most realistic way in Unity3D using the C# programming language. The best of all: it is controlled with the mind through the brain signals explained before. We know equally that, on the one hand, when you buy a Cupra you simply do not look for a regular car, you want the best confort and performance, as well as, on the other hand, the Tavascan represents the most sophisticated and cutting-edge mark of the Brand. This simulation aims to make even the most strict enthusiast fall in love with the car in a way he/she Will not resist it: by being the car and feeling it and its Sporting capabilities.

---

<br>

## Screenshots

![F0](https://github.com/user-attachments/assets/15d5f9a0-cf7c-4b45-a1ce-69290d30af5a)

![F1_1](https://github.com/user-attachments/assets/97f50a95-ec9e-4aab-8528-ac3e16d96f9f)

![F2](https://github.com/user-attachments/assets/443c51f4-efef-4f75-ad2d-f4e8467e8ea1)

![F3_1](https://github.com/user-attachments/assets/26f232ef-38b5-425c-a129-6bf0d05ffc03)

![F4Edited](https://github.com/user-attachments/assets/8d318341-df41-4160-9769-ba4aaf130352)

![F5](https://github.com/user-attachments/assets/6cb98668-a849-4a47-9938-7fd9eeb08a25)

![cupra_bo](https://github.com/user-attachments/assets/c9291779-5761-49b4-a506-8702d5133a34)

<br>
<br>
