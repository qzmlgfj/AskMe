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

service.interceptors.request.use(function (request) {
    // Header中添加token
    const token = localStorage.getItem("token");
    if (token) {
        request.headers.token = token;
    }
    return request;
}, function (error) {
    return Promise.reject(error);
});

service.interceptors.response.use(function (response) {
    return response;
}, function (error) {
    localStorage.clear();
    return Promise.reject(error);
});

export { service };
