import express from "express";
import slack from "slack";
import bodyParser from "body-parser";
import config from "./config";

export const bootstrap = () => {
  const app = express();

  app.use(bodyParser.urlencoded());
  app.use(bodyParser.json());

  app.post("/slack", (req, res) => {
    const data = req.body;

    try {
        
        slack.chat.postMessage({
            channel: "aga-model-notifications",
            token: config.slackApiKey,
            text: `<@U04HYGZ7H5X>\n${JSON.stringify(data, null, 2)}`,
        });
        res.status(200).json({ message: 'Ok'})
    } catch (error) {
        console.log(error)
        res.status(400).json({ message: (error as Error).message, error})
        
    }
  });
  app.listen(config.port, () => {

    console.log(`Running application on port ${config.port}`)
  });
};
