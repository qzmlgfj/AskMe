<template>
    <n-card
        style="width: 350px"
        title="开始整蛊"
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
                <n-form-item label="标题" path="question.title">
                    <n-input
                        v-model:value="formValue.question.title"
                        placeholder="输入问题标题"
                        maxlength="15"
                        show-count
                    />
                </n-form-item>
                <n-form-item label="问题" path="question.content">
                    <n-input
                        v-model:value="formValue.question.content"
                        type="textarea"
                        placeholder="输入问题内容"
                        maxlength="100"
                        show-count
                    />
                </n-form-item>
                <n-form-item label="非公开" path="question.private">
                    <n-switch v-model:value="formValue.question.private" />
                </n-form-item>
            </n-form>
        </n-space>
        <template #footer>
            <n-button
                type="primary"
                :disabled="addBtnDisabled"
                @click="handleAddQuestion"
                >添加</n-button
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
    NSwitch,
    NInput,
    NButton,
    useMessage,
} from "naive-ui";

import { addQuestion } from "@/utils/request";

export default {
    name: "ModalCard",
    components: {
        NCard,
        NSpace,
        NForm,
        NFormItem,
        NSwitch,
        NInput,
        NButton,
    },
    setup() {
        const { closeModal } = inject("closeModal");
        const message = useMessage();
        const store = useStore();

        const formRef = ref(null);
        const formValue = ref({
            question: {
                title: "",
                content: "",
                private: false,
            },
        });
        const rules = {
            question: {
                title: [
                    {
                        required: true,
                        message: "标题不能为空",
                        trigger: ["input", "blur"],
                    },
                ],
                content: [
                    {
                        required: true,
                        message: "内容不能为空",
                        trigger: ["input", "blur"],
                    },
                ],
            },
        };
        const addBtnDisabled = ref(false);

        const handleAddQuestion = function (e) {
            e.preventDefault();
            formRef.value?.validate((errors) => {
                if (!errors) {
                    addBtnDisabled.value = true;
                    addQuestion(formValue.value.question).then((res) => {
                        if (res.data.status == "ok") {
                            message.success(
                                "添加成功，我们回头见，问题id为 " +
                                    res.data.id +
                                    "，记得保存",
                                {
                                    closable: true,
                                    duration: 15000,
                                },
                            );
                            closeModal();
                            store.commit("updateQuestion");
                        } else {
                            message.error("添加失败，要不待会试试？");
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
            addBtnDisabled,
            handleAddQuestion,
        };
    },
};
</script>
