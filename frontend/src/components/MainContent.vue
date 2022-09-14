<template>
    <div class="main">
        <div class="column">
            <question-card :argv="argv"></question-card>
        </div>
        <div class="column">
            <question-card :argv="argv"></question-card>
        </div>
        <div class="column">
            <question-card :argv="argv"></question-card>
        </div>
    </div>
</template>

<script>
import QuestionCard from "./QuestionCard.vue";
export default {
    name: 'MainContent',
    components: {
        QuestionCard,
    },
    data() {
        return {
            argv: {
                question: "这是一个问题",
                answer: "这是一个答案",
                title: "这是一个标题",
                created_at: new Date(2022, 6, 1, 0, 0, 0),
                answered_at: new Date(2022, 7, 1, 0, 0, 0),
            }
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
    grid-template-columns: repeat(3, minmax(0, 1fr));
    align-items: flex-start;
}

.column {
    display: grid;
    gap: 16px;
    grid-template-columns: 100%;
}
</style>
