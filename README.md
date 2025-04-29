<h1> AI Tutor in line bot </h1>

1. Install the packages in Models/Requirement
2. Set your own line_channel_id, line_channel_secret, line_token, host_ip, port_ip, openai token in setting_config.py
3. Edit the file path in test.txt, use folder_path/tutor_ai/tutor_ai.py folder_path to activate the line bot API

<h3> Line bot menu looks like </h3>

![menu](https://github.com/user-attachments/assets/69283359-6c46-4e9b-9f4c-a091d8bf41d8)

To connect to the webhook in Line, I recommend Ngrok to connect your local api to https.
Use ngrok http host_ip/port_ip tp start.
