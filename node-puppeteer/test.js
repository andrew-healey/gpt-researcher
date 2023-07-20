import { launch } from "puppeteer-core";

import { config } from "dotenv";
config();

const headless = false;
const executablePath = process.env.EXECUTABLE_PATH;

const getBrowser = () => launch({
  headless,
  defaultViewport: null,
  args: [
    "--window-size=1920,1080",
    "--window-position=0,0",
    "--disable-blink-features=AutomationControlled"
  ],
  ignoreDefaultArgs: ["--enable-automation"],
  // executablePath,
  channel: "chrome"
});

await getBrowser()