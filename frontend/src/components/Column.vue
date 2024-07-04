<script lang="jsx">
import QuestionCard from "./Cards/QuestionCard.vue";

export default {
    name: "Column",
    components: {
        QuestionCard,
    },
    // eslint-disable-next-line vue/require-prop-types
    props: ["argv"],
    render() {
        return (
            <div class="column">
                {this.argv.map((item) => {
                    return <QuestionCard argv={item}></QuestionCard>;
                })}
            </div>
        );
    },
};
</script>

<style scoped>
.column {
    display: grid;
    gap: 16px;
    grid-template-columns: 100%;
}
</style>
