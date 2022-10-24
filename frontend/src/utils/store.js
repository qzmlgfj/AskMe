import { createStore } from 'vuex';

const store = createStore({
    state() {
        return {
            columnNum: 3,
            updateFlag: 0,
            userName: "",
            currentQuestion: null
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
        }
    }
})

export default store;
