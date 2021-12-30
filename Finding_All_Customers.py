import requests, csv, json, os, time, re
from dotenv import find_dotenv, load_dotenv
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

load_dotenv(find_dotenv(r"envitonmental variables\.env.txt"))

client_key = os.getenv("client_id")
client_secret = os.getenv("client_secret")

def website_password(client_key, client_secret):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options = options, executable_path = r"C:\Program Files\Google\Chrome\Application\\chromedriver.exe")
    website = driver.get("https://website.com/webservices/restapi/docs-ui/index#!/Identities_translation_(for_migration_purposes)/IdentitiesV1_GetAccountIdentities")
    driver.find_element_by_id("input_clientID").send_keys(client_key)
    driver.find_element_by_id("input_clientSecret").send_keys(client_secret)
    time.sleep(1)
    driver.find_element_by_id("button_requestToken").click()
    time.sleep(1)
    driver.find_element_by_id("explore").click()
    password = driver.find_element_by_id("input_apiKey").get_attribute("value")
    return password

def company_info():
    with open(r"All_POA_Contacts_From_IM\POA_contacts.csv") as csvfile:
        all_companies = {}
        reader = csv.DictReader(csvfile)
        for companies in reader:
                all_companies[companies["Company"]] = companies["AccountID"]
        return all_companies

def company_contact_information(all_companies, password):
    new_dictionary = {}
    headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {password}',
    }
    regex = r'\b@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    with open(r"Customers without emails\NoEmails.csv", "w", newline="") as companies:
                writer = csv.writer(companies)
                writer.writerow(["Company", "Account ID", "Access Status"])
                for company, company_id in all_companies.items():
                    response = requests.get(f'https://website.com/webservices/restapi/v1/api/identities/accounts?customerID={company_id}', headers=headers)
                    print(f"Working on {company}......")
                    information = response.json()
                    customer_id = information[f"{company_id}"]
                    customer_json = requests.get(f'https://website.com/webservices/restapi/v1/api/accounts/{customer_id}/contacts', headers=headers)
                    customer_info = customer_json.json()
                    if len(customer_info) == 3:
                        emails = [emails["email"] for emails in customer_info["items"]]
                        all_emails = list(set(["".join(re.findall(regex, email)) for email in emails]))
                        if len(all_emails) == 1 and "@pacificoffice.com" in all_emails:
                            print(f"Company {company} has no email......")
                            writer.writerow([company, company_id, "Emails Retrieved"])
                    else:
                        print(f"Can't access this {company".....Please look into this!")
                        writer.writerow([company, company_id, "Access Denied/Account Possibly No Longer Exists"])
    print("Finishing up with CSV file.....")
    print("Now working on updating the email list and creating a csv file for the current customer email base.....")
