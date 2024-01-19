# Voicera - Academic Certificates IVRS System

## Description

The Academic Certificates IVRS (Interactive Voice Response System) is a streamlined application designed to facilitate the ordering and delivery of academic certificates. The system integrates Twilio for call management, connecting users to the Flask backend. This backend leverages DTMF (Dual-Tone Multi-Frequency) decoding and speech recognition to ensure accurate interaction and routing of requests. The system also includes payment processing for a seamless user experience.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Tech Stack

- Python
- Flask
- Twilio
- MongoDB

## Installation

To install the Academic Certificates IVRS System, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/academic-certificates-ivrs.git
   ```

2. Navigate to the project directory:

   ```bash
   cd code
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the Twilio account and configure the necessary credentials in the Flask backend.

5. Configure MongoDB connection settings in the Flask backend.

## Usage

1. Start the Flask backend:

   ```bash
   python app.py
   ```

2. Set up the Twilio phone number to forward incoming calls to the Flask backend.

3. Users can call the provided Twilio phone number to interact with the IVRS for ordering academic certificates. The system will handle call management, DTMF decoding, speech recognition, and payment processing.

## Contributing

We welcome contributions to enhance the Academic Certificates IVRS System. To contribute, follow these steps:

1. Fork the project.
2. Create a new branch for your feature: `git checkout -b feature/new-feature`.
3. Commit your changes: `git commit -am 'Add new feature'`.
4. Push to the branch: `git push origin feature/new-feature`.
5. Submit a pull request.

## Contact

For any inquiries or support, please contact at hrutuselar@gmail.com.
