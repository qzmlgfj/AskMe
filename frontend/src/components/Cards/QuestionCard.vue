<template>
    <n-card hoverable :title="argv.title" :segmented="{
        content: true,
        footer: 'soft'
    }">
        <template #header-extra>
            <n-space>
                <n-button text strong @click="switchAnswer">
                    <template #icon>
                        <n-icon>
                            <key />
                        </n-icon>
                    </template>
                    <template v-if="!isMobile">查看答案</template>
                </n-button>
                <div v-if="ifLogin">
                    <n-space>
                        <n-button v-if="!argv.answered" text strong @click="handleAnswerQuestion">
                            <template #icon>
                                <n-icon>
                                    <cone />
                                </n-icon>
                            </template>
                            <template v-if="!isMobile">回答问题</template>
                        </n-button>
                        <n-button text strong @click="handleEditQuestion">
                            <template #icon>
                                <n-icon>
                                    <pencil />
                                </n-icon>
                            </template>
                            <template v-if="!isMobile">编辑问题</template>
                        </n-button>
                    </n-space>
                </div>
            </n-space>
        </template>
        {{ argv.content }}
        <br>
        <br>
        <!-- TODO 考虑渲染一下ID -->
        <n-time :time="argv.created_at"></n-time>
        <template v-if="showAnswer" #footer>
            <div v-if="argv.answered">
                {{ argv.answer }}
                <br>
                <br>
                <n-time :time="argv.answered_at"></n-time>
            </div>
            <div v-else>
                <n-empty description="暂无回答">
                    <template #icon>
                        <n-icon>
                            <activity />
                        </n-icon>
                    </template>
                </n-empty>
            </div>
        </template>
    </n-card>
</template>

<script>
import { ref, inject, computed } from "vue";
import { useStore } from "vuex";
import { NCard, NSpace, NButton, NIcon, NEmpty, NTime } from "naive-ui";
import { Key, Activity, Cone, Pencil } from "@vicons/tabler"

export default {
    name: 'QuestionCard',
    props: ["argv"],
    components: {
        NCard,
        NSpace,
        NButton,
        NIcon,
        NEmpty,
        NTime,
        Key,
        Activity,
        Cone,
        Pencil
    },
    setup(props) {
        const store = useStore();
        const showAnswer = ref(false);
        const { showAnswerQuestionModal } = inject("showAnswerQuestionModal");
        const { showEditQuestionModal } = inject("showEditQuestionModal");
        const ifLogin = computed(() => store.state.userName != "");
        const isMobile = computed(() => store.state.isMobile);

        const switchAnswer = () => {
            showAnswer.value = !showAnswer.value;
        };

        const handleAnswerQuestion = () => {
            showAnswerQuestionModal(props.argv);
        };

        const handleEditQuestion = () => {
            showEditQuestionModal(props.argv);
        };

        return {
            showAnswer,
            ifLogin,
            isMobile,
            switchAnswer,
            handleAnswerQuestion,
            handleEditQuestion
        }
    }
}
</script>
