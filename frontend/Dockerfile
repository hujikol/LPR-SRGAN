FROM node:16-alpine 

ENV NODE_ENV development

EXPOSE 5000
WORKDIR /home/app

COPY package.json .
RUN npm install

COPY . .

CMD ["npm", "run", "start"]