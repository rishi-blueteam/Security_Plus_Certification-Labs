# Aim:

To demonstrate **CIA Triad** : (Confidentiality, Integrity, and Availability) using practical file operations. This help's me understand concepts theoritically and practically.


## Tools Used for Lab:

- 7-Zip
- PowerShell



## Practical Application

<h3> Confidentiality </h3>

- Use app 7-Zip

  ![7 Zip APP](../../Screenshots/Domain%201_Fundamentals%20%2B%20TA%20%2B%20SC/7ZIP%20App.png)
- Open the folder where you want to encrypt the file

![App Folder Location](../../Screenshots/Domain%201_Fundamentals%20%2B%20TA%20%2B%20SC/7z1_App%20Open%20and%20Encrypt.png)
  
- Add to archive, and 7zip or ZIP format.
- Set Password to your wish
- Security Algorithm (AES256)

![Format and Password](https://github.com/rishi-blueteam/Security-Certification-Labs/blob/main/Screenshots/Domain%201_Fundamentals%20%2B%20TA%20%2B%20SC/7z1_Password_Confidentiality.png)
  
- File Encrypted Visible

![File Encrypted](https://github.com/rishi-blueteam/Security-Certification-Labs/blob/main/Screenshots/Domain%201_Fundamentals%20%2B%20TA%20%2B%20SC/File%20Encrypted.png)

- Open the same file (if .7Z open with 7Zip app itself)
- The file manager will be asking for password


![File attempt Opening](https://github.com/rishi-blueteam/Security-Certification-Labs/blob/main/Screenshots/Domain%201_Fundamentals%20%2B%20TA%20%2B%20SC/C_Triad.png)

- This shows when we are trying to access a file which is password protected, it prevent us to access it as we do not have the right credentials to access it which verifies **Confidentiality**



---------------------------------------------

<h3> Integrity </h3>

- First we create the File, with its **original contents** that file is 

![File Creation](https://github.com/rishi-blueteam/Security-Certification-Labs/blob/main/Screenshots/Domain%201_Fundamentals%20%2B%20TA%20%2B%20SC/7z1_App.png)

![Original Contents](https://github.com/rishi-blueteam/Security-Certification-Labs/blob/main/Screenshots/Domain%201_Fundamentals%20%2B%20TA%20%2B%20SC/File%20Contents%20Original.png)

- To verify integrity we will first open the terminal in the folder where the actual file is located. Powershell opens up
- We list down what all contents are present in the directory using command [ls]
- Now we hash the file to get a encypted code of the respected algorithm which we will be choosing.

**Hash of Original File:**


**SHA-256** :  5E78D49F7EEB65F67D4E6A4CAADF00537C11DA1B4D2BC81FDA5422E2891634BD

**MD5** : E00817721DAA63F650F415478DA6A46

![Original Hash File](https://github.com/rishi-blueteam/Security-Certification-Labs/blob/main/Screenshots/Domain%201_Fundamentals%20%2B%20TA%20%2B%20SC/File%20Hash%20SHA256%26md5.png)

- Now we will modify a charecter in the same file and then verifiy the hash to see if the integrity of the file has changed or no.

![Modified COntent](https://github.com/rishi-blueteam/Security-Certification-Labs/blob/main/Screenshots/Domain%201_Fundamentals%20%2B%20TA%20%2B%20SC/File%20Contents%20Modified.png)

**Hash of Modified File:**

**SHA-256 :**  4F3CCB6D4A110EA8A399682BCBB607868650FEEB64B8CF49B772FF93476A810B

**MD5 :** 595790DC5DFE21F04D0601E89D496F57

![FIle hash modified](https://github.com/rishi-blueteam/Security-Certification-Labs/blob/main/Screenshots/Domain%201_Fundamentals%20%2B%20TA%20%2B%20SC/File%20Hash%20MD5%20%26%20SHA256%20Modified.png)

Since we changed the file's content we are able to verify the files integrity has been changed

--------------------------------

<h3> Availability </h3>

- This is if you are working for an organization you are most likely to have two sets of users present in your Endpoint. One is The host (you) second would be the another user group like admin.

![Users Info](https://github.com/rishi-blueteam/Security-Certification-Labs/blob/main/Screenshots/Domain%201_Fundamentals%20%2B%20TA%20%2B%20SC/Avaliablity%20.png)

- The level of authorization for a specific file varies from user groups. The admin / IT Support groups has full access like the admin.
- The host working for the organization has limited access to resources present in the system
- **Example:** Registry Hive, Program Files, Network Shares and Services

![Different Users Different Access](https://github.com/rishi-blueteam/Security-Certification-Labs/blob/main/Screenshots/Domain%201_Fundamentals%20%2B%20TA%20%2B%20SC/Avaliablity%202.png)

<h3> SOC Real Life </h3>

These are mostly used in areas:

**Confidentiality:** Securing Databases from attackers, and adding multiple layers of security.

**Integrity:** IOC's Data Integrity for prevention of Tampering specially used in Digital Forensics and Incident Response. Practically I have also applied in Network Analsysis and Phishing analysis

**Availability:** These can be specially used if we wish to classify resource access from users of different level of heireacahy in an organization.

## Conclusion:

This lab has not only helped me learn the traid's of Cyber Security which is important for any any organization but has also practically help me explore tools, basic CLI/powershell commands. 







