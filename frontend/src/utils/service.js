import axios from "axios";

axios.defaults.retry = 4;

const serviceProd = axios.create({
    timeout: 10000,
});

const serviceDev = axios.create({
    baseURL: "http://localhost:5000/",
    timeout: 3000,
});

const service = process.env.NODE_ENV === "development" ? serviceDev : serviceProd;

export {service};
