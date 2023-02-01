from __future__ import print_function
from pydrive2.drive import GoogleDrive
from pydrive2.auth import GoogleAuth
import openai
import csv


class Scribe:
    # table = ["Primary Owner", "APN/PIN", "Name", "Primary Owner Last Name", "Primary Owner First Name",
    # "Site Address", "City", "State", "Zip", "Acreage (Deeded)", "Acreage (Calc)", "Name", "Name", "Total Acres -
    # Same Land Owner", "Owner", "City", "County", "State", "Zip Code", "Company Name", "Street Address", "City",
    # "State", "Zip", "Muni Id", "Muni Name", "Buildable Area (Acres)", "Notes"]

    def __init__(self, csv_path: str, client_params: str):
        self.csv_path = csv_path
        self.client_params = client_params
        openai.organization = "org-qcHPiKIimtg6ssjx0Xla5AGH"
        openai.api_key = "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"

    def getPropertyData(self):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication.

        drive = GoogleDrive(gauth)
        # Open the file and read the data into a list
        with open(self.csv_path) as file:
            reader = csv.reader(file)
            data = [row for row in reader]

        # Get the headers and indexes of the columns we want
        headers = data[0]
        name = headers.index("Name")
        # print(name)
        company_index = headers.index('Owner')
        owner_first_name_index = headers.index('Primary Owner First Name')
        owner_last_name_index = headers.index('Primary Owner Last Name')
        site_address_index = headers.index('Site Address')
        owner_address_index = headers.index('Street Address')
        acreage_deeded_index = headers.index('Acreage (Deeded)')
        acreage_calc_index = headers.index('Acreage (Calc)')
        total_acreage_index = headers.index('Total Acres - Same Land Owner')
        city_index = headers.index('City')
        zip_index = headers.index('Zip')
        county_index = headers.index('County')
        state_index = headers.index('State')

        # Loop through the data and extract the information
        for row in data[1:]:
            company = row[company_index]
            owner_name = row[owner_first_name_index] + " " + row[owner_last_name_index]
            site_address = row[site_address_index]
            owner_address = row[owner_address_index]
            city = row[city_index]
            state = row[state_index]
            zipcode = row[zip_index]
            county = row[county_index]

            # Print the information
            if owner_name == "":
                to = company
            elif company == "":
                to = owner_name
            else:
                to = name
            if row[acreage_calc_index] == "":
                acreage = row[acreage_deeded_index]
            elif acreage_deeded_index == "":
                acreage = row[acreage_calc_index]
            else:
                acreage = row[total_acreage_index]
            # sys.stdout.write(county + ", ")

            file = drive.CreateFile(
                {'title': f'{owner_address}.gdoc'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
            file.SetContentString(f"Address: {owner_address}\n\n" + self.generate_letter(
                f"My Name: Warren Kritko, Owner Name: {to}, Site Address: {site_address}, City: {city}, County: {county}, State: {state}, Zip: {zipcode}, Acreage: {acreage}, Owner Address: {owner_address}, Full property information: {row}"))  # Set content of the file from given string.
            file.Upload()

    def generate_letter(self, plain_text: str) -> str:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=self.client_params + plain_text,
            temperature=0.5,
            max_tokens=1000
        )
        print(f"{response['choices'][0]['text']}\n")
        return response['choices'][0]['text']


email_client = Scribe(csv_path="/Users/collindrake/Downloads/export.csv",
                      client_params="Write me a letter to inquire with a landowner about buying or leasing their "
                                    "property for a potential solar farm. If the owner's name is not present, use their"
                                    " company's name instead; if the company's name is also unavailable, address the "
                                    "recipient with 'to the owner of (property address).'",
                      )

email_client.getPropertyData()
