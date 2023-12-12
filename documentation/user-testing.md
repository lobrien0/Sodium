# User Testing

This will go over the process you can use for user testing

## Description

Because this project is based off unix Shadow files, you can use this program on your system's shadow file in order to test the program.

This program doesn't write anything, so the `shadow` file won't be edited. Just read.

## Steps for testing

1. In order to test this, first open the `shadow` file you'd like to use. You can use something like `vim` or `nano` with superuser

   ```bash
   sudo vim /etc/shadow
   ```

   --

2. Once you have the `shadow` file open, make sure that the default account (your account) doesn't have `$y$` after the account name. If it does have `$y$` after your account name, then go to `Yes-Crypt Workaround`

   example of what it would look like:

   ```
   userAccount:$y$j9T$tnfO3OZnoQI6AF156D8Tf3Hc$GxLWI1bQBC5184y9NbV91GayK5iTMGYAv
   ```
   > Note: this example does have `$y$` this means `YesCrypt` was used to generate the hash.

   --

3. After closing the shadow file, we must create a test account in order to perform the testing.  
   To do this, please enter the following command:

   ```bash
   sudo useradd alice
   ```

   --

4. Now that the `alice` account is made, we must set Alice's password.  
   To do that, please enter this command:

   ```bash
   sudo passwd alice
   ```

   > Note: If your shadow file had `$y$` in it, please go to `Yes-Crypt Work Around` instead of running this command

   For testing, set the password to something in your password list, or the provided `top100k.txt`.  
   Normally this list represents the passwords being checked against in a breach.

   --

5. Now that we have the user account added, we can run the program
   Using the `manage.py` file.  
   Please enter this command:

   ```bash
   sudo python manage.py /etc/shadow top100k.txt alice
   ```

   > If you want to use your password list, replace `top100k.txt` with the path to your own list.

   > `sudo` is used since `shadow` is protected
   > 
   > If you would prefer not to enter the `shadow` file directly, you can create a copy of the `shadow` file and use the path to the copy instead

   the command above will start the program in debugging mode and only compute the user `alice` (to save time)

   --

## Yes-Crypt Work Around

If your user's hash had `$y$` in it, this means your system uses a hashing algorithm called `Yes-Crypt`. Which this program is not designed to handle (yet).

In order to get around this, you must manually create the password for the `alice` account.

1. Install `OpenSSL` for your system

   Apt:

   ```bash
   sudo apt update
   sudo apt install openssl
   ```
   Yum:

   ```bash
   sudo yum install openssl
   ```

   Zypper:

   ```bash
   sudo zypper install openssl
   ```

   --

2. After `OpenSSL` is installed, Run the command:

   ```bash
   sudo usermod --password $(openssl passwd -6 'Password') alice
   ```
   > `Password` can be changed to whatever you'd like it to be.

   OpenSSL allows us to compute a SHA-512 hash for Alice manually since the system defaults to `Yes-Crypt`

   --

3. Return to `step 5` in [Steps For Testing](#steps-for-testing)
