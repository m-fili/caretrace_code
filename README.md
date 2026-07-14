
# MyDataHelps REST API Node Quickstart

This app is a demonstration of how to access the [MyDataHelps REST API](https://developer.mydatahelps.org/) using [Node.js](https://nodejs.org/en/). It gives an example of obtaining an access token and making a simple query to the API. You can use this app for reference, or modify it to test out your own API requests in a development environment.

## Prerequisites

Before you begin, you will need three things:

* Your service account name, like “RKStudio.1234.test.”
* Your project ID, which is a GUID.
* The private key you associated with your service account.

For help finding this information, see the [MyDataHelps Developer Docs](https://developer.mydatahelps.org/api/quickstart.html).

## Using the App

This is a command-line app in Node.js. To run the app:

1. Install NodeJS and the Node Package Manager (npm).
2. Clone this repository.
3. Copy the file `dotenv.sample` and name the new copy `.env`.
4. Edit the `.env` file and fill in your project ID, service account name, and private key. See **Prerequisites** above for how to get this information.  See important private key format info below.
5. From the application directory, install the necessary npm libraries: `npm install`.
6. Run the script: `node quickstart.js`.

### Formatting the Private Key

NOTE! Be sure to include the begin/end tags `--BEGIN RSA PRIVATE KEY--` and `--END RSA PRIVATE KEY--` in your private key. Also format the line breaks using `\n`. The final string should look something like this:

```
RKS_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----\n230703de230703de230703de\nb62b0e24b62b0e24b62b0e24\n...\n-----END RSA PRIVATE KEY-----"
```

## Output

Though primarily intended to show you how to make MyDataHelps API calls, the quickstart also prints out some useful info for debugging.

### Service Token Output

First, it will print out a service token and participant count:

The service access token is only valid for a few minutes, but you can copy/paste it into a REST query tool of your choice to try out advanced queries.

```
Obtained service access token:
  SERVICE_TOKEN_HERE

Total Participants: 5
```

### Participant Token Output

If you have participants, the quickstart will also print out the first participant's details and a participant token for them.

This token is only needed for [MyDataHelps Embeddables](https://developer.mydatahelps.org/embeddables), and is useful for testing with the [MyDataHelps Starter Kit](https://github.com/CareEvolution/MyDataHelpsStarterKit).


```
Participant Found. ID: 59348b19-6e61-4390-a91f-bd0f90a4f307
{
  id: '59348b19-6e61-4390-a91f-bd0f90a4f307',
  enrolled: true,
  ...
}

Obtained participant access token for 59348b19-6e61-4390-a91f-bd0f90a4f307: PARTICIPANT_TOKEN_HERE
```

## Troubleshooting

If you see an error when running the script, double-check the information in the Prerequisites, particularly the format of the private key.

If you have trouble getting the app to work, feel free to [contact MyDataHelps Support](https://support.mydatahelps.org/contact-us).
