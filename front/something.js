// Load the Google Drive API client library
const { google } = require('googleapis');

async function uploadToGoogleDrive(file) {
    // Authorize a client with the Google Drive API credentials
    const client = await google.auth.getClient({
        scopes: ['https://www.googleapis.com/auth/drive'],
    });

    // Create a Google Drive API service instance
    const drive = google.drive({ version: 'v3', auth: client });

    // Define the metadata for the file to be uploaded
    const fileMetadata = {
        name: file.name,
    };

    // Define the media for the file to be uploaded
    const media = {
        mimeType: file.type,
        body: file.data,
    };

    // Upload the file to the user's Google Drive
    const response = await drive.files.create({
        resource: fileMetadata,
        media: media,
        fields: 'id',
    });

    return response.data.id;
}
