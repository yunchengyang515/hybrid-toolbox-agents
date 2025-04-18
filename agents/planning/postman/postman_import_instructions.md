# Importing the Hybrid Training Planning API Collection

## Prerequisites

- [Postman](https://www.postman.com/downloads/) installed on your computer
- The Hybrid Training Planning API running (typically at http://localhost:8000)
- Your API key (if configured in the server)

## Import Steps

1. **Open Postman** and click on the "Import" button in the top left corner

2. **Select "File"** and navigate to this directory

3. **Choose the file**: `planning_agent_collection.json`

4. **Click "Import"** to load the collection

5. **Set the environment variables**:
   - Click on the "Environment" dropdown in the top right
   - Select "No Environment" and then click on "Add" to create a new environment
   - Name it "Hybrid Training Planning Environment"
   - Add the following variables:
     - `baseUrl`: `http://localhost:8000` (or your deployed API URL)
     - `apiKey`: Your API key (leave empty if not required)
     - `apiVersion`: `v1`
   - Save the environment
   - Select your new environment from the dropdown

## Collection Structure

The collection is organized into four main folders:

1. **Health Check**

   - Basic endpoint to verify the API is running

2. **MVP Flow**

   - Complete workflow demonstrating the conversational profile building
   - Shows how to handle incomplete profiles and follow-up questions
   - Includes a complete profile in a single request

3. **Individual Endpoints**

   - Separate endpoints for profile extraction and plan generation
   - Example API usage endpoint

4. **Test Cases by Goal**

   - Weight Loss Focus: For beginners with weight loss goals
   - Triathlon Training: For advanced athletes with specific race goals
   - Health Constraints: For users with health limitations

5. **Parameter Variations**
   - Plans with different emphasis (running, strength)
   - Various durations of training plans

## Using the Collection

### Testing the MVP Endpoint

1. Start with the **Initial Request (Incomplete Profile)** to see how the API handles partial information
2. Note the follow-up questions in the response
3. Use the **Follow-up Request** to complete the profile with conversation history
4. Try the **Complete Profile Request** for a one-step plan generation

### Testing Individual Components

1. Use **Extract Profile** to test just the profile extraction functionality
2. Use **Generate Plan** with a complete profile to test plan generation directly

### Testing Different User Scenarios

The **Test Cases by Goal** folder contains complete examples for different user personas:

- Beginners looking to lose weight
- Advanced athletes training for specific events
- Users with health constraints

### Customizing Plans

The **Parameter Variations** folder demonstrates different plan parameters:

- Changing emphasis between running and strength
- Adjusting plan duration
- Toggling warmup and cooldown inclusion

## Troubleshooting

- If you get authentication errors, check that your `apiKey` environment variable matches your server configuration
- If the server doesn't respond, verify it's running and the `baseUrl` is correct
- For invalid JSON responses, check the console logs on the server for parsing errors
