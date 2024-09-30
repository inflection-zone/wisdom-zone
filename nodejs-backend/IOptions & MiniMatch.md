# Steps to resolve Error :  has no exported member 'IOptions'/''MiniMatch.

<span style="font-size: 18px;">After the `npm install`, When we launch the program. There are two errors saying **has no exported member 'IOptions'/'MiniMatch'** & location is `node_modules/@types/glob`
</span>

<span style="font-size: 18px;">In order to resolve the above error please follow the instructions</span>
> 1.	Remove - mime-types  & @types/mime-types from package.json

> 2.	Update firebase-admin package to latest 

>3.	Final Package.json file
```
{
  "name": "reancare",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "build": "NODE_OPTIONS=--max_old_space_size=5120 tsc",
    "start": "tsc && ts-node --files ./src/index.ts",
    "lint": "eslint ./src/**",
    "lint:fix": "eslint ./src/** --fix",
    "test": "tsc && mocha -u tdd --timeout 999999 --colors ./dist/tests/api-tests/**/*.js",
    "test-debug": "NODE_ENV=test mocha --file ./tests/api-tests/init.ts --reporter spec --exit"
  },
  "repository": {
    "type": "git",
    "url": "yes"
  },
  "keywords": [],
  "author": "Kiran Kharade",
  "license": "ISC",
  "dependencies": {
    "@aws-sdk/client-s3": "^3.325.0",
    "@aws-sdk/client-ses": "^3.370.0",
    "@aws-sdk/credential-provider-node": "^3.405.0",
    "@aws-sdk/lib-storage": "^3.405.0",
    "@aws-sdk/s3-request-presigner": "^3.405.0",
    "@faker-js/faker": "^8.0.2",
    "@opentelemetry/api": "^1.6.0",
    "@opentelemetry/auto-instrumentations-node": "^0.39.3",
    "@opentelemetry/exporter-metrics-otlp-proto": "^0.44.0",
    "@opentelemetry/exporter-trace-otlp-http": "^0.44.0",
    "@opentelemetry/exporter-zipkin": "^1.17.1",
    "@opentelemetry/instrumentation-express": "^0.33.2",
    "@opentelemetry/instrumentation-http": "^0.44.0",
    "@opentelemetry/resources": "^1.17.1",
    "@opentelemetry/sdk-metrics": "^1.17.1",
    "@opentelemetry/sdk-node": "^0.44.0",
    "@opentelemetry/sdk-trace-node": "^1.17.1",
    "@opentelemetry/semantic-conventions": "^1.17.1",
    "@types/adm-zip": "^0.5.1",
    "@types/bcryptjs": "^2.4.3",
    "@types/express": "^4.17.17",
    "@types/express-fileupload": "^1.4.1",
    "@types/sequelize": "^4.28.14",
    "@types/sharp": "^0.31.1",
    "adm-zip": "^0.5.10",
    "approx-string-match": "^1.1.0",
    "async": "^3.2.4",
    "axios": "^1.6.4",
    "bcryptjs": "^2.4.3",
    "body-parser": "^1.20.2",
    "cors": "^2.8.5",
    "country-currency-phone": "^0.1.11",
    "csv-writer": "^1.6.0",
    "dayjs": "^1.11.7",
    "dotenv": "^8.2.0",
    "express": "^4.18.2",
    "express-fileupload": "^1.2.1",
    "express-validator": "^6.15.0",
    "feed": "^4.2.2",
    "firebase-admin": "^12.0.0",
    "generate-password": "^1.7.0",
    "googleapis": "^95.0.0",
    "helmet": "^5.1.1",
    "jsonwebtoken": "^9.0.2",
    "mysql2": "^2.2.5",
    "needle": "^3.2.0",
    "node-cron": "^3.0.0",
    "node-html-to-image": "^3.3.0",
    "node-xlsx": "^0.4.0",
    "nodemailer": "^6.9.4",
    "pdfkit": "^0.13.0",
    "pg": "^8.11.3",
    "pg-hstore": "^2.3.3",
    "puppeteer": "^21.7.0",
    "reflect-metadata": "^0.1.13",
    "sequelize": "^6.30.0",
    "sequelize-typescript": "^2.1.3",
    "sharp": "^0.32.6",
    "sleep": "^6.3.0",
    "terra-api": "^1.4.0",
    "timezone-support": "^3.1.0",
    "tsyringe": "^4.8.0",
    "twilio": "^4.19.3",
    "typeorm": "^0.3.18",
    "uuid": "^9.0.1",
    "uuid-apikey": "^1.5.3",
    "word-wrap": "^1.2.5",
    "xmlbuilder": "^15.1.1"
  },
  "devDependencies": {
    "@types/body-parser": "^1.19.0",
    "@types/chai": "^4.3.5",
    "@types/fs-extra": "^9.0.11",
    "@types/mocha": "^10.0.1",
    "@types/node": "^18.17.15",
    "@types/nodemailer": "^6.4.8",
    "@types/pdfkit": "^0.12.10",
    "@types/shelljs": "^0.8.8",
    "@types/supertest": "^2.0.12",
    "@types/uuid": "^9.0.2",
    "@types/validator": "^13.1.3",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "chai": "^4.3.8",
    "eslint": "8.45.0",
    "eslint-config-airbnb-base": "^15.0.0",
    "eslint-plugin-import": "^2.27.5",
    "mocha": "^10.2.0",
    "supertest": "^6.3.3",
    "ts-node": "^10.9.1",
    "typescript": "^5.1.6"
  },
  "jest": {
    "projects": [
      "src/modules/ehr/jest.config.ts"
    ]
  }
}

```
> 4.	Remove existing package.lock.json & node_modules 

> 5.	`npm install`

>6.	Delete `node_modules\@types\glob`

> 7.	Launch the program.

----------------------------------------------


<span style="font-size: 18px;">Those who are getting issue of building with sqlite3 and facing `gyp` error with `Visual studio version` issue, it is because of `Python 3.12 version` where `distutils` is `removed` from default packages.</span>

<span style="font-size: 18px;">They can solve this issue by installing setuptools.   
`pip install setuptools`</span>