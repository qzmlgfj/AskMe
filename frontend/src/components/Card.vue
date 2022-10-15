<script>
import { inject } from "vue";

import ModalCard from "./Cards/ModalCard.vue";
import LoginCard from "./Cards/LoginCard.vue";
import RegisterCard from "./Cards/RegisterCard.vue";

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
                case "register":
                    return <RegisterCard />;
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