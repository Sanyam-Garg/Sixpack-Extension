/*
Experiment "test" created using this request body:
{
    "name": "test",
    "alternatives": {
        "variantA": [
            ["/html/body/h1", "innerHTML", "Heading A"],
            ["/html/body/img", "src", "https://img.freepik.com/free-vector/letter-brush-stroke-typography-vector_53876-175299.jpg"]
        ],
        "variantB": [
            ["/html/body/h1", "innerHTML", "Heading B"],
            ["/html/body/img", "src", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRLs6Mavwc2pTrEqhYNqPg561fO4kGTsPgbzQ&s"]
        ]
    }
}
*/

function getRandomClientId() {
    // Generate a random string for client ID
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    let result = "";
    for (let i = 0; i < 16; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
  }
  
  function getClientIdFromCookie() {
    // Attempt to retrieve client ID from cookie
    let clientId = document.cookie.split(';').find(c => c.startsWith('client_id='));
    if (clientId) {
      return clientId.split('=')[1];
    }
    return null;
  }
  
  function modifyElement(xpath, property, desiredValue) {
    // Use XPath to find the element
    const element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    if (element) {
      if (property === "innerHTML") {
        element.innerHTML = desiredValue;
      } else {
        element.setAttribute(property, desiredValue);
      }
    } else {
      console.warn(`Element not found for xpath: ${xpath}`);
    }
  }
  
  async function fetchData() {
    // Determine client ID based on cookie or generate a new one
    let clientId = getClientIdFromCookie();
    if (!clientId) {
      clientId = getRandomClientId();
      document.cookie = `client_id=${clientId}`; // Set cookie for future requests
    }
  
    try {
      const response = await fetch(`http://localhost:5000/participate?experiment=test&client_id=${clientId}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
  
      // Access and iterate over alternative object and its 2D array
      const alternativeData = Object.values(data.alternative)[0];
      console.log(alternativeData);
      for (const subArray of alternativeData) {
        console.log(subArray);
        const [xpath, property, desiredValue] = subArray;
        modifyElement(xpath, property, desiredValue);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  }
  
  fetchData();
  