#imports
import string
import random
import requests
import json
import getpass
import steam
import steam.webauth as wa
import colorama
from colorama import *
import time
import os

colorama.init()

def steamiscool():
    print(Fore.RED + """
░██████╗████████╗███████╗░█████╗░███╗░░░███╗  ░██████╗░███████╗███╗░░██╗
██╔════╝╚══██╔══╝██╔════╝██╔══██╗████╗░████║  ██╔════╝░██╔════╝████╗░██║
╚█████╗░░░░██║░░░█████╗░░███████║██╔████╔██║  ██║░░██╗░█████╗░░██╔██╗██║
░╚═══██╗░░░██║░░░██╔══╝░░██╔══██║██║╚██╔╝██║  ██║░░╚██╗██╔══╝░░██║╚████║
██████╔╝░░░██║░░░███████╗██║░░██║██║░╚═╝░██║  ╚██████╔╝███████╗██║░╚███║
╚═════╝░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝  ░╚═════╝░╚══════╝╚═╝░░╚══╝

░█████╗░██╗░░██╗███████╗░█████╗░██╗░░██╗███████╗██████╗░
██╔══██╗██║░░██║██╔════╝██╔══██╗██║░██╔╝██╔════╝██╔══██╗
██║░░╚═╝███████║█████╗░░██║░░╚═╝█████═╝░█████╗░░██████╔╝
██║░░██╗██╔══██║██╔══╝░░██║░░██╗██╔═██╗░██╔══╝░░██╔══██╗
╚█████╔╝██║░░██║███████╗╚█████╔╝██║░╚██╗███████╗██║░░██║
░╚════╝░╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝
""" + Fore.RESET)
    y = input(Fore.CYAN + "Do you want to generate codes? [yes/no]: ")
    if (y)==("yes"):
        def bla():
            codelen = 5
            bros = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            return ''.join(random.choice(bros) for i in range(codelen))

        def blb():
            codelen = 5
            bros = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            return ''.join(random.choice(bros) for i in range(codelen))

        def blc():
            codelen = 5
            bros = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            return ''.join(random.choice(bros) for i in range(codelen))

        j = int(input("Enter the number of codes you want to print: "))
        for i in range (j):
            print(bla(), "-", blb(), "-", blc(),sep="")
        l = input(Fore.MAGENTA + "COPY THE CODES AND PASTE IT IN keys.txt AND PRESS ENTER!")
        if (l)==(""):
            print(Fore.GREEN + "Welcome to the steam code checker!")
            
            keyFileName = "keys.txt"
            p = input(Fore.YELLOW + "Enter your steam username!: ")
            b = input(Fore.YELLOW + "Enter the password for the steam account!: ")
            user = wa.WebAuth(p, b)
            
            try:
                    user.login()
            except wa.CaptchaRequired:
                print(user.captcha_url)
                code = input(Fore.RED + "Please follow the captcha url, enter the code below:\n")
                user.login(captcha=code)
            except wa.EmailCodeRequired:
                code = input(Fore.RED + "Please enter emailed 2FA code:\n")
                user.login(email_code=code)
            except wa.TwoFactorCodeRequired:
                code = input(Fore.RED + "Please enter 2FA code from the Steam app on your phone:\n")
                user.login(twofactor_code=code)

    # Get the sesssion ID, required for the ajax key auth
            sessionID = user.session.cookies.get_dict()["sessionid"]

            keys = []
            f = open(keyFileName)
            for line in f:
                keys.append(line)

    # Iterate over keys, if you need faster than this for some unknown reason you've probably got the skill to make this faster.
            for key in keys:
                r = user.session.post('https://store.steampowered.com/account/ajaxregisterkey/', data={'product_key' : key, 'sessionid' : sessionID})
                blob = json.loads(r.text)

        # Success
                if blob["success"] == 1:
                    for item in blob["purchase_receipt_info"]["line_items"]:
                        print(Fore.GREEN + "[ Redeemed ]", item["line_item_description"])
                else:
            # Error codes from https://steamstore-a.akamaihd.net/public/javascript/registerkey.js?v=qQS85n3B1_Bi&l=english
                    errorCode = blob["purchase_result_details"]
                    sErrorMessage = ""
                    if errorCode == 14:
                        sErrorMessage = 'The product code you\'ve entered is not valid. Please double check to see if you\'ve mistyped your key. I, L, and 1 can look alike, as can V and Y, and 0 and O.'

                    elif errorCode == 15:
                        sErrorMessage = 'The product code you\'ve entered has already been activated by a different Steam account. This code cannot be used again. Please contact the retailer or online seller where the code was purchased for assistance.'

                    elif errorCode == 53:
                        sErrorMessage = 'The product code you\'ve entered is not valid. Please double check to see if you\'ve mistyped your key. I, L, and 1 can look alike, as can V and Y, and 0 and O.'

                    elif errorCode == 13:
                        sErrorMessage = 'Sorry, but this product is not available for purchase in this country. Your product key has not been redeemed.'

                    elif errorCode == 9:
                        sErrorMessage = 'This Steam account already owns the product(s) contained in this offer. To access them, visit your library in the Steam client.'

                    elif errorCode == 24:
                        sErrorMessage = 'The product code you\'ve entered requires ownership of another product before activation.\n\nIf you are trying to activate an expansion pack or downloadable content, please first activate the original game, then activate this additional content.'

                    elif errorCode == 36:
                            sErrorMessage = 'The product code you have entered requires that you first play this game on the PlayStation®3 system before it can be registered.\n\nPlease:\n\n- Start this game on your PlayStation®3 system\n\n- Link your Steam account to your PlayStation®3 Network account\n\n- Connect to Steam while playing this game on the PlayStation®3 system\n\n- Register this product code through Steam.'

                    elif errorCode == 50: 
                        sErrorMessage = 'The code you have entered is from a Steam Gift Card or Steam Wallet Code. Browse here: https://store.steampowered.com/account/redeemwalletcode to redeem it.'

                    else:
                        sErrorMessage = 'An unexpected error has occurred.  Your product code has not been redeemed.  Please wait 30 minutes and try redeeming the code again.  If the problem persists, please contact <a href="https://help.steampowered.com/en/wizard/HelpWithCDKey">Steam Support</a> for further assistance.';
            
                    print(Fore.RED + "[ Error ]", sErrorMessage)

        c = input("Press Enter to close ...")

    elif y == ('no'):
        print("You have said no, make sure you have keys generated in the keys.txt file")
        print("Welcome to the steam code checker!")
        keyFileName = "keys.txt"
        u = input("Enter your steam username!: ")
        z = input("Enter the password for the steam account!: ")
        user = wa.WebAuth(u, z)

    # Create a login session
        try:
            user.login()
        except wa.CaptchaRequired:
            print(user.captcha_url)
            code = input("Please follow the captcha url, enter the code below:\n")
            user.login(captcha=code)
        except wa.EmailCodeRequired:
            code = input("Please enter emailed 2FA code:\n")
            user.login(email_code=code)
        except wa.TwoFactorCodeRequired:
            code = input("Please enter 2FA code from the Steam app on your phone:\n")
            user.login(twofactor_code=code)
        except wa.LoginIncorrect:
            print(Fore.RED + "Incorrect Username Or Password!")
            time.sleep(2)
            os.system('cls')
            steamiscool()

    # Get the sesssion ID, required for the ajax key auth
        sessionID = user.session.cookies.get_dict()["sessionid"]

        keys = []
        f = open(keyFileName)
        for line in f:
            keys.append(line)

    # Iterate over keys, if you need faster than this for some unknown reason you've probably got the skill to make this faster.
        for key in keys:
            r = user.session.post('https://store.steampowered.com/account/ajaxregisterkey/', data={'product_key' : key, 'sessionid' : sessionID})
            blob = json.loads(r.text)

        # Success
            if blob["success"] == 1:
                for item in blob["purchase_receipt_info"]["line_items"]:
                    print("[ Redeemed ]", item["line_item_description"])
            else:
            # Error codes from https://steamstore-a.akamaihd.net/public/javascript/registerkey.js?v=qQS85n3B1_Bi&l=english
                errorCode = blob["purchase_result_details"]
                sErrorMessage = ""
                if errorCode == 14:
                    sErrorMessage = 'The product code you\'ve entered is not valid. Please double check to see if you\'ve mistyped your key. I, L, and 1 can look alike, as can V and Y, and 0 and O.'

                elif errorCode == 15:
                    sErrorMessage = 'The product code you\'ve entered has already been activated by a different Steam account. This code cannot be used again. Please contact the retailer or online seller where the code was purchased for assistance.'

                elif errorCode == 53:
                    sErrorMessage = 'There have been too many recent activation attempts from this account or Internet address. Please wait and try your product code again later.'

                elif errorCode == 13:
                    sErrorMessage = 'Sorry, but this product is not available for purchase in this country. Your product key has not been redeemed.'

                elif errorCode == 9:
                    sErrorMessage = 'This Steam account already owns the product(s) contained in this offer. To access them, visit your library in the Steam client.'

                elif errorCode == 24:
                    sErrorMessage = 'The product code you\'ve entered requires ownership of another product before activation.\n\nIf you are trying to activate an expansion pack or downloadable content, please first activate the original game, then activate this additional content.'

                elif errorCode == 36:
                        sErrorMessage = 'The product code you have entered requires that you first play this game on the PlayStation®3 system before it can be registered.\n\nPlease:\n\n- Start this game on your PlayStation®3 system\n\n- Link your Steam account to your PlayStation®3 Network account\n\n- Connect to Steam while playing this game on the PlayStation®3 system\n\n- Register this product code through Steam.'

                elif errorCode == 50: 
                    sErrorMessage = 'The code you have entered is from a Steam Gift Card or Steam Wallet Code. Browse here: https://store.steampowered.com/account/redeemwalletcode to redeem it.'

                else:
                    sErrorMessage = 'An unexpected error has occurred.  Your product code has not been redeemed.  Please wait 30 minutes and try redeeming the code again.  If the problem persists, please contact <a href="https://help.steampowered.com/en/wizard/HelpWithCDKey">Steam Support</a> for further assistance.';
            
                print("[ Error ]", sErrorMessage)
            
            time.sleep(2)
            os.system('cls')
            steamiscool()
    else:
        print('Invalid Choice... Trying Again...')
        time.sleep(2)
        os.system('cls')
        steamiscool()
    
steamiscool()            