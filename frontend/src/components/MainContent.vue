<script>
import { ref, computed } from 'vue';
import { useStore } from "vuex";

import Column from './Column.vue';

import { getQuestions, getUnansweredQuestionsNum } from "@/utils/request";

export default {
    name: 'MainContent',
    components: {
        Column,
    },
    setup() {
        const store = useStore();
        const column_num = computed(() => store.state.columnNum);
        const column_lst = ref([]);
        const updateFlag = computed(() => store.state.updateFlag);
        let question_data = ref(null);

        // 将数据分散到不同的column中
        const distribute_data = function () {
            column_lst.value = [];
            for (let i = 0; i < column_num.value; i++) {
                column_lst.value.push([]);
            }
            for (let i = 0; i < question_data.value.length; i++) {
                column_lst.value[i % column_num.value].push(question_data.value[i]);
            }
        }

        const getData = function () {
            getQuestions(store.state.queryMode).then((res) => {
                question_data.value = res.data;
                question_data.value.map((item) => {
                    item.created_at = new Date(item.created_at);
                    item.answered_at = new Date(item.answered_at);
                });
                distribute_data(question_data);
            })
            getUnansweredQuestionsNum().then((res) => {
                console.log(res.data.num);
                store.commit('setUnansweredNum', res.data.num);
            })
        }

        getData();

        return {
            column_num,
            column_lst,
            updateFlag,
            question_data,
            distribute_data,
            getData,
        }
    },
    render() {
        return (
            <div class="main">
                {
                    this.column_lst.map((item) => {
                        return <column argv={item}></column>
                    })
                }
            </div>
        )
    },
    watch: {
        column_num: {
            handler: function () {
                this.distribute_data();
            },
            deep: true,
        },
        updateFlag: {
            handler: function () {
                this.getData();
            },
            deep: true,
        }
    },
}
</script>

<style scoped>
.main {
    min-height: 80vh;
    box-sizing: border-box;
    padding: 32px;

    display: grid;
    gap: 16px;
    grid-template-columns: repeat(v-bind(column_num), minmax(0, 1fr));
    align-items: flex-start;
}
</style>
