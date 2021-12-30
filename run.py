from Finding_All_Customers import client_key, client_secret, website_password, company_info, company_contact_information
from uploading_customers import mailjet_uploads, Upload_Contacts

if __name__=="__main__":
    password = website_password(client_key, client_secret)
    all_companies = company_info()
    print("Looking into Customer's without emails.......")
    company_contact_information(all_companies, password)
    print("Looking into customers with emails.....")
    Upload_Contacts(all_companies, password)
    print("Completed both parts. You may now close the programs.")
