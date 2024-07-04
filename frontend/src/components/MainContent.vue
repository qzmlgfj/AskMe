<template>
    <n-spin :show="showSpin">
        <div v-if="showSpin == false && question_num == 0" class="empty">
            <n-empty size="huge" description="啥也没有" />
        </div>
        <div v-else class="column-container">
            <column
                v-for="(item, index) in column_lst"
                :key="index"
                :argv="item"
            />
        </div>
    </n-spin>
</template>

<script>
import { ref, computed } from "vue";
import { useStore } from "vuex";
import { NEmpty, NSpin, useMessage } from "naive-ui";

import Column from "./Column.vue";

import { getQuestions, getUnansweredQuestionsNum } from "@/utils/request";

export default {
    name: "MainContent",
    components: {
        Column,
        NEmpty,
        NSpin,
    },
    setup() {
        window.$message = useMessage();

        const store = useStore();
        const column_num = computed(() => store.state.columnNum);
        const column_lst = ref([]);
        const updateFlag = computed(() => store.state.updateFlag);
        const question_data = ref(null);
        const question_num = ref(0);
        const showSpin = ref(false);

        // 将数据分散到不同的column中
        const distribute_data = function () {
            column_lst.value = [];
            for (let i = 0; i < column_num.value; i++) {
                column_lst.value.push([]);
            }
            for (let i = 0; i < question_data.value.length; i++) {
                column_lst.value[i % column_num.value].push(
                    question_data.value[i],
                );
            }
        };

        const getData = function () {
            showSpin.value = true;
            getQuestions(store.state.queryMode).then((res) => {
                question_data.value = res.data;
                question_num.value = res.data.length;
                question_data.value.map((item) => {
                    item.created_at = new Date(item.created_at);
                    item.answered_at = new Date(item.answered_at);
                });
                distribute_data(question_data);
                showSpin.value = false;
            });
            getUnansweredQuestionsNum().then((res) => {
                store.commit("setUnansweredNum", res.data.num);
            });
        };

        getData();

        return {
            column_num,
            column_lst,
            updateFlag,
            question_data,
            question_num,
            showSpin,
            distribute_data,
            getData,
        };
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
        },
    },
};
</script>

<style scoped>
.empty {
    min-height: 85vh;
    box-sizing: border-box;
    padding: 32px;

    display: flex;
    align-items: center;
    justify-content: center;
}

.column-container {
    min-height: 85vh;
    box-sizing: border-box;
    padding: 32px;

    display: grid;
    gap: 16px;
    grid-template-columns: repeat(v-bind(column_num), minmax(0, 1fr));
    align-items: flex-start;
}
</style>
