# aci-alexa

Amazon Alexa skill that would report Cisco ACI fabric health e.g. controller status, node status, fabric health score.

You can ask Alexa ACI dashboard:

- what is my fabric health?
- how are my APICs?
- how are spines?
- tell me a joke.

Full example: "Alexa, ask ACI dashboard what is my fabric health".

## Instructions to use

This skill is not published. To use it you need to build your custom skill. When building, use two files that are provided:

- interaction-model.json
- alexa-aci-lambda

1. Put the context of `interaction-model.json` into JSON Editor under the "Interaction Model" section of Alexa skill console. Then build the interaction model.

2. Replace the contents of your Lambda function code with the contents of `alexa-aci-lambda`. Change ACI fabric's URL and credentials to your own. Otherwise, the skill will poll Cisco's DevNet Sandbox fabric. Then deploy the code.

After both steps has been finished, you can invoke the skill from your Alexa account. Happy testing!

## Under the hood

The skill polls ACI fabric via REST API. First, it fetches the authentication token. Second, it uses the token to execute an API query (GET).

## Author

[**Vasily Prokopov**](https://github.com/vasilyprokopov)

## License

See the [LICENSE](LICENSE) file for details.