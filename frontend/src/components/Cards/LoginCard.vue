<template>
    <n-card style="width: 400px" title="管理员登录" :bordered="false" size="huge" role="dialog" aria-modal="true"
        footer-style="display:flex;justify-content:space-around;" :segmented="{content: true}" closable
        @close="closeModal">
        <n-space vertical>
            <n-form ref="formRef" :model="formValue">
                <n-form-item label="用户名" path="user.userName">
                    <n-input v-model:value="formValue.user.userName" placeholder="输入用户名" />
                </n-form-item>
                <n-form-item label="密码" path="user.password">
                    <n-input v-model:value="formValue.user.password" type="password" show-password-on="click"
                        placeholder="输入密码" />
                </n-form-item>
                <n-form-item path="user.rememberMe">
                    <n-checkbox v-model:checked="formValue.user.rememberMe">记住我</n-checkbox>
                </n-form-item>
            </n-form>
        </n-space>
        <template #footer>
            <n-button type="primary" @click="handleAddQuestion">快端上来罢</n-button>
            <n-button type="default" @click="closeModal">待会再说罢</n-button>
        </template>
    </n-card>
</template>

<script>
import { ref, inject } from "vue";
import { useStore } from "vuex";

import { NCard, NSpace, NForm, NFormItem, NInput, NCheckbox, NButton, useMessage } from "naive-ui";

import { addQuestion } from "@/utils/request"

export default {
    name: "ModalCard",
    components: {
        NCard,
        NSpace,
        NForm,
        NFormItem,
        NInput,
        NCheckbox,
        NButton
    },
    setup() {
        const { closeModal } = inject("closeModal");
        const formValue = ref({
            user: {
                userName: "",
                password: "",
                rememberMe: false,
            }
        })
        const message = useMessage();
        const store = useStore();

        const handleAddQuestion = function () {
            addQuestion(formValue.value.question).then(res => {
                console.log(res)
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
