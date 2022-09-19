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

export { getAllQuestions, addQuestion };
