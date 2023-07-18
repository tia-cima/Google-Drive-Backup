<p align="center">
    <h1 align="center">Google Drive Backup Script</h1>
    <p align="center">An automatic, storage-space friendly and easy way to backup your Google Drive Data</p>
</p>

---


## 📖 Description

Unable to find a program that backs up my Google Drive folder on the internet, I decided to create one myself. This script is designed to automatically download and backup the entirety of a Google Drive folder. It neatly packages all files and directories into a zip file and, in the event of needing a new authentication token or the starting and conclusion of the backup process, will send notifications via email.


## 🌟 Features

- 📥 Downloads all files and directories from Google Drive.
- 🗜️ Zips the downloaded data for efficient storage.
- 📧 Emails notifications at the start and end of the backup process, as well as when a new token is needed for Google Drive API.
- 🧹 Automatically deletes the downloaded data after a successful backup.
- 💾 Save space and retain only a chosen amount of backups by eliminating older ones.


## 🔍 Prerequisites

Before running the script, ensure that you have the following prerequisites:

- Python 3.6 or higher installed on your machine.
- Python added to your system's PATH environment variable.


## ⚙️ Setup and Installation

1. **Clone the repository**
    You can clone the repository using the following command:

    ```shell
    git clone https://github.com/tia-cima/Google-Drive-Backup.git
    cd google-drive-backup
    ```

2. **Install dependencies**
    Use pip to install the necessary Python libraries:

    ```shell
    pip install -r requirements.txt
    ```

3. **Set up Google Drive API**
    This script uses Google Drive API to access and download your data. Follow the steps below to set up the API:

    1. **Create a new project on Google Cloud Platform (GCP)**:
       - Go to the [Google Cloud Console](https://console.cloud.google.com/).
       - Click the project drop-down and select or create the project for which you want to add an API key.
       - Click the hamburger menu in the top left and select **APIs & Services** > **Library**.

    2. **Enable Google Drive API for your project**:
       - In the API Library, search for "Google Drive API".
       - Click on "Google Drive API" in the search results.
       - Click on **Enable**.

    3. **Create credentials for the Google Drive API**:
       - Go to **APIs & Services** > **Credentials**.
       - Click on **+ CREATE CREDENTIALS** and select **OAuth client ID**.
       - Configure the OAuth consent screen as needed. For the User Type, you can select "External" and click **Create**.
       - Fill in the necessary information for the OAuth consent screen and click **Save and Continue**.
       - For the Application type, select **Desktop app** and give it a name.
       - Click on **Create**.
       - Your client ID and client secret will be displayed. These values will be used in your Python script to access the Google Drive API.

    4. **Download the JSON file with your credentials**:
       - After creating your credentials, go back to the **Credentials** page.
       - In the **OAuth 2.0 Client IDs** section, find the client you just created.
       - Click on the download icon to download the JSON file. This file will be referred to as your "client_json" in the script.
       - Keep this JSON file secure, as it contains sensitive information about your application's access permissions.

    Note: The first time you run the script, you will be prompted to authorize the app with Google Drive. After authorizing, a new file `token.pickle` will be created. This token will be used for future authentications and you will not be prompted to authorize again unless the token becomes invalid.

4. **Set up SendGrid**
    This script uses SendGrid for email notifications. You'll need to create an API key in your SendGrid account in order to send notifications about your backup status (is free). 
    This step is optional, I understand you may not want to create another account for something you'll use only for this program, so when inserting the values you can skip the "Sendgrid API key, from_email and to_email" values, the program will handle this.
    
    If you decide to proceed with SendGrid, here are the steps to configure properly your account:

    1. **Create a new SendGrid account**:
       - Visit the [SendGrid website](https://sendgrid.com/) and sign up for a free account.

    2. **Verify your email address**:
       - After signing up, verify your email address by clicking on the link in the email sent by SendGrid.

    3. **Create a new API Key**:
       - Once you're in the SendGrid dashboard, go to **Email API** on the left navigation bar and click on **Integration Guide**.
       - Select **Web API** (not SMTP Relay).
       - Click on **Choose** under **Integrate using our Web API or SMTP relay**.
       - Give your API Key a name and select either **Full Access** or **Restricted Access**. For this application, we only need the ability to send mail.
       - In the **Restricted Access** section, expand **Mail Send** and switch the toggle to **Enabled**.
       - Click on **Create & View** to create the new API Key.
       - Your new API Key will be displayed. Copy and save this key securely. Remember that this is the only time you'll be able to access this key via the SendGrid interface. If you lose it, you'll have to create a new one.

    4. **Enable "Mail Send" permissions**:
       - Go to the **API Keys** section under **Settings**.
       - Click on the name of the API Key you've just created.
       - In the **API Key Permissions** section, set **Mail Send** to **Full Access**.

    Your SendGrid API setup is now complete! Keep your API key secure as it allows sending emails from your account. In the backup script, you will use this key as the `sendgrid_api_key` variable. You can now send transactional emails through your Python application.

    Note: With a free SendGrid account, you can send up to 100 emails per day. If you need to send more than that, you will need to upgrade your account. Unfortunately, I had no choice but to use Sendgrid for sending emails. Using the default python mail functions, after a few days of non-stop mails, Gmail began to block its reception despite the program sent them without problems.

    IMPORTANT! You can choose whatever email address use to send emails with, but they'll likely go into the spam folder because they're not verified. You can verify a particular email address at this link: https://docs.sendgrid.com/ui/sending-email/sender-verification. Remember to use the same email address you just verified as "from_email" address.

5. **Run the script**
    You can run the script using the CLI or the UI: 

    1. **Using UI script (Recommended)**:
       - Open your terminal and navigate in the folder where the backup.py and ui.py files are located. Run the command `python ui.py`
       - You can also double-click on ui.py file in order to open it.
       - When the window opens, simply insert the required values. 
       - You can click on the "info" button to see more details.
       - You can also save you current data by clicking on "save configuration" and selecting the json file path. IMPORTANT! Store this file in a secure location because it can contain sensitive data. I recommend storing it in the same directory as client.json and token.pickle, I'll explain later.
       - You can also load a different configuration by clicking on "load configuration". The input fields will be filled.
       - When your selected input fields are filled, you can click on "start backup" and then click on "ok". A new terminal window will open, showing the backup status or possible errors.
       - Don't close any of these two windows or the backup process will stop. 

    2. **Using CLI**:
       - Open your terminal and navigate in the folder where the backup.py file is located.
       - Type the following command, replacing the values in <> with the correct values: `python backup.py --download_folder <folder to download files> --backup_folder <folder to save the backup> --sendgrid_api_key <your SendGrid API key> --from_email <email to send notifications from> --to_email <email to send notifications to> --client_json <path to your Google client json> --hour <hour to start the backup> --minute <minute to start the backup>`
       - Each value is explained here: 
            - `download_folder`: This is the folder where the files from Google Drive will be downloaded.
            - `backup_folder`: This is the folder where the downloaded files will be zipped and saved as a backup.
            - `client_json`: The path to your Google client json file. This is used to authenticate the script with Google Drive.
            - `hour` and `minute`: The time at which the script will run every day.
            - `hour` and `minute`: The time at which the script will run every day.
            - `retention_days`: How many days to retain old backups. For instance, if you want to retain 5 days of backup, you'll have 5 zip in total and everytime the program creates a new zip, the oldest one will be eliminated.
            - `sendgrid_api_key`: Your SendGrid API key for sending email notifications. (optional)
            - `from_email`: The email address that will be used to send notifications. (optional - requires SendGrid API key)
            - `to_email`: The email address that will receive notifications. (optional - requires SendGrid API key)
       - The script will now run continuously and start the backup process at the given hour and minute every day.

    The args "sendgrid_api_key", "from_email" and "to_email" are optional, so you can skip them and run the script without the email notification feature.


## 💡 Recommended Settings

The 'token.pickle' file, which is used for Google Drive authentication, will be saved in the same directory as `backup.py` and `ui.py`. This file stores the Google Drive API token and it's auto-generated by the APIs, so don't worry if you'll find it in the folder.

I also recommend putting, in the 'token.pickle' folder, the 'client_json...' file, in order to have it all in one single folder. Save here also your config.json or whatever name you choose to assign to it. Then, save this whole folder in a secure location, because it contains sensitive data about your Google account and the sendgrid API key. 
You don't need to store also the backup and download folder in a secure location because you can select whatever path you want for them, also a non-secure one.

Is important to name the folders you're going to use without spaces, sometimes it can be a problem in an environment like raspberry pi OS. If you want to divide words, use _ or -.


## 📒 Notes

Keep in mind that only the number of backups you will choose via "retention_days" will be kept, so older backups than "retention_days" will be eliminated.

The "hour" and "minute" must be in H24 format. AM and PM aren't supported, so if you want to start backup at 9PM, you'll have to write 21. For starting the script at 12AM, or 00:00, insert "0".

Unfortunately, this application will result in google’s cloud environment as a test app, so every 7 days a new authentication will be required, blocking the script. You will then need, every 7 days, to access the machine in order to reconfirm the token. 
If you can't access your script because you're on vacation or simply not in your home network, you can setup an OpenVPN server on a device like a raspberry pi, so you can access your home network from anywhere in the world and connect to your machine when a new token is needed. Follow the instruction at this link: https://www.wundertech.net/openvpn-raspberry-pi-setup-instructions/.
If your home network changes frequently IP address, you can buy a DDNS to associate with your home network in order to use the DDNS instead of the IP address when configuring OpenVPN. You will no longer have problems connecting to the vpn even if your network changes ip frequently since the DDNS will always point to your network.

In order to request a new token when needed, you can simply access the machine where you're running the script, deleting the old token.pickle file and restart the script changing "hour" and "minute" in order to make the script run instantly. A browser window will open where you have to go through the usual authentication process. Stop the current instance of the program and restart it with the correct "hour" and "time".


## 📄 License

This project is licensed under the terms of the MIT license. See the [LICENSE](https://github.com/tia-cima/Google-Drive-Backup/blob/master/LICENSE.txt) file for details.
