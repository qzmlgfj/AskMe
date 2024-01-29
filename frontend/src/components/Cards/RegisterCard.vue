<template>
    <n-card style="width: 350px" title="管理员注册" :bordered="false" size="huge" role="dialog" aria-modal="true"
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
        const message = useMessage();

        const formRef = ref(null);
        const formValue = ref({
            user: {
                username: "",
                password: "",
                repassword: "",
            }
        })

        const validatePasswordSame = (rule, value) => value === formValue.value.user.password;

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
                ],
                repassword: [
                    {
                        required: true,
                        message: "请再次输入密码",
                        trigger: ["input", "blur"]
                    },
                    {
                        validator: validatePasswordSame,
                        message: "两次密码输入不一致",
                        trigger: ["input", "blur"]
                    }
                ]
            },
        };

        const handleRegister = function (e) {
            e.preventDefault();
            formRef.value?.validate((errors) => {
                if (!errors) {
                    register(formValue.value.user).then(res => {
                        if (res.data.status == "ok") {
                            message.success("注册成功");
                            closeModal();
                        } else {
                            message.error("注册失败");
                        }
                    })
                } else {
                    message.error("请检查输入");
                }
            });
        }

        return {
            closeModal,
            formRef,
            formValue,
            rules,
            handleRegister
        };
    }
};
</script>
