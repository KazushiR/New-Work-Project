import requests, csv, json, os, time, re
from dotenv import find_dotenv, load_dotenv
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from mailjet_rest import Client

load_dotenv(find_dotenv(".env.txt"))

client_key = os.getenv("client_id")
client_secret = os.getenv("client_secret")
mail_jet_key = os.getenv("mailjet_key")
mail_jet_secret = os.getenv("mailjet_secret")


def mailjet_uploads(customer_emails, mail_jet_key, mail_jet_secret):
    mailjet = Client(auth=(mail_jet_key, mail_jet_secret), version='v3')
    id = '36157'
    for email in customer_emails:
        print(email)
        data = {
      'Action': "addnoforce",
      'Contacts': [
        {
          "Email": f"{email}",
          "IsExcludedFromCampaigns": "false",
          "Name": "test",
          "Properties": "object"
        }
        ]
        }
        result = mailjet.contactslist_managemanycontacts.create(id=id, data=data)

def Upload_Contacts(all_companies, password):
    new_dictionary = {}
    headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {password}',
    }
    regex = r'\b@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    with open(r"Customers with emails\Companieswithemails.csv", "w", newline="") as companies:
                writer = csv.writer(companies)
                writer.writerow(["Company", "Account ID", "Access Status"])
                for company, company_id in all_companies.items():
                    print(f"working on {company}......")
                    response = requests.get(f'https://cp.serverdata.net/webservices/restapi/v1/api/identities/accounts?customerID={company_id}', headers=headers)
                    information = response.json()
                    customer_id = information[f"{company_id}"]
                    customer_json = requests.get(f'https://cp.serverdata.net/webservices/restapi/v1/api/accounts/{customer_id}/contacts', headers=headers)
                    customer_info = customer_json.json()
                    if len(customer_info) == 3:
                        emails = [emails["email"] for emails in customer_info["items"]]
                        all_emails = list(set(["".join(re.findall(regex, email)) for email in emails]))
                        if "@pacificoffice.com" in all_emails:
                            all_emails.remove("@pacificoffice.com")
                            if len(all_emails)>0:
                                print(f"Customer has an email for {company}. Updating Mailjet.....")
                                writer.writerow([company, company_id, "Emails Retrieved"])
                            else:
                                print(f"Customer has an email for {company}. Updating Mailjet.....")
                                writer.writerow([company, company_id, "Emails Retrieved"])
                    else:
                        print(f"Can't access this {company}.....Please look into this!")
                        writer.writerow([company, company_id, "Access Denied/Account Possibly No Longer Exists"])
                    customer_emails = [email for email in emails if not email.endswith("@pacificoffice.com")]
                    mailjet_uploads(customer_emails, mail_jet_key, mail_jet_secret)
    print("Finished updating customer database.....")

