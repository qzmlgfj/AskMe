<template>
    <n-card style="width: 400px" title="管理员注册" :bordered="false" size="huge" role="dialog" aria-modal="true"
        footer-style="display:flex;justify-content:space-around;" :segmented="{content: true}" closable
        @close="closeModal">
        <n-space vertical>
            <n-form :model="formValue">
                <n-form-item label="用户名" path="user.userName">
                    <n-input v-model:value="formValue.user.username" placeholder="输入用户名" />
                </n-form-item>
                <n-form-item label="密码" path="user.password">
                    <n-input v-model:value="formValue.user.password" type="password" show-password-on="click"
                        placeholder="输入密码" />
                </n-form-item>
                <n-form-item label="确认密码" path="user.repassword">
                    <n-input v-model:value="formValue.user.repassword" type="password" show-password-on="click"
                        placeholder="再次输入密码" />
                </n-form-item>
            </n-form>
        </n-space>
        <template #footer>
            <n-button type="primary" @click="handleRegister">开始坐牢</n-button>
            <n-button type="default" @click="closeModal">我再等等</n-button>
        </template>
    </n-card>
</template>

<script>
import { ref, inject } from "vue";

import { NCard, NSpace, NForm, NFormItem, NInput, NButton, useMessage } from "naive-ui";

import { register } from "@/utils/request"

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
            user: {
                username: "",
                password: "",
                repassword: "",
            }
        })
        const message = useMessage();

        const handleRegister = function () {
            register(formValue.value.user).then(res => {
                console.log(res)
                if (res.data.status == "ok") {
                    message.success("注册成功");
                    closeModal();
                } else {
                    message.error("注册失败");
                }
            })
        }

        return {
            closeModal,
            formValue,
            handleRegister
        };
    }
};
</script>
