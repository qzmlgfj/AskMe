<template>
    <n-card
        style="width: 350px"
        title="一转攻势"
        :bordered="false"
        size="huge"
        role="dialog"
        aria-modal="true"
        footer-style="display:flex;justify-content:space-around;"
        :segmented="{ content: true }"
        closable
        @close="closeModal"
    >
        <n-space vertical>
            <n-form ref="formRef" :model="formValue" :rules="rules">
                <n-form-item label="回答" path="answer.content">
                    <n-input
                        v-model:value="formValue.answer.content"
                        type="textarea"
                        placeholder="开始辱骂"
                        :maxlength="cardLimits.answerMaxLength"
                        show-count
                    />
                </n-form-item>
                <n-form-item>
                    <n-checkbox v-model:checked="formValue.answer.ai_answer">
                        AI回答
                    </n-checkbox>
                </n-form-item>
            </n-form>
        </n-space>
        <template #footer>
            <n-button type="primary" @click="handleAnswerQuestion"
                >回复</n-button
            >
            <n-button type="default" @click="closeModal">取消</n-button>
        </template>
    </n-card>
</template>

<script>
import { ref, inject } from "vue";
import { useStore } from "vuex";

import {
    NCard,
    NSpace,
    NForm,
    NFormItem,
    NInput,
    NCheckbox,
    NButton,
    useMessage,
} from "naive-ui";

import { answerQuestion } from "@/utils/request";
import { CARD_LIMITS } from "@/config/cardLimits";

export default {
    name: "ModalCard",
    components: {
        NCard,
        NSpace,
        NForm,
        NFormItem,
        NInput,
        NCheckbox,
        NButton,
    },
    setup() {
        const { closeModal } = inject("closeModal");
        const message = useMessage();
        const store = useStore();

        const formRef = ref(null);
        const formValue = ref({
            answer: {
                content: "",
                ai_answer: false,
            },
        });

        const rules = {
            answer: {
                content: [
                    {
                        required: true,
                        message: "回答不能为空",
                        trigger: ["input", "blur"],
                    },
                ],
            },
        };

        const handleAnswerQuestion = function (e) {
            e.preventDefault();
            formRef.value?.validate((errors) => {
                const params = {
                    id: store.state.currentQuestion.id,
                    answer: formValue.value.answer.content,
                    ai_answer: formValue.value.answer.ai_answer,
                };
                if (!errors) {
                    answerQuestion(params).then((res) => {
                        if (res.data.status == "ok") {
                            message.success("回复成功");
                            closeModal();
                            store.commit("updateQuestion");
                        } else {
                            message.error("回复失败");
                        }
                    });
                } else {
                    message.error("请检查输入");
                }
            });
        };

        return {
            closeModal,
            formRef,
            formValue,
            rules,
            cardLimits: CARD_LIMITS,
            handleAnswerQuestion,
        };
    },
};
</script>
