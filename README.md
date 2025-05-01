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

To run the front end follow these steps:
1. Clone the repository to your computer.
2. Open up the code in Visual Studio or your IDE of preference.
3. Open the terminal of Visual Studio.
4. cd into the /project folder.
5. Run the command
   /docker-shell.sh
6. You should be inside the atomized container. Once your inside the container run the following commands:
   npm install (first time to download necessary packages)
   npm run dev
7. You will get a link that says local host. Copy and paste the local host link into your web browser of preference.
8. Go to the annotator section.
9. You need to input your Gemini API key and a sample patient note that you are interested in annotating.
10. Then, click annotate text, which will give you the annotated patient notes. Each drug attribute is color-coded.
11. If you hover over the drug name you can see the RxNorm ID and can click the link to go to the RxNorm website to learn more information about the drug. 
   
