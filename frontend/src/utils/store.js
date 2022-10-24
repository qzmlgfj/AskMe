import { createStore } from 'vuex';

const store = createStore({
    state() {
        return {
            columnNum: 3,
            updateFlag: 0,
            userName: "",
            currentQuestionID: 0,
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
        setCurrentQuestionID(state, id) {
            state.currentQuestionID = id;
        }
    }
})

export default store;
