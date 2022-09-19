import { service } from "./service";

function getAllQuestions() {
    return service({
        method: "get",
        url: "/api/question/all",
    })
}

function addQuestion(data) {
    return service({
        method: "post",
        url: "/api/question/add",
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

export { getAllQuestions, addQuestion, deleteQuestion };
