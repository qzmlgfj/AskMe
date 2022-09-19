<script>
import QuestionCard from "./Cards/QuestionCard.vue";

export default {
    name: 'Column',
    props: ["argv"],
    components: {
        QuestionCard,
    },
    render() {
        return (
            <div class="column">
                {
                    this.argv.map((item) => {
                    return <QuestionCard argv={item}></QuestionCard>
                    })
                }
            </div>
        )
    }
}
</script>

<style scoped>
.column {
    display: grid;
    gap: 16px;
    grid-template-columns: 100%;
}
</style>
