import { createStore } from 'vuex';

const store = createStore({
    state() {
        return {
            column_num: 3
        }
    },
    mutations: {
        changeTheme(state) {
            state.darkMode = state.darkMode == false ? true : false
        },
        updateAlarmCount(state, count) {
            state.alarmCount = count
        }
    }
})

export default store;
