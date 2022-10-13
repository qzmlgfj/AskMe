<script>
import { ref, computed, provide } from 'vue';
import { useStore } from "vuex";
import { useMessage } from 'naive-ui';

import Column from './Column.vue';

import { getAllQuestions, getUnansweredQuestions, deleteQuestion } from "@/utils/request";

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
        const message = useMessage();
        const currentUser = computed(() => store.state.userName);

        const getQuestions = currentUser.value == "" ? getUnansweredQuestions : getAllQuestions;

        // 将数据分散到不同的column中
        const distribute_data = function (question_data) {
            column_lst.value = [];
            for (let i = 0; i < column_num.value; i++) {
                column_lst.value.push([]);
            }
            for (let i = 0; i < question_data.length; i++) {
                column_lst.value[i % column_num.value].push(question_data[i]);
            }
        }

        const getData = function () {
            getQuestions().then((res) => {
                let question_data = res.data;
                question_data.map((item) => {
                    item.created_at = new Date(item.created_at);
                    item.answered_at = new Date(item.answered_at);
                });
                distribute_data(question_data);
            })
        }

        const handleDelete = function (id) {
            deleteQuestion({ id: id }).then(res => {
                console.log(res);
                if (res.data.status == "ok") {
                    message.success("删除成功");
                    store.commit("updateQuestion");
                } else {
                    message.error("删除失败");
                }
            })
        }

        provide("handleDelete", handleDelete);

        getData();

        return {
            column_num,
            column_lst,
            updateFlag,
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
