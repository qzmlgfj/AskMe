<script>
import Column from './Column.vue';
import { ref, computed } from 'vue';
import { useStore } from "vuex";

export default {
    name: 'MainContent',
    components: {
        Column,
    },
    data() {
        return {
            argv: {
                lst: [
                    {
                        question: "这是一个问题",
                        answer: "这是一个答案",
                        title: "这是一个标题",
                        created_at: new Date(2022, 6, 1, 0, 0, 0),
                        answered_at: new Date(2022, 7, 1, 0, 0, 0),
                    },
                    {
                        question: "这是一个问题",
                        answer: "这是一个答案",
                        title: "这是一个标题",
                        created_at: new Date(2022, 6, 1, 0, 0, 0),
                        answered_at: new Date(2022, 7, 1, 0, 0, 0),
                    },
                    {
                        question: "这是一个问题",
                        answer: "这是一个答案",
                        title: "这是一个标题",
                        created_at: new Date(2022, 6, 1, 0, 0, 0),
                        answered_at: new Date(2022, 7, 1, 0, 0, 0),
                    },
                ]
            }
        }
    },
    setup() {
        const store = useStore();
        const column_num = computed(() => store.state.column_num);
        const question_data = [
            {
                question: "这是一个问题",
                answer: "这是一个答案",
                title: "这是一个标题",
                created_at: new Date(2022, 6, 1, 0, 0, 0),
                answered_at: new Date(2022, 7, 1, 0, 0, 0),
            },
            {
                question: "这是一个问题",
                answer: "这是一个答案",
                title: "这是一个标题",
                created_at: new Date(2022, 6, 1, 0, 0, 0),
                answered_at: new Date(2022, 7, 1, 0, 0, 0),
            },
            {
                question: "这是一个问题",
                answer: "这是一个答案",
                title: "这是一个标题",
                created_at: new Date(2022, 6, 1, 0, 0, 0),
                answered_at: new Date(2022, 7, 1, 0, 0, 0),
            },
        ];
        const column_lst = ref([]);

        // 将数据分散到不同的column中
        const distribute_data = function () {
            column_lst.value = [];
            for (let i = 0; i < column_num.value; i++) {
                column_lst.value.push([]);
            }
            for (let i = 0; i < question_data.length; i++) {
                column_lst.value[i % column_num.value].push(question_data[i]);
            }
        }

        distribute_data();

        return {
            column_num,
            column_lst,
            distribute_data,
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
        }
    }
}
</script>

<style scoped>
.main {
    height: 100vh;
    box-sizing: border-box;
    padding: 32px;

    display: grid;
    gap: 16px;
    grid-template-columns: repeat(v-bind(column_num), minmax(0, 1fr));
    align-items: flex-start;
}
</style>
