# Deployment to AWS Lambda

## Prerequisites
    
1. AWS CLI installed
2. SAM installed


```bash
cd deployment

sam build
```

```bash
sam deploy --guided
```

Interactive deployment requires the setting of the following params:

- `NotesBucket` - S3 bucket to store notes
- `TGApiToken` - Telegram Bot token
- `DeepgramToken` - API token for Deepgram


You must register the webhook for your bot:

- You can find your Lambda Function URL Endpoint in the output values displayed 
after deployment. e.g. https://1fgfgfd56.lambda-url.eu-west-1.on.aws/

- Update your Telegram bot to change from polling to Webhook, by pasting this URL 
in your browser, or curl'ing it: https://api.telegram.org/bot12334342:ABCD124324234/setWebHook?url=https://1fgfgfd56.lambda-url.eu-west-1.on.aws/. 
Use your bot token and Lambda Function URL endpoint. You can check that it was 
set correctly by going to https://api.telegram.org/bot12334342:ABCD124324234/getWebhookInfo, 
which should include the url of your Lambda Function URL, as well as any errors 
Telegram is encounterting calling your bot on that API.


## TODO

### Functional

1. Add more transparency to the user
2. Restrict use of the bot to predefined users
3. Allo to add bot to the chats (especially to the self-chat)
4. Add option to view all notes
5. Add option to export all notes to markdown

### Tech Debt

1. Add logging for transition between states 
2. Catch errors in handlers and just cancel the conversations when caught
3. Write a thorough README with project description and deployment guide 
