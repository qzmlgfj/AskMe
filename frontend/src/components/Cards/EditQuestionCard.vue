<template>
    <n-card style="width: 500px" title="修改提问" :bordered="false" size="huge" role="dialog" aria-modal="true"
        footer-style="display:flex;justify-content:space-around;" :segmented="{content: true}" closable
        @close="closeModal">
        <n-space vertical>
            <n-form :model="formValue">
                <n-form-item label="标题" path="question.title">
                    <n-input v-model:value="formValue.question.title" placeholder="输入问题标题" />
                </n-form-item>
                <n-form-item label="问题" path="question.content">
                    <n-input v-model:value="formValue.question.content" type="textarea" placeholder="输入问题内容" />
                </n-form-item>
                <n-form-item label="私密" path="question.private">
                    <n-switch v-model:value="formValue.question.private" />
                </n-form-item>
            </n-form>
        </n-space>
        <template #footer>
            <n-button type="primary" @click="handleAddQuestion">添加</n-button>
            <n-button type="default" @click="closeModal">取消</n-button>
        </template>
    </n-card>
</template>

<script>
import { ref, inject } from "vue";
import { useStore } from "vuex";

import { NCard, NSpace, NForm, NFormItem, NInput, NSwitch, NButton, useMessage } from "naive-ui";

import { addQuestion } from "@/utils/request"

export default {
    name: "ModalCard",
    components: {
        NCard,
        NSpace,
        NForm,
        NFormItem,
        NInput,
        NSwitch,
        NButton
    },
    setup() {
        const { closeModal } = inject("closeModal");
        const formValue = ref({
            question: {
                title: "",
                content: "",
                private: false,
            }
        })
        const message = useMessage();
        const store = useStore();

        const handleAddQuestion = function () {
            addQuestion(formValue.value.question).then(res => {
                if (res.data.status == "ok") {
                    message.success("添加成功");
                    closeModal();
                    store.commit("updateQuestion");
                } else {
                    message.error("添加失败");
                }
            })
        }

        return {
            closeModal,
            formValue,
            handleAddQuestion
        };
    }
};
</script>
