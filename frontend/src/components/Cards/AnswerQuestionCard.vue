<template>
    <n-card style="width: 500px" title="一转攻势" :bordered="false" size="huge" role="dialog" aria-modal="true"
        footer-style="display:flex;justify-content:space-around;" :segmented="{content: true}" closable
        @close="closeModal">
        <n-space vertical>
            <n-form :model="formValue">
                <n-form-item label="回答" path="answer.content">
                    <n-input v-model:value="formValue.answer.content" type="textarea" placeholder="开始辱骂" />
                </n-form-item>
            </n-form>
        </n-space>
        <template #footer>
            <n-button type="primary" @click="handleAnswerQuestion">回复</n-button>
            <n-button type="default" @click="closeModal">取消</n-button>
        </template>
    </n-card>
</template>

<script>
import { ref, inject } from "vue";
import { useStore } from "vuex";

import { NCard, NSpace, NForm, NFormItem, NInput, NButton, useMessage } from "naive-ui";

import { answerQuestion } from "@/utils/request"

export default {
    name: "ModalCard",
    components: {
        NCard,
        NSpace,
        NForm,
        NFormItem,
        NInput,
        NButton
    },
    setup() {
        const { closeModal } = inject("closeModal");
        const formValue = ref({
            answer: {
                content: "",
            }
        })
        const message = useMessage();
        const store = useStore();

        const handleAnswerQuestion = function () {
            const params = {
                id: store.state.currentQuestionID,
                answer: formValue.value.answer.content
            }
            answerQuestion(params).then(res => {
                if (res.data.status == "ok") {
                    message.success("回复成功");
                    closeModal();
                    store.commit("updateQuestion");
                } else {
                    message.error("回复失败");
                }
            })
        }

        return {
            closeModal,
            formValue,
            handleAnswerQuestion
        };
    }
};
</script>
