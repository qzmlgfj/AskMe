import { createStore } from 'vuex';

const store = createStore({
    state() {
        return {
            columnNum: 3,
            updateFlag: 0,
            queryMode: "unprivate_and_answered",
            userName: "",
            currentQuestion: null,
            isMobile: false,
            unansweredNum: 0,
        }
    },
    mutations: {
        updateAlarmCount(state, count) {
            state.alarmCount = count;
        },
        updateQuestion(state) {
            state.updateFlag++;
        },
        setUserName(state, name) {
            state.userName = name;
        },
        clearUserName(state) {
            state.userName = "";
        },
        setCurrentQuestion(state, question) {
            state.currentQuestion = question;
        },
        setIsMobile(state, isMobile) {
            state.isMobile = isMobile;
            state.columnNum = isMobile ? 1 : 3;
        },
        setQueryMode(state, mode) {
            state.queryMode = mode;
        },
        setUnansweredNum(state, num) {
            state.unansweredNum = num;
        },
        initUserStateFromLocalStorage(state) {
            state.userName = localStorage.getItem("userName");
            state.queryMode = "unanswered";
            state.updateFlag++;
        },
        clearUserStateFromLocalStorage(state) {
            state.userName = "";
            state.queryMode = "unprivate_and_answered";
            state.updateFlag++;
            localStorage.clear();
        }
    }
})

export default store;
