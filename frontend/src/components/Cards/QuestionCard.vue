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
                <n-button text strong @click="handleDelete">
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
    </n-card>
</template>

<script>
import { ref, inject } from "vue";
import { NCard, NSpace, NButton, NIcon, NEmpty, NTime, } from "naive-ui";
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
        Key,
        Activity,
        CircleX
    },
    setup(props) {
        const showAnswer = ref(false);
        const switchAnswer = () => {
            showAnswer.value = !showAnswer.value;
        };

        const deleteQuestion = inject("handleDelete");
        const handleDelete = () => {
            deleteQuestion(props.argv.id);
        };

        return {
            showAnswer,
            switchAnswer,
            handleDelete
        }
    }
}
</script>
