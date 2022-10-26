import { service } from "./service";

function getVersion() {
    return service({
        method: "get",
        url: "/api/version",
    })
}

function getQuestions(mode) {
    return service({
        method: "get",
        url: "/api/question/" + mode,
    })
}

function getUnansweredQuestionsNum() {
    return service({
        method: "get",
        url: "/api/question/unanswered_num",
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

function editQuestion(data) {
    return service({
        method: "POST",
        url: "/api/question/edit",
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
    getQuestions,
    getUnansweredQuestionsNum,
    addQuestion,
    answerQuestion,
    deleteQuestion,
    editQuestion,
    login,
    register,
    getCurrentUser,
    checkAdminExists,
};
