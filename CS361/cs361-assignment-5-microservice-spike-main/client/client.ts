import axios from "axios";

const SERVER_ENDPOINT = "http://localhost:3000";
const DATA = "A message from CS361";

/**
 * Makes an HTTP post request to the specified endpoint with the provided data
 * @return void
 */
const handlePostRequest = async () => {
  console.log(`Trying to send "${DATA}" to ${SERVER_ENDPOINT}...`);
  try {
    const response = await axios.post(SERVER_ENDPOINT, {
      data: DATA,
    });
    console.log(`Received HTTP response: ${response.status}`);
  } catch (e) {
    let errorMsg;
    e instanceof Error ? (errorMsg = e.message) : "Post request failed";

    throw new Error(errorMsg);
  }
};

handlePostRequest();
