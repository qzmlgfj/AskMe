<template>
    <n-card :title="argv.title" :segmented="{
      content: true,
      footer: 'soft'
    }">
        <template #header-extra>
            <n-button text strong @click="switchAnswer">
                <template #icon>
                    <n-icon>
                        <key />
                    </n-icon>
                </template>
                查看答案
            </n-button>
        </template>
        {{argv.question}}
        <template v-if="showAnswer" #footer>
            <div v-if="argv.answer!=''">{{argv.answer}}</div>
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
import { ref } from "vue";
import { NCard, NButton, NIcon, NEmpty } from "naive-ui";
import { Key, Activity } from "@vicons/tabler"

export default {
    name: 'QuestionCard',
    props: ["argv"],
    components: {
        NCard,
        NButton,
        NIcon,
        NEmpty,
        Key,
        Activity
    },
    setup() {
        const showAnswer = ref(false);
        const switchAnswer = () => {
            showAnswer.value = !showAnswer.value;
        };

        return {
            showAnswer,
            switchAnswer
        }
    }
}
</script>
