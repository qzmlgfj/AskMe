<script>
import { inject } from "vue";

import AddQuestionCard from "./Cards/AddQuestionCard.vue";
import AnswerQuestionCard from "./Cards/AnswerQuestionCard.vue";
import EditQuestionCard from "./Cards/EditQuestionCard.vue";
import LoginCard from "./Cards/LoginCard.vue";
import RegisterCard from "./Cards/RegisterCard.vue";


export default {
    name: "Modal",
    components: {
        AddQuestionCard,
        LoginCard,
        RegisterCard,
        AnswerQuestionCard
    },
    setup() {
        const { cardName } = inject("cardName");

        const selectCard = () => {
            switch (cardName.value) {
                case "login":
                    return <LoginCard />;
                case "addQuestion":
                    return <AddQuestionCard />;
                case "register":
                    return <RegisterCard />;
                case "answerQuestion":
                    return <AnswerQuestionCard />;
                case "modifyQuestion":
                    return <EditQuestionCard />;
            }
        };

        return {
            selectCard
        }
    },
    render() {
        return (
            <div>
                {
                    this.selectCard()
                }
            </div>
        )
    }
}
</script>