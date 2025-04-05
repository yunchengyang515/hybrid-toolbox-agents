# Importing the Profile Agent Postman Collection

## Prerequisites

- [Postman](https://www.postman.com/downloads/) installed on your computer
- The Profile Agent API running (typically at http://localhost:8000)

## Import Steps

1. **Open Postman** and click on the "Import" button in the top left corner

2. **Select "File"** and navigate to this directory

3. **Choose the file**: `profile_agent_collection.json`

4. **Click "Import"** to load the collection

5. **Set the base URL environment variable**:
   - Click on the "Environment" dropdown in the top right
   - Select "No Environment" and then click on "Add" to create a new environment
   - Name it "Profile Agent Environment"
   - Add a variable named "baseUrl" with value "http://localhost:8000"
   - Save the environment
   - Select your new environment from the dropdown

## Using the Collection

The collection contains several test flows:

1. **Test Flow 1: Runner Adding Strength**

   - Contains a complete conversation flow with follow-ups
   - Run requests in sequence to see how the conversation builds

2. **Test Flow 2: Complete Initial Info**

   - Tests the system with complete information in a single request

3. **Test Flow 3: Weight Loss Focus**

   - Flow for a user with weight loss goals and limited experience

4. **Test Flow 4: Health Constraints**

   - Tests how the system handles users with health restrictions

5. **Test Flow 5: Advanced Athlete**
   - Tests the system with a more experienced athlete

For each flow, run the requests in order to simulate a conversation.

## Viewing and Using Results

After each request:

1. **View the response** to see:

   - Extracted profile data
   - Missing fields
   - Follow-up questions

2. **Copy the follow-up question** from the response to use in the next request

3. **Use the conversation history** from the prepared requests or build your own based on the responses

## Tips for Testing

- If the follow-up questions don't match exactly what's in the prepared requests, update the conversation history accordingly
- Use the "Save Response" feature in Postman to keep track of intermediate results
- Try modifying the requests to create your own test scenarios
