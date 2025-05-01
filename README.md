# BMI702FinalProject

To first access MIMIC data, you need to become a credentialed user.

To get credentialed: https://physionet.org/settings/training/

Once you get credentialed, follow these steps to get the data:
1. To get the prescription.csv file go to the website: https://physionet.org/content/mimiciv/3.1/#files-panel
2. Then run the command: wget -r -N -c -np --user <username> --ask-password https://physionet.org/files/mimiciv/3.1/ (we suggest you use the no hup command or caffinate command to allow the download to happen in the background)
3. The prescription.csv file will be under the /hosp folder
4. To get the discharge.csv file go to the website: https://www.physionet.org/content/mimic-iv-note/2.2/#files-panel
5. Then run the command: wget -r -N -c -np --user <username> --ask-password https://physionet.org/files/mimic-iv-note/2.2/ (we suggest you use the no hup command or caffinate command to allow the download to happen in the background)
6. The discharge.csv file will be under the /note folder

To use our tool you need to get API access to gemini, which can be done by following this link: https://ai.google.dev/gemini-api/docs/api-key
