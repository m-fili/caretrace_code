require('dotenv').config();

const jwt = require('jsonwebtoken');
const util = require('util');
const querystring = require('querystring');
const { v4: uuidv4 } = require('uuid');

// **NOTE!** In a real production app you would want these to be sourced from real environment variables. The .env file is just
// a convenience for development.
const mdhProjectId = process.env.RKS_PROJECT_ID;
const mdhServiceAccount = process.env.RKS_SERVICE_ACCOUNT;
const privateKey = process.env.RKS_PRIVATE_KEY;

const baseUrl = process.env.RKS_BASE_URL || "https://designer.mydatahelps.org";
const tokenUrl = `${baseUrl}/identityserver/connect/token`;

async function getServiceAccessToken() {

  const assertion = {
    "iss": mdhServiceAccount,
    "sub": mdhServiceAccount,
    "aud": tokenUrl,
    "exp": Math.floor(new Date().getTime() / 1000) + 200,
    "jti": uuidv4()
  };

  var signedAssertion;
  try {
    signedAssertion = jwt.sign(assertion, privateKey, { algorithm: 'RS256' });
  }
  catch(err) {
    console.log(`Error signing JWT. Check your private key. Error: ${err}`);
    return null;
  }

  const payload = {
    scope: "api",
    grant_type: "client_credentials",
    client_assertion_type: "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
    client_assertion: signedAssertion
  };
  
  const response = await fetch(tokenUrl, { method: "POST", headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: querystring.stringify(payload) });

  if (!response.ok) {
      const error = `Get service access token failed. ${response.status} - ${await response.text()}`;
      throw new Error(error);
  }

  const data = await response.json();
  return data.access_token;
}


async function getFromApi(serviceAccessToken, resourceUrl, queryParams = null, raiseError = true) {

  const queryString = queryParams ? `?${new URLSearchParams(queryParams)}` : '';
  const url = `${baseUrl}${resourceUrl}${queryString}`;
  
  const response = await fetch(url, {
      headers: { 
        "Authorization": `Bearer ${serviceAccessToken}`,
        "Accept": "application/json",
        "Content-Type": "application/json; charset=utf-8"
        }
    });

  if (!response.ok && raiseError) {
    const error = `API call to ${url} failed. ${response.status} - ${await response.text()}`;
    throw new Error(error);
  }

  return { data: await response.json(), status: response.status };
}

async function postToApi(serviceAccessToken, resourceUrl, queryParams = null, body = null, raiseError = true) {

  const queryString = queryParams ? `?${new URLSearchParams(queryParams)}` : '';
  const url = `${baseUrl}${resourceUrl}${queryString}`;
  
  const response = await fetch(url, {
      headers: { 
        "Authorization": `Bearer ${serviceAccessToken}`,
        "Accept": "application/json",
        "Content-Type": "application/json; charset=utf-8"
        },
      method: 'POST',
      body: JSON.stringify(body)
    });

  if (!response.ok && raiseError) {
    const error = `API call to ${url} failed. ${response.status} - ${await response.text()}`;
    throw new Error(error);
  }

  return { data: await response.json(), status: response.status };
}

// Get a participant access token for the specified participant
// Used for MyDataHelps Embeddables ONLY
async function getParticipantAccessToken(serviceAccessToken, participantID, scopes) {

  const payload = {
      "scope": scopes,
      "grant_type": "delegated_participant",
      "participant_id": participantID,
      "client_id": "MyDataHelps.DelegatedParticipant",
      "client_secret": "secret",
      "token": serviceAccessToken,
  }

  const response = await fetch(tokenUrl, { method: "POST", headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: querystring.stringify(payload) });

  if (!response.ok) {
    const error = `Get participant access token failed. ${response.status} - ${await response.text()}`;
    throw new Error(error);
  }

  const data = await response.json();
  return data.access_token;
}

// Use this utility if you ever need to print a response for debugging
function logResponse(response) {
  console.log(util.inspect(response, { colors: true, depth: 3 }));
}

async function quickstart() {
  var url;
  var response;
  
  // Get a service access token, needed for all API calls.
  const serviceAccessToken = await getServiceAccessToken();
  console.log('Obtained service access token:');
  console.log(serviceAccessToken);

  // Get all participants
  url = `/api/v1/administration/projects/${mdhProjectId}/participants`;
  response = await getFromApi(serviceAccessToken, url);
  const participants = response.data;
  console.log(`\nTotal Participants: ${participants.totalParticipants}`);
  
  // Exit now if no participants found.
  if (!participants["participants"]) {
    return;
  }
  
  // Get first PPT for debugging
  const firstParticipant = participants["participants"][0];
    
  // Get a specific participant by identifier. We disable 'raiseError' here
  // so we can handle the 404 case ourselves.
  const participantIdentifier = firstParticipant["participantIdentifier"];
  
  url = `/api/v1/administration/projects/${mdhProjectId}/participants/${participantIdentifier}`;
  response = await getFromApi(serviceAccessToken, url, null, false );
  if (response.status === 404) {
    console.log("\nParticipant not found.");
  } else {
    const participant = response.data;
    console.log(`\nParticipant Found. ID: ${participant.id}`);
    console.log(participant);

    // NOTE: This piece is only necessary when using MyDataHelps Embeddables in a custom app. 
    // Most API use cases do NOT require a participant token.
    // Be sure to:
    // 1. Use the internal ID field (from participant.id above) and NOT participantIdentifier
    // 2. Request the correct scope(s) for your needs. The default ones here mirror the MyDataHelpsStarterKit needs.
    const scopes = "Participant:read SurveyTasks:read SurveyAnswers:read Notifications:read DataCollectionSettings:read ExternalAccounts:connect ExternalAccounts:read  Project:read";
    const participantAccessToken = await getParticipantAccessToken(serviceAccessToken, participant.id, scopes);
    console.log(`\nObtained participant access token for ${participant.id}: ${participantAccessToken}`);
  }
}


quickstart();
