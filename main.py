from __future__ import print_function

from tkinter import filedialog

from pydrive2.drive import GoogleDrive
from pydrive2.auth import GoogleAuth
import tkinter as tk
import openai
import csv


class Scribe:
    # table = ["Primary Owner", "APN/PIN", "Name", "Primary Owner Last Name", "Primary Owner First Name",
    # "Site Address", "City", "State", "Zip", "Acreage (Deeded)", "Acreage (Calc)", "Name", "Name", "Total Acres -
    # Same Land Owner", "Owner", "City", "County", "State", "Zip Code", "Company Name", "Street Address", "City",
    # "State", "Zip", "Muni Id", "Muni Name", "Buildable Area (Acres)", "Notes"]

    def __init__(self, csv_path: str, client_params: str):
        self.owners = {""}
        self.csv_path = csv_path
        self.client_params = client_params
        openai.organization = "org-qcHPiKIimtg6ssjx0Xla5AGH"
        openai.api_key = "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"

    def getPropertyData(self):
        try:
            gauth = GoogleAuth()
            gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication.
        except Exception as e:
            print("Error in authentication: ", e)
            return

        try:
            drive = GoogleDrive(gauth)
            # Open the file and read the data into a list
            with open(self.csv_path) as file:
                reader = csv.reader(file)
                data = [row for row in reader]
        except Exception as e:
            print("Error in reading file: ", e)
            return

        try:
            # Get the headers and indexes of the columns we want
            headers = data[0]
            name_index = headers.index("Name")
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
        except Exception as e:
            print("Error in accessing columns: ", e)
            return

        # Loop through the data and extract the information
        for row in data[1:]:
            global current_letter

            name = row[name_index]
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
                to = name.split("-")[0]
            if row[acreage_calc_index] == "":
                acreage = row[acreage_deeded_index]
            elif acreage_deeded_index == "":
                acreage = row[acreage_calc_index]
            else:
                acreage = row[total_acreage_index]
            if to in self.owners:
                continue
            else:
                self.owners.add(to)
                file = drive.CreateFile(
                    {'title': f'{owner_address}.gdoc'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
                current_letter = file.SetContentString(f"To {to}at {owner_address},\n\n" + self.generate_letter(
                    f"My Name: Warren Kritko, Owner Name: {to}, Site Address: {site_address}, City: {city}, County: {county}, State: {state}, Zip: {zipcode}, Acreage: {acreage}, Owner Address: {owner_address}, Full property information: {row}"))  # Set content of the file from given string.
                file.Upload()

    def generate_letter(self, plain_text: str) -> str:
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=self.client_params + plain_text,
                temperature=0.1,
                max_tokens=1000
            )
        except Exception as e:
            # handle the error and show a message
            print("Error: " + str(e))
            return ""
        print(f"{response['choices'][0]['text']}\n")
        return response['choices'][0]['text']


def browseFiles():
    try:
        filename = filedialog.askopenfilename(initialdir="/Downloads",
                                              title="Select A CSV File",
                                              filetypes=(("CSV Files",
                                                          "*.csv"),
                                                         ("all files",
                                                          "*.*")))
        return filename
    except Exception as e:
        raise Exception("Failed to open file: " + str(e))


def run():
    Scribe(csv_path=browseFiles(),
           client_params="Write me a letter to inquire with a landowner about buying or leasing their "
                         "property for a potential solar farm. If the owner's name is not present, use their"
                         " company's name instead; if the company's name is also unavailable, address the "
                         "recipient with 'To the owner of (property address). Your letter should closely "
                         "mirror the example provided below:"
                         "Holland, Ware M2797 W Sugarberry Dr Eagle ID, 83616 December 9, 2022 Subject: "
                         "Intent to Lease Land for CTEC Solar Newnan GA,30263 ; Parcel ID: 039 3006 002 & "
                         "surrounding properties Dear Holland, I am contacting you today about a proposal "
                         "to lease several pieces of the property you own in Newnan Ga, 30263  for a "
                         "community solar project. They are currently listed under Ware Holland M "
                         "Charitable Foundation. I believe there are a total of 4 parcels you have in the "
                         "area that we would be interested in speaking with you about. We are currently "
                         "invested in solar projects in your area and we are looking to expand.  CTEC "
                         "Solar not only develops renewable-energy projects, but also constructs, "
                         "operates, and maintains them. In fact, CTEC is the company the other solar "
                         "companies often call to build their projects for them. Making it work for you: "
                         "Landowners receive upfront payments and operating rent. Solar farms can pay rent "
                         "checks for 20+ years. Leasing your land for a solar farm allows you and your "
                         "family to generate income from your land, while also holding onto the property "
                         "and income stream for future generations. Solar farms generate zero emissions "
                         "and are non hazardous. Solar farms create jobs and tax revenue. Currently, "
                         "there is limited availability in most areas to connect projects due to high "
                         "levels of interest among property owners and limited capacity for solar projects "
                         "within the power grid. Because of these factors, I encourage you to reach out to "
                         "me ASAP to discuss this proposal. We assume the costs of development and "
                         "permitting at our own risk. I would appreciate an opportunity to speak with you "
                         "so that I may answer any questions and gauge your potential interest.  Please "
                         "respond by calling my cell at (678) 898-6315 when you receive this. You may also "
                         "text my cell phone or email me at the address below. Sincerely, Warren Kritko "
                         "Project Developer mob: 678-898-6315 Warren.Kritko@ctecsolar.com '").getPropertyData()


class GUI:
    def __init__(self, master):
        self.master = master
        self.root = tk.Tk
        self.master.title("Scribe")
        self.label = tk.Label(self.master, text="Enter CSV Path")
        self.label.pack()

        self.run_button = tk.Button(self.master, text="Find File & Run", command=run)
        self.run_button.pack()

        self.quit_button = tk.Button(self.master, text="Quit", command=self.master.quit)
        self.quit_button.pack()


root = tk.Tk()
app = GUI(root)
tk.mainloop()
