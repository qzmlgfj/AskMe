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
                    查看答案
                </n-button>
                <div v-if="ifLogin">
                    <n-space>
                        <n-button v-if="!argv.answered" text strong @click="handleAnswerQuestion">
                            <template #icon>
                                <n-icon>
                                    <cone />
                                </n-icon>
                            </template>
                            回答问题
                        </n-button>
                        <n-button text strong @click="handleEditQuestion">
                            <template #icon>
                                <n-icon>
                                    <pencil />
                                </n-icon>
                            </template>
                            编辑问题
                        </n-button>
                    </n-space>
                </div>
            </n-space>
        </template>
        {{argv.content}}
        <br>
        <br>
        <n-time :time="argv.created_at"></n-time>
        <template v-if="showAnswer" #footer>
            <div v-if="argv.answered">
                {{argv.answer}}
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
        <n-modal v-model:show="showModal" preset="dialog" title="确认" content="你确认?" positive-text="确认"
            negative-text="算了" @positive-click="submitCallback" @negative-click="cancelCallback" />
    </n-card>
</template>

<script>
import { ref, inject, computed } from "vue";
import { useStore } from "vuex";
import { NCard, NSpace, NButton, NIcon, NEmpty, NTime, NModal } from "naive-ui";
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
        NModal,
        Key,
        Activity,
        Cone,
        Pencil
    },
    setup(props) {
        const store = useStore();
        const showAnswer = ref(false);
        const showModal = ref(false);
        const deleteQuestion = inject("handleDelete");
        const { showAnswerQuestionModal } = inject("showAnswerQuestionModal");
        const { showEditQuestionModal } = inject("showEditQuestionModal");
        const ifLogin = computed(() => store.state.userName != "");

        const switchAnswer = () => {
            showAnswer.value = !showAnswer.value;
        };

        const handleDelete = () => {
            deleteQuestion(props.argv.id);
        };

        const show = () => {
            showModal.value = true;
        };

        const submitCallback = () => {
            handleDelete();
            showModal.value = false;
        };

        const cancelCallback = () => {
            showModal.value = false;
        };

        const handleAnswerQuestion = () => {
            showAnswerQuestionModal(props.argv.id);
        };

        const handleEditQuestion = () => {
            showEditQuestionModal(props.argv.id);
        };

        return {
            showAnswer,
            ifLogin,
            switchAnswer,
            showModal,
            handleDelete,
            show,
            submitCallback,
            cancelCallback,
            handleAnswerQuestion,
            handleEditQuestion
        }
    }
}
</script>
