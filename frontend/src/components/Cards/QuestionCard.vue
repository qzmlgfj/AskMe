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
                <n-button text strong @click="show">
                    <template #icon>
                        <n-icon>
                            <circle-x />
                        </n-icon>
                    </template>
                    删除问题
                </n-button>
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
import { ref, inject } from "vue";
import { NCard, NSpace, NButton, NIcon, NEmpty, NTime, NModal } from "naive-ui";
import { Key, Activity, CircleX } from "@vicons/tabler"

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
        CircleX
    },
    setup(props) {
        const showAnswer = ref(false);
        const showModal = ref(false);
        const deleteQuestion = inject("handleDelete");

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

        return {
            showAnswer,
            switchAnswer,
            showModal,
            handleDelete,
            show,
            submitCallback,
            cancelCallback
        }
    }
}
</script>
