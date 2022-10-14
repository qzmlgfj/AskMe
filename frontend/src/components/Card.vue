<script>
import { inject } from "vue";

import ModalCard from "./Cards/ModalCard.vue";
import LoginCard from "./Cards/LoginCard.vue";

export default {
    name: "Modal",
    components: {
        ModalCard,
        LoginCard,
    },
    setup() {
        const { cardName } = inject("cardName");

        const selectCard = () => {
            switch (cardName.value) {
                case "login":
                    return <LoginCard />;
                case "addQuestion":
                    return <ModalCard />;
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