const openai = require("openai");
const csv = require("csv-parser");
const fs = require("fs");
const path = require("path");

class Scribe {
    constructor(csvPath, clientParams) {
        this.owners = new Set();
        this.csvPath = csvPath;
        this.clientParams = clientParams;
        openai.organization = "org-qcHPiKIimtg6ssjx0Xla5AGH";
        openai.api_key = "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";
    }

    async getPropertyData() {
        try {
            fs.createReadStream(this.csvPath)
                .pipe(csv())
                .on("data", (row) => {
                    let name = row["Name"];
                    let company = row["Owner"];
                    let ownerName = row["Primary Owner First Name"] + " " + row["Primary Owner Last Name"];
                    let siteAddress = row["Site Address"];
                    let ownerAddress = row["Street Address"];
                    let city = row["City"];
                    let state = row["State"];
                    let zipcode = row["Zip"];
                    let county = row["County"];

                    let to = "";
                    if (ownerName === "") {
                        to = company;
                    } else if (company === "") {
                        to = ownerName;
                    } else {
                        to = name.split("-")[0];
                    }

                    let acreage = "";
                    if (row["Acreage (Calc)"] === "") {
                        acreage = row["Acreage (Deeded)"];
                    } else if (row["Acreage (Deeded)"] === "") {
                        acreage = row["Acreage (Calc)"];
                    } else {
                        acreage = row["Total Acres - Same Land Owner"];
                    }

                    if (this.owners.has(to)) {
                        return;
                    } else {
                        this.owners.add(to);
                    }

                    return `To ${to} at ${ownerAddress},\n\n` + this.generateLetter(`My Name: Warren Kritko, Owner Name: ${to}, Site Address: ${siteAddress}, City: ${city}, County: ${county}, State: ${state}, Zip: ${zipcode}, Acreage: ${acreage}, Owner Address: ${ownerAddress}, Full property...`);
                });
        } catch (e) {
            console.error("Error in reading file: ", e);
            return;
        }
    }

    async generateLetter(propertyData) {
        const response = await fetch("https://api.openai.com/v1/engines/text-davinci-003/jobs", {
            method: "POST", headers: {
                "Content-Type": "application/json", "Authorization": 'Bearer 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'
            }, body: JSON.stringify({
                prompt: "Write a letter based on the following property data: " + propertyData,
                max_tokens: 100,
                n: 1,
                stop: null,
                temperature: 0.5
            })
        });

        const result = await response.json();
        return result.choices[0].text;
    }
}

const scribe = new Scribe("path/to/csv/file.csv", "client_params");
scribe.getPropertyData().then(r => scribe.generateLetter());
