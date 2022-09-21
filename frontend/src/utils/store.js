import { createStore } from 'vuex';

const store = createStore({
    state() {
        return {
            columnNum: 3,
            updateFlag: 0,
        }
    },
    mutations: {
        updateAlarmCount(state, count) {
            state.alarmCount = count;
        },
        updateQuestion(state) {
            state.updateFlag++;
        }
    }
})

export default store;
