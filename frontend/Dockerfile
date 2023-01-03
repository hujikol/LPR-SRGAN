FROM node:16-alpine 

ENV NODE_ENV development

EXPOSE 3000
WORKDIR /home/app

COPY package.json .
COPY package-lock.json .

RUN npm install
RUN npm install react-scripts

COPY . .

CMD ["npm", "start", "--port", "3000"]