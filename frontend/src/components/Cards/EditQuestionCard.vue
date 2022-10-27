<template>
    <n-card style="width: 400px" title="修改提问" :bordered="false" size="huge" role="dialog" aria-modal="true"
        footer-style="display:flex;justify-content:space-around;" :segmented="{content: true}" closable
        @close="closeModal">
        <n-space vertical>
            <n-form ref="formRef" :model="formValue" :rules="rules">
                <n-form-item label="标题" path="question.title">
                    <n-input v-model:value="formValue.question.title" placeholder="输入问题标题" maxlength="15" show-count />
                </n-form-item>
                <n-form-item label="问题" path="question.content">
                    <n-input v-model:value="formValue.question.content" type="textarea" placeholder="输入问题内容"
                        maxlength="100" show-count />
                </n-form-item>
                <n-form-item label="回答" path="question.answer">
                    <n-input v-model:value="formValue.question.answer" type="textarea" placeholder="输入回答内容"
                        maxlength="100" show-count />
                </n-form-item>
                <n-space justify="space-around">
                    <n-form-item label="私密" path="question.private">
                        <n-switch v-model:value="formValue.question.private" />
                    </n-form-item>
                    <n-form-item>
                        <n-button type="error" @click="show">删除问题</n-button>
                    </n-form-item>
                </n-space>
            </n-form>
        </n-space>
        <template #footer>
            <n-button type="primary" @click="handleEditQuestion">修改</n-button>
            <n-button type="default" @click="closeModal">取消</n-button>
        </template>
        <n-modal v-model:show="showModal" preset="dialog" title="确认" content="你确认?" positive-text="确认"
            negative-text="算了" @positive-click="submitCallback" @negative-click="cancelCallback" />
    </n-card>
</template>

<script>
import { ref, inject } from "vue";
import { useStore } from "vuex";

import { NCard, NSpace, NForm, NFormItem, NInput, NSwitch, NButton, NModal, useMessage } from "naive-ui";

import { editQuestion, deleteQuestion } from "@/utils/request"
import { computed } from "@vue/reactivity";

export default {
    name: "ModalCard",
    components: {
        NCard,
        NSpace,
        NForm,
        NFormItem,
        NInput,
        NSwitch,
        NButton,
        NModal
    },
    setup() {
        const { closeModal } = inject("closeModal");
        const store = useStore();
        const message = useMessage();

        const currentQuestion = computed(() => store.state.currentQuestion);
        const showModal = ref(false);

        const formRef = ref(null);
        const formValue = ref({
            question: {
                id: currentQuestion.value.id,
                title: currentQuestion.value.title,
                content: currentQuestion.value.content,
                answer: currentQuestion.value.answer,
                private: currentQuestion.value.private,
            }
        })

        const rules = {
            question: {
                title: [
                    {
                        required: true,
                        message: "标题不能为空",
                        trigger: "blur"
                    },
                ],
                content: [
                    {
                        required: true,
                        message: "问题不能为空",
                        trigger: "blur"
                    },
                ],
                answer: [
                    {
                        required: true,
                        message: "回答不能为空",
                        trigger: "blur"
                    },
                ],
            },
        };

        const handleEditQuestion = function (e) {
            e.preventDefault();
            formRef.value?.validate((errors) => {
                if (!errors) {
                    editQuestion(formValue.value.question).then(res => {
                        if (res.data.status == "ok") {
                            message.success("修改成功");
                            closeModal();
                            store.commit("updateQuestion");
                        } else {
                            message.error("修改失败");
                        }
                    })
                } else {
                    message.error("请检查输入");
                }
            });
        }

        const handleDelete = () => {
            deleteQuestion({ id: currentQuestion.value.id }).then(res => {
                if (res.data.status == "ok") {
                    message.success("删除成功");
                    closeModal();
                    store.commit("updateQuestion");
                } else {
                    message.error("删除失败");
                }
            })
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
            closeModal,
            formRef,
            formValue,
            rules,
            handleEditQuestion,
            showModal,
            handleDelete,
            show,
            submitCallback,
            cancelCallback,
        };
    }
};
</script>
