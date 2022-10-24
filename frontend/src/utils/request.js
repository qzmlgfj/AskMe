import { service } from "./service";

function getVersion() {
    return service({
        method: "get",
        url: "/api/version",
    })
}

function getAllQuestions() {
    return service({
        method: "get",
        url: "/api/question/all",
    })
}

function getUnansweredQuestions() {
    return service({
        method: "get",
        url: "/api/question/unanswered",
    })
}

function addQuestion(data) {
    return service({
        method: "post",
        url: "/api/question/add",
        data: data,
    })
}

function answerQuestion(data) {
    return service({
        method: "POST",
        url: "/api/question/answer",
        data: data,
    })
}

function deleteQuestion(data) {
    return service({
        method: "POST",
        url: "/api/question/delete",
        data: data,
    })
}

function login(data) {
    return service({
        method: "POST",
        url: "/api/auth/login",
        data: data,
    })
}

function register(data) {
    return service({
        method: "POST",
        url: "/api/auth/register",
        data: data,
    })
}

function getCurrentUser() {
    return service({
        method: "GET",
        url: "/api/auth/currentuser",
    })
}

function checkAdminExists() {
    return service({
        method: "GET",
        url: "/api/auth/checkadmin",
    })
}

export {
    getVersion,
    getAllQuestions,
    getUnansweredQuestions,
    addQuestion,
    answerQuestion,
    deleteQuestion,
    login,
    register,
    getCurrentUser,
    checkAdminExists,
};
