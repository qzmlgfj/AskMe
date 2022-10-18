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

service.interceptors.request.use(function(config) {
    // Header中添加token
    const token = localStorage.getItem("token");
    if (token) {
        config.headers.token = token;
    }
    return config;
}, function (error) {
    return Promise.reject(error);
});

export { service };
