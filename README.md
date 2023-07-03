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
    This script uses SendGrid for email notifications. You'll need to create an API key in your SendGrid account. Here are the steps:

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

    Remember to replace the `SENDGRID_API_KEY` variable in the script with your generated API key.
    Your SendGrid API setup is now complete! Keep your API key secure as it allows sending emails from your account. In the backup script, you will use this key as the `sendgrid_api_key` variable. You can now send transactional emails through your Python application.
    Note: With a free SendGrid account, you can send up to 100 emails per day. If you need to send more than that, you will need to upgrade your account.

5. **Run the script**
    You can run the script using the following command: 

    `python backup.py --download_folder <folder to download files> --backup_folder <folder to save the backup> --sendgrid_api_key <your SendGrid API key> --from_email <email to send notifications from> --to_email <email to send notifications to> --client_json <path to your Google client json> --hour <hour to start the backup> --minute <minute to start the backup>`

    - `download_folder`: This is the folder where the files from Google Drive will be downloaded.
    - `backup_folder`: This is the folder where the downloaded files will be zipped and saved as a backup.
    - `sendgrid_api_key`: Your SendGrid API key for sending email notifications.
    - `from_email`: The email address that will be used to send notifications.
    - `to_email`: The email address that will receive notifications.
    - `client_json`: The path to your Google client json file. This is used to authenticate the script with Google Drive.
    - `hour` and `minute`: The time at which the script will run every day.
    
    Replace the arguments with your desired settings. The script will run continuously and start the backup process at the given hour and minute.


## 💡 Recommended Settings

The 'token.pickle' file, which is used for Google Drive authentication, will be saved in the directory above the download and backup folders. For instance, if your download folder is "C:\Users\your_user\Desktop\test\d" and your backup folder is "C:\Users\your_user\Desktop\test\b", the 'token.pickle' file will be saved in "C:\Users\your_user\Desktop\test". Please ensure that you have write access to this directory.

I also recommend to put, in the future 'token.pickle' folder, the 'client_json...' file, in order to have all in one single folder.


## 📄 License

This project is licensed under the terms of the MIT license. See the [LICENSE](https://github.com/tia-cima/Google-Drive-Backup/blob/master/LICENSE.txt) file for details.
