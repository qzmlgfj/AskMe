<template>
    <n-card style="width: 400px" title="管理员登录" :bordered="false" size="huge" role="dialog" aria-modal="true"
        footer-style="display:flex;justify-content:space-around;" :segmented="{content: true}" closable
        @close="closeModal">
        <n-space vertical>
            <n-form ref="formRef" :model="formValue" :rules="rules">
                <n-form-item label="用户名" path="user.username">
                    <n-input v-model:value="formValue.user.username" placeholder="输入用户名" />
                </n-form-item>
                <n-form-item label="密码" path="user.password">
                    <n-input v-model:value="formValue.user.password" type="password" show-password-on="click"
                        placeholder="输入密码" />
                </n-form-item>
                <n-form-item path="user.rememberme">
                    <n-checkbox v-model:checked="formValue.user.remember">记住我</n-checkbox>
                </n-form-item>
            </n-form>
        </n-space>
        <template #footer>
            <n-button type="primary" @click="handleLogin">快端上来罢</n-button>
            <n-button type="default" @click="closeModal">待会再说罢</n-button>
        </template>
    </n-card>
</template>

<script>
import { ref, inject } from "vue";
import { useStore } from "vuex";

import { NCard, NSpace, NForm, NFormItem, NInput, NCheckbox, NButton, useMessage } from "naive-ui";

import { login } from "../../utils/request";

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
        const message = useMessage();
        const store = useStore();

        const formRef = ref(null);
        const formValue = ref({
            user: {
                username: "",
                password: "",
                remember: false,
            }
        })
        const rules = {
            user: {
                username: [
                    {
                        required: true,
                        message: "用户名不能为空",
                        trigger: ["input", "blur"]
                    },
                ],
                password: [
                    {
                        required: true,
                        message: "内容不能为空",
                        trigger: ["input", "blur"]
                    },
                ]
            },
        };

        const handleLogin = function () {
            login(formValue.value.user).then(res => {
                if (res.data.authenticated) {
                    message.success("登录成功");
                    store.commit("setUserName", formValue.value.user.username);
                    store.commit("setQueryMode", "unanswered");
                    store.commit("updateQuestion");
                    localStorage.setItem("userName", formValue.value.user.username);
                    localStorage.setItem("token", res.data.token);
                    closeModal();
                } else {
                    message.error("登录失败");
                }
            })
        }

        return {
            closeModal,
            formRef,
            formValue,
            rules,
            handleLogin
        };
    }
};
</script>
